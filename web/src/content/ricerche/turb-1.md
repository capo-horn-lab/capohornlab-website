---
id: "turb-1"
titolo: "TURB-1 — indice di turbolenza (FinRL) come protezione"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "MCL"
finestra: "221 strategie (MES, MNQ, MCL) + dati 2026"
verdetto: "senza verdetto nel registro"
pubblicabilita: "avvertenza"
avvertenza: "(sopravvivenza, campione 2026 minimo)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L7596-L7596"
prove:
  - "runtime/proofs/turb1/turb1.json"
  - "runtime/proofs/turb1/nt2026.json"
---

## Domanda

evitare i giorni dopo turbolenza (distanza di Mahalanobis dei rendimenti Nasdaq-100 sopra il 90° percentile) riduce le perdite?

## Metodo e rubrica

Come TAIL-1: differenza appaiata giornaliera in verifica, BH q≤0,10. Rubrica prima: sì (L7574).

## Esito

| Risultato | Fonte |
|---|---|
| "la protezione AIUTA (BH) in 32 casi, differenza positiva in 198 su 221 (90%)". | docs/EXECUTION_LEDGER.md#L7596-L7596 |
| Dati 2026: 1 solo giorno turbolento per MES e MNQ | docs/EXECUTION_LEDGER.md#L7596-L7596 |
| 79 casi cambiati, 47 positivi (59%), media +1,3 USD/sessione: "troppo pochi giorni per dire". | docs/EXECUTION_LEDGER.md#L7596-L7596 |

## Cosa NON dice

- "Candidata regola di rischio, più debole di P4/P5 sui dati nuovi."
- Limite: costituenti di oggi.

## Prove

- runtime/proofs/turb1/turb1.json
- runtime/proofs/turb1/nt2026.json
