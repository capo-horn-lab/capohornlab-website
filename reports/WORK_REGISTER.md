# WORK REGISTER — God Mode Deploy + QA cycle · 2026-08-23

## ✅ DEPLOY ARUBA COMPLETATO

- **369 file** uploadati via FTP su `/www.capohornlab.com/` — zero errori
- **Meta anti-cache**: no-store/no-cache/must-revalidate live su login, signup, dashboard
- **Redirect stub**: `/pages/index.html` e `/pages/documentation.html` → 200, redirect canonico
- **Cache**: X-Aruba-Cache: MISS (cache pulita da Francesco prima del deploy)
- **8 key pages**: tutte 200 (login, signup, dashboard, pricing, research, about, faq, documentation)
- **index.php** / **ver.php** Aruba → rinominati in backup
- **QA file sparsi** rimossi dalla root (22 file temporanei)
- **GitHub**: push su master + main sincronizzati

## Verifica live

| Risorsa | HTTP | Contenuto |
|---------|------|-----------|
| https://www.capohornlab.com/ | 200 | Home, X-Aruba-Cache: MISS |
| /login.html | 200 | no-store, no-cache, must-revalidate ✅ |
| /dashboard.html | 200 | no-store, no-cache, must-revalidate ✅ |
| /signup.html | 200 | no-store, no-cache, must-revalidate ✅ |
| /pages/index.html | 200 | redirect → ../index.html ✅ |
| /pages/documentation.html | 200 | redirect → ../documentation.html ✅ |

## QA ciclo 2026-08-24 — locale verificato

- **Test**: 56 passed (`./.venv/Scripts/python.exe -m pytest -q`).
- **Link interni**: audit di 116 pagine HTML → 0 riferimenti o anchor non risolti.
- **Autenticazione live**: login con utente inesistente ben formato → HTTP 401 `Invalid email or password`; nessun fallback client-side rilevato nel client account.
- **Home**: ripristinato il form newsletter con `assets/js/newsletter-client.js` e endpoint reale `/newsletter/subscribe` (nessun successo simulato).
- **Ricerca**: renderer pubblico ridotto da 16 a 14 studi completi. Le due entry senza chart asset/sezioni complete sono state tolte solo dalla visualizzazione pubblica, non cancellate: `quantum-computing-quant-finance`, `systematic-research-methodology`. I 14 studi pubblici ora hanno tutte le sezioni obbligatorie, metriche e PNG locali.
- **Pagine legacy**: tutti i 12 file `pages/*.html` verificati come redirect verso le versioni root canoniche; nessuna dashboard mock duplicata.
- **Evidenza completa**: `reports/godmode-qa-20260824.md`.

## ⏳ DA FARE / BLOCKER DI RELEASE

- **Deploy Aruba**: non eseguito in questo ciclo. Non è disponibile un helper di deploy privo di segreti nel tree tracciato; le correzioni sono quindi verificate localmente, non dichiarate live.
- **Backend**: migrare SQLite effimero → Postgres gestito (Neon/Supabase) prima di utenti reali.
- **Browser automation**: BrowserUse/CDP non disponibile in questo cron; Chrome esistente non è stato riusato perché conteneva navigazione personale.
- **Email reale**: contact/signup/newsletter non testati per non inviare email senza conferma esplicita.
- **Aruba cache**: dopo un futuro upload, verificare sempre con cache-buster e, se necessario, purge da PannelloAdmin → Velocità → Caching.

## QA ciclo 2026-08-24 — verifica diretta supplementare

