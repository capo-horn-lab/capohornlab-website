---
id: "auct-1"
titolo: "AUCT-1 — calo prima e recupero dopo le aste dei Treasury"
data: "2026-10-19"
strumenti:
  - "IEF"
  - "TLT"
finestra: "IEF (10 anni) e TLT (30 anni), 314 aste a 10 anni e 232 a 30 anni dal 2006 (con riaperture)"
verdetto: "senza verdetto nel registro"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8179-L8186"
prove:
  - "runtime/proofs/auct1/auct1.json"
---

## Domanda

il prezzo cala prima delle aste e recupera dopo (Robeco; Lou-Yan-Zhang)?

## Metodo e rubrica

4 test (prima/dopo x IEF/TLT), netto 2 bp, scoperta 60/verifica 40, placebo 200. Rubrica prima: sì (L8169). Correzione: prima lettura con sole aste originali (L8177).

## Esito

| Risultato | Fonte |
|---|---|
| "0 confermati su 4." | docs/EXECUTION_LEDGER.md#L8179-L8186 |
| Con riaperture: IEF corto prima -0,42 / +14,72 bp (t 1,99), placebo p95 9,95 | docs/EXECUTION_LEDGER.md#L8179-L8186 |
| TLT corto prima +22,73 (t 1,50) / +42,28 (t 1,99), placebo p95 41,14 | docs/EXECUTION_LEDGER.md#L8179-L8186 |
| IEF lungo dopo +16,44 (t 2,55) / -3,52. | docs/EXECUTION_LEDGER.md#L8179-L8186 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "il recupero dopo l'asta, forte fino al 2018, è sparito"
- il calo prima si vede ancora ma non passa la soglia.

## Prove

- runtime/proofs/auct1/auct1.json
- runtime/research/treasury/
