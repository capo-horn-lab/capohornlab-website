---
id: "phase-3"
titolo: "PHASE-3 / PHASE-3-OOS / PHASE-2-OOS / SIZE-1 — quante fasi usare, previsione dell'ampiezza su dati mai usati, dimensione per fase"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "MCL"
  - "MGC"
finestra: "MES, MNQ, MCL, MGC; PHASE-3: 7 schemi x 2 librerie x 3 strumenti = 42 test; PHASE-2-OOS: sessioni 2025-2026; SIZE-1: 221 strategie."
verdetto: "confermato · non confermato"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8009-L8015"
prove:
  - "runtime/proofs/phase3/phase3.json"
  - "runtime/proofs/phase3/oos_mes.json"
  - "runtime/proofs/phase2/oos.json"
  - "runtime/proofs/size1/size1.json"
---

## Domanda

meno fasi (2-3) aiutano l'ottimizzatore? La fase prevede l'ampiezza su dati mai usati? Scalare la dimensione sull'ampiezza attesa migliora lo Sharpe?

## Metodo e rubrica

Stessi genomi di PARAM-1/WFO-1, F3 prudente, placebo, BH q≤0,10. Rubrica prima: sì (L7945, L8017, L8028, L8048).

## Esito

| Risultato | Fonte |
|---|---|
| PHASE-3: "2 confermati su 42, entrambi MES con la libreria WFO-1": S2v +7,59 USD/sessione t 2,75 | docs/EXECUTION_LEDGER.md#L8009-L8015 |
| S2c +10,56 t 3,00 | docs/EXECUTION_LEDGER.md#L8009-L8015 |
| senza fasi S0 +2,40 (t 1,09) | docs/EXECUTION_LEDGER.md#L8009-L8015 |
| 12 fasi S12 -3,34. | docs/EXECUTION_LEDGER.md#L8009-L8015 |
| PHASE-3-OOS (MES 2025-01..2026-10, 460 sessioni): "NON confermato": S2v +1,83 (t 0,37), S2c +0,34 (t 0,07). | docs/EXECUTION_LEDGER.md#L8036-L8046 |
| PHASE-2-OOS: "CONFERMATO su MES e MNQ, non su MGC": MES rho 0,939 (460 sessioni, 10 fasi) agitato/calmo 1,50 | docs/EXECUTION_LEDGER.md#L8036-L8046 |
| MNQ rho 0,952 agitato/calmo 1,69 | docs/EXECUTION_LEDGER.md#L8036-L8046 |
| MGC rho 0,285 (p 0,25). | docs/EXECUTION_LEDGER.md#L8036-L8046 |
| SIZE-1: "NON confermato": Sharpe migliore in 134 su 221 (60,6%, p del segno 0,001) ma giorno peggiore mediano -367,13 contro -357,80. | docs/EXECUTION_LEDGER.md#L8058-L8061 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "la fase di oggi (nota alla chiusura di ieri) dice quanto si muovera' l'indice domani"...
- "non la direzione"

## Prove

- runtime/proofs/phase3/phase3.json
- runtime/proofs/phase3/oos_mes.json
- runtime/proofs/phase2/oos.json
- runtime/proofs/size1/size1.json
