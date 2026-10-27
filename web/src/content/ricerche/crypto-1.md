---
id: "crypto-1"
titolo: "CRYPTO-1 e CRYPTO-2 — regole su bitcoin (spot e future micro)"
data: "2026-10-19"
strumenti:
  - "BTC"
  - "MBT"
finestra: "BTC-USD giornaliero Yahoo 2014-09-17..2026-10-18 (4.414 giorni, 20 bp a giro) e MBT 1 minuto NinjaTrader 2021-05..2026-10 (1,34 milioni di barre)"
verdetto: "confermato · non confermato"
pubblicabilita: "avvertenza"
avvertenza: "(Yahoo/NinjaTrader solo aggregati; non è consulenza su criptovalute)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8504-L8510"
prove:
  - "runtime/proofs/crypto1/crypto1.json"
  - "runtime/proofs/crypto2/crypto2.json"
---

## Domanda

medie mobili, nuovi massimi, effetto lunedì, crollo e "famiglia" MR funzionano sul bitcoin?

## Metodo e rubrica

12 test (CRYPTO-1), solo lunghi, regole come pubblicate; ≥30 trade, t≥2, placebo con le stesse durate, DSR, BH. CRYPTO-2: SMA50 su MBT 2021-07..2026-10. Rubrica prima: sì (L8492, L8547).

## Esito

| Risultato | Fonte |
|---|---|
| CRYPTO-1: "1 confermato su 12": SMA50, 111 periodi +1.044 bp (t 2,23, placebo media 524, p95 924, DSR 0,982, q 0,025) | docs/EXECUTION_LEDGER.md#L8504-L8510 |
| molto più forte nel 2014-2020 (+1.972) che nel 2021-2026 (+225) | docs/EXECUTION_LEDGER.md#L8504-L8510 |
| la "nostra famiglia" sul bitcoin: IBS 482 trade -1,35 bp (t -0,05). | docs/EXECUTION_LEDGER.md#L8504-L8510 |
| CRYPTO-2: "NON CONFERMATO": SMA50 su MBT 46 periodi, +191,5 bp (t 0,97, p95 462,3) | docs/EXECUTION_LEDGER.md#L8504-L8510 · docs/EXECUTION_LEDGER.md#L8554-L8557 |
| Sharpe giornaliero 0,53 contro comprare e tenere 0,54 | docs/EXECUTION_LEDGER.md#L8554-L8557 |
| rendimento +72,2% contro +79,4%. | docs/EXECUTION_LEDGER.md#L8554-L8557 |

## Grafico

Serie per anno dal file di prova runtime/proofs/crypto2/crypto2.json (chiave anni).

## Cosa NON dice

- "il bitcoin è l'opposto degli indici USA: premia il trend... non la mean reversion"
- "Nessuna strategia crypto per il bot."

## Prove

- runtime/proofs/crypto1/crypto1.json
- runtime/proofs/crypto2/crypto2.json
