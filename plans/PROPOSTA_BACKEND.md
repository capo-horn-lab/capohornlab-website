# PROPOSTA BACKEND — Capo Horn Lab

> **Autore:** Cratos (Backend/Infra Lead)  
> **Collaborazione:** Ares (Frontend)  
> **Stato:** Bozza — in attesa di review  
> **Data:** 22 Luglio 2026

---

## 1. TECH STACK — Scelte e Motivazioni

### Backend Framework
| Opzione | Voto | Perché |
|---------|------|--------|
| **FastAPI (Python 3.11+)** | ✅ **SCELTA** | Async nativo, Pydantic per validazione automatica, OpenAPI docs generati, performance eccellente. Team conosce Python (esistenti script di ricerca su D:). |
| Django REST | ⬜ | Troppo pesante per questo scope, admin già incluso ma meno flessibile. |
| Express/Fastify (Node) | ⬜ | Aggiunge complessità di toolchain (TS, bundler). Non necessario. |

### Database
| Opzione | Voto | Perché |
|---------|------|--------|
| **PostgreSQL 16** | ✅ **SCELTA** | JSONB per form flessibili, array nativi, full-text search, robusto con pgAdmin/DataGrip. |
| SQLite | ❌ | No concorrenza, no JSONB nativo, no pg_hba per sicurezza. |

### ORM / Data Layer
| Opzione | Voto | Perché |
|---------|------|--------|
| **SQLAlchemy 2.0 + Alembic** | ✅ **SCELTA** | Maturità, migrazioni dichiarative, supporto PostgreSQL completo, già noto al team. |
| Prisma | ❌ | Layer JS aggiuntivo, genera complessità cross-language. |

