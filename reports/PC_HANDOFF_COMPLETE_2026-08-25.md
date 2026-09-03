# Capo Horn Lab — handoff completo per il nuovo PC

Data inventario: 2026-08-25
Origine: PC attuale di Francesco
Metodo: inventario filesystem, Git, contratti, servizi locali, endpoint pubblici e test reali. Non contiene segreti.

## 1. Stato esecutivo in una riga

Esiste una piattaforma Capo Horn Lab con sito pubblico, backend FastAPI, motore Python per backtest, artefatti di ricerca quantitativa e infrastruttura multi-agente locale. La base è concreta e testata in parte, ma non è ancora pronta a una migrazione/produzione “senza lavoro”: Git remoto e working branch sono divergenti, il database locale Docker non è avviabile oggi, Stripe non è configurato live, e il gateway Hermes ha un aggiornamento interrotto da sanare.

## 2. Percorsi principali da trasferire

- `D:\CapoHornLab\projects\capohornlab-website\` — prodotto principale: sito, backend, test, ricerca e report.
- `D:\CapoHornLab\marketdata\` e `D:\marketdata\` — dataset proprietari e sorgenti usate dagli studi (verificare dimensione/copia separatamente).
- `D:\CapoHornLab\agent-stack\` — workspace, launcher, servizi locali, repository specialistici, n8n.
- `D:\CapoHornLab\contracts\` — task/result envelope e log di verifica multi-agente.
- `D:\CapoHornLab\JarvisHistory\` — continuità e handoff condivisi.
- `D:\CapoHornLab\ui per camilla\` — dashboard desktop Camilla e backend locale.
- `D:\Models\Qwen3-14B\Qwen3-14B-Q4_K_M.gguf` — consulente locale Qwen3-14B.
- `D:\Hermes\profiles\` — profili Hermes. Contiene configurazioni e può contenere credenziali: trasferire con backup profilo cifrato/controllato, mai come archivio da condividere.

## 3. Sito Capo Horn Lab

### 3.1 Asset e superfici costruite

Repository: `D:\CapoHornLab\projects\capohornlab-website`

- 24 pagine HTML al top-level: home, research, method, pricing, test strategy, dettaglio research, login/signup/dashboard, checkout, contatto, investitori, documentazione, FAQ, amministrazione e pagine legali.
- Design system Observatory definitivo: ink `#070b12`, signal red `#E33B2F`, warm `#FF9B64`, font Playfair Display + DM Sans + DM Mono.
- Sidebar sinistra condivisa con navigazione Home / Research / Method / Enter the Lab / About / Pricing / Contact e login/signup.
- Sfondo orbitale fisso comune alle pagine pubbliche, logo CH corretto, design scuro migrato anche sulle pagine legali.
- Home semplificata a hero → thesis → systems → newsletter → footer.
- Sitemap, robots.txt, favicon, `.htaccess`, CSS/JS condivisi e cache-busting.
- CTA, FAQ, pagine legali e flusso di richiesta strategia presenti.

### 3.2 Stato live verificato oggi

- `https://www.capohornlab.com/` → HTTP 200.
- `https://www.capohornlab.com/login.html` → HTTP 200.
- `https://www.capohornlab.com/research.html` → HTTP 200.
- La login live contiene `account-client.js` e il marker anti-cache `no-store, no-cache`.
- Il dominio API Render risponde su `/api/v1/config` con HTTP 200.
- L’health endpoint provato come `/health` ha fatto timeout: non usarlo come prova di servizio sano senza ricontrollare la route di produzione configurata.

### 3.3 Branch e rischio di rilascio

Working branch corrente: `ui-experiment-v1`, pulito.

- `ui-experiment-v1` e `origin/ui-experiment-v1` contengono il lavoro più recente osservato: pagamenti, UX auth, Observatory, research UI.
- `main` locale è 14 commit dietro `origin/main`.
- `master` locale è 28 commit dietro `origin/master`.
- I 28 commit specifici di `ui-experiment-v1` non risultano contenuti in `main` dal controllo Git di oggi.

Conclusione: prima di cambiare PC o fare un deploy occorre fare una riconciliazione Git esplicita, con diff, test e una sola branch di rilascio. Non assumere che il sito live corrisponda alla branch corrente.

## 4. Backend e funzioni applicative

### 4.1 Backend realizzato

