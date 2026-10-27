---
id: "openpyr-1"
titolo: "OPENPYR-1 e WINDAY-1 — ingresso all'apertura con aggiunte a favore (\"effetto domino\") e trailing"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "M2K"
  - "MYM"
finestra: "MES, MNQ, M2K, MYM 1 minuto 2019-05..2026-10-16"
verdetto: "non confermata · confermato"
pubblicabilita: "avvertenza"
avvertenza: "WINDAY-1: \"confermato secondo la rubrica\" ma riserve pesanti"
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9113-L9113"
prove:
  - "runtime/proofs/openpyr1/openpyr1.json"
  - "runtime/proofs/winday1/winday1_MNQ.json"
  - "runtime/proofs/winday1/winday1_MES.json"
  - "runtime/proofs/winday1/winday1_M2K.json"
  - "runtime/proofs/winday1/winday1_MYM.json"
---

## Domanda

entrare all'apertura, aggiungere unità a favore con trailing stop comune dà profitto? Cosa rende vincenti i giorni migliori su MNQ?

## Metodo e rubrica

80 combinazioni, scoperta 2019-05..2023-12, BH q 0,10, al massimo 3 in verifica, CONFERMATA se media netta>0 con p<0,05, positiva su ≥3 strumenti su 4 e con +1 tick. Rubrica prima: sì (L9101, L9115).

## Esito

| Risultato | Fonte |
|---|---|
| OPENPYR-1: "NON CONFERMATA, nessuna combinazione passa BH in scoperta": 0 combinazioni positive su 80 (convenzione prudente), migliore t -0,23, peggiore t -35,9 | docs/EXECUTION_LEDGER.md#L9113-L9113 |
| con aggiunte i vincenti scendono al 20-40%, "il 60-90% dei guadagni sta nel 10% dei giorni migliori". | docs/EXECUTION_LEDGER.md#L9113-L9113 |
| WINDAY-1 MNQ: 1.761 giorni, media +0,156 U, il 10% migliore fa il 67% dei guadagni | docs/EXECUTION_LEDGER.md#L9123-L9123 |
| "CONFERMATO SECONDO LA RUBRICA, con riserve" per il range notturno terzile medio (235 giorni, +0,395 U, t 1,83, p 0,035) ma differenza dagli altri giorni +0,16 U con t di Welch 0,65 (non significativa). | docs/EXECUTION_LEDGER.md#L9123-L9123 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "con un mercato martingala ogni regola d'uscita ha attesa = - costi"
- nota fuori protocollo: una variante rende +12 bp su MNQ ma "scelta dopo aver visto 80 x 4 risultati, non è una prova"
- WINDAY-1: "Conferma completa solo dopo MES, M2K, MYM" ( riporta gli altri strumenti).

## Prove

- runtime/proofs/openpyr1/openpyr1.json
- runtime/proofs/winday1/winday1_MNQ.json
- runtime/proofs/winday1/winday1_MES.json
- runtime/proofs/winday1/winday1_M2K.json
- runtime/proofs/winday1/winday1_MYM.json
