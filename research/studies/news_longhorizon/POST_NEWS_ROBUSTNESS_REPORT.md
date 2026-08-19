# Post-News COVID Robustness — ES Long-Horizon Event Study

**Status:** Preliminary and non-promotable. Descriptive sensitivity only; not a trading rule.

## Objective
Test whether the parent study's post-release r20 summaries persist after excluding March–April 2020 and, separately, all of 2020. Event definitions, session alignment, and r20 calculation are unchanged.

## Results (r20)

| Scenario | Family / group | N | Mean % | Median % | t | unadjusted p | Win % |
|---|---|---:|---:|---:|---:|---:|---:|
| full_sample | fomc/hold | 28 | 3.4705 | 2.791 | 2.642 | 0.0082 | 75.0 |
| full_sample | fomc/cut | 4 | 2.537 | 2.3645 | 0.405 | 0.6853 | 75.0 |
| full_sample | fomc/hike | 11 | 0.6236 | 0.0593 | 0.51 | 0.6104 | 54.55 |
| full_sample | cpi/moderate | 26 | 1.3658 | 2.5915 | 1.516 | 0.1296 | 73.08 |
| full_sample | cpi/cool | 9 | 0.6592 | -0.0547 | 0.3 | 0.7642 | 44.44 |
| full_sample | cpi/hot | 23 | 0.9855 | 0.7792 | 1.031 | 0.3026 | 65.22 |
| full_sample | nfp/moderate | 9 | 0.3986 | 0.7652 | 0.234 | 0.8149 | 66.67 |
| full_sample | nfp/strong | 38 | 0.095 | 1.0203 | 0.115 | 0.9081 | 55.26 |
| full_sample | nfp/weak | 11 | 4.6657 | 5.0744 | 3.217 | 0.0013 | 90.91 |
| exclude_covid_mar_apr_2020 | fomc/hold | 24 | 1.4144 | 2.1132 | 1.831 | 0.0671 | 70.83 |
| exclude_covid_mar_apr_2020 | fomc/hike | 11 | 0.6236 | 0.0593 | 0.51 | 0.6104 | 54.55 |
| exclude_covid_mar_apr_2020 | fomc/cut | 2 | 2.3645 | 2.3645 | 2.262 | 0.0237 | 100.0 |
| exclude_covid_mar_apr_2020 | cpi/moderate | 26 | 1.3658 | 2.5915 | 1.516 | 0.1296 | 73.08 |
| exclude_covid_mar_apr_2020 | cpi/cool | 7 | 0.0338 | -0.5967 | 0.012 | 0.9902 | 42.86 |
| exclude_covid_mar_apr_2020 | cpi/hot | 23 | 0.9855 | 0.7792 | 1.031 | 0.3026 | 65.22 |
| exclude_covid_mar_apr_2020 | nfp/moderate | 9 | 0.3986 | 0.7652 | 0.234 | 0.8149 | 66.67 |
| exclude_covid_mar_apr_2020 | nfp/weak | 10 | 3.7322 | 4.9796 | 3.042 | 0.0024 | 90.0 |
| exclude_covid_mar_apr_2020 | nfp/strong | 37 | 0.5057 | 1.3022 | 0.689 | 0.4906 | 56.76 |
| exclude_2020 | fomc/hold | 17 | 1.8346 | 2.311 | 2.356 | 0.0185 | 76.47 |
| exclude_2020 | fomc/hike | 11 | 0.6236 | 0.0593 | 0.51 | 0.6104 | 54.55 |
| exclude_2020 | fomc/cut | 2 | 2.3645 | 2.3645 | 2.262 | 0.0237 | 100.0 |
| exclude_2020 | cpi/hot | 21 | 0.8145 | 0.5556 | 0.789 | 0.43 | 61.9 |
| exclude_2020 | cpi/moderate | 21 | 1.9967 | 2.2813 | 4.251 | 0.0 | 71.43 |
| exclude_2020 | cpi/cool | 5 | -2.4115 | -5.0887 | -0.972 | 0.3309 | 40.0 |
| exclude_2020 | nfp/weak | 9 | 3.181 | 4.8847 | 2.595 | 0.0094 | 88.89 |
| exclude_2020 | nfp/strong | 30 | 0.4168 | 1.3271 | 0.48 | 0.6313 | 56.67 |
| exclude_2020 | nfp/moderate | 8 | 1.7998 | 2.0517 | 1.64 | 0.101 | 75.0 |

## Interpretation
The table is a stress test of sample composition, not confirmatory evidence. A result that materially changes under either exclusion is regime-sensitive. A result that does not change still remains preliminary because it has not passed the parent study's provenance, as-of-vintage, IS/OOS, overlap-robust, multiple-testing, and execution-assumption gates.

## Limits
- Event-date sensitivity is not an as-of event-vintage or source-provenance validation.
- Twenty-session windows overlap; the parent study's unadjusted normal-approximation p-values remain indicative.
- No multiplicity correction is applied across families, groups, horizons, or sensitivity scenarios.
- Daily-close reference returns have no executable fill, cost, slippage, roll, or position-sizing model.
- This does not establish a tradeable strategy or causal mechanism.

## Reproducibility
Run `.venv/Scripts/python.exe research/studies/news_longhorizon/post_news_robustness.py`. Output: `post_news_robustness_results.json` and this report.
