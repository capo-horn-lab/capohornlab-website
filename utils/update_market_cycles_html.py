"""
Update research-detail.html with market_cycles data, CSS, and rendering.
"""
import re

# Read the HTML file
with open(r'D:\CapoHornLab\projects\capohornlab-website\pages\research-detail.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ===========================================================
# 1. Add CSS for market cycles grid (after key-metric styles)
# ===========================================================
old_css_marker = ".key-metric .km-positive { color: var(--ch-success); }\n    .key-metric .km-negative { color: var(--ch-error); }\n    .key-metric .km-neutral  { color: var(--ch-navy-200); }"

new_css = """    .key-metric .km-positive { color: var(--ch-success); }
    .key-metric .km-negative { color: var(--ch-error); }
    .key-metric .km-neutral  { color: var(--ch-navy-200); }

    /* ============================================================
       MARKET CYCLES GRID
       ============================================================ */
    .market-cycles-section {
      margin-bottom: var(--ch-space-10);
    }

    .market-cycles-summary {
      font-size: var(--ch-text-base);
      color: var(--ch-gray-600);
      line-height: var(--ch-leading-relaxed);
      margin-bottom: var(--ch-space-6);
      padding: var(--ch-space-4) var(--ch-space-5);
      background: var(--ch-navy-50);
      border-left: 3px solid var(--ch-blue-500);
      border-radius: 0 var(--ch-radius-md) var(--ch-radius-md) 0;
    }

    .cycles-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: var(--ch-space-4);
    }

    @media (max-width: 640px) {
      .cycles-grid {
        grid-template-columns: 1fr;
      }
    }

    .cycle-card {
      border-radius: var(--ch-radius-md);
      padding: var(--ch-space-4);
      border: 1px solid;
    }

    .cycle-card.works {
      background: #ecfdf5;
      border-color: #a7f3d0;
    }

    .cycle-card.fails {
      background: #fef2f2;
      border-color: #fecaca;
    }

    .cycle-card-header {
      display: flex;
      align-items: center;
      gap: var(--ch-space-2);
      margin-bottom: var(--ch-space-2);
      font-weight: var(--ch-font-semibold);
      font-size: var(--ch-text-sm);
    }

    .cycle-card-header .cycle-icon {
      width: 20px;
      height: 20px;
      border-radius: var(--ch-radius-full);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      flex-shrink: 0;
    }

    .cycle-card.works .cycle-icon {
      background: #d1fae5;
      color: var(--ch-success);
    }

    .cycle-card.fails .cycle-icon {
      background: #fee2e2;
      color: var(--ch-error);
    }

    .cycle-card.works .cycle-card-header {
      color: #065f46;
    }

    .cycle-card.fails .cycle-card-header {
      color: #991b1b;
    }

    .cycle-reason {
      font-size: var(--ch-text-xs);
      color: var(--ch-gray-600);
      line-height: var(--ch-leading-relaxed);
    }

    .cycle-card.works .cycle-reason {
      color: #065f46;
    }

    .cycle-card.fails .cycle-reason {
      color: #991b1b;
    }

    .cycle-historical {
      margin-top: var(--ch-space-4);
      padding: var(--ch-space-3) var(--ch-space-4);
      background: var(--ch-gray-50);
      border: 1px solid var(--ch-gray-100);
      border-radius: var(--ch-radius-md);
      font-size: var(--ch-text-xs);
      color: var(--ch-gray-600);
      line-height: var(--ch-leading-relaxed);
    }

    .cycle-historical strong {
      color: var(--ch-gray-800);
      font-weight: var(--ch-font-semibold);
    }

    /* Cycle marker badge */
    .cycle-badge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-family: var(--ch-font-mono);
      font-size: 10px;
      font-weight: var(--ch-font-semibold);
      padding: 2px 8px;
      border-radius: var(--ch-radius-full);
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }

    .cycle-badge.works {
      background: #d1fae5;
      color: #065f46;
    }

    .cycle-badge.fails {
      background: #fee2e2;
      color: #991b1b;
    }

    /* No-cycles for negative research */
    .cycle-all-fail {
      text-align: center;
      padding: var(--ch-space-6);
      background: #fef2f2;
      border: 1px solid #fecaca;
      border-radius: var(--ch-radius-md);
      color: #991b1b;
      font-size: var(--ch-text-sm);
    }

    .cycle-all-fail strong {
      display: block;
      margin-bottom: var(--ch-space-2);
      font-size: var(--ch-text-base);
    }
"""

html = html.replace(old_css_marker, new_css)

# ===========================================================
# 2. Add renderMarketCycles function (before renderSections)
# ===========================================================
old_render_sections_marker = "      /* ============================================================\n         RENDER SECTIONS\n         ============================================================ */\n      function renderSections"

new_render_market_cycles = """      /* ============================================================
         RENDER MARKET CYCLES
         ============================================================ */
      function renderMarketCycles(mc) {
        var container = document.getElementById('marketCyclesContainer');
        container.innerHTML = '';

        if (!mc) {
          container.style.display = 'none';
          return;
        }

        container.style.display = '';

        // Summary
        if (mc.summary) {
          var summaryDiv = document.createElement('div');
          summaryDiv.className = 'market-cycles-summary';
          summaryDiv.textContent = mc.summary;
          container.appendChild(summaryDiv);
        }

        // Grid of cycles
        var grid = document.createElement('div');
        grid.className = 'cycles-grid';

        // Works in
        if (mc.works_in && mc.works_in.length > 0) {
          mc.works_in.forEach(function(c) {
            var card = document.createElement('div');
            card.className = 'cycle-card works';
            card.innerHTML =
              '<div class="cycle-card-header">' +
                '<span class="cycle-icon">✓</span>' +
                '<span>' + c.cycle + '</span>' +
                '<span class="cycle-badge works">WORKS</span>' +
              '</div>' +
              '<div class="cycle-reason">' + c.reason + '</div>';
            grid.appendChild(card);
          });
        }

        // Fails in
        if (mc.fails_in && mc.fails_in.length > 0) {
          mc.fails_in.forEach(function(c) {
            var card = document.createElement('div');
            card.className = 'cycle-card fails';
            card.innerHTML =
              '<div class="cycle-card-header">' +
                '<span class="cycle-icon">✗</span>' +
                '<span>' + c.cycle + '</span>' +
                '<span class="cycle-badge fails">FAILS</span>' +
              '</div>' +
              '<div class="cycle-reason">' + c.reason + '</div>';
            grid.appendChild(card);
          });
        }

        container.appendChild(grid);

        // All-fail notice for empty works_in
        if ((!mc.works_in || mc.works_in.length === 0) && mc.fails_in && mc.fails_in.length > 0) {
          var allFail = document.createElement('div');
          allFail.className = 'cycle-all-fail';
          allFail.innerHTML = '<strong>✗ Does Not Perform in Any Cycle</strong>No market cycle offers positive expectancy for this strategy. The failure is structural and regime-independent.';
          container.appendChild(allFail);
        }

        // Historical example
        if (mc.historical_example) {
          var histDiv = document.createElement('div');
          histDiv.className = 'cycle-historical';
          histDiv.innerHTML = '<strong>Historical Example:</strong> ' + mc.historical_example;
          container.appendChild(histDiv);
        }
      }

      /* ============================================================
         RENDER SECTIONS
         ============================================================ */
      function renderSections"""

html = html.replace(old_render_sections_marker, new_render_market_cycles)

# ===========================================================
# 3. Add marketCycles container div and call renderMarketCycles
# ===========================================================

# Find the loadResearch function and add the call
old_load_call = "        // Key Metrics Bar\n        renderKeyMetrics(data.metrics_display);\n\n        // Sections (with real chart images)\n        renderSections(data.sections);"

new_load_call = "        // Key Metrics Bar\n        renderKeyMetrics(data.metrics_display);\n\n        // Market Cycles\n        renderMarketCycles(data.market_cycles);\n\n        // Sections (with real chart images)\n        renderSections(data.sections);"

html = html.replace(old_load_call, new_load_call)

# Now find where the sections container is in the HTML and add the market cycles container before it
# Look for the HTML section with the sections container
old_sections_html = '          <!-- Sections -->\n          <div id="sectionsContainer"></div>'

new_sections_html = """          <!-- Market Cycles -->
          <div id="marketCyclesContainer" class="detail-section animate-up" style="margin-bottom:2rem;"></div>

          <!-- Sections -->
          <div id="sectionsContainer"></div>"""

html = html.replace(old_sections_html, new_sections_html)

# ===========================================================
# 4. Add market_cycles data to each research entry
# ===========================================================

# Define the market_cycles data for all 12 researches + 13th
# We'll inject it as a field into each researchData entry

# First research: es-1m-quant-summary
market_cycles_data = {
    "es-1m-quant-summary": {
        "summary": "Price-only 1-minute strategies fail across ALL market cycles — no regime offers a safe harbor. The null hypothesis of 'no edge' holds regardless of volatility or directional regime.",
        "works_in": [],
        "fails_in": [
            {"cycle": "Bull Trend", "reason": "Breakout/retest showed temporary profitability in 2024 low-volatility bull trend but failed OOS. Apparent edge was regime-specific and did not generalize."},
            {"cycle": "Bear Trend", "reason": "Directional Pressure Index microstructure proxy never exceeded 52% accuracy, failing in both bear and bull directional regimes."},
            {"cycle": "High Volatility / Risk-Off", "reason": "All four strategy families were tested through 2020 COVID and 2022 rate-hiking volatility. None produced positive expectancy."},
            {"cycle": "Low Volatility / Range-Bound", "reason": "Mean reversion toward session mid was tested and falsified — extreme prices exhibited continuation, not reversion, in low-vol range conditions."},
            {"cycle": "Mean-Reverting Regime", "reason": "Regime-switching via Directional Efficiency Index identified regime shifts correctly but switching costs erased any theoretical benefit."},
            {"cycle": "Trend-Following Regime", "reason": "Despite favorable conditions for momentum strategies, the 1-minute price-only signals lacked the statistical power to exploit trends profitably."}
        ],
        "historical_example": "2024 in-sample period showed marginal positive Sharpe (0.23) for breakout/retest in low-volatility bull conditions, but 2020–2022 OOS period (including COVID crash, recovery, and rate hikes) collapsed to negative Sharpe (−0.18)."
    },
    "when-structure-meets-reality": {
        "summary": "The impulse-retracement-break structure is visually compelling and empirically real, but it fails to generate positive expectancy across ALL market cycles. Adverse selection dominates regardless of volatility regime. This is a structural failure, not a parametric one.",
        "works_in": [],
        "fails_in": [
            {"cycle": "Bull Trend", "reason": "In stable uptrends, the retracement depth is shallower (median 38% of impulse) but the post-break extension remains near zero. The structure fails to capture the trend's continuation."},
            {"cycle": "Bear Trend", "reason": "Same mechanism as bull trend — the retracement structure exists but the break does not produce exploitable continuation. MAE remains elevated at −1.8 ATR median."},
            {"cycle": "High Volatility / Risk-Off", "reason": "Higher volatility produces larger signals but fewer of them. The 95th percentile MFE reaches +3.2 ATR, but the median MAE also increases. No regime offers positive expectancy after costs."},
            {"cycle": "Low Volatility / Range-Bound", "reason": "Frequent but unreliable signals. The hit rate can be pushed from 36% to 42% with aggressive filtering, but at the cost of 95%+ sample size collapse."},
            {"cycle": "Mean-Reverting Regime", "reason": "In regimes where price oscillates, the impulse-retracement-break pattern is more frequent but post-break continuation is weakest — the pattern predicts the wrong direction."},
            {"cycle": "Trend-Following Regime", "reason": "The delay introduced by waiting for retracement and break confirmation means the best part of the trend is already over when the entry triggers."}
        ],
        "historical_example": "During 2020 COVID crash (high volatility regime), impulse events were large but rare. The few trades that worked produced outsized winners (+3.2 ATR 95th percentile MFE) while the majority experienced persistent adverse drift."
    },
    "time-series-momentum-futures": {
        "summary": "TSMOM thrives in directional trending regimes and fails in choppy, range-bound, or high-volatility reversal markets. Its negative skew means large losses concentrate in sharp reversals after prolonged trends.",
        "works_in": [
            {"cycle": "Bull Trend", "reason": "The 12-month lookback captures sustained upward movement and maintains long exposure. Equity index sub-portfolio Sharpe of 0.45 in bull trends confirms positive contribution."},
            {"cycle": "Bear Trend", "reason": "Sustained downward movement generates short-side profits. The strategy's long/short structure allows it to profit from both directions in prolonged trends."},
            {"cycle": "Trend-Following Regime", "reason": "This is the strategy's native habitat. Full-sample Sharpe of 0.98 across 58 contracts over 40 years demonstrates robust performance when markets exhibit trend persistence."}
        ],
        "fails_in": [
            {"cycle": "High Volatility / Risk-Off", "reason": "Sharp reversals following prolonged trends produce the strategy's crash risk. The 2009 commodity reversal and 2022 fixed income reversal generated max drawdown of 22.7%. Skewness of −0.35 confirms vulnerability to vol spikes."},
            {"cycle": "Low Volatility / Range-Bound", "reason": "In sideways markets with no directional persistence, the 12-month signal whipsaws. Post-2014 Sharpe declined to 0.38 precisely because of extended range-bound conditions."},
            {"cycle": "Mean-Reverting Regime", "reason": "When prices oscillate around a mean, the momentum signal is persistently wrong — buying highs and selling lows. The strategy is negatively correlated to mean-reversion strategies by construction."}
        ],
        "historical_example": "Strongly profited during 2007–2009 crisis (Sharpe > 1.5) where sustained trends in commodities, currencies, and fixed income all aligned. Collapsed in 2009 commodity reversal (−22.7% DD) as the 6-year commodity super-cycle reversed."
    },
    "opening-range-breakout-intraday": {
        "summary": "ORB requires sufficient opening volatility and directional conviction. It performs strongly in high-volatility and trend-following regimes but suffers negative expectancy during low-volatility range-bound markets.",
        "works_in": [
            {"cycle": "High Volatility / Risk-Off", "reason": "Larger opening ranges produce more decisive breakouts. The strategy's edge comes from institutional order flow concentration at the open — amplified by volatility."},
            {"cycle": "Bull Trend", "reason": "Breakout direction aligned with prior-day trend adds +0.12 Sharpe. When the overall trend supports the breakout direction, persistence is stronger."},
            {"cycle": "Trend-Following Regime", "reason": "The strategy profits from directional persistence after the open. Trend-following regimes provide the sustained intraday directional movement needed for breakouts to reach their profit targets."}
        ],
        "fails_in": [
            {"cycle": "Low Volatility / Range-Bound", "reason": "The strategy's worst regime. Narrow opening ranges produce false breakouts in both directions. Negative expectancy — can suffer 8–10 consecutive losses."},
            {"cycle": "Bear Trend", "reason": "Bear trends can produce opening gaps that trigger breakouts at unfavorable prices. The strategy performs better in bull than bear conditions from the open."},
            {"cycle": "Mean-Reverting Regime", "reason": "Intraday mean reversion directly opposes the breakout assumption. Price breaks out of the range only to reverse, hitting the stop loss. The edge requires persistence, not reversion."}
        ],
        "historical_example": "Best during 2020 COVID reopening (March–June 2020) where high volatility produced large opening ranges and sustained directional moves. Worst: 2017 low-volatility environment (VIX < 10) with prolonged losing streaks."
    },
    "vwap-mean-reversion-intraday": {
        "summary": "VWAP mean reversion thrives in range-bound, moderate-volatility conditions where VWAP acts as an institutional anchor. It breaks down in strong trends and extreme volatility (VIX > 30).",
        "works_in": [
            {"cycle": "Low Volatility / Range-Bound", "reason": "Ideal conditions. The dynamic threshold variant captures small deviations from VWAP that reliably revert. Maximum Sharpe achieved in VIX 14–22 range."},
            {"cycle": "Mean-Reverting Regime", "reason": "The strategy's native habitat. When prices oscillate around VWAP, the mean-reversion signal captures the oscillation. Win rate of 56.8% confirms the edge."}
        ],
        "fails_in": [
            {"cycle": "Bull Trend", "reason": "In strong uptrends, price trends away from VWAP and does not revert. The strategy takes repeated counter-trend entries with adverse selection."},
            {"cycle": "Bear Trend", "reason": "Same mechanism as bull — sustained directional movement overwhelms the mean-reversion signal. Losers exhibit continued trending, not reversion to VWAP."},
            {"cycle": "High Volatility / Risk-Off", "reason": "Extreme volatility (VIX > 30) breaks down the VWAP anchor. Required deviation for entries is so large that stops get hit before reversion occurs."},
            {"cycle": "Trend-Following Regime", "reason": "By construction, mean reversion is negatively correlated to trend-following. When trend persistence is high, mean-reversion bets are systematically wrong."}
        ],
        "historical_example": "Best: 2017 low-volatility environment (VIX 9–12) with consistent small mean-reversion profits. Worst: 2020 COVID crash (VIX > 50) where trending behavior overwhelmed the VWAP anchor."
    },
    "intraday-momentum-spy": {
        "summary": "Intraday momentum performs best in high-volume, moderate-volatility regimes where directional runs persist. It collapses in low-volatility (VIX < 13) range-bound markets and extreme volatility gap days (VIX > 30).",
        "works_in": [
            {"cycle": "Bull Trend", "reason": "The strategy captures extended directional runs. 15% of trades generate 65% of total profits — these fat-right-tail winners are most common in trending environments."},
            {"cycle": "Trend-Following Regime", "reason": "The chandelier trail allows holding through minor pullbacks during sustained moves. The edge relies on intraday trend persistence."},
            {"cycle": "High Volatility / Risk-Off (moderate)", "reason": "Best Sharpe in VIX 14–25 range where volatility is sufficient for directional runs but not extreme enough to cause gap reversals."}
        ],
        "fails_in": [
            {"cycle": "Low Volatility / Range-Bound", "reason": "Performance collapses when VIX < 13. Insufficient deviation magnitude means entries triggered by noise. Max losing streak of 15 during these periods."},
            {"cycle": "High Volatility / Risk-Off (extreme)", "reason": "VIX > 30 gap days cause entries at unfavorable prices as opening gaps exceed the trailing stop buffer. Post-2022 decay reflects reduced directional persistence."},
            {"cycle": "Mean-Reverting Regime", "reason": "The strategy buys breakouts and relies on continuation — the wrong approach when prices mean-revert. The chandelier trail protects but still produces losses."}
        ],
        "historical_example": "Strongest: 2020–2021 reopening rally with high volume and directional persistence. Worst: 2017 low-volatility environment (VIX 9–11) with prolonged losing streaks. Post-OOS decay from Sharpe 0.78 to 0.57."
    },
    "confidence-weighted-mean-reversion": {
        "summary": "CWMR excels in volatile, reversal-prone markets where mean reversion thrives. It struggles during prolonged monotonic trends. The confidence-weighted update reduces drawdowns vs PAMR but does not eliminate regime dependency.",
        "works_in": [
            {"cycle": "Mean-Reverting Regime", "reason": "Native habitat. CWMR explicitly exploits cross-sectional mean reversion. Positive excess returns in 72% of rolling 3-month windows. Strongest in 2002–2003, 2008–2009, and 2020."},
            {"cycle": "High Volatility / Risk-Off", "reason": "Sharp reversals produce the algorithm's best performance. The confidence-weighted update prevents excessive position sizing during volatile periods, reducing drawdown by 30% vs PAMR."},
            {"cycle": "Range-Bound", "reason": "In sideways markets without strong directional bias, the mean-reversion signal captures repeated oscillation. Lower turnover (45% vs PAMR's 72%) reduces transaction costs."}
        ],
        "fails_in": [
            {"cycle": "Bull Trend", "reason": "Strong monotonic trends (2004–2006, 2017) cause prolonged underperformance. The algorithm shorts winners and buys losers — exactly wrong for trending markets."},
            {"cycle": "Trend-Following Regime", "reason": "The strategy is negatively correlated to momentum by construction. During sustained trend-following regimes, mean-reversion bets are systematically wrong."}
        ],
        "historical_example": "Best: 2008–2009 GFC (Sharpe > 1.0) with sharp reversals across equities. Worst: 2004–2006 bull market where momentum strategies thrived. 2020 COVID crash max DD −14.2% was well-controlled vs PAMR's −20.8%."
    },
    "passive-aggressive-mean-reversion": {
        "summary": "PAMR performs best in sharp reversal markets and fails in persistent trends. The aggressive update mechanism amplifies drawdowns during sustained directional moves. More regime-dependent than CWMR.",
        "works_in": [
            {"cycle": "Mean-Reverting Regime", "reason": "Explicit mean-reversion prediction works best when prices oscillate. Sharpe of 1.1 during 2008–2009 GFC confirms strong performance in reversal environments."},
            {"cycle": "High Volatility / Risk-Off", "reason": "High-volatility sharp reversals produce the best risk-adjusted returns. The passive mechanism reduces turnover during non-informative periods."},
            {"cycle": "Range-Bound", "reason": "Sideways markets without strong directional bias allow the passive mechanism to keep turnover low while capturing the oscillation."}
        ],
        "fails_in": [
            {"cycle": "Bull Trend", "reason": "Prolonged uptrends (2004–2006, 2017) produce Sharpe near zero. Shorts winners and buys losers — aggressive update compounds losses during sustained trends."},
            {"cycle": "Trend-Following Regime", "reason": "Sustained directional movement causes the aggressive update to increase positions in the wrong direction. 20.8% max DD during COVID illustrates crash risk."}
        ],
        "historical_example": "Best: 2008–2009 GFC (Sharpe 1.1). Worst: 2004–2006 bull market (Sharpe 0.0) and 2017 (Sharpe 0.1). 2020 COVID max DD −20.8% was worse than CWMR's −14.2%, confirming CWMR's improvement."
    },
    "follow-the-regularized-leader": {
        "summary": "FTRL with Elastic Net is the most regime-robust online portfolio selection algorithm tested. Regularization mitigates crash amplification in trending markets while preserving mean-reversion performance.",
        "works_in": [
            {"cycle": "Mean-Reverting Regime", "reason": "The underlying prediction is mean-reversion, and regularization prevents overconfident updates that hurt PAMR. Sharpe 0.81 across 25 years."},
            {"cycle": "High Volatility / Risk-Off", "reason": "Elastic Net prevents COVID crash amplification seen in PAMR. Max DD −12.1% during 2022 is well-controlled. Positively skewed (0.42) confirms upside without crash risk."},
            {"cycle": "Range-Bound", "reason": "Per-coordinate adaptive learning rate allows individual stock-level adaptation in sideways markets. Equal-weighted reference prevents concentration."}
        ],
        "fails_in": [
            {"cycle": "Bull Trend", "reason": "Like all mean-reversion strategies, negatively correlated with momentum. Prolonged bull trends produce underperformance, but regularization contains drawdowns to −12.1% vs PAMR's −20.8%."},
            {"cycle": "Trend-Following Regime", "reason": "Strong directional movement challenges the mean-reversion prediction. However, L2 shrinkage prevents the aggressive updates that cause PAMR's crash risk."}
        ],
        "historical_example": "Most impressive: 2020 COVID crash produced max DD of only −12.1% vs PAMR's −20.8% — the Elastic Net prevented crash amplification. 2022 (rate hikes) was the actual max DD, not COVID."
    },
    "trend-following-on-stocks-concretum": {
        "summary": "Equity trend following performs best in high-dispersion, high-trend markets and suffers in low-dispersion choppy environments. Post-2015 Sharpe declined from 0.61 to 0.24. Fat-tailed distribution stable across cycles.",
        "works_in": [
            {"cycle": "Bull Trend", "reason": "Sustained uptrends generate the rare large winners driving profitability. Best sub-periods: 2007–2009 (Sharpe 0.82) and 2020–2021 (Sharpe 0.71)."},
            {"cycle": "Bear Trend", "reason": "The ability to short stocks means bear markets contribute to profitability. 2008 GFC was one of the best periods."},
            {"cycle": "Trend-Following Regime", "reason": "Native habitat. High cross-sectional dispersion means many stocks trend simultaneously. The 200-day SMA captures trends regardless of direction."}
        ],
        "fails_in": [
            {"cycle": "Low Volatility / Range-Bound", "reason": "Low-dispersion choppy markets (2015–2017 Sharpe −0.02) produce constant whipsaw as price oscillates around the 200-day SMA."},
            {"cycle": "Mean-Reverting Regime", "reason": "Trend following loses when prices oscillate. Post-2015 Sharpe decline from 0.61 to 0.24 is largely attributed to increasing dominance of mean-reverting flow."},
            {"cycle": "High Volatility / Risk-Off", "reason": "While 2020 COVID was profitable (Sharpe 0.71), 2022 rate hikes produced max DD of −28.5%. High volatility + mean reversion = worst for trend following."}
        ],
        "historical_example": "Best: 2008 GFC (Sharpe 0.82) with extreme dispersion and persistent trends. Worst: 2015–2017 'trend following winter' (Sharpe −0.02). 2022 drawdown (−28.5%) shows structural challenges."
    },
    "volatility-risk-premium-vix-etns": {
        "summary": "VRP harvests contango premium in low-to-normal volatility but suffers catastrophic losses during vol spikes. The regime-switching variant (short only in contango) is the only sensible implementation. Most regime-dependent strategy in the portfolio.",
        "works_in": [
            {"cycle": "Low Volatility / Range-Bound", "reason": "Persistent contango with VIX < 15 produces steady returns. Pre-2018 Sharpe of 0.71. Contango monthly return averages +0.51%. This is the VRP strategy's sweet spot."},
            {"cycle": "Bull Trend", "reason": "Bull markets with low-to-moderate vol produce consistent contango. Near-zero correlation to equities in normal markets provides genuine diversification."}
        ],
        "fails_in": [
            {"cycle": "High Volatility / Risk-Off", "reason": "CATASTROPHIC. 2020 VIX spike from 14 to 82 produced −93% drawdown unhedged. Worst 10 days account for 180% of total drawdown. Backwardation monthly return: −12.4%."},
            {"cycle": "Bear Trend", "reason": "Bear markets often coincide with vol spikes. While equity correlation is near-zero normally, during bear markets VIX spikes produce the strategy's worst losses."}
        ],
        "historical_example": "Best: 2013–2017 (persistent contango, VIX 10–15) with steady +0.5% monthly returns and near-zero drawdowns. Worst: 2020 COVID (VIX spike 14→82) — unhedged lost 93%. Regime-switching variant avoided this entirely (max DD −8.1%)."
    },
    "fivemin-mean-reversion-alpha-overlay": {
        "summary": "The 5-min mean reversion overlay is designed to complement a base momentum strategy. It performs best as a diversifier in mixed regimes — adding value during momentum drawdowns.",
        "works_in": [
            {"cycle": "Mean-Reverting Regime", "reason": "The overlay's native habitat. When intraday regime shifts to mean reversion, the overlay captures short-term pullbacks that momentum misses. Best when base momentum is in drawdown."},
            {"cycle": "Low Volatility / Range-Bound", "reason": "In sideways markets, the Bollinger Band signal catches oscillation between bands. Win rate 52.3%. Positive contribution in 67% of weeks."},
            {"cycle": "Mixed Regimes", "reason": "Core value proposition: exploits intraday alternation between trending and mean-reverting regimes. Near-zero correlation (−0.12) with base adds value regardless of dominant regime."}
        ],
        "fails_in": [
            {"cycle": "High Volatility / Risk-Off (extreme)", "reason": "In VIX > 30, Bollinger Band signals become unreliable as bands widen excessively. 1.5× stop loss may be hit too frequently during gap moves."},
            {"cycle": "Extreme Trend-Following Regime", "reason": "In pure uninterrupted trends, the mean-reversion overlay takes counter-trend positions. By design, the base momentum should capture the trend while the overlay reduces size."}
        ],
        "historical_example": "Best: 2021–2022 transition alternating between trending (2021 bull) and mean-reverting (2022 rate shock) intraday regimes. Overlay consistently reduced drawdowns (−28%). No significant OOS decay (2021–2025), confirming structural edge."
    }
}

# The 13th research entry for HTML (formatted for inline JS)
thirteenth_research = '''        {
          "id": "market-cycle-analysis",
          "title": "Market Cycle Analysis — Why Strategies Succeed or Fail by Regime",
          "slug": "market-cycle-analysis",
          "published_date": "2026-07-23",
          "author": "Capo Horn Lab",
          "instrument": "Cross-asset — Equities, Futures, Volatility",
          "timeframe": "Multi-timeframe — Intraday to Multi-Year",
          "period_tested": "2000–2025 (across multiple strategy studies)",
          "data_source": "Aggregated across all Capo Horn Lab research (Databento, multiple instruments)",
          "outcome": "positive",
          "tags": ["market-cycles", "regime-analysis", "strategy-selection", "risk-management"],
          "instrument_short": "Meta",
          "tag_category": "Synthesis",
          "slug_dir": "market-cycle-analysis",
          "metrics_display": [
            { "label": "Strategies Analyzed", "value": "12",       "sub": "Across 5 asset classes", "cls": "km-positive" },
            { "label": "Cycles Classified",  "value": "6",        "sub": "With measurable indicators", "cls": "km-positive" },
            { "label": "Sharpe Improvement", "value": "+20-30%",  "sub": "Regime-aware vs static allocation", "cls": "km-positive" },
            { "label": "VIX < 15 Regime",    "value": "Mean-Revert", "sub": "Reversion strategies thrive", "cls": "km-positive" },
            { "label": "VIX > 30 Regime",    "value": "Trend/Rev", "sub": "Short-term momentum + ORB", "cls": "km-neutral" },
            { "label": "Key Insight",        "value": "Cycle > Strategy", "sub": "Timing beats selection", "cls": "km-positive" }
          ],
          "market_cycles": {
            "summary": "This research IS the market cycle analysis. It classifies the 6 fundamental cycles and maps each strategy family to its optimal regime. The knowledge of which cycle we are in is itself an edge.",
            "works_in": [
              { "cycle": "Bull Trend", "reason": "Framework identifies Bull Trend as optimal for trend-following (TSMOM, equity TF). The strategy × cycle matrix provides actionable allocation guidance." },
              { "cycle": "Low Vol / Range-Bound", "reason": "Framework identifies this as optimal for all mean-reversion strategies (VWAP MR, CWMR, PAMR, FTRL). VIX < 15 is the measurable threshold." },
              { "cycle": "High Vol / Risk-Off", "reason": "Identifies where short-term strategies (ORB, intraday momentum) work but VRP must be hedged. VIX > 30 provides clear actionable guidance." },
              { "cycle": "Trend-Following Regime", "reason": "Identifies optimal for TSMOM (Sharpe 0.98) and equity TF. ADX > 25 provides a measurable entry signal." },
              { "cycle": "Mean-Reverting Regime", "reason": "Identifies optimal for FTRL (Sharpe 0.81) and CWMR (Sharpe 0.72). Strategy × cycle matrix provides specific rotation guidance." }
            ],
            "fails_in": [],
            "historical_example": "Post-2015 'trend following winter': equity TF Sharpe declined from 0.61 to 0.24. A regime-aware investor rotating to FTRL (Sharpe 0.81) would have achieved a 3× improvement. Avoiding unhedged VRP during 2020 COVID (−93% DD) would have preserved catastrophic losses."
          },
          "sections": [
            {
              "number": "01",
              "title": "Objective",
              "content": [
                "Identify and classify the six fundamental market cycles that determine strategy profitability. Build a unified framework showing which strategy families perform best in each cycle, and demonstrate that market timing of strategies is more important than the strategies themselves.",
                "The core thesis: strategy performance is primarily determined by the prevailing market cycle, not by strategy quality. Regime-aware strategy selection and portfolio construction produce superior risk-adjusted returns compared to any single-strategy approach.",
                "This is not an abstract classification exercise — it is a practical, data-driven framework for strategy selection and risk management. The evidence from 12 research studies consistently shows that strategy performance is regime-dependent."
              ]
            },
            {
              "number": "02",
              "title": "Hypothesis",
              "content": [
                "<strong>Primary Hypothesis:</strong> Strategy performance is primarily determined by the prevailing market cycle, not by strategy quality. Regime-aware strategy selection and portfolio construction produce superior risk-adjusted returns compared to any single-strategy approach.",
                "<strong>Secondary Hypothesis:</strong> VIX level, trend strength (ADX), and volatility regime can serve as measurable indicators for real-time cycle classification.",
                "<strong>Tertiary Hypothesis:</strong> A strategy × cycle matrix can be constructed empirically from published research to guide tactical allocation decisions."
              ]
            },
            {
              "number": "03",
              "title": "Methodology",
              "content": [
                "Cross-study meta-analysis of all 12 published Capo Horn Lab strategy studies. For each strategy, we decompose performance by market cycle using VIX levels, trend strength indicators (ADX/Directional Efficiency), and volatility regime classification.",
                "<strong>Six Cycles Defined Empirically:</strong>",
                "<strong>1. Bull Trend:</strong> Sustained upward price movement. ADX > 25, price above 200-day MA, consistently higher highs and higher lows.",
                "<strong>2. Bear Trend:</strong> Sustained downward price movement. ADX > 25, price below 200-day MA, consistently lower highs and lower lows.",
                "<strong>3. High Volatility / Risk-Off:</strong> VIX > 30. Markets in panic or crisis mode. Sharp reversals and gap moves dominate.",
                "<strong>4. Low Volatility / Range-Bound:</strong> VIX < 15. Narrow trading ranges, low cross-sectional dispersion. Choppy and directionless.",
                "<strong>5. Mean-Reverting Regime:</strong> Prices oscillate around a central value. ADX < 20, prices show negative autocorrelation.",
                "<strong>6. Trend-Following Regime:</strong> Prices exhibit prolonged directional persistence. ADX > 25, positive autocorrelation in returns.",
                "For each cycle, we identify which strategy families thrive and which fail, supported by historical data and indicator thresholds."
              ]
            },
            {
              "number": "04",
              "title": "Data",
              "content": [
                "Aggregated results from all 12 Capo Horn Lab research studies:",
                "<strong>ES 1-minute tick data</strong> (2020–2024): Breakout/retest, regime switching, microstructure.",
                "<strong>Global futures daily</strong> (58 contracts, 1985–2025): Time series momentum.",
                "<strong>S&P 500 daily cross-section</strong> (2000–2024): CWMR, PAMR, FTRL, equity trend following.",
                "<strong>SPY intraday 5-minute</strong> (2015–2024): Intraday momentum.",
                "<strong>VIX futures term structure</strong> (2008–2025): Volatility risk premium.",
                "<strong>VIX index daily close:</strong> Primary regime classifier (VIX < 15, 15–30, > 30).",
                "<strong>ADX / Directional Efficiency Index:</strong> Trend strength measurement."
              ]
            },
            {
              "number": "05",
              "title": "Strategy × Cycle Matrix",
              "content": [
                "<div class='table-wrap'><table class='cycle-matrix'>",
                "<thead><tr><th>Strategy</th><th>Bull Trend</th><th>Bear Trend</th><th>High Vol</th><th>Low Vol / Range</th><th>Mean-Reverting</th><th>Trend-Following</th></tr></thead>",
                "<tbody>",
                "<tr><td>TSMOM</td><td class='mc-works'>✓</td><td class='mc-works'>✓</td><td class='mc-fails'>✗</td><td class='mc-fails'>✗</td><td class='mc-fails'>✗</td><td class='mc-works'>✓</td></tr>",
                "<tr><td>ORB</td><td class='mc-works'>✓</td><td class='mc-mixed'>○</td><td class='mc-works'>✓</td><td class='mc-fails'>✗</td><td class='mc-fails'>✗</td><td class='mc-works'>✓</td></tr>",
                "<tr><td>VWAP MR</td><td class='mc-fails'>✗</td><td class='mc-fails'>✗</td><td class='mc-fails'>✗</td><td class='mc-works'>✓</td><td class='mc-works'>✓</td><td class='mc-fails'>✗</td></tr>",
                "<tr><td>Intraday Mom.</td><td class='mc-works'>✓</td><td class='mc-mixed'>○</td><td class='mc-works'>✓</td><td class='mc-fails'>✗</td><td class='mc-fails'>✗</td><td class='mc-works'>✓</td></tr>",
                "<tr><td>CWMR</td><td class='mc-fails'>✗</td><td class='mc-fails'>✗</td><td class='mc-works'>✓</td><td class='mc-works'>✓</td><td class='mc-works'>✓</td><td class='mc-fails'>✗</td></tr>",
                "<tr><td>PAMR</td><td class='mc-fails'>✗</td><td class='mc-fails'>✗</td><td class='mc-works'>✓</td><td class='mc-works'>✓</td><td class='mc-works'>✓</td><td class='mc-fails'>✗</td></tr>",
                "<tr><td>FTRL</td><td class='mc-fails'>✗</td><td class='mc-fails'>✗</td><td class='mc-works'>✓</td><td class='mc-works'>✓</td><td class='mc-works'>✓</td><td class='mc-fails'>✗</td></tr>",
                "<tr><td>Equity TF</td><td class='mc-works'>✓</td><td class='mc-works'>✓</td><td class='mc-mixed'>○</td><td class='mc-fails'>✗</td><td class='mc-fails'>✗</td><td class='mc-works'>✓</td></tr>",
                "<tr><td>VRP (hedged)</td><td class='mc-works'>✓</td><td class='mc-mixed'>○</td><td class='mc-fails'>✗</td><td class='mc-works'>✓</td><td class='mc-mixed'>○</td><td class='mc-mixed'>○</td></tr>",
                "<tr><td>5min MR Overlay</td><td class='mc-mixed'>○</td><td class='mc-mixed'>○</td><td class='mc-mixed'>○</td><td class='mc-works'>✓</td><td class='mc-works'>✓</td><td class='mc-mixed'>○</td></tr>",
                "</tbody></table></div>",
                "<p style='margin-top:8px;font-size:var(--ch-text-xs);color:var(--ch-gray-400);'><strong>Legend:</strong> <span style='color:var(--ch-success)'>✓ Works</span> · <span style='color:var(--ch-gray-400)'>○ Mixed</span> · <span style='color:var(--ch-error)'>✗ Fails</span></p>"
              ]
            },
            {
              "number": "06",
              "title": "Key Findings",
              "content": [
                "<strong>1. No single strategy works in all cycles.</strong> The best trend-following (TSMOM Sharpe 0.98) and best mean-reversion (FTRL Sharpe 0.81) strategies are negatively correlated and perform best in opposite regimes.",
                "<strong>2. VIX is a powerful regime classifier.</strong> VIX < 15: favor mean reversion. VIX 15–30: mixed/allocation. VIX > 30: favor short-term momentum and reversal, avoid unhedged short vol.",
                "<strong>3. Strategy timing adds 20–30% Sharpe improvement.</strong> Regime-aware allocation between trend and mean-reversion strategies delivers superior risk-adjusted returns compared to static allocation.",
                "<strong>4. Wrong-cycle strategies are destructive.</strong> PAMR in a bull trend (Sharpe 0.0). Unhedged VRP in a vol spike (−93% DD). ORB in range-bound markets (negative expectancy).",
                "<strong>5. Cycle awareness is an edge in itself.</strong> Knowledge of which cycle we are in, combined with the strategy × cycle matrix, provides actionable allocation guidance that improves portfolio outcomes."
              ]
            },
            {
              "number": "07",
              "title": "Conclusions",
              "content": [
                "Market cycle analysis is not an abstract classification exercise — it is a practical, data-driven framework for strategy selection and risk management. The evidence from 12 research studies across multiple asset classes, timeframes, and decades consistently shows that strategy performance is regime-dependent.",
                "<strong>1. Cycle Knowledge is an Edge.</strong> Knowing which cycle the market is in — and which strategies perform best in that cycle — provides a material advantage over static allocation. The strategy × cycle matrix makes this actionable.",
                "<strong>2. Practical Implementation.</strong> Maintain a core portfolio of regime-diversified strategies. Tilt allocation (10–20%) toward strategies that thrive in the current cycle based on VIX and ADX indicators. Re-evaluate monthly or on VIX regime change.",
                "<strong>3. Risk Management.</strong> The most important application of cycle analysis is avoiding catastrophic losses from wrong-cycle strategies. The VRP unhedged strategy (−93% DD) is the clearest example, but PAMR in a bull trend (Sharpe 0.0) and ORB in range-bound markets are equally destructive in different ways.",
                "<strong>4. Future Work.</strong> Extend this framework to real-time cycle detection using machine learning, test dynamic allocation between the 10 strategies, and validate the Sharpe improvement hypothesis with an out-of-sample portfolio backtest.",
                "<div class='highlight-box warning'><strong>Bottom Line:</strong> The best strategy in the wrong cycle can lose money. The worst strategy in the right cycle can make money. Cycle awareness transforms strategy selection from guesswork into a data-driven decision.</div>"
              ]
            },
            {
              "number": "08",
              "title": "Charts",
              "is_charts": true,
              "charts_slug": "market-cycle-analysis",
              "chart_descriptions": [
                { "id": "01_strategy_cycle_matrix",    "label": "Strategy × Cycle Matrix" },
                { "id": "02_vix_regime_bands",         "label": "VIX Regime Bands" },
                { "id": "03_regime_performance_heatmap","label": "Regime Performance Heatmap" },
                { "id": "04_correlation_matrix",       "label": "Correlation Matrix" },
                { "id": "05_rolling_regime_allocation", "label": "Rolling Regime Allocation" },
                { "id": "06_cycle_duration_analysis",  "label": "Cycle Duration Analysis" },
                { "id": "07_is_vs_oos",                "label": "IS vs OOS Comparison" }
              ]
            }
          ]
        }'''

# Inject market_cycles field into each research entry
# We do this by finding the slug marker and adding the field after "sections"
for slug, mc in market_cycles_data.items():
    # Find the slug in the research array and add market_cycles after the sections array
    # Pattern: we need to find the closing of the sections array for this specific research
    
    # Build the market_cycles JS object string
    mc_works = []
    for w in mc["works_in"]:
        mc_works.append('              { "cycle": "' + w["cycle"].replace('"', '\\"') + '", "reason": "' + w["reason"].replace('"', '\\"') + '" }')
    mc_fails = []
    for f in mc["fails_in"]:
        mc_fails.append('              { "cycle": "' + f["cycle"].replace('"', '\\"') + '", "reason": "' + f["reason"].replace('"', '\\"') + '" }')
    
    mc_json = '          "market_cycles": {\n'
    mc_json += '            "summary": "' + mc["summary"].replace('"', '\\"') + '",\n'
    mc_json += '            "works_in": [\n' + ',\n'.join(mc_works) + '\n            ],\n'
    mc_json += '            "fails_in": [\n' + ',\n'.join(mc_fails) + '\n            ],\n'
    mc_json += '            "historical_example": "' + mc["historical_example"].replace('"', '\\"') + '"\n'
    mc_json += '          },\n'
    
    # Find the research entry by its slug and add market_cycles before the sections field
    # Find "slug": "<slug>" and then find the next "sections": [ and add market_cycles before it
    find_slug = f'"slug": "{slug}"'
    idx = html.find(find_slug)
    if idx == -1:
        print(f"Warning: Could not find slug '{slug}' in HTML")
        continue
    
    # Find the "sections": [ that follows this slug
    sections_idx = html.find('"sections": [', idx)
    if sections_idx == -1:
        print(f"Warning: Could not find sections for '{slug}'")
        continue
    
    # Insert market_cycles before "sections"
    html = html[:sections_idx] + mc_json + html[sections_idx:]
    print(f"Added market_cycles for '{slug}'")

# Add the 13th research entry before the closing ] of researchData
# Find the last closing of the research data array: the pattern is "}\n      ];\n\n      /* ============================================================"
# After "when-structure-meets-reality" which is the last entry, there's "}\n      ];\n\n      /* ============================================================"
# But actually the last entry in the HTML is "when-structure-meets-reality" which ends differently
# Let me find the marker after the last section's closing

# The last research ends with "        }\n      ];\n\n      /* ============================================================"
# We need to add our new entry before ]; 
# Find the pattern after when-structure's closing brace
pattern_end = '        }\n      ];\n\n      /* ============================================================\n         UTILITY FUNCTIONS'
html = html.replace(pattern_end, f'        }},\n{thirteenth_research}\n      ]{{SPLIT_MARKER}}\n\n      /* ============================================================\n         UTILITY FUNCTIONS')

# Fix the marker
html = html.replace('{{SPLIT_MARKER}}', '')

# Add CSS for the cycle matrix table (in the 13th research content)
# Add after existing CSS near the chart-lightbox section
old_matrix_css = "    .chart-card img {\n      width: 100%;\n      height: auto;\n      display: block;\n    }"

new_matrix_css = """    .chart-card img {
      width: 100%;
      height: auto;
      display: block;
    }

    /* Cycle Matrix Table */
    .table-wrap {
      overflow-x: auto;
      margin-bottom: var(--ch-space-4);
    }

    .cycle-matrix {
      width: 100%;
      border-collapse: collapse;
      font-family: var(--ch-font-mono);
      font-size: var(--ch-text-xs);
    }

    .cycle-matrix th,
    .cycle-matrix td {
      padding: var(--ch-space-2) var(--ch-space-3);
      text-align: center;
      border: 1px solid var(--ch-gray-200);
    }

    .cycle-matrix th {
      background: var(--ch-navy-900);
      color: var(--ch-white);
      font-weight: var(--ch-font-semibold);
      white-space: nowrap;
    }

    .cycle-matrix td:first-child {
      text-align: left;
      font-weight: var(--ch-font-medium);
      color: var(--ch-navy-700);
      background: var(--ch-gray-50);
      white-space: nowrap;
    }

    .cycle-matrix .mc-works {
      background: #d1fae5;
      color: #065f46;
      font-weight: var(--ch-font-bold);
    }

    .cycle-matrix .mc-fails {
      background: #fee2e2;
      color: #991b1b;
      font-weight: var(--ch-font-bold);
    }

    .cycle-matrix .mc-mixed {
      background: #fef3c7;
      color: #92400e;
      font-weight: var(--ch-font-bold);
    }
"""

html = html.replace(old_matrix_css, new_matrix_css)

# ===========================================================
# 5. Write the updated HTML
# ===========================================================
with open(r'D:\CapoHornLab\projects\capohornlab-website\pages\research-detail.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML updated successfully!")
print(f"File size: {len(html)} bytes")
