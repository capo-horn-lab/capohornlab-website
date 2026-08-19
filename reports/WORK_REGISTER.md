# Capo Horn Lab Website — Work Register

**Updated:** 2026-08-19
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

### Real owned-NQ replay with provenance gate + CME Globex rule — 2026-08-18 (evening)

- **Objective completed:** attached the existing NQ provenance manifest and the `cme_globex_equity_index` venue rule to a real replay of the owned raw NQ trades file (`D:/marketdata/NQ/tick_trades_raw/NQ_trades_2024-01-02_2024-01-03.parquet`), closing the register's next gate before any candidate backtest.
- **Artifacts:** `research/nq_cme_replay_study.py`; `research/studies/data_quality/nq_cme_globex_replay_2024-01-02_2024-01-03.json`; `nq_cme_globex_replay_2024-01-02_2024-01-03_REPORT.md`.
- **Verified outcome:** provenance gate `REPLAY_GATE_PASS` (SHA-256 `547d5ab9…` matches the separately recorded manifest, 8,842,273 bytes); 374,387 accepted events; 1,380 non-synthetic 1-minute bars across 2 CME Globex sessions (2024-01-02 and 2024-01-03, 17:00 America/Chicago DST-aware boundary); 0 out-of-order, 0 unknown-side, 0 maintenance-break rows, 0 synthetic bars; quote features `not_available` (source has no bid/ask columns).
- **Verification:** `.venv/Scripts/python.exe -m py_compile research/nq_cme_replay_study.py` and execution (exit 0, `STUDY_OK gate=REPLAY_GATE_PASS … bars=1380 sessions=2`); independent readback returned `READBACK_PASS bars=1380 sessions=2 sum_bars=1380 sha_match=True`; full suite `.venv/Scripts/python.exe -m pytest -q` → `40 passed in 1.52s`; `git diff --check` → exit 0.
- **Next gate:** add only explicitly declared fill limitations/cost assumptions (slippage, commissions, fill-model scope) before any candidate strategy backtest; holiday/early-close/contract-roll mapping remains unimplemented. No alpha work was performed in this cycle.


### Execution-assumptions declaration update — 2026-08-19

- **Objective completed:** added `ExecutionAssumptions` to `research/market_data_engine.py` so a future bar-based backtest must carry a machine-readable execution classification, stated cost inputs, calibration status, and fill limitations.
- **Fail-closed policy:** only `bar_reference_only` is currently supported. It explicitly sets `executable_fills: false` and rejects any configuration that attempts to claim executable fills.
- **Required declaration:** per-contract commission and per-side slippage inputs are accepted as stated assumptions; `costs_are_calibrated` defaults to false. The provenance payload records that the model excludes bid/ask path, queue position, partial-fill probability, market impact, latency, and order priority.
- **TDD evidence:** the new focused test first failed with `ImportError` because `ExecutionAssumptions` was absent, then passed after the minimal implementation.
- **Verification:** `.venv/Scripts/python.exe -m pytest tests/test_market_data_engine.py::test_bar_reference_execution_assumptions_are_explicit_and_cannot_claim_executable_fills -q` -> `1 passed in 0.64s`; full `.venv/Scripts/python.exe -m pytest -q` -> `41 passed in 1.60s`; `py_compile research/market_data_engine.py` and `git diff --check` exited 0.
- **Scope boundary:** this is a declared reference-price stress-assumption contract, not a calibrated broker schedule or a fill simulator. No alpha, candidate strategy, live order, external data access, deployment, or publication was performed.
- **Next gate:** attach a deliberate `ExecutionAssumptions` instance to each candidate backtest artifact and retain `executable_fills: false` unless a provenance-backed quote/fill validation is implemented.

### Backtest-artifact execution-disclosure update — 2026-08-19

