---
id: "cond-1"
titolo: "COND-1 / COND-1-OOS / COND-2 / LEVELS-1 — dove vincono le strategie, esclusione dei momenti in perdita, livelli"
data: "2026-10-17"
strumenti:
  - "MES"
  - "MNQ"
  - "MCL"
  - "NQ"
  - "ES"
  - "CL"
finestra: "i 216 test di LAB-2 (MES, MNQ, MCL) e i livelli tondi/giornalieri di NQ, ES, CL"
verdetto: "verdetto non estratto: vedi Esito"
pubblicabilita: "avvertenza"
avvertenza: "`trades.json` e `cond1.json` contengono tracce di trade derivate da dati licenziati (solo aggregati); il book L2 è catturato da NinjaTrader (licenza)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L6527-L6527"
prove:
  - "runtime/proofs/cond1/cond1.json"
  - "runtime/proofs/cond1/oos.json"
  - "runtime/proofs/cond2/cond2.json"
  - "runtime/proofs/cond2/trades.json"
  - "runtime/proofs/levels1/levels1.json"
  - "docs/research/COND1_CONDIZIONI_LIVELLI_2026-10-18.md"
---

## Domanda

escludere ore/giorni/mesi/regimi in perdita rende profittevole una strategia? I livelli tondi tengono più del caso?

## Metodo e rubrica

Filtro per esclusione una dimensione alla volta, scelto in scoperta e misurato in verifica; placebo 200; BH; COND-2 ripete la scelta in walk-forward (ancorato e mobile 250 sessioni); LEVELS-1 con controlli a griglia spostata (metodo Osler). Rubrica prima: sì (L6469, L6533).

## Esito

| Risultato | Fonte |
|---|---|
| COND-1: "216 test, 1728 filtri, 0 confermati (BH q minimo 0,33)" | docs/EXECUTION_LEDGER.md#L6557-L6581 |
| "in 108 dei 188 test negativi la scelta a posteriori giorno x ora rende la media positiva" (illusione). | docs/EXECUTION_LEDGER.md#L6557-L6581 |
| COND-1-OOS: "0 filtri confermati su 14 prove (9 filtri x periodi disponibili; q minimo 0,61)". | docs/EXECUTION_LEDGER.md#L6527-L6527 · docs/EXECUTION_LEDGER.md#L6528-L6528 |
| COND-2: "216 test, 3456 filtri walk-forward, 0 confermati (q minimo 0,26)". | docs/EXECUTION_LEDGER.md#L6557-L6581 |
| LEVELS-1: "nessun livello tiene più del caso in entrambi i periodi" | docs/EXECUTION_LEDGER.md#L6527-L6527 · docs/EXECUTION_LEDGER.md#L6557-L6581 |
| NQ 29300 (descrittivo): 25 esiti, rimbalzo 36% contro 49,5% dei multipli di 100 e 50,2% dei controlli | docs/EXECUTION_LEDGER.md#L6557-L6581 |
| muri ES 12-26 (2 sessioni, descrittivo): 1514 muri, 76% ritirati prima del tocco, rimbalzo 57% (83/145) contro 47%. | docs/EXECUTION_LEDGER.md#L6557-L6581 |

## Lettura e limiti (dal registro)

- Muri e NQ 29300 sono "DESCRITTIVO (nessun verdetto)"
- 2 sessioni di book.

## Prove

- runtime/proofs/cond1/cond1.json
- runtime/proofs/cond1/oos.json
- runtime/proofs/cond2/cond2.json
- runtime/proofs/cond2/trades.json
- runtime/proofs/levels1/levels1.json
- docs/research/COND1_CONDIZIONI_LIVELLI_2026-10-18.md
