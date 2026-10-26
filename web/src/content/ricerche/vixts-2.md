---
id: "vixts-2"
titolo: "VIXTS-2 — pendenza della struttura a termine del VIX come predittore del rendimento di MES a 1, 5, 22 sessioni"
data: "2026-10-20"
strumenti:
  - "MES"
  - "SPY"
finestra: "MES 1.831 sessioni valide 2019-05-06..2026-10-19 e SPY 5.232 sedute 2006-2026"
verdetto: "parziale"
pubblicabilita: "avvertenza"
avvertenza: "(IC correlati, 2 prove indipendenti)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9845-L9861"
prove:
  - "runtime/proofs/vixts2/vixts2.json"
  - "runtime/proofs/vixts2/spy_daily.csv"
  - "runtime/proofs/vixts2/run.log"
---

## Domanda

VIX9D/VIX, VIX/VIX3M e variazione del VIX prevedono i rendimenti a 1, 5, 22 sessioni (Johnson; Whaley)?

## Metodo e rubrica

IC di Spearman Newey-West, BH sulle 20 p di verifica, regola lungo MES con VIX/VIX3M>1 per 5 sessioni, placebo 200. Rubrica prima: sì.

## Esito

| Risultato | Fonte |
|---|---|
| "Esecuzione PASS, verdetto PARZIALE": "8 IC su 18 hanno stesso segno in scoperta e verifica, \\|t\\| >= 2 e q <= 0,10 in verifica" (es. MES VIX/VIX3M 5 sessioni scoperta 0,108 (t 2,17) / verifica 0,203 (t 3,06), q 0,016; SPY VIX/VIX3M 22 sessioni 0,175 (t 3,15) / 0,228 (t 3,01)) | docs/EXECUTION_LEDGER.md#L9845-L9861 |
| regola MES: verifica +104,30 USD (t 0,40, n 16, placebo p95 294,87): non passa. | docs/EXECUTION_LEDGER.md#L9845-L9861 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "gli 8 IC non sono 8 prove indipendenti ma circa 2"
- "la regola binaria con tenuta 5 sessioni non batte ingressi casuali".
- Nulla cambia in carta.

## Prove

- runtime/proofs/vixts2/vixts2.json
- runtime/proofs/vixts2/spy_daily.csv
- runtime/proofs/vixts2/run.log
