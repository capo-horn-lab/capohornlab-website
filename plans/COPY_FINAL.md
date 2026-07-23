# COPY_FINAL.md — Capo Horn Lab

> **Author:** Afrodite (Content Lead)
> **Date:** 2026-07-22
> **Status:** Final — Sprint 2 / Task 2.4
> **Language:** English (primary)
> **Voice:** Technical · Precise · Authoritative · Never promotional
> **Claim:** *Beyond the Market Edge*
> **Motto:** *We test. We measure. We publish the truth.*

---

## Table of Contents

1. [About (`/about`)](#1-about)
2. [Method (`/method`)](#2-method)
3. [Contact (`/contact`)](#3-contact)
4. [Auth — Login / Signup / Reset Password](#4-auth)
5. [Test Your Strategy (`/test-your-strategy`)](#5-test-your-strategy)
6. [Empty States](#6-empty-states)
7. [Email Templates](#7-email-templates)

---

## 1. About (`/about`)

### 1.1 Mission

**Headline:**
```
Beyond the Market Edge
```

**Subheadline:**
```
We are Capo Horn Lab — a quantitative research group that tests
trading strategies on historical market data.

Our mission: to replace market noise with reproducible evidence.
```

**Lead paragraph:**
```
Most trading strategies fail in the real world. Not because the ideas
are bad — but because they have never been tested against actual
market data with realistic costs, slippage, and statistical rigour.

We exist to fix that.
```

### 1.2 Philosophy — Rigour Over Hype

```
We test ideas against real data and publish what we find —
including when it hurts.

A negative result is not a failure. It is a successful falsification.
It saves you time, capital, and the cost of learning the hard way.

Every study we publish is:
- Falsifiable — future data can disprove it
- Reproducible — methodology is transparent, code is available
- Net of costs — every result includes commissions and slippage
- Limitless in its limitations — we name what the test does not cover

We do not sell strategies. We do not sell signals. We do not sell
the fantasy of easy returns.

We test. We measure. We publish the truth.
```

### 1.3 Team

**Section headline:**
```
Who We Are
```

**Section subheadline:**
```
Quantitative finance, statistical modelling, and software engineering.
No stock photos. No inflated titles. Just the people doing the work.
```

**Members (placeholder format — names to be filled):**

| Name | Role | Bio |
|------|------|-----|
| [Name] | Quantitative Research Lead | Institutional markets background. Statistical modelling, hypothesis design, and result interpretation. Driven by the conviction that most retail strategies fail from untested assumptions — not bad ideas. |
| [Name] | Quantitative Research | Strategy formulation, backtesting pipeline, and data analysis. Focused on rigour: IS/OOS splits, Monte Carlo simulation, and parameter stability testing. |
| [Name] | Full-Stack Development | Architecture, infrastructure, and the client platform. Every study we publish runs on systems built for reproducibility from the ground up. |
| [Name] | Data Engineering | Tick-level data ingestion, cleaning, and normalisation. Ensures that what we test against is accurate, consistent, and verifiable. |

**Bio guidelines:**
- No headshots required — minimal text or abstract visual only
- Focus on: years in markets/data, quantitative background, what drives them (curiosity, rigour, falsification)
- No promotional language — each bio is a fact sheet, not a resume pitch

### 1.4 Data Infrastructure

**Section headline:**
```
Infrastructure
```

| Parameter | Detail |
|-----------|--------|
| **Tick data source** | Databento MDP3 |
| **Depth** | 5+ years of ES, NQ, CL, 6E tick data |
| **Resolution** | Tick → 1m / 5m / 15m / 1h / Daily — multi-resolution on every study |
| **Pipeline** | Python + pandas/polars + Matplotlib/Plotly |
| **Reproducibility** | All results are scripted, version-controlled, and repeatable |
| **Computing** | Local high-performance workstations — no cloud latency, full data control |

### 1.5 Closing One-Liner

```
We don't sell strategies. We sell the truth about them.
```

**CTA block:**
```
Have a strategy you want tested?
[Submit Your Strategy → /test-your-strategy]

Read our published research:
[Read Our Research → /research]
```

---

## 2. Method (`/method`)

### 2.1 Headline

```
How We Backtest
Rigour. Reproducibility. Realism.
```

### 2.2 Pipeline

**Visual pipeline (arrow flow):**
```
Idea → Formalise Rules → Code → Run on Tick Data → Statistical Analysis → Interpretation → Publication
```

**Pipeline description (for SEO / text fallback):**
```
Every study begins as a hypothesis. We formalise it into a set of
unambiguous trading rules, code them into our backtesting pipeline,
and run them against tick-level historical data. The output —
equity curves, trade logs, and performance metrics — is analysed
statistically, interpreted candidly, and published in full.

No black boxes. No cherry-picked results. No skipped steps.
```

### 2.3 Rigour Standards

**Section headline:**
```
Rigour Standards
```

| Standard | What It Means |
|----------|---------------|
| **IS/OOS Split** | 70% of data for development, 30% held out for validation. We never test on data used during development. |
| **Monte Carlo Simulation** | 1,000+ randomised trade sequences to estimate the distribution of possible outcomes — not just the one path that happened. |
| **Parameter Stability** | Parameters are varied across a defined grid. If performance collapses outside a narrow optimal zone, that is a red flag for data-mining, not a valid edge. |
| **Transaction Costs** | Realistic slippage and commissions per instrument. ES: 1 tick slippage, NQ: 2 ticks. Commissions: $2.50 per side per contract. Every result is net of costs. |
| **Multiple Timeframes** | A strategy must hold up across resolutions. If it works on 1-minute but fails on 5-minute and 1-hour, the edge is not structural. |

### 2.4 Data Section

**Section headline:**
```
Data & Execution Parameters
```

| Parameter | Detail |
|-----------|--------|
| Tick data source | Databento MDP3 |
| Instruments | ES (E-mini S&P 500), NQ (Nasdaq-100), CL (Crude Oil), 6E (Euro FX) — others on request |
| Historical depth | 2020–present, growing with each new data ingestion cycle |
| Resolution | Tick → 1m / 5m / 15m / 1h / Daily |
| Default slippage | ES: 1 tick · NQ: 2 ticks (configurable per request) |
| Default commissions | $2.50 per side per contract (configurable per request) |
| Execution model | Bar-close execution with configurable order delay |

### 2.5 FAQ

**Section headline:**
```
Frequently Asked Questions
```

| Question | Answer |
|----------|--------|
| **Do you sell trading strategies?** | No. We test yours. We never sell strategies, indicators, signals, or subscriptions. Our revenue comes from backtesting services — not from the performance of any strategy. |
| **How is this different from backtesting on TradingView?** | We use tick-level data, realistic slippage and commission models, Monte Carlo simulation, and strict IS/OOS validation. TradingView bar-replay runs on OHLC data with no slippage model. That difference matters — especially for high-frequency or intraday strategies where tick dynamics change outcomes. |
| **How long does a backtest take?** | Typically 3–10 business days depending on complexity, data volume, and our current queue. Simple single-instrument tests are faster; multi-parameter or cross-instrument studies take longer. |
| **Do you test crypto strategies?** | Not in MVP. Our current data infrastructure covers futures: ES, NQ, CL, 6E. Crypto may be added in a future phase. |
| **What if my strategy does not work?** | That is the most valuable outcome. A clear, data-backed "this does not produce an edge" saves you time, capital, and the cognitive bias of believing otherwise. We publish negative results — they are not failures, they are successful falsifications. |
| **Can I see an example before submitting?** | Yes. All our published research is available on the Research page. You will see the exact format, rigour standards, and candid language before you submit anything. |

**FAQ CTA block:**
```
Have a question we did not answer?
[Contact Us → /contact]
```

---

## 3. Contact (`/contact`)

### 3.1 Page Copy

**Headline:**
```
Contact
```

**Subheadline:**
```
Have a question about our methodology, a collaboration idea,
or a strategy you would like to discuss before submitting?
```

**Form fields:**

| Field | Label | Placeholder | Type | Required |
|-------|-------|-------------|------|----------|
| 1 | Name | Your full name | text | Yes |
| 2 | Email | you@example.com | email | Yes |
| 3 | Subject | What is this regarding? | text | Yes |
| 4 | Message | — | textarea | Yes |
| 5 | — | [Send Message] | submit button | — |

**Form help text:**
```
All fields are required. We aim to respond within 2 business days.
```

**Email fallback:**
```
Prefer email? Write to us directly at:
contact@capohornlab.com
```

**Form submission confirmation (inline):**
```
Message sent.
We have received your message and will respond within 2 business days.
If you have not heard from us by then, feel free to follow up.

— Capo Horn Lab
```

**Form validation messages:**

| Condition | Message |
|-----------|---------|
| Name empty | Please enter your name. |
| Email empty | Please enter your email address. |
| Email invalid | Please enter a valid email address. |
| Subject empty | Please enter a subject. |
| Message empty | Please enter your message. |
| Server error | Something went wrong. Please try again or email us directly. |
| Rate limit | Too many submissions. Please wait a few minutes and try again. |

---

## 4. Auth — Login / Signup / Reset Password

### 4.1 Login (`/login`)

**Headline:**
```
Welcome Back
```

**Subheadline:**
```
Log in to view your dashboard, track requests, and access results.
```

**Form fields:**

| Field | Label | Placeholder | Type | Required |
|-------|-------|-------------|------|----------|
| 1 | Email | you@example.com | email | Yes |
| 2 | Password | — | password | Yes |
| 3 | — | [Log In] | submit button | — |

**Footer links:**
```
Forgot your password? [Reset it → /reset-password]

Don't have an account? [Sign Up → /signup]
```

**Validation messages:**

| Condition | Message |
|-----------|---------|
| Email empty | Please enter your email address. |
| Password empty | Please enter your password. |
| Invalid credentials | Invalid email or password. Please try again. |
| Account not verified | Please verify your email address before logging in. [Resend verification email] |
| Account disabled | This account has been disabled. Please contact support. |
| Too many attempts | Too many login attempts. Please try again in 15 minutes. |
| Server error | Something went wrong. Please try again. |

### 4.2 Signup (`/signup`)

**Headline:**
```
Create an Account
```

**Subheadline:**
```
Submit your strategies, track backtests, and access results.
```

**Form fields:**

| Field | Label | Placeholder | Type | Required |
|-------|-------|-------------|------|----------|
| 1 | Email | you@example.com | email | Yes |
| 2 | Password | At least 8 characters | password | Yes |
| 3 | Confirm Password | Confirm your password | password | Yes |
| 4 | — | [Create Account] | submit button | — |

**Legal text:**
```
By signing up, you agree to our Terms of Service and Privacy Policy.
```

**Footer link:**
```
Already have an account? [Log In → /login]
```

**Validation messages:**

| Condition | Message |
|-----------|---------|
| Email empty | Please enter your email address. |
| Email invalid | Please enter a valid email address. |
| Email already registered | An account with this email already exists. [Log In → /login] |
| Password empty | Please enter a password. |
| Password too short | Password must be at least 8 characters. |
| Password weak | Password must include at least one uppercase letter and one number. |
| Confirm password empty | Please confirm your password. |
| Passwords do not match | Passwords do not match. |
| Server error | Something went wrong. Please try again. |

**Success state:**
```
Account created. Check your email for a verification link.
```

### 4.3 Reset Password (`/reset-password`)

**Headline:**
```
Reset Your Password
```

**Subheadline:**
```
Enter your email and we will send you a reset link.
```

**Form fields:**

| Field | Label | Placeholder | Type | Required |
|-------|-------|-------------|------|----------|
| 1 | Email | you@example.com | email | Yes |
| 2 | — | [Send Reset Link] | submit button | — |

**Footer link:**
```
Remember your password? [Log In → /login]
```

**Validation messages:**

| Condition | Message |
|-----------|---------|
| Email empty | Please enter your email address. |
| Email invalid | Please enter a valid email address. |
| Email not found | If this email is registered, you will receive a reset link. |
| Rate limit | Too many reset requests. Please try again in one hour. |
| Server error | Something went wrong. Please try again. |

**Success state (same for found and not-found to avoid email enumeration):**
```
If this email is registered, you will receive a reset link within a few minutes.
Check your spam folder if you do not see it.
```

### 4.4 Set New Password (`/reset-password/[token]`)

**Headline:**
```
Set a New Password
```

**Subheadline:**
```
Enter your new password below.
```

| Field | Label | Placeholder | Type | Required |
|-------|-------|-------------|------|----------|
| 1 | New Password | At least 8 characters | password | Yes |
| 2 | Confirm New Password | — | password | Yes |
| 3 | — | [Update Password] | submit button | — |

**Validation messages:**

| Condition | Message |
|-----------|---------|
| Password empty | Please enter a new password. |
| Password too short | Password must be at least 8 characters. |
| Passwords do not match | Passwords do not match. |
| Token invalid or expired | This reset link is invalid or has expired. [Request a new one → /reset-password] |
| Server error | Something went wrong. Please try again. |

**Success state:**
```
Password updated. You can now log in with your new password.
[Log In → /login]
```

---

## 5. Test Your Strategy (`/test-your-strategy`)

### 5.1 Pre-Auth Hero (Anonymous Visitor)

```
Test Your Strategy

Describe your strategy. We will backtest it on tick-level historical data.
You get a full quantitative report with equity curve, Sharpe ratio,
drawdown analysis, and Monte Carlo simulation.

[Sign Up to Submit → /signup]
Already have an account? [Log In → /login]
```

### 5.2 Multi-Step Wizard (Authenticated User)

**Step 1 — Strategy Identity**

| Field | Label | Placeholder / Options | Help Text | Required |
|-------|-------|-----------------------|-----------|----------|
| 1 | Strategy Name | e.g. "Breakout ES 1m" | Choose a descriptive name for your strategy. This is how it will appear in your dashboard. | Yes |
| 2 | Brief Description | Describe your strategy's logic in plain language | What is the core idea behind this strategy? Be as specific as possible. This helps us understand intent before we touch the parameters. | Yes |
| 3 | Asset Class | Futures | Which asset class does your strategy trade? | Yes |
| 4 | Instrument(s) | ES · NQ · CL · 6E | Which instrument(s) does your strategy trade? | Yes |
| 5 | Direction | Long only · Short only · Both | Does your strategy take long positions, short positions, or both? | Yes |

**Step 2 — Time Settings**

| Field | Label | Placeholder / Options | Help Text | Required |
|-------|-------|-----------------------|-----------|----------|
| 1 | Timeframe | 1m · 5m · 15m · 1h · Daily · Custom | On what bar resolution does your strategy operate? | Yes |
| 2 | Start Date | YYYY-MM-DD | When should the backtest period begin? | Yes |
| 3 | End Date | YYYY-MM-DD | When should the backtest period end? | Yes |
| 4 | Session Times | Regular (RTH) · Electronic (ETH) · Custom | During which trading session(s) does your strategy take signals? | No |

**Step 3 — Entry Rules**

| Field | Label | Placeholder / Options | Help Text | Required |
|-------|-------|-----------------------|-----------|----------|
| 1 | Entry Trigger | Describe the condition that triggers an entry | What specific market condition must be met before you enter? Include indicator values, price levels, or pattern recognition logic. Be precise — "RSI below 30 and price closes above SMA(20)" is clearer than "oversold condition." | Yes |
| 2 | Indicators & Parameters | e.g. SMA(20), RSI(14), Bollinger(20,2) | Which indicators does your strategy use, and what are their specific parameters? | No |
| 3 | Filter Conditions | (optional) | Any additional filters that must be true before entry (e.g. "only enter if ADX > 25," "skip first 30 minutes of session")? | No |
| 4 | Max Positions per Day | (number) | Maximum number of entries per trading day. | No |

**Step 4 — Exit Rules**

| Field | Label | Placeholder / Options | Help Text | Required |
|-------|-------|-----------------------|-----------|----------|
| 1 | Stop Loss | e.g. 10 ticks, $500, 2% of account | How does your strategy define the maximum acceptable loss per trade? | Yes |
| 2 | Take Profit | e.g. 20 ticks, $1,000, 3:1 reward:risk | At what profit level does the strategy exit? | No |
| 3 | Trailing Stop | (optional) | Does the strategy use a trailing stop? If so, describe the trail distance and activation condition. | No |
| 4 | Break-Even Move | (optional) | Does the strategy move the stop to break-even after a certain profit level? | No |
| 5 | Time-Based Exit | e.g. "Exit all positions 5 minutes before session close" | Does the strategy exit based on time rather than price? | No |

**Step 5 — Execution Parameters**

| Field | Label | Placeholder / Options | Help Text | Required |
|-------|-------|-----------------------|-----------|----------|
| 1 | Contracts per Trade | (number) | How many contracts does your strategy trade per entry? | Yes |
| 2 | Position Sizing | Fixed contracts · Percentage of capital · Risk-based (% of equity) | How is position size determined? | No |
| 3 | Commission per Side | Default: $2.50 | Commission cost per contract per side. Default reflects standard retail futures brokerage. | Yes |
| 4 | Slippage per Entry | Default varies by instrument | Expected slippage in ticks. Default: 1 tick (ES), 2 ticks (NQ). Adjust if you have empirical data on your fill quality. | Yes |
| 5 | Order Type | Market · Limit (specify offset) · Stop (specify trigger) | What order type does your strategy use to enter and exit? | No |

**Step 6 — Attachments & Notes**

| Field | Label | Placeholder / Options | Help Text | Required |
|-------|-------|-----------------------|-----------|----------|
| 1 | Files | Upload (max 5 files, 10MB each) | Upload any supporting material: screenshots of your strategy rules, spreadsheets, indicator configurations, or existing backtest results. Accepted formats: PDF, PNG, JPG, CSV, TXT. | No |
| 2 | Additional Notes | (optional textarea) | Anything else we should know about your strategy that does not fit into the fields above? | No |

**Step 7 — Review & Submit**

**Subheadline:**
```
Review your submission before sending.
```

**Summary card structure:**
```
Strategy: [Name]
Instrument: [ES / NQ / CL / 6E]
Timeframe: [value] · Period: [Start] → [End]
Direction: [Long / Short / Both]
Entry Trigger: [preview — truncated to 2 lines]
Stop Loss: [value] · Take Profit: [value] · Trailing: [Yes/No]
Contracts: [N] · Commissions: [$X/side] · Slippage: [Y ticks]
Attachments: [N files]
```

**Actions:**
```
[Edit Sections]  [Submit Strategy]
```

### 5.3 Post-Submission Confirmation

```
Request Received

We have received your strategy submission. Here is what happens next:

1. Our team reviews your strategy parameters (1–2 business days)
2. We may reach out if we need clarification
3. We run the backtest against historical tick data (3–10 business days)
4. You receive a full quantitative report

Your request ID: [ID]
You can track its status on your Dashboard.

[Go to Dashboard → /dashboard]
```

### 5.4 Help Text — Section Level

**Wizard sidebar / tooltip copy for each step:**

| Step | Guidance |
|------|----------|
| 1 | **Precision matters.** A strategy described as "buy when it goes up" cannot be tested. A strategy described as "enter long when the 20-period SMA crosses above the 50-period SMA on the 5-minute chart" can. The more specific you are, the more accurate your results will be. |
| 2 | **Choose your period thoughtfully.** Include enough data for statistical significance — typically 2+ years for daily strategies, 6+ months for intraday. The system will default to maximum available data if you leave the range open. |
| 3 | **Detail is better than brevity.** If your strategy uses multiple indicators, list them all. If there is a sequence (e.g. "first check A, then wait for B"), describe it. Ambiguous rules produce ambiguous results. |
| 4 | **Define risk before reward.** A stop loss is required for every strategy. Take profit, trailing stops, and break-even logic are optional but recommended — they define how the strategy manages open positions. |
| 5 | **Honest slippage matters.** The biggest gap between backtest and live trading is execution. Using 0 slippage and $0 commissions will produce beautiful equity curves that do not survive real markets. Be realistic. |
| 6 | **Context helps interpretation.** If you have existing trading logs, spreadsheet models, or indicator screenshots, include them. They help us understand your intent. |
| 7 | **Final check.** Read through every field before submitting. Incomplete or contradictory parameters may delay the review. You will not be able to edit after submission — if something is wrong, submit again with corrections. |

---

## 6. Empty States

### 6.1 Dashboard — "No Requests Yet"

```
No submissions yet.

Submit your first strategy to get started.
Backtests typically take 3–10 business days.

[Submit Your Strategy → /test-your-strategy]
```

### 6.2 Dashboard — "No Research Yet"

```
No research published yet.

The lab is running its first studies. Subscribe to be notified
when new research is published.

[email input] [Notify Me]
```

### 6.3 Request Detail — "No Results Yet"

```
No results yet.

Your request is [current status]. We will update this page
and notify you by email when the backtest is complete.

Status: [status badge]
Submitted: [date]
Estimated completion: [date or "TBD after review"]

In the meantime:
- [View all my requests → /dashboard]
- [Read published research → /research]
```

### 6.4 Request — "No Clarifications"

```
No clarification requests.
If our team has questions about your strategy, they will appear here.
```

### 6.5 Research Detail — "No Charts Available"

```
Charts are being generated.
Visualisations will appear here once the study is complete.
```

### 6.6 Admin — "No New Submissions"

```
No new submissions.

All requests have been reviewed. Check the full list to filter by status.
[View All Requests → /admin/requests]
```

### 6.7 Search — "No Results"

```
No results found.

Try a different search term or browse our research catalogue.
[Browse All Research → /research]
```

---

## 7. Email Templates

> **Platform:** Resend (MVP)
> **Frequency:** Transactional only — maximum 1 marketing email per month
> **Brand signature block (all emails):**
> ```
> — Capo Horn Lab
> Beyond the Market Edge
> [contact@capohornlab.com]
> [Unsubscribe link]
> ```

---

### 7.1 Welcome Email

**Trigger:** User signs up and verifies email.

**Subject:**
```
Welcome to Capo Horn Lab
```

**Preheader:**
```
Submit your first strategy. Track backtests. Access results.
```

**Body:**
```
Welcome to Capo Horn Lab.

You now have access to submit trading strategies for quantitative
backtesting on tick-level historical data.

Here is what you can do next:

1. Submit a strategy → Tell us your rules. We test them.
   /test-your-strategy

2. Read our research → See the format, rigour, and quality of
   our published work. /research

3. View your dashboard → Track submissions and access results.
   /dashboard

We test on ES, NQ, CL, and 6E — tick-level data from Databento,
with realistic slippage and commissions. Every result is net of costs.

No strategy selling. No signals. No subscriptions.
Just evidence.

— Capo Horn Lab
```

---

### 7.2 Request Received Confirmation

**Trigger:** User submits a strategy request.

**Subject:**
```
Your backtest request has been received — [REQUEST_ID]
```

**Preheader:**
```
We have received your [Strategy Name] submission. Here is what happens next.
```

**Body:**
```
Hi [Name],

We have received your backtest request.

  Strategy: [Strategy Name]
  Instrument: [ES / NQ / CL / 6E]
  Request ID: [REQUEST_ID]
  Submitted: [Date]

Here is what happens next:

1. Review → Our team reviews your parameters (1–2 business days)
2. Clarify → We may reach out if we need additional details
3. Backtest → We run the test against historical tick data
   (3–10 business days depending on complexity)
4. Deliver → You receive a full quantitative report with equity
   curve, Sharpe ratio, drawdown analysis, and Monte Carlo simulation

You can track your request status at any time:
/dashboard/requests/[REQUEST_ID]

— Capo Horn Lab
```

---

### 7.3 Status Change Emails

#### 7.3.1 → In Review (In Valutazione)

**Subject:**
```
Your request status has been updated: In Review — [REQUEST_ID]
```

**Preheader:**
```
We are evaluating your [Strategy Name] submission.
```

**Body:**
```
Hi [Name],

Your backtest request for [Strategy Name] is now in review.

Our team is evaluating your parameters to confirm that the strategy
can be tested within our current infrastructure and data scope.

We will update you once the evaluation is complete.

  Current status: In Review
  Request ID: [REQUEST_ID]

/dashboard/requests/[REQUEST_ID]

— Capo Horn Lab
```

#### 7.3.2 → Accepted (Accettata)

**Subject:**
```
Your request status has been updated: Accepted — [REQUEST_ID]
```

**Preheader:**
```
Your [Strategy Name] backtest has been accepted and is moving into production.
```

**Body:**
```
Hi [Name],

Good news: your backtest request for [Strategy Name] has been accepted.

We have started running the test against historical tick data. Results
are typically ready within 3–10 business days, depending on the
complexity and scope of the test.

We will notify you as soon as the report is ready.

  Current status: Accepted — In Progress
  Request ID: [REQUEST_ID]

/dashboard/requests/[REQUEST_ID]

— Capo Horn Lab
```

#### 7.3.3 → Rejected (Rifiutata)

**Subject:**
```
Your request status has been updated: Not Accepted — [REQUEST_ID]
```

**Preheader:**
```
We were unable to accept your [Strategy Name] submission at this time.
```

**Body:**
```
Hi [Name],

After reviewing your submission for [Strategy Name], we are unable
to accept it for testing at this time.

Reason:
[Admin provides specific reason — e.g. "The strategy rules are not
sufficiently defined to produce a deterministic test," "The instrument
requested is outside our current coverage," etc.]

If you would like to refine your strategy and resubmit, we welcome
a revised request. You can also reach out via our contact page if
you have questions about the decision.

  Request ID: [REQUEST_ID]

/contact

— Capo Horn Lab
```

#### 7.3.4 → Completed (Completata)

**Subject:**
```
Your backtest results are ready — [Strategy Name]
```

**Preheader:**
```
The report for [Strategy Name] is available on your dashboard.
```

**Body:**
```
Hi [Name],

Your backtest for [Strategy Name] is complete.

The full report is available on your dashboard and includes:

  • Equity curve (IS / OOS)
  • Sharpe ratio (IS / OOS)
  • Profit factor
  • Win rate (with context)
  • Maximum drawdown
  • Total trades
  • Monte Carlo simulation results
  • Trade distribution analysis

View and download your report:
/dashboard/requests/[REQUEST_ID]

If you would like us to test a variation of this strategy or test
the same approach on a different instrument, submit a new request.

  [Submit Another Strategy → /test-your-strategy]

— Capo Horn Lab
```

---

### 7.4 Clarification Request

**Trigger:** Admin needs more information before proceeding.

**Subject:**
```
We have a question about your strategy, [Name]
```

**Preheader:**
```
We need clarification on [specific topic] before we can proceed.
```

**Body:**
```
Hi [Name],

We are reviewing your [Strategy Name] submission and need additional
details before we can proceed with the backtest.

Question:
[Admin's specific question — e.g. "When you say 'RSI below 30',
which RSI period are you using? Default 14? Custom?"]

Please respond through your dashboard or reply to this email with
the clarification. Once we hear back, we will resume the review.

  Request ID: [REQUEST_ID]

/dashboard/requests/[REQUEST_ID]

— Capo Horn Lab
```

---

### 7.5 Research Notification

**Trigger:** New research published.

**Subject:**
```
[Research Title] — New Publication from Capo Horn Lab
```

**Preheader:**
```
We tested [hypothesis] on [instrument]. Here is what we found.
```

**Body:**
```

[Research Title]


[Result Badge: Positive / Mixed / No Edge]


[1-paragraph abstract — the "what" and the "so what"]

Example:
"We tested whether a simple moving-average crossover system
(20/50 SMA) on ES daily data produces a statistically significant
edge over a 5-year period. The system generates trades — but after
slippage and commissions, the net performance is indistinguishable
from noise. Full results, charts, and code are available."

Key Metrics Snapshot:
  • Sharpe (OOS): [value]
  • Profit Factor: [value]
  • Total Trades: [N]
  • Max Drawdown: [value]%

[Read the Full Study → /research/[slug]]


Have a strategy you want tested?
[Submit Your Strategy → /test-your-strategy]


— Capo Horn Lab
Beyond the Market Edge

[Unsubscribe link]
```

---

### 7.6 Password Reset Email

**Trigger:** User requests password reset.

**Subject:**
```
Reset your Capo Horn Lab password
```

**Preheader:**
```
Use the link below to reset your password. This link expires in 1 hour.
```

**Body:**
```
Hi [Name],

We received a request to reset your Capo Horn Lab password.

Click the link below to set a new password:

[Reset Password → /reset-password/[TOKEN]]

This link expires in 1 hour. If you did not request a password reset,
you can safely ignore this email.

— Capo Horn Lab
```

---

### 7.7 Email Verification

**Trigger:** User signs up.

**Subject:**
```
Verify your email — Capo Horn Lab
```

**Preheader:**
```
Confirm your email address to activate your account.
```

**Body:**
```
Welcome to Capo Horn Lab.

Please verify your email address by clicking the link below:

[Verify Email → /verify-email/[TOKEN]]

Once verified, you will be able to submit strategies and access results.

If you did not create this account, you can ignore this email.

— Capo Horn Lab
```

---

## Appendix: Style Guide Reference

### Tone Rules

| Axis | Always | Never |
|------|--------|-------|
| Tone | Confident but humble. Authoritative but not arrogant. Warm but not salesy. | Hype, urgency, FOMO, "get rich," "secret," "proven system" |
| Vocabulary | "Hypothesis," "falsifiable," "reproducible," "net of costs," "edge," "distribution," "statistical significance" | "Guaranteed," "easy money," "100% win rate," "insider," "guru," "secret formula," "proven" |
| Structure | Declarative, concise. Short paragraphs. Bullet points where precise. | Run-on marketing copy. Wall-of-text testimonials. |
| Pronouns | "We" (lab identity), "You" (client in CTAs only), "Our research shows…" | Overuse of "I" — the lab speaks, not an individual. |
| Data | Tables, charts, quantitative summaries. "Sharpe: 0.12 IS / -0.08 OOS" | Vague percentages. Cherry-picked best-case metrics. |

### Banned Terms

- "proven" / "guaranteed" / "secret" / "hidden" / "revealed"
- "guru" / "expert" / "master"
- "easy" / "simple" / "instant" / "immediate"
- "passive income" / "financial freedom" / "millionaire" / "wealth"
- "win rate" without profit factor and Sharpe context
- "backtested" without specifying slippage and commission assumptions

### Required Phrases

- "falsifiable" — our results can be disproven by future data
- "reproducible" — methodology is transparent
- "net of costs" — every result includes transaction costs
- "statistical significance" — or lack thereof
- "limitations" — every study has them, and we name them
- "hypothesis" — not "prediction" or "forecast"
- "evidence" — not "proof"

### Site-Wide Disclaimer (Footer + Research Pages)

```
All content on this site is for informational and educational purposes only.
Past performance is not indicative of future results. Trading futures involves
substantial risk of loss. Capo Horn Lab does not provide financial advice,
does not sell trading strategies or signals, and does not guarantee
any specific outcome from backtesting or forward testing.
```

---

*"Beyond the Market Edge" — We test. We measure. We publish the truth.*

*Prepared by Afrodite (Content Lead) — Sprint 2 / Task 2.4*
