# NQ directional screen — permutation benchmark (2023 IS / 2024 OOS)

## Objective

Falsify the previously negative descriptive screen: does its daily directional result differ from a control that randomly reassigns the observed first-30-minute long/short signs across the same days? This is a research control, **not** a trade rule or performance claim.

## Data and split

- Input: `D:/CapoHornLab/projects/capohornlab-website/research/studies/nq_rth_2023_2024/daily_observations.csv` produced from owned NQ one-minute OHLCV.
- RTH convention: weekdays, 09:30–15:59 America/New_York; complete days only.
- Fixed split: 2023 IS and 2024 OOS. The control fits no signal and uses no OOS parameter selection.

## Formula and null

For day $d$, observed gross return in basis points is:

`mean(sign(first30_return_d) × last30_return_d) × 10,000`.

For each sample separately, the null preserves all final-30-minute returns and the exact empirical distribution of first-30-minute signs, then randomly permutes those signs across days without replacement. We use 10,000 deterministic permutations (NumPy PCG64 seed `20260818`). The two-sided Monte-Carlo p-value is `(1 + count(|null| >= |observed|)) / (10000 + 1)`.

## Results

| Sample | Days | Observed gross mean bps/day | Null mean | 5th–95th null interval | Two-sided p | Z vs null |
|---|---:|---:|---:|---:|---:|---:|
| IS_2023 | 244 | -1.388 | 0.075 | -2.590 to 2.760 | 0.3980 | -0.906 |
| OOS_2024 | 245 | -1.669 | 0.044 | -2.852 to 2.882 | 0.3449 | -0.982 |

The screen remains unsuitable for promotion: its observed means are negative, and this test is only a directional-association control rather than an executable cost-aware backtest.

## Costs and limitations

- Gross descriptive returns only: no spread, bid/ask execution, commissions, slippage, market impact, latency, roll handling, or partial fills.
- One-minute OHLCV cannot establish order-flow or order-book imbalance.
- The shuffled-sign null does not cure multiple-hypothesis risk or prove causal predictability.
- Two years of NQ data are too short for robustness claims across contract rolls and market regimes.

## Artifacts

- `permutation_summary.csv`
- `summary.json`
- `nq_directional_permutation_null.png`
