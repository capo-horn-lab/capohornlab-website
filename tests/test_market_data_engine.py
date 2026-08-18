"""Tests for the deterministic, source-aware market-data processing engine."""
from __future__ import annotations

import pandas as pd
import pytest


def test_trade_processor_aggregates_source_sided_events_without_filling_empty_bars():
    from research.market_data_engine import TradeBarProcessor

    events = pd.DataFrame(
        {
            "ts_event": pd.to_datetime(
                [
                    "2024-01-02T14:30:05Z",
                    "2024-01-02T14:30:15Z",
                    "2024-01-02T14:32:05Z",
                ],
                utc=True,
            ),
            "price": [17000.00, 17000.25, 17001.00],
            "size": [2, 3, 4],
            "side": ["B", "A", "B"],
            "sequence": [10, 11, 12],
        }
    )

    result = TradeBarProcessor(symbol="NQ", source="owned-nq-trades").build_bars(events)

    assert list(result.bars.index.strftime("%H:%M")) == ["14:30", "14:32"]
    first = result.bars.iloc[0]
    assert first.open == 17000.00
    assert first.high == 17000.25
    assert first.low == 17000.00
    assert first.close == 17000.25
    assert first.volume == 5
    assert first.buy_volume == 2
    assert first.sell_volume == 3
    assert first.signed_volume == -1
    assert first.imbalance == pytest.approx(-0.2)
    assert result.quality["row_count"] == 3
    assert result.quality["empty_bars_synthesized"] == 0
    assert result.provenance["symbol"] == "NQ"
    assert result.provenance["side_mapping"] == {"B": 1, "A": -1}


def test_trade_processor_anchors_bars_to_explicit_utc_session_start():
    from research.market_data_engine import TradeBarProcessor

    events = pd.DataFrame(
        {
            "ts_event": pd.to_datetime(
                ["2024-01-02T23:02:10Z", "2024-01-02T23:06:00Z", "2024-01-03T00:01:00Z"],
                utc=True,
            ),
            "price": [17000.0, 17000.25, 17000.5],
            "size": [2, 3, 4],
            "side": ["B", "A", "B"],
        }
    )

    result = TradeBarProcessor(
        symbol="NQ", source="fixture", timeframe="5min", session_start_utc="23:02"
    ).build_bars(events)

    assert list(result.bars.index.strftime("%Y-%m-%dT%H:%MZ")) == [
        "2024-01-02T23:02Z",
        "2024-01-02T23:57Z",
    ]
    assert list(result.bars["session_date"].astype(str)) == ["2024-01-02", "2024-01-02"]
    assert result.quality["session_count"] == 1
    assert result.provenance["session_start_utc"] == "23:02"


def test_trade_processor_keeps_distinct_events_that_share_a_source_sequence():
    from research.market_data_engine import TradeBarProcessor

    events = pd.DataFrame(
        {
            "ts_event": pd.to_datetime(["2024-01-02T14:30:10Z", "2024-01-02T14:30:10Z"], utc=True),
            "price": [17000.0, 17000.25],
            "size": [2, 3],
            "side": ["B", "B"],
            "sequence": [42, 42],
        }
    )

    result = TradeBarProcessor(symbol="NQ", source="fixture").build_bars(events)

    assert result.quality["duplicate_sequence_rows"] == 1
    assert result.quality["accepted_row_count"] == 2
    assert result.bars.iloc[0].volume == 5


def test_trade_processor_reports_and_removes_duplicate_sequence_events():
    from research.market_data_engine import TradeBarProcessor

    events = pd.DataFrame(
        {
            "ts_event": pd.to_datetime(["2024-01-02T14:30:10Z", "2024-01-02T14:30:10Z"], utc=True),
            "price": [17000.0, 17000.0],
            "size": [2, 2],
            "side": ["B", "B"],
            "sequence": [42, 42],
        }
    )

    result = TradeBarProcessor(symbol="NQ", source="fixture").build_bars(events)

    assert result.quality["duplicate_sequence_rows"] == 1
    assert result.quality["accepted_row_count"] == 1
    assert result.bars.iloc[0].volume == 2


