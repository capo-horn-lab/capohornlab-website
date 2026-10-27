---
id: "earn-1"
titolo: "EARN-1 — trimestrali delle mega-cap del Nasdaq come eventi per MNQ"
data: "2026-10-19"
strumenti:
  - "MNQ"
finestra: "MNQ 1 minuto NinjaTrader 2019-05..2026-10 (202 sessioni evento su 1.922); 285 pubblicazioni 8-K item 2.02 di 8 aziende dal 2019 (SEC EDGAR)"
verdetto: "confermato"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8161-L8166"
prove:
  - "runtime/proofs/earn1/earn1.json"
---

## Domanda

le sessioni dopo le trimestrali delle mega-cap sono più ampie? Evitarle protegge le strategie MNQ?

## Metodo e rubrica

Test 1 ampiezza (\|rendimento\| e (max-min)/chiusura), scoperta/verifica; Test 2 protezione P8 sulle 86 strategie MNQ di adapt1, BH q≤0,10. Rubrica prima: sì (L8154).

## Esito

| Risultato | Fonte |
|---|---|
| "CONFERMATO sull'ampiezza; protezione P8 utile in parte." \\|rendimento\\| chiusura su chiusura scoperta 136,8 contro 114,4 bp (t 1,86), verifica 115,0 contro 86,8 (t 2,72) | docs/EXECUTION_LEDGER.md#L8161-L8166 |
| ampiezza sessione scoperta 197,0 contro 170,0 (t 2,34), verifica 169,3 contro 131,9 (t 4,00). | docs/EXECUTION_LEDGER.md#L8161-L8166 |
| P8 aiuta 9 (BH), differenza positiva in 62 su 86 (72%), 19 sessioni evento in verifica. | docs/EXECUTION_LEDGER.md#L8161-L8166 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Lettura e limiti (dal registro)

- "le trimestrali delle mega-cap allargano MNQ di circa il 25-30% come le fasi agitate" (ampiezza, non direzione).

## Prove

- runtime/proofs/earn1/earn1.json
