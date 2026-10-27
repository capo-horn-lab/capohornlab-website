---
id: "param-1"
titolo: "PARAM-1 e PARAM-2 — ottimizzatore parametrico per fase (EMA + RSI), entrata/volatilità/timeframe"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "MCL"
finestra: "MES, MNQ, MCL; PARAM-1: 51.840 genomi EMA+RSI x filtri (MES 42.720, MNQ 41.688, MCL 40.514 con trade); PARAM-2: 3.456 combinazioni per strumento (3 metodi di entrata)."
verdetto: "verdetto non estratto: vedi Esito"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L7904-L7911"
prove:
  - "runtime/proofs/param1/param1.json"
  - "runtime/proofs/param2/param2.json"
---

## Domanda

ottimizzare i parametri per ciascuna delle 12 fasi batte l'ottimizzazione senza fasi?

## Metodo e rubrica

Walk-forward mobile (250/20) e ancorato, F1/F2/F3, placebo 100-200, BH q≤0,10 su 18 (PARAM-1) e 12 (PARAM-2) test. Rubrica prima: sì (L7770, L7838).

## Esito

| Risultato | Fonte |
|---|---|
| PARAM-1: "0 confermati su 18" | docs/EXECUTION_LEDGER.md#L7937-L7943 |
| "dividere per 12 fasi PEGGIORA in 13 casi su 18 rispetto al senza fasi" (≈21 sessioni per fase). | docs/EXECUTION_LEDGER.md#L7937-L7943 |
| PARAM-2: "0 confermati su 12" | docs/EXECUTION_LEDGER.md#L7904-L7911 |
| media dei trade per metodo di entrata (USD): MES mercato -1,22, limite -2,83, conferma -4,51 | docs/EXECUTION_LEDGER.md#L7904-L7911 |
| MNQ F3 mobile +21,10 (t 1,64, placebo p95 8,98), ancorato +17,11 (t 1,31), "t sotto 2 con 163 sessioni" | docs/EXECUTION_LEDGER.md#L7904-L7911 |
| MCL tutti negativi (da -7,96 a -12,77). | docs/EXECUTION_LEDGER.md#L7904-L7911 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Lettura e limiti (dal registro)

- "Entrare con limite o stop di conferma non migliora l'EMA + RSI"
- con F1 l'ottimizzatore "insegue i vincitori del passato e perde".

## Prove

- runtime/proofs/param1/param1.json
- runtime/proofs/param2/param2.json
