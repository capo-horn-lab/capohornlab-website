---
id: "openlim-1"
titolo: "OPENLIM-1 — ordini lontani dal prezzo alla prima candela delle 9:30"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "M2K"
  - "MYM"
finestra: "MES, MNQ, M2K, MYM 1 minuto 2019-05..2026-10-16; idea del proprietario: \"le prime candele oscillano molto, poi prendono un trend\""
verdetto: "non confermata"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9142-L9142"
prove:
  - "runtime/proofs/openlim1/openlim1.json"
---

## Domanda

ordini OCO a p0 ± D (D 0,15-0,5 U, U = mediana del range 9:29-10:29 delle ultime 60 sessioni) con limite (contro il movimento) o stop (a favore) hanno edge?

## Metodo e rubrica

72 combinazioni (famiglie L e S, uscite X1/X2/X3), scoperta 2019-05..2023-12, BH q 0,10, max 3 in verifica; CONFERMATA se media netta>0 con p<0,05, positiva su ≥3 strumenti su 4, +1 tick. Rubrica prima: sì (L9132).

## Esito

| Risultato | Fonte |
|---|---|
| "NON CONFERMATA, nessuna combinazione passa BH in scoperta (positive 8 su 72, migliore t +0,77: L D 0,5 U finestra 1 minuto X3, 52 giorni; peggiori L D 0,15 U con stop e obiettivo, t -13,6)". | docs/EXECUTION_LEDGER.md#L9142-L9142 |
| MNQ 2019-2026: i limiti contro il movimento perdono in ogni variante (da -4 a -19 punti per trade, vincenti 28-46%) | docs/EXECUTION_LEDGER.md#L9142-L9142 |
| gli stop a favore con sola uscita a tempo rendono da +0,6 a +12,9 punti ma "sugli altri micro no" (media dei 4 t ≤ 0,30). | docs/EXECUTION_LEDGER.md#L9142-L9142 |
| Giorno del proprietario 19/10: limite buy 29.740, obiettivo 29.800: +60 punti ma "è un caso della famiglia L... che sul campione perde in media". | docs/EXECUTION_LEDGER.md#L9142-L9142 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- Il caso singolo del proprietario non è una prova della regola.

## Prove

- runtime/proofs/openlim1/openlim1.json
