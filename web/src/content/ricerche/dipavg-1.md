---
id: "dipavg-1"
titolo: "DIPAVG-1 e EARLYEXIT-1 — mediare al ribasso con obiettivo cumulato; uscita anticipata del bot"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "M2K"
  - "MYM"
finestra: "DIPAVG-1: MES (1.778 sessioni), MNQ (1.788), M2K (1.760), MYM (1.772) 1 minuto 2019-05..2026-10, 4 micro x 32 combinazioni; EARLYEXIT-1: MES 2020-2024, 62 strategie COND-1 x 3 regole = 186 righe (61 con ≥30 trade in verifica)."
verdetto: "non confermata"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9235-L9247"
prove:
  - "runtime/proofs/dipavg1/dipavg1.json"
  - "runtime/proofs/earlyexit1/earlyexit1.json"
---

## Domanda

"so che non funziona ma sono curioso" (comprare il dip e aggiungere a ogni nuovo minimo); il bot che rivaluta il trade e esce prima dello stop.

## Metodo e rubrica

Rubriche prima: sì (L9221, L9229); BH q 0,10 (DIPAVG-1); regole E1 (metà strada), E2 (guadagno restituito dopo +0,5 R), E3.

## Esito

| Risultato | Fonte |
|---|---|
| DIPAVG-1: "NON CONFERMATA su tutti e quattro": nessuna combinazione passa BH q 0,10 (q minimo MNQ 0,65, MYM 0,85, MES 0,98, M2K 1,00) | docs/EXECUTION_LEDGER.md#L9235-L9247 |
| fuori rubrica, MES D 0,25 S 0,5 N 5 T 0,5 swing 84,76 USD/sessione (t 3,03) ma sequenza peggiore -8.031 USD e drawdown 15.877 USD su un micro | docs/EXECUTION_LEDGER.md#L9235-L9247 |
| MNQ sequenza peggiore in assoluto -19.528 USD. | docs/EXECUTION_LEDGER.md#L9235-L9247 |
| EARLYEXIT-1: "NON CONFERMATA come regola generale (1 su 61, su una strategia a zero)": E1 24 migliorano, 25 peggiorano, media +0,25 USD/trade | docs/EXECUTION_LEDGER.md#L9235-L9247 |
| 1 confermata (C1_ORB 30m da -1,27 a +0,98 USD/trade, t giorni 2,15, q 0,091). | docs/EXECUTION_LEDGER.md#L9235-L9247 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- DIPAVG-1: "è il profilo martingala atteso: 9 sequenze su 10 chiudono all'obiettivo, le altre perdono quanto decine di vincite"
- EARLYEXIT-1: "Rileggere il trade a metà strada non aiuta in modo sistematico".

## Prove

- runtime/proofs/dipavg1/dipavg1.json
- runtime/proofs/earlyexit1/earlyexit1.json
