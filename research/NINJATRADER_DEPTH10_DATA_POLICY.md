# NinjaTrader 10-Level Depth Data — Research Policy

## Decision

NinjaTrader data with ten bid and ten ask levels is a useful **order-book-aware research source** for Capo Horn Lab when it is recorded live with complete coverage and documented provenance. It is not automatically equivalent to market-by-order data and must not be described as a queue-accurate execution record.

## Suitable research uses

A validated 10-level depth stream can support:

- top-of-book and depth imbalance;
- spread, midpoint and microprice features;
- liquidity concentration and book slope;
- liquidity withdrawal/replenishment around scheduled releases;
- filters for intraday breakout, mean-reversion and news-event studies;
- conservative fill assumptions that explicitly state their limits.

## Explicit boundaries

Ten-level depth does **not** establish:

- individual order identity or queue position;
- complete order/cancel lifecycle reconstruction;
- exact historical fills, latency or market impact;
- a complete historical news archive.

NinjaTrader documents that Tick Replay should not be used to expect the exact execution sequence of a live strategy. It replays Last market-data events and does not make historical bid/ask volume events available through Tick Replay. Where a provider does not supply bid/ask data tied to Last ticks, NinjaTrader may substitute bid/ask values for consistency. Treat any export as source-specific until verified.

## Collection rule

For live Market Replay collection, Level II depth is recorded only while an eligible NinjaTrader depth-consuming window is open and receiving data for that instrument. Use one monitored collection window per symbol, retain the connection/provider metadata, and log all coverage gaps.

## Required provenance manifest

Every imported day must include:

- symbol and contract;
- source label and feed/connection identifier;
- collection/export mode;
- declared depth: 10 levels per side;
- timezone and trading-session coverage;
- first/last event timestamp and gap report;
- SHA-256 checksum and byte count;
- known quote/data limitations.

The local engine must reject the file when its manifest checksum does not match.

## News-event backtest contract

A news-event request must identify the event family and the entry/exit rule. It can only be evaluated once the dataset provides authoritative scheduled time, first public availability, actual, forecast, prior, revision handling, and source evidence. Post-release returns are retrospective research outcomes; they are never features available before release.

## Website intake choices

The Test Your Strategy wizard offers three request modes:

1. **Tick & trades** — price, volume and time-based research.
2. **10-level market depth** — liquidity and imbalance research; no claim of queue position or exact fills.
3. **News-event study** — scheduled-release response research, with event family and explicit rule captured in the request.

## Sources

- NinjaTrader Market Replay recording: https://ninjatrader.com/support/helpguides/nt8/set_up12.htm
- NinjaTrader Tick Replay limits: https://ninjatrader.com/support/helpguides/nt8/developing_for__tick_replay.htm
- NinjaTrader data-provider limitations: https://ninjatrader.com/support/helpguides/nt8/data_by_provider.htm
