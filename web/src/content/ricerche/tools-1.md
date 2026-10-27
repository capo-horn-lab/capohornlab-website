---
id: "tools-1"
titolo: "TOOLS-1 / SHORT-1 / SETUP-1 — walk-forward del motore RizzoFlow su ES (ottobre 2026)"
data: "2026-10-15"
strumenti:
  - "ES"
finestra: "ES 12-26, 54 sessioni (2 agosto-15 ottobre 2026), 1.392 punti, 9 finestre (poi 7 finestre per SETUP-1)"
verdetto: "senza verdetto nel registro"
audit: {"stato": "nota", "id": ["SETUP-1"]}
pubblicabilita: "avvertenza"
avvertenza: "costi PROVVISORI dichiarati."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L5558-L5559"
prove:
  - "runtime/proofs/tools/walkforward.json"
  - "runtime/proofs/tools/walkforward-compatto.json"
  - "runtime/proofs/tools/walkforward-adattiva.json"
---

## Ritiri e correzioni

- SETUP-1: prima misura (+21.82/trade su 85 trade) contava due volte lo stesso trade; corretta a -14.53 USD/trade su 88 (L5950-L5955).

## Domanda

il decisore del motore (BUY con bracket per fase, filtro RizzoFlow) e i setup adattivi hanno vantaggio fuori campione?

## Metodo e rubrica

Walk-forward con selezione su sessioni passate e prova fuori campione; base rate "entrate a ogni punto senza scelta"; costi ≈32 USD a trade (2 x 3,50 commissioni + 1 tick d'ingresso + 1 tick di slittamento). Rubrica prima: sì, a livello di piano (TOOLS-1 e SETUP-1 registrati prima; nessun BH).

## Esito

| Risultato | Fonte |
|---|---|
| TOOLS-1: "FUORI CAMPIONE 284 trade, vinti 35.9%, medio -25.44 USD, netto -7225.50, drawdown 7647.50, t-stat -2.68; base rate 1132 trade, 34.6%, medio -30.48, netto -34499, t -6.78" | docs/EXECUTION_LEDGER.md#L5558-L5559 · docs/EXECUTION_LEDGER.md#L5557-L5557 |
| "il filtro RizzoFlow riduce la perdita per trade, non la inverte". | docs/EXECUTION_LEDGER.md#L5558-L5559 · docs/EXECUTION_LEDGER.md#L5889-L5898 · docs/EXECUTION_LEDGER.md#L5952-L5955 |
| SHORT-1 (due lati, forma compatta): 300 trade, -21.04 USD/trade, t -2.16 | docs/EXECUTION_LEDGER.md#L5889-L5898 |
| BUY 154 a -16.33 (t -1.25), SELL 146 a -26.01 (t -1.78) | docs/EXECUTION_LEDGER.md#L5889-L5898 |
| base rate BUY -30.62 (t -6.88), SELL -32.03 (t -7.14). | docs/EXECUTION_LEDGER.md#L5889-L5898 |
| staffa fissa 2 ATR/2R 104 trade -51.95 (t -0.74) | docs/EXECUTION_LEDGER.md#L5889-L5898 · docs/EXECUTION_LEDGER.md#L5952-L5955 |
| cella migliore BREAK_RETEST/con 15 trade +183.0 (t 1.41). | docs/EXECUTION_LEDGER.md#L5889-L5898 · docs/EXECUTION_LEDGER.md#L5952-L5955 |

1 righe della scheda non riportate: la prova citata non le contiene.

## Cosa NON dice

- "entrambe le direzioni a caso perdono circa i costi"
- "Nessun vantaggio dimostrato; il segno del totale cambia con pochi trade"
- "Lo short non produce un vantaggio: non lo dimostra né lo esclude".
- Prima misura di SETUP-1 corretta per doppio conteggio (+21.82/trade su 85 trade -> -14.53 su 88).

## Prove

- runtime/proofs/tools/walkforward.json
- runtime/proofs/tools/walkforward-compatto.json
- runtime/proofs/tools/walkforward-adattiva.json
- runtime/proofs/tools-scorecard-*.json
