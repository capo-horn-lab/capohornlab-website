---
id: "trend-1"
titolo: "TREND-1 e VRP-1 — trend multi-mercato mensile; premio di volatilità"
data: "2026-10-19"
strumenti:
  - "SPY"
  - "QQQ"
  - "VIX"
finestra: "17 ETF Yahoo 2006-2026 (2,93 MB) per TREND-1; SPY/QQQ + VIX per VRP-1."
verdetto: "senza verdetto nel registro"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8105-L8108"
prove:
  - "runtime/proofs/trend1/trend1.json"
  - "runtime/proofs/vrp1/vrp1.json"
---

## Domanda

TSMOM 12-1 e Faber 10 mesi funzionano dopo la pubblicazione? Il premio di varianza (VIX²/12 - varianza realizzata 21 sessioni) prevede i rendimenti a 5 e 22 giorni?

## Metodo e rubrica

TREND-1: scoperta 60/verifica 40 dei mesi, placebo 200; VRP-1: IC di Spearman, Newey-West, BH q≤0,10 su 4 test. Rubrica prima: sì (L8096, L8110).

## Esito

| Risultato | Fonte |
|---|---|
| TREND-1: "0 confermati su 2" (TSMOM 12-1, 16 mercati, 236 mesi: scoperta +82,99 bp (Sharpe 0,61), verifica +51,89 bp (t 1,04); Faber: drawdown 10,3% contro 16,2% sempre investito, Sharpe 1,06 contro 1,18). | docs/EXECUTION_LEDGER.md#L8105-L8108 |
| VRP-1: "0 confermati su 4, tutti con il segno atteso": SPY 5 giorni scoperta IC +0,068 (t 2,09), verifica +0,038 (t 0,96) | docs/EXECUTION_LEDGER.md#L8105-L8108 · docs/EXECUTION_LEDGER.md#L8118-L8118 |
| SPY 22 giorni +0,130 (t 2,55) / +0,079 (t 1,14). | docs/EXECUTION_LEDGER.md#L8118-L8118 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- VRP: "effetto noto e coerente ma sotto la soglia di verifica"
- Bollerslev-Tauchen-Zhou citato a memoria, non riletto.

## Prove

- runtime/proofs/trend1/trend1.json
- runtime/proofs/vrp1/vrp1.json
