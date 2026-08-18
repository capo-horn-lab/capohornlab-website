# Strategy Candidates — Top 10 Research Backlog

**Date:** 2026-08-17  
**Status:** research roadmap, **not** trading advice and **not** evidence of profitability.

## Decision rule

A candidate enters implementation only after a pre-registered hypothesis, clear session/roll rules, realistic costs, separated IS/OOS windows, and regime analysis. A short pilot never validates an edge. The academic literature gives us testable **families**—time-series momentum across liquid futures,[1] threshold-based opening-range breakouts,[2] and intraday momentum conditioned by volatility/volume[3]—not a transferable guarantee of profitability for ES, NQ or CL.

## Owned-data fit (verified)

| Instrument | Available local data | Practical use now |
|---|---|---|
| ES | 1-minute OHLCV, annual files 2020–2024; two short trades files | multi-year price/volume intraday tests; limited trade-event experiments |
| NQ | 1-minute OHLCV, monthly/annual files 2023–2024 | intraday price/volume tests; short two-year OOS only |
| CL | MBP-1 top-of-book monthly files, 2024–2025 | 1-minute/5-minute OHLCV derived from quotes plus spread, displayed depth and liquidity filters |

The current engine already runs `TSMomentum`, `OpeningRangeBreakout`, `VWAPMeanReversion`, and `IntradayMomentumSPY` (adapted to futures). Local pilot artefacts exist but are short windows and are explicitly non-decision-useful for annualized return claims. The CL MBP-1 fields make liquidity-aware hypotheses feasible; time-of-day must be modeled explicitly because intraday activity and volatility are structurally seasonal in market microstructure studies.[5]

## Ranked candidate backlog

| # | Candidate | First market/data | Why it is worth falsifying | Minimum implementation/test design |
|---:|---|---|---|---|
| 1 | **ES opening-range breakout with volatility and prior-day-direction filter** | ES 1-minute, 2020–2024 | The ORB literature documents testable threshold-based intraday rules.[2] | Freeze 5/15/30-min opening definitions; 2020–22 IS, 2023 validation, 2024 final OOS; realistic entry slippage; reject if performance is confined to one year. |
| 2 | **NQ opening-range breakout, same frozen rules as ES** | NQ 1-minute, 2023–2024 | Cross-market replication is a necessary robustness check, not an optimisation exercise. | Use ES-selected parameters unchanged; 2023 IS / 2024 OOS only; compare with a shuffled-entry benchmark. |
| 3 | **Open-to-close / first-30-min to final-30-min momentum** | ES then NQ 1-minute | Gao et al. document predictive intraday momentum in liquid S&P exposure, stronger on high-volatility and high-volume days.[3] | Map RTH sessions correctly for futures; test a pre-defined volatility/volume gate; do not transfer ETF results to futures without direct validation. |
| 4 | **Intraday demand-imbalance momentum with trailing exit** | ES, NQ 1-minute | A 2024 working paper proposes an intraday momentum design using abnormal demand/supply imbalance and trailing stops; it must be independently replicated.[4] | Reconstruct only variables observable in OHLCV; compare fixed stop, trailing stop and no-trade baseline; use nested IS/OOS. |
| 5 | **Time-series momentum at daily / multi-day horizon** | ES and CL, resampled daily | Evidence supports own-past-return momentum across liquid futures at 1–12-month horizons, but the original result is diversified cross-asset, not proof for a single contract.[1] | Build robust continuous/roll-aware daily series first; test 1/3/6/12-month signals with predeclared volatility scaling; report reversal drawdowns. |
| 6 | **CL opening-range breakout with MBP-1 liquidity gate** | CL MBP-1 2024–2025 | CL has the best local microstructure coverage; opening moves can be filtered by quoted spread, top-of-book size and event intensity. | Derive bars and liquidity metrics without look-ahead; 2024 IS / 2025 OOS; execution is modeled at bid/ask, not mid-price. |
| 7 | **CL VWAP reversion only after exhaustion** | CL MBP-1 2024–2025 | Mean reversion must be conditional; the existing unrestricted short pilot lost after realistic costs. | Require extreme VWAP deviation plus spread/liquidity and momentum-exhaustion conditions; test target at VWAP versus time exit; reject if costs remove expectancy. |
| 8 | **CL microprice / order-book imbalance continuation** | CL MBP-1 2024–2025 | The data contains bid/ask price and size fields, allowing an actual microstructure hypothesis rather than a price-only proxy. | Define imbalance and prediction horizon before testing; timestamp-safe quote sampling; calculate fills on the executable side; embargo adjacent observations. |
| 9 | **Session-seasonality as a *filter*, not standalone alpha** | ES/NQ/CL intraday | Intraday activity, volatility and spread exhibit strong time-of-day structure in market microstructure research.[5] | Estimate session buckets exclusively on IS; apply unchanged to OOS; use only to disable weak/liquidity-poor periods for candidates 1–8. |
| 10 | **Volatility-regime switch: breakout vs. reversion vs. flat** | ES/NQ/CL | This is a portfolio/control hypothesis: trend and reversion should not be traded indiscriminately in the same regime. | Use only pre-trade realized volatility/range/efficiency variables; compare to each strategy alone; penalize parameter search and measure turnover. |

## Important negative evidence already in the repository

- The broad **ES 1-minute price-only** research summary is negative: it reports that breakout/retest, regime switching, mean reversion and a microstructure proxy did not generalize out of sample.
- The local **CL VWAP mean-reversion** pilot for Jan–Feb 2024 changes from modestly positive before costs to negative after modeled commissions/slippage. It is therefore *not* promoted to an edge.
- The ES ORB and NQ intraday-momentum pilots are short. Their headline annualised numbers are not valid forecasts and must not be used on the public site as performance claims.

## Implementation order

1. Harden the current engine with regression tests around existing four strategies and cost model.
2. Run candidate #1 across all ES years with a locked research protocol.
3. Run candidate #6 on CL with executable bid/ask assumptions.
4. Add #3 and #9 as independent, low-complexity research modules.
5. Only then introduce #8; it is the most data-specific and easiest to overfit.

## Data currently required before adding other families

Do **not** start options-volatility, cross-asset relative-value, COT positioning, macro-news, or full multi-contract TSMOM portfolios until we have their underlying data, a continuous-contract/roll specification, and a cost model.

## Sources

[1] Time Series Momentum (Moskowitz, Ooi, Pedersen): https://w4.stern.nyu.edu/facdir/lpederse/papers/TimeSeriesMomentum.pdf

[2] Assessing the profitability of intraday opening range breakout strategies (Holmberg, Lönnbark, Lundström): https://ideas.repec.org/p/hhs/umnees/0845.html

[3] Market intraday momentum (Gao, Han, Li, Zhou): https://www.sciencedirect.com/science/article/abs/pii/S0304405X18301351

[4] Beat the Market: An Effective Intraday Momentum Strategy for S&P500 ETF (Zarattini, Aziz, Barbon; working paper): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4824172

[5] Intra-day Seasonality in Activities of the Foreign Exchange Markets (Ito, Hashimoto; mechanism reference): https://www.nber.org/system/files/working_papers/w12413/w12413.pdf
