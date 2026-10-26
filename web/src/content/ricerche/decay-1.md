---
id: "decay-1"
titolo: "DECAY-1 — l'edge delle regole confermate si sta riducendo nel tempo?"
data: "2026-10-19"
strumenti:
  - "SPY"
  - "QQQ"
finestra: "12 regole di MR-1-ADJ sui 4 micro 2019-2026 e su SPY/QQQ 2006-2026 + IBS-NT; 25 prove"
verdetto: "non confermata"
pubblicabilita: "avvertenza"
avvertenza: "\"non significativo\" non è assenza di decadimento (potenza)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9053-L9053"
prove:
  - "runtime/proofs/decay1/decay1.json"
---

## Domanda

decadimento dell'edge?

## Metodo e rubrica

Media prima/seconda metà e pendenza OLS del P&L per trade, BH; DECADIMENTO se pendenza<0 con q≤0,10 e metà recente < metà dell'altra. Rubrica prima: sì (L9048).

## Esito

| Risultato | Fonte |
|---|---|
| "NESSUN decadimento significativo (25 prove, q minimo 0,90)". | docs/EXECUTION_LEDGER.md#L9053-L9053 |
| In direzione: IBS-NT 942 trade prima metà +49,2 bp, seconda +29,8, pendenza -5,0 bp/anno (p 0,13) | docs/EXECUTION_LEDGER.md#L9053-L9053 |
| TT future +112,9 -> +14,7 (140 trade, p 0,16) | docs/EXECUTION_LEDGER.md#L9053-L9053 |
| ETF stabili o in crescita (WR2 +41,7 -> +62,9). | docs/EXECUTION_LEDGER.md#L9053-L9053 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- Valore atteso prudente = media della metà recente (IBS-NT +29,8 bp per trade invece di +39,5).

## Prove

- runtime/proofs/decay1/decay1.json
