# NQ CME Globex replay study — owned raw trades (2024-01-02 / 2024-01-03)

**Gate (WORK_REGISTER 2026-08-18):** attach the existing NQ provenance manifest and the
`cme_globex_equity_index` venue rule to a real replay result.

## Result

- Provenance gate: **REPLAY_GATE_PASS** (SHA-256 `547d5ab92e7673e3…`, 8,842,273 bytes)
- Accepted events: 374,387 (source rows 377,859)
- Exact duplicate events removed: 3,472 — repeated sequence rows (not deduplicated): 27,968
- Out-of-order rows: 0 · unknown-side rows: 1
- Maintenance-break rows rejected: 0
- **Bars (1-min, non-synthetic): 1,380** · sessions: 2 · bars/session: {'2024-01-01': 1320, '2024-01-02': 60}
- Session dates: 2024-01-01, 2024-01-02
- Bar range: 2024-01-02 00:00:00+00:00 → 2024-01-02 23:59:00+00:00 UTC
- Price range: 16622.5 – 17038.5 · total volume 629,405 · total trades 374,387

## Session rule applied

- Venue rule: `cme_globex_equity_index` — 17:00 America/Chicago DST-aware boundary; maintenance break 16:00–17:00 Chicago rejected.
- Regular CME Globex equity-index session boundary only; excludes holidays, early closes, product-specific halts and contract rolls.
- Quote features: `not_available` (no bid/ask columns in this source).

## Scope boundary

This is a data-quality replay, not a fill simulator and not a strategy result. It records
deterministic, source-aware bar construction with a fail-closed provenance gate. Holiday,
early-close, product-halt, contract-roll mapping, executable bid/ask fills, queue position,
latency, slippage and commissions remain explicitly unimplemented.
