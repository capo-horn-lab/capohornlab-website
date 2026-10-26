---
id: "sent-4"
titolo: "SENT-4 — sentiment per fasce orarie"
data: "2026-10-18"
strumenti:
  - "MES"
  - "MNQ"
  - "MCL"
finestra: "MES, MNQ, MCL a 5 m, 30 m, 1 h"
verdetto: "descrittivo"
pubblicabilita: "avvertenza"
avvertenza: "esplorativo; le finestre notturne non erano in rubrica (H-NEXT-3) e non sono adottate; dati licenziati solo aggregati."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L6888-L6900"
prove:
  - "runtime/proofs/sent4/sent4.json"
---

## Domanda

tagliare le ore fuori dalle aperture principali migliora il motore di SENT-3?

## Metodo e rubrica

6 finestre in ora di New York; modello addestrato sulle sole finestre principali; stesso voto di SENT-3. Rubrica prima: sì (L6862+).

## Esito

| Risultato | Fonte |
|---|---|
| Voto 57,9 contro 64,5 di SENT-3 ("tagliare le ore toglie proprio le ore in cui il motore funziona"). | docs/EXECUTION_LEDGER.md#L6888-L6900 |
| MES 5 m fuori orari IC 0,054 (t 15,4) su 40-80% e 0,057 (t 9,8) nel test, apertura USA 0,017 e -0,001 | docs/EXECUTION_LEDGER.md#L6888-L6900 |
| spostamento medio MES 2,6 punti base fuori orari contro 7,6 all'apertura USA. | docs/EXECUTION_LEDGER.md#L6888-L6900 |
| Il modello solo-finestre non è mai tenuto. | docs/EXECUTION_LEDGER.md#L6888-L6900 |

## Cosa NON dice

- Le finestre notturne (18:00-02:00 ET) non erano nella rubrica: dichiarate H-NEXT-3, solo su sessioni future, non adottate.

## Prove

- runtime/proofs/sent4/sent4.json
