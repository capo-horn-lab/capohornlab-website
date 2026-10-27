---
id: "bc-1"
titolo: "BC-1 — strategie intraday, di volatilità e cross-asset dalle schede B e C"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "SPY"
  - "QQQ"
  - "FESX"
  - "FDXM"
  - "VIX"
finestra: "MES, MNQ, SPY, QQQ, FESX/FDXM; 12 test eseguiti (VWAP trend, momentum del resto del giorno, primo VIX spike, VIX Stretch, inversione overnight, settimana OpEx, USA->Europa, petrolio, rame/oro, fade del VWAP)"
verdetto: "verdetto non estratto: vedi Esito"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8419-L8422"
prove:
  - "runtime/proofs/bc1/bc1.json"
---

## Domanda

reggono i costi reali?

## Metodo e rubrica

t sui giorni≥2, placebo 200, DSR con N=13. Rubrica prima: sì (L8401).

## Esito

| Risultato | Fonte |
|---|---|
| "0 confermati." | docs/EXECUTION_LEDGER.md#L8419-L8422 |
| Intraday tutti negativi dopo i costi: B1 VWAP trend MES+MNQ 62.351 trade -1,02 bp (t giorni -7,49) | docs/EXECUTION_LEDGER.md#L8419-L8422 |
| B19 fade VWAP 8.607 trade -3,42 (t giorni -5,14) | docs/EXECUTION_LEDGER.md#L8419-L8422 |
| B4 USA->Europa 3.544 trade -3,20 (t giorni -4,05). | docs/EXECUTION_LEDGER.md#L8419-L8422 |
| Mensili/volatilità ETF positivi ma sotto i placebo: C6 VIX spike 21 sessioni 79 trade +115,9 (t 1,87, p95 175,1). | docs/EXECUTION_LEDGER.md#L8419-L8422 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Lettura e limiti (dal registro)

- "Nessun edge intraday sugli indici dopo commissioni e 1 tick"
- le idee mensili sono "il rialzo di fondo comprato in giorni a caso con una storia".

## Prove

- runtime/proofs/bc1/bc1.json
