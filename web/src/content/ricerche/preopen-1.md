---
id: "preopen-1"
titolo: "PREOPEN-1 — breakout del range di pre-apertura su MNQ"
data: "2026-10-19"
strumenti:
  - "MNQ"
  - "NQ"
finestra: "MNQ base 1 s 2023-01..2024-08-15 + NQ 1m fine 2024 + MNQ 12-26 2026"
verdetto: "non confermata"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L7678-L7678"
prove:
  - "runtime/proofs/preopen1/preopen1.json"
---

## Domanda

trend-following sul primo limite sfondato del range di pre-apertura (R1 notte Globex 18:00-9:30 ET, R2 pre-mercato 8:00-9:30 ET), stop 150 tick, trailing, ha edge?

## Metodo e rubrica

4 test (R1/R2 x trailing T1/T2), rubrica LAB-2 (scoperta 60/verifica 40, placebo 200, BH). Rubrica prima: sì (richiesta del proprietario, L7645).

## Esito

| Risultato | Fonte |
|---|---|
| "0 adottate su 4". | docs/EXECUTION_LEDGER.md#L7678-L7678 |
| MNQ 2023-2024 verifica: R1 notte T1 -1,19 USD (151 trade, t -0,18), R2 T2 -9,47 (t -1,53) | docs/EXECUTION_LEDGER.md#L7678-L7678 |
| +1 tick tutte negative. | docs/EXECUTION_LEDGER.md#L7678-L7678 |
| Dati mai usati: NQ 1m fine 2024 positivi (R2 T1 +20,99 t 2,02), MNQ 2026 negativi (da -20,68 a -32,09; R2 T2 t -2,36). | docs/EXECUTION_LEDGER.md#L7678-L7678 |
| "Esiti discordi tra periodi: nessun vantaggio stabile." | docs/EXECUTION_LEDGER.md#L7678-L7678 |

## Cosa NON dice

- —

## Prove

- runtime/proofs/preopen1/preopen1.json
