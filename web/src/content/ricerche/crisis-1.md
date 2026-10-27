---
id: "crisis-1"
titolo: "CRISIS-1, EIA-1, CARRY-1, OPT-ALL-ZN — altri mercati: trend nello stress, petrolio EIA, carry, ottimizzazione su ZN"
data: "2026-10-19"
strumenti:
  - "TLT"
  - "IEF"
  - "GLD"
  - "SLV"
  - "USO"
  - "UNG"
  - "UUP"
  - "FXE"
  - "FXY"
  - "ZN"
  - "MGC"
  - "M6E"
  - "MCL"
  - "MBT"
finestra: "ETF 2009-09..2018-12 (TLT, IEF, GLD, SLV, USO, UNG, UUP, FXE, FXY) e future ZN, MGC, M6E, MCL 2019-2026; MCL 1 minuto giugno 2021..ottobre 2026 (205 rilasci EIA); MCL, MGC, ZN, M6E, MBT (222 periodi tra cambi di contratto); ZN per OPT-ALL."
verdetto: "non confermato"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8797-L8800"
prove:
  - "runtime/proofs/optall/optall.json"
---

## Domanda

il trend nei mercati non azionari rende nei giorni di stress azionario? La prima mezz'ora dopo il rapporto EIA prevede l'ultima mezz'ora? Il carry in serie storica funziona?

## Metodo e rubrica

Nullo con 1.000 spostamenti circolari (CRISIS-1); R² fuori campione + Clark-West (EIA-1); t sui periodi e placebo 1.000 (CARRY-1). Rubrica prima: sì (L8787, L8802, L8817).

## Esito

| Risultato | Fonte |
|---|---|
| CRISIS-1: "NON CONFERMATO in entrambi gli insiemi": ETF d +0,80 bp/giorno, p 0,40 | docs/EXECUTION_LEDGER.md#L8797-L8800 |
| future d -6,98, p 0,83. | docs/EXECUTION_LEDGER.md#L8797-L8800 |
| EIA-1: "NON CONFERMATO": 203 eventi, correlazione -0,001, R² fuori campione -1,2%, Clark-West p 0,91 | docs/EXECUTION_LEDGER.md#L8811-L8811 |
| regola 195 trade -8,36 bp (t -2,93). | docs/EXECUTION_LEDGER.md#L8811-L8811 |
| CARRY-1: "NON CONFERMATO": 222 periodi, -25,4 bp per periodo netti, t -0,37 (placebo p95 +109). | docs/EXECUTION_LEDGER.md#L8825-L8825 · docs/EXECUTION_LEDGER.md#L8797-L8800 |
| OPT-ALL-ZN: "0 confermati su 66" (ZN: IBS -1,33 bp/sessione, t -2,08). | docs/EXECUTION_LEDGER.md#L8797-L8800 · docs/EXECUTION_LEDGER.md#L8827-L8827 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- CRISIS-1: "il 'crisis alpha'... non si vede a livello giornaliero"
- "Per i mercati dove la mean reversion non vale non abbiamo ancora una strategia con edge"
- EIA-1: "Nessun momentum intraday sul petrolio"
- CARRY-1: con un solo strumento per mercato il carry è solo un'esposizione al prezzo.

## Prove

- runtime/proofs/crisis1/*.json
- runtime/proofs/eia1/*.json
- runtime/proofs/carry1/*.json
- runtime/proofs/optall/optall.json
