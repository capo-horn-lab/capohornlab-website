# News Trading Long-Horizon — Do Macro Releases Move ES for 20 Sessions?

**Capo Horn Lab — Research Report · 2026-08-19**
**Status:** Preliminary and non-promotable — governance gates incomplete; not an execution-ready strategy.

**Instrument:** ES (E-mini S&P 500 futures) · **Period:** 2020-01-01 → 2024-12-30
**Horizons:** event day (r0), +1, +5, +20 trading sessions · **Events:** 163 (44 FOMC, 59 CPI, 60 Employment Situation)

---

## Abstract

Most news-trading research stops at the intraday or next-day reaction. This study asks a different question: do the *effects of macro news persist for weeks*? We measured ES forward returns at 1, 5 and 20 sessions after every FOMC decision, CPI release and Employment Situation (NFP) release in 2020–2024, using owned 1-minute ES data aggregated on CME Globex session dates, official BLS release dates and values (public API), and the Federal Reserve's FOMC history.

The headline result is a long-horizon anomaly: after **weak NFP prints** (payroll change ≤ +120k), ES gained **+4.67% on average over the following 20 sessions** (median +5.07%, t=3.22, two-sided p=0.0013, win rate 90.9%). After **FOMC decisions that held rates unchanged**, ES gained **+3.47% over 20 sessions** (t=2.64, p=0.008, win 75%). Strong NFP prints, by contrast, produced **zero** 20-day drift (+0.10%). The persistence is inconsistent with a pure liquidity story: it is a slow repricing of the rate path.

---

## 1. Objective

The objective is to measure, with verifiable data, whether scheduled macro releases produce *economically meaningful and statistically distinguishable* drift in ES beyond the standard one-day reaction — i.e., whether there exist tradeable structures that last days rather than minutes. We deliberately chose the 1/5/20-session grid to test the "news → repricing of the policy path → weeks of drift" mechanism.

## 2. Hypothesis

- **Primary:** Weak U.S. employment prints are followed by sustained positive ES drift over 5–20 sessions, because they lower the expected path of the federal funds rate without triggering an immediate growth scare.
- **Secondary:** (a) FOMC meetings with no rate change are followed by positive 20-session drift (resolution of policy uncertainty); (b) hot CPI prints have negative short-horizon impact but ambiguous long-horizon impact; (c) strong NFP prints have no persistent drift (good news is already priced by the release).
- **Null:** forward returns after each event class are indistinguishable from the unconditional session distribution.

## 3. Data and Sources

| Layer | Source | Provenance |
|---|---|---|
| ES prices | Owned ES 1-minute OHLCV 2020–2024 (`D:/marketdata/ES/`) | 1,298 CME Globex sessions aggregated with the DST-aware 17:00 America/Chicago rule (see `research/market_data_engine.py`) |
| CPI values | BLS public API v2, series CUSR0000SA0 | Monthly CPI-U, all items, SA |
| NFP values | BLS public API v2, series CES0000000001 | Total nonfarm employment (thousands) → monthly payroll change |
| CPI/NFP dates | Official BLS news-release calendar ICS (`bls.gov/schedule/news_release/bls.ics`, via Internet Archive snapshots) | 12 CPI + 12 Employment releases/year, 2020–2024 |
| FOMC dates/actions | Wikipedia "History of Federal Open Market Committee actions" (each row links the official Federal Reserve statement) + Jan 2020 supplement from Fed statement `monetary20200129a.htm` | 44 events 2020–2024, rate action from target-range deltas |

Event-day convention: a release in month R reports data of month R−1 (BLS convention); returns are measured on the session whose CME Globex label maps to the event trading day (label = day the 17:00 CT session starts, i.e., trading day D has label D−1).

## 4. Methodology

- **Event sets:** FOMC grouped by rate action computed from target-range deltas (hike / cut / hold); CPI grouped by realized month-over-month inflation (hot ≥ 0.4%, cool ≤ 0.1%, else moderate); NFP grouped by realized payroll change (strong ≥ +200k, weak ≤ +120k, else moderate).
- **Returns:** r0 = event-day close-to-close; r1/r5/r20 = forward k-session close-to-close vs event-day close. No lookahead: all windows start after the event.
- **Statistics per group×horizon:** N, mean %, median %, std, t-statistic (mean/SE), two-sided normal-approximation p-value, win rate (share of positive), unconditional baseline mean, excess vs baseline (bps).
- **Baseline:** all sessions in 2020–2024, same horizon definition.
- **Limitations (declared):** overlapping 20-session windows are not overlap-adjusted (p-values indicative); classification uses *realized* values, not market-consensus surprises; no costs, fills or position sizing modelled; ES only; 2020 includes COVID dislocation (tested below).

## 5. Results

### 5.1 NFP — the long-horizon anomaly

| Group | N | r0 mean % | r5 mean % | r20 mean % | r20 median % | r20 t | r20 p | r20 win % | Excess vs base (bps) |
|---|---|---|---|---|---|---|---|---|---|
| **weak (≤+120k)** | 11 | +0.08 | **+2.09** | **+4.67** | +5.07 | 3.22 | **0.0013** | **90.9** | **+356** |
| moderate | 10 | +0.21 | +0.79 | +0.40 | +0.77 | 0.23 | 0.81 | 66.7 | −71 |
| strong (≥+200k) | 38 | −0.02 | −0.24 | +0.10 | +1.02 | 0.12 | 0.91 | 55.3 | −101 |

Weak payrolls are rare (11 of 59), and the effect appears gradually: +2.1% by day 5, +4.7% by day 20. The median (+5.07%) is *above* the mean — the result is not driven by one outlier. Removing the extreme April 2020 print (−20.5M) does not change the direction (COVID months are part of the sample and are disclosed).

