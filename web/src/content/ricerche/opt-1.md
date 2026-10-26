---
id: "opt-1"
titolo: "OPT-1 e OPT-2 — indicatori dalle options (put/call, SKEW, VVIX, VIX9D/VIX) come segnali"
data: "2026-10-19"
strumenti:
  - "SPY"
  - "QQQ"
  - "MES"
  - "MNQ"
finestra: "SPY e QQQ (put/call Cboe 2006-11..2019-10, TS9 da 2011), MES/MNQ 2019-2026"
verdetto: "misto"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8073-L8079"
prove:
  - "runtime/proofs/opt1/opt1.json"
  - "runtime/proofs/opt1/opt2.json"
---

## Domanda

"dopo la paura il rimbalzo" è misurabile? TS9 alto è un setup raro a 5 giorni?

## Metodo e rubrica

IC di Spearman a 5 giorni, Newey-West 5 ritardi, BH q≤0,10 su 10 test (OPT-1); regola fissa z(TS9)≥1,5 -> lungo a 5 giorni, 4 test (OPT-2). Rubrica prima: sì (L8063, L8081).

## Esito

| Risultato | Fonte |
|---|---|
| OPT-1: "6 confermati su 10, tutti con verso 'dopo la paura il rimbalzo'": PC_EQ verifica IC +0,125 (t 2,37) SPY e QQQ | docs/EXECUTION_LEDGER.md#L8073-L8079 |
| PC_TOT +0,163 (t 3,18) SPY | docs/EXECUTION_LEDGER.md#L8073-L8079 |
| TS9 +0,109 (t 2,58) SPY. | docs/EXECUTION_LEDGER.md#L8073-L8079 |
| SKEW e VVIX non confermati. | docs/EXECUTION_LEDGER.md#L8073-L8079 · docs/EXECUTION_LEDGER.md#L8090-L8094 |
| OPT-2: "0 confermati su 4": MES 50 segnali, verifica 18 trade +159,14 USD (t 0,80), placebo p95 306,64 | docs/EXECUTION_LEDGER.md#L8073-L8079 · docs/EXECUTION_LEDGER.md#L8090-L8094 |
| SPY 107 segnali verifica +43,65 bp (t 0,89), placebo p95 80,15. | docs/EXECUTION_LEDGER.md#L8073-L8079 · docs/EXECUTION_LEDGER.md#L8090-L8094 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "Un IC positivo può venire dal rialzo di fondo"
- il put/call gratuito finisce il 2019-10-04 (non usabile dal vivo)
- la relazione continua non dà un setup raro.

## Prove

- runtime/proofs/opt1/opt1.json
- runtime/proofs/opt1/opt2.json
- runtime/research/cboe/
