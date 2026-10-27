---
id: "setup-2"
titolo: "SETUP-2 — catalogo setup futures e walk-forward adattivo con RizzoFlow"
data: "2026-10-16"
strumenti:
  - "MES"
  - "ES"
  - "NQ"
  - "RTY"
finestra: "MES (barre ES/NQ/RTY 1m, 55 sessioni dal 02/08 al 16/10/2026)"
verdetto: "senza verdetto nel registro"
pubblicabilita: "avvertenza"
avvertenza: "costi provvisori, campione di 55 sessioni, selezione a posteriori; dati NinjaTrader (licenza)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L6047-L6055"
prove:
  - "runtime/proofs/tools/walkforward-adattiva.json"
  - "runtime/proofs/tools/walkforward-compatto.json"
  - "runtime/proofs/tools/walkforward.json"
  - "docs/research/STRATEGIE_FUTURES_2026-10-16.md"
---

## Domanda

i 15 setup del catalogo e il motore adattivo (entrate strategiche + meta-selezione + filtro RizzoFlow) hanno un vantaggio fuori campione?

## Metodo e rubrica

Walk-forward su 7 finestre (`--fino 2026-10-16T17:00Z`), 1 USD/lato PROVVISORIO, slittamento stop 1 tick; confronto motore vs varianti; filtro RizzoFlow `take_setup` su 755 setup. Rubrica prima: parziale (piano e accettazione scritti prima, soglie t≥2 citate nel testo; nessun BH).

## Esito

| Risultato | Fonte |
|---|---|
| Nessun verdetto formale | docs/EXECUTION_LEDGER.md#L6047-L6055 |
| "Nessun vantaggio dimostrato: nessun totale con t >= 2". | docs/EXECUTION_LEDGER.md#L6047-L6055 |
| Motore 36 trade fuori campione, +25.22 USD/trade, netto +908, drawdown 376, t 1.27 | docs/EXECUTION_LEDGER.md#L6047-L6055 |
| entrate sul livello 26 trade +58.79 (t 2.46) | docs/EXECUTION_LEDGER.md#L6047-L6055 |
| ritracciamento 10 trade -62.05 | docs/EXECUTION_LEDGER.md#L6047-L6055 |
| a mercato piano fisso 153 trade -53.49 (t -2.58). | docs/EXECUTION_LEDGER.md#L6047-L6055 |
| RizzoFlow su 755 setup: TAKE -15.72/trade (598), SKIP -43.98 (157). | docs/EXECUTION_LEDGER.md#L6047-L6055 |
| Lordo senza costi: nessun setup robusto (t>2 solo PULLBACK 60m, ORB 15m, LATE_MOMENTUM 15m su 30 prove). | docs/EXECUTION_LEDGER.md#L6047-L6055 |

## Cosa NON dice

- "il confronto tra varianti è selezione a posteriori"
- commissione provvisoria.

## Prove

- runtime/proofs/tools/walkforward-adattiva.json
- runtime/proofs/tools/walkforward-compatto.json
- runtime/proofs/tools/walkforward.json
- docs/research/STRATEGIE_FUTURES_2026-10-16.md
