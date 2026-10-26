---
id: "tugwar-1"
titolo: "TUGWAR-1 e GHLZ-1 — tiro alla fune notte/giorno; momentum della prima alla ultima mezz'ora (sei future azionari)"
data: "2026-10-20"
strumenti:
  - "MES"
  - "MNQ"
  - "M2K"
  - "MYM"
  - "FESX"
  - "FDXM"
finestra: "MES, MNQ, M2K, MYM (dal 2019-05) e FESX, FDXM (dal 2019-03) fino al 2026-10-19"
verdetto: "non confermata"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9744-L9752"
prove:
  - "runtime/proofs/tugwar1/tugwar1.json"
---

## Domanda

la notte rende e il giorno è piatto (Lou-Polk-Skouras)? La prima mezz'ora prevede l'ultima (Gao-Han-Li-Zhou)?

## Metodo e rubrica

TUGWAR: famiglia di 13 regole, BH q 0,10, placebo; GHLZ: regressione con t Newey-West e regola 15:30->chiusura, condizionamento al GEX. Rubriche prima: sì (L9705, L9755).

## Esito

| Risultato | Fonte |
|---|---|
| Entrambi "PASS, NON CONFERMATA". | docs/EXECUTION_LEDGER.md#L9744-L9752 · docs/EXECUTION_LEDGER.md#L9810-L9815 |
| TUGWAR-1: notte lorda in verifica MES +4,8 bp (t 2,11), MNQ +7,0 (t 2,21), M2K +6,7 (t 1,98) ma in scoperta MES +2,1 (t 0,79) | docs/EXECUTION_LEDGER.md#L9744-L9752 |
| "0 regole su 13 passano (t >= 2, q <= 0,10, sopra il p95)" | docs/EXECUTION_LEDGER.md#L9744-L9752 |
| la correlazione notte-giorno è negativa in verifica su tutti e sei (MES -0,12, t -3,1) | docs/EXECUTION_LEDGER.md#L9744-L9752 |
| lungo solo di notte MES +11,1 USD (t 1,62), MNQ +28,0 (t 1,97) sotto il compra-e-tieni (MES 17,5). | docs/EXECUTION_LEDGER.md#L9744-L9752 |
| GHLZ-1: pendenza della prima mezz'ora nulla in entrambe le fasi (es. verifica MES -0,002, t -0,06) | docs/EXECUTION_LEDGER.md#L9810-L9815 |
| regola verifica MES -5,5 USD (t -2,35), MYM -3,8 (t -2,64), FESX -20,6 EUR (t -5,90) | docs/EXECUTION_LEDGER.md#L9810-L9815 |
| nessun effetto del GEX. | docs/EXECUTION_LEDGER.md#L9744-L9752 · docs/EXECUTION_LEDGER.md#L9810-L9815 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- TUGWAR: "I fatti del paper... compaiono solo in verifica, non in scoperta... tutte rendono meno del compra-e-tieni"
- GHLZ: "Il momentum intraday... non c'è nei future 2019-2026" (conferma LASTHALF-OOS e BC-1).

## Prove

- runtime/proofs/tugwar1/tugwar1.json
- runtime/proofs/ghlz1/*.json
