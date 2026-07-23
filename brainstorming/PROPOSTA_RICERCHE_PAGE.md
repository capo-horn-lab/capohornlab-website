# PROPOSTA — Pagina Ricerche / Research
**Data:** 22 Luglio 2026  
**Autore:** Midas (Lead Data/Research)  
**Team:** Cupido, Odino  
**Progetto:** Capo Horn Lab — Website  

---

## Executiv Summary

La pagina Ricerche è il cuore intellettuale del sito. Non vende nulla — dimostra rigore. Ogni ricerca pubblicata è un *falsificazionista manifesto*: si espone al mercato reale, mostra cosa ha funzionato, cosa no, e perché. Il visitatore deve uscire dalla pagina con una sola convinzione: *"Qui sanno quello che fanno."*

La proposta si articola in **5 sezioni**:
1. Struttura della pagina
2. Catalogo grafici statistici (standard library)
3. Integrazione ricerche esistenti
4. Metodologia editoriale
5. Piano tecnico implementativo

---

## 1. STRUTTURA DELLA PAGINA

### 1.1 Overview Page (`/research/`)

```
┌─────────────────────────────────────────────────────┐
│  🔬 Ricerche                                       │
│  Quantitative research on real historical data.     │
│  No strategy selling. No signals. Just evidence.    │
│                                                     │
│  [FILTRI: Tutte | ES | NQ | CL | Altro]            │
│  [ORDINA: Più recenti | Più letti | A-Z]           │
│                                                     │
│  ┌───────────────────┐  ┌───────────────────┐      │
│  │ ES 1m Quant       │  │ When Structure    │      │
│  │ Research Summary  │  │ Meets Reality     │      │
│  │ 📄 2026-01-20     │  │ 📄 2026-01-20     │      │
│  │                   │  │                   │      │
│  │ Nessun edge su    │  │ Impulse-          │      │
│  │ prezzo puro ES    │  │ retracement:      │      │
│  │ 1-minuto.         │  │ pattern reale,    │      │
│  │                   │  │ non profittevole. │      │
│  │ [Leggi →]         │  │ [Leggi →]         │      │
│  └───────────────────┘  └───────────────────┘      │
│                                                     │
│  ...altre card...                                    │
└─────────────────────────────────────────────────────┘
```

**Elementi della card:**
- Titolo ricerca
- Data pubblicazione
- Badge strumento (ES, NQ, CL...)
- Badge esito: 🟢 Positivo / 🔴 Negativo / 🟡 Misto
- Abstract di 1-2 righe
- CTA "Leggi la ricerca →"
- Tag: metodologia usata (Machine Learning, Statistica, Pattern...)

### 1.2 Pagina Dettaglio Ricerca (`/research/<slug>`)

Template unico con sezioni obbligatorie:

```
┌─────────────────────────────────────────────────────┐
│  # Titolo Ricerca                                   │
│  Pubblicato: GG/MM/AAAA  ·  Strumento: ES  ·        │
│  Esito: 🔴 Nessun edge rilevato                    │
│                                                     │
│  ## 1. Obiettivo                                    │
│  Una frase che spiega cosa si voleva scoprire.      │
│                                                     │
│  ## 2. Ipotesi                                      │
│  Ipotesi nulla + alternativa, formulate             │
│  statisticalmente.                                  │
│                                                     │
│  ## 3. Dati                                         │
│  - Strumento: ES futures                            │
│  - Timeframe: 2020-2024, 1-minuto OHLCV            │
│  - Fonte: Databento, tick → aggregato 1m           │
│  - N. osservazioni: ~1.2M                           │
│  - Split: 70% IS / 30% OOS                         │
│                                                     │
│  ## 4. Metodologia                                  │
│  Descrizione chiara dell'approccio, replicabile.    │
│                                                     │
│  ## 5. Risultati                                    │
│  [GALLERIA GRAFICI — vedi Sezione 2]               │
│                                                     │
│  ## 6. Interpretazione                             │
│  Cosa dicono (e non dicono) i numeri.              │
│                                                     │
│  ## 7. Limitazioni                                  │
│  Onestà intellettuale. Cosa NON copre questo test.  │
│                                                     │
│  ## 8. Conclusione                                  │
│  Takeaway in 2-3 frasi.                             │
│                                                     │
│  ## 9. Riferimenti                                  │
│  Citazioni, paper, dati, codice (se pubblico).      │
│                                                     │
│  ──────────────────────────────────────────────      │
│  📎 Scarica report PDF  ·  🐍 Codice su GitHub     │
│  (se applicabile)                                    │
└─────────────────────────────────────────────────────┘
```

