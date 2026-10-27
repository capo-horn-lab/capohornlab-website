---
id: "h-next-4b"
titolo: "H-NEXT-4b — IBS su SPY e QQQ giornalieri (dati mai usati 2006-2019)"
data: "2026-10-18"
strumenti:
  - "SPY"
  - "QQQ"
finestra: "SPY e QQQ giornalieri rettificati da Yahoo, 2006-2019 (principale), 2025-2026 (nuovo), 2020-2024 (descrittivo)"
verdetto: "senza verdetto nel registro"
audit: {"stato": "nota", "id": ["H-NEXT-4b"]}
pubblicabilita: "avvertenza"
avvertenza: "risultato forte ma effetto già noto in letteratura"
fonte_ledger: "docs/EXECUTION_LEDGER.md#L7277-L7293"
prove:
  - "runtime/proofs/sig2/ibs_etf.json"
  - "runtime/research/spy_qqq_ohlc.csv"
---

## Ritiri e correzioni

- H-NEXT-4b: placebo corretto prima del verdetto (L7289)

## Domanda

la regola IBS<0,20 -> lungo, uscita IBS>0,90 o 5ª sessione, regge su dati mai usati?

## Metodo e rubrica

Regola SIG-2 B1b senza modifiche; costo 2 bp; placebo 200; BH q≤0,10 su 4 test; ≥30 trade, t≥2. Rubrica prima: sì (L7250).

## Esito

| Risultato | Fonte |
|---|---|
| "CONFERMATA su 2006-2019 per entrambi": SPY 374 trade +47,1 bp netti t 4,32, 67% vincenti, placebo p95 33,8, q<0,001 (negativo solo il 2018) | docs/EXECUTION_LEDGER.md#L7277-L7293 |
| QQQ 375 trade +40,7 bp t 3,29, q 0,001. | docs/EXECUTION_LEDGER.md#L7277-L7293 |
| "Non confermata sul 2025-2026 (39 trade a testa, bassa potenza)": SPY +20,5 bp t 0,76 | docs/EXECUTION_LEDGER.md#L7277-L7293 |
| QQQ +16,2 bp t 0,47. | docs/EXECUTION_LEDGER.md#L7277-L7293 |
| Descrittivo 2020-2024: SPY +54,4 bp (t 3,15) | docs/EXECUTION_LEDGER.md#L7277-L7293 |
| QQQ +91,8 (t 4,67). | docs/EXECUTION_LEDGER.md#L7277-L7293 |

## Cosa NON dice

- "È la prima regola del progetto confermata su dati mai usati"
- limite: "l'IBS è un effetto pubblicato da anni proprio su SPY. Il periodo è nuovo per noi, non per la letteratura."
- Placebo corretto prima del verdetto.

## Prove

- runtime/proofs/sig2/ibs_etf.json
- runtime/research/spy_qqq_ohlc.csv