- **Objective completed:** attached a machine-readable `execution_assumptions` provenance block to every `BacktestEngine.get_report()` output, closing the immediate reporting gate without changing any strategy logic or producing a performance claim.
- **Implementation:** `research/backtest_engine.py` now accepts an optional `ExecutionAssumptions` instance and defaults to the existing stated reference assumptions: `bar_reference_only`, `executable_fills: false`, USD 2.50 commission per contract per side, and 1.0 assumed slippage tick per side. The report exports its full limitations declaration with the results artifact.
- **TDD evidence:** new `tests/test_backtest_execution_assumptions.py` failed first with `KeyError: 'execution_assumptions'`, then passed after the minimal report wiring.
- **Verification:** focused test -> `1 passed in 1.78s`; full `.venv/Scripts/python.exe -m pytest -q` -> `42 passed in 2.44s`; `py_compile research/backtest_engine.py research/market_data_engine.py` and `git diff --check` -> exit 0. Independent report readback returned `READBACK_PASS` and confirmed `bar_reference_only`, `executable_fills=false`, USD 2.50/side and 1.0 tick/side.
- **Scope boundary:** this records a non-executable reference-price assumption; it neither calibrates costs nor validates bid/ask path, queue position, partial fills, impact, latency, order priority, venue holidays/early closes, or contract rolls. No candidate strategy alpha, raw data access, deployment, publication, payment, email, or order was performed.
- **Next gate:** preserve the report declaration in the first separately pre-registered candidate run; only provenance-backed venue-calendar/roll and quote/fill work can relax its non-executable limit.

### News long-horizon quarantine — 2026-08-19

- **Objective completed:** quarantined the unverified ES macro-event exploratory study from all local public research pages rather than presenting it as a positive trading claim.
- **Why:** although the generic engine gates now exist, this ES study has no attached ES source-file provenance manifest, no as-of actual/forecast vintage and availability record, no pre-registered IS/OOS protocol, overlap-robust inference, or cost-aware execution evaluation. It cannot be an execution-ready strategy.
- **Artifacts:** `research/studies/news_longhorizon/REPORT.md`; regression guard `tests/test_news_longhorizon_governance.py`. The report is explicitly marked **Preliminary and non-promotable** and names the missing gates; `news-event-long-horizon-es` was removed from `research.html`, `research-detail.html`, and their `pages/` mirrors.
- **TDD evidence:** the new governance test was written first and failed because the report lacked the mandatory status and public pages still exposed the slug; after the quarantine, focused test passed.
- **Verification:** `.venv/Scripts/python.exe -m pytest tests/test_news_longhorizon_governance.py -q` → `1 passed in 0.20s`; full `.venv/Scripts/python.exe -m pytest -q` → `43 passed in 2.17s`; `py_compile` for the market-data engine, backtest engine, and study script plus `git diff --check` passed. Readback confirmed public slug count `0`.
- **Next gate:** do not promote or trade this study. If resumed, build a separately checksummed ES replay manifest and as-of event-vintage record first, then pre-register and test IS/OOS with explicitly non-executable execution assumptions.

### Declared-cost execution wiring update — 2026-08-19

- **Objective completed:** made `BacktestEngine` apply the same explicit bar-reference cost assumptions it exports in every report, removing hidden volume/volatility adjustments and daily-volume commission discounts from this non-executable research path.
- **Implementation:** `research/backtest_engine.py` now initializes its slippage component from `ExecutionAssumptions`, applies the declared per-contract-per-side commission through `_commission_for`, and describes both modes accurately: `ottimale` is a zero-cost counterfactual and `realistico` is a stated-cost, bar-reference stress run. Neither is labelled an executable fill simulation.
- **TDD evidence:** `tests/test_backtest_execution_assumptions.py::test_declared_reference_costs_drive_engine_commission_and_slippage` was added first and failed with `AttributeError: _commission_for`; after the minimal wiring it passed and confirms USD 3.75 × 2 contracts = USD 7.50 and NQ 2 ticks = 0.50 price points.
- **Verification:** `.venv/Scripts/python.exe -m pytest -q` → `44 passed in 2.62s`; `.venv/Scripts/python.exe -m py_compile research/backtest_engine.py research/market_data_engine.py` and `git diff --check` exited 0. Independent report readback confirmed `bar_reference_only`, `executable_fills: false`, USD 3.75/side, and 2.0 ticks/side.
- **Scope boundary:** these are transparent stress assumptions, not calibrated costs or validation of bid/ask path, queue position, partial fills, impact, latency, order priority, venue holiday/early-close, or contract-roll behavior. No candidate alpha, raw-data access, deployment, publication, payment, email, or order was performed.
- **Next gate:** attach the existing provenance-checked NQ CME replay context and these declared assumptions to one separately pre-registered candidate protocol before running any strategy research.

