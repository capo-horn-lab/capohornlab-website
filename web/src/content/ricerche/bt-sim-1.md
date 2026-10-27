---
id: "bt-sim-1"
titolo: "BT-SIM-1 — backtest figurativo a 10.000 EUR sui soli segnali dello screener"
data: "2026-09-28"
strumenti:
  - "ES"
finestra: "strumento ES 1 minuto, anno 2024 intero (354.799 barre)"
verdetto: "senza verdetto nel registro"
pubblicabilita: "avvertenza"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L2287-L2347"
prove:
  - "docs/evidence/BT-SIM-1-results.json"
  - "docs/evidence/BT-SIM-1-statistiche.md"
---

## Domanda

una regola meccanica guidata solo dai 28 riquadri dello screener, tarata sulla prima metà del 2024 e misurata sulla seconda metà, guadagna al netto dei costi?

## Metodo e rubrica

Motore `backtest.py`; taratura in-sample (1ª metà 2024), risultato riportato out-of-sample (2ª metà), costi (0,62 USD per lato, 1 tick di slittamento per lato) e slittamento espliciti; controllo a segnale invertito. Rubrica fissata prima: sì (criteri di accettazione 1-8 scritti all'apertura, L2087).

## Esito

| Risultato | Fonte |
|---|---|
| Nessun verdetto PASS/FAIL di strategia: esplorazione. | docs/EXECUTION_LEDGER.md#L2287-L2347 |
| Netto fuori campione: 1m 503 op. **-1.678,06 EUR** (-16,78%), DD 21,17%; 5m 181 op. **+1.710,03 EUR** (+17,10%), DD 9,64%; 15m 72 op. **+1.961,42 EUR** (+19,61%), DD 3,71%. | docs/EXECUTION_LEDGER.md#L2287-L2347 |
| Stesse operazioni senza attrito: +2.276,64 / +2.596,55 / +2.252,31 EUR | docs/EXECUTION_LEDGER.md#L2287-L2347 |
| attrito 4.271 / 957 / 314 USD. | docs/EXECUTION_LEDGER.md#L2287-L2347 |
| Segnale invertito perde di più in tutti e tre. | docs/EXECUTION_LEDGER.md#L2287-L2347 |

## Cosa NON dice

- Testo del ledger: "esplorazione, non convalida"
- un anno, uno strumento, un regime
- il secondo semestre 2024 fu di tendenza rialzista, "il periodo ha fatto la parte maggiore del lavoro"
- la costanza del lordo è "compatibile" con la spiegazione dell'attrito, non una dimostrazione.

## Prove

- docs/evidence/BT-SIM-1-results.json
- docs/evidence/BT-SIM-1-statistiche.md
