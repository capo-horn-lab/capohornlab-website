---
id: "phase-2"
titolo: "PHASE-2 — le fasi per prevedere l'ampiezza e per escludere"
data: "2026-10-19"
strumenti:
  - "SPY"
  - "QQQ"
  - "MES"
  - "MNQ"
  - "MCL"
finestra: "SPY e QQQ 2006-2026 (giornalieri), MES, MNQ, MCL"
verdetto: "confermata"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L7699-L7702"
prove:
  - "runtime/proofs/phase2/phase2.json"
  - "runtime/proofs/phase2/oos.json"
---

## Domanda

le 12 fasi prevedono direzione o ampiezza della sessione successiva? Escludere le fasi in cui la strategia perdeva migliora il risultato?

## Metodo e rubrica

A) Spearman tra le medie di fase in scoperta e verifica; B) esclusione walk-forward, differenza appaiata (come TAIL-1). Rubrica prima: sì (L7680).

## Esito

| Risultato | Fonte |
|---|---|
| A) AMPIEZZA: "VALE": SPY rho 0,81, QQQ 0,87 (2006-2026), MES 0,78 (p 0,001), MNQ 0,90 (p 0,048), BH q≤0,10 | docs/EXECUTION_LEDGER.md#L7699-L7702 |
| es. | docs/EXECUTION_LEDGER.md#L7699-L7702 |
| SPY in verifica 49 bp in "rialzo calmo direzionale", 149 bp in "ribasso agitato direzionale". | docs/EXECUTION_LEDGER.md#L7699-L7702 |
| DIREZIONE: "non vale" (rho da -0,10 a +0,34, p≥0,15). | docs/EXECUTION_LEDGER.md#L7699-L7702 |
| B) 221 strategie: AIUTA (BH) in 76, differenza positiva in 173 | docs/EXECUTION_LEDGER.md#L7699-L7702 |
| "EDGE 0". | docs/EXECUTION_LEDGER.md#L7699-L7702 |

## Cosa NON dice

- "Le fasi non sono sbagliate (prevedono l'ampiezza); il limite è nelle strategie, che non hanno edge da preservare."

## Prove

- runtime/proofs/phase2/phase2.json
- runtime/proofs/phase2/oos.json
