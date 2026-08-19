"""Deterministic processing of source-sided trade events into research bars.

This module deliberately does not invent prices for intervals without trades.
It records data-quality counters so downstream research can exclude or inspect
imperfect source slices instead of silently treating them as clean data.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping

import pandas as pd


_REQUIRED_SOURCE_METADATA = (
    "schema_version",
    "source",
    "dataset_id",
    "symbol",
    "expected_sha256",
)


def validate_source_file_provenance(
    source_file: str | Path, source_metadata: Mapping[str, Any]
) -> dict[str, Any]:
    """Validate immutable source identity before it enters a replay run.

    The caller supplies a SHA-256 recorded outside the processing result.  This
    prevents a changed, truncated, or mislabelled local file from silently
    inheriting a prior run's provenance.
    """
    missing = [key for key in _REQUIRED_SOURCE_METADATA if not source_metadata.get(key)]
    if missing:
        raise ValueError(f"missing required source metadata: {', '.join(missing)}")
    if source_metadata["schema_version"] != "1.0":
        raise ValueError("unsupported source metadata schema_version")

    expected_sha256 = str(source_metadata["expected_sha256"]).lower()
    if len(expected_sha256) != 64 or any(char not in "0123456789abcdef" for char in expected_sha256):
        raise ValueError("expected_sha256 must be a lowercase SHA-256 hex digest")

    path = Path(source_file)
    if not path.is_file():
        raise ValueError("source file does not exist or is not a regular file")

    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    actual_sha256 = digest.hexdigest()
    if actual_sha256 != expected_sha256:
        raise ValueError("checksum mismatch for source file")

    return {
        "schema_version": source_metadata["schema_version"],
        "source": str(source_metadata["source"]),
        "dataset_id": str(source_metadata["dataset_id"]),
        "symbol": str(source_metadata["symbol"]).upper(),
        "file_name": path.name,
        "byte_count": path.stat().st_size,
        "sha256": actual_sha256,
        "checksum_verified": True,
    }


@dataclass(frozen=True)
class ProcessedTradeBars:
    """Canonical bars with explicit provenance and quality metadata."""

    bars: pd.DataFrame
    quality: dict[str, Any]
    provenance: dict[str, Any]


@dataclass(frozen=True)
class ExecutionAssumptions:
    """Declared cost assumptions without pretending OHLCV bars prove fills."""

    fill_model: str
    executable_fills: bool
    commission_per_contract_per_side: float
    assumed_slippage_ticks_per_side: float
    costs_are_calibrated: bool = False
    limitations: str = (
        "Reference-price assumptions only; not executable fills. Excludes bid/ask path, "
        "queue position, partial-fill probability, market impact, latency, and order priority."
    )

    def __post_init__(self) -> None:
        if self.fill_model != "bar_reference_only":
            raise ValueError("only bar_reference_only fill_model is supported")
        if self.executable_fills:
            raise ValueError("bar_reference_only assumptions cannot claim executable fills")
        if self.commission_per_contract_per_side < 0:
            raise ValueError("commission_per_contract_per_side must be non-negative")
        if self.assumed_slippage_ticks_per_side < 0:
            raise ValueError("assumed_slippage_ticks_per_side must be non-negative")

    @classmethod
    def bar_reference_only(
        cls, commission_per_contract_per_side: float, assumed_slippage_ticks_per_side: float
    ) -> "ExecutionAssumptions":
        return cls(
            fill_model="bar_reference_only",
            executable_fills=False,
            commission_per_contract_per_side=float(commission_per_contract_per_side),
            assumed_slippage_ticks_per_side=float(assumed_slippage_ticks_per_side),
        )

    def to_provenance(self) -> dict[str, Any]:
        return {
            "fill_model": self.fill_model,
            "executable_fills": self.executable_fills,
            "commission_per_contract_per_side": self.commission_per_contract_per_side,
            "assumed_slippage_ticks_per_side": self.assumed_slippage_ticks_per_side,
            "costs_are_calibrated": self.costs_are_calibrated,
            "limitations": self.limitations,
        }


class TradeBarProcessor:
    """Convert individual trades to timestamped OHLCV and source-side features.

    ``B`` and ``A`` are retained as source-provided classifications. The signed
    volume mapping is descriptive only; it is not labelled as executable order
    flow or a prediction signal.
    """

    REQUIRED_COLUMNS = ("ts_event", "price", "size", "side")
    QUOTE_PRICE_COLUMNS = ("bid_price", "ask_price")
    QUOTE_SIZE_COLUMNS = ("bid_size", "ask_size")
    SIDE_MAPPING = {"B": 1, "A": -1}

    def __init__(
        self,
        symbol: str,
        source: str,
        timeframe: str = "1min",
        session_start_utc: str = "00:00",
        venue_session_rules: str | None = None,
    ) -> None:
        try:
            parsed_session_start = pd.to_datetime(session_start_utc, format="%H:%M")
        except (TypeError, ValueError) as error:
            raise ValueError("session_start_utc must use HH:MM in UTC") from error
        normalized_rules = venue_session_rules.lower() if venue_session_rules else None
        if normalized_rules not in (None, "cme_globex_equity_index"):
            raise ValueError("unsupported venue_session_rules")
        try:
            self._bar_interval = pd.Timedelta(timeframe)
        except ValueError as error:
            raise ValueError("timeframe must be a fixed-duration pandas interval") from error
        if self._bar_interval <= pd.Timedelta(0):
            raise ValueError("timeframe must be positive")
        self.symbol = symbol.upper()
        self.source = source
        self.timeframe = timeframe
        self.session_start_utc = parsed_session_start.strftime("%H:%M")
        self.venue_session_rules = normalized_rules
        self._session_offset = pd.Timedelta(
            hours=parsed_session_start.hour, minutes=parsed_session_start.minute
        )

    def _apply_venue_session_rules(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Attach DST-aware CME Globex labels and reject planned maintenance data."""
        if self.venue_session_rules is None:
            frame["_bar_timestamp"] = frame["ts_event"]
            frame["_session_date"] = (frame["ts_event"] - self._session_offset).dt.date
            return frame

        local = frame["ts_event"].dt.tz_convert("America/Chicago")
        local_minutes = local.dt.hour * 60 + local.dt.minute
        in_maintenance_break = (local_minutes >= 16 * 60) & (local_minutes < 17 * 60)
        if in_maintenance_break.any():
            raise ValueError("source event falls within venue maintenance break")

        session_start_day = local.dt.normalize().where(
            local.dt.hour >= 17, local.dt.normalize() - pd.Timedelta(days=1)
        )
        session_start = session_start_day + pd.Timedelta(hours=17)
        elapsed = local - session_start
        bar_offset = (elapsed // self._bar_interval) * self._bar_interval
        frame["_bar_timestamp"] = (session_start + bar_offset).dt.tz_convert("UTC")
        frame["_session_date"] = session_start_day.dt.date
        return frame

    def build_bars(self, events: pd.DataFrame) -> ProcessedTradeBars:
        missing = [name for name in self.REQUIRED_COLUMNS if name not in events.columns]
        if missing:
            raise ValueError(f"missing required trade columns: {', '.join(missing)}")

        frame = events.copy()
        original_rows = len(frame)
        frame["ts_event"] = pd.to_datetime(frame["ts_event"], utc=True, errors="raise")
        frame["price"] = pd.to_numeric(frame["price"], errors="raise")
        frame["size"] = pd.to_numeric(frame["size"], errors="raise")
        if (frame["price"] <= 0).any():
            raise ValueError("trade price must be positive")
        if (frame["size"] <= 0).any():
            raise ValueError("trade size must be positive")

        quote_price_columns_present = [
            name for name in self.QUOTE_PRICE_COLUMNS if name in frame.columns
        ]
        quote_size_columns_present = [
            name for name in self.QUOTE_SIZE_COLUMNS if name in frame.columns
        ]
        if quote_price_columns_present and len(quote_price_columns_present) != len(self.QUOTE_PRICE_COLUMNS):
            raise ValueError("bid_price and ask_price must be supplied together")
        if quote_size_columns_present and len(quote_size_columns_present) != len(self.QUOTE_SIZE_COLUMNS):
            raise ValueError("bid_size and ask_size must be supplied together")
        has_quote_prices = len(quote_price_columns_present) == len(self.QUOTE_PRICE_COLUMNS)
        has_quote_sizes = len(quote_size_columns_present) == len(self.QUOTE_SIZE_COLUMNS)
        if has_quote_sizes and not has_quote_prices:
            raise ValueError("bid_size and ask_size require bid_price and ask_price")
        if has_quote_prices:
            for name in self.QUOTE_PRICE_COLUMNS:
                frame[name] = pd.to_numeric(frame[name], errors="raise")
                if (frame[name] <= 0).any():
                    raise ValueError(f"{name} must be positive")
            if (frame["ask_price"] < frame["bid_price"]).any():
                raise ValueError("ask_price must be greater than or equal to bid_price")
            frame["quoted_spread"] = frame["ask_price"] - frame["bid_price"]
            frame["midpoint"] = (frame["ask_price"] + frame["bid_price"]) / 2
        if has_quote_sizes:
            for name in self.QUOTE_SIZE_COLUMNS:
                frame[name] = pd.to_numeric(frame[name], errors="raise")
                if (frame[name] <= 0).any():
                    raise ValueError(f"{name} must be positive")
            quote_depth = frame["bid_size"] + frame["ask_size"]
            frame["microprice"] = (
                frame["ask_price"] * frame["bid_size"]
                + frame["bid_price"] * frame["ask_size"]
            ) / quote_depth
            frame["quote_imbalance"] = (frame["bid_size"] - frame["ask_size"]) / quote_depth

        out_of_order_rows = int((frame["ts_event"].diff().dt.total_seconds() < 0).sum())
        duplicate_sequence_rows = 0
        duplicate_event_rows = 0
        if "sequence" in frame.columns:
            sequence_present = frame["sequence"].notna()
            duplicate_sequence_rows = int(frame.loc[sequence_present].duplicated(subset=["sequence"]).sum())
            # A provider sequence is not a globally unique trade identifier:
            # real NQ data can reuse it for distinct prints at the same instant.
            # Drop only exact source-event duplicates, retaining distinct prints.
            event_identity = ["ts_event", "sequence", "price", "size", "side"]
            event_identity.extend(name for name in ("instrument_id", "symbol") if name in frame.columns)
            duplicate_event_rows = int(frame.duplicated(subset=event_identity).sum())
            frame = frame.drop_duplicates(subset=event_identity, keep="first")

        frame = frame.sort_values("ts_event", kind="mergesort")
        frame = self._apply_venue_session_rules(frame)
        frame["side"] = frame["side"].astype(str).str.upper()
        frame["side_sign"] = frame["side"].map(self.SIDE_MAPPING).fillna(0).astype(int)
        frame["buy_volume"] = frame["size"].where(frame["side_sign"] == 1, 0.0)
        frame["sell_volume"] = frame["size"].where(frame["side_sign"] == -1, 0.0)
        frame["unknown_side_volume"] = frame["size"].where(frame["side_sign"] == 0, 0.0)
        frame["signed_volume"] = frame["size"] * frame["side_sign"]

        if self.venue_session_rules:
            grouped = frame.groupby("_bar_timestamp", observed=True)
        else:
            grouped = frame.groupby(
                pd.Grouper(
                    key="ts_event",
                    freq=self.timeframe,
                    label="left",
                    closed="left",
                    origin="start_day",
                    offset=self._session_offset,
                ),
                observed=True,
            )
        bars = grouped.agg(
            open=("price", "first"),
            high=("price", "max"),
            low=("price", "min"),
            close=("price", "last"),
            volume=("size", "sum"),
            trade_count=("size", "count"),
            buy_volume=("buy_volume", "sum"),
            sell_volume=("sell_volume", "sum"),
            unknown_side_volume=("unknown_side_volume", "sum"),
            signed_volume=("signed_volume", "sum"),
        )
        if has_quote_prices:
            quote_bars = grouped.agg(
                close_bid_price=("bid_price", "last"),
                close_ask_price=("ask_price", "last"),
                close_quoted_spread=("quoted_spread", "last"),
                close_midpoint=("midpoint", "last"),
                quote_rows=("bid_price", "count"),
            )
            bars = bars.join(quote_bars)
        if has_quote_sizes:
            size_quote_bars = grouped.agg(
                close_microprice=("microprice", "last"),
                close_quote_imbalance=("quote_imbalance", "last"),
            )
            bars = bars.join(size_quote_bars)
        # Pandas time grouping materializes empty time buckets. They are not
        # executable observations and must never become synthetic price bars.
        bars = bars.loc[bars["trade_count"] > 0].copy()
        bars["imbalance"] = bars["signed_volume"] / bars["volume"]
        bars["session_date"] = grouped["_session_date"].first().reindex(bars.index)
        bars.index.name = "ts_event"

        quality = {
            "row_count": original_rows,
            "accepted_row_count": len(frame),
            "duplicate_sequence_rows": duplicate_sequence_rows,
            "duplicate_event_rows": duplicate_event_rows,
            "out_of_order_rows": out_of_order_rows,
            "unknown_side_rows": int((frame["side_sign"] == 0).sum()),
            "empty_bars_synthesized": 0,
            "session_count": int(bars["session_date"].nunique()),
            "timestamp_timezone": "UTC",
            "venue_maintenance_break_rows": 0,
            "quote_rows": int(frame["bid_price"].notna().sum()) if has_quote_prices else 0,
        }
        provenance = {
            "symbol": self.symbol,
            "source": self.source,
            "timeframe": self.timeframe,
            "session_start_utc": self.session_start_utc,
            "venue_session_rules": self.venue_session_rules or "none",
            "venue_timezone": "America/Chicago" if self.venue_session_rules else None,
            "maintenance_break_local": "16:00-17:00" if self.venue_session_rules else None,
            "venue_rules_limit": (
                "Regular CME Globex equity-index session boundary only; excludes holidays, early closes, product-specific halts and contract rolls."
                if self.venue_session_rules
                else "No venue-specific calendar rules applied."
            ),
            "side_mapping": self.SIDE_MAPPING.copy(),
            "side_mapping_note": "Source-provided B/A classifications; not asserted to be executable aggressor flow.",
            "quote_features": (
                "bid_ask_prices_and_sizes"
                if has_quote_sizes
                else "bid_ask_prices"
                if has_quote_prices
                else "not_available"
            ),
        }
        return ProcessedTradeBars(bars=bars, quality=quality, provenance=provenance)