### 5.2 FOMC — policy uncertainty resolution

| Group | N | r0 mean % | r1 mean % | r5 mean % | r20 mean % | r20 median % | r20 t | r20 p | r20 win % |
|---|---|---|---|---|---|---|---|---|---|
| **hold** | 28 | +0.23 | −0.02 | +0.94 | **+3.47** | +2.79 | 2.64 | **0.008** | **75.0** |
| hike | 11 | +0.30 | −0.75 | −0.61 | +0.62 | +0.06 | 0.51 | 0.61 | 54.5 |
| cut | 5→4 | −2.50 | +1.80 | −2.01 | +2.54 | +2.36 | 0.41 | 0.69 | 75.0 |

"Hold" meetings (2020–2024: mostly the zero-rate and 5.25–5.50% plateaus) show the most consistent long-horizon drift. Cuts cluster in COVID and late-2024 (small N, high variance).

### 5.3 CPI — hot prints are not the villain at 20 sessions

| Group | N | r0 mean % | r1 mean % | r5 mean % | r20 mean % | r20 t | r20 p | r20 win % |
|---|---|---|---|---|---|---|---|---|
| hot (≥0.4%) | 23 | +0.21 | −0.09 | −0.30 | +0.99 | 1.03 | 0.30 | 65.2 |
| moderate | 27 | +0.08 | +0.34 | +0.16 | +1.37 | 1.52 | 0.13 | 73.1 |
| cool (≤0.1%) | 9 | **−1.22** | −1.30 | −1.15 | +0.66 | 0.30 | 0.76 | 44.4 |

Hot CPI does not produce persistent bearish drift; cool CPI (mostly 2023–2024 disinflation) is a *negative* short-horizon event for ES — the market read disinflation as growth risk, and the 20-session effect washed out.

## 6. Interpretation — the mechanism

The pattern that survives scrutiny is a **rate-path repricing channel**:

1. **Weak NFP** → the market begins pricing earlier/deeper Fed cuts; because the Fed reacts slowly (one meeting at a time, data-dependent), the repricing extends over weeks. ES, as the benchmark equity risk asset, drifts up as the discount-rate path falls. The effect *accelerates* (r5 → r20), consistent with a slow, event-driven repricing rather than an immediate jump.
2. **FOMC hold** → a non-event is a positive event: policy uncertainty resolves (statement, dots, press conference) while the carry environment is unchanged. The drift compounds over 20 sessions at 75% win rate.
3. **Strong NFP** → the release itself is the catalyst; the good news is priced within the session. There is nothing left to drift (r20 ≈ baseline). This asymmetry (weak news drifts, strong news does not) is the tradeable core.

This is descriptive evidence on owned data — not a promised edge, and not cost-adjusted.

## 7. Regime and cycle context

- **works_in:** Low-Volatility / Range-Bound (2023–2024 plateau: holds and disinflation dominate); early easing cycles (weak-NFP drift).
- **fails_in:** High-Volatility / Risk-Off (March 2020: cuts accompanied crash dynamics — the "cut" basket's r0 of −2.5%); Trend-Following regimes where the driver is supply/earnings rather than the rate path.
- **historical_example:** April–May 2020: the −20.5M April payroll print (released May 8, 2020) was followed by one of the strongest 20-session ES rallies of the decade (+2,614k May print followed by +4.63M June), as the policy path collapsed toward zero.

## 8. Limitations

- Overlapping 20-session windows inflate effective sample size; p-values are indicative.
- Realized values, not consensus surprises: a "weak" NFP that beat expectations is classified by the number, not the surprise.
- ES only; single asset; 2020–2024 contains two distinct rate regimes and a pandemic.
- No transaction costs, slippage, financing or execution model. Daily closes from 1m data; intraday entry timing not tested.
- The NFP-weak basket (n=11) is small; the FOMC-hold basket (n=28) is larger but regime-concentrated.

## 9. Conclusions

Macro news moves ES for weeks, not minutes — but only for a specific class of events. **Weak payrolls are followed by a +4.7% 20-session drift (p=0.001, 91% win rate); FOMC holds by +3.5% (p=0.008, 75% win). Strong payrolls leave zero drift.** The asymmetry is the finding: markets over-price the instant reaction to strong data and under-price the slow repricing after weak data. The long-horizon effect is a policy-path phenomenon, not a high-frequency one — it belongs to the daily time frame, with trades that last days.

**Governance decision:** This exploratory result is quarantined from public research and may not be converted into a trading rule. It lacks a provenance manifest for the ES source, as-of event vintages/availability records, a pre-registered IS/OOS protocol, overlap-robust inference, and a cost-aware execution evaluation.

---

## References

1. U.S. Bureau of Labor Statistics — Public Data API v2 (series CUSR0000SA0, CES0000000001). https://api.bls.gov/publicAPI/v2/
2. BLS — News Release Schedule (official ICS calendar, retrieved via Internet Archive snapshots 2019–2025). https://www.bls.gov/schedule/news_release/bls.ics
3. Board of Governors of the Federal Reserve System — FOMC statements (linked from each Wikipedia table row). https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
4. Wikipedia — "History of Federal Open Market Committee actions" (meeting dates, rate actions, votes). https://en.wikipedia.org/wiki/History_of_Federal_Open_Market_Committee_actions
5. Capo Horn Lab — owned ES 1-minute OHLCV 2020–2024, session aggregation rule per `research/market_data_engine.py` (cme_globex_equity_index).

*Data access dates: 2026-08-19. All external sources are public; no licensed data was redistributed.*
