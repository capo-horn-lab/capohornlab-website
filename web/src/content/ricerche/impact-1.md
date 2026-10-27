---
id: "impact-1"
titolo: "IMPACT-1 — spread effettivo e impatto dai tick; prudenza dello slittamento di SIM-APERTURE"
data: "2026-10-20"
strumenti:
  - "MNQ"
  - "MES"
  - "M2K"
  - "MYM"
finestra: "tick NinjaTrader 20/9-16/10/2026 di MNQ, MES, M2K, MYM (20 giorni di sessione)"
verdetto: "verdetto non estratto: vedi Esito"
pubblicabilita: "avvertenza"
avvertenza: "i tick sono dati NinjaTrader/CME"
fonte_ledger: "docs/EXECUTION_LEDGER.md#L10004-L10018"
prove:
  - "runtime/proofs/impact1/impact1.json"
---

## Domanda

lo slittamento della simulazione delle aperture (1 tick + 2% dell'escursione, tetto 10) è prudente rispetto al costo empirico dell'ordine a mercato all'apertura?

## Metodo e rubrica

Spread di Roll, lambda di Kyle (tick per 100 contratti), movimento nel primo secondo; PRUDENTE se ≥3 dei 4 strumenti e MNQ hanno costo del modello ≥ costo empirico. Rubrica prima: sì (L9994).

## Esito

| Risultato | Fonte |
|---|---|
| "Verdetto: OTTIMISTA (0 strumenti prudenti su 4 all'apertura)": MNQ empirico 30,0 / 23,8 / 55,1 tick (media/mediana/p90) contro modello 4,9 / 5 / 6 | docs/EXECUTION_LEDGER.md#L10004-L10018 |
| MES 5,8 / 4,7 / 12,4 contro 1,6 / 2 / 2. | docs/EXECUTION_LEDGER.md#L10004-L10018 |
| Lambda di Kyle 8:30 / 10:00 / 12:00: MNQ 8,2 / 5,4 / 6,5. | docs/EXECUTION_LEDGER.md#L10004-L10018 |
| Lo slittamento è stato portato a 1 tick + 15% dell'escursione senza tetto (MNQ 0,15, MES 0,20, M2K 0,20, MYM 0,30) e la simulazione è ripartita da zero. | docs/EXECUTION_LEDGER.md#L10004-L10018 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Lettura e limiti (dal registro)

- "all'apertura il costo è il movimento del primo secondo, non lo spread"
- la calibrazione è "una taratura, non una verifica" sugli stessi 20 giorni
- il confronto è prudente per costruzione.

## Prove

- runtime/proofs/impact1/impact1.json
- runtime/research/ticks/*.parquet