Stack Python/FastAPI in `app/`:

- autenticazione: signup, login, token, cambio password, storico login;
- contatti e newsletter;
- richieste di strategie e suggerimenti di research;
- pannello admin e note/stati interni;
- upload allegati;
- modelli per utente, richieste, newsletter, contatti, ordini e pagamenti;
- API pagamenti: setup carta, carte salvate, acquisto, storico acquisti, dashboard pagamenti;
- servizio email e struttura per Resend;
- rate limiter Redis con comportamento fail-open quando Redis non è disponibile;
- fallback SQLite portabile per sviluppo/ambiente senza PostgreSQL.

Migrazioni disponibili: `0001` utenti/login, `0002` richieste strategia, `0003` newsletter, `0004` contatti.

### 4.2 Verifiche eseguite

- Test suite: **56 passed in 11.96 s** oggi.
- Il registro storico documenta che signup live ha restituito 201, login reale 200 con token e credenziali errate 401; questa prova è storica, non ripetuta oggi per non creare account o alterare dati.
- API config live: chiavi `app_name`, `stripe_publishable_key`, `support_email`.
- `stripe_publishable_key` live è vuota: Stripe non è pronto per acquistare in produzione.

### 4.3 Limiti da non nascondere

- L’avvio/migrazione locale prova a collegarsi all’host PostgreSQL Docker `db`, che oggi non esiste perché Docker Desktop/daemon è spento. Il comando Alembic fallisce quindi con `could not translate host name "db"`.
- Il fallback SQLite è utile per continuità e test, non per il lancio con utenti reali: su Render l’archivio può essere effimero se non si configura Postgres gestito.
- Pagamenti: codice e interfacce esistono, ma chiave pubblica Stripe live assente; non sono verificati acquisti reali/webhook firmati.
- OAuth Google/GitHub è da verificare end-to-end: nella pagina ci sono i pulsanti, ma non c’è una prova attuale che siano configurati.
- Email transazionale: configurazione DNS/Resend era stata lavorata, ma va verificata nuovamente dopo migrazione senza copiare chiavi.

## 5. Motore di backtest e dati

### 5.1 Componenti creati

Cartella: `research/`.

- `backtest_engine.py`: motore Python per ES, NQ e CL.
- strategie incluse e visibili dalla CLI:
  1. `TSMomentum` — time-series momentum;
  2. `OpeningRangeBreakout`;
  3. `VWAPMeanReversion`;
  4. `IntradayMomentumSPY` adattata ai futures.
- `market_data_engine.py`: caricamento/adattamento dati.
- `chart_pipeline.py`: 7 grafici per run (equity, drawdown, distribuzione, heatmap, long/short, tabella, IS/OOS).
- `verification_engine.py` e `run_verification.py`: controllo/veridicità delle strategie.
- moduli per calendario news, studio NQ RTH e benchmark permutation.
- doppio modo `ottimale` vs `realistico`: costi, commissioni, slippage e fill parziali; la quantità di posizione è signed (long positivo, short negativo).

Entrambe le forme sono state verificate oggi:

```text
.venv/Scripts/python.exe research/backtest_engine.py --list
.venv/Scripts/python.exe -m research.backtest_engine --demo
```

È stato corretto il bootstrap degli import per supportare l’invocazione diretta documentata, e aggiunto un test di regressione.

### 5.2 Prova motore di oggi

Il demo a 30 barre ha eseguito le 4 strategie e prodotto statistiche/costi. È solo smoke test con dati demo, non una validazione di performance. La CLI ha enumerato correttamente tutte le 4 strategie.

### 5.3 Dati rinvenuti e usati

- ES: OHLCV 1 minuto 2020–2024.
- NQ: OHLCV 1 minuto 2023–2024; tick/trades storici e aggregati buy/sell menzionati nei report.
- CL: MBP-1 top-of-book 2024–2025, trasformabile in barre e filtri di spread/liquidità.
- GC/Gold: non confermato un dataset utilizzabile; non va dichiarato disponibile.

### 5.4 Run salvati: realistica, non materiale promozionale

Run locali con dati non sintetici e costi modellati:

