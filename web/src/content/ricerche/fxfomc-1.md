---
id: "fxfomc-1"
titolo: "FXFOMC-1 — euro (M6E) attorno al FOMC e incertezza di politica monetaria"
data: "2026-10-20"
strumenti:
  - "M6E"
finestra: "M6E 1.958 sessioni (1.900 valide), 60 riunioni FOMC (36 scoperta, 24 verifica), 1.840 giorni di controllo"
verdetto: "non confermata"
audit: {"stato": "nota", "id": ["FXFOMC-1"]}
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9829-L9841"
prove:
  - "runtime/proofs/fxfomc1/fxfomc1.json"
---

## Ritiri e correzioni

- FXFOMC-1 limiti rettificati (L9841).

## Domanda

l'euro si apprezza/deprezza attorno al FOMC con l'incertezza (Mueller-Tahbaz-Salehi-Vedolin)?

## Metodo e rubrica

Finestre W0-W3, regole R0-R2 su W1, BH, placebo. Rubrica prima: sì (L9801).

## Esito

| Risultato | Fonte |
|---|---|
| "PASS, NON CONFERMATA": W0 scoperta +18,9 pip (+17,0 bp, t 1,79, n 36), verifica -20,7 pip (-17,6 bp, t -1,58, n 24) | docs/EXECUTION_LEDGER.md#L9829-L9841 |
| W1 scoperta +11,9 pip (t 2,15), verifica -7,1 pip (t -0,92) | docs/EXECUTION_LEDGER.md#L9829-L9841 |
| regola W1 netta R0 scoperta +11,63 USD (t 1,69, q 0,103), verifica -12,11 USD (t -1,25); "0 su 3". | docs/EXECUTION_LEDGER.md#L9829-L9841 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "Il deprezzamento del dollaro attorno al FOMC c'era nel 2019-2023... e si è rovesciato nel 2023-2026 (W0 -17,6 bp)": scompone il -0,09 di MACRO-1 C10, "la media di due fasi di segno opposto, non un'assenza di effetto".

## Prove

- runtime/proofs/fxfomc1/fxfomc1.json
