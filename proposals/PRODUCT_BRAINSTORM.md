# Capo Horn Lab — Product Brainstorming Proposal

> **Author:** Atlas (Product/UX Lead)
> **Date:** 2026-07-22
> **Claim:** *Beyond the Market Edge*
> **Language:** English (primary)
> **Style:** Technical · Quantitative · Premium · Minimal

---

## 1. Concept Map — Site Hierarchy

```
CAPO HORN LAB
│
├─ PUBLIC (no auth)
│  ├─ HOME          — Brand intro, value prop, latest research teaser, CTA → Test Your Strategy
│  ├─ ABOUT         — Team (quant background), mission, methodology ethos
│  ├─ METHOD        — How backtesting works, data pipeline, statistical rigour, FAQ accordion
│  ├─ RESEARCH      — Published quantitative research (filterable gallery)
│  │  ├─ Research Detail   — Full report: hypothesis, data, methodology, charts, interpretation
│  │  └─ Download PDF      — Print-friendly version
│  ├─ TEST YOUR STRATEGY  — Backtest submission wizard (see §4)
│  ├─ CONTACT       — Form + email + social (no newsletter signup here — it's on Home & Research)
│  └─ AUTH GATES
│     ├─ LOGIN      — Email/password or OAuth (Google/GitHub)
│     ├─ SIGNUP     — Email + password + accept terms
│     └─ RESET PWD  — Email token flow
│
├─ AUTHENTICATED (client area)
│  ├─ DASHBOARD     — My requests overview (status badges, last updated)
│  ├─ REQUEST DETAIL — Full submission read-only view + status timeline + admin notes
│  ├─ SUBMIT NEW    — Re-route to /test-your-strategy (pre-filled if returning)
│  └─ PROFILE       — Name, email, password change, notification prefs
│
├─ ADMIN (role-gated)
│  ├─ DASHBOARD     — Queue summary: pending, in evaluation, completed counts
│  ├─ REQUESTS      — Full table: filter by status, date, instrument
│  ├─ REQUEST DETAIL — Read params, download attachments, add internal notes
│  │  ├─ Change status workflow (dropdown: Inviata → Info mancanti → In valutazione → Accettata → In lavorazione → Completata → Rifiutata)
│  │  └─ Request clarification (email trigger to client)
│  ├─ RESEARCH MANAGER — Draft / publish / unpublish research articles
│  └─ USERS         — View / disable users, basic role management
│
└─ SYSTEM
   ├─ NEWSLETTER    — Mailchimp / Resend webhook: triggers on research publish
   └─ NOTIFICATIONS — Email: submission received, status change, clarification requested, research published
```

---

## 2. User Flows

### 2.1 Anonymous → Lead
```
HOME → Method (validate rigour) → Research (read a report) → Test Your Strategy → signup prompt → SIGNUP → DASHBOARD
```

### 2.2 Returning Client
```
Email link (magic or reset) → LOGIN → DASHBOARD (see status) → REQUEST DETAIL (download result)
```

### 2.3 Admin Workflow
```
LOGIN (admin) → ADMIN DASHBOARD → REQUEST DETAIL → review → add note / change status / request clarification → email sent → mark complete → publish research
```

### 2.4 Research Publication
```
ADMIN → RESEARCH MANAGER → write + upload charts → set category/tags → PUBLISH → auto-email newsletter → Home banner updates → Research gallery refreshes
```

---

## 3. Page-by-Page Architecture

### HOME
- **Hero**: "Beyond the Market Edge" + subtitle explaining quantitative backtesting mission
- **Trust signals**: Logos of instruments tested (NQ, ES, CL — not broker logos)
- **How it works**: 3-step visual (Describe → We Backtest → You Get Results)
- **Latest research**: Card teaser (latest 2 reports) → CTA "Read Research"
- **CTA block**: "Have a strategy? Test it with real data." → /test-your-strategy
- **Footer**: Newsletter signup, quick links, "data-driven, not guru-driven" disclaimer

### ABOUT
- **Mission statement**: Rigour over hype. No strategy selling. Just data.
- **Team**: Photo-less (or small headshots), emphasis on quant background, years in markets
- **Philosophy**: Brief on why most retail strategies fail, how proper backtesting helps
- **Data sources**: Databento, tick data, multi-year history

### METHOD
- **Pipeline graphic**: Idea → Formalize Rules → Code → Run on Tick Data → Analyze → Publish
- **Rigour standards**: IS/OOS split, Monte Carlo, parameter stability, multiple timeframes
- **Data**: What instruments, tick vs minute, slippage model, commission assumptions
- **FAQ accordion**: "What's the difference between backtesting and forward testing?", "Do you sell strategies?" (no), "How long does it take?"

