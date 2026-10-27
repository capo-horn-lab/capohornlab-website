---
id: "ibs-nt"
titolo: "IBS-NT, IBS-MYM, IBS-EU, L38, L40 — la regola IBS sui future (e H-NEXT-6 in carta)"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "M2K"
  - "MYM"
  - "FESX"
  - "FDXM"
finestra: "MES e MNQ 2025-01-01..2026-10-16, M2K 2019-05..2026-10, MYM 2019-05..2026-10 (2,54 milioni di barre), FESX (1,61 milioni) e FDXM (1,59 milioni) 2019-2026"
verdetto: "IBS-NT: confermata"
audit: {"stato": "nota", "id": ["IBS-NT"]}
pubblicabilita: "avvertenza"
avvertenza: "Dati NinjaTrader solo aggregati."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8216-L8222"
prove:
  - "runtime/proofs/ibsnt/ibsnt.json"
  - "runtime/proofs/ibsnt/mym.json"
  - "runtime/proofs/ibsnt/eu.json"
  - "runtime/proofs/ibsnt/regime.json"
  - "runtime/proofs/ibsnt/portfolio.json"
---

## Ritiri e correzioni

- IBS-NT regge "con margine sottile" (L8966): t sui giorni d'ingresso 2,22, placebo p95 27,3 contro media 28,8; poggia soprattutto su M2K (MES t 1,48, MNQ 0,77); parte del guadagno è il rialzo di fondo (placebo medio +10,6 bp, L8222). H-NEXT-6 (prova in carta) NON ha esito.

## Domanda

la regola IBS<0,20 -> lungo (uscita IBS>0,90 o 5ª sessione), confermata su SPY/QQQ (H-NEXT-4b), regge sui future micro con costi reali e su altri mercati?

## Metodo e rubrica

Regola invariata (sig-2 ibs_only, motore LAB-2), ≥30 trade, media>0, t≥2, sopra il p95 di 200 placebo, +1 tick, BH. Rubrica prima: sì (L8205, L8236, L8274).

## Esito

| Risultato | Fonte |
|---|---|
| IBS-NT: "CONFERMATA sull'insieme; nessun singolo strumento ha potenza sufficiente": insieme 333 trade, +28,8 bp/trade, t 2,43, 54,7% vincenti, profit factor 1,44, q 0,031, placebo p95 27,3 ("battuto di poco") | docs/EXECUTION_LEDGER.md#L8216-L8222 |
| MES 47 trade +91,53 USD t 1,42 q 0,108 | docs/EXECUTION_LEDGER.md#L8216-L8222 |
| MNQ 43 trade +85,86 t 0,67 | docs/EXECUTION_LEDGER.md#L8216-L8222 |
| M2K 243 trade +23,72 t 1,63. | docs/EXECUTION_LEDGER.md#L8216-L8222 |
| IBS-MYM: "CONFERMATA": 238 trade, +66,58 USD/trade (+39,7 bp), t 3,95, 67,2% vincenti, profit factor 1,93, drawdown massimo 1.862 USD, placebo p95 45,69. | docs/EXECUTION_LEDGER.md#L8243-L8248 |
| IBS-EU: "NON confermata su nessuno dei 2": FESX 232 trade -8,26 EUR t -0,14 | docs/EXECUTION_LEDGER.md#L8282-L8285 |
| FDXM 208 trade -101,56 EUR t -0,86. | docs/EXECUTION_LEDGER.md#L8282-L8285 |
| L38 (descrittivo): 892 trade, +42,16 bp/trade, t 6,34, 64,5% vincenti, profit factor 1,78 (periodi già usati: "non è una prova") | docs/EXECUTION_LEDGER.md#L8257-L8272 |
| VIX/VIX3M>1: 72 trade +148,7 bp (t 4,79) contro +32,8. | docs/EXECUTION_LEDGER.md#L8257-L8272 |
| L40 (descrittivo): 942 trade, netto +67.589 USD, nessun anno negativo | docs/EXECUTION_LEDGER.md#L8257-L8272 |
| giorni peggiori 27/02/2025 -3.297, 07/08/2024 -2.849 USD | docs/EXECUTION_LEDGER.md#L8257-L8272 |
| 4 indici aperti insieme il 16% dei giorni. | docs/EXECUTION_LEDGER.md#L8257-L8272 |

## Grafico

Serie per anno dal file di prova runtime/proofs/ibsnt/portfolio.json (chiave anni). Contenuto del file secondo l'inventario: L40 portafoglio IBS 4 micro: netto per anno, giorno peggiore, giorni peggiori, drawdown, posizioni aperte insieme, correlazione giornaliera

## Cosa NON dice

- "L'effetto confermato è degli indici USA... non come una regola universale"
- "Margine sul placebo stretto: una parte del guadagno è il rialzo di fondo (placebo medio +10,6 bp)"
- "l'edge più solido trovato dal progetto"
- L38/L40 solo descrittivi, nessun conto con questi risultati come prova.

## Prove

- runtime/proofs/ibsnt/ibsnt.json
- runtime/proofs/ibsnt/mym.json
- runtime/proofs/ibsnt/eu.json
- runtime/proofs/ibsnt/regime.json
- runtime/proofs/ibsnt/portfolio.json
