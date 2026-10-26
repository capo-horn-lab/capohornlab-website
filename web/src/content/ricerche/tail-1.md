---
id: "tail-1"
titolo: "TAIL-1 / TAIL-1-OOS / TAIL-1-NT — i giorni negativissimi e le protezioni di rischio P1-P5"
data: "2026-10-18"
strumenti:
  - "MES"
  - "MNQ"
  - "MCL"
  - "NQ"
finestra: "tutte le strategie LAB-1/LAB-2/ICT con ≥200 trade in scoperta su MES, MNQ, MCL; dati mai usati: NQ 1m 16/08-31/12/2024 e export NinjaTrader MES/MNQ 12-26 2026"
verdetto: "confermata"
pubblicabilita: "avvertenza"
avvertenza: "caso con ~20-39 sessioni per caso; dati licenziati solo aggregati."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L7360-L7360"
prove:
  - "runtime/proofs/tail1/tail1.json"
  - "runtime/proofs/tail1/oos.json"
  - "runtime/proofs/tail1/nt2026.json"
---

## Domanda

un limite di perdita giornaliero (P4) o lo stop dopo 2 perdite (P5) riducono le perdite dei giorni peggiori?

## Metodo e rubrica

1.345 confronti (test x varianti x protezioni), differenza appaiata del P&L giornaliero in verifica, BH q≤0,10; protezioni P1 eventi macro, P2 VIX alto, P3 dopo shock, P4, P5, regole fisse non ottimizzate. Rubrica prima: sì (L7323, L7363, L7453).

## Esito

| Risultato | Fonte |
|---|---|
| TAIL-1: "In mediana i giorni sotto il 5 percentile pesano il 15% delle perdite di verifica" | docs/EXECUTION_LEDGER.md#L7360-L7360 |
| AIUTANO P1 22, P2 37, P3 19, P4 110, P5 115 | docs/EXECUTION_LEDGER.md#L7360-L7360 |
| "EDGE REALE (protetta e anche positiva con t >= 2): 1, MNQ noise area griglia 5m intera con P5". | docs/EXECUTION_LEDGER.md#L7360-L7360 |
| TAIL-1-OOS: "NON confermata" (NQ fine 2024: 56 sessioni, senza +29,97 USD/sessione t 1,14, con P5 +36,49 t 1,46, differenza +6,52 t 0,77). | docs/EXECUTION_LEDGER.md#L7382-L7382 |
| TAIL-1-NT: "le protezioni VALGONO in generale": P4 differenza positiva in 14 casi su 15 (p 0,0004), media +29,3 USD per sessione | docs/EXECUTION_LEDGER.md#L7382-L7382 · docs/EXECUTION_LEDGER.md#L7360-L7360 · docs/EXECUTION_LEDGER.md#L7474-L7474 |
| P5 13 su 13 (p 0,0002), media +33,6 | docs/EXECUTION_LEDGER.md#L7474-L7474 |
| "Non creano un edge": con protezione positive 5 strategie su 28 (senza: 1). | docs/EXECUTION_LEDGER.md#L7360-L7360 · docs/EXECUTION_LEDGER.md#L7382-L7382 · docs/EXECUTION_LEDGER.md#L7474-L7474 |

## Cosa NON dice

- Le protezioni riducono le perdite ma non creano edge
- P4 e P5 diventano regole di rischio predefinite (task L13)
- default max_consecutive_losses da 4 a 2.

## Prove

- runtime/proofs/tail1/tail1.json
- runtime/proofs/tail1/oos.json
- runtime/proofs/tail1/nt2026.json