### RESEARCH
- **Gallery layout**: Card grid with title, instrument, date, excerpt, one key metric (Sharpe / Profit Factor)
- **Filters**: By instrument (ES, NQ, CL), by year, by theme (e.g. microstructure, statistical)
- **Detail page**:
  - Sticky sidebar: quick stats (Sharpe, CAGR, Max DD, Trades)
  - Body: Objective → Hypothesis → Data → Method → Results → Charts → Interpretation
  - Chart gallery: equity curve, drawdown, monthly heatmap, by-day/by-hour, IS vs OOS
  - Download PDF button
- **Empty state**: "No research published yet. Subscribe to be notified."

### CONTACT
- Minimal form: Name, Email, Subject, Message
- Direct email fallback visible
- No phone, no address — pure remote quant lab positioning

---

## 4. Test Your Strategy — Backtest Submission Module (deep dive)

The core product interaction. Must feel technical and precise, not like a support ticket.

### 4.1 Entry Point
From: `/test-your-strategy`, any nav link, Home CTA
- **If not logged in**: Show hero + "Sign up to submit your strategy" → redirects after auth
- **If logged in**: Go straight to form

### 4.2 Form Architecture (multi-step wizard, progress bar)

| Step | Section | Fields |
|------|---------|--------|
| **1** | **Strategy Identity** | Name*, brief description*, asset class & instrument* (NQ, ES, CL, other — dropdown with free text) |
| **2** | **Time Settings** | Timeframe (1m, 5m, 15m, 1h, Daily), historical period (start date* – end date*), session times (presets: RTH, ETH, Custom) |
| **3** | **Rules — Entry** | Direction (Long / Short / Both), entry trigger* (free text: "Buy when SMA(20) > SMA(50) AND RSI < 30"), indicator parameters (free form — key-value pairs, e.g. SMA period: 20) |
| **4** | **Rules — Exit** | Stop Loss* (fixed ticks / ATR multiple / %), Take Profit, Trailing Stop (on/off + step), Breakeven, time-based exit flag |
| **5** | **Execution** | Contracts* (1, 2, 5, 10+), commissions* (per lot), slippage* (ticks), position sizing (fixed / % equity) |
| **6** | **Attachments** | File uploads (max 5): screenshots of the strategy's own tests, code snippets (.py/.txt), PDF notes, images of charts. Structured notes field* |
| **7** | **Review & Submit** | Full summary card, edit any step. Confirm + Submit → confirmation screen + email |

**Design principles for the form:**
- All *free text* entry rules because we're not auto-backtesting — we manually review. The form captures structure so the admin can *understand instantly*, not so a machine can execute.
- Visual separation between **required** and **optional**. Strategy name, instrument, period, entry, SL, contracts are required — everything else helps but isn't blocking.
- Progress indicators with step numbers. Prevent multi-click submit.

### 4.3 Post-Submission Flow

```
SUBMIT → "Request received" screen (request ID + summary) → Email sent → DASHBOARD shows status: "Inviata"
                                                                    ↓
Request lands in Admin queue → Admin reviews → changes status
                                                                    ↓
Client sees update in Dashboard → Email notification → Client can reply via contact (or in-app notes in v2)
                                                                    ↓
Admin completes test → status: "Completata" → PDF/summary attached → Client downloads from REQUEST DETAIL
```

### 4.4 Status Lifecycle

```
Inviata ──→ Info mancanti ──→ Inviata (resubmit)
    │
    └──→ In valutazione ──→ Accettata ──→ In lavorazione ──→ Completata
                               │
                               └──→ Rifiutata
```

Each status change triggers an email to the client with a short explanation.

---

## 5. Visual Identity Notes

- **Color**: Dark navy (`#0F172A`) as primary background, off-white (`#F1F5F9`) for text/cards, accent blue (`#3B82F6`) for interactive elements, amber (`#F59E0B`) for data viz highlights
- **Typography**: System font stack or Inter (clean, readable at small sizes on charts)
- **Layout**: Generous whitespace, max-width 1200px content, left-aligned navigation
- **Imagery**: Abstract data visualizations, chart patterns, ocean/navigation metaphor — *no* stock photos of traders

---

## 6. Newsletter Integration Points

| Trigger | Email Content |
|---------|--------------|
| Research published | Summary excerpt + link to full article |
| New Method content | "How we test: behind the scenes" |
| Occasional (max 1/month) | Market structure observations, data-driven insights |

No weekly signals. No "market moving" content. Pure quantitative communication.

---

## 7. Open Questions (to discuss with Dioniso)

1. **Single-page wizard vs. multi-page** for "Test Your Strategy"? I propose single-page wizard (all on `/test-your-strategy` with JS step management) — less navigation friction, better progress persistence.
2. **Admin features**: MVP should have status management + notes. File attachment management for admin (upload results PDFs) — needed at MVP?
3. **Research page**: Will research be written as markdown rendered to HTML, or as uploaded PDFs with metadata? I propose markdown + chart image uploads — better UX, searchable.
4. **Auth method**: Traditional email/password + magic link? Or OAuth-only? I'd suggest both for flexibility.
5. **Newsletter**: Third-party (Mailchimp, Resend) or custom? I'd start with Resend API — developer-friendly, tracks opens/clicks, simple webhook.
