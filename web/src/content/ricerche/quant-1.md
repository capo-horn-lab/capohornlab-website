---
id: "quant-1"
titolo: "QUANT-1 — combinazione di segnali deboli (ridge/LightGBM), walk-forward e soglia di costo"
data: "2026-10-17"
strumenti:
  - "MNQ"
  - "MCL"
  - "MES"
  - "NQ"
finestra: "MNQ, MCL, MES, 5 minuti, orizzonte 60 minuti; periodo mai usato: NQ 1m 16/08-31/12/2024 e export NinjaTrader 2026"
verdetto: "senza verdetto nel registro"
pubblicabilita: "avvertenza"
avvertenza: "dati licenziati solo aggregati; costi NinjaTrader piano Free."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L6435-L6444"
prove:
  - "runtime/proofs/quant1/quant1.json"
  - "runtime/proofs/quant1/quant1-partial-run1.json"
  - "runtime/proofs/quant1/vnpy_check.json"
  - "docs/research/QUANT1_SEGNALI_DEBOLI_2026-10-17.md"
---

## Domanda

combinare molti segnali deboli in un modello supera il costo di andata e ritorno?

## Metodo e rubrica

Ridge (alpha fisso) e LightGBM-Alpha158 (qlib), walk-forward con purging/embargo, entrata se \|previsione\| > k x costo, 17 test, BH su 17; criteri (a)-(g). Rubrica prima: sì ("Progetto congelato PRIMA dei risultati", L6343+).

## Esito

| Risultato | Fonte |
|---|---|
| "0 su 17 adottabili". | docs/EXECUTION_LEDGER.md#L6435-L6444 |
| MNQ positiva nel walk-forward in tutte le varianti (migliore X: 1498 trade +4,66 USD t 1,69, +1 tick +3,66, q 0,48), ma sull'export NinjaTrader 2026 A/X/V tra -15,62 e -28,12 USD a trade | docs/EXECUTION_LEDGER.md#L6435-L6444 |
| MES negativa (A k1 4322 trade -3,12 t -3,08) | docs/EXECUTION_LEDGER.md#L6435-L6444 |
| MCL negativa. | docs/EXECUTION_LEDGER.md#L6435-L6444 |
| IC fuori campione 0,02-0,035 (metodo corretto). | docs/EXECUTION_LEDGER.md#L6435-L6444 |
| Controllo vnpy: 1996 trade contro 1995, -1,74 contro -1,94 USD netti a trade. | docs/EXECUTION_LEDGER.md#L6435-L6444 |

## Cosa NON dice

- Movimento previsto sotto il costo.

## Prove

- runtime/proofs/quant1/quant1.json
- runtime/proofs/quant1/quant1-partial-run1.json
- runtime/proofs/quant1/vnpy_check.json
- docs/research/QUANT1_SEGNALI_DEBOLI_2026-10-17.md
