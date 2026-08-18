# Fix Auth (fail-closed) + Grafici Ricerche — 2026-08-18

**Working copy:** `D:/CapoHornLab/projects/capohornlab-website` · **Nessun deploy eseguito.**

---

## 1. Cosa era rotto

- **Auth live (Aruba):** `login.html` VECCHIO non chiama il backend: "Logging in…" + redirect a `dashboard.html` dopo 800ms → accesso libero. Il backend `/api/v1` sul live risponde 404.
- **Working copy:** login/signup erano GIÀ fail-closed (client reale `assets/js/account-client.js` + `CHLAccount`); verificato e confermato, nessun mock residuo.
- **Grafici:** `research/published_research.json` (13 ricerche) aveva `slug_dir` assente/`None`; `research-detail.html` usava `slug_dir`/`charts_slug` corti (`tsmom`, `orb`, `vwap-mr`, `spy-momentum`) che NON esistevano come directory → ogni immagine 404 con fallback ai PNG generici root (ciclo di richieste inutili, grafici generici al posto di quelli reali).

## 2. Cosa ho corretto (file + righe)

| File | Riga | Modifica |
|---|---|---|
| `research-detail.html` | 1850, 1934 | `slug_dir`/`charts_slug` `tsmom` → `local-es-tsmom-2023-01` |
| `research-detail.html` | 1974, 2046 | `orb` → `local-es-orb-2023-01` |
| `research-detail.html` | 2085, 2156 | `vwap-mr` → `local-cl-vwap-mr-2024q1` |
| `research-detail.html` | 2195, 2265 | `spy-momentum` → `local-nq-intraday-momentum-2023-01` |
| `research-detail.html` | 2304 | `slug_dir` entry `cwm` → `cwmr` (consistenza con `charts_slug`) |
| `research-detail.html` | 3417 | `renderCharts`: `'../research/charts/' + (slugDir ? slugDir + '/' : '') + chart.id + '.png'` (gestisce slugDir vuoto) |
| `research-detail.html` | 3423 | `onerror` con guardia anti-loop: `if(!this.dataset.fb){this.dataset.fb='1';this.src='../research/charts/'+chart.id+'.png'}` — fallback singolo, niente loop infinito |
| `research/published_research.json` | tutti i 13 entry | aggiunto `"slug_dir"` dopo `"slug"` (mappa sotto) — JSON valido |
| `research/charts/{cwmr, pamr, ftrl, trend-following-stocks, vix-vrp, fivemin-overlay, market-cycle-analysis}/` | nuovi | 7 dirs × 7 PNG standard copiati dai generici root (fallback autorizzato; nessuna backtest run locale esiste per queste strategie → nessun dato per-trade per `chart_pipeline.py`) |
| `dashboard.html` | ~1590 | `getMe` fallito: pulizia token + redirect a `login.html?next=dashboard.html` (prima: `logout()` → index.html) — fail-closed su token scaduto/falso |
| `test-strategy.html` | ~2089 | commento fuorviante "Placeholder: in production..." rimosso (il redirect a login/signup era già reale) |

**Verificato già OK (nessuna modifica):** `login.html` `handleLogin` (631–647), `signup.html` `handleSignup` (327–346) — redirect SOLO dopo successo del backend, errore mostrato altrimenti; `account-client.js` rigetta su `!response.ok`; nessun `setTimeout`+redirect/mock rimasto (grep su login/signup/dashboard/test-strategy: NESSUN match).

## 3. Test curl sul backend locale (127.0.0.1:8000, attivo, health OK)

| Test | Esito |
|---|---|
| `POST /api/v1/auth/signup` (utente di test) | **HTTP 503** `{"detail":"Account created, but verification email delivery is unavailable."}` — account **CREATO** e persistito (SMTP non configurato in dev → 503 solo sulla consegna email) |
| `POST /api/v1/auth/login` (credenziali corrette) | **HTTP 200** → `access_token` + `user` (role=client, verified=false) |
| `POST /api/v1/auth/login` (password errata) | **HTTP 401** `{"detail":"Invalid email or password"}` |
| `GET /api/v1/auth/me` (Bearer token) | **HTTP 200** → user JSON |
| `GET /api/v1/auth/me` (senza token) | **HTTP 401** `{"detail":"Not authenticated"}` |

**Utente di test NON cancellato** (come richiesto): `chl-auth-test-1787072728@example.com` / id `81bceca8-41af-4e3a-ac7f-172f35a35e4e` (password `TestPass123!` — riportata solo perché è un utente di test creato ad hoc).

## 4. Stato grafici per ricerca

| slug | dir | PNG count |
|---|---|---|
| es-1m-quant-summary | `es-1m-quant` | 7 |
| when-structure-meets-reality | `when-structure` | 7 |
| time-series-momentum-futures | `local-es-tsmom-2023-01` | 7 |
| opening-range-breakout-intraday | `local-es-orb-2023-01` | 7 |
| vwap-mean-reversion-intraday | `local-cl-vwap-mr-2024q1` | 7 |
| intraday-momentum-spy | `local-nq-intraday-momentum-2023-01` | 7 |
| confidence-weighted-mean-reversion | `cwmr` | 7* |
| passive-aggressive-mean-reversion | `pamr` | 7* |
| follow-the-regularized-leader | `ftrl` | 7* |
| trend-following-on-stocks-concretum | `trend-following-stocks` | 7* |
| volatility-risk-premium-vix-etns | `vix-vrp` | 7* |
| fivemin-mean-reversion-alpha-overlay | `fivemin-overlay` | 7* |
| market-cycle-analysis | `market-cycle-analysis` | 7* |

\* = PNG generici di fallback (nessuna run locale per queste strategie; vedi "Da fare").

**Verifica finale:** tutte le 13 `charts_slug` in `research-detail.html` puntano a dirs esistenti (7 png ciascuna); zero vecchi valori residui; `node --check` superato sugli script inline di login, signup, dashboard, test-strategy, research-detail.

## 5. Da fare (fuori scope / prossimi passi)

- **Deploy** (non eseguito): pubblicare la working copy su Aruba — login/signup reali, dashboard/test-strategy fail-closed, nuova mappatura grafici.
- **7 ricerche con PNG generici:** generare grafici REALI con `research/chart_pipeline.py` appena esistono CSV per-trade (`date,equity,drawdown,trade_return,direction,regime`) per CWMR/PAMR/FTRL/trend-following-stocks/VIX-VRP/fivemin-overlay/market-cycle-analysis (nessuna run backtest locale presente in `research/runs/`).
- **Email verification:** configurare SMTP per il flusso signup (in dev risponde 503 dopo aver creato l'account).
- **Note:** `checkout.html` non usa `CHLAccount` (pagina di pagamento statica) — da rivalutare nel deploy review. Il patch tool ha scritto LF su alcuni hunk di `research-detail.html` (file CRLF): solo cosmetico.
