---
id: "chop-1"
titolo: "CHOP-1 — all'apertura il mercato è \"choppy\"?"
data: "2026-10-19"
strumenti: []
finestra: "4 micro 1 minuto 2019-05..2026-10-16"
verdetto: "non confermata"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9150-L9150"
prove:
  - "runtime/proofs/chop1/chop1.json"
---

## Domanda

dopo aver toccato un estremo (p0 ± D) il prezzo torna al centro più spesso del caso?

## Metodo e rubrica

Corse G1 (ritorno a p0 contro stop) e G2 per D in {0,10-0,50 U}; quota di obiettivi primi contro la soglia di pareggio, binomiale in verifica; scoperta 2019-05..2023-12 / verifica 2024-01..2026-10. Rubrica prima: sì (L9144).

## Esito

| Risultato | Fonte |
|---|---|
| "NON CONFERMATO, 0 strumenti su 4 per ogni combinazione. Dopo il tocco di un estremo il ritorno NON è più probabile del caso." D 0,25 U: obiettivo G1 primo nel 44-51% contro 50% del caso e soglia di pareggio 52-59% | docs/EXECUTION_LEDGER.md#L9150-L9150 |
| G2 28-34% contro 33,3% | docs/EXECUTION_LEDGER.md#L9150-L9150 |
| P&L sempre negativo (MNQ da -0,9 a -4,7 punti per trade). | docs/EXECUTION_LEDGER.md#L9150-L9150 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- Limite del dato a 1 minuto: su MNQ il 36% (D 0,10) e il 13% (D 0,15) delle corse si chiude con lo stop già nella barra d'ingresso
- per distanze piccole serve il tick (TICK-1 ha solo un mese per contratto).

## Prove

- runtime/proofs/chop1/chop1.json