| Run | Finestra | Risultato realistico | Lettura corretta |
|---|---|---|---|
| ES ORB | gennaio 2023 | 104 trade, PnL netto +$2,462.80, PF 1.12, Sharpe 0.087 | Finestra breve, non prova di edge. |
| ES TSMOM | gennaio 2023 | 5,090 trade, PnL netto −$107,917.90, PF 0.51 | Negativa, non promossa. |
| NQ intraday momentum | gennaio 2023 | 298 trade, PnL netto +$82,025.40, PF 4.75 | Finestra breve; annualizzazione assurda/non pubblicabile come previsione. |
| CL VWAP MR | gen–feb 2024 | 2,303 trade, PnL netto −$35,393.20, PF 0.65 | Negativa dopo costi; non promossa. |

Artefatti: `research/runs/<nome-run>/`, con barre, trade CSV, summary ottimale/realistico e grafici.

### 5.5 Ricerca quantitativa completata

- Studio riproducibile NQ RTH 2023–2024: 489 sessioni complete, ipotesi “primi 30 minuti predicono ultimi 30”. Risultato negativo: −1.528 bps/giorno lordo, 46.0% giorni positivi, correlazione −0.0244. IS 2023 e OOS 2024 entrambe negative.
- Corretto nel corso dello studio un errore metodologico: il gap overnight non è più incorporato impropriamente nel primo minuto RTH.
- Studi news long-horizon: NFP/CPI/FOMC, robustezza senza COVID/2020, split di regime e interazioni pre/post evento.
- Backlog di 10 candidate con paper, dati richiesti e protocolli: ES/NQ ORB, intraday momentum, demand imbalance, TSMOM, CL con filtri MBP-1, VWAP condizionale, microprice/order-book imbalance, stagionalità filtro, regime switch.
- I report dichiarano esplicitamente che i risultati negativi sono validi e non vendibili come edge.

Documenti chiave:

- `research/RESEARCH_METHODOLOGY.md`
- `research/STRATEGY_CANDIDATES_TOP10.md`
- `research/studies/nq_rth_2023_2024/REPORT.md`
- `research/studies/news_longhorizon/REPORT.md`
- `research/sources-evidence.md`
- `research/published_research.json`

## 6. Ricerca/web engine e pipeline di verifica

- Ricerca web svolta con fonti primarie/accademiche, citazioni persistite nei markdown e JSON.
- Paper e fonti includono Moskowitz/Ooi/Pedersen su TSMOM, Holmberg et al. su ORB, Gao et al. su intraday momentum, paper SSRN per ipotesi da replicare, NBER per stagionalità intraday.
- Il principio operativo è stato cambiato da “profitto” a “veridicità”: risultato negativo, costi realistici, split IS/OOS e limiti sono parte del prodotto.
- `responsible_web_scraper.py` e relativo test esistono nel repository.
- Per una nuova installazione non si trasferiscono automaticamente cookie, token, cache browser o chiavi; si reinstalla il browser research/agent in modo pulito.

## 7. Sistema multi-agente e infrastruttura locale

### 7.1 Architettura

- Profili Hermes: Camilla coordinatrice; Atlas sviluppo/deploy; Cratos QA; Midas dati/backtest; Afrodite advertising; Cupido ricerca finanziaria; Odino web research; Dioniso asset; Ares segreti isolati; Era trading in standby.
- Contratti task/result v1 in `D:\CapoHornLab\contracts\`: almeno 60 result envelope e relativi log osservati nell’inventario, dal 28 luglio al 24 agosto.
- n8n: template per intake, dispatch, result ingest, approval gate; servizio locale risponde oggi su porta 5678.
- Camofox risponde su 9377; Camilla UI backend su 4177; llama.cpp/Qwen su 8080; Ollama su 11434.
- Qwen3-14B GGUF esiste su D: e il suo endpoint locale ha restituito il modello atteso.
- Fincept Terminal e repository Fooocus presenti; Fooocus è on-demand per non impegnare la GPU.

### 7.2 Stato osservato oggi

- GPU: Quadro RTX 5000 Max-Q, 16 GB VRAM, 8.4 GB in uso al momento dell’inventario.
- n8n, Camofox, Camilla UI, llama.cpp e Ollama: HTTP 200 sui rispettivi endpoint locali.
- Docker Desktop daemon: non disponibile; nessun container verificabile.
- Era era avviato contro policy. È stato **fermato e verificato non in esecuzione**. Non è stato avviato nessun trading.
- Gateway Camilla, Midas, Odino e Dioniso risultavano attivi. Altri profili risultano spenti.
- Hermes è versione 0.20.5, ma segnala un aggiornamento interrotto: il recovery automatico non può sostituire `hermes.exe` mentre è in uso. Va chiuso Hermes e va completato il reinstall indicato dal tool prima della migrazione.

## 8. Dashboard Camilla

Percorso: `D:\CapoHornLab\ui per camilla\`.

- `backend.py`: API locali per health, sistema, performance, agenti, servizi, chat, God Mode, conversazioni e progetti.
- `index.html`: interfaccia a 5 tab: Chat, Performance, Agents, Conversations, Projects.
- `camilla-desktop.py`: wrapper pywebview.
- Il backend locale è raggiungibile oggi su `http://127.0.0.1:4177/api/health`.