---

## 2. CATALOGO GRAFICI STATISTICI — Standard Library

Ogni ricerca DEVE includere un sottoinsieme di questi grafici. Definisco uno **standard minimo** (MVP) e uno **standard completo** (full).

### 2.1 Standard Minimo (MVP) — 7 grafici

| # | Grafico | Tipo | Cosa mostra |
|---|---------|------|-------------|
| 1 | **Equity Curve** | Line chart (cumulativo) | Crescita/decrescita del capitale nel tempo. Con banda OOS evidenziata. |
| 2 | **Drawdown** | Area chart | Massimi drawdown consecutivi. Linea orizzontale a -20% come reference. |
| 3 | **Trade Distribution** | Histogram + Kernel density | Distribuzione dei PnL per trade. Media, mediana, skewness. |
| 4 | **Monthly/Annual Returns** | Heatmap (mesi × anni) | Rendimenti mensili colorati (verde/rosso). Pattern stagionali. |
| 5 | **Long vs Short Breakdown** | Bar chart affiancato | Profit factor, win rate, avg trade separati per direzione. |
| 6 | **Performance Table** | Tabella statica | Sharpe, Sortino, Calmar, Profit Factor, Win Rate, Avg Trade, Max DD, % Positive, N trades, % OOS |
| 7 | **IS vs OOS Comparison** | Bar chart affiancato | Sharpe, DD, Profit Factor affiancati IS vs OOS. R^2 delle barre. |

### 2.2 Standard Completo (Full) — +6 grafici

| # | Grafico | Tipo | Cosa mostra |
|---|---------|------|-------------|
| 8 | **Monte Carlo Simulation** | 100-1000 linee semitrasparenti | Equity curve simulata con shuffle dei trade. Banda 5°-95° percentile. |
| 9 | **Parameter Stability** | Heatmap 2D | Sharpe ratio al variare di 2 parametri. Zona di stabilità evidente. |
| 10 | **By Day of Week** | Bar chart | Average trade PnL per giorno (Mon-Fri). |
| 11 | **By Hour of Day** | Bar/Line chart | Average trade PnL per ora di esecuzione (sessioni). |
| 12 | **Convergence Chart** | Line chart overlay | Equity curve + buy-hold comparativo sullo stesso periodo. |
| 13 | **Trade Duration** | Histogram | Durata delle operazioni (minuti/giorni). Trade brevi vs lunghi. |

### 2.3 Specifiche Tecniche Grafici

