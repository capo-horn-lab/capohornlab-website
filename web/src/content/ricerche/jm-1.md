---
id: "jm-1"
titolo: "JM-1 — statistical jump model come filtro di rischio"
data: "2026-10-19"
strumenti:
  - "SPY"
  - "QQQ"
finestra: "SPY e QQQ 2014-2026"
verdetto: "non confermata"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8540-L8545"
prove:
  - "runtime/proofs/jm1/jm1.json"
---

## Domanda

un jump model a 2 stati riduce il drawdown senza peggiorare lo Sharpe del comprare e tenere?

## Metodo e rubrica

Penalità scelta ogni mese sugli 8 anni precedenti, 1 giorno di ritardo, 10 bp per lato; confronto con filtri semplici (VIX/VIX3M>1, VIX sopra la mediana a 252 giorni). Rubrica prima: sì (L8474).

## Esito

| Risultato | Fonte |
|---|---|
| "NON CONFERMATO" (esito a): SPY comprare e tenere Sharpe 1,02, drawdown 23,2% | docs/EXECUTION_LEDGER.md#L8540-L8545 |
| JM Sharpe 0,24, drawdown 27,4%, investito 50%, 47 cambi | docs/EXECUTION_LEDGER.md#L8540-L8545 |
| QQQ comprare e tenere 0,94 / 33,7% | docs/EXECUTION_LEDGER.md#L8540-L8545 |
| JM 0,56 / 30,3%. | docs/EXECUTION_LEDGER.md#L8540-L8545 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "nessun filtro di regime (JM, VIX/VIX3M, VIX alto) batte il comprare e tenere: uscire nei periodi di stress perde i rimbalzi".

## Prove

- runtime/proofs/jm1/jm1.json
