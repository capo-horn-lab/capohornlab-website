# Capo Horn Lab — Observatory Copy Rewrite
## Afrodite // Copy Audit & Recommendations
Date: 2026-08-24
Task: chl-20260824-0005

---

## Executive Summary

The current copy is already well above average for a quantitative research brand — it is direct, avoids motivational fluff, and anchors claims in specific deliverables. This audit identifies three categories of improvement:

1. **Security issues** — internal data-provider names exposed in public copy (must fix)
2. **Tightening opportunities** — wording that can be sharper, more specific, less generic
3. **Identity alignment** — places where the Observatory brand can be reinforced without decorative hype

No page requires a full rewrite. Most changes are surgical.

---

## 1. HOMEPAGE (index.html)

### 1.1 Hero Section

**Location:** Lines 1583–1590

**Current H1:**
> Strategies don't lie. Markets reveal the truth.

**Assessment:** "The truth" is abstract. Capo Horn Lab's real differentiator is the rigour of the testing — not that it tells the truth (everyone claims that), but *how* it arrives at its conclusions.

**Recommended H1:**
> Strategies don't lie. Markets expose what works.

**Rationale:** "What works" is outcome-oriented and aligns with the backtesting service. It promises a result the reader wants — knowing whether their strategy holds up — rather than an abstract virtue.

**Current sub-copy:**
> We run your trading idea through institutional-grade backtests with real tick data, Monte Carlo validation, and honest reporting. No hype. No fake Sharpe ratios. Just truth.

**Problems:**
- "honest reporting" is a claim that must be demonstrated, not stated
- "Just truth" is an empty closer that many brands use
- "No hype. No fake Sharpe ratios." is actually strong — it names a specific enemy

**Recommended sub-copy:**
> Your strategy, tested on tick-level data with IS/OOS splits, Monte Carlo simulation, and realistic fills. Results come back as they are — no sugar-coating.

**Rationale:** Front-loads the specific methodology. "As they are" is more grounded than "honest." The specific deliverables (IS/OOS splits, tick-level data, realistic fills) do the persuasion work — they demonstrate rigour without having to claim it.

### 1.2 Hero Metrics (Lines 1595–1612)

**Current:**
- "10B+ Ticks Analyzed"
- "6 Futures Markets"
- "16 Verified Studies"
- "8-Gate Verification Pipeline"

**Issue:** "10B+ Ticks Analyzed" is unverifiable by a visitor and reads as vanity metric. The other three are concrete and defensible.

**Recommended:**
- Remove "10B+ Ticks Analyzed"
- Keep "6 Futures Markets", "16 Verified Studies", "8-Gate Verification Pipeline"
- Replace the removed metric with something rooted in methodology, not scale:
  - Option: "IS/OOS Validated" or "Tick-Level Precision"
  - Recommend: **"Tick-Level Data"** — states the data quality without claiming a volume

### 1.3 "What We Stand For" Comparison Table (Lines 1788–1853)

**Current "are" item (Line 1801):**
> Institutional-grade tick data (Databento)

**CRITICAL ISSUE:** Databento is an internal data provider. This name must not appear in public-facing copy. It signals internal supplier relationships and cost structure.

**Fix:**
> Institutional-grade tick data

Remove the parenthetical entirely. The data quality claim stands without naming the supplier.

### 1.4 Newsletter Section (Lines 1862–1878)

**Current heading:**
> Stay Ahead of the Curve

**Assessment:** Generic. Every newsletter says this.

**Recommended:**
> New Research, No Noise

**Rationale:** Short. Specific. Contrasts the signal/noise framing already present in the brand.

**Current sub-copy (Line 1867):**
> Get notified when new research is published. No spam, no strategy pitches — just raw data and honest analysis delivered to your inbox.

**Recommended sub-copy:**
> Receive our published studies as they come out. No pitches, no trade alerts — just the research and the data.

**Rationale:** "Raw data and honest analysis" is a claim. "The research and the data" is a description of what you actually receive.

### 1.5 Footer Tagline (Line 1892)

**Current:**
> Quantitative backtesting and strategy research. Data-driven, not guru-driven.

**Assessment:** Good. Keep as is.

### 1.6 Missing: Motto

