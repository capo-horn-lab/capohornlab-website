---
id: "mr-1-adj"
titolo: "MR-1-ADJ — MR-1 con segnali sui prezzi raccordati"
data: "2026-10-19"
strumenti: []
finestra: "stessi test di MR-1 con segnali calcolati sulla serie raccordata ai cambi di contratto (esecuzioni sui prezzi grezzi)"
verdetto: "confermata"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9023-L9023"
prove:
  - "runtime/proofs/mr1/mr1_adj.json"
---

## Domanda

la correzione dell'audit cambia i 16 confermati?

## Metodo e rubrica

Rubrica identica a MR-1. Rubrica prima: sì (L9019).

## Esito

| Risultato | Fonte |
|---|---|
| "le conferme di MR-1 REGGONO": tutte le 16 restano confermate e se ne aggiunge una (PCTB future: da +43,2 bp t 1,79 a +66,0 t 2,74): 17 su 24 | docs/EXECUTION_LEDGER.md#L9023-L9023 |
| R1a +47,7 -> +40,5 (t 2,45) | docs/EXECUTION_LEDGER.md#L9023-L9023 |
| R1b +38,1 -> +25,4 (t 2,24) | docs/EXECUTION_LEDGER.md#L9023-L9023 |
| TT +61,5 -> +63,8 (140 trade). | docs/EXECUTION_LEDGER.md#L9023-L9023 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- Quando una conferma cambia, vale MR-1-ADJ.

## Prove

- runtime/proofs/mr1/mr1_adj.json
