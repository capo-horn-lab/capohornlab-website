---
id: "mr-2"
titolo: "MR-2 — la mean reversion di breve fuori dagli indici USA"
data: "2026-10-19"
strumenti:
  - "FESX"
  - "FDXM"
  - "MGC"
  - "M6E"
finestra: "FESX+FDXM, MGC, M6E 2019-2026; 36 test (12 regole x 3 gruppi)"
verdetto: "verdetto non estratto: vedi Esito"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8434-L8438"
prove:
  - "runtime/proofs/mr2/mr2.json"
---

## Domanda

la famiglia di MR-1 funziona anche su Europa, oro, euro?

## Metodo e rubrica

≥30 trade, t giorni≥2, placebo, +1 tick, DSR(N=36)≥0,95, BH q≤0,10. Rubrica prima: sì (L8424).

## Esito

| Risultato | Fonte |
|---|---|
| "0 confermate su 36." | docs/EXECUTION_LEDGER.md#L8434-L8438 |
| Europa: 7 regole positive su 12, nessuna con t giorni≥2 (3WEAK 76 trade +26,8 bp, t giorni 1,85; TT 93 trade +29,0, t 1,09) | docs/EXECUTION_LEDGER.md#L8434-L8438 |
| oro 9 positive su 12 tutte deboli (PCTB 21 trade +87,0, t 1,61) | docs/EXECUTION_LEDGER.md#L8434-L8438 |
| euro 3 su 12. | docs/EXECUTION_LEDGER.md#L8434-L8438 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Lettura e limiti (dal registro)

- "forte e significativa solo sugli indici azionari USA... in Europa ha lo stesso segno ma è debole... su oro ed euro è assente. Il bot la usa solo sui micro USA."

## Prove

- runtime/proofs/mr2/mr2.json
