# Capo Horn Lab Website — Work Register

**Updated:** 2026-08-18
**Scope:** Continue local implementation, verify production readiness, and prioritize evidence-based strategy research compatible with owned market data.

## Active workstreams

| Workstream | Owner | Status | Acceptance gate |
|---|---|---:|---|
| Local website / backend / test audit | Camilla (Atlas delegation failed: provider HTTP 401) | Verified locally | Docker stack healthy; Alembic `0004`; 26 tests passing; external go-live gates remain |
| Data inventory / backtest feasibility | Camilla (Midas delegation failed: provider HTTP 401) | Verified locally | ES 2020–2024 1m, NQ 2023–2024 1m, CL MBP-1 2024–2025; engine lists four strategies |
| Academic/web candidate research | Camilla | Completed — research backlog | Cited Top-10 candidate backlog stored under `research/` |
| Final synthesis and implementation backlog | Camilla | In progress | Select candidate #1 research protocol, then build/test one strategy at a time |
| NQ RTH first-30→last-30 exploratory screen | Camilla (Midas delegation blocked: provider HTTP 401) | **Negative / do not promote** | Reproducible 2023 IS / 2024 OOS screen completed on owned NQ 1-minute OHLCV; OOS gross mean = -1.669 bps/day before any costs |
| NQ directional shuffled-sign control | Camilla | **Negative / verified** | Deterministic 10,000-permutation benchmark on the frozen source screen; OOS two-sided p = 0.3449 and observed mean = -1.669 bps/day; research control only |

## Cycle log — 2026-08-18 (God Mode, local only)

- **Objective completed:** hardened the active NQ RTH exploratory screen with a frozen 2023 IS / 2024 OOS split. The first-30-minute-range terciles are fitted exclusively on 2023 (47.06 / 65.49 bps cuts) and applied unchanged to 2024.
- **Evidence:** `research/nq_session_study.py`; `research/studies/nq_rth_2023_2024/summary.json`; `research/studies/nq_rth_2023_2024/REPORT.md`; `daily_observations.csv`; `conditions.csv`; two PNG charts in the same directory.
- **Verified outcome:** 489 complete RTH days (IS 2023 = 244; OOS 2024 = 245). The gross directional screen is negative in IS (-1.388 bps/day) and OOS (-1.669 bps/day); OOS positive-day rate 44.5%, correlation -0.0227. This candidate is **not promotable** and must not be used as a public performance claim or trading rule.
- **Method limits:** owned 1-minute OHLCV only; it cannot establish order-book imbalance, bid/ask fills, latency, roll handling, commissions, or slippage. The study remains descriptive, not cost-adjusted and not a promised edge.
- **Specialist protocol:** `chl-20260818-0001` was saved and dispatched to Midas; the configured delegation provider returned HTTP 401 before work began. Failed result + verification log archived under `D:/CapoHornLab/contracts/envelopes/` and `logs/`.
- **Verification command:** `D:/CapoHornLab/projects/capohornlab-website/.venv/Scripts/python.exe C:/Users/farne/AppData/Local/Temp/chl_verify_nq_is_oos.py` returned `VERIFY_PASS rows=489 IS=244 OOS=245 conditions=6 OOS_gross_mean_bps=-1.668729` (temp verifier removed after run). Script execution plus `py_compile` also passed.
- **Next gate:** retain this negative result; inspect a separately pre-registered NQ hypothesis that does not reuse this signal. Restore a valid delegation credential before assigning specialist analysis.

### Permutation-control update — 2026-08-18

