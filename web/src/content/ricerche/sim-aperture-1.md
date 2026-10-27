---
id: "sim-aperture-1"
titolo: "SIM-APERTURE-1 e SIM-APERTURE-2 — simulazione delle aperture di MNQ con modelli locali (poi due agenti Claude Opus) in dibattito, RizzoFlow arbitro e cancello"
data: "2026-10-20"
strumenti:
  - "MNQ"
finestra: "MNQ 1 minuto NinjaTrader 2019-05..2026-10 (1.919 sessioni con barra delle 8:30 CT); eseguite 190 sessioni (13/5/2019-4/2/2020) per SIM-APERTURE-2; SIM-APERTURE-1 (modelli locali) fermata dopo 11 sessioni."
verdetto: "non confermata"
pubblicabilita: "avvertenza"
avvertenza: "il risultato è su 190 sessioni 2019-2020 (non su tutto il periodo)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L10116-L10123"
prove:
  - "runtime/sim-aperture/sessioni.jsonl"
  - "runtime/sim-aperture/bilancio-190.json"
  - "runtime/sim-aperture/riepilogo-unito.json"
---

## Domanda

l'app (modelli in dibattito TORO/ORSO + RizzoFlow come arbitro + cancello) ottiene un netto positivo sull'apertura di MNQ?

## Metodo e rubrica

Per sessione: previsioni 7:30-8:15 CT, parere RizzoAdvisor, piani TORO/ORSO, repliche, arbitro, cancello, ordine simulato con slittamento IMPACT-1, analisi; rubrica con 4 criteri fissati prima, applicata a 200 sessioni (riusciti 190); costo stimato 150,75 USD per 190 sessioni (0,79 a sessione). Rubrica prima: sì (L9936, L10029).

## Esito

| Risultato | Fonte |
|---|---|
| "Verdetto: NON CONFERMATA (vale solo il criterio 1)": criterio 1 PASSATO (0 entrate mancate; 0 risposte finali con numeri inventati su 2.090 domande) | docs/EXECUTION_LEDGER.md#L10116-L10123 |
| criterio 2 FALLITO: media -6,05 USD a sessione (t -1,42; vincenti 39,5%; totale -1.149,50) contro il lato a caso -4,85 (p95 +2,72) e l'acquisto a mercato -5,04 | docs/EXECUTION_LEDGER.md#L10116-L10123 |
| criterio 3 FALLITO: 760 previsioni giuste 52,2% (p 0,12), solo SU e GIU 45,0%, errore medio 8,5 punti contro 7,0 della previsione "nessun cambiamento". | docs/EXECUTION_LEDGER.md#L10116-L10123 |
| RizzoFlow arbitro: vendita 138 volte su 190 (72,6%) con 90 sessioni su 190 favorevoli all'acquisto. | docs/EXECUTION_LEDGER.md#L10116-L10123 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Lettura e limiti (dal registro)

- "il dibattito con RizzoFlow come arbitro non ha un vantaggio sull'apertura di MNQ: sceglie il piano migliore come una moneta e pende verso la vendita in un mercato in salita"
- periodo coperto 2019-2020 soltanto
- simulazione fermata dal proprietario il 20/10 alle 22:21 per costo.

## Prove

- runtime/sim-aperture/sessioni.jsonl
- runtime/sim-aperture/bilancio-190.json
- runtime/sim-aperture/riepilogo-unito.json
