---
id: "lab-1"
titolo: "LAB-1 — laboratorio strategie su tutti i contratti e tutto lo storico locale"
data: "2026-10-16"
strumenti:
  - "ES"
  - "NQ"
  - "CL"
finestra: "ES 1m 2020-2024, NQ 1m 2023-2024 (+ trade tick con aggressore), CL MBP-1 2024-2025, export NinjaTrader 2026"
verdetto: "senza verdetto nel registro"
pubblicabilita: "avvertenza"
avvertenza: "costi provvisori."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L6139-L6146"
prove:
  - "runtime/proofs/lab/lab.json"
  - "docs/research/LAB_STRATEGIE_2026-10-16.md"
  - "runtime/history/macro-events.json"
---

## Domanda

quali delle 125 coppie strategia x strumento sono profittevoli con piano canonico, e dove smettono di funzionare?

## Metodo e rubrica

Piano unico (stop 2 ATR, scala 1/1.5/2/3 R, 4 micro, break-even dopo TP2, uscita 60 min, 1 USD/lato PROVVISORIO), scoperta 60% / verifica 40%, placebo 200, BH q≤0,10; condizioni, fasce di volatilità, hedge, eventi. Rubrica prima: sì ("congelata PRIMA dei risultati", L6107).

## Esito

| Risultato | Fonte |
|---|---|
| "0 strategie ADOTTATE su 125 strategia x strumento; 0 condizioni confermate (5 candidate in scoperta, 4 negative in verifica)". | docs/EXECUTION_LEDGER.md#L6139-L6146 |
| Più vicina: ES FVG verifica 750 trade +16.06 USD (4 MES) t 2.08, placebo battuti 100%, fallisce solo BH (q 0.999). | docs/EXECUTION_LEDGER.md#L6139-L6146 |
| Hedge: 16 su 65 rispettano la regola, ma su strategie non adottate. | docs/EXECUTION_LEDGER.md#L6139-L6146 |
| Eventi: ES CPI volatilità prima -> ampiezza dopo Spearman 0.48 p 0.0001, direzione no | docs/EXECUTION_LEDGER.md#L6139-L6146 |
| 94.5% delle mezz'ore più ampie di ES non su FOMC/CPI/NFP. | docs/EXECUTION_LEDGER.md#L6139-L6146 |

## Cosa NON dice

- "una strategia non profittevole non si adotta"
- 12 giornate non programmate con cause da fonti pubbliche
- calendario EIA non scaricato (BLOCKED/NOT_RUN).

## Prove

- runtime/proofs/lab/lab.json
- docs/research/LAB_STRATEGIE_2026-10-16.md
- runtime/history/macro-events.json