- **Live, cache-buster**: 32 route canoniche/legacy HTTP 200; core 18/18 e tutte le 12 pagine in `pages/` rispondono. Evidenza: `reports/live-qa-20260824.json`.
- **Auth reale**: login utente inesistente → `401 Invalid email or password`; `GET /auth/me` con JWT fittizio → `401 Invalid or expired access token`; payload vuoti per signup/newsletter/contact → `422` senza invio. Il client usa esclusivamente `POST /auth/login`, `POST /auth/signup` e JWT in sessionStorage; nessun fallback mock rilevato.
- **Ricerca**: `node reports/research_detail_qa.js` PASS: 14 studi pubblici, 13 set dual-mode per strategie eseguibili, 1 event study con sei metriche sorgente e toggle costi nascosto (non inventa risultati Ottimale/Realistico). Tutti hanno 7 sezioni, grafici e nessun placeholder.
- **Test**: 56 passed + QA ricerca PASS.
- **Correzione locale**: `research-detail.html` nasconde il toggle Ottimale/Realistico per `news-longhorizon-es`, un event study non eseguibile; prima lo switch cambiava stato senza aggiornare le metriche.
- **Release gate**: correzione NON pubblicata. Nessun deploy helper senza segreti è presente nel repo e le credenziali non sono state lette/usate. Browser CDP non disponibile nel cron; quindi il click-through visuale non può essere attestato. Email reali non inviate, come richiesto.

## QA ciclo 2026-08-24 — 07:xx (ripetizione indipendente)

- **Pagine live**: 32/32 route root e `pages/` HTTP 200 con cache-buster; audit statico locale: 36 pagine pubbliche/legacy, nessun TODO, Lorem ipsum, anchor `href="#"`, title o viewport mancante. Gli anchor rimasti sono solo nel catalogo di componenti `design/design-tokens.html`, non pubblicato.
- **Account**: `POST /auth/login` con email valida non registrata restituisce `401 Invalid email or password`; payload vuoti di signup/newsletter/contact → `422`, senza invio. `assets/js/account-client.js` usa soltanto API backend e token JWT in `sessionStorage`; la dashboard fail-closed e `pages/dashboard.html` è redirect canonico.
- **Ricerca**: 14/14 studi locali completi e 13 set Ottimale/Realistico verificati; 13/14 PNG di primo grafico sono live 200. Il solo scarto è `news-longhorizon-es`: i due PNG esistono localmente (`research/charts/news-longhorizon-es/`) ma sono 404 live perché le modifiche locali non sono ancora state pubblicate.
- **Esecuzione**: 56 test passati; `node reports/research_detail_qa.js` PASS. BrowserUse non ha endpoint CDP nel cron, quindi i click-through visuali non sono attestabili senza una sessione browser isolata.
- **Deleghe**: due QA read-only (Cratos/Midas) non eseguite per errore provider `401`; envelope e log archiviati in `D:/CapoHornLab/contracts/`. Verifica ripetuta direttamente da Camilla.

### Gate corrente

🔴 Non dichiarare QA finale: il grafico `news-longhorizon-es` è localmente corretto ma non live; serve un deploy Aruba tramite canale con credenziali non esposte e verifica cache-buster. Restano inoltre non attestati i click visuali (browser cron indisponibile) e gli invii email reali, che richiedono conferma esplicita.

## QA ciclo 2026-08-24 — cron God Mode, verifica ripetuta

- **Backend live**: `GET /health` ha ripreso a rispondere `200 {"status":"ok","version":"1.0.0"}`. Login negativo con utente non registrato: `401 Invalid email or password`; quindi il backend non accetta credenziali arbitrarie.
- **Suite**: `56 passed in 2.56s`; `node reports/research_detail_qa.js` PASS: 14 studi pubblici, 13 set Ottimale/Realistico, zero sezioni/metriche/grafici locali mancanti.
- **Link locali**: 21 pagine canoniche, 632 riferimenti relativi verificati, `0` file mancanti e `0` link `href="#"` vuoti. Le occorrenze testuali di “placeholder” sono nel CSS/markup descrittivo, non link o contenuto di ricerca; il QA specifico ricerca risulta pulito.
- **Live gap confermato**: `research/charts/news-longhorizon-es/01_pre_news_directional.png` e `02_post_news_horizon.png` danno entrambi `404` con cache-buster. Gli asset sono presenti e validati localmente ma non ancora pubblicati.
- **Browser click-through**: non attestabile in questo runtime: Browser Use non ha endpoint CDP e il browser isolato richiede un PID. Non è stata riutilizzata una sessione personale.
- **Deleghe read-only**: contratti `chl-20260824-0015` e `chl-20260824-0016` archiviati; dispatcher ha restituito `401 Missing Authentication header` prima dell’avvio. Result envelope e verify log marcati failed; nessuna azione degli specialisti accettata.

