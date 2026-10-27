---
id: "res2-1"
titolo: "RES2-1 — 26 strategie dalla ricerca web (articoli, blog, Reddit/forum), regole come pubblicate"
data: "2026-10-19"
strumenti:
  - "SPY"
  - "QQQ"
  - "MES"
  - "MNQ"
  - "MCL"
finestra: "SPY e QQQ giornalieri 2006-2026 (16 test, costo 2 bp), MES/MNQ/MCL intraday (10 test)"
verdetto: "senza verdetto nel registro"
pubblicabilita: "avvertenza"
avvertenza: "regole di terzi; dati Yahoo solo aggregati."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L7913-L7923"
prove:
  - "runtime/proofs/res2/res2_1.json"
---

## Domanda

le regole complete pubblicate da blog/paper (fine mese, Double 7s, Oops, Smash Day, pre-festivo, payday, FOMC, deriva pre-FOMC, gap, inside bar, volatility breakout di Williams, momentum EIA, box EIA) funzionano?

## Metodo e rubrica

Scoperta 60/verifica 40, placebo 200 (stesse durate), BH, trade minimi 50/30 (15/10 per regole rare); regole come pubblicate. Rubrica prima: sì (L7874).

## Esito

| Risultato | Fonte |
|---|---|
| "0 adottate su 26". | docs/EXECUTION_LEDGER.md#L7913-L7923 |
| D2 Double 7s: SPY +63,3 bp (t 2,61), QQQ +90,3 (t 2,93) "ma sotto i placebo con le stesse durate (p95 104,0 e 130,0): è il rialzo del mercato" | docs/EXECUTION_LEDGER.md#L7913-L7923 |
| D4 Smash Day: SPY +214,6 (t 3,73) ma 37/41 trade in scoperta | docs/EXECUTION_LEDGER.md#L7913-L7923 |
| I7 momentum EIA MCL -15,11 (t -3,06) | docs/EXECUTION_LEDGER.md#L7913-L7923 |
| I5 inside bar corto -4,81 (t -12,4: 21.570 segnali). | docs/EXECUTION_LEDGER.md#L7913-L7923 |
| I1 pre-FOMC MES 12 trade +73,0 USD (t 1,25). | docs/EXECUTION_LEDGER.md#L7913-L7923 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "restano positive ma deboli e in gran parte spiegate dal rialzo; nessuna batte i placebo. Restano informazione di calendario... non strategie da sole."

## Prove

- runtime/proofs/res2/res2_1.json
