---
id: "harx-1"
titolo: "HARX-1 — previsione dell'ampiezza del giorno dopo (HAR e HAR-X)"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "M2K"
  - "MYM"
  - "SPY"
  - "QQQ"
finestra: "MES, MNQ, M2K, MYM (~1.020 previsioni dal 2023) e SPY/QQQ (2.732 previsioni dal 2016)"
verdetto: "confermato"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8452-L8455"
prove:
  - "runtime/proofs/harx1/harx1.json"
---

## Domanda

aggiungere la struttura a termine del VIX a un modello HAR migliora la previsione della varianza del giorno dopo?

## Metodo e rubrica

OLS a finestra espansa, perdita QLIKE, test di Diebold-Mariano con correzione di Holm. Rubrica prima: sì (L8441).

## Esito

| Risultato | Fonte |
|---|---|
| "CONFERMATO HAR + struttura a termine (log VIX/VIX3M, log VIX9D/VIX)": QLIKE MES 0,290 -> 0,242 (DM t 3,74, Holm p 0,003) | docs/EXECUTION_LEDGER.md#L8452-L8455 |
| MNQ 0,252 -> 0,224 (t 2,90, p 0,050) | docs/EXECUTION_LEDGER.md#L8452-L8455 |
| M2K 0,215 -> 0,190 (t 2,99, p 0,038) | docs/EXECUTION_LEDGER.md#L8452-L8455 |
| MYM 0,206 -> 0,175 (t 2,70, p 0,088). | docs/EXECUTION_LEDGER.md#L8452-L8455 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Lettura e limiti (dal registro)

- "le fasi aggiungono poco a ciò che l'HAR già sa dalla volatilità passata"
- sostituisce la media per fase.

## Prove

- runtime/proofs/harx1/harx1.json
