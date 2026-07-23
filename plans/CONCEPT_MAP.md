# 🗺️ Capo Horn Lab — Mappa Concettuale Unificata

> **Sintesi da 4 proposte:** Atlas (Prodotto) · Midas (Ricerche) · Cratos (Backend) · Afrodite (Content)
> **Data:** 22 Luglio 2026
> **Claim:** *Beyond the Market Edge*

---

## Indice

1. [Mappa Architetturale del Sito](#1-mappa-architetturale-del-sito)
2. [Mappa Entità / Dati](#2-mappa-entità--dati)
3. [Mappa dei Flussi (User Journey)](#3-mappa-dei-flussi-user-journey)
4. [Mappa delle Dipendenze](#4-mappa-delle-dipendenze)
5. [Stack Tecnologico Finale Unificato](#5-stack-tecnologico-finale-unificato)
6. [Schema MVP vs Future](#6-schema-mvp-vs-future)

---

## 1. Mappa Architetturale del Sito

```
CAPO HORN LAB
│
├─ 🌐 ZONA PUBBLICA (no auth)
│  │
│  ├─ HOME  (/)
│  │   ├─ Hero: "Beyond the Market Edge"
│  │   ├─ Trust Signals: [ES] [NQ] [CL] [6E] [YM]
│  │   ├─ How It Works (3-step: Describe → We Backtest → Results)
│  │   ├─ Latest Research Teaser (2 card grid)
│  │   ├─ Why Capo Horn Lab (comparativa "What We Are / What We Are Not")
│  │   └─ Footer CTA + Newsletter signup
│  │
│  ├─ ABOUT  (/about)
│  │   ├─ Mission statement
│  │   ├─ Philosophy (rigour over hype)
│  │   ├─ Team (quant background, no stock photos)
│  │   ├─ Data Infrastructure (Databento, tick data, Python pipeline)
│  │   └─ One-liner closing: "We sell the truth"
│  │
│  ├─ METHOD  (/method)
│  │   ├─ Pipeline visual: Idea → Rules → Code → Tick Data → Analysis → Publication
│  │   ├─ Rigour Standards (IS/OOS, Monte Carlo, Parameter Stability, Costs, Multi-TF)
│  │   ├─ Data Section (instruments, depth, resolution, slippage, commissions)
│  │   └─ FAQ Accordion (6 domande: selling strategies? TradingView? tempi? crypto? fallimento? esempio?)
│  │
│  ├─ RESEARCH  (/research)
│  │   ├─ Overview Gallery  (/research/)
│  │   │   ├─ Cards: titolo, data, badge strumento, badge esito 🟢/🔴/🟡, abstract 2 righe, metrica chiave
│  │   │   ├─ Filtri: per strumento (ES/NQ/CL/Altro), per anno, per tema
│  │   │   └─ Ordinamento: più recenti, più letti, A-Z
│  │   │
│  │   ├─ Research Detail  (/research/<slug>)
│  │   │   ├─ Sticky sidebar: Sharpe, CAGR, Max DD, N Trades
│  │   │   ├─ Sezioni: Obiettivo → Ipotesi → Dati → Metodologia → Risultati → Interpretazione → Limitazioni → Conclusioni → Riferimenti
│  │   │   ├─ Galleria grafici (MVP: 7, Full: 13)
│  │   │   ├─ Download PDF button
│  │   │   └─ CTA block: "Have a strategy? Put it to the test."
│  │   │
│  │   └─ Methodology Page  (/research/methodology/) [FUTURE]
│  │
│  ├─ TEST YOUR STRATEGY  (/test-your-strategy)
│  │   ├─ Pre-auth Hero (invito a signup/login)
│  │   └─ Multi-step wizard (7 steps — solo se autenticato)
│  │       ├─ Step 1: Strategy Identity (nome*, descrizione*, asset class*, strumento*)
│  │       ├─ Step 2: Time Settings (timeframe*, periodo start/end*, session times)
│  │       ├─ Step 3: Entry Rules (direzione*, trigger* text, indicatori params)
│  │       ├─ Step 4: Exit Rules (SL*, TP, trailing, BE, time-based)
│  │       ├─ Step 5: Execution (contratti*, commissioni*, slippage*, sizing)
│  │       ├─ Step 6: Attachments (upload max 5 files, notes*)
│  │       └─ Step 7: Review & Submit (summary card → conferma)
│  │
│  ├─ CONTACT  (/contact)
│  │   └─ Form: Name, Email, Subject, Message + email diretta fallback
│  │
│  ├─ BLOG  (/blog) [FUTURE — contenuti metodologici e critiche separati dalle ricerche]
│  │
│  └─ 🔐 AUTH GATES
│      ├─ LOGIN  (/login)
│      │   └─ Email/password → JWT (httpOnly cookie) + forgot password link
│      ├─ SIGNUP  (/signup)
│      │   └─ Email + password + conferma password + accetta terms
│      └─ RESET PASSWORD  (/reset-password)
│          └─ Email token flow (2 richieste/ora)
│
├─ 👤 ZONA AUTENTICATA (client area)
│  │  [Auth gate: JWT valido]
│  │
│  ├─ DASHBOARD  (/dashboard)
│  │   ├─ My Requests Overview (card grid con status badges)
│  │   ├─ Ultima attività (timestamp ultimo aggiornamento)
│  │   └─ CTA: New Submission
│  │
│  ├─ REQUEST DETAIL  (/requests/:id)
│  │   ├─ Read-only view of full submission
│  │   ├─ Status Timeline (da status_history)
│  │   ├─ Admin Notes (se presenti)
│  │   ├─ Download attachments
│  │   └─ Download result (PDF quando completata)
│  │
│  ├─ SUBMIT NEW  → redirect a /test-your-strategy
│  │
│  └─ PROFILE  (/profile)
│      ├─ Nome, Email
│      ├─ Cambio password
│      ├─ Notifiche prefs (FUTURE)
│      └─ Newsletter subscription status
│
├─ ⚙️ ZONA ADMIN (role-gated: is_admin=true)
│  │  [Auth gate: JWT valido + is_admin flag]
│  │
│  ├─ ADMIN DASHBOARD  (/admin)
│  │   ├─ KPI cards: Inviate | Info Manc. | In Valut. | Accettate | Completate
│  │   ├─ Ultime richieste (tabella paginata)
│  │   ├─ Nuove registrazioni oggi
│  │   ├─ Newsletter iscritti totali
│  │   └─ Ultimo accesso admin
│  │
│  ├─ REQUESTS  (/admin/requests)
│  │   ├─ Tabella completa con filtri (status, data, cliente, parola chiave)
│  │   └─ Azioni bulk (FUTURE)
│  │
│  ├─ REQUEST DETAIL  (/admin/requests/:id)
│  │   ├─ Full submission view (params, attachments)
│  │   ├─ Status dropdown → cambia stato + nota obbligatoria
│  │   ├─ Note interne (CRUD)
│  │   ├─ Richiedi chiarimenti (email trigger)
│  │   └─ Status history timeline
│  │
│  ├─ RESEARCH MANAGER  (/admin/research)
│  │   ├─ Lista ricerche (bozza/pubblicata)
│  │   ├─ Crea/Modifica ricerca (titolo, slug, sezioni, charts, files)
│  │   └─ Pubblica / Annulla pubblicazione
│  │
│  ├─ USERS  (/admin/users)
│  │   ├─ Lista utenti
│  │   └─ Modifica (admin toggle, disabilita)
│  │
│  └─ NEWSLETTER  (/admin/newsletter) [FUTURE]
│      ├─ Gestione iscritti
│      ├─ Crea campagna
│      └─ Stats invio
│
└─ 🔧 ZONA SISTEMA (infrastruttura)
    │
    ├─ NEWSLETTER SYSTEM
    │   ├─ Iscrizione doppio opt-in (Resend)
    │   ├─ Campagne via ARQ worker (Redis-backed)
    │   ├─ Tracking aperture/click (Resend pixel)
    │   └─ Unsubscribe one-click (/newsletter/unsubscribe/:token)
    │
    ├─ NOTIFICHE EMAIL (tutte via Resend)
    │   ├─ Benvenuto / Verifica email
    │   ├─ Conferma richiesta strategia
    │   ├─ Cambio stato richiesta
    │   ├─ Richiesta chiarimenti
    │   ├─ Nuova ricerca pubblicata
    │   └─ Password reset
    │
    ├─ FILE STORAGE
    │   ├─ MVP: locale (D:\CapoHornLab\uploads\)
    │   └─ FUTURE: S3 / Cloudflare R2
    │
    └─ API HEALTH
        ├─ GET /health (pubblico)
        └─ GET /health/ready (DB + Redis + storage)
```

---

## 2. Mappa Entità / Dati

```
┌──────────────────────────────────────────────────────────────────┐
│                    ENTITY RELATIONSHIP MAP                        │
│                                                                   │
│  ┌──────────────┐       ┌──────────────────────┐                 │
│  │     User     │1──N──>│   StrategyRequest    │                 │
│  │──────────────│       │──────────────────────│                 │
│  │ id (UUID)    │       │ id (UUID)            │                 │
│  │ email        │       │ status (enum: 7)     │                 │
│  │ password_hash│       │ strategy_name        │                 │
│  │ full_name    │       │ description          │                 │
│  │ company      │       │ instrument           │                 │
│  │ is_admin     │       │ timeframe            │                 │
│  │ is_active    │       │ historical_period    │                 │
│  │ email_verif. │       │ entry_rules          │                 │
│  │ last_login   │       │ exit_rules           │                 │
│  │ created_at   │       │ stop_loss            │                 │
│  └──────┬───────┘       │ take_profit          │                 │
│         │               │ trailing_stop        │                 │
│         │               │ break_even           │                 │
│         │               │ session_times        │                 │
│         │               │ contracts            │                 │
│         │               │ commission_slippage  │                 │
│         │               │ indicators_params    │─── JSONB        │
│         │               │ screenshots_notes    │                 │
│         │               │ additional_notes     │                 │
│         │               │ admin_notes          │                 │
│         │               │ clarification_req.   │                 │
│         │               │ submitted_at         │                 │
│         │               │ evaluated_at         │                 │
│         │               │ completed_at         │                 │
│         │               │ created_at/updated_at│                 │
│         │               └──────────┬───────────┘                 │
│         │                          │                             │
│         │             1────────────┼────────────1                │
│         │             │            │            │                │
│         │             ▼            ▼            ▼                │
│         │    ┌────────────┐ ┌──────────┐ ┌──────────────┐       │
│         │    │ Attachment │ │StatusHist│ │InternalNote  │       │
│         │    │────────────│ │─────────│ │──────────────│       │
│         │    │ id (UUID)  │ │ id (UUID)│ │ id (UUID)    │       │
│         │    │ request_id │ │request_id│ │ request_id   │       │
│         │    │ file_name  │ │from_stat │ │ author_id    │──>User│
│         │    │ file_path  │ │to_status │ │ content      │       │
│         │    │ file_size  │ │changed_by│──>User│ created_at      │
│         │    │ mime_type  │ │ note     │ │ updated_at   │       │
│         │    │ uploaded_at│ │created_at│ └──────────────┘       │
│         │    └────────────┘ └──────────┘                         │
│         │                                                        │
│         │              ┌────────────────────┐                    │
│         │              │      Research      │                    │
│         │              │────────────────────│                    │
│         │              │ id (UUID)          │                    │
│         │              │ title              │                    │
│         │              │ slug (UNIQUE)      │                    │
│         │              │ abstract           │                    │
│         │              │ objective          │                    │
│         │              │ hypothesis         │                    │
│         │              │ instrument         │                    │
│         │              │ period             │                    │
│         │              │ methodology        │                    │
│         │              │ data_sources       │                    │
│         │              │ results_summary    │                    │
│         │              │ interpretation     │                    │
│         │              │ limitations        │                    │
│         │              │ conclusions        │                    │
│         │              │ published (bool)   │                    │
│         │              │ published_at       │                    │
│         │              └────────┬───────────┘                    │
│         │                       │                               │
│         │              1────────┼────────1                      │
│         │              │        │        │                      │
│         │              ▼        ▼        ▼                      │
│         │     ┌────────────┐ ┌────────┐ ┌──────────────┐       │
│         │     │ResearchChrt│ │Research│ │ ResearchMeta │       │
│         │     │────────────│ │File    │ │ (ricerca.yml)│       │
│         │     │ research_id│ │────────│ │──────────────│       │
│         │     │ chart_type │ │file_name│ │ result       │       │
│         │     │ file_path  │ │file_path│ │ tags[]       │       │
│         │     │ caption    │ │mime_type│ │ metrics      │       │
│         │     │ sort_order │ │file_size│ │ team         │       │
│         │     └────────────┘ └────────┘ │ charts: mvp/full│    │
│         │                               └──────────────┘       │
│         │                                                        │
│         │              ┌────────────────────┐                    │
│         │              │ NewsletterSubscriber│                   │
│         │              │────────────────────│                    │
│         │      ┌──N────│ id (UUID)          │                    │
│         │      │       │ email (UNIQUE)     │                    │
│         │      │       │ name               │                    │
│         │      │       │ user_id ───────────│──>User (opzionale) │
│         │      │       │ subscribed_at      │                    │
│         │      │       │ unsubscribed_at    │                    │
│         │      │       │ is_active          │                    │
│         │      │       │ token (UNIQUE)     │                    │
│         │      │       └────────┬───────────┘                    │
│         │      │                │                                │
│         │      │    N───────────┼────────N                       │
│         │      │   │           │        │                       │
│         │      │   ▼           ▼        ▼                       │
│         │  ┌──────────────────────────────────────────────┐     │
│         │  │          NewsletterCampaign                   │     │
│         │  │──────────────────────────────────────────────│     │
│         │  │ id (UUID) · title · subject · preheader      │     │
│         │  │ html_content · plain_text · status (enum: 4) │     │
│         │  │ sent_at · created_by ───>User                  │     │
│         │  └──────────────┬───────────────────┘             │     │
│         │                 │                                 │     │
│         │        1────────┼────────1                        │     │
│         │        │        │        │                       │     │
│         │        ▼        ▼        ▼                       │     │
│         │  ┌────────────┐ ┌──────────────┐  N──────────N   │     │
│         │  │Newsletter  │ │NewsletterSend│ │ Subscriber  │       │
│         │  │Attachment  │ │──────────────│ │   (già sopra│       │
│         │  │────────────│ │ campaign_id  │ │             │       │
│         │  │ campaign_id │ │ subscriber_id│ │             │       │
│         │  │ file_name   │ │ status (enum)│ │             │       │
│         │  │ file_path   │ │ sent_at      │ │             │       │
│         │  │ mime_type   │ │ opened_at    │ │             │       │
│         │  │ file_size   │ │ UNIQUE(camp+ │ │             │       │
│         │  └────────────┘ │   subscr)    │ │             │       │
│         │                 └──────────────┘ │             │       │
│         │                                  │             │       │
│         │              ┌────────────────┐  │             │       │
│         │              │  LoginHistory  │  │             │       │
│         │              │────────────────│  │             │       │
│         └──────N──────>│ user_id        │  │             │       │
│                        │ ip_address     │  │             │       │
│                        │ user_agent     │  │             │       │
│                        │ success (bool) │  │             │       │
│                        │ failure_reason │  │             │       │
│                        │ created_at     │  │             │       │
│                        └────────────────┘  │             │       │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘

┌──── LEGENDA RELAZIONI ──────────────────────────────────────────┐
│                                                                  │
│  User 1──N StrategyRequest    User 1──N LoginHistory            │
│  User 1──N NewsletterSubscriber                                  │
│  StrategyRequest 1──N Attachment                                 │
│  StrategyRequest 1──N StatusHistory                              │
│  StrategyRequest 1──N InternalNote (admin only → author_id)      │
│  Research 1──N ResearchChart      Research 1──N ResearchFile     │
│  Research 1──1 ResearchMeta (ricerca.yml — metadati estesi)     │
│  NewsletterCampaign 1──N NewsletterAttachment                    │
│  NewsletterCampaign N──M NewsletterSubscriber (via sends)        │
│  NewsletterCampaign 1──N NewsletterSend                          │
│                                                                  │
│  TUTTI GLI ID: UUID v4                                           │
│  TUTTE LE TABELLE: created_at / updated_at TIMESTAMPTZ           │
│  SOFT DELETE: is_active flag (no hard delete sui dati utente)    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. Mappa dei Flussi (User Journey)

### 3.1 Anonymous → Lead (Primo Contatto)

```
[ACQUISITION]                            [CONVERSION]                 [ATTIVAZIONE]
                                                                   
  ┌──────────┐     ┌──────────┐     ┌─────────────┐     ┌──────────┐     ┌──────────┐
  │  Google  │     │ LinkedIn │     │    Home     │     │ Research │     │  Method  │
  │  Search  │     │ / Reddit │────>│  (/read)    │────>│  (/read)  │────>│  (/read) │
  └──────────┘     └──────────┘     └──────┬──────┘     └─────┬────┘     └────┬─────┘
                                           │                  │               │
                                           ▼                  ▼               ▼
                              ┌─────────────────────────────────────────────────┐
                              │           Trust Building Stage                  │
                              │  • Legge value proposition (Home)              │
                              │  • Legge ricerca → valuta rigore (Research)    │
                              │  • Capisce metodologia (Method)                │
                              │  • Vede risultati negativi → brand credibility │
                              └───────────────────┬─────────────────────────────┘
                                                  │
                                                  ▼
                              ┌──────────────────────────────────┐
                              │  DECISION POINT                  │
                              │  "Voglio testare la mia strategia"│
                              └──────────────────────────────────┘
                                                  │
                                                  ▼
                              ┌──────────────────────────────────┐
                              │  /test-your-strategy             │
                              │  → Pre-auth Hero                 │
                              │  → CTA: [Sign Up to Submit]     │
                              └──────────────────────────────────┘
                                                  │
                                                  ▼
                              ┌──────────────────────────────────┐
                              │  SIGNUP  (/signup)               │
                              │  • Email + password              │
                              │  • Verifica email (token)        │
                              │  • Welcome email                  │
                              └──────────────────────────────────┘
                                                  │
                                                  ▼
                              ┌──────────────────────────────────┐
                              │  → DASHBOARD (vuoto — nessuna    │
                              │    richiesta ancora)             │
                              │  → CTA: Create New Submission    │
                              └──────────────────────────────────┘

   CONTENT TOUCHPOINTS lungo il percorso:
   • SEO: "futures backtesting service" "backtest trading strategy futures"
   • Social: LinkedIn/X thread su ricerche pubblicate
   • Newsletter: Welcome email + invito a prima submission
   • Email transazionale: conferma signup + benvenuto
```

### 3.2 Lead → Client (Prima Submission)

```
  ┌────────────────────────────────────────────────────────────────────┐
  │                   TEST YOUR STRATEGY WIZARD (7 step)               │
  │                                                                    │
  │  Step 1 ──> Step 2 ──> Step 3 ──> Step 4 ──> Step 5 ──> Step 6 │
  │  Ident.    Time      Entry     Exit      Exec.     Attach.        │
  │    │        │          │         │         │         │            │
  │    ▼        ▼          ▼         ▼         ▼         ▼            │
  │  ┌───────────────────────────────────────────────────────────┐   │
  │  │              Step 7: Review & Submit                      │   │
  │  │  Summary card → [Submit] → loading state → confirm        │   │
  │  └───────────────────────────────────────────────────────────┘   │
  │                                                                    │
  └────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
  ┌────────────────────────────────────────────────────────────────────┐
  │  POST-SUBMISSION                                                   │
  │                                                                    │
  │  ┌─────────────────────────┐     ┌─────────────────────────────┐  │
  │  │  "Request Received"     │     │  EMAIL AL CLIENTE           │  │
  │  │  • Request ID           │────>│  Subject: "Your backtest    │  │
  │  │  • Next steps (4 punti) │     │  request has been received  │  │
  │  │  • Link to Dashboard    │     │  — [ID]"                    │  │
  │  │  • Status: "Inviata"    │     │  • Next steps              │  │
  │  └─────────────────────────┘     │  • Link dashboard           │  │
  │                                  └─────────────────────────────┘  │
  └────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
  ┌────────────────────────────────────────────────────────────────────┐
  │  BACKEND: Richiesta atterra in Admin Queue                        │
  │  • strategy_requests → status='inviata'                           │
  │  • Admin vede nel dashboard KPI                                   │
  │  • Notifica admin (via email o dashboard)                         │
  └────────────────────────────────────────────────────────────────────┘
```

### 3.3 Client → Risultato (Ciclo di Vita Richiesta)

```
  ┌──────────┐
  │ INVIATA  │──────────────────────────────────────────────────────────┐
  └────┬─────┘                                                          │
       │                                                                 │
       ▼                                                                 │
  ┌────────────┐      ┌─────────────────┐                               │
  │INFO MANCANTI│<────│  Admin richiede  │                               │
  │             │     │  chiarimenti     │                               │
  │   [Cliente  │────>│  → Email al      │                               │
  │   risponde] │     │    cliente       │                               │
  └──────┬──────┘     └─────────────────┘                               │
         │                                                                │
         ▼                                                                │
  ┌──────────────┐                                                       │
  │IN VALUTAZIONE│────>  Admin esamina parametri, decide se accettare   │
  └──────┬───────┘                                                       │
         │                                                                │
         ├──────────────────────────────┐                                 │
         ▼                              ▼                                │
  ┌──────────┐                  ┌──────────┐                             │
  │ACCETTATA │                  │RIFIUTATA │                             │
  └────┬─────┘                  └──────────┘                             │
       │                          │                                      │
       ▼                          │                                      │
  ┌──────────────┐                │                                      │
  │IN LAVORAZIONE│                │  Email: "Richiesta rifiutata —      │
  └──────┬───────┘                │  motivazione"                       │
         │                         └──────────────────────────────────────┘
         ▼
  ┌───────────┐
  │COMPLETATA │
  └─────┬─────┘
        │
        ▼
  ┌────────────────────────────────────────────────────────────────────┐
  │  EMAIL AL CLIENTE: "Your request status has been updated:          │
  │  Completata" + link al report                                      │
  │                                                                    │
  │  CLIENTE → DASHBOARD → REQUEST DETAIL → Download risultato (PDF)  │
  │                                                                    │
  │  ADMIN: Mark as complete → upload result file → pubblica ricerca   │
  │  (se la strategia merita uno studio pubblico)                       │
  └────────────────────────────────────────────────────────────────────┘

   EMAIL NOTIFICHE per ogni cambio stato:
   • Inviata: conferma iniziale
   • Info mancanti: richiesta chiarimenti
   • In valutazione: "stiamo esaminando"
   • Accettata: "test iniziato"
   • Rifiutata: motivazione
   • Completata: link al risultato
```

### 3.4 Admin Workflow (Giornata Tipo)

```
  ┌─────────────────────────────────────────────────────────────────────┐
  │                         ADMIN DAILY                                 │
  │                                                                    │
  │  LOGIN → ADMIN DASHBOARD                                           │
  │    ├─ Vedi KPI: quante in attesa, in valutazione, completate       │
  │    ├─ Vedi ultime richieste                                        │
  │    │                                                               │
  │    ├─ ADMIN REQUESTS LIST                                          │
  │    │  ├─ Filtra per status "Inviata"                               │
  │    │  ├─ Apri dettaglio richiesta                                  │
  │    │  │   ├─ Leggi parametri strategia                             │
  │    │  │   ├─ Scarica allegati                                      │
  │    │  │   ├─ Aggiungi nota interna                                │
  │    │  │   ├─ Cambia status (dropdown + nota obbligatoria)         │
  │    │  │   │   └→ Email automatica al cliente                      │
  │    │  │   └─ [Richiedi chiarimenti] → email template al cliente   │
  │    │  └─ Richiesta completata → upload risultato                  │
  │    │                                                               │
  │    ├─ ADMIN RESEARCH MANAGER                                       │
  │    │  ├─ Crea nuova ricerca (bozza)                                │
  │    │  │   ├─ Compila titolo, slug, sezioni                         │
  │    │  │   ├─ Upload charts (da pipeline Python)                    │
  │    │  │   ├─ Allega PDF / dataset                                 │
  │    │  │   └─ [Salva bozza] / [Pubblica]                           │
  │    │  └─ Pubblica → attivazione newsletter                         │
  │    │                                                               │
  │    └─ ADMIN USERS (occasionale)                                    │
  │       └─ Vedi/Modifica utenti, disabilita se necessario            │
  │                                                                    │
  └─────────────────────────────────────────────────────────────────────┘
```

### 3.5 Ricerca → Newsletter → Distribuzione

```
  ┌──────────────────┐
  │  ADMIN pubblica  │
  │  nuova ricerca   │
  └────────┬─────────┘
           │
           ▼
  ┌────────────────────────────────────────────────────────────────────┐
  │  EVENTI A CASCATA                                                  │
  │                                                                    │
  │  1. Research.published = true, published_at = NOW()               │
  │  2. Research gallery si aggiorna (nuova card in cima)             │
  │  3. Home page "Latest Research" si aggiorna                        │
  │  4. Sitemap si aggiorna (lastmod)                                  │
  │                                                                    │
  │  5. ARQ Worker: Crea newsletter campaign "auto"                   │
  │     ├─ Carica tutti i subscriber is_active=true                    │
  │     ├─ Genera email: abstract + key metrics + link                 │
  │     ├─ Batch di 50 → Resend API                                   │
  │     ├─ Registra in newsletter_sends                                │
  │     └─ Notifica admin "Campagna completata: X inviate"            │
  │                                                                    │
  │  6. CONTENT REPURPOSING (manuale)                                  │
  │     ├─ LinkedIn: thread 3-5 post (ipotesi → dati → risultato)     │
  │     ├─ Twitter/X: 1 chart + 1 insight                             │
  │     ├─ Reddit r/algotrading: post con summary                     │
  │     └─ The Quant Newsletter / Quantocracy: submission             │
  │                                                                    │
  └────────────────────────────────────────────────────────────────────┘
```

---

## 4. Mappa delle Dipendenze

### 4.1 Matrice di Blocco (Cosa Dipende da Cosa)

```
FASE 0 — FONDAMENTA (Setup infrastruttura)
═══════════════════════════════════════════════════════════════
  PostgreSQL 16
    ↑
  FastAPI scaffold + config
    ↑
  Docker Compose (PostgreSQL + Redis + API)
    ↑
  Project structure (models/ + schemas/ + api/)
═══════════════════════════════════════════════════════════════

FASE 1 — AUTH (Niente funziona senza identità)
═══════════════════════════════════════════════════════════════
  Modello User + LoginHistory
    ↑
  Auth endpoints (signup, login, refresh, verify, reset)
    ↑
  JWT middleware + rate limiting (Redis)
    ↑
  ┌────┬────┬────┐
  │    │    │    │
  ▼    ▼    ▼    ▼
  Tutti gli altri moduli dipendono dall'auth
═══════════════════════════════════════════════════════════════

FASE 2 — CORE BUSINESS (Strategy Requests)
═══════════════════════════════════════════════════════════════
  Modello User (da Fase 1) ────┐
                               ├──> Modello StrategyRequest
  Modello StatusHistory ───────┘         ↑
                                         │
  Modello Attachment ────────────────────┘
                                         │
  Modello InternalNote ─────────────────┘
                                         │
                              ┌──────────┘
                              ▼
  Endpoint Strategy Requests (CRUD)
                              ↑
  Endpoint Admin (cambia stato, note, chiarimenti)
                              ↑
  Email transazionali (Resend)
                              ↑
  File upload validatore (estensione + MIME + size)
═══════════════════════════════════════════════════════════════

FASE 3 — RICERCA & NEWSLETTER
═══════════════════════════════════════════════════════════════
  ┌──────────────────────┐     ┌──────────────────────┐
  │  MODELLO RESEARCH    │     │  NEWSLETTER SYSTEM   │
  │  + chart + files     │     │                      │
  │         ↑            │     │  Dipende da:         │
  │  Dipende da:         │     │  • Resend API key    │
  │  • Admin auth        │     │  • Redis (ARQ)       │
  │  • File storage      │     │  • Modello User      │
  │  • Chart pipeline    │     │    (user_id FK opz.) │
  └──────────┬───────────┘     └──────────┬────────────┘
             │                            │
             ▼                            ▼
  ┌────────────────────────────────────────────────────┐
  │  INTEGRAZIONE:                                      │
  │  • Research.publish → trigger Newsletter campaign   │
  │  • Newsletter → Home teaser update                  │
  │  • Entrambe dipendono da: Email service (Resend)   │
  │  • Entrambe dipendono da: Admin role-gating         │
  └────────────────────────────────────────────────────┘

FASE 4 — FRONTEND INTEGRATION
═══════════════════════════════════════════════════════════
  Frontend framework (React / Next.js / Astro)
    ↑
  Dipende da: TUTTI gli endpoint API backend
    ↑
  Layout statici (Home, About, Method) → possono essere
  sviluppati in parallelo al backend (mock data)
    ↑
  Pagine dinamiche (Dashboard, Request Detail, Admin)
  → dipendono da API completate
    ↑
  Research page con grafici → dipende da chart pipeline
═══════════════════════════════════════════════════════════
```

### 4.2 Chain Critica (Percorso più Lungo)

```
Il cammino più lungo per il completamento MVP:

Setup DB ──> Auth ──> StrategyRequest CRUD ──> Admin endpoints
                         ↑                            │
                         └── File upload ──────────────┘
                                                            │
                                      ┌─────────────────────┘
                                      ▼
                            Research Model + API ──> Chart Pipeline
                                                            │
                                      ┌─────────────────────┘
                                      ▼
                            Newsletter System (se in MVP)
                                      │
                                      ▼
                            Frontend Integration + Deploy

BLOCCHERÀ identificate:
1. Chart pipeline Python (Midas) → blocca pubblicazione ricerche
2. Auth → blocca tutto il client area
3. Admin endpoints → bloccano ciclo vita richieste
4. Resend API key → blocca tutte le email (transazionali + newsletter)
5. Redis → blocca newsletter batch (ARQ) e rate limiting
```

### 4.3 Dipendenze Cross-Team

```
  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
  │   ATLAS (UX)    │     │  MIDAS (Data)   │     │  CRATOS (Backend)│
  │─────────────────│     │─────────────────│     │─────────────────│
  │ Fornisce:       │     │ Fornisce:       │     │ Fornisce:       │
  │ • Wireframe     │     │ • Metadata      │     │ • API endpoints │
  │ • User flows    │     │   schema        │     │ • DB schema     │
  │ • Page arch.    │     │   (ricerca.yml) │     │ • Auth system   │
  │ • Form wizard   │     │ • Chart specs   │     │ • File upload   │
  │ • Visual design │     │ • Chart pipeline│     │ • Email service │
  │                 │     │ • PDF generation│     │ • Admin panel   │
  └────────┬────────┘     └────────┬────────┘     └────────┬────────┘
           │                       │                       │
           ▼                       ▼                       ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │              AFRODITE (Content)                                   │
  │──────────────────────────────────────────────────────────────────│
  │ Fornisce: copy per ogni pagina, CTA strategy, brand voice,       │
  │           newsletter templates, SEO keyword clusters,             │
  │           content calendar, social distribution plan              │
  │                                                                  │
  │ Dipende da: atlas per layout definitivo (dove va la copy)       │
  │             cratos per email templates (Resend/react-email)      │
  │                                                                  │
  │ NON bloccata: copy può essere scritta in parallelo,              │
  │               integrata dopo il deploy frontend                  │
  └──────────────────────────────────────────────────────────────────┘
```

---

## 5. Stack Tecnologico Finale Unificato

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     STACK TECNOLOGICO — CAPO HORN LAB                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  BACKEND (Cratos)                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Framework │ FastAPI (Python 3.11+) — async nativo, Pydantic,        │   │
│  │           │ OpenAPI docs automatiche                                │   │
│  │ Database  │ PostgreSQL 16 — JSONB, array nativi, full-text search   │   │
│  │ ORM       │ SQLAlchemy 2.0 + Alembic (migrazioni dichiarative)     │   │
│  │ Auth      │ JWT (access 15min + refresh 7gg, rotation), httpOnly   │   │
│  │           │ cookies, bcrypt/argon2id                                │   │
│  │ Cache     │ Redis — rate limiting, ARQ task queue                   │   │
│  │ Queue     │ ARQ (Redis-backed) — newsletter batch, email async      │   │
│  │ Email     │ Resend API — transazionali + newsletter, react-email    │   │
│  │ Files     │ MVP: locale (D:\CapoHornLab\uploads\), Future: S3/R2   │   │
│  │ Security  │ CORS, Helmet headers, CSRF (SameSite + X-CSRF-Token),  │   │
│  │           │ rate limiting (slowapi), upload validator               │   │
│  │ Testing   │ pytest + httpx (integration tests)                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  FRONTEND                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Framework │ [DA DECIDERE — Ares] React / Next.js / Astro / puro     │   │
│  │ Stili     │ Tailwind CSS + palette custom Capo Horn                 │   │
│  │ Charts    │ Plotly.py → embed HTML interattivo + PNG fallback       │   │
│  │ Font      │ Inter (UI) / JetBrains Mono (numeri/metriche)           │   │
│  │ Search    │ Pagefind / Lunr (full-text ricerca senza backend)       │   │
│  │ PDF       │ WeasyPrint / Puppeteer (da HTML template a PDF)         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  DATA / RESEARCH (Midas)                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Analysis  │ Python 3.11, pandas/polars                              │   │
│  │ Data src  │ D:\marketdata\ (parquet — ES, NQ, CL tick data)         │   │
│  │           │ Databento MDP3 (feed istituzionale)                     │   │
│  │ Charts    │ Plotly.py → HTML statico interattivo + PNG export       │   │
│  │ PDF       │ ReportLab / WeasyPrint per report PDF                   │   │
│  │ Pipeline  │ Script Python CLI unificato (generate_research_charts)  │   │
│  │ Metadata  │ YAML frontmatter (ricerca.yml) → JSON index             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  INFRASTRUTTURA                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ MVP Host  │ [DA DECIDERE] Hetzner VPS / Railway / Fly.io / on-prem  │   │
│  │ Container │ Docker + docker-compose (PostgreSQL + Redis + API)      │   │
│  │ CDN       │ Future: Cloudflare R2 per file upload                   │   │
│  │ Monitor   │ Logging strutturato (Python logging)                    │   │
│  │ Deploy    │ Docker Compose → VPS / Railway                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  CONTENT / MARKETING (Afrodite)                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Newsletter │ Resend API (doppio opt-in, tracking pixel, templates)   │   │
│  │ Analytics  │ Resend (email open/click) + Google Analytics (site)     │   │
│  │ Social     │ LinkedIn, Twitter/X, Reddit (r/algotrading, r/quant)   │   │
│  │ SEO        │ JSON-LD (ResearchArticle, Organization), OG tags,      │   │
│  │            │ sitemap.xml, meta description con metrica chiave       │   │
│  │ Disclaimers│ Site-wide footer + ogni pagina ricerca                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  STRUMENTI COMUNI                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Git       │ Repository: progetti separati backend + frontend        │   │
│  │ CI/CD     │ [Future] GitHub Actions per test + deploy               │   │
│  │ Docs      │ OpenAPI (auto), README, DESIGN.md                       │   │
│  │ Design    │ Palette: #0F172A (navy), #F1F5F9 (text), #3B82F6 (acc.)│   │
│  │           │ #F59E0B (amber/data), #14B8A6 (teal/pos), #E11D48 (neg)│   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Schema MVP vs Future

### 6.1 MVP (Sprint 1-4) — IN SCOPE

```
  ✅ BACKEND MVP
     ├─ FastAPI scaffold + modelli DB (tutti)
     ├─ Auth: signup, login, refresh, verify email, reset password
     ├─ Strategy Requests: CRUD utente + upload allegati
     ├─ Admin: dashboard stats, lista richieste, cambio stato, note interne
     ├─ Email transazionali: conferma signup, richiesta ricevuta, cambio stato
     ├─ Ricerca: CRUD admin, API pubblica read-only
     ├─ Security: CORS, rate limiting, upload validation, Helmet headers
     └─ Docker Compose: PostgreSQL + API

  ✅ FRONTEND MVP
     ├─ Home, About, Method (statiche)
     ├─ Research: overview gallery + detail page (template con 7 grafici MVP)
     ├─ Login, Signup, Reset Password
     ├─ Test Your Strategy: wizard 7-step (autenticato)
     ├─ Dashboard utente
     ├─ Request Detail (read-only + status timeline)
     ├─ Admin Dashboard + Richiesta Detail + Note + Cambio Status
     └─ Contact form

  ✅ RICERCHE MVP
     ├─ Pubblicare Ricerca #1: "ES 1-Minute Quantitative Research Summary" 🔴
     ├─ Pubblicare Ricerca #2: "When Structure Meets Reality" 🔴
     ├─ 7 grafici standard MVP per ricerca
     └─ Template pagina dettaglio completo

  ✅ NEWSLETTER MVP
     ├─ Iscrizione doppio opt-in (subscribe, confirm, unsubscribe)
     ├─ Welcome email automatica
     ├─ Campagna manuale (admin crea e invia)
     └─ Notifica nuove ricerche via email

  ✅ CONTENT MVP
     ├─ Copy per tutte le pagine (Home, About, Method, Research, Contact)
     ├─ CTA strategy implementata
     ├─ Newsletter template email
     ├─ SEO base: meta description, OG tags, sitemap
     └─ Disclaimer legale (footer + research pages)
```

### 6.2 Stretch MVP (Sprint 4-6) — Se il tempo lo permette

```
  🔶 Grafici aggiuntivi: Monte Carlo, Parameter Stability, By Day/Hour
  🔶 PDF export ricerca (da HTML a PDF via WeasyPrint/Puppeteer)
  🔶 Ricerca full-text con Pagefind/Lunr
  🔶 2 contenuti metodo: "How We Backtest" + "Why We Publish Negative Results"
  🔶 LinkedIn presence setup + primi 3 post
  🔶 Research filter/sort funzionante
  🔶 Schema.org JSON-LD (ResearchArticle)
  🔶 File attachment admin (upload risultati PDF)
```

### 6.3 V1 (Post-MVP — Prossimi Mesi)

```
  🟢 METODO
     ├─ Pagina metodologia generale (/research/methodology/)
     ├─ Video esplicativi (screen recording della pipeline)
     └─ Calcolatore interattivo di metriche (Sharpe, DD)

  🟢 RICERCHE
     ├─ Galleria interattiva grafici (zoom, tooltip, export PNG)
     ├─ Scaricamento dataset parziali (parquet filtrato)
     ├─ GitHub pubblico con codice ricerca
     ├─ Repository Python: script di ricerca aperti
     └─ Blog separato (/blog/) per metodologia e critiche

  🟢 NEWSLETTER
     ├─ Programmazione campagne automatizzata (ARQ worker)
     ├─ Stats: aperture, click, bounce, unsubscribe
     └─ Segmentazione iscritti (per interesse, frequenza)

  🟢 ADMIN
     ├─ Research Manager completo (bozza/anteprima/pubblica)
     ├─ Users: CRUD completo, disabilita, audit log
     └─ Newsletter management dall'admin panel

  🟢 FRONTEND
     ├─ Pre-filled form per utenti di ritorno
     ├─ Notifiche in-app (badge dashboard)
     ├─ Dark mode / theme switching
     └─ Mobile responsive testing + fix

  🟢 INFRASTRUTTURA
     ├─ Deploy: Docker Compose → VPS / Railway
     ├─ CDN: Cloudflare R2 per file upload
     ├─ CI/CD: GitHub Actions (test + deploy)
     └─ Monitoring: error tracking (Sentry o simile)
```

### 6.4 V2 (Future — 6+ Mesi)

```
  🔵 FUNZIONALITÀ AVANZATE
     ├─ Backtest automatico (pipeline Python → marketdata D:\)
     ├─ Calendario editoriale newsletter (ARQ scheduling)
     ├─ OAuth social login (Google/GitHub)
     ├─ Admin: azioni bulk su richieste
     ├─ Notifiche push (email + in-app)
     ├─ Comments su ricerche con moderazione
     └─ Referral / word-of-mouth tracking (non programmatico)

  🔵 CONTENUTI AVANZATI
     ├─ 3+ ricerche nuove all'anno su NQ, CL, microstructure
     ├─ Data snapshots regolari (1 al mese)
     ├─ Guest post / collaborazioni con quant community
     ├─ Reddit r/algotrading presenza continuativa
     ├─ Newsletter "Capo Horn Lab Research Brief" matura
     ├─ Corso / guida scritta: "How to Backtest Properly"
     └─ Traduzione pagine statiche in italiano

  🔵 INFRASTRUTTURA AVANZATA
     ├─ Multi-tenancy (se richiesto)
     ├─ API pubblica per terze parti
     ├─ WebSocket per notifiche real-time
     ├─ Auto-generazione report PDF
     ├─ Multi-language (EN primario, IT secondario)
     └─ Community Discord/Slack (no trading advice)
```

### 6.5 HARD NO (Esplicitamente fuori scope — NON implementare)

```
  ❌ Backtest automatico (MVP manuale — Francesco esegue)
  ❌ Connessione a NinjaTrader / motori di trading / broker API
  ❌ Marketplace strategie (compravendita)
  ❌ Segnali live / alert / notifiche trading
  ❌ Chat interna tra utenti
  ❌ Auto-generazione report PDF (MVP manuale)
  ❌ OAuth social login in MVP
  ❌ WebSocket / real-time data
  ❌ API pubblica per terze parti (MVP)
  ❌ Vendita di strategie, indicatori, subscription
  ❌ Vendita di dati / dataset a pagamento
  ❌ Criptovalute (MVP solo futures ES/NQ/CL/6E)
  ❌ Strategie "guaranteed", "proven", "100% win rate" — qualsiasi contenuto
  ❌ Foto stock di trader sorridenti, lusso, auto, soldi
  ❌ Testimonial con importi in dollari
  ❌ Glow effects, gradienti, emoji nei bottoni CTA
```

### 6.6 Timeline Riassuntiva

```
Settimana 1     Settimana 2     Settimana 3     Settimana 4     Settimana 5-6
──────────────────────────────────────────────────────────────────────────────
FONDAMENTA      CORE BUSINESS   RESEARCH +       RIFINITURE      STRETCH MVP
                                NEWSLETTER
┌─────────┐    ┌─────────┐    ┌─────────┐     ┌─────────┐     ┌─────────┐
│FastAPI  │    │Requests │    │Research │     │Logging  │     │Charts+  │
│DB       │    │Upload   │    │Newsletter│    │Tests    │     │PDF      │
│Auth     │    │Admin    │    │ARQ      │     │Docker   │     │Search   │
│Security │    │Email    │    │Campaign │     │Deploy   │     │Method   │
│         │    │         │    │         │     │         │     │Content  │
│Home     │    │Wizard   │    │Research │     │Admin    │     │LinkedIn │
│About    │    │Dashboard│    │Detail   │     │Research │     │Filters  │
│Method   │    │Research │    │Charts   │     │Manager  │     │Schema   │
│Auth UI  │    │Gallery  │    │Opt-in   │     │Copy     │     │org      │
└─────────┘    └─────────┘    └─────────┘     └─────────┘     └─────────┘
                   │              │                │
                   ▼              ▼                ▼
               Ricerca #1    Ricerca #2       Newsletter
               pubblicata    pubblicata       operativa
```

---

## Appendice A: Glossario dei Ruoli

| Ruolo | Agente | Responsabilità chiave |
|-------|--------|----------------------|
| **Atlas** | Product/UX | Architettura sito, flussi utente, wizard submission, visual design |
| **Midas** | Data/Research | Ricerche, grafici, pipeline dati, template dettaglio, metadati |
| **Cratos** | Backend/Infra | API, database, auth, email, newsletter, security, deploy |
| **Afrodite** | Content/Marketing | Copy, brand voice, CTA, newsletter content, SEO, social |
| **Ares** | Frontend | Implementazione frontend, integrazione API, componenti UI |
| **Cupido / Odino** | Reviewers | Peer review ricerche, validazione metodologica |
| **Francesco** | Cliente/CEO | Decisioni finali, validazione strategica, execution backtest manuale |

## Appendice B: Decisioni Ancora Aperte

| # | Domanda | Opzioni | Propone | Da decidere |
|---|---------|---------|---------|-------------|
| 1 | Hosting MVP | Hetzner VPS / Railway / Fly.io / On-prem | Cratos | Francesco |
| 2 | Frontend framework | React / Next.js / Astro / HTML+JS | Ares | Ares + Francesco |
| 3 | Docker in MVP? | Sì (docker-compose) / No (solo venv) | ✅ Sì | — |
| 4 | Redis in MVP? | Sì (rate limit + newsletter) / No | ✅ Sì | — |
| 5 | Doppio opt-in newsletter? | Sì (GDPR) / No | ✅ Sì | — |
| 6 | PDF esistenti: codice sorgente? | Da rigenerare / OCR / solo PDF download | Midas | Da verificare |
| 7 | Grafici interattivi o statici? | Plotly HTML interattivo + PNG fallback | ✅ Misto | — |
| 8 | Multi-lingua? | Solo EN / EN+IT secondario | ✅ Solo EN MVP | Afrodite |
| 9 | Download dati pubblici? | Sì (parquet filtrato) / No | Midas | Francesco |
| 10 | Ricerche dietro email-wall? | No — tutte pubbliche | ✅ No | Afrodite |
| 11 | Comments su ricerche? | Disabilitato MVP, v2 con moderazione | ✅ Disabilitato | — |
| 12 | Social voice diverso da sito? | Leggermente più conversazionale su X | ✅ Sì | Afrodite |
| 13 | Blog separato o sotto research? | /blog/ per metodo, /research/ per studi | ✅ Separato | Atlas |
| 14 | OAuth in MVP? | No — solo email/password | ✅ No | Cratos |

---

> *Documento generato dalla sintesi di 4 proposte (Product, Research, Backend, Content). Ogni mappa riflette il consenso emerso dall'analisi incrociata, con le divergenze segnalate in Appendice B.*
>
> **Prossimo passo:** Validazione di Francesco + assegnazione sprint Fase 1.
