# News-aware Market Data Engine — v0.1

## Goal

Build a research engine that reproduces **observed** market behaviour from owned event data, then measures responses around verifiable news releases. It does not simulate a market from invented prices, and it does not treat a news label as a tradable prediction.

## What is implemented

### 1. Source-event processing

`research/market_data_engine.py` converts individual source-sided trades into event-time OHLCV bars with:

- UTC timestamp normalization;
- explicit positive-price and positive-size validation;
- counters for out-of-order events and unknown source sides;
- exact-event deduplication only;
- source-sequence reuse recorded but **not** treated as a duplicate, because real NQ source data contains distinct prints that can share a sequence;
- no forward-filled or synthetic empty bars;
- OHLC, volume, trade count, source-side volume, signed volume and normalized imbalance;
- per-run provenance (`symbol`, source, timeframe, side-map) and quality counters;
- optional DST-aware CME Globex equity-index session rules: 17:00 America/Chicago session start, 16:00–17:00 local maintenance-break rejection, and a stable local `session_date` label across the UTC daylight-saving shift.

The CME rule is deliberately narrow: it does **not** claim holiday/early-close coverage, product-specific halts, contract-roll mapping, or a complete venue calendar. A source event inside the regular maintenance break fails closed instead of being silently assigned to a session.

`B`/`A` side labels remain *source-provided classifications*. They are deliberately not described as executable aggressor flow until their precise provider semantics are separately validated.

### 2. Look-ahead-safe calendar

`research/news_calendar.py` requires every economic event to carry:

- immutable `event_id`;
- `release_time_utc` and `available_at_utc` as timezone-aware UTC values;
- event family/category/importance;
- authoritative source and source URL.

For strategy features, only records whose `available_at_utc <= bar_timestamp` enter the feature set. Retrospective post-release returns are written with the explicit label `post_release_outcome_not_a_signal`; they cannot be used as contemporaneous inputs.

## Initial authoritative public calendar registry

`research/news_calendar_sources.json` contains ingestion contracts for four public sources:

- BLS publishes a release calendar and an ICS subscription; it identifies scheduled releases including CPI, employment, JOLTS and PPI, with times stated in Eastern Time.[1]
- The Federal Reserve publishes FOMC meeting calendars, statements and minutes; the calendar documents eight regular meetings per year and historical material.[2]
- BEA publishes dated, timed GDP, Personal Income/Outlays (including PCE), and trade releases.[3]
- EIA publishes the WPSR schedule, normally Wednesday 10:30 ET with documented holiday exceptions; this is the initial CL-specific release family.[4]

## News-trading research contract

Every future event study must store the following separately:

| Field | Rule |
|---|---|
| Scheduled time | Original official scheduled timestamp, UTC normalized |
| First availability | Earliest verifiable public timestamp; do not substitute a later article date |
| Actual / forecast / prior | Versioned values, units and source; preserve revisions |
| Source evidence | URL, retrieval time, source hash/version where practical |
| Market response | Predefined baseline and post-event windows; output only as retrospective label |
| Execution constraints | Bid/ask, spread, slippage, latency, position and session rules — no midpoint-fill fiction |
| Split | Calendar/time split fixed before fitting; no future events in features |

## Coverage boundary

No public browser collection can honestly claim to contain *all* market-impacting news. The current registry is an authoritative scheduled-release layer, not a complete historical newswire. A complete historical headline layer needs a licensed archive with publication timestamps, revisions, and rights to retain/use content. The registry names these gaps explicitly instead of filling them with scraped headlines or guessed timestamps.

## Next implementation gates

1. Add deterministic parquet read/write and file checksum provenance.
2. Build a source adapter for the BLS ICS calendar, preserving source timezone and observed retrieval time.
3. Add historical events only when `available_at_utc`, actual/forecast/prior and source evidence are all present.
4. Join calendar events to NQ/ES/CL bars for retrospective event studies, then test each hypothesis with fixed IS/OOS windows and realistic execution inputs.

## Sources

[1] BLS selected releases schedule — https://www.bls.gov/schedule
[2] Federal Reserve FOMC calendar — https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
[3] BEA release schedule — https://www.bea.gov/news/schedule
[4] EIA WPSR schedule — https://www.eia.gov/petroleum/supply/weekly/schedule.php