## 9. Cosa manca prima del nuovo PC / produzione

Priorità alta:

1. Backup verificato: export Hermes per profilo, repository Git clone/remote verificato, dataset con checksum, contratti, JarvisHistory, Camilla UI, modelli locali. Non trasferire `.env` in chiaro o credenziali come file ordinari.
2. Riconciliazione Git: scegliere branch di rilascio e fondere `ui-experiment-v1` con `origin/main` dopo test e review.
3. Ripristino Docker: installare/avviare Docker Desktop o definire un ambiente senza Docker; far tornare operativi Postgres/Redis; applicare migrazioni con host corretto.
4. Database produzione gestito: configurare Postgres persistente e backup/restore prima di acquisire clienti reali.
5. Stripe: inserire le chiavi tramite secret manager/Render, configurare webhook firmato e fare test separato, mai una carta reale senza protocollo.
6. Resend/email: verificare dominio DNS, chiavi in secret manager e invio reale controllato.
7. OAuth: decidere se configurarlo davvero oppure rimuovere/indicare chiaramente i pulsanti segnaposto.
8. Completare la hardening del motore con run multi-annuali, cost model calibrato e test d’integrazione su dataset reali (la CLI diretta è ora coperta da test).
9. Riparare l’installazione Hermes interrotta prima di trattarla come baseline migrabile.
10. Nuovo QA live: login/signup controllato, richiesta strategia, newsletter, dashboard, ricerca, checkout in modalità test e link/CTA pagina per pagina.

Priorità ricerca:

11. ES ORB multi-annuale con protocollo congelato; NQ solo come replica OOS.
12. CL MBP-1 con fill bid/ask e filtri di liquidità.
13. Niente claim di performance dai piloti brevi; servono periodi separati, costi, regimi e robustezza.
14. Recuperare dataset GC solo se viene identificato un percorso/provenance reale.

## 10. Stato God Mode

La richiesta di autonomia è registrata dalla presenza di `.godmode_autonomy` nel repository. Si applica a lavoro reversibile e deploy interni del sito con verifica obbligatoria. Rimangono fuori: segreti, pagamenti, DNS/provider, ordini, cancellazioni e messaggi esterni. Era resta in standby.

## 11. Checklist operativa per il giorno del trasferimento

1. Congelare nuove modifiche e annotare l’ultima branch/commit deliberatamente scelti.
2. Fare backup e verificare almeno un restore test di un profilo Hermes e del repository.
3. Copiare i dataset con hash SHA-256 e confronto dimensioni/file count.
4. Trasferire Qwen GGUF e verificare `GET /v1/models` sul nuovo PC.
5. Reinstallare Hermes pulito, importare profili senza mostrare segreti, eseguire `hermes doctor`.
6. Portare su Docker/Postgres/Redis, testare migrazioni e 56 test.
7. Avviare servizi locali e verificare le cinque porte: 5678, 9377, 4177, 8080, 11434.
8. Configurare il nuovo PC come ambiente di staging; non puntare subito Aruba/Render senza smoke test.
9. Verificare sito live, backend live e branch di rilascio una volta sola, con un report di diff.
10. Mantenere Era fermo e Ares isolato.

## 12. Evidenze principali

- Test: `56 passed in 11.96s` (2026-08-25).
- Backtest smoke test: eseguito con successo come modulo Python; 4 strategie elencate.
- Endpoint pubblici: sito/root/login/research HTTP 200; API config Render HTTP 200.
- Servizi locali: n8n/Camofox/Camilla UI/llama.cpp/Ollama HTTP 200.
- Git: working tree pulito; divergence fra `ui-experiment-v1`, `main` e `master` rilevata e documentata.
- Safety: Era fermato, stato verificato come not running.

