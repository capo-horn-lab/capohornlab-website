---
id: "opt-all"
titolo: "OPT-ALL (e OPT-ALL-ZN) — ottimizzazione vera (griglia + walk-forward) di tutte le famiglie su tutti gli strumenti"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "M2K"
  - "MYM"
  - "MGC"
  - "M6E"
  - "FESX"
  - "FDXM"
  - "MBT"
  - "MCL"
  - "ZN"
finestra: "10 strumenti (MES, MNQ, M2K, MYM, MGC, M6E, FESX, FDXM, MBT, MCL) e ZN; 6 famiglie (IBS, RSI2, TT, NDOWN, MA, DONCHIAN), 98 combinazioni per strumento"
verdetto: "non confermata"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8622-L8626"
prove:
  - "runtime/proofs/optall/optall.json"
---

## Domanda

ottimizzare i parametri per strumento (come lo Strategy Analyzer) aggiunge valore?

## Metodo e rubrica

Walk-forward mobile 500/60, obiettivo prudente, 200 placebo con combinazioni casuali, PBO CSCV, DSR, BH sui 60 test. Rubrica prima: sì (L8581).

## Esito

| Risultato | Fonte |
|---|---|
| "0 confermati su 60." Migliori fuori campione: MES IBS +4,41 bp/sessione (t 2,85, q 0,089) ma sotto il p95 dei placebo 5,04 e DSR 0,34 | docs/EXECUTION_LEDGER.md#L8622-L8626 · docs/EXECUTION_LEDGER.md#L8644-L8644 |
| MNQ IBS +5,08 (t 2,58, p95 6,56) | docs/EXECUTION_LEDGER.md#L8622-L8626 |
| MCL nessuna famiglia con t sopra 1,3 | docs/EXECUTION_LEDGER.md#L8644-L8644 |
| PBO medio 0,43. | docs/EXECUTION_LEDGER.md#L8622-L8626 · docs/EXECUTION_LEDGER.md#L8644-L8644 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "il vantaggio è della famiglia, non della combinazione ottimizzata. Ottimizzare i parametri non aggiunge nulla (ciò che lo Strategy Analyzer non può vedere senza placebo)".

## Prove

- runtime/proofs/optall/optall.json
