---
id: "macro-1"
titolo: "MACRO-1 — strategie sugli annunci macro (FOMC, CPI, NFP)"
data: "2026-10-19"
strumenti:
  - "M6E"
finestra: "indici micro, M6E, 2020-2026 (77 giorni NFP, 53 riunioni FOMC, 206 giorni di annunci)"
verdetto: "non confermata"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8532-L8538"
prove:
  - "runtime/proofs/macro1/macro1.json"
---

## Domanda

deriva pre-NFP, reversal/fade FOMC, rally con proiezioni, euro nel giorno FOMC, premio degli annunci.

## Metodo e rubrica

6 regole codificabili, ≥30 trade, t giorni≥2, placebo 200. Rubrica prima: sì (L8520).

## Esito

| Risultato | Fonte |
|---|---|
| "0 confermate su 6": C1 deriva pre-NFP -4,81 bp (t giorni -0,58) | docs/EXECUTION_LEDGER.md#L8532-L8538 |
| C4 reversal FOMC +8,4 (t 0,70, p95 13,2) | docs/EXECUTION_LEDGER.md#L8532-L8538 |
| C6 fade dopo FOMC +16,3 (t 0,76, p95 19,4) | docs/EXECUTION_LEDGER.md#L8532-L8538 |
| C11 premio annunci (206 giorni) -2,82 (t -0,28). | docs/EXECUTION_LEDGER.md#L8532-L8538 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "gli annunci macro non danno un vantaggio direzionale semplice; restano utili come eventi di ampiezza (regime) e come giorni da evitare".

## Prove

- runtime/proofs/macro1/macro1.json
