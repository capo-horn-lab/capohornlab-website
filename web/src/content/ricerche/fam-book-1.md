---
id: "fam-book-1"
titolo: "FAM-BOOK-1 — budget di rischio tra i 4 micro e tetto di posizioni per l'IBS"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "M2K"
  - "MYM"
finestra: "IBS-NT su MES, MNQ, M2K, MYM 2019-2026 (942 trade, gran parte già usati: prova descrittiva di gestione del rischio)"
verdetto: "senza verdetto nel registro"
pubblicabilita: "avvertenza"
avvertenza: "(importi in USD su 1 micro per indice: non indicano capitale consigliato)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9064-L9064"
prove:
  - "runtime/proofs/fambook1/fambook1.json"
---

## Domanda

pesare i micro per rischio (ERC) o limitare le posizioni (CAP2) migliora drawdown e giorno peggiore?

## Metodo e rubrica

Varianti BASE, ERC, CAP2, ERC+CAP2; bootstrap; adottata se drawdown e giorno peggiore migliorano ≥15% e il limite inferiore al 90% della differenza di Sharpe lo consente. Rubrica prima: sì (L9058).

## Esito

| Risultato | Fonte |
|---|---|
| "NESSUNA VARIANTE ADOTTATA secondo la rubrica; ERC vicina alla soglia": BASE Sharpe 1,40, netto 67.784 USD, drawdown massimo 7.189, giorno peggiore -3.297 | docs/EXECUTION_LEDGER.md#L9064-L9064 |
| ERC Sharpe 1,51 (diff +0,12, IC90 -0,03 / +0,28), drawdown 5.405 (-25%), giorno peggiore -2.918 (-11,5%) | docs/EXECUTION_LEDGER.md#L9064-L9064 |
| CAP2 574 trade Sharpe 1,00, netto dimezzato. | docs/EXECUTION_LEDGER.md#L9064-L9064 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "i giorni con molti segnali insieme rendono in media, quindi tagliarli costa più di quanto protegge"
- ERC candidata per prova in carta (H-NEXT-6-ERC).

## Prove

- runtime/proofs/fambook1/fambook1.json
