---
id: "scenari-1"
titolo: "SCENARI-1 — albero degli scenari con percentuali sul grafico live (motore Python + indicatore NinjaScript)"
data: "2026-10-21"
strumenti:
  - "MNQ"
  - "MES"
  - "M2K"
  - "MYM"
finestra: "MNQ (e MES, M2K, MYM), ultime 250 sessioni; richiesta del proprietario: vedere sul grafico live i rami (primo movimento di 50 punti, ritorno, 50 opposto, estensione) con le probabilità statistiche."
verdetto: "pass · not_run"
pubblicabilita: "avvertenza"
avvertenza: "il codice dell'indicatore è prodotto proprio (nessun dato di terzi)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L10320-L10320"
prove:
  - "runtime/proofs/scenari1/PIANO.md"
  - "runtime/proofs/scenari1/PIANO_indicatore.md"
  - "runtime/proofs/scenari1/truth.json"
  - "runtime/proofs/scenari1/run.log"
  - "runtime/proofs/scenari1/esempio-MNQ-prossima-apertura.json"
  - "runtime/proofs/scenari1/esempio-4-strumenti.json"
  - "ninjatrader/TradingAgentScenari.cs"
  - "docs/research/SCENARI_GRAFICO_RICERCA_2026-10-21.md"
---

## Domanda

MNQ (e MES, M2K, MYM), ultime 250 sessioni; richiesta del proprietario: vedere sul grafico live i rami (primo movimento di 50 punti, ritorno, 50 opposto, estensione) con le probabilità statistiche.

## Metodo e rubrica

Visualizzazione delle frequenze di FREQ-LIVE-1; ogni ramo con p, k, n, margine max(1,96·√(p(1-p)/n), 3/n); rami con n<20 omessi, 20≤n<40 "pochi casi"; verità: casi costruiti a mano uguali al conteggio diretto; passeggiata casuale entro il margine del 50%. Rubrica prima: sì (L10306).

## Esito

| Risultato | Fonte |
|---|---|
| Motore PASS (11-15 test PASS; 0,97 s di ciclo, 2,8 s a regime per 4 strumenti). | docs/EXECUTION_LEDGER.md#L10328-L10350 |
| Albero MNQ "prossima apertura" (prezzo di riferimento 29.791): primo movimento di 50 giù p 0,536 (134/250, ±0,062) con ritorno entro 30 min 0,709 (95/134), 50 opposto 0,642 (86/134), mai 0,172 (23/134) | docs/EXECUTION_LEDGER.md#L10328-L10350 |
| primo movimento su 0,464 (116/250). | docs/EXECUTION_LEDGER.md#L10328-L10350 |
| Indicatore: compilazione in NinjaTrader PASS (602 righe con codice generato) | docs/EXECUTION_LEDGER.md#L10320-L10320 |
| resa a video "NOT_RUN" nel ledger. | docs/EXECUTION_LEDGER.md#L10320-L10320 · docs/EXECUTION_LEDGER.md#L10328-L10350 |

## Cosa NON dice

- "frequenze descrittive su 76-250 casi (margini 6-12 punti); nessuna prova di vantaggio economico"
- il verso del primo movimento "è moneta (46/54 ±6)" (brainstorming)
- informano solo i figli con n>100.
- Proposta CAL-SCENARI-1 (calibrazione in avanti) in passo a parte.

## Prove

- runtime/proofs/scenari1/PIANO.md
- runtime/proofs/scenari1/PIANO_indicatore.md
- runtime/proofs/scenari1/truth.json
- runtime/proofs/scenari1/run.log
- runtime/proofs/scenari1/esempio-MNQ-prossima-apertura.json
- runtime/proofs/scenari1/esempio-4-strumenti.json
- ninjatrader/TradingAgentScenari.cs
- docs/research/SCENARI_GRAFICO_RICERCA_2026-10-21.md
