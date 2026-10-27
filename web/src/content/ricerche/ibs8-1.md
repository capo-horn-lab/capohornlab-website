---
id: "ibs8-1"
titolo: "IBS8-1 — la variante IBS 0,20/0,80/8 contro la regola in carta 0,20/0,90/5"
data: "2026-10-19"
strumenti: []
finestra: "4 micro 2019-05-06..2026-10-19; esame di controllo 2024-2026"
verdetto: "non confermata"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9441-L9452"
prove:
  - "runtime/proofs/ibs81/ibs81.json"
---

## Domanda

DAILY-1 ha trovato la variante 0,80/8 "confermata" su MES e MYM; è un edge o rumore di selezione?

## Metodo e rubrica

Confronto accoppiato per giorno d'ingresso, BH sulle 44 p, placebo 200 (seme 17), sensibilità 12 celle; CONFERMATA se vale su ≥3 strumenti su 4. Rubrica prima: sì (L9382).

## Esito

| Risultato | Fonte |
|---|---|
| "NON CONFERMATA su tutti e quattro, la variante 0,20 / 0,80 / 8 non merita di affiancare la regola in carta": BH q minimo 0,672, "0 su 4, serviva 3 su 4" | docs/EXECUTION_LEDGER.md#L9441-L9452 |
| MES D verifica +9,3 USD per giorno (t 0,28) | docs/EXECUTION_LEDGER.md#L9441-L9452 |
| MNQ D +87,1 USD (t 1,26) | docs/EXECUTION_LEDGER.md#L9441-L9452 |
| M2K D -10,5 (t -0,63) | docs/EXECUTION_LEDGER.md#L9441-L9452 |
| MYM D +16,5 (t 0,78) | docs/EXECUTION_LEDGER.md#L9441-L9452 |
| esame 2024-2026: D di V negativa su MES -28,1 USD, M2K -23,8, MYM -14,7. | docs/EXECUTION_LEDGER.md#L9441-L9452 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Lettura e limiti (dal registro)

- "è rumore di selezione"
- "è la firma del rumore di selezione, non di una zona robusta"
- la regola H-NEXT-6 resta 0,20 / 0,90 / 5.

## Prove

- runtime/proofs/ibs81/ibs81.json
