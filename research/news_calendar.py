"""Source-validated economic-event calendar with look-ahead-safe features.

It separates facts available at an event timestamp from retrospective event
studies. A post-release return is an outcome label only and is never emitted as
a tradable feature.
"""
from __future__ import annotations

from typing import Iterable

import pandas as pd


class EconomicNewsCalendar:
    REQUIRED_COLUMNS = (
        "event_id",
        "release_time_utc",
        "available_at_utc",
        "event_name",
        "category",
        "source",
        "source_url",
        "importance",
    )

    def __init__(self, events: pd.DataFrame) -> None:
        missing = [column for column in self.REQUIRED_COLUMNS if column not in events.columns]
        if missing:
            raise ValueError(f"missing required calendar columns: {', '.join(missing)}")
        if events["event_id"].duplicated().any():
            raise ValueError("event_id must be unique")
        self.events = events.copy()
        for column in ("release_time_utc", "available_at_utc"):
            values = self.events[column]
            if not isinstance(values.dtype, pd.DatetimeTZDtype):
                raise ValueError(f"{column} must be timezone-aware UTC timestamps")
            self.events[column] = values.dt.tz_convert("UTC")
        if (self.events["available_at_utc"] < self.events["release_time_utc"]).any():
            raise ValueError("available_at_utc cannot precede release_time_utc")
        if (self.events["source_url"].astype(str).str.len() == 0).any():
            raise ValueError("source_url is required for each event")
        self.events = self.events.sort_values("available_at_utc", kind="mergesort").reset_index(drop=True)

    @staticmethod
    def _bar_times(bars: pd.DataFrame) -> pd.DatetimeIndex:
        if not isinstance(bars.index, pd.DatetimeIndex) or bars.index.tz is None:
            raise ValueError("bars must use a timezone-aware UTC DatetimeIndex")
        return bars.index.tz_convert("UTC")

    def known_event_features(self, bars: pd.DataFrame) -> pd.DataFrame:
        """Return features built only from events available by each bar start."""
        timestamps = self._bar_times(bars)
        previous_timestamp: pd.Timestamp | None = None
        rows: list[dict[str, float | int | None]] = []
        for timestamp in timestamps:
            known = self.events[self.events["available_at_utc"] <= timestamp]
            released_now = known if previous_timestamp is None else known[known["available_at_utc"] > previous_timestamp]
            last_time = known["available_at_utc"].max() if not known.empty else None
            rows.append(
                {
                    "high_impact_event_now": int((released_now["importance"] == "high").sum()),
                    "event_count_now": int(len(released_now)),
                    "minutes_since_last_event": None if last_time is None else (timestamp - last_time).total_seconds() / 60.0,
                }
            )
            previous_timestamp = timestamp
        return pd.DataFrame(rows, index=bars.index)

    def event_study(self, bars: pd.DataFrame, post_minutes: int, event_ids: Iterable[str] | None = None) -> pd.DataFrame:
        """Create retrospective, explicitly non-signal post-release outcome labels."""
        if post_minutes <= 0:
            raise ValueError("post_minutes must be positive")
        timestamps = self._bar_times(bars)
        if "close" not in bars.columns:
            raise ValueError("bars require a close column")
        selected = self.events if event_ids is None else self.events[self.events["event_id"].isin(list(event_ids))]
        rows: list[dict[str, object]] = []
        for event in selected.itertuples(index=False):
            before = bars.loc[timestamps < event.release_time_utc, "close"]
            after = bars.loc[timestamps <= event.release_time_utc + pd.Timedelta(minutes=post_minutes), "close"]
            if before.empty or after.empty:
                continue
            baseline = float(before.iloc[-1])
            post = float(after.iloc[-1])
            rows.append(
                {
                    "event_id": event.event_id,
                    "release_time_utc": event.release_time_utc,
                    "event_name": event.event_name,
                    "category": event.category,
                    "importance": event.importance,
                    "baseline_close": baseline,
                    "post_close": post,
                    "post_return_bps": round((post / baseline - 1.0) * 10_000, 10),
                    "post_minutes": post_minutes,
                    "analysis_label": "post_release_outcome_not_a_signal",
                }
            )
        return pd.DataFrame(rows)