### File Storage
| Opzione | Voto | Perché |
|---------|------|--------|
| **Locale → S3 (crescita)** | ✅ **SCELTA** | Files su `D:\CapoHornLab\uploads\` in MVP, migrazione a S3/Cloudflare R2 quando serve. |

### Email / Newsletter
| Opzione | Voto | Perché |
|---------|------|--------|
| **Resend** | ✅ **SCELTA** | API moderna, deliverability alta, template React via react-email, 100 email/giorno gratis. |
| SendGrid | ⬜ | Affidabile ma API più datata. |
| Mailchimp API | ❌ | Overhead gestionale, pricing complesso. |

### Task Queue (per newsletter)
| Opzione | Voto | Perché |
|---------|------|--------|
| **ARQ (Redis-backed)** | ✅ **SCELTA** | Leggero, async, ottimo per code email. Redis già utile per cache + rate limiting. |
| Celery | ❌ | Troppo pesante per questo use case. |
| Huey | ⬜ | Valido ma meno diffuso di ARQ. |

### Auth
| Opzione | Voto | Perché |
|---------|------|--------|
| **JWT (access + refresh tokens)** | ✅ **SCELTA** | Stateless, httpOnly cookies, refresh rotation. Nessuna sessione server. |
| Session-based | ❌ | Stateful, scalabilità peggiore per pochi utenti ma comunque più complesso. |

---

## 2. DATABASE — Schema Models

### 2.1 Entity-Relationship (testuale)

```
User 1─N StrategyRequest
User 1─N NewsletterSubscription
User 1─N LoginHistory
StrategyRequest 1─N Attachment
StrategyRequest 1─N StatusHistory
StrategyRequest 1─N InternalNote  (solo admin)
Research 1─N ResearchChart
Research 1─N ResearchFile
Newsletter 1─N NewsletterAttachment
```

### 2.2 Models Dettagliati

#### `users`
```sql
CREATE TABLE users (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email           VARCHAR(255) NOT NULL UNIQUE,
  password_hash   VARCHAR(255) NOT NULL,
  full_name       VARCHAR(150) NOT NULL,
  company         VARCHAR(255),
  is_admin        BOOLEAN NOT NULL DEFAULT FALSE,
  is_active       BOOLEAN NOT NULL DEFAULT TRUE,
  email_verified  BOOLEAN NOT NULL DEFAULT FALSE,
  verification_token  VARCHAR(64),
  reset_token         VARCHAR(64),
  reset_token_expires TIMESTAMPTZ,
  last_login         TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_reset_token ON users(reset_token);
```

#### `strategy_requests` — il cuore del sistema
```sql
CREATE TABLE strategy_requests (
  id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id             UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  status              VARCHAR(30) NOT NULL DEFAULT 'inviata'
                      CHECK (status IN (
                        'inviata', 'info_mancanti', 'in_valutazione',
                        'accettata', 'in_lavorazione', 'completata', 'rifiutata'
                      )),
  strategy_name       VARCHAR(255) NOT NULL,
  description         TEXT,
  instrument          VARCHAR(50) NOT NULL,  -- 'NQ', 'ES', 'CL', '6E', altri
  timeframe           VARCHAR(30),
  historical_period   VARCHAR(100),
  entry_rules         TEXT,
  exit_rules          TEXT,
  stop_loss           VARCHAR(100),
  take_profit         VARCHAR(100),
  trailing_stop       VARCHAR(100),
  break_even          VARCHAR(100),
  session_times       VARCHAR(200),
  contracts           INTEGER,
  commission_slippage TEXT,
  indicators_params   JSONB,
  screenshots_notes   TEXT,
  additional_notes    TEXT,
  admin_notes         TEXT,                  -- note interne admin
  clarification_request TEXT,               -- richiesta info aggiuntive al cliente
  submitted_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  evaluated_at        TIMESTAMPTZ,
  completed_at        TIMESTAMPTZ,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_sr_user_id ON strategy_requests(user_id);
CREATE INDEX idx_sr_status ON strategy_requests(status);
CREATE INDEX idx_sr_submitted ON strategy_requests(submitted_at DESC);
```

#### `status_history` — audit trail cambi di stato
```sql
CREATE TABLE status_history (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  request_id      UUID NOT NULL REFERENCES strategy_requests(id) ON DELETE CASCADE,
  from_status     VARCHAR(30),
  to_status       VARCHAR(30) NOT NULL,
  changed_by      UUID REFERENCES users(id),       -- NULL = sistema
  note            TEXT,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_sh_request ON status_history(request_id);
```

#### `attachments`
```sql
CREATE TABLE attachments (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  request_id      UUID NOT NULL REFERENCES strategy_requests(id) ON DELETE CASCADE,
  file_name       VARCHAR(255) NOT NULL,
  file_path       VARCHAR(500) NOT NULL,       -- percorso su disco / S3 key
  file_size       BIGINT NOT NULL,
  mime_type       VARCHAR(100) NOT NULL,
  uploaded_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_att_request ON attachments(request_id);
```

#### `internal_notes`
```sql
CREATE TABLE internal_notes (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  request_id      UUID NOT NULL REFERENCES strategy_requests(id) ON DELETE CASCADE,
  author_id       UUID NOT NULL REFERENCES users(id),
  content         TEXT NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_in_request ON internal_notes(request_id);
```

#### `research` — pubblicazioni
```sql
CREATE TABLE research (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title           VARCHAR(255) NOT NULL,
  slug            VARCHAR(255) NOT NULL UNIQUE,
  abstract        TEXT,
  objective       TEXT,
  hypothesis      TEXT,
  instrument      VARCHAR(50),
  period          VARCHAR(100),
  methodology     TEXT,
  data_sources    TEXT,
  results_summary TEXT,
  interpretation  TEXT,
  limitations     TEXT,
  conclusions     TEXT,
  published       BOOLEAN NOT NULL DEFAULT FALSE,
  published_at    TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE research_charts (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  research_id     UUID NOT NULL REFERENCES research(id) ON DELETE CASCADE,
  chart_type      VARCHAR(50) NOT NULL,   -- equity_curve, drawdown, sharpe, etc.
  file_path       VARCHAR(500) NOT NULL,
  caption         TEXT,
  sort_order      INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE research_files (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  research_id     UUID NOT NULL REFERENCES research(id) ON DELETE CASCADE,
  file_name       VARCHAR(255) NOT NULL,
  file_path       VARCHAR(500) NOT NULL,
  mime_type       VARCHAR(100),
  file_size       BIGINT
);
```

#### `newsletter` — sistema di invio
```sql
CREATE TABLE newsletter_subscribers (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email           VARCHAR(255) NOT NULL UNIQUE,
  name            VARCHAR(150),
  user_id         UUID REFERENCES users(id) ON DELETE SET NULL,  -- opzionale
  subscribed_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  unsubscribed_at TIMESTAMPTZ,
  is_active       BOOLEAN NOT NULL DEFAULT TRUE,
  token           VARCHAR(64) NOT NULL UNIQUE   -- per unsubscribe one-click
);
CREATE INDEX idx_ns_email ON newsletter_subscribers(email);
CREATE INDEX idx_ns_token ON newsletter_subscribers(token);

CREATE TABLE newsletter_campaigns (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title           VARCHAR(255) NOT NULL,
  subject         VARCHAR(255) NOT NULL,
  preheader       VARCHAR(150),
  html_content    TEXT NOT NULL,
  plain_text      TEXT,
  status          VARCHAR(30) NOT NULL DEFAULT 'bozza'
                  CHECK (status IN ('bozza', 'in_coda', 'invio', 'completata', 'annullata')),
  sent_at         TIMESTAMPTZ,
  created_by      UUID REFERENCES users(id),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE newsletter_attachments (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  campaign_id     UUID NOT NULL REFERENCES newsletter_campaigns(id) ON DELETE CASCADE,
  file_name       VARCHAR(255) NOT NULL,
  file_path       VARCHAR(500) NOT NULL,
  mime_type       VARCHAR(100),
  file_size       BIGINT
);

CREATE TABLE newsletter_sends (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  campaign_id     UUID NOT NULL REFERENCES newsletter_campaigns(id) ON DELETE CASCADE,
  subscriber_id   UUID NOT NULL REFERENCES newsletter_subscribers(id) ON DELETE CASCADE,
  status          VARCHAR(30) NOT NULL DEFAULT 'in_coda'
                  CHECK (status IN ('in_coda', 'inviata', 'aperta', 'cliccata', 'bounce', 'unsubscribed')),
  sent_at         TIMESTAMPTZ,
  opened_at       TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(campaign_id, subscriber_id)
);
```

#### `login_history` — sicurezza
```sql
CREATE TABLE login_history (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  ip_address      INET,
  user_agent      TEXT,
  success         BOOLEAN NOT NULL,
  failure_reason  VARCHAR(100),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_lh_user ON login_history(user_id);
CREATE INDEX idx_lh_time ON login_history(created_at DESC);
```

---

## 3. API ENDPOINTS — REST Design

### 3.1 Auth (`/api/v1/auth`)

| Metodo | Endpoint | Descrizione | Auth |
|--------|----------|-------------|------|
| POST | `/auth/signup` | Registrazione utente | ❌ |
| POST | `/auth/login` | Login → set httpOnly cookie | ❌ |
| POST | `/auth/logout` | Logout + clear cookie | ✅ |
| POST | `/auth/refresh` | Refresh token rotation | ✅ |
| POST | `/auth/forgot-password` | Invia email reset | ❌ |
| POST | `/auth/reset-password` | Reset con token | ❌ (token valido) |
| GET | `/auth/verify-email/:token` | Verifica email | ❌ |
| GET | `/auth/me` | Profilo utente corrente | ✅ |

### 3.2 Strategy Requests (`/api/v1/requests`)

| Metodo | Endpoint | Descrizione | Auth |
|--------|----------|-------------|------|
| POST | `/requests` | Crea nuova richiesta | ✅ |
| GET | `/requests` | Lista richieste (utente: proprie; admin: tutte) | ✅ |
| GET | `/requests/:id` | Dettaglio richiesta | ✅ |
| PATCH | `/requests/:id` | Modifica richiesta (solo stato `inviata` / `info_mancanti`) | ✅ |
| DELETE | `/requests/:id` | Elimina (solo stato `inviata`) | ✅ |
| POST | `/requests/:id/attachments` | Upload allegato | ✅ |
| DELETE | `/requests/:id/attachments/:attId` | Elimina allegato | ✅ |
| GET | `/requests/:id/status-history` | Cronologia stati | ✅ |

### 3.3 Admin (`/api/v1/admin`) — solo ruolo admin

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| GET | `/admin/dashboard` | Stats: totale richieste, per stato, nuovi utenti |
| GET | `/admin/requests` | Tutte le richieste con filtri e paginazione |
| GET | `/admin/requests/:id` | Dettaglio completo richiesta (admin view) |
| PATCH | `/admin/requests/:id/status` | Cambia stato + nota obbligatoria |
| POST | `/admin/requests/:id/notes` | Aggiunge nota interna |
| PATCH | `/admin/requests/:id/clarify` | Invia richiesta chiarimenti al cliente |
| GET | `/admin/users` | Lista utenti |
| PATCH | `/admin/users/:id` | Modifica utente (admin toggle, disabilita) |

### 3.4 Research (`/api/v1/research`)

| Metodo | Endpoint | Descrizione | Auth |
|--------|----------|-------------|------|
| GET | `/research` | Lista pubblicazioni (pubblicate) | ❌ |
| GET | `/research/:slug` | Dettaglio pubblicazione | ❌ |
| POST | `/research` | Crea (admin) | ✅ admin |
| PATCH | `/research/:id` | Modifica (admin) | ✅ admin |
| DELETE | `/research/:id` | Elimina (admin) | ✅ admin |
| POST | `/research/:id/charts` | Upload chart (admin) | ✅ admin |
| POST | `/research/:id/files` | Upload file (admin) | ✅ admin |

### 3.5 Newsletter (`/api/v1/newsletter`)

| Metodo | Endpoint | Descrizione | Auth |
|--------|----------|-------------|------|
| POST | `/newsletter/subscribe` | Iscrizione (doppia opt-in via email) | ❌ |
| GET | `/newsletter/unsubscribe/:token` | One-click unsubscribe | ❌ |
| GET | `/newsletter/subscribers` | Lista iscritti (admin) | ✅ admin |
| DELETE | `/newsletter/subscribers/:id` | Rimuovi iscritto (admin) | ✅ admin |
| POST | `/newsletter/campaigns` | Crea campagna (admin) | ✅ admin |
| GET | `/newsletter/campaigns` | Lista campagne (admin) | ✅ admin |
| POST | `/newsletter/campaigns/:id/send` | Invia campagna (admin, via task queue) | ✅ admin |
| GET | `/newsletter/campaigns/:id/stats` | Stats apertura/click (admin) | ✅ admin |

### 3.6 Files

| Metodo | Endpoint | Descrizione | Auth |
|--------|----------|-------------|------|
| GET | `/files/:fileId` | Download allegato (richiesta: proprietario o admin) | ✅ |
| GET | `/files/research/:fileId` | Download file ricerca | ❌ (pubblico) |

### 3.7 Health

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| GET | `/health` | Health check pubblico |
| GET | `/health/ready` | Readiness (DB, Redis, storage) |

---

## 4. SICUREZZA — Architettura Difensiva

### 4.1 Autenticazione

```
┌─────────┐        POST /auth/login         ┌──────────┐
│ Cliente │ ──────────────────────────────>  │ FastAPI  │
│ Browser │ <──────────────────────────────  │          │
└─────────┘   Set-Cookie: access_token=jwt   └──────────┘
                    refresh_token=jwt
```

**Schema token:**
- **Access Token** — JWT, 15 minuti, firmato HS256, contiene `{sub, email, is_admin, iat, exp}`
- **Refresh Token** — JWT, 7 giorni, firmato con chiave diversa, rotazione su ogni uso (vecchio invalidato)
- **Cookie** — `HttpOnly`, `Secure`, `SameSite=Strict`, `Path=/api`

### 4.2 Rate Limiting (Redis + slowapi / middleware)

| Endpoint | Limite | Penalità |
|----------|--------|----------|
| `/auth/login` | 5 tentativi / 15 min per IP | Blocco 15 min |
| `/auth/signup` | 3 / ora per IP | Blocco 1 ora |
| `/auth/forgot-password` | 2 / ora per email | |
| `/auth/reset-password` | 3 / ora per IP | |
| `/newsletter/subscribe` | 5 / ora per IP | |
| API generica | 100 / min per utente | 429 Too Many Requests |

### 4.3 Upload File — Validazione Rigorosa

```
[Client] → POST /requests/:id/attachments
                    │
                    ▼
          1. Check estensione (.pdf, .png, .jpg, .jpeg, .gif, .zip, .py, .ipynb, .txt, .csv, .xlsx)
          2. Check MIME type reale (non fidarti del Content-Type inviato)
          3. Limite dimensione: 20 MB per file, 50 MB totali per richiesta
          4. Scansione antivirus (ClamAV opzionale in MVP)
          5. Salva su disco con nome UUID: {uuid}_{original_name}
          6. Registra record in attachments table
          7. Restituisce attachment_id
```

**Bloccati esplicitamente:** `.exe`, `.bat`, `.cmd`, `.sh`, `.ps1`, `.vbs`, `.scr`, `.dll`, `.msi`, `.jar`, `.wsf`, `.hta`, `.cpl`, `.msc`, `.reg`, `.docm`, `.xlsm`, `.pptm`, `.wasm`, `.php`, `.asp`, `.jsp`, `.htaccess`, `.env`, `.config`.

### 4.4 Protezioni Generali

| Misura | Implementazione |
|--------|-----------------|
| **CSRF** | Cookie `SameSite=Strict` + custom header `X-CSRF-Token` su mutazioni |
| **CORS** | Solo origin del frontend (configurabile) |
| **SQL Injection** | ORM (SQLAlchemy parametrizzato) — zero query raw |
| **XSS** | Output sanificato lato template; mai renderizzare HTML crudo dall'input |
| **Helmet headers** | `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Strict-Transport-Security` |
| **Password** | bcrypt (cost=12) o argon2id |
| **UUID v4** per ID | Nessun ID sequenziale esposto |
| **Logging** | Tutti i cambi di stato, login falliti, accessi anomali |
| **Input validation** | Pydantic models — validazione automatica su ogni endpoint |

### 4.5 Architettura di Rete (MVP → Produzione)

```
[MVP]
Browser ──HTTPS──> FastAPI ──> PostgreSQL
                        └──> Redis (opzionale MVP)
                        └──> File System (D:\CapoHornLab\uploads\)

[Produzione]
Cloudflare ──> Nginx ──> FastAPI (Docker) ──> PostgreSQL (RDS)
                         ├──> Redis (ElastiCache)
                         ├──> S3 / R2 (file)
                         └──> Resend API (email)
```

---

## 5. ADMIN PANEL — Schema Funzionale

### 5.1 Dashboard Principale

```
┌──────────────────────────────────────────────────────────┐
│  Capo Horn Lab Admin                       [Ciao, Admin]│
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌───────┐ │
│  │ Inviate │ │ Info   │ │ In     │ │ Accet- │ │ Comple-│ │
│  │   12    │ │ Manc.  │ │ Valut. │ │ tate   │ │ tate   │ │
│  │         │ │    3   │ │    5   │ │    8   │ │    7   │ │
│  └────────┘ └────────┘ └────────┘ └────────┘ └───────┘ │
│                                                          │
│  Ultime richieste (tabella):                            │
│  Data │ Nome │ Status │ Azioni                          │
│  ...                                                     │
│                                                          │
│  [x] Nuove registrazioni oggi: 2                        │
│  [x] Newsletter iscritti: 147                           │
│  [x] Ultimo accesso admin: 10:32 AM                     │
└──────────────────────────────────────────────────────────┘
```

### 5.2 Dettaglio Richiesta (Admin View)

```
┌──────────────────────────────────────────────────────────┐
│  Richiesta #a3f2...  ←  Torna alla lista                │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Status: [ In Valutazione ▼ ]  [Salva]                  │
│  ─────────────────────────────────────────               │
│                                                          │
│  Cliente: Marco Rossi (marco@email.com)                  │
│  Inviata: 20/07/2026                                    │
│                                                          │
│  ┌─ STRATEGIA ─────────────────────────────────────┐    │
│  │ Nome:       ES Breakout V3                       │    │
│  │ Strumento:  ES                                   │    │
│  │ Timeframe:  5 min                                │    │
│  │ Periodo:    Jan 2023 - Jun 2026                   │    │
│  │ Entrata:    ...                                  │    │
│  │ Uscita:     ...                                  │    │
│  └──────────────────────────────────────────────────┘    │
│                                                          │
│  ┌─ ALLEGATI ───────────────────────────────────────┐   │
│  │ [📄] strat_breakout_v3.pdf     2.3 MB  [Scarica] │   │
│  │ [🖼] screenshot_entry.png       1.1 MB  [Scarica] │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  ┌─ NOTE INTERNE ───────────────────────────────────┐   │
│  │ [Admin] Strategia interessante. Da verificare il   │   │
│  │ trailing stop.                                     │   │
│  │ [Aggiungi nota...]                    [Invia]      │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  [Richiedi chiarimenti al cliente]                       │
│  ┌─ Richiesta: ─────────────────────────────────────┐   │
│  │ Specificare lo slippage assunto e...       │         │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  ┌─ CRONOLOGIA STATI ───────────────────────────────┐   │
│  │ 20/07 14:32  inviata → in_valutazione  (Admin)   │   │
│  │ 20/07 10:15  —       → inviata          (Sistema) │   │
│  └──────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

### 5.3 Ricerca & Filtri

| Filtro | Tipo |
|--------|------|
| Status | Multi-select checkbox |
| Data range | Date picker (da / a) |
| Cliente | Search by name/email |
| Parola chiave | Full-text search su nome strategia e descrizione |

### 5.4 Gestione Ricerche (Admin)

```
┌─ NUOVA RICERCA ────────────────────────────────────┐
│ Titolo:    [When Structure Meets Reality]           │
│ Slug:      [when-structure-meets-reality]           │
│ Strumento: [ES ▼]  Periodo: [2018-2025]            │
│                                                      │
│ Abstract: [Testo...]                                │
│ Obiettivo: [Testo...]                               │
│ ...                                                  │
│ Charts:  [+] Aggiungi chart                          │
│ Files:   [+] Allega PDF/dataset                     │
│                                                      │
│ [Salva bozza]  [Pubblica]  [Anteprima]              │
└──────────────────────────────────────────────────────┘
```

---

## 6. NEWSLETTER SYSTEM — Architettura

### 6.1 Flusso Iscrizione

```
┌─────────┐                   ┌──────────┐              ┌────────┐
│ Browser │ POST /subscribe   │ FastAPI  │  Email       │ Resend │
│  Form   │ ───────────────>  │          │ ──────────>  │  API   │
│ "Email" │                   │          │              │        │
└─────────┘                   │ 1. Validate email       │        │
                              │ 2. Check existing       │        │
                              │ 3. Genera token         │        │
                              │ 4. Salva (is_active=F)  │        │
                              │ 5. Invia conferma       │        │
                              └──────────┘              └────────┘
                                        │
                                        ▼
                              ┌──────────────────┐
                              │ Email: "Conferma  │
                              │ iscrizione"       │
                              │ [Conferma Iscrizione]
                              └──────────────────┘
                                        │
                              (click sul link)
                                        ▼
                              ┌──────────┐
                              │ FastAPI  │  GET /newsletter/confirm/:token
                              │ 6. Attiva subscriber (is_active=T)
                              │ 7. Email: "Benvenuto!"
                              └──────────┘
```

### 6.2 Flusso Invio Campagna

```
Admin crea campagna (bozza)
        │
        ▼
Admin clicca "Invia"
        │
        ▼
FastAPI → ARQ queue (Redis)
        │
        ▼
Worker ARQ:
  1. Prende campagna
  2. Carica tutti i subscriber attivi
  3. Per ogni batch di 50:
     - Genera email personalizzata (o usa template unico)
     - Chiama Resend API (batch)
     - Salva record in newsletter_sends
  4. Al completamento → status = 'completata'
  5. Invia notifica admin
```

### 6.3 Metriche Newsletter

| Metrica | Fonte |
|---------|-------|
| Tasso apertura | Resend tracking pixel |
| Tasso click | Resend link tracking |
| Bounce | Resend webhook → aggiorna subscriber |
| Unsubscribe | Link `unsubscribe/:token` nel footer |

### 6.4 Email Transazionali (non newsletter)

| Tipo | Trigger | Servizio |
|------|---------|----------|
| Conferma registrazione | POST /auth/signup | Resend |
| Benvenuto | Email verificata | Resend |
| Password reset | POST /auth/forgot-password | Resend |
| Conferma richiesta | POST /requests | Resend |
| Cambio stato richiesta | PATCH admin status | Resend |
| Richiesta chiarimenti | POST admin clarify | Resend |
| Iscrizione newsletter | POST /subscribe | Resend (conferma opt-in) |
| Benvenuto newsletter | Conferma iscrizione | Resend |

---

## 7. STRUTTURA PROGETTO — File Tree

```
capohornlab-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app, middlewares, CORS
│   ├── config.py                # Pydantic Settings (env vars)
│   ├── database.py              # SQLAlchemy engine + session
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── strategy_request.py
│   │   ├── attachment.py
│   │   ├── status_history.py
│   │   ├── internal_note.py
│   │   ├── research.py
│   │   ├── newsletter.py
│   │   └── login_history.py
│   │
│   ├── schemas/                 # Pydantic request/response
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── strategy_request.py
│   │   ├── research.py
│   │   └── newsletter.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py              # Dependency injection (get_db, get_current_user)
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py        # Aggrega tutti i router
│   │   │   ├── auth.py
│   │   │   ├── requests.py
│   │   │   ├── admin.py
│   │   │   ├── research.py
│   │   │   ├── newsletter.py
│   │   │   └── files.py
│   │   └── health.py
│   │
│   ├── services/                # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── request_service.py
│   │   ├── file_service.py
│   │   ├── email_service.py
│   │   ├── newsletter_service.py
│   │   └── research_service.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py          # JWT, hashing, tokens
│   │   ├── rate_limit.py        # Rate limiter setup
│   │   └── upload_validator.py  # File type/size scanning
│   │
│   └── tasks/                   # ARQ background tasks
│       ├── __init__.py
│       ├── worker.py            # ARQ worker setup
│       └── newsletter_send.py   # Campagna invio
│
├── alembic/                     # Migrazioni database
│   ├── versions/
│   └── env.py
│
├── alembic.ini
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml           # PostgreSQL + Redis + API
├── .env.example
├── requirements.txt
└── README.md
```

---

## 8. IMPLEMENTAZIONE — Roadmap Suggerita

### Fase 1 — Fondamenta (Settimana 1)
- [x] Scaffold progetto FastAPI
- [x] Modelli SQLAlchemy + migrazione Alembic iniziale
- [x] Auth completo (signup, login, refresh, verify email, reset password)
- [x] Middleware sicurezza (CORS, Helmet, rate limiting)

### Fase 2 — Core Business (Settimana 2)
- [x] CRUD strategy requests (utente)
- [x] Upload allegati con validazione
- [x] Endpoint admin (dashboard stats, lista richieste, cambio stato)
- [x] Note interne e cronologia stati
- [x] Email transazionali (conferma richiesta, cambio stato)

### Fase 3 — Research & Newsletter (Settimana 3)
- [x] CRUD ricerche (admin)
- [x] Upload chart e file ricerca
- [x] API pubblica ricerche
- [x] Sistema newsletter (subscribe, confirm, unsubscribe)
- [x] Campagne email (ARQ worker)
- [x] Landing page subscribe nell'API

### Fase 4 — Rifiniture (Settimana 4)
- [x] Logging strutturato
- [x] Test integration (pytest + httpx)
- [x] Documentazione API (OpenAPI già automatica)
- [x] Docker Compose completo
- [x] Deploy MVP

---

## 9. OPEN QUESTIONS / DECISIONS

| Domanda | Opzioni | Decisione |
|---------|---------|-----------|
| Hosting | Hetzner VPS / Railway / Fly.io / On-prem D: server | ❌ DA DECIDERE |
| Docker in MVP? | Sì / No (solo venv) | Suggerito: Sì (docker-compose) |
| Redis in MVP? | Sì / No (senza newsletter batch) | Suggerito: Sì (rate limiting + cache) |
| Tracciamento apertura newsletter | Resend pixel / custom pixel | Resend è zero-implementazione |
| Doppio opt-in newsletter | Sì / No | Suggerito: Sì (legale GDPR) |
| CDN per file upload | Cloudflare R2 / S3 / Locale → migrare | MVP: locale, poi R2 |
| Frontend framework | React / Next.js / Astro / HTML+JS puro | Decisione di Ares |

---

## 10. HARD NO (fuori scope MVP)

- ❌ Backtest automatico (manuale — Francesco)
- ❌ Connessione a NinjaTrader / motori di trading
- ❌ Marketplace strategie
- ❌ Segnali live
- ❌ Chat interna
- ❌ Auto-generazione report PDF
- ❌ OAuth social login (Google/GitHub)
- ❌ WebSocket / real-time
- ❌ Multi-tenancy
- ❌ API pubblica per terze parti

---

*Fine proposta. Pronta per review con Francesco e Ares.*
