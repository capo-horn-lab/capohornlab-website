---
id: "meta-1"
titolo: "META-1 — meta-labeling dei segnali IBS"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "M2K"
  - "MYM"
finestra: "942 trade IBS su MES, MNQ, M2K, MYM 2019-2026 (757 con previsione dal 2020-10-06)"
verdetto: "non confermato"
audit: {"stato": "corretto", "id": ["META-1"]}
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8300-L8305"
prove:
  - "runtime/proofs/meta1/meta1.json"
---

## Ritiri e correzioni

- META-1 (L8954): feature calcolate un minuto dopo la decisione e VIX dello stesso giorno (look-ahead); verdetto negativo invariato.

## Domanda

un modello logistico sulle variabili d'ingresso separa i trade IBS buoni dai cattivi (SALTA o DIMENSIONE)?

## Metodo e rubrica

Regressione logistica L2 in walk-forward espanso; due usi (salta se p<0,5; dimensione 0/1/2 micro). Rubrica prima: sì (L8287).

## Esito

| Risultato | Fonte |
|---|---|
| "NON confermato in nessuno dei due usi." | docs/EXECUTION_LEDGER.md#L8300-L8305 |
| Regola sola sui 757: +35,03 bp/trade, t 5,10, 63,7% vincenti. | docs/EXECUTION_LEDGER.md#L8300-L8305 |
| SALTA: salta 36 trade che rendono +54,97 bp contro +34,03 dei 721 tenuti (t di Welch -0,85, verso sbagliato). | docs/EXECUTION_LEDGER.md#L8300-L8305 |
| DIMENSIONE: +31,99 bp per micro esposto contro +35,03 | docs/EXECUTION_LEDGER.md#L8300-L8305 |
| differenza giornaliera +40,4 bp (t 2,37) "solo perché si espone di più". | docs/EXECUTION_LEDGER.md#L8300-L8305 |

## Cosa NON dice

- "il modello non separa i trade buoni dai cattivi;... La regola IBS resta com'è."

## Prove

- runtime/proofs/meta1/meta1.json