### Pre-news macro screen — 2026-08-19

- **Objective completed:** extended the quarantined ES macro-event study with a reproducible pre-news screen: drift over t−5..t−1 by realised CPI/NFP outcome, Pearson association to event-day and +20-session returns, and same-sign hit rates.
- **Statistical hardening:** `pre_news_study.py` now excludes non-finite trailing values, reports conventional even-sample medians, uses finite-sample two-sided Student-t inference, Pearson t inference, and exact two-sided binomial p-values against a 50% hit rate. `tests/test_pre_news_statistics.py` protects these behaviours.
- **Verified outcome:** the only nominal pre/post association is weak-NFP pre-5 drift vs r20 (n=11, r=−0.651, p=0.0300); its same-sign hit rate is 54.5% (p=1.0000). CPI-moderate’s 73.1% same-sign r20 rate (n=26, p=0.0290) is unadjusted. Across the screen, there is no validated pre-release predictive signal.
- **Verification:** `.venv/Scripts/python.exe -m pytest tests/test_pre_news_statistics.py -q` → `2 passed`; `.venv/Scripts/python.exe research/studies/news_longhorizon/pre_news_study.py`; full `.venv/Scripts/python.exe -m pytest -q` → `46 passed in 2.77s`; `py_compile` and `git diff --check` passed.
- **Publication decision:** no `research-detail.html` change. The parent study remains preliminary/non-promotable: no checksummed ES manifest, as-of release-vintage/forecast record, pre-registration/IS-OOS split, overlap/multiple-testing robustness, or cost-aware non-executable evaluation.
- **Next gate:** establish the ES provenance and as-of calendar/vintage dataset before treating any pre-news question as confirmatory.

### Pre-news robustness update — 2026-08-19 (God Mode)

- **Objective completed:** extended the quarantined ES pre-news macro screen with explicit pre/post interaction, fixed 2020–2021 versus 2022–2024 regime sensitivity, COVID-year exclusion, and Holm family-wise correction for the within-release pre5→r20 correlation family.
- **Implementation/artifacts:** `research/studies/news_longhorizon/pre_news_study.py`; generated `pre_news_results.json`; updated `PRE_NEWS_REPORT.md` and parent `REPORT.md`; regression guard `tests/test_news_longhorizon_robustness.py`.
- **Verified outcome:** weak-NFP pre5→r20 raw r=−0.651 (n=11, raw p=0.0300) becomes Holm-adjusted p=0.0900. Across all NFP rows, positive-versus-negative pre5 r20 difference is −2.188% (Welch p=0.1243). NFP association is not stable by regime (2020–2021 r=−0.353, p=0.0983; 2022–2024 r=−0.007, p=0.9676) and is absent when 2020 is excluded (r=−0.054, n=48, p=0.7166). CPI all-sample association is r=+0.002 (n=59, p=0.9853).
- **Implied-volatility boundary:** not evaluated: owned `es_daily.csv` contains OHLCV/bar-count only; no VIX/options-IV or external proxy was introduced.
- **Verification:** TDD first: robustness import failed before implementation, then `2 passed`; full `.venv/Scripts/python.exe -m pytest -q` -> `48 passed in 2.73s`; `py_compile`, `git diff --check`, and JSON/report readback all passed. Public-slug grep returned `PUBLIC_QUARANTINE_PASS`.
- **Publication decision:** no `research-detail.html` update and no deploy. The entire parent study remains preliminary/non-promotable due to absent ES source provenance/as-of vintage, overlap-robust inference, pre-registration/IS-OOS, and non-executable cost-aware evaluation.
- **Next gate:** obtain/checksum an ES source manifest and an as-of release-vintage record before any confirmatory test; do not add implied-volatility analysis without a separately licensed/provenanced IV series.

