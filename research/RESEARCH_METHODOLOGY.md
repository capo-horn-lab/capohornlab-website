# Capo Horn Lab — Standard Research Methodology

## Research Protocol

Every strategy study follows this standardized pipeline:

### Phase 1: Strategy Decomposition
- Extract the exact entry/exit rules from the strategy description
- Identify all parameters (indicators, thresholds, time filters)
- Document assumptions and edge cases
- Determine data requirements (instrument, timeframe, depth)

### Phase 2: Data Selection
- Select appropriate data tier (OHLC, Trades, MBP-1, MBP-10, MBO)
- Define IS (In-Sample) and OOS (Out-Of-Sample) periods
- Ensure no lookahead bias in data alignment

### Phase 3: Backtest Execution
- Code the strategy rules exactly as specified
- Run IS period to calibrate
- Run OOS period unchanged
- Benchmark against random entries

### Phase 4: Profitability Segmentation
- Split equity curve into profitable vs drawdown regimes
- Identify market conditions for each regime (volatility, direction, volume)
- Measure: Sharpe, CAGR, Max DD, Win Rate, Profit Factor, N Trades
- Statistical significance test (p-value, Monte Carlo)

### Phase 5: Final Report
- Objective and hypothesis
- Methodology and data
- Results with full statistics
- Profitability/drawdown regime analysis
- Verdict: Profitable, Not Profitable, or Inconclusive

## Protocol giallo per richieste cliente
Il cliente descrive la strategia → noi la decomponiamo e testiamo → produciamo report completo con grafici → il report viene pubblicato nella sua area personale.
