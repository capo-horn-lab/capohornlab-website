---
id: "sent-1"
titolo: "SENT-1 — il sentiment (Technical Rating tipo TradingView) all'entrata come filtro delle strategie"
data: "2026-10-18"
strumenti:
  - "MES"
  - "MNQ"
  - "MCL"
finestra: "i 216 test di COND-1 (MES, MNQ, MCL; 5 m, 30 m, 1 h, 4 h, giornaliero)"
verdetto: "senza verdetto nel registro"
pubblicabilita: "avvertenza"
avvertenza: "usa la definizione pubblica del Technical Rating TradingView; dati licenziati solo aggregati."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L6662-L6674"
prove:
  - "runtime/proofs/sent1/sent1.json"
  - "runtime/proofs/sent1/codes.json"
---

## Domanda

il rating (strong sell...strong buy) al momento dell'entrata separa i trade buoni dai cattivi?

## Metodo e rubrica

22 regole (A, F, X, S per timeframe, A4, A5); adozione come DIR-1 (≥100 trade, media>0, t≥2, sopra R0, BH q≤0,10 su 4752, periodi mai usati). Rubrica prima: sì (modificata PRIMA di qualsiasi risultato, L6621-L6660).

## Esito

| Risultato | Fonte |
|---|---|
| "0 regole adottate su 4752 (q minimo 1,0)" | docs/EXECUTION_LEDGER.md#L6662-L6674 |
| 6 regole arrivano in verifica a 100 trade, media>0, t≥2 ma "nessuna regge i periodi mai usati". | docs/EXECUTION_LEDGER.md#L6662-L6674 |
| P&L in verifica per numero di timeframe a favore (media delle medie): 0 su 5 -2,96; 1 -2,84; 2 -1,57; 3 -2,24; 4 -2,55 | docs/EXECUTION_LEDGER.md#L6662-L6674 |
| 5 -1,22 USD a trade. | docs/EXECUTION_LEDGER.md#L6662-L6674 |

## Cosa NON dice

- "Il sentiment non separa i trade buoni dai cattivi."
- Per l'ORB il sentiment a 30 m/1 h dipende in parte dal segnale stesso (nota dichiarata).

## Prove

- runtime/proofs/sent1/sent1.json
- runtime/proofs/sent1/codes.json
