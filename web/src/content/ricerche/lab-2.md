---
id: "lab-2"
titolo: "LAB-2 — claim di profitto da forum e paper, su più timeframe (con LAB-2-OOS e correzione IC)"
data: "2026-10-17"
strumenti:
  - "MNQ"
  - "MCL"
  - "MES"
finestra: "MNQ (base 1 s, 2023-01-01..2024-08-15), MCL (base 1 s, 2024-01..2025-12), MES (1 m, 2020-2024)"
verdetto: "pass · fail · not_run · non adottata"
audit: {"stato": "corretto", "id": ["LAB-2"]}
pubblicabilita: "avvertenza"
avvertenza: "i claim sono di terzi; Reddit via archivio pubblico; dati licenziati solo aggregati."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L6306-L6334"
prove:
  - "runtime/proofs/lab2/lab2.json"
  - "runtime/proofs/lab2/digest.json"
  - "runtime/proofs/lab2/oos.json"
  - "runtime/proofs/lab2/tables.md"
  - "docs/research/LAB2_MULTITIMEFRAME_2026-10-17.md"
---

## Ritiri e correzioni

- LAB-2, studio IC (L6409): "864 IC confermati" era "in gran parte un artefatto" del metodo (correlazione dentro la giornata); rifatto con `pooled_ic`; file distorto `lab2/lab2-ic-biased.json` da non usare. I test delle strategie non sono toccati.

## Domanda

i claim di profitto pubblicati (ORB5, Noise area, Last half hour, Overnight, MACD+EMA200, Supertrend, RSI2, Turtle, SMA20, ICT Silver Bullet) reggono su 1 s-1 h con costi reali?

## Metodo e rubrica

Regole prese dal claim e mai ottimizzate; scoperta 60% / verifica 40%; placebo 200; BH q≤0,10; +1 tick per lato; costi dal template NinjaTrader (MES 0,95, MNQ 0,95, MCL 1,10 USD per lato); controllo lookahead. Rubrica prima: sì ("congelata PRIMA di qualsiasi backtest", L6177).

## Esito

| Risultato | Fonte |
|---|---|
| "0 ADOTTATE su 274 test; 29 positivi nei due periodi, nessuno con t >= 2 e q <= 0,10"; "1 s-15 s: 0 test positivi su 72 anche al lordo (2.056.183 trade in verifica)". | docs/EXECUTION_LEDGER.md#L6306-L6334 |
| LAB-2-OOS: "0 ipotesi confermate su 8, in entrambi i periodi" (NQ 1m 16/08-31/12/2024, 95 sessioni; MNQ 12-26 2026, 40 sessioni), q BH ≥ 0,40 e ≥ 0,59. | docs/EXECUTION_LEDGER.md#L6306-L6334 |
| R2 ICT Silver Bullet: MES verifica 1164 trade -1,44 t -0,74 | docs/EXECUTION_LEDGER.md#L6432-L6432 |
| MNQ verifica 389 -9,38 t -1,53: NON ADOTTATA. | docs/EXECUTION_LEDGER.md#L6433-L6433 |

## Cosa NON dice

- Testo: "Con circa 95 e 55 sessioni la potenza è bassa: un esito negativo o non significativo non è una conferma."
- CORREZIONE DICHIARATA: lo studio IC "864 IC confermati" era "in gran parte un artefatto" (correlazione di rango dentro ogni giornata: su passeggiata casuale IC fino a -0,43, t fino a -12)
- rifatto con `pooled_ic`

## Prove

- runtime/proofs/lab2/lab2.json
- runtime/proofs/lab2/digest.json
- runtime/proofs/lab2/oos.json
- runtime/proofs/lab2/tables.md
- docs/research/LAB2_MULTITIMEFRAME_2026-10-17.md
