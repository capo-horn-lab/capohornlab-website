---
id: "mr-1"
titolo: "MR-1 — la famiglia dell'IBS: 12 regole di mean reversion pubblicate e il comitato"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "M2K"
  - "MYM"
  - "SPY"
  - "QQQ"
finestra: "MES, MNQ, M2K, MYM NinjaTrader 2019-2026 (insieme \"future\") e SPY+QQQ 2006-2026 (ETF)"
verdetto: "confermata"
pubblicabilita: "avvertenza"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8329-L8344"
prove:
  - "runtime/proofs/mr1/mr1.json"
  - "runtime/proofs/mr1/mr1_adj.json"
---

## Domanda

le regole pubblicate di mean reversion di breve (RSI2, CUMRSI, R3, 3DHL, PCTB, WR2, Turnaround Tuesday, 3DOWN, 3WEAK, BB20, COMITATO) funzionano oltre l'IBS?

## Metodo e rubrica

12 regole x 2 gruppi = 24 test (nel testo "22" corretto a 24); ≥30 trade, media>0, t≥2, sopra il p95 di 200 placebo, +1 tick, BH q≤0,10 sui 24; quota di trade coincidenti con IBS<0,2. Rubrica prima: sì (L8307).

## Esito

| Risultato | Fonte |
|---|---|
| "16 confermati su 24 test". | docs/EXECUTION_LEDGER.md#L8329-L8344 |
| Es. (bp per trade): R1a RSI2<5 future 139 trade +47,7 (t 2,97, p95 17,6) CONFERMATA, ETF +39,4 sotto il p95 40,8 | docs/EXECUTION_LEDGER.md#L8329-L8344 |
| TT future 161 trade +61,5 (t 3,88, p95 37,1) e ETF 252 +68,4 (t 4,81, p95 19,6) CONFERMATE | docs/EXECUTION_LEDGER.md#L8329-L8344 |
| 3WEAK future 189 +53,5 (t 5,05, placebo p95 1,5) | docs/EXECUTION_LEDGER.md#L8329-L8344 |
| WR2 future 576 +48,0 (t 5,78) "ma quota IBS 0,97-0,98: è l'IBS" | docs/EXECUTION_LEDGER.md#L8329-L8344 |
| 3DOWN future 678 +8,4 (t 2,38). | docs/EXECUTION_LEDGER.md#L8329-L8344 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "un fenomeno di famiglia, non una regola isolata... non sono edge indipendenti: si sovrappongono all'IBS (dal 27% al 98% dei trade) e vivono degli stessi giorni di calo. I dati erano già stati usati per l'IBS."
- Prova in avanti H-NEXT-7 (nessun esito ancora).

## Prove

- runtime/proofs/mr1/mr1.json
- runtime/proofs/mr1/mr1_adj.json