- **Objective completed:** added a deterministic shuffled-sign benchmark to falsify the active NQ first-30-minute-direction → final-30-minute descriptive screen, with no parameter fitting on 2024.
- **Method/formula:** per sample, `mean(sign(first30_return) × last30_return) × 10,000`; retain final-30-minute returns and permute observed first-30-minute signs across days without replacement. PCG64 seed `20260818`, 10,000 permutations, two-sided Monte-Carlo p-value `(1 + count(|null| >= |observed|)) / 10,001`.
- **Evidence/artifacts:** `research/nq_permutation_benchmark.py`; `research/studies/nq_rth_permutation_2023_2024/REPORT.md`; `summary.json`; `permutation_summary.csv`; `nq_directional_permutation_null.png`.
- **Verified outcome:** IS: -1.388 gross bps/day, p=0.3980, z=-0.906; OOS: -1.669 gross bps/day, p=0.3449, z=-0.982. The OOS result remains negative and statistically indistinguishable from the shuffled-sign control; it is **not promotable**.
- **Method limits:** gross one-minute-OHLCV screen only; no order-book data, executable bid/ask fills, commission, slippage, impact, latency, roll handling, or causal/strategy validation.
- **Verification command:** `.venv/Scripts/python.exe -m py_compile research/nq_permutation_benchmark.py && .venv/Scripts/python.exe research/nq_permutation_benchmark.py` completed (exit 0). Independent readback verifier returned `VERIFY_PASS samples=2` and confirmed both source-derived observed means plus a 75,256-byte chart.

## Market-data engine and news-calendar build — 2026-08-18

- **Objective in progress:** replace simplistic bar-only assumptions with a deterministic, source-aware replay layer and a look-ahead-safe economic-news calendar.
- **Implemented:** `research/market_data_engine.py` and `research/news_calendar.py`; tested trade-event canonicalization, exact-event deduplication, non-synthetic bars, UTC policy, source-side volume/imbalance fields, event provenance, calendar timestamp validation, look-ahead-safe features and explicitly retrospective event-study labels.
- **Critical real-data finding:** a NQ raw-trades replay of `NQ_trades_2024-01-02_2024-01-03.parquet` has 377,859 source rows, 27,968 repeated sequence rows but only 3,472 exact duplicate events. Sequence alone is therefore not a valid deduplication key; distinct prints with a shared sequence are retained. 374,387 accepted events produce 1,380 non-synthetic one-minute bars; 0 out-of-order rows; 1 unknown-side row. Evidence: `research/studies/data_quality/nq_trades_2024-01-02.json`.
- **News sources registered:** BLS scheduled releases, Federal Reserve FOMC calendar, BEA release schedule and EIA WPSR schedule in `research/news_calendar_sources.json`; methodology and explicit coverage boundary in `research/NEWS_AWARE_DATA_ENGINE.md`.
- **Verification:** focused test suite `5 passed`; full suite `31 passed`; `py_compile` passed. The research document citation ledger is `research/news-calendar-citations.json`.
- **Not yet modelled:** executable bid/ask fill price, queue/impact, latency, exchange session and roll mapping, actual-vs-forecast vintages, or a licensed historical newswire. Do not describe the current work as a fill simulator or a complete news archive.

### Specialist-dispatch failure — 2026-08-18

- **Attempted wave:** Atlas website audit (`chl-20260818-0002`) and Midas market-data-engine audit (`chl-20260818-0003`) after the provider's unauthenticated model endpoint returned HTTP 200.
- **Verified result:** both execution requests failed immediately with HTTP 401 before any agent tool call or audit. Both transcripts were truncated at `max_iterations`; no deliverable or artifact is accepted.
- **Archived evidence:** result envelopes in `D:/CapoHornLab/contracts/envelopes/` and verification logs in `D:/CapoHornLab/contracts/logs/` for task IDs 0002 and 0003.
- **Operational decision:** keep the project loop local and verified; do not re-dispatch specialists through the same provider until the authenticated generation credential/provider is repaired. This avoids repeated empty task waves.

### NinjaTrader depth-10 and news-event request intake — 2026-08-18

- **Saved policy:** `research/NINJATRADER_DEPTH10_DATA_POLICY.md` records the validated use case for a ten-level NinjaTrader depth feed, required provenance, Market Replay/Tick Replay limits, and source URLs. It explicitly excludes claims of queue position, exact fills, order-level reconstruction, or complete news coverage.
- **Website request capture:** `test-strategy.html` Step 2 now offers three explicit research modes — tick/trades, 10-level market depth, and news-event study — plus fields for event families and a falsifiable news signal rule. The selected mode and news requirements are retained structurally in the existing `indicators_params` JSON request field, so no database migration was needed.
- **Verification:** new contract test `tests/test_test_strategy_data_modes.py` was RED first (`3 failed`), then passed (`3 passed`). Full suite: `.venv/Scripts/python.exe -m pytest -q` → `38 passed in 1.13s`; inline JavaScript syntax check, `git diff --check`, and structural HTML responsive-control check all passed.
- **Scope boundary:** this captures a request and preserves its methodology; it does not yet promise availability of a particular depth/news dataset or initiate an external data download.

