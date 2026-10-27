---
id: "oc-explore-1"
titolo: "OC-EXPLORE-1 e DIXCLOSE-1 — cosa condiziona aperture e chiusure; DIX basso e chiusura venduta (prova in carta)"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "M2K"
  - "MYM"
finestra: "MES (controllo MNQ, M2K, MYM), scoperta 2019-05..2023-12 (1.155 sessioni), verifica 2024-01..2026-10 (693 sessioni)"
verdetto: "senza verdetto nel registro"
pubblicabilita: "avvertenza"
avvertenza: "(esplorativo; DIX è dato SqueezeMetrics)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9072-L9082"
prove:
  - "runtime/paper/dixclose1.csv"
---

## Domanda

quali variabili note prima condizionano gap, prima mezz'ora, apertura-chiusura, ultima ora? DIXCLOSE-1: short alle 15:00 ET con DIX del giorno prima ≤0,430, solo in avanti dal 20/10/2026.

## Metodo e rubrica

189 relazioni in scoperta, BH q 0,10, al massimo 10 portate in verifica. Rubrica prima: sì (disegno prima, L9066, L9074).

## Esito

| Risultato | Fonte |
|---|---|
| "189 relazioni provate in scoperta (1.155 sessioni MES 2019-05 / 2023-12), 3 sopravvivono a BH q 0,10; delle 10 portate in verifica (693 sessioni 2024-01 / 2026-10) ne restano 2, entrambe col DIX del giorno prima": DIX -> ultima ora (scoperta t +3,22, verifica t +1,80, p 0,036) | docs/EXECUTION_LEDGER.md#L9072-L9082 |
| DIX -> ultimi 30' (t +3,33 / +2,40). | docs/EXECUTION_LEDGER.md#L9072-L9082 |
| "Verdetto: nessuna regola adottata". | docs/EXECUTION_LEDGER.md#L9072-L9082 |
| Lato short DIX≤0,430, 15:00->16:00: verifica MES 64 trade +10,5 bp lordi (t NW 2,9), senza i 3 migliori +5,0 (t 0,8). | docs/EXECUTION_LEDGER.md#L9072-L9082 |
| Momentum dalla distanza VWAP alle 15:00: "Morte in verifica" (scoperta t +3,66, verifica -1,74). | docs/EXECUTION_LEDGER.md#L9072-L9082 |
| DIXCLOSE-1: esito non ancora presente (prova in avanti). | docs/EXECUTION_LEDGER.md#L9072-L9082 |

## Cosa NON dice

- "Esito esplorativo, non una conferma"
- "il DIX ha cambiato regime (giorni <= 0,430: 50-68% nel 2019-21, 0-14% dal 2022)".

## Prove

- runtime/research/fable_oc/
- runtime/paper/dixclose1.csv