The GODMODE brief states the motto is:
> Beyond the hedge of the market

This motto does not currently appear in the HTML. The meta title says "Beyond the Market Edge" which is close but not identical.

**Recommendation:** Add the correct motto as a visual element — possibly in the hero section beneath the H1, or in the footer next to the brand name. Use weight-300 Inter, small size, high tracking — sotto voce, not shouty.

---

## 2. TEST-STRATEGY PAGE (test-strategy.html)

### 2.1 Pre-Auth Hero (Lines 1439–1444)

**Current:**
> Describe your strategy. We will backtest it on tick-level historical data. You get a full quantitative report with equity curve, Sharpe ratio, drawdown analysis, and Monte Carlo simulation.

**Assessment:** Functional. Clear. No fluff. Good.

**Minor recommendation — tighten slightly:**
> Describe your strategy. We backtest it on tick-level data. You receive a quantitative report with equity curve, Sharpe ratio, drawdown analysis, and Monte Carlo simulation — plus a clear verdict.

**Rationale:** "We will" → "We" is slightly more confident. Adding "plus a clear verdict" reinforces the differentiation (no sugar-coating). The rest works as-is.

### 2.2 Wizard Guidance Boxes

**Assessment:** The guidance copy in the wizard steps is exceptionally good — precise, instructive, no fluff. The "💡" icons are acceptable given the instructional context. No changes needed.

**Notable strong copy:**
- "Precision matters. A strategy described as 'buy when it goes up' cannot be tested." (Step 1)
- "Honest slippage matters. The biggest gap between backtest and live trading is execution." (Step 5)
- "Detail is better than brevity." (Step 3)

### 2.3 Data Mode Descriptions (Lines 1621–1623)

**Current:**
> 10-level market depth — liquidity and imbalance research

**Assessment:** Specific and honest about what depth data can and cannot do. No overclaiming. No changes needed.

**Current disclaimer (Line 1625):**
> 10-level depth is used for liquidity and imbalance research; it does not claim queue position or exact fills.

**Assessment:** Excellent. This is the kind of honest scoping that builds trust. No changes needed.

---

## 3. PRICING PAGE (pricing.html)

### 3.1 Hero (Lines 1207–1211)

**Current:**
> Transparent pricing for institutional-grade quantitative research and multi-tier backtesting services. Subscribe for research or commission a backtest — no lock-in, no hidden fees.

**Issues:**
- "institutional-grade" appears again — slightly buzzy
- "commission a backtest" feels transactional

**Recommended:**
> Research subscriptions and backtesting services. Transparent pricing, no lock-in, no hidden fees.

**Rationale:** Shorter. The value is in the simplicity. The research and backtest pages already explain the quality.

### 3.2 Research Subscription Badge (Line 1248)

**Current:**
> Zero-Profit · 100% reinvested

**Assessment:** Acceptable. This is a funding model statement, not internal economics. It signals alignment of incentives. Keep.

### 3.3 Data + Backtest Section Header (Line 1273)

**Current:**
> Market data is a one-time acquisition — you own it, you backtest it, forever. Each backtest run costs €3–5, covering only the compute. No subscription, no markup.

**Issue:** "covering only the compute" — this edges into internal cost structure.

**Recommended:**
> Market data is a one-time acquisition — you own it, you backtest it, forever. Each backtest run costs €3–5. No subscription, no markup.

**Rationale:** The price stands on its own. Explaining *why* it costs €3–5 (compute costs) is internal economics territory. Remove the justification; let the price speak.

### 3.4 Backtest Card Description (Line 1312)

**Current:**
> Compute cost only. No markup, no margin, no subscription.

**Same issue** — "compute cost only" is internal.

**Recommended:**
> €3–5 per test. No markup, no subscription.

### 3.5 Bottom Info Box (Lines 1325–1331)

**Current:**
> Own your data, own your edge. Data is a one-time purchase — you own it, you backtest it, forever. No recurring fees, no forced subscriptions. Every backtest run costs €3–5, covering only the compute. 100% transparent, 100% research-funded.

**Issues:**
- "covering only the compute" again
- "100% transparent, 100% research-funded" — "research-funded" is acceptable identity; "100% transparent" is a claim