## 13. Inventario esteso dati e backup

### 13.1 Dataset proprietari

La directory dati principale effettiva è `D:\marketdata`, non `D:\CapoHornLab\marketdata`.

- `D:\marketdata`: **697 file, 33 GB**. È il dataset che richiede trasferimento con checksum e una copia indipendente.
- `D:\CapoHornLab\marketdata`: **2 file, 72 KB**; contiene `realtime_feed.py`, non lo storico di mercato.

Contenuto confermato in `D:\marketdata`:

- `ES/`: barre OHLCV 1 minuto annuali 2020, 2021, 2022, 2023, 2024; smoke test; due finestre di trade raw (ott–nov 2022 e gen–feb 2024).
- `NQ/1m/`: file annuali 2023 e 2024 più file mensili 2023–2024.
- `NQ/tick_trades_raw/`: file giornalieri raw, osservati almeno da 2023-01-01 in avanti; il report storico registra 593 file fino al 2024-08-15.
- `CL/mbp1/parquet/`: un file top-of-book MBP-1 per ciascun mese dal 2024-01 al 2025-12, più manifest e validazione.

Il trasferimento non deve deduplicare automaticamente i file annuali e mensili NQ: prima va chiarito se sono rappresentazioni sovrapposte volute o copie da normalizzare.

### 13.2 Backup già presenti

In `D:\CapoHornLab\agent-stack\backups` sono stati rilevati:

- archivi profilo Hermes per afrodite, archivist, ares, atlas, camilla, cratos, cupido, default, dioniso, era, midas e odino;
- `camilla-backup.zip` e `hermes.zip`;
- `capohornlab-website-clean.zip`;
- manifest e blueprint di luglio;
- una copia del sito e relativi database SQLite locali.

Questi file sono backup esistenti, non prove di restore: sul PC nuovo va testato almeno il ripristino di Camilla e del sito in una directory/profilo separato.

## 14. Inventario esteso prodotti e servizi

### 14.1 Repository specialistici installati

Sotto `D:\CapoHornLab\agent-stack\repositories\` sono presenti:

1. `advertising-skills` — base operativa Afrodite.
2. `camoufox` — browser research anti-bot/automazione Odino.
3. `fincept-terminal` — ricerca/terminal per Cupido.
4. `fooocus` — generazione immagini per Dioniso.
5. `hyperframes` — rendering video/composizioni.
6. `n8n` — automazione workflow.
7. `plausible-analytics` e `plausible-community-edition` — analytics self-hosted, non confermati in esecuzione.
8. `vibe-trading` — repository Era; deve restare inattivo.
9. `whisper` — pipeline speech-to-text locale.

### 14.2 Asset sito e marketing

Asset condivisi del sito già creati:

- `assets/css/sidebar.css`, `assets/js/sidebar.js`, `assets/js/orbit-background.js`;
- `assets/js/account-client.js`, `newsletter-client.js`, `stripe-buy.js`;
- logo wordmark e orbit mark SVG;
- funnel e copy per 5 campagne marketing;
- media: hero/social creatives HTML e storyboard video;
- manifest asset/design in `design/ASSET_MANIFEST.md` e brief Observatory.

### 14.3 Test disponibili nel repository

La suite attuale copre: auth/account wiring, contact flow, execution assumptions del backtest, market data engine/feed, calendario news, governance e robustezza degli studi news, controlli non operativi, dataset research detail, security guards e modalità dati della pagina di richiesta strategia.

## 15. Contratti multi-agente: stato reale

Nel filesystem risultano 62 result envelope. I loro stati non sono uniformi: 10 `completed`, 1 `complete`, 1 `pass`, 1 `warning`, 48 `failed`, 1 `fail`.

Questa è evidenza di sperimentazione e QA, non di 62 attività concluse. Per la migrazione vanno mantenuti tutti gli envelope e log, ma la dashboard futura deve distinguere chiaramente esiti riusciti, falliti e warning. Il parser di inventario ha trovato il campo destinatario solo in 6 result envelope; questo suggerisce che alcuni result legacy non rispettano pienamente lo schema corrente e devono essere normalizzati solo dopo conservarne l’originale.