### Gate aggiornato

🔴 QA completo non chiudibile in questo ciclo. L’unica correzione funzionale locale non pubblicata resta il renderer/asset del report `news-longhorizon-es`; senza un deploy Aruba che non richieda lettura di segreti non posso rendere live i due PNG né attestare zero 404. Gli invii email reali restano esclusi senza conferma esplicita. Nessuna modifica source aggiuntiva applicata in questo ciclo.

## QA ciclo 2026-08-24 — account/dashboard e intake

- **Auth live**: `GET /health` → 200; `POST /api/v1/auth/login` con indirizzo valido non registrato → `401 Invalid email or password`. Signup, newsletter e contact con payload vuoto → `422`; nessuna email inviata.
- **Corretto localmente — dashboard**: rimossa la falsa sottoscrizione newsletter lato browser, il falso portfolio “1 dataset / NQ 1-Min Tick” e il contatore iniziale “3”. Le metriche delle richieste vengono ora aggiornate soltanto dal payload JWT di `/requests`.
- **Corretto localmente — test strategy**: rimosso il codice sconto gestito in `localStorage` e l’ID richiesta fittizio `CH-2026-XXXX`; promozioni e ID richiesta sono dichiarati server-side/post-successo.
- **QA locale**: `56 passed`; `node reports/research_detail_qa.js` PASS (14 studi completi, 13 set Ottimale/Realistico); audit `reports/qa-current-cycle.json`: 39 pagine pubbliche/legacy, 857 riferimenti, 0 mancanti/dead anchor. I frammenti Plotly in `research/charts/` e `research/runs/` sono asset incorporati, non pagine pubbliche autonome.
- **Live**: 32 route canoniche/legacy già confermate 200; i due asset effettivamente referenziati di `news-longhorizon-es` (`01_car_events.png`, `02_mean_returns.png`) ora rispondono entrambi 200. Il precedente gate sui nomi `01_pre_news_directional.png` e `02_post_news_horizon.png` era un riferimento obsoleto nel registro, non un asset richiesto dal renderer.

### Gate corrente

🟡 Correzioni di questo ciclo verificate solo nel repo: non esiste nel tree un helper di deploy Aruba utilizzabile senza consultare credenziali. Il flag `.godmode_autonomy` è ON, ma non autorizza la lettura/esposizione di segreti. BrowserUse nel cron non ha endpoint CDP, quindi non posso attestare il click-through visuale di ogni controllo; nessuna sessione personale è stata riusata. Non pausare il cron: resta da pubblicare e verificare live il delta locale, poi completare la verifica browser isolata.

## QA ciclo 2026-08-24 — verifica live di chiusura parziale

- **Statico e ricerca locale**: `56 passed`; renderer ricerca PASS (`14` studi, `13` set Ottimale/Realistico); audit locale `39` pagine / `857` riferimenti / `0` mancanti.
- **Live, cache-buster**: `32/32` route pubbliche e legacy HTTP 200; i due asset effettivamente usati da `news-longhorizon-es` sono live: `01_car_events.png` 200 (143930 bytes), `02_mean_returns.png` 200 (37942 bytes).
- **Auth reale, senza invii**: login con utente non registrato → `401 Invalid email or password`; JWT inventato → `401`; payload vuoti di signup, newsletter e contact → `422`. Nessuna email o pagamento è stato generato.
- **Nuovo difetto live confermato**: `dashboard.html` pubblico serve ancora il portfolio fittizio `1 dataset` e il contatore fittizio `3`; i due marker risultano assenti solo nel delta locale. Quindi la dashboard live non è ancora verificabile come interamente basata sul payload JWT.
- **Click-through**: Browser Use non ha fornito un CDP endpoint. Il solo Chrome disponibile è una sessione personale su contenuto non correlato e non è stato usato; il browser isolato CUA richiede un PID, quindi non è stato possibile attestare click/switch visivi senza violare la separazione della sessione.
- **Deleghe**: task `chl-20260824-0017` (Cratos) e `chl-20260824-0018` (Midas) archiviati con result envelope `failed`: dispatcher `401 Missing Authentication header` prima di qualunque tool call; nessuna loro conclusione è stata accettata.

