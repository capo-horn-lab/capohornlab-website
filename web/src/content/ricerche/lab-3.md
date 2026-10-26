---
id: "lab-3"
titolo: "LAB-3 — libreria LAB-2 e ottimizzatore WFO-1 su contratti mai provati (MGC, M2K, M6E)"
data: "2026-10-19"
strumenti:
  - "MGC"
  - "M2K"
  - "M6E"
finestra: "MGC 2,65 milioni di barre, M2K 2,47 milioni, M6E 2,28 milioni (1 minuto NinjaTrader 2019-2026)"
verdetto: "non confermata"
pubblicabilita: "avvertenza"
avvertenza: "(dati NinjaTrader solo aggregati)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8199-L8203"
prove:
  - "runtime/proofs/lab3/lab3.json"
  - "runtime/proofs/wfo1/wfo_long_MGCL.json"
  - "runtime/proofs/wfo1/wfo_long_M2KL.json"
  - "runtime/proofs/wfo1/wfo_long_M6EL.json"
---

## Domanda

le strategie classiche e l'ottimizzatore hanno edge su oro, small cap ed euro?

## Metodo e rubrica

Test 1: 168 test (56 per strumento) con rubrica LAB-2; Test 2: WFO-1 invariato (3.832 genomi). Rubrica prima: sì (L8188).

## Esito

| Risultato | Fonte |
|---|---|
| Test 1: "0 adottate su 168". | docs/EXECUTION_LEDGER.md#L8199-L8203 |
| Test 2: "0 confermati su 3": MGC F3 -1,90 (t -0,77) | docs/EXECUTION_LEDGER.md#L8199-L8203 · docs/EXECUTION_LEDGER.md#L8230-L8234 |
| M2K F3 +1,21 (t 0,81) | docs/EXECUTION_LEDGER.md#L8230-L8234 |
| M6E F3 -1,84 (t -5,26). | docs/EXECUTION_LEDGER.md#L8199-L8203 · docs/EXECUTION_LEDGER.md#L8230-L8234 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "l'ottimizzatore WFO-1 non trova edge stabile su nessuno dei 6 strumenti provati (MES, MNQ, MCL, MGC, M2K, M6E)"
- l'oro premia i trend solo nel rialzo 2025-2026
- l'euro perde con ogni obiettivo (costi alti).

## Prove

- runtime/proofs/lab3/lab3.json
- runtime/proofs/wfo1/wfo_long_MGCL.json
- runtime/proofs/wfo1/wfo_long_M2KL.json
- runtime/proofs/wfo1/wfo_long_M6EL.json
