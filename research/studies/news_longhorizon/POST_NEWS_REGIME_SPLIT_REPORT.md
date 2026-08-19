# Post-News Fixed-Calendar Regime Split — ES Long-Horizon Event Study

**Status:** Preliminary and non-promotable. Descriptive sensitivity only; not a trading rule.

## Method
The predeclared event-date buckets are 2020–2021 and 2022–2024. Event definitions and r20 alignment are unchanged from the parent study.

## Results (r20)

| Regime | Family/group | N | Mean % | Median % | Std % | t | two-sided p | Win % |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 2020_2021 | fomc/hold | 19 | 4.2409 | 2.9286 | 8.0343 | 2.301 | 0.0336 | 73.68 |
| 2020_2021 | fomc/cut | 2 | 2.7094 | 2.7094 | 21.6306 | 0.177 | 0.8884 | 50.0 |
| 2020_2021 | cpi/moderate | 8 | -0.602 | 2.3398 | 7.7418 | -0.22 | 0.8322 | 62.5 |
| 2020_2021 | cpi/cool | 4 | 4.4976 | 2.8483 | 6.29 | 1.43 | 0.2481 | 50.0 |
| 2020_2021 | cpi/hot | 11 | 2.2001 | 1.6115 | 2.2261 | 3.278 | 0.0083 | 90.91 |
| 2020_2021 | nfp/moderate | 1 | -10.811 | -10.811 | 0.0 | None | None | 0.0 |
| 2020_2021 | nfp/strong | 19 | 0.516 | 1.3022 | 4.9666 | 0.453 | 0.656 | 63.16 |
| 2020_2021 | nfp/weak | 3 | 8.1118 | 8.6931 | 6.1999 | 2.266 | 0.1516 | 100.0 |
| 2022_2024 | fomc/hike | 11 | 0.6236 | 0.0593 | 4.0589 | 0.51 | 0.6214 | 54.55 |
| 2022_2024 | fomc/hold | 9 | 1.8439 | 1.9154 | 3.6682 | 1.508 | 0.17 | 77.78 |
| 2022_2024 | fomc/cut | 2 | 2.3645 | 2.3645 | 1.478 | 2.262 | 0.2649 | 100.0 |
| 2022_2024 | cpi/hot | 12 | -0.1279 | -0.1101 | 5.8918 | -0.075 | 0.9414 | 41.67 |
| 2022_2024 | cpi/moderate | 18 | 2.2403 | 2.5915 | 1.9335 | 4.916 | 0.0001 | 77.78 |
| 2022_2024 | cpi/cool | 5 | -2.4115 | -5.0887 | 5.5458 | -0.972 | 0.3859 | 40.0 |
| 2022_2024 | nfp/strong | 19 | -0.3259 | -0.0304 | 5.2873 | -0.269 | 0.7912 | 47.37 |
| 2022_2024 | nfp/moderate | 8 | 1.7998 | 2.0517 | 3.1039 | 1.64 | 0.145 | 75.0 |
| 2022_2024 | nfp/weak | 8 | 3.3734 | 4.9796 | 3.8819 | 2.458 | 0.0436 | 87.5 |

## Interpretation
Differences between the two cells are regime sensitivity, not confirmation. Small cells, overlapping horizons, multiple exploration, and missing source/vintage/execution gates prevent promotion.

## Limits
- This is a fixed-calendar descriptive split, not a causal or volatility-regime model.
- The ES daily source has no attached source-file provenance manifest or as-of actual/forecast-vintage record.
- Twenty-session windows overlap; reported Student-t p-values are not overlap-robust.
- No multiplicity correction is applied across the wider exploratory study family.
- Daily-close reference returns have no executable fill, cost, slippage, roll, or position-sizing model.
- This does not establish a tradeable strategy or a promised edge.

## Reproducibility
Run `.venv/Scripts/python.exe research/studies/news_longhorizon/post_news_regime_split.py`. Outputs: `post_news_regime_split_results.json` and this report.
