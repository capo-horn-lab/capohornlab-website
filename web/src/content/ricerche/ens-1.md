---
id: "ens-1"
titolo: "ENS-1 e LASTHALF-OOS — insieme lineare di segnali semplici; momentum dell'ultima mezz'ora fuori campione"
data: "2026-10-19"
strumenti:
  - "SPY"
  - "QQQ"
  - "MES"
  - "MNQ"
  - "M2K"
  - "MYM"
finestra: "ENS-1: SPY e QQQ 2006-2026 (previsioni dal 2010); LASTHALF-OOS: MES, MNQ, M2K, MYM 2019-2026"
verdetto: "confermato"
pubblicabilita: "avvertenza"
avvertenza: "R² dello 0,3-0,4%: effetto minuscolo"
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8481-L8490"
prove:
  - "runtime/proofs/ens1/ens1.json"
  - "runtime/proofs/lasthalf/lasthalf.json"
---

## Domanda

una media di regressioni semplici sui segnali della famiglia (IBS, RSI2, lunedì in calo, 3 giorni deboli, overnight) prevede il rendimento del giorno dopo meglio della media storica? Il rendimento di inizio/fine giornata prevede l'ultima mezz'ora (R² fuori campione)?

## Metodo e rubrica

R² fuori campione contro la media espansa, Clark-West, nullo per permutazione a blocchi (200). Proposte 3-4 dell'agente K, rubriche registrate prima (L8458).

## Esito

| Risultato | Fonte |
|---|---|
| ENS-1: "CONFERMATO per la combinazione delle previsioni, non per la ridge": SPY R² fuori campione +0,416%, Clark-West t 1,93 (p 0,027), permutazione p<0,005 | docs/EXECUTION_LEDGER.md#L8481-L8490 |
| ridge -0,391% | docs/EXECUTION_LEDGER.md#L8481-L8490 |
| QQQ +0,328% (t 2,46, p 0,007) | docs/EXECUTION_LEDGER.md#L8481-L8490 |
| ridge -0,299%. | docs/EXECUTION_LEDGER.md#L8481-L8490 |
| LASTHALF-OOS: "NON CONFERMATO": R² negativo ovunque: MES -3,24%, MNQ -6,32%, M2K -5,87%, MYM -4,12%, insieme -4,85% (Clark-West t -2,85, p 0,998). | docs/EXECUTION_LEDGER.md#L8481-L8490 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- ENS-1: "il filone 'direzione' resta aperto solo in questa forma: segnali semplici della famiglia, combinati con pesi uguali"
- LASTHALF-OOS "chiude il momentum intraday dell'ultima mezz'ora sui micro USA 2019-2026" (con BC-1).

## Prove

- runtime/proofs/ens1/ens1.json
- runtime/proofs/lasthalf/lasthalf.json
