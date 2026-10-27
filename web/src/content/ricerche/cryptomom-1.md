---
id: "cryptomom-1"
titolo: "CRYPTOMOM-1 — momentum settimanale e attenzione sul bitcoin (Liu-Tsyvinski)"
data: "2026-10-20"
strumenti:
  - "BTC"
  - "ETH"
  - "MBT"
finestra: "BTC 631 settimane (2014-09..2026-10), ETH 467 settimane, MBT 284 settimane (2021-05..2026-10)"
verdetto: "pass · parziale"
pubblicabilita: "avvertenza"
avvertenza: "(non è consulenza sulle criptovalute)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9776-L9781"
prove:
  - "runtime/proofs/cryptomom1/cryptomom1.json"
  - "runtime/proofs/cryptomom1/crypto_daily_vol.csv"
---

## Domanda

il rendimento della settimana corrente prevede le 1-4 seguenti?

## Metodo e rubrica

Regressioni e regole R1/R2/R1-4, BH q 0,10, placebo; costi MBT 0,35 USD per lato + 1 tick. Rubrica prima: sì (L9723).

## Esito

| Risultato | Fonte |
|---|---|
| "Esito PASS, verdetto PARZIALE": momentum a 4 settimane (R1-4) CONFERMATO sullo spot BTC ed ETH 2021-2026 (BTC verifica 78,4 bp/settimana, t 2,53, Sharpe 1,05, drawdown 29%, placebo 64,2, q 0,037; 2 righe su 12) e NON sul future MBT (t 1,47). | docs/EXECUTION_LEDGER.md#L9776-L9781 |
| Proxy dell'attenzione (volume): "NON CONFERMATA", IC tra -0,03 e +0,05. | docs/EXECUTION_LEDGER.md#L9776-L9781 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Lettura e limiti (dal registro)

- "Nessuna strategia crypto per il bot"
- in scoperta l'effetto non c'era (BTC k1 t 0,6): "l'effetto è del periodo recente".

## Prove

- runtime/proofs/cryptomom1/cryptomom1.json
- runtime/proofs/cryptomom1/crypto_daily_vol.csv
