---
id: "stop-1"
titolo: "STOP-1 — stop di protezione sui trade della famiglia MR"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "M2K"
  - "MYM"
finestra: "IBS, R1b, TT, 3WEAK su MES, MNQ, M2K, MYM dal 2022 (stessi trade di BRIDGE-1)"
verdetto: "non confermata"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8836-L8841"
prove:
  - "runtime/proofs/stop1/stop1.json"
---

## Domanda

uno stop a 2 o 3 sigma previste riduce drawdown e giorno peggiore?

## Metodo e rubrica

Varianti S2 e S3 (stop a ingresso x (1 - 2 o 3 x sigma_prev)), bootstrap a blocchi accoppiato 20 giorni (2.000); adottata se su ≥3 regole su 4 drawdown e CVaR 5% migliorano e la differenza di Sharpe ≥0. Rubrica prima: sì (L8829).

## Esito

| Risultato | Fonte |
|---|---|
| "NESSUNA VARIANTE ADOTTATA; gli stop peggiorano la famiglia MR anche nei giorni negativissimi." IBS 582 trade +31,4 bp: S2 +17,5 bp (34% stoppati, Sharpe -0,87, DD 4.655 contro 3.525) | docs/EXECUTION_LEDGER.md#L8836-L8841 |
| R1b S2 Sharpe -2,59, DD 2.811 contro 1.409 | docs/EXECUTION_LEDGER.md#L8836-L8841 |
| solo 3WEAK S3 migliora (+40,1, Sharpe +0,18, DD 453 contro 576). | docs/EXECUTION_LEDGER.md#L8836-L8841 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "lo stop vende il minimo e trasforma perdite temporanee in perdite reali... Il rischio dei giorni negativissimi si gestisce con la dimensione (una posizione, un micro) e non con lo stop."

## Prove

- runtime/proofs/stop1/stop1.json
