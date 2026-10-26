---
id: "keylim-1"
titolo: "KEYLIM-1 e LIMALL-1 — entrata a limite su un punto chiave invece che a mercato"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "M2K"
  - "MYM"
finestra: "MES, MNQ, M2K, MYM 2019-2026, 942 segnali IBS (614 scoperta, 328 verifica) (KEYLIM-1); LIMALL-1 su tutte le famiglie (parte A: famiglia MR-1; parte B: libreria OPT-FULL v2 di 11 strumenti)"
verdetto: "non confermata"
pubblicabilita: "avvertenza"
avvertenza: "(per LIMALL-1 serve prima leggere i file di proofs: nel ledger manca l'esito numerico). LIMALL-1: esito non chiuso nel ledger, non pubblicato."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L10178-L10178"
prove:
  - "runtime/proofs/keylim1/keylim1.json"
  - "runtime/proofs/keylim1/keylim1_trades.csv"
---

## Domanda

"niente entrate a mercato" — comprare con un limite su un livello sotto il prezzo migliora l'IBS?

## Metodo e rubrica

6 livelli (px-0,25 ATR20, px-0,5 ATR20, minimo della sessione...) x 2 validità = 12 test, differenza per segnale rispetto all'entrata a mercato, bootstrap a blocchi, BH.; Rubrica prima: sì (L9152, L9163).

## Esito

| Risultato | Fonte |
|---|---|

Non verificabile (i numeri non compaiono nelle fonti citate: restano fuori dalla tabella):

- KEYLIM-1: "NON CONFERMATA, nessuna variante con differenza positiva (BH: 0 su 12)". — non verificabile: 0, 12
- A mercato +47,2 bp per segnale in scoperta (t giorni 3,50), +25,0 in verifica (t 1,86) — non verificabile: 47,2, 3,50, 25,0, 1,86
- il limite perde i trade che non tornano indietro: differenza per segnale da -0,7 (K1 V2, riempiti 79%) a -38,1 bp (K4 V1, 15%) in scoperta — non verificabile: 0,7, 79, 38,1, 15
- in verifica da -0,1 (K3 V2, 91%) a -16,5. — non verificabile: 0,1, 91, 16,5

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "selezione avversa; per la regola con vantaggio l'entrata mirata non aggiunge, toglie poco o molto secondo quanto è lontano il livello."
- LIMALL-1: esito non chiuso nel ledger, non pubblicato.

## Prove

- runtime/proofs/keylim1/keylim1.json
- runtime/proofs/keylim1/keylim1_trades.csv
