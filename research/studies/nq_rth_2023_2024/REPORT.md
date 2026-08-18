# NQ RTH exploratory session study — 2023–2024

## Scope

This is a descriptive, reproducible screen of the hypothesis: **the sign of the first 30 RTH minutes predicts the sign of the final 30 RTH minutes**. It is not a trade recommendation and it is not cost-adjusted.

- Source: `D:/marketdata/NQ/1m/NQ_ohlcv_1m_2023.parquet` and `...2024.parquet`
- Session: weekdays, 09:30–15:59 America/New_York
- Observations: 489 complete RTH days
- Gross mean signal return: -1.528 bps/day
- Gross median signal return: -1.660 bps/day
- Positive-day rate: 46.0%
- Correlation, first-30 vs final-30 return: -0.0244

## Frozen IS/OOS screen

The threshold rule is fixed before OOS inspection: first-30-minute range terciles are fitted on 2023 only and applied unchanged to 2024. No parameter is selected from 2024.

| Sample | Complete days | Gross mean bps/day | Positive-day rate | First-30 / final-30 correlation |
|---|---:|---:|---:|---:|
| IS (2023) | 244 | -1.388 | 47.5% | -0.0297 |
| OOS (2024) | 245 | -1.669 | 44.5% | -0.0227 |

Frozen 2023 range cuts: low ≤ 47.06 bps; mid between the cuts; high > 65.49 bps.

## Interpretation boundary

A positive gross result is only a hypothesis filter. It fails promotion unless it survives a pre-registered 2023/2024 split, realistic bid/ask execution, commissions, slippage, minimum holding/exposure controls, and a no-look-ahead review. The output specifically exposes hours of activity and conditional range buckets so that a future strategy has testable **when-not-to-trade** filters as well as entries.

## Artifacts

- `daily_observations.csv` — one row per complete RTH day
- `conditions.csv` — performance by first-30-minute range tercile
- `session_profile.csv` — minute-by-minute activity/volume profile
- `nq_rth_signal_and_activity.png` — cumulative line and RTH activity profile
- `nq_condition_range_terciles.png` — condition chart
