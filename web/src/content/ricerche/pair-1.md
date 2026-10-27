---
id: "pair-1"
titolo: "PAIR-1 — spread MNQ contro MES (stat-arb intraday)"
data: "2026-10-19"
strumenti:
  - "MNQ"
  - "MES"
finestra: "MNQ e MES 1 minuto NinjaTrader, 146.937 candele 5m comuni, 1.914 sessioni 2019-05..2026-10"
verdetto: "verdetto non estratto: vedi Esito"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8024-L8026"
prove:
  - "runtime/proofs/pair1/pair1.json"
---

## Domanda

lo spread z-score tra MNQ e MES ha mean reversion sfruttabile?

## Metodo e rubrica

4 varianti (Z 2/2,5 x L 60/120), costi 0,95 USD per lato, 1 tick per gamba; rubrica LAB-2. Rubrica prima: sì (L7996).

## Esito

| Risultato | Fonte |
|---|---|
| "0 adottate su 4". | docs/EXECUTION_LEDGER.md#L8024-L8026 |
| Netto per trade scoperta/verifica: Z 2 L 60 -11,43 / -9,01 USD (t -3,80). | docs/EXECUTION_LEDGER.md#L8024-L8026 |
| Costo di un trade a due gambe ≈10,5 USD (commissioni 5,2 + slippage 5,3). | docs/EXECUTION_LEDGER.md#L8024-L8026 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Lettura e limiti (dal registro)

- "il ritorno dello spread verso la media c'è appena".

## Prove

- runtime/proofs/pair1/pair1.json
