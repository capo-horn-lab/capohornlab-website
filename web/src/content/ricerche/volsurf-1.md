---
id: "volsurf-1"
titolo: "VOLSURF-1, VOLSURF-2, VOLSURF-3 / 3B — superficie di volatilità implicita (SVI) e fonte delle catene di opzioni"
data: "2026-10-25"
strumenti:
  - "NDX"
  - "QQQ"
  - "SPX"
  - "SPY"
finestra: "catene Cboe del 23/10 (NDX 34 scadenze, QQQ, SPX, SPY), poi istantanea IBKR su NDX (49 opzioni)"
verdetto: "pass · blocked_env · not_run"
pubblicabilita: "avvertenza"
avvertenza: "il PNG del pannello mostra valori di superficie derivati da dati licenziati."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L10656-L10662"
prove:
  - "runtime/proofs/volsurf1/pannello_640x300.png"
  - "runtime/proofs/volsurf1/pannello_1280x550.png"
  - "docs/research/VOLSURF_RICERCA_2026-10-25.md"
  - "docs/research/VOLSURF_FONTI_2026-10-25.md"
---

## Domanda

costruire la superficie SVI (ATM, RR25, BF25, skew) e trovare una fonte automatica per le catene di opzioni.

## Metodo e rubrica

OTM con bid>0, spread/medio≤0,5; forward dalla parità put-call; SVI per scadenza con penalità di farfalla, calendario, ali di Lee; soglie del PIANO fissate prima: RMSE ≤ 1,0 punti, farfalla g ≥ -1e-4, calendario ≥ -1e-5. Rubrica prima: sì (L10644, L10670, L10678).

## Esito

| Risultato | Fonte |
|---|---|
| VOLSURF-1: RMSE max NDX 0,183, QQQ 0,237, SPX 0,206, SPY 0,127 (dopo la correzione dello sconto dalla parità), 0 violazioni di farfalla e calendario | docs/EXECUTION_LEDGER.md#L10656-L10662 |
| ATM 30 g NDX 24,06 contro 24,21 Cboe | docs/EXECUTION_LEDGER.md#L10656-L10662 |
| VOLSURF-2: "NinjaTrader: NO" (opzioni non supportate in NinjaScript) | docs/EXECUTION_LEDGER.md#L10656-L10662 · docs/EXECUTION_LEDGER.md#L10673-L10682 · docs/EXECUTION_LEDGER.md#L10761-L10761 |
| IBKR: API BLOCKED_ENV, connettore claude.ai PASS su NDX (bid/ask identici a Cboe su 49/49), RMSE 0,070 / 0,067 / 0,044, ATM entro 0,27 punti contro Cboe. | docs/EXECUTION_LEDGER.md#L10673-L10682 |
| 22 test PASS in 3B | docs/EXECUTION_LEDGER.md#L10761-L10761 |
| chiamate reali NOT_RUN. | docs/EXECUTION_LEDGER.md#L10656-L10662 · docs/EXECUTION_LEDGER.md#L10673-L10682 · docs/EXECUTION_LEDGER.md#L10761-L10761 |

2 righe della scheda non riportate: la prova citata non le contiene.

## Cosa NON dice

- I termini Cboe vietano lo scarico automatico (cboe.com/terms sez. 2): "il motore NON scarica nulla, legge... salvato a mano" (decisione sulla fonte al proprietario).

## Prove

- runtime/proofs/volsurf1/
- runtime/proofs/volsurf2/
- runtime/proofs/volsurf3/
- runtime/proofs/volsurf3b/
- runtime/proofs/volsurf1/pannello_640x300.png
- runtime/proofs/volsurf1/pannello_1280x550.png
- docs/research/VOLSURF_RICERCA_2026-10-25.md
- docs/research/VOLSURF_FONTI_2026-10-25.md
