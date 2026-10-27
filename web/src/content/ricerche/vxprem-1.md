---
id: "vxprem-1"
titolo: "VXPREM-1 — premio dei future VIX (Cheng, RFS 2019) come predittore dei rendimenti di VX, MES e SPY"
data: "2026-10-20"
strumenti:
  - "VX"
  - "MES"
  - "SPY"
finestra: "174 CSV di scadenze mensili VX Cboe 2013-01-16..2027-06-16 (2 min 53 s di download), MES e SPY; la robustezza della regola confermata è in VXPREM-2 (scheda successiva)"
verdetto: "pass · confermata"
pubblicabilita: "avvertenza"
avvertenza: "Avvertenza forte: confermata \"con riserve forti\" (76% del risultato nel 2020, t<2 senza i 5 giorni migliori)"
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9919-L9927"
prove:
  - "runtime/proofs/vxprem1/vxprem1.json"
---

## Domanda

il premio dei future VIX prevede i rendimenti dei VX e di MES/SPY?

## Metodo e rubrica

IC di Spearman Newey-West, regole con t NW 5, placebo 200 rotazioni, q su 16 p; costi 100,70 USD a giro sul VX. Rubrica prima: sì.

## Esito

| Risultato | Fonte |
|---|---|
| VXPREM-1 "PASS, CONFERMATA secondo la rubrica per una sola regola (R-VX con P2), con riserve forti": verifica +109,1 USD/giorno (t 2,50, 709 giorni, totale 77.382 USD per contratto) contro sempre corto +48,3 (t 1,70); p95 +91,8; q 0,025 | docs/EXECUTION_LEDGER.md#L9919-L9927 |
| ma in scoperta +3,0 (t 0,09), "tre quarti del risultato vengono dal 2020 e senza i 5 giorni migliori t < 2" | docs/EXECUTION_LEDGER.md#L9919-L9927 |
| 108 entrate in verifica, costi 11.782 USD su 89.163 lordi | docs/EXECUTION_LEDGER.md#L9919-L9927 |
| peggior giorno -6.125 USD (26/1/2021). | docs/EXECUTION_LEDGER.md#L9919-L9927 |
| VXPREM-2: scheda dedicata. | docs/EXECUTION_LEDGER.md#L9919-L9927 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Lettura e limiti (dal registro)

- "una pista da ripetere, non una regola"
- salto del VX1 di febbraio 2018 fino a 17.600 USD in un giorno per 1 contratto corto
- il VX non è nel bot.

## Prove

- runtime/proofs/vxprem1/
- runtime/proofs/vxprem1/VX_<scadenza>.csv
- runtime/proofs/vxprem1/vxprem1.json
