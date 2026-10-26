---
id: "lenti-1"
titolo: "LENTI-1 — lenti separate sul campione intero (VWAP, gap, volume, range, posizione, calendario) e concordanza"
data: "2026-10-22"
strumenti:
  - "MNQ"
finestra: "MNQ (e gli altri micro), ultime 500 sessioni, lenti misurate allo stesso minuto; richiesta del proprietario: \"non voglio dimezzare i casi, voglio aumentarli ... analisi multiple e vedere se concordano\"."
verdetto: "descrittivo"
pubblicabilita: "avvertenza"
avvertenza: "(retrospettiva su dati già visti; nessuna prova di vantaggio)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L10363-L10371"
prove:
  - "runtime/proofs/lenti1/PIANO.md"
  - "runtime/proofs/lenti1/verita.py"
  - "runtime/proofs/lenti1/truth.json"
  - "runtime/proofs/lenti1/run.log"
  - "runtime/proofs/lenti1/calibrazione.json"
  - "runtime/proofs/lenti1/esempio-4-strumenti.json"
---

## Domanda

MNQ (e gli altri micro), ultime 500 sessioni, lenti misurate allo stesso minuto; richiesta del proprietario: "non voglio dimezzare i casi, voglio aumentarli... analisi multiple e vedere se concordano".

## Metodo e rubrica

6 lenti (8 righe), ciascuna da sola; 5 esiti uguali per tutte; concordanza (quante lenti pendono su/giù oltre il margine); registro in avanti e calibrazione con Brier contro 0,25 e 200 placebo. Rubrica prima: sì, con attesa dichiarata (concordanza sul "quanto" (ampiezza), poca o nessuna sul "dove" (verso della chiusura)) (L10352).

## Esito

| Risultato | Fonte |
|---|---|
| Esito PASS (19 test PASS), calibrazione in avanti NOT_RUN. | docs/EXECUTION_LEDGER.md#L10363-L10371 |
| MNQ alle 14:15 Roma: base "chiusura sopra" 54 ±4 | docs/EXECUTION_LEDGER.md#L10363-L10371 |
| L1 VWAP notte SOTTO n 208: 60 ±7 | docs/EXECUTION_LEDGER.md#L10363-L10371 |
| L5 posizione bassa n 131: 61 ±8 | docs/EXECUTION_LEDGER.md#L10363-L10371 |
| "concordano sul quanto, non sul dove: +0,3 A 1 lente su, 0 giu', 7 neutre; -0,3 A 0 / 0 / 8; chiusura sopra 0 / 0 / 8". | docs/EXECUTION_LEDGER.md#L10363-L10371 |
| Retrospettiva "già vista" (MNQ 250 sessioni): Brier L5 posizione 0,231, L1 VWAP notte 0,234 contro base 0,2465 | docs/EXECUTION_LEDGER.md#L10363-L10371 |
| per "chiusura sopra" base 0,2512 e "nessuna lente la batte (0,2506-0,2544)". | docs/EXECUTION_LEDGER.md#L10363-L10371 |

## Cosa NON dice

- "Esattamente l'attesa dichiarata nella rubrica: concordanza sul quanto, nulla sul dove"
- il vantaggio delle lenti di prezzo sta in nuovo minimo/massimo: "effetto meccanico della posizione".

## Prove

- runtime/proofs/lenti1/PIANO.md
- runtime/proofs/lenti1/verita.py
- runtime/proofs/lenti1/truth.json
- runtime/proofs/lenti1/run.log
- runtime/proofs/lenti1/calibrazione.json
- runtime/proofs/lenti1/esempio-4-strumenti.json
