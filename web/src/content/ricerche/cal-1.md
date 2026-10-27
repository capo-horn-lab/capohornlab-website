---
id: "cal-1"
titolo: "CAL-1 (ottimizzatore, L27) — il calendario come filtro dei genomi"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "MCL"
finestra: "(non è il CAL-1 di calibrazione del 4/10, che è infrastruttura); MES, MNQ, MCL"
verdetto: "verdetto non estratto: vedi Esito"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8148-L8151"
prove:
  - "runtime/proofs/cal1/cal1.json"
---

## Domanda

filtri di calendario (senza eventi FOMC/CPI/NFP; solo fine mese) migliorano l'ottimizzatore WFO-1?

## Metodo e rubrica

Libreria WFO-1 con 2 filtri per genoma, F3 prudente, BH q≤0,10 su 3. Rubrica prima: sì (L8120).

## Esito

| Risultato | Fonte |
|---|---|
| "0 confermati su 3." | docs/EXECUTION_LEDGER.md#L8148-L8151 |
| Con i filtri di calendario: MES +3,85 (t 1,73) contro +4,09 (t 1,54) senza | docs/EXECUTION_LEDGER.md#L8148-L8151 |
| MNQ +34,37 (t 2,72) contro +36,01 (t 2,88) | docs/EXECUTION_LEDGER.md#L8148-L8151 |
| MCL -0,77 contro -0,31. | docs/EXECUTION_LEDGER.md#L8148-L8151 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Lettura e limiti (dal registro)

- "il calendario non aggiunge nulla all'ottimizzatore... Coerente con RES2-1: gli effetti di calendario sono deboli."

## Prove

- runtime/proofs/cal1/cal1.json
