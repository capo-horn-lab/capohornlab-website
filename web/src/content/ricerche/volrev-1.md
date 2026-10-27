---
id: "volrev-1"
titolo: "VOLREV-1, H-NEXT-8, STBOND-1, FXHEDGE-1 — volume/VIX/Treasury/euro come condizioni dell'IBS"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "M2K"
  - "MYM"
  - "SPY"
  - "QQQ"
  - "ZN"
  - "M6E"
finestra: "IBS-NT su MES, MNQ, M2K, MYM 2019-2026 (918-941 trade) e SPY/QQQ 2006-2018 (volume Yahoo); ZN 1 minuto NinjaTrader; M6E, 90 fine mese 2019-2026."
verdetto: "non confermato"
audit: {"stato": "ritirato", "id": ["VOLREV-1"]}
pubblicabilita: "avvertenza"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8780-L8785"
prove: []
---

## Ritiri e correzioni

- VOLREV-1 e GEX-1 (L8968-L8970): due conferme registrate come CONFERMATO sono state RITIRATE dall'audit (artefatto di cambio contratto; terzili in dollari = epoche): ora "NON CONFERMATO". H-NEXT-8/9 solo descrittivi.

## Domanda

l'IBS rende di più con volume atteso alto (VOLX) o VIX alto? Nei giorni "rifugio" (azioni giù, Treasury su)? L'euro a fine mese segue la copertura dei gestori?

## Metodo e rubrica

Terzili fissi, bootstrap a blocchi di 20 giorni (2.000), BH q≤0,10 su 4 (VOLREV-1); Holm su 3 (STBOND-1); placebo 200 (FXHEDGE-1). Rubrica prima: sì (L8733, L8742, L8771).

## Esito

| Risultato | Fonte |
|---|---|
| STBOND-1: "NON CONFERMATO, direzione coerente per l'IBS": 941 trade, +54,8 bp rifugio contro +19,1 rischio, diff +35,7, t 1,77 (p 0,077, Holm 0,23). | docs/EXECUTION_LEDGER.md#L8780-L8785 |
| FXHEDGE-1: "NON CONFERMATO": 89 trade, -5,43 bp netti, t -1,76, placebo p95 +1,5. | docs/EXECUTION_LEDGER.md#L8780-L8785 |

## Cosa NON dice

- ATTENZIONE, RITIRO REGISTRATO (AUDIT-FABLE): "VOLREV-1 (future VOLX, registrato CONFERMATO): il VOLX della serie continua cala meccanicamente nelle sessioni intorno al cambio di contratto... Senza i trade adiacenti ai cambi (762): terzili +32,6 / +62,2 / +57,4, alto - basso +24,8, p 0,131.... CONFERMA RITIRATA, VOLREV-1 = NON CONFERMATO."
- H-NEXT-8/9 "restano solo come osservazione descrittiva".
- STBOND-1 "da tenere come descrittivo".

## Prove

- runtime/proofs/volrev1/*.json
- runtime/proofs/stbond1/*.json
- runtime/proofs/fxhedge1/*.json
