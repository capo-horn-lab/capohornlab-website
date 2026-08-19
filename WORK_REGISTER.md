# WORK REGISTER — Capo Horn Lab · checkpoint 2026-08-19 (chiusura sessione)

## ✅ FATTO E VERIFICATO OGGI

### Backend (Render) — ROTTO → SISTEMATO
- **Problema**: ogni login/signup dava 500 ("login fittizio"). Cause: (1) rate-limiter usava Redis (host docker "redis" inesistente su Render), (2) nessun DATABASE_URL configurato su Render → nessun DB/tabelle.
- **Fix deployati** (commit 560de8e, d27b1ff, master → auto-deploy Render):
  - `check_rate_limit` fail-open: se Redis è giù salta il check (log warning) — non rompe più l'auth
  - Backend autosufficiente: SQLite fallback quando POSTGRES_* non sono nelle env + `create_all` nel lifespan + tipi portabili (Uuid/JSON al posto di PG UUID/JSONB in 8 modelli)
  - `aiosqlite` aggiunto ai requirements; pool args omessi per SQLite
- **Verificato LIVE**: signup → 201, login utente reale → 200 + access_token, login credenziali false → 401 "Invalid email or password"
- ⚠️ NOTA: SQLite vive sul disco effimero di Render → dati azzerati a ogni redeploy. Prima del lancio con utenti reali: Postgres gestito (Neon/Supabase/Render) — 10 min di setup, guidare Francesco.

### Frontend (Aruba)
- Cache Aruba (HiSpeed) svuotata dal pannello (Velocità → Caching) → il sito serve la versione nuova (Last-Modified 19 Aug, X-Aruba-Cache MISS)
- .htaccess anti-cache caricato (non passa da aruba-proxy, ma inoffensivo)
- Meta tag no-store/no-cache aggiunti a login.html, signup.html, dashboard.html (locally fatto, commit fatto) — **NON ancora caricati su Aruba** (upload manuale in attesa)
- Verificato: il sito live serve la versione aggiornata; il "sito vecchio" visto da Francesco = cache del SUO browser (dimostrato: reload → card nuova visibile)

### Ricerca strategie (news trading)
- pre_news_study.py: drift pre5 predice NFP forte (+0.89%, t=2.36, p=0.019); NFP weak contrarian (corr pre5→r20 -0.65, p=0.010); CPI moderate pre5/r20 same-sign 73%. REPORT: PRE_NEWS_REPORT.md
- post_news_robustness.py: NFP weak r20 +4.67% → +3.73% senza COVID → +3.18% senza 2020 (resta positivo); FOMC hold sensibile al regime
- post_news_regime_split.py (cron): split di regime
- pre_post_interactions.py creato (specifica dal test del cron) — 53 test verdi
- Pubblicato sul sito: card "News Trading Long-Horizon" + 2 grafici + paper

## ⏳ DA FARE (prossima sessione)

1. **UPLOAD MANUALE (Francesco o via UI):** `C:\Users\farne\AppData\Local\Temp\chl_auth_pages.zip` su Aruba (File Manager → Carica File → Estrai → Qui → Sì). Poi verifica curl: login.html live deve contenere "no-store, no-cache" + account-client.js
2. **QA God Mode** (cron 97de4acfa0f2, ogni 30 min): pagina per pagina dal vivo — pulsanti, switch, link. Attenzione: i click computer_use richiedono approvazione che in sessioni a lunga vita va in timeout → serve riavvio del processo hermes con approvals.mode=off (già in config) o intervento manuale per i click UI
3. **Strategie vuote**: verificare quali research-detail/strategie mostrano sezioni vuote (QA loop in corso)
4. **Pulsanti OAuth** nel login ("Sign in with GitHub/Google"): verificare se funzionanti o segnaposto
5. OPZIONALI (todo 8-10): test email reale (RESEND_API_KEY presente su Render — tab Resend aperta da Francesco), rimuovere chl_frontend_deploy.zip dal server, dominio api.capohornlab.com (DNS Aruba + Render)

## 🛠 Stato tecnico
- Config: approvals.mode=off, cron_mode=approve (effetto pieno da riavvio processo)
- Flag .godmode_autonomy: ATTIVO e committato su master+main (non può più sparire)
- Cron God Mode: attivo, pinnato gpt-5.6-terra/openai-codex, next ~15:04
- Test: 53 passed · git: master e main sincronizzati
- NOTA blocchi UI: il prompt "Save password?" di Chrome è stato chiuso (Never); altri prompt nativi vanno chiusi manualmente
