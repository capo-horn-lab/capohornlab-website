---
id: "vixts-1"
titolo: "VIXTS-1 — struttura a termine del VIX (VIX/VIX3M) come regime e protezione"
data: "2026-10-19"
strumenti:
  - "SPY"
  - "QQQ"
finestra: "SPY/QQQ 2009-09..2026-10 (4.295 giorni, 324 in backwardation)"
verdetto: "non confermato"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L7990-L7994"
prove:
  - "runtime/proofs/vixts1/vixts1.json"
---

## Domanda

giorni dopo backwardation (VIX/VIX3M>1) hanno rendimenti peggiori o ampiezza maggiore? Evitarli protegge le strategie?

## Metodo e rubrica

Test 1 direzione, Test 2 ampiezza (descrittivo), Test 3 protezione P7 sui 221 trade-set. Rubrica prima: sì (L7982).

## Esito

| Risultato | Fonte |
|---|---|
| Direzione: "NON confermato" (SPY backwardation/contango scoperta +16,83 / +4,45 bp t 0,99, verifica +9,68 / +6,25 t 0,12). | docs/EXECUTION_LEDGER.md#L7990-L7994 |
| Ampiezza: "in backwardation il giorno dopo è 2-2,7 volte più ampio (SPY 214 contro 94 bp in scoperta, 304 contro 112 in verifica)". | docs/EXECUTION_LEDGER.md#L7990-L7994 |
| Protezione P7: aiuta in 18 casi su 221 (BH), differenza positiva in 162 su 221. | docs/EXECUTION_LEDGER.md#L7990-L7994 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- Il segno è semmai positivo (rimbalzo dopo il panico), non "stare fuori".

## Prove

- runtime/proofs/vixts1/vixts1.json
