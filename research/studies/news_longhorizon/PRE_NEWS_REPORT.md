# Pre-News Predictive Study — ES Behavior Before Macro Releases

**Capo Horn Lab · 2026-08-19 · Status: preliminary, quarantined and non-promotable**

## Question and design

This descriptive extension asks whether ES drift in the five CME Globex sessions before scheduled CPI and Employment Situation/NFP releases is associated with the realised release bucket or subsequent ES returns. It covers 2020–2024 (1,298 ES sessions); `pre5` ends before the event session, `r0` is event-day close-to-close, and `r20` is the following 20-session close-to-close return.

Buckets use realised macro values rather than as-of consensus surprises: CPI hot/cool/moderate and NFP strong/weak/moderate. For each bucket the study reports n, mean, median, t and two-sided finite-sample Student-t p for pre-drift; Pearson pre5→post correlations; exact two-sided binomial same-sign tests; a Welch comparison of r20 after positive versus negative pre5; fixed 2020–2021 / 2022–2024 regime splits; and an exclusion of 2020 as the explicit COVID sensitivity.

## Results

- **NFP strong pre5 drift:** n=38, mean +0.892%, median +1.257%, t=2.36, unadjusted p=0.0239. This is descriptive variation by realised outcome, not an available pre-release forecast, because the bucket is only known after the release.
- **NFP weak pre5→r20:** n=11, Pearson r=−0.651, raw p=0.0300. The Holm within-NFP-family adjusted p is **0.0900**, so it does not clear a 5% family-wise threshold. Its 54.5% same-sign rate has exact p=1.0000.
- **NFP interaction:** across all 59 NFP rows, r20 after positive pre5 averaged +0.254% (n=38) versus +2.443% after negative pre5 (n=20); difference −2.188%, Welch t=−1.57, p=0.1243. No validated interaction.
- **Regime sensitivity:** the all-NFP pre5→r20 correlation is −0.163 (n=59, p=0.2207); 2020–2021 is −0.353 (n=23, p=0.0983), 2022–2024 is −0.007 (n=36, p=0.9676), and excluding 2020 is −0.054 (n=48, p=0.7166). The apparent weak-NFP result is not stable.
- **CPI:** all-CPI pre5→r20 correlation is +0.002 (n=59, p=0.9853); neither regime split nor the COVID-excluded sample produces a predictive association. CPI-moderate’s 73.1% same-sign rate (n=26, raw binomial p=0.0290) is an exploratory multiple-testing result, not a rule.

## Explicit data boundary

Implied volatility was **not evaluated**. The owned `es_daily.csv` has OHLCV and bar-count fields only, with no VIX, option-implied-volatility, forecast-vintage, or positioning series. No external volatility series was inserted as a substitute.

## Limits and decision

This study has overlapping r20 windows, realised-value classifications, small rare-event cells, no as-of availability record, no pre-registered IS/OOS split, no ES provenance manifest, and no cost-aware executable-fill evaluation. Holm adjustment applies only to the narrow family of within-release pre5→r20 correlations; remaining p-values are descriptive.

**Decision: do not publish and do not trade.** The result is retained as a negative robustness finding inside the quarantined parent study. The reproducible artefacts are `pre_news_study.py` and `pre_news_results.json`.