def test_source_file_provenance_requires_matching_checksum_and_complete_metadata(tmp_path):
    from research.market_data_engine import validate_source_file_provenance

    source_file = tmp_path / "NQ_trades_2024-01-02.parquet"
    source_file.write_bytes(b"deterministic-owned-market-data-fixture")

    metadata = {
        "schema_version": "1.0",
        "source": "owned-nq-trades",
        "dataset_id": "NQ-trades-2024-01-02",
        "symbol": "NQ",
        "expected_sha256": "63c23ee00e5c939037e5c35098f2cf9fa83956bc269f4efb723459d4038878d6",
    }

    provenance = validate_source_file_provenance(source_file, metadata)

    assert provenance["file_name"] == "NQ_trades_2024-01-02.parquet"
    assert provenance["byte_count"] == 39
    assert provenance["sha256"] == metadata["expected_sha256"]
    assert provenance["source"] == "owned-nq-trades"
    assert provenance["symbol"] == "NQ"

    with pytest.raises(ValueError, match="checksum mismatch"):
        validate_source_file_provenance(source_file, {**metadata, "expected_sha256": "0" * 64})

    with pytest.raises(ValueError, match="missing required source metadata"):
        validate_source_file_provenance(source_file, {"source": "owned-nq-trades"})


def test_trade_processor_emits_explicit_quote_features_when_bid_ask_data_is_supplied():
    from research.market_data_engine import TradeBarProcessor

    events = pd.DataFrame(
        {
            "ts_event": pd.to_datetime(
                ["2024-01-02T14:30:05Z", "2024-01-02T14:30:25Z"], utc=True
            ),
            "price": [17000.00, 17000.25],
            "size": [2, 3],
            "side": ["B", "A"],
            "bid_price": [16999.75, 17000.00],
            "ask_price": [17000.25, 17000.50],
            "bid_size": [4, 6],
            "ask_size": [2, 2],
        }
    )

    result = TradeBarProcessor(symbol="NQ", source="fixture").build_bars(events)

    bar = result.bars.iloc[0]
    assert bar.close_bid_price == 17000.00
    assert bar.close_ask_price == 17000.50
    assert bar.close_quoted_spread == pytest.approx(0.5)
    assert bar.close_midpoint == pytest.approx(17000.25)
    assert bar.close_microprice == pytest.approx(17000.375)
    assert bar.close_quote_imbalance == pytest.approx(0.5)
    assert result.quality["quote_rows"] == 2
    assert result.provenance["quote_features"] == "bid_ask_prices_and_sizes"

    with pytest.raises(ValueError, match="ask_price must be greater than or equal to bid_price"):
        TradeBarProcessor(symbol="NQ", source="fixture").build_bars(
            events.assign(ask_price=[16999.50, 17000.50])
        )


def test_cme_globex_equity_index_rules_anchor_in_chicago_time_and_reject_maintenance_break():
    from research.market_data_engine import TradeBarProcessor

    events = pd.DataFrame(
        {
            "ts_event": pd.to_datetime(
                ["2024-01-02T23:01:00Z", "2024-06-03T22:01:00Z"], utc=True
            ),
            "price": [17000.0, 18000.0],
            "size": [2, 3],
            "side": ["B", "A"],
        }
    )

    result = TradeBarProcessor(
        symbol="NQ", source="fixture", venue_session_rules="cme_globex_equity_index"
    ).build_bars(events)

    assert list(result.bars["session_date"].astype(str)) == ["2024-01-02", "2024-06-03"]
    assert result.provenance["venue_session_rules"] == "cme_globex_equity_index"
    assert result.provenance["venue_timezone"] == "America/Chicago"
    assert result.provenance["maintenance_break_local"] == "16:00-17:00"
    assert result.quality["venue_maintenance_break_rows"] == 0

    maintenance_break = events.iloc[[0]].assign(ts_event=pd.to_datetime(["2024-01-02T22:30:00Z"], utc=True))
    with pytest.raises(ValueError, match="venue maintenance break"):
        TradeBarProcessor(
            symbol="NQ", source="fixture", venue_session_rules="cme_globex_equity_index"
        ).build_bars(maintenance_break)