### Live QA and publication-quarantine deployment gate — 2026-08-19 (God Mode)

- **Objective completed locally:** ran a sitemap-driven read-only audit of `https://www.capohornlab.com/` and prepared the smallest reviewed release payload to remove the quarantined preliminary macro-event study from production.
- **Live evidence:** `reports/qa-stress-test-report.md` records 14/14 sitemap pages HTTP 200 and a correct default document title, but the public `research.html` and `research-detail.html` still expose `news-event-long-horizon-es`; therefore the live release is **fix_before_deploy**. The report also has one mailto false-positive and four dead anchors for a later focused remediation.
- **Release payload verified:** `dist/godmode-research-quarantine-20260819.zip`, SHA-256 `b66e9fa974246ee76803b0e001a3995fa4d2d363ff804c15de77083f458bc8b5`; exactly `research.html` (60,960 bytes), `research-detail.html` (238,472 bytes), and `.htaccess` (449 bytes), all with `/` separators and with no local occurrence of the quarantined slug.
- **Local verification:** `.venv/Scripts/python.exe -m pytest -q` → `48 passed in 2.56s`; `git diff --check` → exit 0.
- **Next gate:** upload and extract the reviewed 3-file payload in Aruba File Manager root, then re-run live HTTP/content QA and confirm the public quarantined-slug count is zero.

### Aruba release attempt — 2026-08-19 (God Mode)

- **Objective:** remove the quarantined preliminary macro-event study from public pages using the reviewed minimal Aruba payload.
- **Pre-upload verification:** `.venv/Scripts/python.exe -m pytest -q` -> `48 passed in 2.62s`; `git diff --check` -> exit 0. `dist/godmode-research-quarantine-20260819.zip` verified at 67,017 bytes, SHA-256 `b66e9fa974246ee76803b0e001a3995fa4d2d363ff804c15de77083f458bc8b5`, with exactly `research.html`, `research-detail.html`, and `.htaccess` using `/` archive separators.
- **External action and evidence:** the zip was uploaded successfully to the Aruba File Manager root (`www.capohornlab.com`); live File Manager UI showed the selected `godmode-research-quarantine-20260819.zip` (65 KB).
- **Current status:** **not yet deployed**. elFinder's `Estrai Archivio` context submenu would not open through background-only computer control, and typed existing-profile browser control refused without a fresh `browser-approve` artifact. The archive remains on the server, intentionally retained; no extraction, overwrite, cache purge, or deletion was performed.
- **Live readback before release:** `https://www.capohornlab.com/research.html?v=20260819-predeploy` returned 60,115 bytes with quarantined-slug count `1`; production remains unchanged and must not be described as remediated.
- **Next gate:** extract the already-uploaded archive in the Aruba File Manager root (context menu -> `Estrai Archivio` -> `Qui`), then re-run live content and sitemap QA with a cache-busting query string.


### God Mode deployment retry and production readback — 2026-08-19 (05:43 CEST)

- **Objective attempted:** extract the already uploaded, reviewed release archive `godmode-research-quarantine-20260819.zip` into the Aruba hosting root to remove the quarantined preliminary macro-event study from production.
- **Fresh UI evidence:** Aruba File Manager was open at the `www.capohornlab.com` root; the selected archive was visible at 65 KB and the contextual **Estrai Archivio** command was present. Two background clicks were delivered and fresh UI captures confirmed the submenu did not open; no extraction, overwrite, cache purge, or deletion occurred.
- **Production readback:** cache-busted HTTPS checks remain unchanged: `/research.html` = HTTP 200, 62,121 bytes, quarantined slug count **1**; `/research-detail.html` = HTTP 200, 250,863 bytes, slug count **2**; `/` = HTTP 200, 60,917 bytes, slug count 0, `X-Aruba-Cache: MISS`. Production is therefore still **fix_before_deploy**, not remediated.
- **Local regression verification:** `.venv/Scripts/python.exe -m pytest -q` -> **48 passed in 12.93s**; `git diff --check` -> exit 0.
- **Next gate:** perform the File Manager archive-extract operation through a control path that can trigger its hover-only submenu, then immediately repeat the same live readback; do not claim the public quarantine release until slug counts are zero.


