# Capo Horn Lab — Website Project Brief

## Brand
- Name: **Capo Horn Lab**
- Claim: **"Beyond the Market Edge"**
- Language: English (primary)
- Style: Technical, quantitative, modern, premium, minimal, authoritative

## Mission
A website dedicated to backtesting trading strategies on real historical data.
No strategy selling, no indicators, no signals, no subscriptions.

## Core Pages
1. **Home** — Brand intro, value proposition
2. **Chi siamo / About** — Team, mission, methodology
3. **Metodo / Method** — How backtesting works, rigour, data sources
4. **Ricerche / Research** — Published quantitative research with charts
5. **Testa la tua strategia / Test Your Strategy** — Client submission form
6. **Contatti / Contact** — Contact form/info

## Key Module: "Test Your Strategy"
Clients submit:
- Strategy name & description
- Instrument (NQ, ES, other futures)
- Timeframe, historical period
- Entry rules (long/short), exit rules, SL, TP, trailing, BE
- Indicators & params, session times, contracts
- Commissions, slippage, screenshots
- Documents, images, code, notes

Post-submission: confirmation email + viewable in personal area.

## Admin Panel
- View all requests
- Read params, download attachments
- Change status (Inviata, Info mancanti, In valutazione, Accettata, In lavorazione, Completata, Rifiutata)
- Add internal notes
- Request clarifications from client
- Mark test as complete

## Research Page
Publish quantitative research with:
- Objective, hypothesis, instrument, period
- Methodology, data, results
- Charts: equity curve, drawdown, monthly/annual, trade distribution
  Long vs short, by day/hour, profit factor, Sharpe, Monte Carlo
  IS vs OOS, parameter stability
- Interpretation, limitations, conclusions

## Newsletter
For publishing new research, sharing results, explaining method, updates, CTAs

## Visual Identity
- Colors: dark/navy, clean whites, accent for data viz
- Imagery: data, research, markets, technology, navigation, open sea
- **AVOID**: smiling stock traders, luxury cars, money, guru aesthetics

## Data Resources (on D:)
- `D:\marketdata\` — ES, NQ, CL tick data (parquet)
- `D:\marketdata\databento\` — Databento data
- Existing research PDFs in `D:\applicazioni per ricerca\ricerche pdf\`

## Existing Research
1. **ES 1-Minute Quantitative Research Summary** — No price-only edge found
2. **When Structure Meets Reality** — Impulse-retracement-break structures are real but not profitable

## NOT in MVP
- Automated backtesting
- Connection to NinjaTrader / Python / marketdata folder
- Selling strategies, indicators, subscriptions
- Marketplace, live signals, internal chat
- Auto report generation

## Technical Stack (TBD by team)
- Responsive, modern frontend
- Auth system (signup, login, password reset)
- User personal area
- Admin panel
- Newsletter system
