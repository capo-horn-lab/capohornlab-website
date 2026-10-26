---
id: "opt-full-1"
titolo: "OPT-FULL-1 / OPT-FULL-1M / OPT-COND-1 — ottimizzazione completa a forza bruta (circa 6,35 milioni di combinazioni) e per condizioni di mercato"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "M2K"
  - "MYM"
  - "MGC"
  - "M6E"
  - "FESX"
  - "FDXM"
  - "MBT"
  - "MCL"
  - "ZN"
finestra: "11 strumenti (MES, MNQ, M2K, MYM, MGC, M6E, FESX, FDXM, MBT, MCL, ZN), 7 timeframe (1 m-giornaliero), 47 setup, ~520.000 combinazioni per strumento (94.752 a 1 minuto), 198 walk"
verdetto: "non confermata"
pubblicabilita: "avvertenza"
avvertenza: "citare esito finale OPT-FULL; per OPT-COND-1 dichiarare \"esito intermedio\". OPT-COND-1: esito non chiuso nel ledger, non pubblicato."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9017-L9017"
prove:
  - "runtime/proofs/optfull/optfull.json"
  - "runtime/proofs/optfull/optfull_v2_6tf.json"
---

## Domanda

una ricerca "a forza bruta" come lo Strategy Analyzer trova qualcosa di vero se validata con placebo, DSR e verifica?

## Metodo e rubrica

Walk-forward mobile (8 blocchi da 60 sessioni), F3 prudente, placebo abbinato per numero di trade (correzione 26), BH, DSR≥0,95, t sui giorni, +1 tick; prima, prove di verità (TRUTH-1) e revisione dell'agente Fable 5.1.; Rubrica prima: sì (L8843, L8880, L8885).

## Esito

| Risultato | Fonte |
|---|---|

Non verificabile (i numeri non compaiono nelle fonti citate: restano fuori dalla tabella):

- FINALE: "0 CANDIDATI e 0 CONFERMATI su 198 walk" — non verificabile: 198
- migliori M2K famiglia MACD 69 trade +59,4 bp t 2,87 (q 0,29) — non verificabile: 59,4, 2,87, 0,29
- MES famiglia STO 79 trade +52,7 t 2,79 — non verificabile: 52,7, 2,79
- MYM famiglia RSI 59 trade +82,9 t 2,71 — non verificabile: 82,9, 2,71
- a 1 minuto nessun walk positivo con t sopra 0,6 e i più negativi FESX -5,58 bp t -5,88, M2K -5,19 t -4,84, MBT -6,88 t -3,78 ("i costi dominano"). — non verificabile: 0,6, 5,58, 5,88, 5,19, 4,84, 6,88, 3,78

## Cosa NON dice

- "l'ottimizzazione completa a forza bruta... non trova nessuna strategia nuova oltre alla famiglia di mean reversion già nota sugli indici USA"
- OPT-COND-1: esito non chiuso nel ledger, non pubblicato.

## Prove

- runtime/proofs/optfull/optfull.json
- runtime/proofs/optfull/optfull_v2_6tf.json
- runtime/proofs/optfull_barra
- runtime/proofs/optfull_lim025
- runtime/proofs/optfull_lim05
