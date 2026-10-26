---
id: "timestral-1"
titolo: "TIMESTRAL-1 e TIMESTRAL-2 — modello di serie temporali di Mistral (Timestral) e suo fine-tuning"
data: "2026-10-23"
strumenti:
  - "MNQ"
finestra: "MNQ 1 minuto (scoperta 200 giorni 2020-2023, validazione 2023, test 2024-2026: 697 giorni, 6.970 punti); pesi Timestral 5M/28M/123M/209M da huggingface.co/mistralai, licenza Modified MIT"
verdetto: "non confermata"
pubblicabilita: "avvertenza"
avvertenza: "valutazione di un modello di terzi (rispettare la licenza e citare); nessuna implicazione di trading."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L10635-L10638"
prove:
  - "docs/research/TIMESTRAL_RICERCA_2026-10-23.md"
  - "docs/research/TIMESTRAL_FINETUNING_2026-10-23.md"
---

## Domanda

il modello (zero-shot e dopo fine-tuning con perdita pinball e AdamW) prevede meglio della base B1 gli orizzonti 30/60/120 minuti?

## Metodo e rubrica

Skill CRPS contro la base B1, copertura 10-90 e 25-75; regola fissata nel PIANO prima: copertura entro ±5 punti su tutti gli orizzonti. Rubrica prima: sì (L10582, L10627).

## Esito

| Risultato | Fonte |
|---|---|
| TIMESTRAL-1 "FAIL, nessuna integrazione": 209M passo 1 L 8192, skill CRPS contro B1 +0,21% [-0,41; +0,85] a 30 min, +0,23% [-0,38; +0,89] a 60 min, +0,94% [+0,31; +1,58] a 120 min | docs/EXECUTION_LEDGER.md#L10635-L10638 |
| copertura 10-90 74,6 / 75,5 / 77,8% (B1 78,4 / 79,2 / 80,1). | docs/EXECUTION_LEDGER.md#L10635-L10638 |
| TIMESTRAL-2 "FAIL, nessuna integrazione": dopo fine-tuning skill +0,17% [-0,45; +0,81] a 30 min, +0,13% [-0,47; +0,79] a 60, +0,88% [+0,22; +1,55] a 120 | docs/EXECUTION_LEDGER.md#L10664-L10667 |
| contro il 209M originale -0,04 / -0,09 / -0,06% con intervalli che contengono 0. | docs/EXECUTION_LEDGER.md#L10635-L10638 · docs/EXECUTION_LEDGER.md#L10664-L10667 |

## Cosa NON dice

- Post hoc (non decide): "meglio della base sull'ampiezza delle prossime 1-2 ore fuori dall'apertura (10:00-14:00 NY +2,3/+2,7%), peggio all'apertura (-8/-12%), ventaglio troppo stretto, guadagno solo nel 2025"
- il verso della mediana "non prevede il verso"
- contaminazione del test non verificabile (dati di addestramento Mistral non dichiarati).

## Prove

- runtime/proofs/timestral1/
- runtime/proofs/timestral2/
- docs/research/TIMESTRAL_RICERCA_2026-10-23.md
- docs/research/TIMESTRAL_FINETUNING_2026-10-23.md
