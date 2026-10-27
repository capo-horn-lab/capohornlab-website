---
id: "sent-2"
titolo: "SENT-2 — un motore di sentiment veritiero (TV, regressione logistica, LightGBM)"
data: "2026-10-18"
strumenti:
  - "MES"
  - "ES"
  - "MNQ"
  - "NQ"
  - "MCL"
  - "CL"
finestra: "MES (ES 1m), MNQ (NQ 1s), MCL (CL 1s); 5 m, 30 m, 1 h, 4 h, giornaliero (45 combinazioni motore x strumento x timeframe)"
verdetto: "senza verdetto nel registro"
pubblicabilita: "avvertenza"
avvertenza: "dati licenziati solo aggregati."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L6704-L6728"
prove:
  - "runtime/proofs/sent2/sent2.json"
---

## Domanda

dopo "strong sell" a 5 m il mercato scende davvero nei 5 minuti successivi?

## Metodo e rubrica

Tre motori (TV, LOG, LGB), scoperta 60% / verifica 40%, 4 criteri di "veritiero" (verso, ordine Spearman con BH q≤0,10 su 45, calibrazione ±0,03, periodi mai usati). Rubrica prima: sì (L6676+).

## Esito

| Risultato | Fonte |
|---|---|
| "veritieri 2 su 45, LightGBM a 5 minuti su MES e su MCL". | docs/EXECUTION_LEDGER.md#L6704-L6728 |
| TradingView rating non veritiero | docs/EXECUTION_LEDGER.md#L6704-L6728 |
| a 5 m è al contrario (IC -0,022 MES, -0,018 MNQ e MCL; dopo strong sell sale nel 53,8% MES). | docs/EXECUTION_LEDGER.md#L6704-L6728 |
| LGB MES 5 m verifica: strong sell 773 casi scende nel 60,1% (promesso 61,3%) | docs/EXECUTION_LEDGER.md#L6704-L6728 |
| strong buy 1.123 casi 60,6% | docs/EXECUTION_LEDGER.md#L6704-L6728 |
| IC 0,043 (t 17,4). | docs/EXECUTION_LEDGER.md#L6704-L6728 |
| Spostamento medio 0,1-0,4 punti base contro costo 1-1,5 punti base. | docs/EXECUTION_LEDGER.md#L6704-L6728 |

## Cosa NON dice

- "vero ma non tradabile da solo"
- 30 m-giornaliero: nessun motore veritiero.

## Prove

- runtime/proofs/sent2/sent2.json
- runtime/models/sentiment/
