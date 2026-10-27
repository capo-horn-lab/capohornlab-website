---
id: "macrowin-1"
titolo: "MACROWIN-1 e MACROWIN-2 — formazione del prezzo di ZN attorno agli annunci; NFP e CPI sui micro azionari"
data: "2026-10-20"
strumenti:
  - "ZN"
finestra: "ZN 1 minuto (1.886 sessioni valide), NFP 80, CPI 79, FOMC 60, 1.671 giorni di controllo (MACROWIN-1); micro azionari NFP/CPI 8:30 ET (MACROWIN-2)"
verdetto: "pass · parziale"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9793-L9798"
prove:
  - "runtime/proofs/macrowin1/macrowin1.json"
  - "runtime/proofs/macrowin2/macrowin2.json"
---

## Domanda

i prezzi saltano subito e la deriva successiva è negoziabile (Fleming-Remolona)?

## Metodo e rubrica

Salto in bp da T0 a T0+1/5/15 minuti contro i giorni di controllo, persistenza, regola nel segno dei primi 5 minuti (netto 31,95 USD). Rubrica prima: sì (L9736, L10142).

## Esito

| Risultato | Fonte |
|---|---|
| MACROWIN-1 "Esito PASS, verdetto PARZIALE": "il risultato descrittivo del paper è confermato in entrambe le fasi (salto immediato 6-13 volte il normale, volatilità 2-3 volte per un'ora), la deriva negoziabile no": NFP 1 minuto 17,5 contro 2,9 bp (x6,0, t 5,8) in scoperta e 33,9 contro 3,5 (x9,8, t 8,4) in verifica | docs/EXECUTION_LEDGER.md#L9793-L9798 |
| regola NFP scoperta 43 giorni -73,4 USD/contratto (t -2,18), verifica -62,3 (t -1,64). | docs/EXECUTION_LEDGER.md#L9793-L9798 |
| MACROWIN-2 "Esito PASS, verdetto PARZIALE": salto dalle 8:30 ET a 1 minuto 6,1-13,0 volte i giorni normali (MNQ NFP 36,1 contro 5,3 bp in scoperta e 29,5 contro 4,5 in verifica; MNQ CPI 63,9 contro 5,3 e 44,1 contro 4,5) | docs/EXECUTION_LEDGER.md#L10150-L10157 |
| volatilità 8:30-9:30 ET 2,1-3,9 volte | docs/EXECUTION_LEDGER.md#L10150-L10157 |
| prima ora regolare 9:30-10:30 solo 1,10-1,22 volte | docs/EXECUTION_LEDGER.md#L9793-L9798 · docs/EXECUTION_LEDGER.md#L10150-L10157 |
| regole nette: "nessuna scelta in scoperta (q 0,978-0,993)", R1 su NFP negativa in tutte le 8 celle (MNQ -38,65 USD, t -2,13 in scoperta). | docs/EXECUTION_LEDGER.md#L10150-L10157 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- MACROWIN-1: "dopo l'annuncio ZN è un mercato da non inseguire"
- MACROWIN-2: "il fatto del calendario (CPI/NFP alle 7:30 CT) serve a dimensionare lo stop, non a scegliere il lato"
- la continuazione del CPI fino alle 9:30 "c'era nel 2020-2023 ed è sparita dopo il taglio".

## Prove

- runtime/proofs/macrowin1/macrowin1.json
- runtime/proofs/macrowin2/macrowin2.json
