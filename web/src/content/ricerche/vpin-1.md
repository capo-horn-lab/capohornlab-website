---
id: "vpin-1"
titolo: "VPIN-1 — tossicità del flusso (Easley, López de Prado, O'Hara) su MES e MNQ"
data: "2026-10-20"
strumenti:
  - "MES"
  - "MNQ"
finestra: "MES 1.915 sessioni (103.403 secchi di volume) e MNQ 1.924 (103.329), 2019-05..2026-10"
verdetto: "pass · non confermata"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9715-L9721"
prove:
  - "runtime/proofs/vpin1/vpin1.json"
---

## Domanda

VPIN prevede la volatilità oltre l'HAR, il rendimento, o filtra l'IBS?

## Metodo e rubrica

Secchi di volume V=1/50 del volume mediano, 4 prove (volatilità oltre HAR, IC con rendimento, filtro IBS, classificatore su 4 settimane di tick); BH q 0,10. Rubrica prima: sì (L9673).

## Esito

| Risultato | Fonte |
|---|---|
| "Esito PASS, verdetto NON CONFERMATA sull'intera famiglia (0 su 4)". | docs/EXECUTION_LEDGER.md#L9715-L9721 |
| Prova 1: MES verifica beta 0,32 t 0,53 (placebo p95 1,87, R² aggiunto 0,0002) | docs/EXECUTION_LEDGER.md#L9715-L9721 |
| "VPIN non aggiunge nulla alla volatilita' passata: NON CONFERMATA (q 0,64)". | docs/EXECUTION_LEDGER.md#L9715-L9721 |
| Prova 3: MES verifica i trade IBS con VPIN alto rendono di più (terzile alto 39 trade +160,9 USD) | docs/EXECUTION_LEDGER.md#L9715-L9721 |
| regola F 46 trade 38,9 contro piena 85 trade 94,9 | docs/EXECUTION_LEDGER.md#L9715-L9721 |
| differenza -56,0 USD (t -1,37). | docs/EXECUTION_LEDGER.md#L9715-L9721 |
| Prova 4: correlazione tra sbilancio con regola del tick e BVC 0,54 (MES) e 0,63 (MNQ). | docs/EXECUTION_LEDGER.md#L9715-L9721 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Lettura e limiti (dal registro)

- "è la volatilità passata travestita"
- "Nessun cancello VPIN per il bot: su MES toglierebbe i trade migliori"
- il VPIN non è stazionario con il volume dei micro.

## Prove

- runtime/proofs/vpin1/vpin1.json
