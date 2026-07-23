# CAPO HORN LAB — Piano d'Azione & Divisione Compiti

**Data:** 22 Luglio 2026
**Basato su:** Concept Map (67KB) + 4 Proposte Brainstorming

---

## Architettura Team

| Agente | Ruolo | Sprint |
|--------|-------|--------|
| **Cratos** | Backend Lead — DB, Auth, API, Admin, Newsletter | 1→4 |
| **Atlas** | Frontend Lead — Architecture, Pages, Wizard, UX | 1→4 |
| **Dioniso** | Visual Lead — Design System, UI, Grafici, Stile | 1→4 |
| **Midas** | Data Lead — Research Page, Charts, Pipeline | 3→4 |
| **Afrodite** | Content Lead — Copy, Newsletters, Brand Voice | 2→4 |
| **Ares** | Security Advisor — Audit, Secret Management | 1,4 |
| **Cupido** | Finance QA — Verifica contenuti finanziari | 3 |
| **Odino** | Research Support — Web references | 3 |
| **Camilla** | Coordinatrice — Supervisione, decisioni, QA | All |

---

## SPRINT 1 — Foundation
*Dipendenze: Nessuna — parte da zero*

### Task 1.1 — Progetto Scaffold
**Responsabile:** Cratos  
**Coinvolti:** Atlas, Dioniso  
**Output:** Struttura progetto, Docker Compose (PostgreSQL 16 + Redis + FastAPI), config
**File:** `docker-compose.yml`, `app/core/config.py`, `app/main.py`

### Task 1.2 — Design System e Tokens
**Responsabile:** Dioniso  
**Output:** Palette colori, typography, spacing, componenti base HTML/CSS
**Riferimento:** Palette da Atlas brainstorms (navy/off-white/blue/amber)

### Task 1.3 — Modello User + Auth
**Responsabile:** Cratos  
**Output:** Modello User + LoginHistory, endpoint signup/login/refresh/verify/reset, JWT dual-token, rate limiting Redis
**Dipende da:** Task 1.1
**Security:** Ares review

### Task 1.4 — Home Page Statics
**Responsabile:** Atlas  
**Coinvolti:** Dioniso (design)  
**Output:** Home page HTML/CSS responsiva con Hero, Trust Signals, How It Works
**Dipende da:** Task 1.2 (design tokens)

---

## SPRINT 2 — Core Business
*Dipende da: Sprint 1 (Auth)*

### Task 2.1 — Modelli StrategyRequest
**Responsabile:** Cratos  
**Output:** Modelli StrategyRequest, StatusHistory, Attachment, InternalNote + migrazioni
**Dipende da:** Auth (User model)

### Task 2.2 — API Strategy Requests + Admin
**Responsabile:** Cratos  
**Coinvolti:** Ares (security)  
**Output:** 30+ endpoint REST, admin cambio stato, note, chiarimenti, file upload validator

### Task 2.3 — Wizard "Test Your Strategy" (Frontend)
**Responsabile:** Atlas  
**Coinvolti:** Dioniso (UI)  
**Output:** Multi-step wizard 7 step con validazione, upload file, review & submit
**Dipende da:** Task 2.2 (API), Task 1.2 (design)

### Task 2.4 — Copy Pagine Core
**Responsabile:** Afrodite  
**Output:** Copy definitiva per Home, About, Method, Contact, Test Your Strategy, Auth pages

### Task 2.5 — About + Method + Contact Pages
**Responsabile:** Atlas  
**Output:** Pagine statiche responsive con copy da Afrodite
**Dipende da:** Task 2.4 (copy)

---

## SPRINT 3 — Research & Analytics
*Dipende da: Sprint 2 (Admin API)*

### Task 3.1 — Modello Research + Chart Pipeline
**Responsabile:** Midas  
**Coinvolti:** Cratos (API), Dioniso (visualizzazione)  
**Output:** Modelli Research, ResearchChart, ResearchFiles; pipeline Python Plotly.py per 7 grafici MVP
**Integrazione:** Ricerche ES esistenti da PDF

### Task 3.2 — Research Page (Frontend)
**Responsabile:** Atlas  
**Output:** Research Gallery (card filtrate) + Research Detail (sidebar stats, galleria grafici, download PDF)
**Dipende da:** Task 3.1, Task 2.4

### Task 3.3 — Admin Research Publication
**Responsabile:** Cratos  
**Output:** Admin può creare/pubblicare ricerche con upload grafici e PDF
**Dipende da:** Task 3.1

---

## SPRINT 4 — Newsletter & Final
*Dipende da: Sprint 2 (User model, Email)*

### Task 4.1 — Newsletter System
**Responsabile:** Cratos  
**Output:** Double opt-in, subscribe/unsubscribe, ARQ worker, template email Resend, metriche

### Task 4.2 — User Dashboard + Personal Area
**Responsabile:** Atlas  
**Output:** Dashboard utente con storico richieste, stato, download risultati
**Dipende da:** Sprint 2 (StrategyRequest API)

### Task 4.3 — Admin Panel Completo
**Responsabile:** Atlas + Cratos  
**Output:** Dashboard admin con stats, richieste, ricerche, newsletter

### Task 4.4 — Newsletter Content + Launch
**Responsabile:** Afrodite  
**Coinvolti:** Midas  
**Output:** Template email, welcome series, ricerca notification, content calendar 12 mesi

---

## SPRINT 5+ — Stretch
### Task 5.1 — Grafici Full (Monte Carlo, Parameter Stability, ecc.)
**Responsabile:** Midas  
### Task 5.2 — Pubblicazione Ricerche ES esistenti
**Responsabile:** Midas + Afrodite  
### Task 5.3 — Blog
**Responsabile:** Afrodite  

---

## Percorso Critico (Critical Path)

```
Setup (1.1) → Auth (1.3) → StrategyRequest (2.1+2.2) → Research (3.1) → Research Page (3.2)
                          ↘ Wizard (2.3) → User Dashboard (4.2)
                          ↘ Copy (2.4) → Pages (2.5)
                          ↘ Newsletter (4.1) → Content (4.4)
```

## Stima Tempi

| Sprint | Durata | Dipendenze esterne |
|--------|--------|-------------------|
| Sprint 1 | Foundation | Nessuna |
| Sprint 2 | Core | Auth completata |
| Sprint 3 | Research | Admin API completata |
| Sprint 4 | Final | Auth + StrategyRequest |

## Criteri di Accettazione MVP
- [ ] Utente può registrarsi, fare login, reset password
- [ ] Utente può inviare strategia con wizard 7-step + upload file
- [ ] Admin vede richieste, cambia stato, aggiunge note, richiede chiarimenti
- [ ] Email di conferma a ogni cambio stato
- [ ] Home, About, Method, Research, Test Your Strategy, Contact funzionanti
- [ ] Ricerche pubblicate con grafici (7 MVP)
- [ ] Newsletter con doppio opt-in
- [ ] User dashboard con storico richieste
- [ ] Admin panel completo
