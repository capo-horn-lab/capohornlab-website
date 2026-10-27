---
id: "ibsvix-1"
titolo: "IBSVIX-1 — la regola IBS condizionata al regime di volatilità noto il giorno prima (storico Cboe)"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "M2K"
  - "MYM"
  - "VIX"
finestra: "MES 1.915, MNQ 1.924, M2K 1.917, MYM 1.918 sessioni (dal 2019-05-06 al 2026-10-19), 9 celle di regime (livello VIX, struttura VIX/VIX3M, z VIX9D/VIX, cambio a 5 giorni)"
verdetto: "non confermata"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9307-L9314"
prove:
  - "runtime/proofs/ibsvix1/ibsvix1.json"
---

## Domanda

filtrare l'IBS per regime di volatilità noto il giorno prima migliora il risultato?

## Metodo e rubrica

BH sulle 36 p di scoperta (Welch cella contro resto), placebo 200 (seme 16); una cella è CONFERMATA come filtro solo su ≥2 strumenti su 4. Rubrica prima: sì (L9285).

## Esito

| Risultato | Fonte |
|---|---|
| "NON CONFERMATA su tutte le celle": "BH sulle 36 p di scoperta (Welch cella contro resto): NESSUNA cella scelta. Il q minimo e' MNQ backwardation 0,16" | docs/EXECUTION_LEDGER.md#L9307-L9314 |
| fuori rubrica, le celle di "paura" (VIX alto, backwardation) sono le migliori su tutti e 4 gli strumenti ma "con 7-10 trade ciascuna" (es. VIX alto MES +202 bp, 9 trade, t 1,85) | docs/EXECUTION_LEDGER.md#L9307-L9314 |
| VIX basso cella peggiore ovunque (verifica MES +14,6, MNQ -6,2 bp). | docs/EXECUTION_LEDGER.md#L9307-L9314 |
| Ampiezza attesa backwardation MES 314 / 229 bp contro contango 117 / 90. | docs/EXECUTION_LEDGER.md#L9307-L9314 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Lettura e limiti (dal registro)

- "Il regime del giorno prima prevede bene l'ampiezza della sessione (2-3 volte tra gli estremi), non il P&L della regola... con potenza sufficiente"
- "NULLA cambia da solo" per la carta.

## Prove

- runtime/proofs/ibsvix1/ibsvix1.json