## Known constraints

- No live orders or trading execution.
- No publication, DNS, hosting or provider changes without Francesco's explicit confirmation.
- A strategy is a **research candidate**, never a promised edge, until it passes a cost-aware IS/OOS backtest on owned data.
- Research outputs must preserve negative results and include realistic costs/slippage.

## Immediate next gates

1. Verify exact local data coverage and current backtest interfaces.
2. Audit executable website setup and fix only local, reversible items.
3. Source and rank research candidates against actual data coverage.
4. Implement candidates one at a time, with tests and dual-mode backtests.
5. Run production readiness review; present any external go-live payload for approval.

### Provenance/checksum gate update — 2026-08-18

- **Objective completed:** added a fail-closed source-file provenance validator at `research/market_data_engine.py::validate_source_file_provenance` before any new raw-data replay is admitted.
- **Validated metadata contract:** `schema_version` (`1.0`), source label, dataset ID, symbol, and externally recorded `expected_sha256`; regular-file existence is required. The validator streams files in 1 MiB chunks, verifies SHA-256, and returns deterministic source, dataset, uppercase symbol, file name, byte count, digest, and `checksum_verified: true`.
- **TDD evidence:** the new provenance test was written and observed failing first with `ImportError` (validator absent), then passed after minimal implementation. Its fixture is intentionally local and deterministic; mismatched digests and incomplete metadata are asserted to fail closed.
- **Verification:** `.venv/Scripts/python.exe -m pytest tests/test_market_data_engine.py::test_source_file_provenance_requires_matching_checksum_and_complete_metadata -q` → `1 passed in 0.62s`; `.venv/Scripts/python.exe -m py_compile research/market_data_engine.py` → exit 0; full `.venv/Scripts/python.exe -m pytest -q` → `32 passed in 1.11s`; `git diff --check` → exit 0.
- **Scope boundary:** no raw market-data file outside this project was accessed or altered in this cycle, so no historical source checksum was fabricated. The next replay must provide a separately recorded source-metadata object with the real checksum; CME session/roll mapping remains unimplemented.

### Session-anchor aggregation update — 2026-08-18

- **Objective completed:** added deterministic, configurable UTC session anchoring to `research/market_data_engine.py::TradeBarProcessor`. Bars now accept `session_start_utc="HH:MM"` (default `00:00`), are grouped from that daily UTC boundary, and receive a `session_date` label that remains stable across midnight. Quality now reports `session_count`; provenance records the exact session boundary used.
- **TDD evidence:** `tests/test_market_data_engine.py::test_trade_processor_anchors_bars_to_explicit_utc_session_start` was added first and observed failing with `TypeError: unexpected keyword argument 'session_start_utc'`; it then passed after the minimal implementation. The test deliberately uses a 23:02 UTC boundary and 5-minute bins, proving aggregation does not silently fall back to midnight-aligned buckets.
- **Verification:** `.venv/Scripts/python.exe -m pytest tests/test_market_data_engine.py::test_trade_processor_anchors_bars_to_explicit_utc_session_start -q` → `1 passed in 0.62s`; full `.venv/Scripts/python.exe -m pytest -q` → `33 passed in 1.11s`; `py_compile research/market_data_engine.py` and `git diff --check` both exited 0.
- **Scope boundary:** this is an explicit UTC session configuration mechanism, not a claim of CME holiday, daylight-saving, maintenance-break, or contract-roll mapping. Those venue-calendar rules remain a separate unimplemented gate.

### Real owned-NQ provenance-manifest replay update — 2026-08-18

