---
id: "wfo-1"
titolo: "WFO-1 e WFO-1-LONG — ottimizzatore walk-forward che si ri-ottimizza da solo (metodo NinjaTrader riscritto)"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "MCL"
finestra: "MES, MNQ, MCL (genomi: MES 3.962, MNQ 3.962, MCL 3.832); WFO-1-LONG su MNQ 1 minuto NinjaTrader 2019-05..2026-10 (1.923 sessioni, 2,62 milioni di barre, 31 contratti)"
verdetto: "confermata"
pubblicabilita: "avvertenza"
avvertenza: "citare entrambi gli esiti insieme (confermato in-sample WFO-1, non confermato WFO-1-LONG)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L7817-L7828"
prove:
  - "runtime/proofs/wfo1/wfo1.json"
  - "runtime/proofs/wfo1/nt2026_mnq.json"
  - "runtime/proofs/wfo1/wfo_long.json"
  - "runtime/proofs/wfo1/wfo_long_MGCL.json"
  - "runtime/proofs/wfo1/wfo_long_M2KL.json"
  - "runtime/proofs/wfo1/wfo_long_M6EL.json"
  - "runtime/proofs/rizzo_wfo/step1.json"
---

## Ritiri e correzioni

- WFO-1 confermato in-sample, WFO-1-LONG NON confermato (L7817, L8129-L8136); H-NEXT-5 "di fatto risolta in negativo".

## Domanda

un ottimizzatore che sceglie ogni 20 sessioni il miglior "genoma" (strategia x timeframe x stop x RR x direzione x protezioni x fasi) sulle 250 precedenti produce profitto fuori campione?

## Metodo e rubrica

Finestra 250 sessioni, blocco 20, 3 funzioni obiettivo (F1 MaxNetProfit, F2 MaxStrength, F3 prudente media-1,645·σ/√n), placebo 200, BH q≤0,10 sui 9 test. Rubrica prima: sì (L7707, L7925).

## Esito

| Risultato | Fonte |
|---|---|
| WFO-1: MNQ F3 "prudente" (StrategyGenerator di NinjaTrader): "CONFERMATO": 163 sessioni fuori campione (9 riottimizzazioni), +36,01 USD per sessione, t 2,88 | docs/EXECUTION_LEDGER.md#L7817-L7828 |
| metà +8,05 e +63,63 | docs/EXECUTION_LEDGER.md#L7817-L7828 |
| placebo p95 16,41 | docs/EXECUTION_LEDGER.md#L7817-L7828 |
| q 0,02 | docs/EXECUTION_LEDGER.md#L7817-L7828 |
| dati mai usati 2026 (40 sessioni): 8 trade, +6,02 per sessione, t 0,19. | docs/EXECUTION_LEDGER.md#L7817-L7828 |
| Tutti gli altri NON confermati (MES F1 +4,90 t 1,21; MNQ F1 +16,88 t 0,53). | docs/EXECUTION_LEDGER.md#L7817-L7828 |
| WFO-1-LONG (storico MNQ mai usato 2020-05..2022-12, 695 sessioni): "NON CONFERMATO": +6,62 USD/sessione, t 1,45, metà +9,41 / +3,85 | docs/EXECUTION_LEDGER.md#L8129-L8135 |
| serie intera F3 -0,25/sessione | docs/EXECUTION_LEDGER.md#L8129-L8135 |
| per anno 2024 +17,38, 2025 -28,42 (257 sessioni). | docs/EXECUTION_LEDGER.md#L7817-L7828 · docs/EXECUTION_LEDGER.md#L8129-L8135 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "potenza minima" nei dati 2026
- MNQ ha solo 413 sessioni al secondo (9 passi)
- il genoma cambia spesso.
- Ipotesi H-NEXT-5 da provare in avanti (≥60 sessioni).
- Il ledger: "H-NEXT-5 (prova in avanti) è di fatto risolta in negativo sul 2025-2026 NinjaTrader. Nessun ottimizzatore confermato da usare con soldi; WFO-1 resta lo strumento di ricerca, non un sistema."

## Prove

- runtime/proofs/wfo1/wfo1.json
- runtime/proofs/wfo1/nt2026_mnq.json
- runtime/proofs/wfo1/wfo_long.json
- runtime/proofs/wfo1/wfo_long_MGCL.json
- runtime/proofs/wfo1/wfo_long_M2KL.json
- runtime/proofs/wfo1/wfo_long_M6EL.json
- runtime/proofs/rizzo_wfo/step1.json