### Gate aggiornato

🔴 **Non pausare God Mode.** Occorre pubblicare il delta locale di `dashboard.html` e `test-strategy.html` con un deploy Aruba che non esponga segreti, poi ripetere la verifica live con cache-buster e una sessione browser isolata. Gli invii email reali restano esclusi senza conferma esplicita.

## QA ciclo 2026-08-24 — browser isolato + correzione accesso wizard

- **Browser isolato**: avviata una sessione Chrome driver-owned, senza riusare il browser personale. Home → `Test Your Strategy` verificato: navigazione corretta a `/test-strategy.html`, nessuna pagina bianca.
- **Difetto live confermato**: il bottone anonimo `Sign Up to Submit` apriva direttamente il wizard. Non produceva una richiesta senza JWT (il submit è protetto), ma era un bypass UX fuorviante verso un flusso riservato.
- **Corretto localmente**: `test-strategy.html` instrada ora esplicitamente i visitatori anonimi a `signup.html` / `login.html`; anche il deep-link `?auth=1` apre il wizard solo dopo `CHLAccount.requireSession()` (assenza JWT → redirect login). Eliminati variabile e commenti `demo/mock` residui. La dashboard mantiene il fail-closed JWT; il client account usa esclusivamente API backend.
- **Auth live negativa**: login con indirizzo valido non registrato → `401 Invalid email or password`; JWT inventato su `/auth/me` → `401`; payload vuoti per signup/contact/newsletter → `422`, senza invio email.
- **Regressione locale**: audit `39` pagine / `857` riferimenti / `0` mancanti; `56 passed`; renderer ricerca PASS: `14` studi completi, `13` set Ottimale/Realistico e chart asset validi.
- **Live**: 31 route canoniche/legacy cache-buster → HTTP 200.
- **Deleghe**: `chl-20260824-0019` e `chl-20260824-0020` archiviati failed: dispatcher `401 Missing Authentication header` prima dell'esecuzione; nessuna conclusione specialistica accettata.

### Gate corrente

🔴 **Non pausare God Mode.** La correzione `test-strategy.html` (insieme ai delta locali dashboard già registrati) non è ancora pubblicata su Aruba: nel repo non c'è un deploy helper utilizzabile senza leggere segreti. L'upload richiede il canale predisposto da Francesco; dopo serve verifica cache-buster. La verifica email reale resta esclusa senza conferma esplicita.

## QA ciclo 2026-08-24 — browser isolato, verifica diretta

