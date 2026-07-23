# NEWSLETTER_CONTENT.md — Capo Horn Lab

> **Author:** Afrodite (Content Lead)
> **Sprint:** 4 — Task 4.4
> **Date:** 22 Luglio 2026
> **Status:** Final
> **Voice:** Technical · Precise · Authoritative · Never promotional
> **Claim:** *Beyond the Market Edge*
> **Motto:** *We test. We measure. We publish the truth.*

---

## Table of Contents

1. [Newsletter Identity & Architecture](#1-newsletter-identity--architecture)
2. [Welcome Email Series (3 Emails)](#2-welcome-email-series-3-emails)
3. [HTML Email Templates](#3-html-email-templates)
4. [Research Notification Template](#4-research-notification-template)
5. [Content Calendar — 12 Mesi](#5-content-calendar--12-mesi)
6. [Subject Line Patterns Bank](#6-subject-line-patterns-bank)
7. [CTA Strategy per Email](#7-cta-strategy-per-email)
8. [Brand Signature Block & Style Guide](#8-brand-signature-block--style-guide)
9. [Implementation Notes](#9-implementation-notes)

---

## 1. Newsletter Identity & Architecture

### 1.1 Identity

| Element | Value |
|---------|-------|
| **Name** | Capo Horn Lab Research Brief |
| **Sender name** | Capo Horn Lab |
| **Sender email** | research@capohornlab.com |
| **Frequency** | Maximum 1 per month. No exceptions. |
| **Platform** | Resend (MVP) |
| **Opt-in** | Double opt-in (email verification required) |
| **Unsubscribe** | One-click, instant, no login required |
| **Tracking** | Open + click tracking via Resend pixel |
| **Tone** | Quantitative · Minimal · Authoritative |
| **Purpose** | Notify subscribers of new research. Occasionally share methodology insights. |
| **Anti-purpose** | NOT market commentary · NOT trade ideas · NOT "check out this cool chart" |

### 1.2 Email Taxonomy

| Category | Type | Trigger | Volume | Volume Notes |
|----------|------|---------|--------|--------------|
| **Onboarding** | Welcome Series (3 emails) | Email verified | Per new user | 3 emails over ~5 days, then monthly |
| **Transactional** | Request Received | Strategy submission | Per submission | Single email |
| **Transactional** | Status Change | Admin status update | Per status change | 6 status variants |
| **Transactional** | Clarification Request | Admin needs info | Per clarification | Single email |
| **Transactional** | Password Reset | User request | Per request | Single email |
| **Transactional** | Email Verification | Signup | Per signup | Single email |
| **Marketing** | Research Published | New research | ~1 per month | The core newsletter |
| **Marketing** | Methodology Deep-Dive | Editorial schedule | ~1 per quarter | Optional supplement |
| **Marketing** | Aggregate / Review | Editorial schedule | ~2 per year | Half-year / Year-end |

### 1.3 Email Dependencies Flow

```
User Signs Up
  │
  ├─ Email Verification ────────────> Welcome Email #1 (immediate)
  │                                     │
  │                                     ├─ Welcome #2 (Day +2)
  │                                     │
  │                                     └─ Welcome #3 (Day +5) ────> Invitation to submit
  │
  ├─ Submission ───────────────────> Request Received (immediate)
  │                                     │
  │                                     └─ Status Changes (per update)
  │                                         ├─ In Review
  │                                         ├─ Clarification Request ← Admin question
  │                                         ├─ Accepted
  │                                         ├─ Rejected
  │                                         └─ Completed ──> Results ready
  │
  └─ Research Published ───────────> Notification (sends to ALL active subscribers)
```

---

## 2. Welcome Email Series (3 Emails)

### 2.1 Welcome Email #1 — "Welcome to Capo Horn Lab"

**Purpose:** Confirm signup, set expectations, establish brand voice immediately.
**Delay:** Immediate upon email verification.
**Goal:** New subscriber understands exactly what Capo Horn Lab is (and is not).

---

**Subject:**
```
Welcome to Capo Horn Lab
```

**Preheader:**
```
Submit your first strategy. Track backtests. Access results.
```

**Body (plain text):**
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
Beyond the Market Edge
```

**CTA:**
- Primary: [Submit Your Strategy → /test-your-strategy]
- Secondary: [Read Our Research → /research]

---

### 2.2 Welcome Email #2 — "How It Works: From Hypothesis to Result"

**Purpose:** Educate on the backtesting process. Reduce friction for first submission.
**Delay:** 2 days after Email #1.
**Goal:** Subscriber understands the pipeline and trusts the rigour.

---

**Subject:**
```
How to Get Your Strategy Tested — Capo Horn Lab
```

**Preheader:**
```
A strategy backtest takes 3–10 business days. Here is the full path.
```

**Body (plain text):**
```
Hi [Name],

Now that you have an account, here is exactly how a backtest works
from submission to results.

─── The Pipeline ───

1. You submit → Describe your strategy through our 7-step wizard.
   Entry rules, exit rules, risk parameters, execution details.

2. We review → Our team evaluates your parameters (1–2 business days).
   We check that your rules are deterministic and testable within our
   data scope.

3. We test → We run your strategy against tick-level historical data
   from Databento. Realistic slippage. Realistic commissions.

4. You get results → A full quantitative report: equity curve, Sharpe
   ratio, drawdown, Monte Carlo simulation, trade distribution.

─── What Makes Our Testing Different ───

  • Tick-level data — not OHLC bar replay
  • IS/OOS split — 70/30, never tested on training data
  • Monte Carlo simulation — 1,000+ randomised trade sequences
  • Parameter stability — we check if the edge is robust or fragile
  • Net of costs — every result includes slippage and commissions

─── Next Step ───

Ready to put your strategy to the test?

[Submit Your Strategy → /test-your-strategy]

Not ready yet? Read one of our published studies first to see
the format and rigour you will receive.

[Read Published Research → /research]

— Capo Horn Lab
Beyond the Market Edge
```

**CTA:**
- Primary: [Submit Your Strategy → /test-your-strategy]
- Secondary: [Read Published Research → /research]

---

### 2.3 Welcome Email #3 — "Your First Test: What to Expect When You Submit"

**Purpose:** Remove last barriers to submission. Set expectations for the review process.
**Delay:** 5 days after Email #1 (3 days after Email #2).
**Goal:** Convert the subscriber from passive reader to active client.

---

**Subject:**
```
Ready to Submit? What Happens After You Click "Send"
```

**Preheader:**
```
A walkthrough of the submission process and what to expect after.
```

**Body (plain text):**
```
Hi [Name],

This is your third and final onboarding email. By now you should have
a clear picture of what Capo Horn Lab does and how our backtesting
process works.

This time, we want to walk you through the submission experience itself.

─── The 7-Step Wizard ───

Step 1 — Strategy Identity          What is your strategy called?
Step 2 — Time Settings              Period, timeframe, session
Step 3 — Entry Rules                How does your strategy enter?
Step 4 — Exit Rules                 Stop loss, take profit, risk mgmt
Step 5 — Execution Parameters       Contracts, commissions, slippage
Step 6 — Attachments & Notes        Supporting material (optional)
Step 7 — Review & Submit            Final check before sending

Total time: 10–15 minutes for a well-defined strategy.

─── After You Submit ───

  1. You receive a confirmation email with your Request ID
  2. Our team reviews your parameters (1–2 business days)
  3. We may reach out if we need clarification (see next email)
  4. We run the backtest (3–10 business days)
  5. You receive the full report via email and dashboard

─── The Result ───

Your report includes:
  • Equity curve (IS / OOS)
  • Sharpe ratio (IS / OOS)
  • Profit factor
  • Win rate (with context)
  • Maximum drawdown
  • Trade distribution analysis
  • Monte Carlo simulation (1,000+ paths)
  • Parameter stability assessment

[Submit Your Strategy → /test-your-strategy]

This is your last onboarding email. You will only hear from us now
when new research is published or when we have updates on your
submissions.

— Capo Horn Lab
Beyond the Market Edge
```

**CTA:**
- Primary: [Submit Your Strategy → /test-your-strategy]

---

## 3. HTML Email Templates

### 3.1 Global HTML Shell (Base Template)

All transactional and marketing emails use this shell. Variables: `{{CONTENT}}`, `{{SUBJECT}}`, `{{PREHEADER}}`, `{{UNSUBSCRIBE_URL}}`.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="color-scheme" content="dark light">
  <title>{{SUBJECT}}</title>
  <!--[if mso]>
  <noscript>
    <xml>
      <o:OfficeDocumentSettings>
        <o:PixelsPerInch>96</o:PixelsPerInch>
      </o:OfficeDocumentSettings>
    </xml>
  </noscript>
  <![endif]-->
  <style>
    /* RESET */
    body, table, td, p, a, li, blockquote {
      -webkit-text-size-adjust: 100%;
      -ms-text-size-adjust: 100%;
      margin: 0;
      padding: 0;
      border: 0;
    }
    table, td {
      mso-table-lspace: 0pt;
      mso-table-rspace: 0pt;
    }
    img {
      -ms-interpolation-mode: bicubic;
      border: 0;
      height: auto;
      line-height: 100%;
      outline: none;
      text-decoration: none;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      font-size: 16px;
      line-height: 1.6;
      color: #E2E8F0;
      background-color: #0F172A;
    }
    .email-wrapper {
      background-color: #0F172A;
      padding: 40px 0;
    }
    .email-container {
      max-width: 600px;
      margin: 0 auto;
      background-color: #1E293B;
      border-radius: 8px;
      overflow: hidden;
    }
    .email-header {
      background-color: #0F172A;
      padding: 32px 40px 24px;
      text-align: center;
      border-bottom: 1px solid #334155;
    }
    .brand-name {
      font-size: 20px;
      font-weight: 700;
      color: #F8FAFC;
      letter-spacing: 1px;
      text-transform: uppercase;
    }
    .brand-claim {
      font-size: 13px;
      color: #94A3B8;
      margin-top: 4px;
      letter-spacing: 0.5px;
    }
    .email-body {
      padding: 32px 40px;
      color: #E2E8F0;
    }
    .email-body h1 {
      font-size: 24px;
      font-weight: 700;
      color: #F8FAFC;
      margin: 0 0 16px;
      line-height: 1.3;
    }
    .email-body h2 {
      font-size: 18px;
      font-weight: 600;
      color: #F8FAFC;
      margin: 24px 0 12px;
      line-height: 1.4;
    }
    .email-body p {
      margin: 0 0 16px;
      color: #E2E8F0;
    }
    .email-body ul, .email-body ol {
      margin: 0 0 16px;
      padding-left: 24px;
      color: #CBD5E1;
    }
    .email-body li {
      margin-bottom: 8px;
    }
    .email-body a {
      color: #60A5FA;
      text-decoration: underline;
    }
    .metric-block {
      background-color: #0F172A;
      border-radius: 6px;
      padding: 16px 20px;
      margin: 16px 0 20px;
      border-left: 3px solid #3B82F6;
    }
    .metric-block td {
      padding: 4px 16px 4px 0;
      font-size: 14px;
    }
    .metric-label {
      color: #94A3B8;
      font-size: 13px;
    }
    .metric-value {
      color: #F8FAFC;
      font-weight: 600;
      font-size: 15px;
    }
    .cta-button {
      display: inline-block;
      background-color: #3B82F6;
      color: #FFFFFF !important;
      text-decoration: none !important;
      font-weight: 600;
      font-size: 15px;
      padding: 14px 32px;
      border-radius: 6px;
      margin: 8px 0 16px;
      text-align: center;
    }
    .cta-button-secondary {
      display: inline-block;
      background-color: transparent;
      color: #60A5FA !important;
      text-decoration: none !important;
      font-weight: 500;
      font-size: 14px;
      padding: 10px 24px;
      border-radius: 6px;
      margin: 4px 0 12px;
      border: 1px solid #475569;
      text-align: center;
    }
    .divider {
      height: 1px;
      background-color: #334155;
      margin: 24px 0;
    }
    .status-badge {
      display: inline-block;
      padding: 4px 12px;
      border-radius: 4px;
      font-size: 13px;
      font-weight: 600;
      background-color: #1E293B;
      border: 1px solid #475569;
      color: #F8FAFC;
    }
    .result-badge-positive {
      background-color: #065F46;
      color: #6EE7B7;
      border-color: #059669;
    }
    .result-badge-mixed {
      background-color: #78350F;
      color: #FCD34D;
      border-color: #D97706;
    }
    .result-badge-negative {
      background-color: #7F1D1D;
      color: #FCA5A5;
      border-color: #DC2626;
    }
    .email-footer {
      background-color: #0F172A;
      padding: 24px 40px;
      text-align: center;
      font-size: 12px;
      color: #64748B;
      border-top: 1px solid #334155;
    }
    .email-footer a {
      color: #64748B;
      text-decoration: underline;
    }
    @media only screen and (max-width: 480px) {
      .email-container { border-radius: 0; }
      .email-header { padding: 24px 20px; }
      .email-body { padding: 24px 20px; }
      .email-footer { padding: 20px; }
      .cta-button {
        display: block;
        width: 100%;
        box-sizing: border-box;
      }
    }
  </style>
</head>
<body>
  <div class="email-wrapper">
    <!--[if mso]>
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="600" align="center">
    <tr><td>
    <![endif]-->
    <div class="email-container">
      <div class="email-header">
        <div class="brand-name">Capo Horn Lab</div>
        <div class="brand-claim">Beyond the Market Edge</div>
      </div>
      <div class="email-body">
        {{CONTENT}}
      </div>
      <div class="email-footer">
        <p>Capo Horn Lab &mdash; Beyond the Market Edge</p>
        <p style="margin-top:8px;">
          <a href="{{UNSUBSCRIBE_URL}}">Unsubscribe</a> &nbsp;|&nbsp;
          <a href="https://capohornlab.com">capohornlab.com</a>
        </p>
      </div>
    </div>
    <!--[if mso]>
    </td></tr>
    </table>
    <![endif]-->
  </div>
</body>
</html>
```

---

### 3.2 Welcome Email HTML Content Block

Replace `{{CONTENT}}` in the shell:

```html
<h1>Welcome to Capo Horn Lab</h1>

<p>You now have access to submit trading strategies for quantitative backtesting on tick-level historical data.</p>

<p>Here is what you can do next:</p>

<ol>
  <li><strong>Submit a strategy</strong> &mdash; Tell us your rules. We test them.</li>
  <li><strong>Read our research</strong> &mdash; See the format, rigour, and quality of our published work.</li>
  <li><strong>View your dashboard</strong> &mdash; Track submissions and access results.</li>
</ol>

<p>We test on ES, NQ, CL, and 6E &mdash; tick-level data from Databento, with realistic slippage and commissions. Every result is net of costs.</p>

<p>No strategy selling. No signals. No subscriptions.<br>
Just evidence.</p>

<div class="divider"></div>

<a href="https://capohornlab.com/test-your-strategy" class="cta-button">Submit Your Strategy</a>

<p style="text-align:center; margin-top:4px;">
  <a href="https://capohornlab.com/research">Read Our Research</a>
</p>
```

---

### 3.3 Request Received HTML Content Block

```html
<h1>Request Received</h1>

<p>We have received your backtest request.</p>

<div class="metric-block">
  <strong>Strategy:</strong> [Strategy Name]<br>
  <strong>Instrument:</strong> [ES / NQ / CL / 6E]<br>
  <strong>Request ID:</strong> [REQUEST_ID]<br>
  <strong>Submitted:</strong> [Date]
</div>

<h2>What Happens Next</h2>

<ol>
  <li><strong>Review</strong> &mdash; Our team reviews your parameters (1&ndash;2 business days)</li>
  <li><strong>Clarify</strong> &mdash; We may reach out if we need additional details</li>
  <li><strong>Backtest</strong> &mdash; We run the test against historical tick data (3&ndash;10 business days depending on complexity)</li>
  <li><strong>Deliver</strong> &mdash; You receive a full quantitative report with equity curve, Sharpe ratio, drawdown analysis, and Monte Carlo simulation</li>
</ol>

<div class="divider"></div>

<a href="https://capohornlab.com/dashboard/requests/[REQUEST_ID]" class="cta-button">View Request Status</a>
```

---

### 3.4 Status Change — In Review (In Valutazione) HTML Content Block

```html
<h1>Status Update: In Review</h1>

<p>Your backtest request for <strong>[Strategy Name]</strong> is now in review.</p>

<p>Our team is evaluating your parameters to confirm that the strategy can be tested within our current infrastructure and data scope.</p>

<p>We will update you once the evaluation is complete.</p>

<div class="metric-block">
  <strong>Current status:</strong> <span class="status-badge">In Review</span><br>
  <strong>Request ID:</strong> [REQUEST_ID]
</div>

<div class="divider"></div>

<a href="https://capohornlab.com/dashboard/requests/[REQUEST_ID]" class="cta-button">View Request Details</a>
```

---

### 3.5 Status Change — Accepted (Accettata) HTML Content Block

```html
<h1>Status Update: Accepted</h1>

<p>Good news: your backtest request for <strong>[Strategy Name]</strong> has been accepted.</p>

<p>We have started running the test against historical tick data. Results are typically ready within 3&ndash;10 business days, depending on the complexity and scope of the test.</p>

<p>We will notify you as soon as the report is ready.</p>

<div class="metric-block">
  <strong>Current status:</strong> <span class="status-badge">Accepted &mdash; In Progress</span><br>
  <strong>Request ID:</strong> [REQUEST_ID]
</div>

<div class="divider"></div>

<a href="https://capohornlab.com/dashboard/requests/[REQUEST_ID]" class="cta-button">View Request Details</a>
```

---

### 3.6 Status Change — Rejected (Rifiutata) HTML Content Block

```html
<h1>Status Update: Not Accepted</h1>

<p>After reviewing your submission for <strong>[Strategy Name]</strong>, we are unable to accept it for testing at this time.</p>

<h2>Reason</h2>
<p>[Admin provides specific reason &mdash; e.g. "The strategy rules are not sufficiently defined to produce a deterministic test," "The instrument requested is outside our current coverage," etc.]</p>

<p>If you would like to refine your strategy and resubmit, we welcome a revised request. You can also reach out via our contact page if you have questions about the decision.</p>

<div class="metric-block">
  <strong>Request ID:</strong> [REQUEST_ID]
</div>

<div class="divider"></div>

<a href="https://capohornlab.com/test-your-strategy" class="cta-button">Submit a Revised Strategy</a>
<p style="text-align:center; margin-top:4px;">
  <a href="https://capohornlab.com/contact">Contact Us</a>
</p>
```

---

### 3.7 Status Change — Completed (Completata) HTML Content Block

```html
<h1>Your Backtest Results Are Ready</h1>

<p>Your backtest for <strong>[Strategy Name]</strong> is complete.</p>

<p>The full report is available on your dashboard and includes:</p>

<div class="metric-block">
  &bull; Equity curve (IS / OOS)<br>
  &bull; Sharpe ratio (IS / OOS)<br>
  &bull; Profit factor<br>
  &bull; Win rate (with context)<br>
  &bull; Maximum drawdown<br>
  &bull; Total trades<br>
  &bull; Monte Carlo simulation results<br>
  &bull; Trade distribution analysis
</div>

<div class="divider"></div>

<a href="https://capohornlab.com/dashboard/requests/[REQUEST_ID]" class="cta-button">View &amp; Download Report</a>

<p style="margin-top:16px;">If you would like us to test a variation of this strategy or test the same approach on a different instrument, submit a new request.</p>

<p style="text-align:center;">
  <a href="https://capohornlab.com/test-your-strategy">Submit Another Strategy</a>
</p>
```

---

### 3.8 Clarification Request HTML Content Block

```html
<h1>We Have a Question About Your Strategy</h1>

<p>We are reviewing your <strong>[Strategy Name]</strong> submission and need additional details before we can proceed with the backtest.</p>

<h2>Question</h2>
<p>[Admin's specific question &mdash; e.g. "When you say 'RSI below 30', which RSI period are you using? Default 14? Custom?"]</p>

<p>Please respond through your dashboard or reply to this email with the clarification. Once we hear back, we will resume the review.</p>

<div class="metric-block">
  <strong>Request ID:</strong> [REQUEST_ID]
</div>

<div class="divider"></div>

<a href="https://capohornlab.com/dashboard/requests/[REQUEST_ID]" class="cta-button">Respond via Dashboard</a>
```

---

### 3.9 Password Reset HTML Content Block

```html
<h1>Reset Your Password</h1>

<p>We received a request to reset your Capo Horn Lab password.</p>

<p>Click the link below to set a new password. This link expires in <strong>1 hour</strong>.</p>

<div class="divider"></div>

<a href="https://capohornlab.com/reset-password/[TOKEN]" class="cta-button">Reset Password</a>

<p style="margin-top:16px;">If you did not request a password reset, you can safely ignore this email.</p>
```

---

### 3.10 Email Verification HTML Content Block

```html
<h1>Verify Your Email</h1>

<p>Welcome to Capo Horn Lab. Please verify your email address by clicking the link below.</p>

<div class="divider"></div>

<a href="https://capohornlab.com/verify-email/[TOKEN]" class="cta-button">Verify Email</a>

<p style="margin-top:16px;">Once verified, you will be able to submit strategies and access results.</p>

<p>If you did not create this account, you can ignore this email.</p>
```

---

## 4. Research Notification Template

### 4.1 Plain Text Version

**Trigger:** New research published on the site.
**Audience:** All active newsletter subscribers.
**Frequency:** ~1 per month (tied to research publication).

---

**Subject:**
```
[Research Title] — New Publication from Capo Horn Lab
```

**Preheader:**
```
We tested [hypothesis] on [instrument]. Here is what we found.
```

**Body (plain text):**
```

[Research Title]

[Result Badge: Positive / Mixed / No Edge]

[1-paragraph abstract — the "what" and the "so what"]

We tested whether [hypothesis] on [instrument] over [period].
[Concise finding — 2-3 sentences describing the result,
including whether the edge held up net of costs.]

Key Metrics Snapshot:
  • Sharpe (OOS): [value]
  • Profit Factor: [value]
  • Total Trades: [N]
  • Max Drawdown: [value]%

[Read the Full Study → /research/[slug]]

───

Have a strategy you want tested?
[Submit Your Strategy → /test-your-strategy]

───

— Capo Horn Lab
Beyond the Market Edge

[Unsubscribe link]
```

---

### 4.2 HTML Version

Replace `{{CONTENT}}` in the global shell:

```html
<h1>[Research Title]</h1>

<p>
  <span class="status-badge result-badge-[positive|mixed|negative]">
    [Positive/Mixed/No Edge]
  </span>
</p>

<p>[1-paragraph abstract &mdash; the "what" and the "so what"]</p>

<div class="metric-block">
  <table role="presentation" cellpadding="0" cellspacing="0">
    <tr>
      <td class="metric-label">Sharpe (OOS)</td>
      <td class="metric-value">[value]</td>
    </tr>
    <tr>
      <td class="metric-label">Profit Factor</td>
      <td class="metric-value">[value]</td>
    </tr>
    <tr>
      <td class="metric-label">Total Trades</td>
      <td class="metric-value">[N]</td>
    </tr>
    <tr>
      <td class="metric-label">Max Drawdown</td>
      <td class="metric-value">[value]%</td>
    </tr>
  </table>
</div>

<div class="divider"></div>

<a href="https://capohornlab.com/research/[slug]" class="cta-button">Read the Full Study</a>

<div class="divider"></div>

<h2>Have a Strategy You Want Tested?</h2>
<p>Submit your strategy and get a full quantitative report with equity curve, Sharpe ratio, and Monte Carlo simulation.</p>

<a href="https://capohornlab.com/test-your-strategy" class="cta-button-secondary">Submit Your Strategy</a>
```

---

### 4.3 Trigger Logic

| Condition | Action |
|-----------|--------|
| Research published → `is_published = true` | Queue notification to all `subscriber.is_active = true` |
| Rate limit | Maximum 1 research notification per 14 days per subscriber |
| Suppression | Skip if subscriber received a notification in the last 7 days |
| Retry | 3 retries with exponential backoff (30 min, 2h, 6h) |
| Bounce handling | Mark as inactive after 3 consecutive bounces |

---

## 5. Content Calendar — 12 Mesi

### 5.1 Overview

| Mese | Tipo | Tema | Titolo Provvisorio | Data Suggerita | Trigger |
|------|------|------|--------------------|----------------|---------|
| **Mese 1** | Welcome | Onboarding | *Welcome to Capo Horn Lab: What We Do and Why* | Immediato (signup) | Sito live |
| **Mese 1** | Research | ES 1m Price-Only | *ES 1-Minute Quantitative Research Summary* | Settimana 2 | 1° ricerca pubblicata |
| **Mese 2** | Research | Structure Patterns | *When Structure Meets Reality: Impulse-Retracement on ES* | Settimana 6 | 2° ricerca pubblicata |
| **Mese 3** | Methodology | Pipeline | *How We Backtest: Pipeline Transparency* | Settimana 10 | Editoriale |
| **Mese 4** | Research | NQ Moving Averages | *Moving Averages on NQ: A Systematic Test* | Settimana 14 | 3° ricerca pubblicata |
| **Mese 5** | Methodology | Ethos | *Why We Publish Negative Results — And Why You Should Care* | Settimana 18 | Editoriale |
| **Mese 6** | Research | Volume Profile | *Volume Profile on ES: Signal or Noise?* | Settimana 22 | 4° ricerca pubblicata |
| **Mese 7** | Research | Breakout Patterns | *Breakout Confirmation on NQ: Testing the Retest* | Settimana 26 | 5° ricerca pubblicata |
| **Mese 8** | Methodology | IS/OOS | *IS/OOS Split: Why It Matters for Backtesting* | Settimana 30 | Editoriale |
| **Mese 9** | Research | CL Momentum | *Crude Oil Momentum: 5 Years of Intraday Data* | Settimana 34 | 6° ricerca pubblicata |
| **Mese 10** | Update | 6-Month Review | *Research Progress: 6 Months of Results* | Settimana 38 | Aggregato |
| **Mese 11** | Research | ES Microstructure | *ES Tick-Level Microstructure: Patterns in the Noise* | Settimana 42 | 7° ricerca pubblicata |
| **Mese 12** | Update | Annual Review | *Year in Review: What We Tested, What We Found* | Settimana 48 | Aggregato |

### 5.2 Month-by-Month Detail

#### Mese 1 — Lancio

**Settimana 1-2**
- Welcome email series (3 emails) → tutti i nuovi utenti
- Newsletter #1: Welcome + Research #1 announcement
- Canali: Email + LinkedIn + X

**Deliverables newsletter #1:**
```
Subject: Welcome to Capo Horn Lab + First Research Published
Content:
  - Brief welcome to new subscribers
  - Research #1 highlight: ES 1-Minute Price-Only
  - Key metric snapshot
  - CTA: Read the Full Study
  - CTA: Submit Your Strategy
```

#### Mese 2

**Settimana 5-6**
- Newsletter #2: Research #2 (Structure Patterns on ES)
- LinkedIn thread: 3-5 post su Research #2
- X post: chart + insight

```
Subject: When Structure Meets Reality — New Research on ES
Content:
  - Abstract: Impulse-retracement patterns on ES
  - Key metrics (OOS Sharpe, Trades, Max DD)
  - Key finding paragraph
  - CTA: Read the Full Study
  - CTA: Submit Your Strategy
```

#### Mese 3

**Settimana 9-10**
- Newsletter #3: Methodology Deep-Dive
- Blog post: "How We Backtest: Inside the Capo Horn Lab Pipeline"
- X thread: pipeline visual breakdown

```
Subject: Behind the Backtest: How We Structure Every Study
Content:
  - Pipeline walkthrough: Idea → Code → Data → Analysis → Publication
  - Rigour standards highlight (IS/OOS, Monte Carlo)
  - Why tick-level data matters
  - CTA: Read Our Research
  - CTA: Submit Your Strategy
```

#### Mese 4

**Settimana 13-14**
- Newsletter #4: Research #3 (NQ Moving Averages)
- LinkedIn thread with key charts
- Reddit r/algotrading post

```
Subject: Moving Averages on NQ — A Systematic Test
Content:
  - Abstract: SMA crossover on NQ
  - Performance table (IS vs OOS)
  - Parameter stability findings
  - CTA: Read the Full Study
  - CTA: Submit Your Strategy
```

#### Mese 5

**Settimana 17-18**
- Newsletter #5: Ethos / Brand Piece
- Blog post: "Why We Publish Negative Results"

```
Subject: Why We Publish Negative Results
Content:
  - The value of successful falsification
  - Example from recent research
  - What negative results save you (time, capital, bias)
  - CTA: Read Our Research
  - CTA: Submit Your Strategy
```

#### Mese 6

**Settimana 21-22**
- Newsletter #6: Research #4 (Volume Profile)
- LinkedIn thread with volume distribution charts

```
Subject: Volume Profile on ES — Signal or Noise?
Content:
  - Abstract: Testing volume-based signals
  - Key metrics
  - Comparison against time-based approaches
  - CTA: Read the Full Study
  - CTA: Submit Your Strategy
```

#### Mese 7

**Settimana 25-26**
- Newsletter #7: Research #5 (Breakout Patterns on NQ)
- X post with chart

```
Subject: Breakout Confirmation on NQ — Testing the Retest
Content:
  - Abstract: Breakout-retest pattern on NQ
  - Key metrics
  - Session dependency analysis
  - CTA: Read the Full Study
  - CTA: Submit Your Strategy
```

#### Mese 8

**Settimana 29-30**
- Newsletter #8: Educational Methodology
- Blog post: "IS/OOS Split: Why It Matters"

```
Subject: IS/OOS Split — Why It Matters for Backtesting
Content:
  - What IS/OOS means
  - How data-mining bias inflates results
  - Real example from our research
  - CTA: Read Our Research
  - CTA: Submit Your Strategy
```

#### Mese 9

**Settimana 33-34**
- Newsletter #9: Research #6 (CL Momentum)
- LinkedIn thread with crude oil analysis

```
Subject: Crude Oil Momentum — 5 Years of Intraday Data
Content:
  - Abstract: Momentum in CL
  - Period-specific analysis
  - Key metrics
  - CTA: Read the Full Study
  - CTA: Submit Your Strategy
```

#### Mese 10

**Settimana 37-38**
- Newsletter #10: 6-Month Aggregate
- Blog post: aggregate post

```
Subject: 6 Months of Research: What We've Learned
Content:
  - Studies published: N
  - Positive / Mixed / Negative breakdown
  - Key insights aggregate
  - What's coming next half
  - CTA: Read All Research
  - CTA: Submit Your Strategy
```

#### Mese 11

**Settimana 41-42**
- Newsletter #11: Research #7 (ES Microstructure)
- X thread with tick-level charts

```
Subject: ES Tick-Level Microstructure — Patterns in the Noise
Content:
  - Abstract: Microstructure patterns in ES tick data
  - Key metrics
  - Practical implications
  - CTA: Read the Full Study
  - CTA: Submit Your Strategy
```

#### Mese 12

**Settimana 45-48**
- Newsletter #12: Year in Review
- Blog post: annual summary

```
Subject: Year in Review — What We Tested, What We Found
Content:
  - All 7 studies summary table
  - Methodology improvements
  - Instrument coverage growth
  - Plans for Year 2
  - CTA: Read All Research
  - CTA: Submit Your Strategy
```

### 5.3 Calendar Rules

1. **Research-first**: At least one research-focused email every quarter
2. **No dry months**: Never two months in a row without substantive research content
3. **Quality over schedule**: Never publish just to hit a deadline
4. **Frequency cap**: Maximum 1 email per month per subscriber
5. **Buffer**: Research slots marked "TBD" can flex ±2 weeks based on study completion
6. **Methodology emails**: Can shift to fill gaps if research pipeline is delayed

---

## 6. Subject Line Patterns Bank

### 6.1 Pattern Categories

| Category | Pattern | When to Use | Example |
|----------|---------|-------------|---------|
| **R1** | [Result Badge Prefix] + [Title] | Research published (negative "🔴") | *No edge found: ES 1-Minute Price-Only* |
| **R2** | Question + Finding | Research published (educational hook) | *Do impulse-retracement patterns work? We tested 5 years of ES data.* |
| **R3** | Direct Statement | Research published (neutral) | *New research: Structure patterns on ES — real but not profitable* |
| **R4** | Process-Focused | Methodology / behind-the-scenes | *Behind the backtest: how we structured our ES 1-minute study* |
| **R5** | Aggregate | Half-year / Year-end | *6 months of research: 3 studies, 2 negative, 1 mixed — here's what we learned* |
| **W1** | Welcome | Welcome email #1 | *Welcome to Capo Horn Lab* |
| **W2** | Educational | Welcome email #2 | *How to Get Your Strategy Tested* |
| **W3** | Invitation | Welcome email #3 | *Ready to Submit? What Happens After You Click "Send"* |
| **T1** | Transactional — Received | Request confirmation | *Your backtest request has been received — [ID]* |
| **T2** | Transactional — Update | Status change | *Your request status has been updated: In Review — [ID]* |
| **T3** | Question | Clarification needed | *We have a question about your strategy, [Name]* |
| **T4** | Result Ready | Backtest complete | *Your backtest results are ready — [Strategy Name]* |

### 6.2 Subject Line Bank by Category

#### Research Published (R1–R3)

```
  R1  🔴 No edge found: [Research Title]
  R1  🟢 Positive result: [Research Title]
  R1  🟡 Mixed findings: [Research Title]

  R2  Do [pattern/method] work on [Instrument]? We tested [N] years of data.
  R2  Can [Indicator] predict [Instrument] moves? Here's the data.
  R2  Is [common belief] true? We tested it on [Instrument].

  R3  New research: [Key Finding] on [Instrument]
  R3  [Research Title] — New Publication from Capo Horn Lab
  R3  We tested [hypothesis] on [Instrument]. Here's what we found.
  R3  [Instrument] [Topic] — A Quantitative Study
```

#### Methodology / Process (R4)

```
  R4  Behind the backtest: [Methodology Topic]
  R4  How We Backtest: [Specific Aspect]
  R4  Why [Methodology Concept] Matters for Your Backtest Results
  R4  [Topic] — And Why Most Traders Get It Wrong
  R4  The [Concept] Trap: How to Avoid Data-Mining Bias
```

#### Aggregate / Review (R5)

```
  R5  [N] Months of Research: What We've Learned
  R5  Year in Review: [N] Studies, [X] Instruments, [Key Metric]
  R5  Research Progress: [Topics Covered] and What's Next
  R5  From [Date] to [Date]: Every Study We Published
```

#### Welcome Series (W1–W3)

```
  W1  Welcome to Capo Horn Lab
  W1  Welcome to Capo Horn Lab — Start Here
  W2  How to Get Your Strategy Tested — Capo Horn Lab
  W3  Ready to Submit? What Happens After You Click "Send"
  W3  Your First Backtest: A Step-by-Step Walkthrough
```

#### Transactional (T1–T4)

```
  T1  Your backtest request has been received — [REQUEST_ID]
  T1  Request received: we'll test [Strategy Name] on [Instrument]
  T2  Your request status has been updated: [New Status] — [REQUEST_ID]
  T3  We have a question about your [Strategy Name] submission
  T4  Your backtest results are ready — [Strategy Name]
  T4  Report ready: [Strategy Name] backtest results available
```

### 6.3 Subject Line Rules

| Rule | Guidance |
|------|----------|
| **Length** | 40–60 characters. Max 70. |
| **Emoji** | Use only result badges (🔴🟢🟡) in research notifications. No other emoji. |
| **Personalisation** | Use [Name] in transactional emails only. Not in newsletters. |
| **Capitalisation** | Sentence case. No ALL CAPS except acronyms (IS, OOS, ES, NQ). |
| **Punctuation** | Avoid exclamation marks. Question marks allowed for R2 pattern. |
| **Banned words** | "Proven," "guaranteed," "secret," "easy," "instant" — same as site-wide rules. |
| **Numbers** | Use digits (5 not five) for metrics and data points. |
| **Instrument** | Always use ticker symbol (ES, NQ, CL, 6E) — never full name in subject. |
| **Preheader** | Always pair with a preheader that complements (not repeats) the subject. |

---

## 7. CTA Strategy per Email

### 7.1 CTA Classification

| Type | Copy | Visual | Purpose |
|------|------|--------|---------|
| **Primary Research** | "Read the Full Study" | Blue button (#3B82F6) | Drive traffic to research page |
| **Primary Submission** | "Submit Your Strategy" | Blue button | Convert to submission |
| **Primary Dashboard** | "View Request Status" | Blue button | Drive to dashboard |
| **Primary Results** | "View & Download Report" | Blue button | Deliverable access |
| **Secondary** | "Read Our Research" | Text link | Content discovery |
| **Secondary** | "Contact Us" | Text link | Support path |
| **Tertiary** | "Submit Another Strategy" | Text link | Repeat engagement |
| **Transactional** | "Reset Password" | Blue button | Auth flow |
| **Transactional** | "Verify Email" | Blue button | Auth flow |

### 7.2 CTA Placement per Email Type

| Email Type | Primary CTA | Secondary CTA | Rationale |
|------------|-------------|---------------|-----------|
| **Welcome #1** | Submit Your Strategy | Read Our Research | Convert early. Offer research as lower-friction alternative. |
| **Welcome #2** | Submit Your Strategy | Read Published Research | Educated subscriber → more ready to submit. |
| **Welcome #3** | Submit Your Strategy | — | Last onboarding email. Single focus. |
| **Request Received** | View Request Status | — | Trackability. Reduces support questions. |
| **In Review** | View Request Details | — | Status transparency. |
| **Accepted** | View Request Details | — | Status transparency. |
| **Rejected** | Submit a Revised Strategy | Contact Us | Recovery path. Keep engagement. |
| **Completed** | View & Download Report | Submit Another Strategy | Deliverable first, then re-engagement. |
| **Clarification** | Respond via Dashboard | — | Single action. Speed. |
| **Research Notification** | Read the Full Study | Submit Your Strategy | Content first, conversion second. |
| **Password Reset** | Reset Password | — | Single action. |
| **Email Verification** | Verify Email | — | Single action. |

### 7.3 CTA Tone Rules per Email Type

| Email Type | Tone | Example | Anti-Example |
|------------|------|---------|--------------|
| **Welcome** | Invitational, process-focused | "Submit Your Strategy" | "Start Making Profits Now" |
| **Transactional** | Neutral, informative | "View Request Status" | "Check Your Amazing Results" |
| **Research** | Intellectual, curiosity-driven | "Read the Full Study" | "Don't Miss This Opportunity" |
| **Methodology** | Educational, rigorous | "Read Our Research" | "Learn the Secrets" |
| **Aggregate** | Reflective, cumulative | "Read All Research" | "See What You've Been Missing" |

### 7.4 CTA Visual Guide

```
Welcome / Newsletters:
  ┌─────────────────────────────────┐
  │   [Read the Full Study]        │  ← Primary: Blue #3B82F6
  └─────────────────────────────────┘
  [Submit Your Strategy →]          ← Secondary: Text link, accent blue

Transactional:
  ┌─────────────────────────────────┐
  │   [View Request Status]        │  ← Primary: Blue #3B82F6
  └─────────────────────────────────┘
```

### 7.5 CTA Frequency Rules

| Rule | Detail |
|------|--------|
| **Primary CTAs per email** | Exactly 1 |
| **Secondary CTAs per email** | Maximum 2 |
| **Total CTAs per email** | Maximum 3 (including text links) |
| **Above the fold** | Primary CTA must appear in first 50% of content |
| **Repetition** | Never repeat the same CTA copy in the same email |
| **Button first** | Primary CTA is always a button. Secondary CTAs can be text links. |

---

## 8. Brand Signature Block & Style Guide

### 8.1 Brand Signature (All Emails)

```
— Capo Horn Lab
Beyond the Market Edge
research@capohornlab.com
[Unsubscribe link]
```

### 8.2 Site-Wide Disclaimer (Footer)

```
All content on this site is for informational and educational purposes only.
Past performance is not indicative of future results. Trading futures involves
substantial risk of loss. Capo Horn Lab does not provide financial advice,
does not sell trading strategies or signals, and does not guarantee
any specific outcome from backtesting or forward testing.
```

### 8.3 Tone Rules — Email-Specific

| Axis | Always | Never |
|------|--------|-------|
| **Tone** | Confident but humble. Authoritative but not arrogant. Warm but not salesy. | Hype, urgency, FOMO, "get rich," "secret," "proven system" |
| **Vocabulary** | "Hypothesis," "falsifiable," "reproducible," "net of costs," "edge," "distribution," "statistical significance" | "Guaranteed," "easy money," "100% win rate," "insider," "guru," "secret formula," "proven" |
| **Structure** | Declarative, concise. Short paragraphs. Bullet points where precise. | Run-on marketing copy. Wall-of-text testimonials. |
| **Pronouns** | "We" (lab identity), "You" (client in CTAs only), "Our research shows…" | Overuse of "I" — the lab speaks, not an individual. |
| **Data** | Tables, charts, quantitative summaries. "Sharpe: 0.12 IS / -0.08 OOS" | Vague percentages. Cherry-picked best-case metrics. |

### 8.4 Banned Terms in All Emails

```
❌ "proven" / "guaranteed" / "secret" / "hidden" / "revealed"
❌ "guru" / "expert" / "master"
❌ "easy" / "simple" / "instant" / "immediate"
❌ "passive income" / "financial freedom" / "millionaire" / "wealth"
❌ "win rate" without profit factor and Sharpe context
❌ "backtested" without specifying slippage and commission assumptions
❌ Exclamation marks in subject lines (except transactional confirmations)
❌ Emoji other than 🔴🟢🟡 result badges
```

### 8.5 Required Phrases

```
✅ "falsifiable" — our results can be disproven by future data
✅ "reproducible" — methodology is transparent
✅ "net of costs" — every result includes transaction costs
✅ "statistical significance" — or lack thereof
✅ "limitations" — every study has them, and we name them
✅ "hypothesis" — not "prediction" or "forecast"
✅ "evidence" — not "proof"
```

---

## 9. Implementation Notes

### 9.1 Technical Variables

All dynamic values must be injected by the ARQ worker or transactional email service:

| Variable | Used In | Source |
|----------|---------|--------|
| `[Name]` | Transactional emails | `User.full_name` |
| `[REQUEST_ID]` | Transactional emails | `StrategyRequest.id` (short UUID) |
| `[Strategy Name]` | Transactional emails | `StrategyRequest.strategy_name` |
| `[TOKEN]` | Auth emails | `User.reset_token / verify_token` |
| `[UNSUBSCRIBE_URL]` | All marketing emails | `NewsletterSubscriber.token` |
| `[Research Title]` | Research notifications | `Research.title` |
| `[slug]` | Research notifications | `Research.slug` |
| `[value]` metrics | Research notifications | `ResearchMeta.metrics` |

### 9.2 Sending Schedule

| Email Type | Sending Window | Delay |
|------------|---------------|-------|
| Welcome #1 | Immediate | After email verification |
| Welcome #2 | 10:00 UTC | 48h after Welcome #1 |
| Welcome #3 | 10:00 UTC | 120h after Welcome #1 |
| Transactional (all) | Immediate | On trigger event |
| Research Notification | 14:00 UTC Thursday | On research publish |
| Methodology / Aggregate | 14:00 UTC Thursday | Per editorial calendar |

### 9.3 Unsubscribe Handling

- **Method:** One-click unsubscribe via URL parameter (`{{UNSUBSCRIBE_URL}}`)
- **Speed:** Instant. No login required.
- **Confirmation:** Show inline "You've been unsubscribed" page. Send confirmation email.
- **Re-subscribe:** Allow via site (newsletter signup form + new verification).
- **Suppression:** Unsubscribed emails permanently suppressed. Never re-imported.

### 9.4 Metrics Tracking

| Metric | Tracking Method | Purpose |
|--------|----------------|---------|
| Sent | Resend API response | Delivery confirmation |
| Delivered | Resend webhook | Bounce / spam detection |
| Opened | Resend tracking pixel | Engagement rate |
| Clicked | Resend link tracking | CTA effectiveness |
| Unsubscribed | URL click | Churn rate |
| Complained | Resend webhook (FBL) | Spam complaint rate |

### 9.5 Target Benchmarks

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Open rate | > 35% | < 25% |
| Click rate | > 5% | < 3% |
| Unsubscribe rate | < 0.5% per send | > 1% per send |
| Bounce rate | < 2% | > 5% |
| Spam complaint rate | < 0.1% | > 0.1% |

---

*"Beyond the Market Edge" — We test. We measure. We publish the truth.*

*Prepared by Afrodite (Content Lead) — Sprint 4 / Task 4.4*
