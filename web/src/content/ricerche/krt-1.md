---
id: "krt-1"
titolo: "KRT-1 — due premi nelle materie prime (Kang-Rouwenhorst-Tang): pressione di copertura e inversione degli speculatori"
data: "2026-10-20"
strumenti:
  - "MCL"
  - "MGC"
finestra: "CFTC disaggregated futures-only 2006-2026 (34,7 MB), 11 mercati continui Yahoo 2005-01..2026-10 (60.290 barre), MCL e MGC con costi"
verdetto: "non confermata"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9766-L9771"
prove:
  - "runtime/proofs/krt1/krt1.json"
  - "runtime/proofs/krt1/run.log"
  - "runtime/proofs/krt1/yahoo_daily.csv"
---

## Domanda

la posizione degli hedger (HP) e la variazione dei money manager (MM) prevedono i rendimenti settimanali?

## Metodo e rubrica

Pannello con t Driscoll-Kraay; IC per mercato (33 righe per segnale) con BH; regola di terzile e placebo 200 permutazioni. Rubrica prima: sì (L9683).

## Esito

| Risultato | Fonte |
|---|---|
| "NON CONFERMATA". | docs/EXECUTION_LEDGER.md#L9766-L9771 |
| Pannello: HP z52 h1 +0,019 (t 1,02) -> +0,005 (t 0,26) | docs/EXECUTION_LEDGER.md#L9766-L9771 |
| segni del paper presenti ma mai t≥2. | docs/EXECUTION_LEDGER.md#L9766-L9771 |
| IC per mercato: HP 0 su 33 | docs/EXECUTION_LEDGER.md#L9766-L9771 |
| MM 1 su 33 (ZW h13 scoperta -0,059 -> verifica -0,178, t -3,73, q 0,006). | docs/EXECUTION_LEDGER.md#L9766-L9771 |
| Regola di terzile: HP 0 su 11, MM 0 su 11, CIT 0 su 8 | docs/EXECUTION_LEDGER.md#L9766-L9771 |
| micro MGC MM +76,0 USD (t 1,81, n 199, p95 68,1, q 0,14). | docs/EXECUTION_LEDGER.md#L9766-L9771 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- MGC MM "sopra il placebo ma t < 2 e q >..." (non provato).

## Prove

- runtime/proofs/krt1/krt1.json
- runtime/proofs/krt1/run.log
- runtime/proofs/krt1/yahoo_daily.csv