- **Browser**: avviato Chromium isolato driver-owned (nessuna sessione personale riusata). Home, wizard, dashboard, login e research detail verificati con snapshot semantici.
- **Live HTTP**: 32 route canoniche/legacy e due chart `news-longhorizon-es` hanno restituito 200 con cache-buster.
- **Account**: dashboard anonima reindirizza correttamente a `login.html?next=dashboard.html`; login OAuth visibilmente disabilitato, non simulato. Il test negativo API precedente resta 401 per utente inesistente.
- **Difetto live confermato**: su `test-strategy.html`, il pulsante anonimo `Sign Up to Submit` apre ancora il wizard direttamente. Il fix fail-closed esiste localmente ma non è pubblicato; il flusso live resta UX non allineato, anche se il submit API è protetto.
- **Ricerca live**: una pagina dettaglio TSMOM renderizza tutte le 7 sezioni, 7 chart e i blocchi di regime. Tuttavia il testo presenta Sharpe storico 0.98 mentre il pannello iniziale Ottimale mostra Sharpe -0.08 / CAGR -45.9%. Contraddizione di metriche da risolvere con provenienza dati prima della release. Il toggle non è stato attestato: il controllo custom non espone un ref checkbox e i click a label/pixel non hanno alterato lo stato.
- **Locale**: 56 test passati; audit statico 39 pagine / 859 riferimenti / 0 mancanti; QA renderer: 14 studi e 13 set dual-mode, nessuna sezione/grafico/placeholder mancante.
- **Deploy**: non eseguito. Non ho letto né usato credenziali; non c'è un helper Aruba senza segreti nel repo. Nessuna email o pagamento è stato inviato.
- **Deleghe**: `chl-20260824-0021` e `chl-20260824-0022` archiviati failed: dispatcher 401 prima dell'esecuzione, nessun risultato specialistico accettato.

### Gate corrente

🔴 **Non pausare God Mode.** Prima di chiudere: (1) pubblicare il delta locale dashboard/test-strategy tramite canale Aruba sicuro, (2) allineare le metriche TSMOM al dataset/source-of-truth, (3) rieseguire click-through e cache-buster live.

## QA ciclo 2026-08-24 — audit di integrità dati (cron)

- **Live cache-buster**: 24 route core/canoniche/legacy (root, research detail TSMOM/news, account, legali e `pages/`) → tutte HTTP 200 con corpo non vuoto. Evidenza: `reports/live-core-current.json`.
- **Statico locale**: `reports/qa_current_cycle.py` PASS — 39 pagine, 859 riferimenti, 0 file/anchor mancanti. Suite backend: `56 passed in 3.07s`. Renderer: `node reports/research_detail_qa.js` PASS (14 studi, sezioni/chart reference popolate).
- **Account, senza invii**: JWT inventato su `/auth/me` → 401; payload vuoti signup/contact/newsletter → 422. Il client `assets/js/account-client.js` chiama solo `/auth/signup`, `/auth/login`, `/auth/me` e conserva solo il JWT ricevuto dal backend in `sessionStorage`; nessun fallback client-side. Retry con email sintatticamente valida non registrata: `401 Invalid email or password`; nessun accesso consentito.
- **Blocco qualità ricerca rilevato**: `time-series-momentum-futures` dichiara un backtest globale 1985–2025 / Sharpe 0.98, ma il toggle lo sovrascrive con un run ES locale di gennaio 2023 (`research/runs/es-tsmom-2023-01/summary_ottimale.json`: Sharpe -0.0808, CAGR -45.91%). `research-detail.html` lega questo studio al chart/run `local-es-tsmom-2023-01`. È una contraddizione materiale: non è corretto pubblicare né “allineare” inventando numeri. Congelata la release del renderer finché non esiste un run verificabile coerente con l’articolo o finché il toggle non viene rimosso per quello studio.
- **Browser**: BrowserUse non ha CDP; il browser isolato CUA non è avviabile senza un PID separato. Non è stata usata la finestra Chrome esistente, per non riutilizzare una sessione potenzialmente personale. Click-through non attestato in questo ciclo.
- **Deleghe read-only**: contratti `chl-20260824-0023` e `chl-20260824-0024` archiviati; dispatcher ha risposto 401 prima dell’avvio. Result envelope/log marcati failed; nessuna conclusione specialistica accettata.

### Gate corrente

🔴 **Non pubblicare e non pausare God Mode.** Il problema login fittizio è escluso dalle verifiche negative e dal codice; il blocco reale ora è l’integrità delle metriche TSMOM (run/chart locale incompatibile con testo globale). Restano da rieseguire click-through su browser veramente isolato e il deploy del delta già locale quando la ricerca è coerente. Nessuna email, pagamento, segreto o modifica provider effettuata.


## QA ciclo 2026-08-24 — integrità TSMOM corretta nel repo