- **Objective completed:** separately recorded a SHA-256 provenance manifest for the owned raw NQ trade file, then used that manifest as the metadata input to the fail-closed replay gate. The source file was read for hashing only and was not modified.
- **Artifact:** `research/studies/data_quality/nq_trades_2024-01-02_2024-01-03.provenance.json`.
- **Recorded identity:** `NQ_trades_2024-01-02_2024-01-03.parquet`; 8,842,273 bytes; SHA-256 `547d5ab92e7673e30b824a1f1cf2fb3098591bec6fbe75c20b8b022a9761a132`; source `owned-nq-trades`; dataset ID `NQ-trades-2024-01-02_2024-01-03`; symbol `NQ`.
- **Replay-gate verification:** `validate_source_file_provenance(manifest['source_file'], manifest)` returned `REPLAY_GATE_PASS` with the recorded digest, byte count, uppercase symbol, and `checksum_verified: true`.
- **Regression verification:** `.venv/Scripts/python.exe -m pytest tests/test_market_data_engine.py -q` → `5 passed in 0.68s`; `.venv/Scripts/python.exe -m pytest -q` → `33 passed in 1.04s`; `py_compile research/market_data_engine.py` and `git diff --check` both exited 0. Git emitted pre-existing CRLF-normalization warnings only.
- **Next gate:** attach this immutable manifest to the next owned-NQ replay result before interpreting research output; venue calendar, roll mapping, and executable fill modelling remain unimplemented.

### Optional bid/ask feature update — 2026-08-18

- **Objective completed:** extended `research/market_data_engine.py::TradeBarProcessor` so a source frame that actually supplies bid/ask prices emits explicit quote-derived fields, rather than inferring them from trade sides. With `bid_size` and `ask_size` also supplied, it emits the closing microprice and top-of-book quote imbalance.
- **Schema and quality policy:** `bid_price`/`ask_price` and `bid_size`/`ask_size` are all-or-nothing pairs; prices and sizes must be positive; `ask_price >= bid_price` is enforced. Bars expose closing bid, ask, quoted spread, midpoint, microprice and quote imbalance. Quality reports `quote_rows`; provenance records `quote_features` as `not_available`, `bid_ask_prices`, or `bid_ask_prices_and_sizes`.
- **TDD evidence:** `tests/test_market_data_engine.py::test_trade_processor_emits_explicit_quote_features_when_bid_ask_data_is_supplied` was written and observed failing first because `close_bid_price` did not exist. It passed after the minimal optional quote-schema and aggregation implementation; the invalid crossed quote assertion also passes.
- **Verification:** `.venv/Scripts/python.exe -m pytest tests/test_market_data_engine.py::test_trade_processor_emits_explicit_quote_features_when_bid_ask_data_is_supplied -q` → `1 passed in 0.74s`; `tests/test_market_data_engine.py -q` → `6 passed in 0.83s`; `.venv/Scripts/python.exe -m py_compile research/market_data_engine.py` and `git diff --check` both exited 0; full `.venv/Scripts/python.exe -m pytest -q` → `34 passed in 1.12s`.
- **Scope boundary:** no owned market-data source outside this project was read or modified in this cycle. This proves deterministic handling of a supplied quote schema via a local fixture, not the availability or provider semantics of CL MBP-1 data, executable fills, queue position, impact, latency, rolls, or venue-calendar mapping.

### CME Globex session-rule update — 2026-08-18

- **Objective completed:** added optional, DST-aware `cme_globex_equity_index` session handling to `research/market_data_engine.py::TradeBarProcessor`. It derives bars and `session_date` from a 17:00 America/Chicago session boundary rather than a fixed UTC offset, and fails closed on source events during the regular 16:00–17:00 Chicago maintenance break.
- **TDD evidence:** `tests/test_market_data_engine.py::test_cme_globex_equity_index_rules_anchor_in_chicago_time_and_reject_maintenance_break` was added first and failed as expected with `TypeError: unexpected keyword argument 'venue_session_rules'`. It now proves correct winter/summer DST labeling and maintenance-break rejection.
- **Method declaration:** emitted provenance records the venue rule, `America/Chicago`, maintenance-break window, and explicit limit: regular-session boundary only; no holiday, early-close, product-specific halt, or contract-roll mapping claim. `research/NEWS_AWARE_DATA_ENGINE.md` documents the same scope.
- **Verification:** `.venv/Scripts/python.exe -m pytest tests/test_market_data_engine.py -q && .venv/Scripts/python.exe -m py_compile research/market_data_engine.py && git diff --check` → `7 passed` (exit 0); full `.venv/Scripts/python.exe -m pytest -q` → `35 passed in 1.27s`.
- **Next gate:** attach the existing NQ provenance manifest and this CME rule to a replay result, then add only explicitly declared fill limitations/cost assumptions before any candidate strategy backtest. No strategy alpha work was performed.
