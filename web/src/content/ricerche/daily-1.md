---
id: "daily-1"
titolo: "DAILY-1 — quattro famiglie di effetti giornalieri (fine mese, pre-FOMC, notte contro giorno, varianti IBS)"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "M2K"
  - "MYM"
finestra: "MES, MNQ, M2K, MYM 1 minuto 2019-05..2026-10 (1.837-1.843 sessioni valide per strumento; 58 riunioni FOMC)"
verdetto: "verdetto non estratto: vedi Esito"
pubblicabilita: "avvertenza"
avvertenza: "2 conferme IBS su 12 prove con margine di 5 USD sul p95 per MES (rumore di selezione, come in IBS8-1); costi del modello a 0,95 USD per lato."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9298-L9304"
prove:
  - "runtime/proofs/daily1/daily1.json"
---

## Domanda

gli effetti giornalieri della letteratura (Ariel, Lakonishok-Smidt, Lucca-Moench, Cooper-Cliff-Gulen) e 18 varianti IBS reggono con costi e placebo?

## Metodo e rubrica

Scoperta 60% / verifica 40% (taglio 2023-10-25/26), BH q≤0,10, t sui giorni≥2, placebo 200. Rubrica prima: sì (L9275).

## Esito

| Risultato | Fonte |
|---|---|
| Famiglie 1-3 "NON CONFERMATA su tutti e quattro": fine mese regola 0/+3 in verifica MES +46,7 USD/trade (t 0,49), MNQ +194,2 (t 1,09) | docs/EXECUTION_LEDGER.md#L9298-L9304 |
| "le medie positive sono la deriva del mercato: il placebo... rende 62-140 USD/trade" | docs/EXECUTION_LEDGER.md#L9298-L9304 |
| pre-FOMC chiusura->chiusura negativa ovunque (MES -55,6, MNQ -14,0 USD) | docs/EXECUTION_LEDGER.md#L9298-L9304 |
| notte contro giorno: notte MES +9,6 USD/sessione (t 1,41), MNQ +25,7 (t 1,82), sotto il p95 degli scambi casuali. | docs/EXECUTION_LEDGER.md#L9298-L9304 |
| Famiglia 4: "2 CONFERMATE su 12 prove di verifica" (IBS<0,20 -> IBS>0,80 o 8 sessioni): MES verifica 74 trade +132,8 USD (t 3,4) contro p95 del placebo 127,4 (margine 5 USD) | docs/EXECUTION_LEDGER.md#L9298-L9304 |
| MYM 79 trade +101,3 (t 3,62) contro p95 89,1. | docs/EXECUTION_LEDGER.md#L9298-L9304 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Lettura e limiti (dal registro)

- "Lettura onesta: tre famiglie su quattro non si distinguono dal caso su nessuno strumento... 2 su 12 prove al 5% ne vale 0,6 per caso. Non è una ragione per cambiare la regola in carta."

## Prove

- runtime/proofs/daily1/daily1.json
