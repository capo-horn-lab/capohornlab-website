---
id: "ict-1"
titolo: "ICT-1 e ICT-1-OOS — modelli ICT (2022 model, OTE, Power of 3, NDOG/NWOG)"
data: "2026-10-18"
strumenti:
  - "MES"
  - "MNQ"
  - "MCL"
  - "NQ"
finestra: "MES, MNQ, MCL (1m, 5m); fuori campione NQ 1m 16/08-31/12/2024 e export NinjaTrader 2026"
verdetto: "senza verdetto nel registro"
pubblicabilita: "avvertenza"
avvertenza: "(regole \"ICT\" implementate in forma meccanica propria: non equivale al metodo discrezionale)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L7089-L7102"
prove:
  - "runtime/proofs/ict1/ict1.json"
  - "runtime/proofs/ict1/oos.json"
---

## Domanda

i modelli ICT hanno vantaggio netto dei costi?

## Metodo e rubrica

Rubrica di adozione = LAB-2 (scoperta 60/verifica 40, placebo 200, BH q≤0,10 su 24 test, +1 tick); poi 5 ipotesi su dati mai usati. Rubrica prima: sì (L7011, L7104).

## Esito

| Risultato | Fonte |
|---|---|
| ICT-1: "0 ADOTTATE su 24 test" | docs/EXECUTION_LEDGER.md#L7089-L7102 |
| MES 2022 model 1m verifica -5,25 USD t -3,01 | docs/EXECUTION_LEDGER.md#L7089-L7102 |
| MNQ 2022 model 5m 158/90 trade +4,89 / +23,69 t 1,99 (a un passo). | docs/EXECUTION_LEDGER.md#L7089-L7102 |
| ICT-1-OOS: "0 confermate su 5, tutte negative sui dati nuovi" (NQ fine 2024: 2022 model 5m 54 trade -7,08 t -0,43; OTE 1m 46 trade -19,71 t -2,43). | docs/EXECUTION_LEDGER.md#L7089-L7102 · docs/EXECUTION_LEDGER.md#L7175-L7185 |

## Cosa NON dice

- "I modelli ICT non reggono fuori campione."
- Potenza bassa (~95 e 55 sessioni).

## Prove

- runtime/proofs/ict1/ict1.json
- runtime/proofs/ict1/oos.json
