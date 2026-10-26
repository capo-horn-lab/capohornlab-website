---
id: "safehaven-1"
titolo: "SAFEHAVEN-1, CP-1, GAPFILL-1 — oro come rifugio; fattore Cochrane-Piazzesi su ZN; gap in calo"
data: "2026-10-20"
strumenti:
  - "GLD"
  - "SPY"
  - "MGC"
  - "ZN"
  - "MES"
  - "MNQ"
  - "M2K"
  - "MYM"
finestra: "GLD e SPY 2005-2026 e MGC/ZN su MES 2019-2026 (SAFEHAVEN-1); curva GSW e ACM (784 mesi) e ZN 93 fine mese (CP-1); MNQ, MES, M2K, MYM 2019-2026 (GAPFILL-1: 334-384 giorni G1)."
verdetto: "non confermata"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9863-L9870"
prove: []
---

## Domanda

l'oro è copertura/rifugio nei giorni di stress azionario? Il fattore CP prevede ZN? Comprare un gap in calo con obiettivo la chiusura di ieri ha edge?

## Metodo e rubrica

Regressioni annidate con Newey-West (SAFEHAVEN), IC e placebo (CP-1), scoperta/verifica e placebo (GAPFILL-1). Rubriche prima: sì (L9783, L9872, L9883).

## Esito

| Risultato | Fonte |
|---|---|
| SAFEHAVEN-1 "PASS, NON CONFERMATA": parte paper non confermata (in verifica b>0 con t 2,79; scoperta copertura debole), regola operativa non confermata (ZN in verifica perde con t -2,5). | docs/EXECUTION_LEDGER.md#L9863-L9870 |
| CP-1 "PASS (parte DGS10 BLOCKED_ENV), NON CONFERMATA": scoperta R² 0,228 (Wald 26,2, p 0,00008) ma fuori campione 2019-2025 pendenza +0,26 (t NW12 0,44), R² 0,006 | docs/EXECUTION_LEDGER.md#L9863-L9870 · docs/EXECUTION_LEDGER.md#L9909-L9914 |
| ZN IC CP +0,062 (t 0,56). | docs/EXECUTION_LEDGER.md#L9909-L9914 |
| GAPFILL-1 "Esito PASS, verdetto NON CONFERMATA per G1 e G2 su entrambi gli orizzonti (0 strumenti di verifica su 3": "il gap si chiude due volte su tre" ma i giorni in cui non si chiude perdono molto (peggiore da -180 a -1.287 USD). | docs/EXECUTION_LEDGER.md#L9863-L9870 · docs/EXECUTION_LEDGER.md#L9909-L9914 · docs/EXECUTION_LEDGER.md#L9891-L9896 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- SAFEHAVEN: "nel 2019-2026 oro e Treasury non hanno fatto da rifugio"
- GAPFILL: "'il gap si chiude due volte su tre' è vero e non è un vantaggio, perché la terza volta costa più delle altre due".

## Prove

- runtime/proofs/safehaven1/
- runtime/proofs/cp1/
- runtime/proofs/gapfill1/
