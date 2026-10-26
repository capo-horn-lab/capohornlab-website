---
id: "hmm-1"
titolo: "HMM-1 — HMM di regime e filtro di Kalman come filtri dell'IBS"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "M2K"
  - "MYM"
finestra: "MES, MNQ, M2K, MYM NinjaTrader 2019-2026 (714 trade IBS dopo i primi 500 giorni)"
verdetto: "confermata"
pubblicabilita: "avvertenza"
avvertenza: "\"CONFERMATO secondo la rubrica\" ma migliora la qualità per trade, non il guadagno totale; usato solo come variante in carta."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8394-L8399"
prove:
  - "runtime/proofs/hmm1/hmm1.json"
---

## Domanda

un filtro di regime (HMM a 2 stati, Kalman) migliora l'IBS?

## Metodo e rubrica

3 regole dichiarate; CONFERMATO se ≥60 trade, media e Sharpe maggiori dell'IBS non filtrato, DSR(N=20)≥0,95, PSR≥0,95. Rubrica prima: sì (L8384).

## Esito

| Risultato | Fonte |
|---|---|
| (a) IBS solo con P(calmo)≥0,5: "CONFERMATO secondo la rubrica": 503 trade +34,47 bp (t 4,95), scartati 211 +24,69, DSR 0,972 | docs/EXECUTION_LEDGER.md#L8394-L8399 |
| (b) P(calmo)<0,5: 211 trade +24,69 (t 1,45), DSR 0,331: no | docs/EXECUTION_LEDGER.md#L8394-L8399 |
| (c) z Kalman ≤ -1: 131 trade -6,23 bp (t -0,27): peggiora. | docs/EXECUTION_LEDGER.md#L8394-L8399 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "migliora la qualità per trade, non il guadagno" (netto totale ~17.300 bp contro ~22.500)
- entra solo come variante in carta (H-NEXT-6a).

## Prove

- runtime/proofs/hmm1/hmm1.json
