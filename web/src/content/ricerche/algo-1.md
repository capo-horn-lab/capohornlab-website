---
id: "algo-1"
titolo: "ALGO-1 — strategie dai repository open source (hummingbot, nautilus, lumibot, backtrader)"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "MCL"
finestra: "MES, MNQ, MCL; 15 test (5 strategie x 3 strumenti)"
verdetto: "senza verdetto nel registro"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L7539-L7539"
prove:
  - "runtime/proofs/algo1/algo1.json"
  - "docs/research/ALGO_REPOS_2026-10-19.md"
---

## Domanda

le regole dei sorgenti dei repository funzionano su futures micro?

## Metodo e rubrica

Rubrica LAB-2 (scoperta 60/verifica 40, placebo, BH, +1 tick). Rubrica prima: sì (L7483).

## Esito

| Risultato | Fonte |
|---|---|
| "0 ADOTTATE su 15". | docs/EXECUTION_LEDGER.md#L7539-L7539 |
| Bollinger+MACD e Bollinger+RSI negativi ovunque (BB+RSI MES verifica -6,18 USD t -4,53) | docs/EXECUTION_LEDGER.md#L7539-L7539 |
| buy the dip MES verifica +72,16 t 2,69 ma scoperta +0,47 e sotto il p95 dei placebo lunghi (85,83): "la deriva rialzista spiega il risultato". | docs/EXECUTION_LEDGER.md#L7539-L7539 · docs/EXECUTION_LEDGER.md#L7541-L7541 |

## Cosa NON dice

- —

## Prove

- runtime/proofs/algo1/algo1.json
- docs/research/ALGO_REPOS_2026-10-19.md
