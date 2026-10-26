---
id: "res2-2"
titolo: "RES2-2 — oro: ritracciamento dell'initial balance (tradethatswing)"
data: "2026-10-19"
strumenti:
  - "MGC"
finestra: "MGC 1 minuto NinjaTrader, 1.986 sessioni 2019-01-28..2026-10-16 (2,65 milioni di barre)"
verdetto: "non confermata"
pubblicabilita: "avvertenza"
avvertenza: "(dati NinjaTrader solo aggregati)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L7975-L7980"
prove:
  - "runtime/proofs/res2/res2_2.json"
---

## Domanda

la strategia di ritracciamento del 25% dell'initial balance è profittevole?

## Metodo e rubrica

Regole originali della fonte, rubrica LAB-2. Rubrica prima: sì ("rubrica PRIMA dei dati", L7959).

## Esito

| Risultato | Fonte |
|---|---|
| "NON ADOTTATA". 1.075 trade | docs/EXECUTION_LEDGER.md#L7975-L7980 |
| scoperta 599 trade -0,10 USD, verifica 464 trade +12,79 USD (t 2,18), +11,07 con +1 tick | docs/EXECUTION_LEDGER.md#L7975-L7980 |
| per anno 2021 -5,16, 2025 +20,94, 2026 +18,41. | docs/EXECUTION_LEDGER.md#L7975-L7980 |

## Grafico

Serie per anno dal file di prova runtime/proofs/res2/res2_2.json (chiave anni).

## Cosa NON dice

- "strategia di regime (oro in tendenza e agitato), non stabile".

## Prove

- runtime/proofs/res2/res2_2.json