| Parametro | Valore |
|-----------|--------|
| Palette | Palette custom Capo Horn (navy #0F172A, teal #14B8A6 per positivo, rose #E11D48 per negativo, amber #F59E0B per warning) |
| Font | Inter (UI) / JetBrains Mono (numeri) |
| Interattività | Tooltip hover, zoom X/Y opzionale (Plotly) |
| Fallback | Static image (PNG/SVG) per embed statico |
| Libreria | Plotly.py → export HTML statico + PNG fallback |
| Aspect ratio | 16:9 per landscape, 1:1 per heatmap |
| DPI | 150 (screen), 300 (PDF export) |

---

## 3. INTEGRAZIONE RICERCHE ESISTENTI

### 3.1 Stato Attuale

| Ricerca | File | Contenuto | Stato |
|---------|------|-----------|-------|
| ES 1m Quant Research Summary | `ES_1m_Quant_Research_Summary.pdf` | 2 pagine, test su prezzo puro ES 1-minuto | ✅ Da pubblicare |
| When Structure Meets Reality | `When_Structure_Meets_Reality_ES_Research.pdf` | 2 pagine, pattern impulse-retracement su ES | ✅ Da pubblicare |

**Nota:** Entrambi i PDF sono binari (ReportLab-generated, with FlateDecode compression). Non estraibili via read_file come testo. Vanno:
1. Ri-generati da codice sorgente Python (se disponibile)
2. Oppure estratti via strumento OCR (pymupdf, marker-pdf) e riscritti
3. O pubblicati solo come PDF scaricabili con pagina-riassunto manuale

### 3.2 Workflow Integrazione

```
ES_1m_Quant_Research_Summary.pdf
├── Estrarre testo (pymupdf) o riscrivere da sorgente
├── Validare metriche contro market data
├── Generare grafici standard (MVP: equity, drawdown, distribuzione, monthly, long/short, performance table, IS/OOS)
├── Compilare template dettaglio
└── Pubblicare come /research/es-1m-quant-summary

When_Structure_Meets_Reality_ES_Research.pdf
├── Stesso workflow
├── Grafici aggiuntivi: struttura pattern recognition visual, distribution by pattern type
├── Nota metodologica extra su come sono stati identificati gli impulsi
├── Compilare template dettaglio
└── Pubblicare come /research/when-structure-meets-reality
```

### 3.3 Contenuti Estratti (ciò che sappiamo dai PDF)

**Ricerca #1 — ES 1m Quant Research Summary:**
- Ipotesi: il prezzo puro (price-only) su timeframe 1-minuto ES ha potere predittivo?
- Risultato: NO — nessun edge statisticamente significativo
- Implicazione: strategie price-only su ES 1m sono rumorose, serve contesto aggiuntivo (struttura, volume, ordini)

**Ricerca #2 — When Structure Meets Reality:**
- Ipotesi: i pattern impulse-retracement-breakout hanno valore predittivo?
- Risultato: i pattern ESISTONO (non sono rumore) ma NON SONO PROFITTEVOLI dopo costi di transazione
- Implicazione: pattern recognition funziona in isolation, ma lo slippage e le commissioni erodono ogni edge

### 3.4 Value Proposition delle Ricerche Negative

Entrambe le ricerche sono **negative** — e questa è la forza del brand. La pagina Ricerche deve rendere esplicito:

> "Qui pubblichiamo risultati veri, non quelli che fanno bella figura. Abbiamo speso tempo e potenza di calcolo per dimostrare che due idee comuni NON funzionano. Questo è più utile della maggior parte delle 'strategie vincenti' in vendita online."

**Badge esito previsto per entrambe: 🔴 (Nessun edge significativo)**

---

## 4. METODOLOGIA EDITORIALE

### 4.1 Criteri di Pubblicazione

Una ricerca è pubblicabile se:
1. **Ipotesi falsificabile** — deve poter essere smentita dai dati
2. **Dati riproducibili** — Databento / fonti citate, non dati proprietari inaccessibili
3. **Metriche complete** — Sharpe, DD, nTrades, IS/OOS
4. **No data snooping** — train/test split temporale (non random), walk-forward se applicabile
5. **Costi inclusi** — slippage e commissioni realistiche per strumento
6. **Onestà intellettuale** — limitazioni esplicite, non "funziona ma..."

### 4.2 Tassonomia Ricerche

```
Categoria          | Sotto-categoria         | Esempi
-------------------|------------------------|---------------------------
Price Action       | Pure price, patterns   | ES 1m price-only
Strutturale        | Order flow, book       | (Da fare con Databento MDP3)
Statistica         | Distribuzioni, corr    | (Da fare)
Macro / Cross-asset| Correlazioni           | ES vs NQ, ES vs CL
Machine Learning   | Feature importance     | (Pipeline futura)
Microstruttura     | Tick, bid/ask, spread  | (Da fare con tick data)
```

### 4.3 Pipeline di Produzione

```
IDEA → Validazione peer (Cupido/Odino) → 
Script Python su D:\marketdata → 
Generazione grafici (Plotly → HTML + PNG) → 
Compilazione template → 
Review Midas → 
Pubblicazione
```

**Strumenti tecnici:**
- Python 3.11 + pandas/polars per analisi
- Plotly per grafici interattivi → export HTML + PNG statico
- ReportLab / WeasyPrint per PDF export
- Dati da `D:\marketdata\` (parquet) via polars/pandas
- Template ricerca in YAML/MD → build statica

### 4.4 Schema Dati Metadati (ricerca.yml)

```yaml
---
title: "ES 1-Minute Quantitative Research Summary"
slug: es-1m-quant-summary
published: 2026-01-20
updated: 2026-07-22
status: published  # draft | published | updated
instrument: ES
timeframe: "1-minute"
period: "2020-2024"
data_source: "Databento"
obs_count: 1200000
split: "70/30 IS/OOS"
result: negative  # positive | negative | mixed | inconclusive
tags:
  - price-action
  - pure-price
  - no-edge
metrics:
  sharpe_is: 0.12
  sharpe_oos: -0.08
  profit_factor_is: 1.03
  profit_factor_oos: 0.97
  max_dd_is: -8.2
  max_dd_oos: -11.4
  win_rate_is: 48.2
  win_rate_oos: 47.1
  n_trades: 45230
team:
  lead: Midas
  reviewers: [Cupido, Odino]
charts:
  mvp: true
  full: false
---
```

---

## 5. PIANO TECNICO IMPLEMENTATIVO

### 5.1 Architettura Pagina

```
/research/                    → Lista ricerche (grid cards + filtri)
/research/<slug>/             → Pagina dettaglio ricerca
/research/methodology/        → Pagina metodologia generale

Assets statici:
  /assets/research/<slug>/charts/   → Grafici (HTML + PNG)
  /assets/research/<slug>/pdf/      → PDF scaricabili
  
Dati:
  /data/research/index.json         → Indice ricerche
  /data/research/<slug>.md          → Contenuto ricerca (frontmatter + body)
```

### 5.2 Stack Consigliato

| Layer | Tecnologia | Perché |
|-------|-----------|--------|
| Build | Astro / Next.js SSG | Pagine statiche veloci, MDX per contenuti ricerca |
| Charts | Plotly.py → embed HTML | Interattività senza librerie JS pesanti |
| Stili | Tailwind + palette custom | Dark/navy brand identity |
| Ricerca full-text | Pagefind / Lunr | Senza backend |
| PDF export | WeasyPrint / Puppeteer | Da HTML template a PDF |
| Download dati | Parquet + Hugging Face Datasets | Se vogliamo rendere i dati pubblici |

### 5.3 Priorità

| Priorità | Cosa | Quando |
|----------|------|--------|
| P0 | Template pagina dettaglio ricerca (MVP 7 grafici) | Settimana 1 |
| P0 | Pubblicare Ricerca #1 (ES 1m) con template | Settimana 1-2 |
| P0 | Pubblicare Ricerca #2 (Structure) con template | Settimana 2-3 |
| P1 | Pagina overview con filtri/griglia | Settimana 3 |
| P1 | Grafici aggiuntivi (Monte Carlo, Parameter Stability) | Settimana 3-4 |
| P2 | Galleria interattiva grafici con zoom/tooltip | Settimana 4-5 |
| P2 | PDF export automatico | Settimana 5-6 |
| P3 | Pagina metodologia generale | Settimana 6 |
| P3 | Schema dati strutturato (JSON-LD) per SEO | Settimana 6 |

### 5.4 Generazione Grafici — Pipeline Automazione

```python
# generate_research_charts.py
# Input: research YAML config + parquet data path
# Output: directory con tutti i grafici (HTML + PNG)

def generate_equity_curve(trades, output_dir): ...
def generate_drawdown(trades, output_dir): ...
def generate_trade_distribution(trades, output_dir): ...
def generate_monthly_heatmap(trades, output_dir): ...
def generate_long_short(trades, output_dir): ...
def generate_performance_table(trades, output_dir): ...
def generate_is_oos(is_trades, oos_trades, output_dir): ...
# ... full suite

# CLI: python generate_research_charts.py --config research_001.yml
```

---

## 6. OPEN QUESTIONS (da decidere con Cupido, Odino, Francesco)

1. **PDF esistenti**: abbiamo il codice sorgente Python che li ha generati? O dobbiamo estrarre via OCR/pymupdf?
2. **Grafici interattivi o statici?** Plotly HTML interattivo per web + PNG per PDF/email
3. **Multi-lingua?** Research in inglese (default) con italiano secondario?
4. **Download dati**: rendiamo pubblici i dataset usati (parquet filtrato)? O solo risultati?
5. **Codice**: repo pubblico con gli script di ricerca? Trasparenza totale.
6. **Newsletter**: ogni nuova ricerca → notifica email + abstract + link.
7. **Metriche comparative**: ha senso una tabella "Research Dashboard" riassuntiva di tutte le ricerche?
8. **Rolling update**: quando una ricerca viene aggiornata con nuovi dati, versione o appendice?

---

## 7. PROSSIMI STEP (consigliati)

1. ✅ **APPROVARE questa proposta** da Francesco e team
2. Estrarre testo dai PDF esistenti con pymupdf + validare contenuti
3. Costruire template pagina dettaglio (MVP 7 grafici)
4. Scrivere script generazione grafici (riutilizzabile)
5. Pubblicare Ricerca #1 e #2
6. Identificare prossima ricerca (suggerimento: volume profile su ES? order flow da Databento MDP3? structure su NQ?)

---

*"Beyond the Market Edge" — Non vendiamo strategie. Vendiamo verità.*
