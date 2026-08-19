"""Attach the owned-NQ provenance manifest and CME Globex session rules to a real replay.

God-Mode gate (WORK_REGISTER 2026-08-18): "attach the existing NQ provenance
manifest and this CME rule to a replay result" before any candidate strategy
backtest. Fail-closed provenance + venue validation only; no executable fill,
queue, latency, roll, holiday, or alpha claims are made here.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from market_data_engine import TradeBarProcessor, validate_source_file_provenance  # noqa: E402

STUDY_DIR = Path(__file__).resolve().parent / "studies" / "data_quality"
MANIFEST = STUDY_DIR / "nq_trades_2024-01-02_2024-01-03.provenance.json"
OUTPUT_JSON = STUDY_DIR / "nq_cme_globex_replay_2024-01-02_2024-01-03.json"
OUTPUT_REPORT = STUDY_DIR / "nq_cme_globex_replay_2024-01-02_2024-01-03_REPORT.md"


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    # 1) Fail-closed provenance gate against the separately recorded manifest.
    gate = validate_source_file_provenance(manifest["source_file"], manifest)

    # 2) Replay with the DST-aware CME Globex equity-index session rule.
    events = pd.read_parquet(manifest["source_file"])
    processor = TradeBarProcessor(
        symbol="NQ",
        source="owned-nq-trades",
        timeframe="1min",
        venue_session_rules="cme_globex_equity_index",
    )
    result = processor.build_bars(events)
    bars = result.bars

    bars_per_session = {
        str(key): int(value)
        for key, value in bars["session_date"].value_counts().sort_index().items()
    }
    study = {
        "study": "nq_cme_globex_replay",
        "recorded_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_file": manifest["source_file"],
        "gate": {
            "validator": "research.market_data_engine.validate_source_file_provenance",
            "result": "REPLAY_GATE_PASS",
            "sha256": gate["sha256"],
            "byte_count": gate["byte_count"],
            "symbol": gate["symbol"],
            "manifest": MANIFEST.name,
        },
        "quality": result.quality,
        "provenance": result.provenance,
        "bars_summary": {
            "bar_count": int(len(bars)),
            "session_count": result.quality["session_count"],
            "session_dates": [str(d) for d in sorted(bars["session_date"].unique())],
            "bars_per_session": bars_per_session,
            "first_bar_ts": str(bars.index.min()),
            "last_bar_ts": str(bars.index.max()),
            "min_low": float(bars["low"].min()),
            "max_high": float(bars["high"].max()),
            "total_volume": int(bars["volume"].sum()),
            "total_trade_count": int(bars["trade_count"].sum()),
            "columns": list(bars.columns),
        },
    }

    OUTPUT_JSON.write_text(
        json.dumps(study, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    OUTPUT_REPORT.write_text(_render_report(study), encoding="utf-8")

    print(
        f"STUDY_OK gate=REPLAY_GATE_PASS accepted={result.quality['accepted_row_count']} "
        f"bars={study['bars_summary']['bar_count']} "
        f"sessions={study['bars_summary']['session_count']} "
        f"sha256={gate['sha256'][:12]}"
    )
    return 0


def _render_report(study: dict) -> str:
    s = study["bars_summary"]
    q = study["quality"]
    return f"""# NQ CME Globex replay study — owned raw trades (2024-01-02 / 2024-01-03)

**Gate (WORK_REGISTER 2026-08-18):** attach the existing NQ provenance manifest and the
`cme_globex_equity_index` venue rule to a real replay result.

## Result

- Provenance gate: **REPLAY_GATE_PASS** (SHA-256 `{study['gate']['sha256'][:16]}…`, {study['gate']['byte_count']:,} bytes)
- Accepted events: {q['accepted_row_count']:,} (source rows {q['row_count']:,})
- Exact duplicate events removed: {q['duplicate_event_rows']:,} — repeated sequence rows (not deduplicated): {q['duplicate_sequence_rows']:,}
- Out-of-order rows: {q['out_of_order_rows']:,} · unknown-side rows: {q['unknown_side_rows']:,}
- Maintenance-break rows rejected: {q['venue_maintenance_break_rows']:,}
- **Bars (1-min, non-synthetic): {s['bar_count']:,}** · sessions: {s['session_count']} · bars/session: {s['bars_per_session']}
- Session dates: {", ".join(s['session_dates'])}
- Bar range: {s['first_bar_ts']} → {s['last_bar_ts']} UTC
- Price range: {s['min_low']} – {s['max_high']} · total volume {s['total_volume']:,} · total trades {s['total_trade_count']:,}

## Session rule applied

- Venue rule: `cme_globex_equity_index` — 17:00 America/Chicago DST-aware boundary; maintenance break 16:00–17:00 Chicago rejected.
- {study['provenance']['venue_rules_limit']}
- Quote features: `{study['provenance']['quote_features']}` (no bid/ask columns in this source).

## Scope boundary

This is a data-quality replay, not a fill simulator and not a strategy result. It records
deterministic, source-aware bar construction with a fail-closed provenance gate. Holiday,
early-close, product-halt, contract-roll mapping, executable bid/ask fills, queue position,
latency, slippage and commissions remain explicitly unimplemented.
"""


if __name__ == "__main__":
    raise SystemExit(main())
