---
id: "rob-1"
titolo: "ROB-1 — robustezza dei risultati confermati (t sui giorni, deflated Sharpe, PBO)"
data: "2026-10-19"
strumenti:
  - "MYM"
finestra: "16 test confermati di MR-1 + IBS-NT + IBS-MYM"
verdetto: "confermata"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8360-L8370"
prove:
  - "runtime/proofs/rob1/rob1.json"
---

## Domanda

i risultati reggono se si conta per giorno invece che per trade e si penalizza il numero di prove?

## Metodo e rubrica

t sui giorni, PSR e deflated Sharpe con N=24 (e N=1.000), PBO con CSCV a 10 blocchi sulle 12 regole. ROBUSTO se t giorni≥2 e DSR(24)≥0,95. Rubrica prima: sì (L8351).

## Esito

| Risultato | Fonte |
|---|---|
| ROBUSTI: TT future 161 trade su 74 giorni, t trade 3,88 -> t giorni 2,31, DSR24 0,996, DSR1000 0,903 | docs/EXECUTION_LEDGER.md#L8360-L8370 |
| TT SPY+QQQ t giorni 3,59, DSR24 0,999 | docs/EXECUTION_LEDGER.md#L8360-L8370 |
| 3WEAK future 189 trade su 113 giorni, t giorni 3,20, DSR24 1,000, DSR1000 0,981 | docs/EXECUTION_LEDGER.md#L8360-L8370 |
| WR2 future t giorni 3,74 DSR24 0,989 DSR1000 0,645 | docs/EXECUTION_LEDGER.md#L8360-L8370 |
| IBS future 4 indici (942 trade) t giorni 4,17, DSR24 0,967, DSR1000 0,234. | docs/EXECUTION_LEDGER.md#L8360-L8370 |
| NON robusti: R1a (DSR24 0,872), R1b (0,887), R3 (0,827), 3DOWN future (1,44, 0,125)... | docs/EXECUTION_LEDGER.md#L8360-L8370 |
| PBO 0,536 (logit mediano -0,15). | docs/EXECUTION_LEDGER.md#L8360-L8370 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "il t per trade sovrastima"
- "le regole della famiglia sono intercambiabili"
- per il bot: "famiglia usata insieme (non la 'migliore')".

## Prove

- runtime/proofs/rob1/rob1.json