**Recommended:**
> Own your data, own your edge. Data is a one-time purchase — you own it, you backtest it, forever. No recurring fees, no forced subscriptions. Backtests run at €3–5 per test.

### 3.6 CTA Section Header (Line 1447)

**Current:**
> Ready to Get Started?

**Assessment:** Generic.

**Recommended:**
> Start Testing

**Rationale:** Action verb. No question mark. Fits the Observatory identity — these are professionals, not browsers.

### 3.7 CTA Sub-copy (Line 1448)

**Current:**
> Subscribe for full research access, or choose a backtest tier and start running institutional-grade analysis on your strategies today.

**Recommended:**
> Subscribe for full research access or begin backtesting your strategy.

**Rationale:** Removes "institutional-grade" (buzzword). Removes "today" (urgency padding). Shorter is more confident.

### 3.8 FAQ Assessment

The FAQ copy is excellent — direct, honest about what's included and what's not, covers the mechanics clearly. No changes needed.

---

## 4. CROSS-PAGE: "Institutional-Grade" Audit

The phrase "institutional-grade" appears in:
- index.html meta description: "...institutional-grade analytics"
- test-strategy.html meta: "...institutional-grade backtesting engine"
- pricing.html meta: "...institutional-grade quantitative research"
- pricing.html hero: "...institutional-grade quantitative research"
- pricing.html CTA: "...institutional-grade analysis"

**Finding:** The term is repeated across meta tags and body copy. It is a claim, and it's becoming a crutch. Capo Horn Lab demonstrates institutional-grade through its specific methodology (tick-level data, IS/OOS, Monte Carlo) — it should not need to claim it.

**Recommendation:** Reduce to at most one use per page. Prefer the methodology specifics over the label.

---

## 5. ACCEPTANCE CRITERIA CHECK

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Name "Capo Horn Lab" preserved | PASS | Unchanged in all recommendations |
| Motto "Beyond the hedge of the market" | FLAG | Currently absent from HTML. Recommend adding. |
| Copy is concise, serious, no decorative hype | PASS | All recommendations reduce word count and remove claims |
| No internal provider/cost/markup language | FLAG | "Databento" found in index.html L1801 (must remove). "covering only the compute" / "compute cost only" found in pricing.html (must remove) |
| Result envelope written | PENDING | Will write after copy artifact |

---

## 6. PATCH SEQUENCE (if authorized to apply)

If Francesco authorizes direct application, the following changes are patch-ready:

### 6.1 CRITICAL (provider exposure):
- index.html L1801: Remove "(Databento)"
- pricing.html L1273: "covering only the compute. " → ""
- pricing.html L1312: "Compute cost only. " → ""
- pricing.html L1327-1330: Remove "covering only the compute. "
- pricing.html L1327-1330: Remove "100% transparent, 100% research-funded."

### 6.2 RECOMMENDED (tightening):
- index.html L1584: H1 → "Strategies don't lie. Markets expose what works."
- index.html L1586-1589: Sub-copy → tightened version
- index.html L1595-1612: Remove "10B+ Ticks Analyzed" metric, replace with "Tick-Level Data"
- index.html L1865: "Stay Ahead of the Curve" → "New Research, No Noise"
- index.html L1866-1868: Newsletter sub-copy → tightened
- pricing.html L1207-1210: Hero sub-copy → tightened
- pricing.html L1447-1448: CTA heading + sub → tightened
- index.html: Add motto "Beyond the hedge of the market" to hero or footer

### 6.3 OPTIONAL (identity):
- Reduce "institutional-grade" occurrences across meta tags and body

---

## 7. WHAT NOT TO CHANGE

The following copy is strong and should be preserved:
- All wizard guidance box text (test-strategy.html) — precise, instructive, honest
- "Own the Raw Tick Data" and "Test on Your Data" backtest cards (pricing.html) — clear, differentiated
- "What We Are / What We Are Not" comparison table (index.html) — one of the strongest sections
- All FAQ entries (pricing.html) — thorough and transparent
- Footer tagline "Data-driven, not guru-driven" — ownable, memorable
- Data mode descriptions with honest constraints (test-strategy.html)
- "No sugar-coating" — consistent, distinctive voice element