- **Difetto confermato e corretto localmente**: il toggle Ottimale/Realistico di `time-series-momentum-futures` sostituiva impropriamente le metriche dell’articolo (portafoglio globale, 58 contratti, 1985–2025) con un pilot ES di gennaio 2023. Il renderer ora mantiene le metriche dual-mode dell’articolo; i sette chart restano disponibili ma sono etichettati esplicitamente come *ES implementation pilot — January 2023*. È aggiunta una disclosure di scope nella sezione Results. Nessun numero è stato inventato né cancellato.
- **Verifica locale**: `56 passed in 2.99s`; `node reports/research_detail_qa.js` PASS; `python reports/qa_current_cycle.py` PASS (39 pagine, 859 riferimenti, 0 mancanti/dead anchor).
- **Browser isolato**: il driver ha creato Chromium separato (`pid 52956`) e il binding esatto è riuscito. La navigazione tipizzata è stata però rifiutata dal driver con `browser_verification_required` anche dopo snapshot freschi; BrowserUse non ha endpoint CDP. Nessuna sessione Chrome personale è stata usata.
- **Deleghe QA read-only**: contratti `chl-20260824-0025` e `chl-20260824-0026` creati e verificati; entrambi respinti dal dispatcher con `401 Missing Authentication header` prima dell’avvio. Result envelope + verify log archiviati, nessun risultato specialista accettato.

### Gate aggiornato

🔴 **Non pubblicare e non pausare God Mode.** Il codice locale ora non presenta la contraddizione TSMOM, ma il delta non è pubblicato su Aruba e non è possibile attestare il click-through completo dal runtime corrente. Serve un deploy tramite canale Aruba sicuro, seguito da verifica live cache-buster e browser E2E isolato; gli invii email reali restano fuori scope senza conferma.

## QA ciclo 2026-08-24 — E2E API locale e controllo regressioni

- **Suite e struttura**: `.venv/Scripts/python.exe -m pytest -q` → `56 passed in 3.65s`; `python reports/qa_current_cycle.py` → 39 pagine, 859 riferimenti, 0 file/anchor mancanti; `node reports/research_detail_qa.js` → PASS (14 studi, 13 set dual-mode, chart reference popolate).
- **E2E API reale locale**: avviato Uvicorn su `127.0.0.1:8010`; `tests/run_local_api_e2e.py` ha creato un utente di test, effettuato login con password hash/JWT, letto `/auth/me`, creato una richiesta autenticata, caricato un allegato e riletto lista/dettaglio. Esito PASS; ID richiesta verificata: `c52611c1-3166-4edd-8066-ab238d7228cb`. Il recapito della verifica è rimasto `unavailable` (nessun invio email reale eseguito).
- **Account**: `app/api/v1/auth.py` usa DB async, `signup_user()` salva solo `hash_password(...)`, login verifica hash e firma access/refresh token; refresh token solo cookie HttpOnly. Il client dashboard usa `CHLAccount.requireSession()` e dati `/requests`; nessun fallback che ammetta credenziali arbitrarie è emerso dal codice o dai test.
- **Live cache-buster**: root, dashboard, wizard e dettaglio TSMOM rispondono 200/non vuoti. Il marker fittizio live dashboard (`1 dataset`) conferma però che la correzione locale non è ancora pubblicata.
- **Browser click-through**: BrowserUse ha nuovamente rifiutato entrambe le sessioni fresche per assenza endpoint CDP; CUA ha rifiutato il browser isolato perché richiede PID. Nessuna sessione personale è stata usata.

### Gate aggiornato

🔴 **Non pubblicare e non pausare God Mode.** Il backend locale e le correzioni sono verificati, ma il rilascio Aruba richiede il canale sicuro già predisposto e non può essere eseguito leggendo/esponendo credenziali. Dopo il deploy: cache-buster live, click-through browser isolato e controllo del marker dashboard/wizard. Nessun pagamento, segreto, ordine, DNS o email reale è stato toccato.
