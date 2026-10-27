---
id: "xmom-1"
titolo: "XMOM-1 — valore e momentum tra attivi della stessa classe (Asness-Moskowitz-Pedersen)"
data: "2026-10-20"
strumenti: []
finestra: "ETF mensili: 12 borse nazionali, 4 valute, 11 materie prime, 11 settori USA; scoperta fino al 2018-12, verifica 2019-01..2026-09 (92 mesi)"
verdetto: "pass · non confermata"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L10053-L10061"
prove:
  - "runtime/proofs/xmom1/xmom1.json"
---

## Domanda

valore e momentum in sezione trasversale funzionano dentro ogni classe?

## Metodo e rubrica

Terzile lungo / terzile corto, pesi uguali, 2 bp per unità, t Newey-West 3 ritardi, placebo 200, BH. Rubrica prima: sì (L10045).

## Esito

| Risultato | Fonte |
|---|---|
| "Esito PASS, verdetto NON CONFERMATA: il globale combinato è sotto zero in verifica e nessuna riga passa la soglia." | docs/EXECUTION_LEDGER.md#L10053-L10061 |
| Es.: globale COMBO scoperta +27,5 t 0,73 / verifica -4,3 t -0,22 (placebo p95 22,5, q 0,86) | docs/EXECUTION_LEDGER.md#L10053-L10061 |
| valore materie prime verifica +215,5 bp t 2,23 (Sharpe 0,77) ma q 0,19 su 15 righe. | docs/EXECUTION_LEDGER.md#L10053-L10061 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- Il valore sulle materie prime "poggia sui continui di Yahoo con i salti ai rolli: prezzi e rendimenti non scambiabili"
- "il momentum tra materie prime è negativo in entrambe le fasi, l'opposto del paper"
- fatto descrittivo ritrovato: correlazione negativa valore-momentum in ogni classe (borse -0,53, materie prime -0,56).

## Prove

- runtime/proofs/xmom1/xmom1.json
