---
id: "size-2"
titolo: "SIZE-2 — dimensionamento a volatilità prevista sulle regole di mean reversion"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "M2K"
  - "MYM"
finestra: "IBS, R1b, TT, 3WEAK su MES, MNQ, M2K, MYM 2019-2026 (trade dal 2022)"
verdetto: "non adottata"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8512-L8518"
prove:
  - "runtime/proofs/size2/size2.json"
---

## Domanda

scalare la dimensione con la volatilità prevista (RV21 o HAR) migliora Sharpe e drawdown?

## Metodo e rubrica

Sharpe giornaliero, Calmar, drawdown, CVaR 5%; adottata se differenza di Sharpe ≥0 su ≥3 regole su 4 e drawdown non peggiore. Rubrica prima: sì (L8460).

## Esito

| Risultato | Fonte |
|---|---|
| "NON ADOTTATA nessuna variante." | docs/EXECUTION_LEDGER.md#L8512-L8518 |
| RV21 1 su 4 (solo TT: Sharpe 2,44 vs 2,33, DD 997 vs 1.242), HAR 0. | docs/EXECUTION_LEDGER.md#L8512-L8518 |
| IBS 566 trade: Sharpe 2,54 (non scalata) vs 2,62 (RV21). | docs/EXECUTION_LEDGER.md#L8512-L8518 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "la scalatura per volatilità aiuta il momentum, non la mean reversion: queste regole rendono di più proprio nei giorni volatili"
- le regole restano a 1 micro.

## Prove

- runtime/proofs/size2/size2.json
