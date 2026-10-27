---
id: "poly-1"
titolo: "POLY-1 — probabilità Polymarket sulla Fed come dato per ES/NQ"
data: "2026-10-19"
strumenti:
  - "SPY"
  - "QQQ"
finestra: "API pubbliche Polymarket (16 riunioni FOMC da dicembre 2024, 292 giorni, 201 con rendimenti SPY/QQQ)"
verdetto: "verdetto non estratto: vedi Esito"
pubblicabilita: "avvertenza"
avvertenza: "dati pubblici Polymarket"
fonte_ledger: "docs/EXECUTION_LEDGER.md#L7451-L7451"
prove:
  - "runtime/proofs/poly1/poly1.json"
---

## Domanda

la variazione giornaliera della probabilità di taglio prevede il rendimento di SPY/QQQ?

## Metodo e rubrica

Spearman con Newey-West lag 1, segno uguale nelle due metà, BH q≤0,10 su 2 strumenti; prova descrittiva stesso giorno e sull'entropia. Rubrica prima: sì (L7428).

## Esito

| Risultato | Fonte |
|---|---|
| "NON AIUTA": dp di ieri contro rendimento di oggi rho +0,039 (t 0,52) SPY, +0,042 (t 0,60) QQQ, q 0,61. | docs/EXECUTION_LEDGER.md#L7451-L7451 |
| Stesso giorno rho -0,10 / -0,12 (t -1,3 / -1,6) ("reazione, non previsione") | docs/EXECUTION_LEDGER.md#L7451-L7451 |
| entropia contro \\|movimento\\| del giorno della riunione rho +0,29 su 13 riunioni (descrittivo). | docs/EXECUTION_LEDGER.md#L7451-L7451 |

## Lettura e limiti (dal registro)

- "Entra solo come contesto descrittivo."

## Prove

- runtime/proofs/poly1/poly1.json
- runtime/research/polymarket/
