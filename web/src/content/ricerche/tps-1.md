---
id: "tps-1"
titolo: "TPS-1 — ingresso a scaglioni di Connors sulla regola IBS"
data: "2026-10-19"
strumenti:
  - "SPY"
  - "QQQ"
finestra: "SPY e QQQ giornalieri 2006-2018"
verdetto: "confermata"
pubblicabilita: "avvertenza"
avvertenza: "(adozione per la sola carta, non edge nuovo)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9099-L9099"
prove:
  - "runtime/proofs/tps1/tps1.json"
---

## Domanda

aggiungere una seconda unità se la chiusura scende ancora (scaling-in) migliora il rendimento per unità esposta?

## Metodo e rubrica

Base 1 unità vs TPS; adottata (per la carta) se bp/unità ≥ base e IC90 della differenza di Sharpe > -0,2. Rubrica prima: sì (L9092).

## Esito

| Risultato | Fonte |
|---|---|
| "ADOTTATA secondo la rubrica, con una riserva dichiarata": base 698 unità +40,7 bp, Sharpe 1,07 | docs/EXECUTION_LEDGER.md#L9099-L9099 |
| TPS 812 unità +46,0 bp, Sharpe 1,12 (diff +0,04, IC90 -0,10 / +0,18), drawdown 729 contro 1.149 bp. | docs/EXECUTION_LEDGER.md#L9099-L9099 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "Riserva: il criterio di rischio 'per unità di esposizione massima' favorisce per costruzione l'ingresso a scaglioni... Il risultato solido è che la seconda unità comprata più in basso rende di più (+5,3 bp per unità); lo Sharpe non migliora in modo significativo."

## Prove

- runtime/proofs/tps1/tps1.json