### Post-news COVID robustness — 2026-08-19 (God Mode)

- **Objective completed:** added a reproducible post-release r20 sensitivity study that reuses the parent ES event classifications and forward-return convention, then compares the full sample with two predeclared exclusions: events dated March–April 2020 and all calendar-2020 events.
- **Artifacts:** `research/studies/news_longhorizon/post_news_robustness.py`; `post_news_robustness_results.json`; `POST_NEWS_ROBUSTNESS_REPORT.md`; regression test `tests/test_post_news_robustness.py`.
- **Verified outcome:** weak-NFP r20 remains positive but attenuates from +4.6657% (n=11, p=0.0013) to +3.7322% when March–April 2020 is excluded (n=10, p=0.0024) and +3.1810% when all 2020 is excluded (n=9, p=0.0094). FOMC-hold is materially regime-sensitive: +3.4705% (n=28, p=0.0082) falls to +1.4144% (n=24, p=0.0671) after March–April removal and +1.8346% (n=17, p=0.0185) excluding 2020. Both remain preliminary, with overlapping-window and multiplicity limits explicitly retained.
- **Verification:** TDD red state: missing module produced `ModuleNotFoundError`; after implementation focused test passed (`1 passed in 1.05s`). `py_compile` passed; study execution completed; full suite -> `49 passed in 2.65s`; `git diff --check` -> exit 0. Independent readback: `READBACK_PASS scenarios=3 nfp_weak_marapr_n=10 fomc_hold_ex2020_n=17`.
- **Next gate:** do not promote either post-news result. Proceed only with regime split/volatility proxy after an ES source-provenance manifest and as-of event-vintage record are established; any additional sensitivity family requires a predeclared correction plan.

### Post-news fixed-calendar regime split — 2026-08-19 (God Mode)

- **Objective completed:** added a reproducible post-release r20 regime-split sensitivity using the predeclared calendar buckets 2020–2021 and 2022–2024, without changing the parent realized-outcome event classifications or forward-return alignment.
- **Artifacts:** `research/studies/news_longhorizon/post_news_regime_split.py`; `post_news_regime_split_results.json`; `POST_NEWS_REGIME_SPLIT_REPORT.md`; regression test `tests/test_post_news_regime_split.py`.
- **Verified outcome:** FOMC-hold attenuates from +4.2409% (n=19, Student-t p=0.0336) in 2020–2021 to +1.8439% (n=9, p=0.1700) in 2022–2024. Weak-NFP is +8.1118% (n=3, p=0.1516) versus +3.3734% (n=8, p=0.0436); the small, exploratory cells and uncorrected family mean neither result is promotable. A nominal 2022–2024 CPI-moderate value (+2.2403%, n=18, p=0.0001) is likewise quarantined pending the same gates.
- **Verification:** focused regression test -> `2 passed in 2.08s`; script `py_compile` + execution -> exit 0; full `.venv/Scripts/python.exe -m pytest -q` -> `51 passed in 2.52s`; `git diff --check` -> exit 0. Independent JSON/report readback returned `READBACK_PASS regimes=2 families=3 fomc_hold_n=19,9 means=4.2409,1.8439`.
- **Specialist constraint:** Midas temporary delegation `chl-20260819-0002` failed before tools with provider HTTP 401; no specialist artifact was accepted. The local, verified fallback above is separately evidenced.
- **Scope boundary:** fixed calendar dates are not a realised/implied-volatility split; the study still lacks an ES source-provenance manifest, as-of release-vintage/forecast record, overlap-robust inference, pre-registration/IS-OOS, multiplicity correction across the wider exploratory family, and executable/cost-aware fill validation.
- **Next gate:** establish ES provenance and as-of event vintages before any confirmatory work; do not introduce an IV proxy without separately licensed/provenanced data.
