---
id: "invariance-1"
titolo: "INVARIANCE-1 — invarianza della microstruttura (Kyle-Obizhaeva) sui tick di 11 future"
data: "2026-10-20"
strumenti:
  - "FDXM"
  - "FESX"
  - "M2K"
  - "M6E"
  - "MBT"
  - "MCL"
  - "MES"
  - "MGC"
  - "MNQ"
  - "MYM"
  - "ZN"
finestra: "tick 20/9-16/10/2026 di FDXM, FESX, M2K, M6E, MBT, MCL, MES, MGC, MNQ, MYM, ZN (263 strumenti-giorno)"
verdetto: "parziale"
pubblicabilita: "avvertenza"
avvertenza: "(20-29 giorni di tick: campione breve)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L10105-L10109"
prove:
  - "runtime/proofs/invariance1/invariance1.json"
---

## Domanda

con W = P x V x σ il numero di scambi scala come W^(2/3) e la dimensione media come W^(1/3)?

## Metodo e rubrica

Regressioni log-log con errori a grappolo per strumento; CONFERMATA se le pendenze stanno in 2/3 ± 0,1 e 1/3 ± 0,1 in entrambe le metà. Rubrica prima: sì (L10099).

## Esito

| Risultato | Fonte |
|---|---|
| "Verdetto secondo la rubrica: PARZIALE": pendenza del numero di scambi scoperta 0,641 (0,062), verifica 0,641 (0,071) | docs/EXECUTION_LEDGER.md#L10105-L10109 |
| dimensione media scoperta 0,229 (0,075), verifica 0,252 (0,078). | docs/EXECUTION_LEDGER.md#L10105-L10109 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Lettura e limiti (dal registro)

- Si contano gli scambi registrati, non le scommesse del paper
- scala per strumento (MNQ 1,9 milioni di scambi e 149 miliardi USD al giorno, ZN 526 mila e 255 miliardi).

## Prove

- runtime/proofs/invariance1/invariance1.json
