---
id: "ins-1"
titolo: "INS-1 — compravendite degli insider (Form 4 SEC) come sentiment per ES e NQ"
data: "2026-10-18"
strumenti:
  - "SPY"
  - "QQQ"
  - "ES"
finestra: "SPY/QQQ giornalieri 2006-2026 (5230 giorni, Yahoo), ES 2020-2024, dati SEC DERA 2016q1-2026q2"
verdetto: "senza verdetto nel registro"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L6939-L6948"
prove:
  - "runtime/proofs/ins1/ins1.json"
  - "docs/research/INS1_INSIDER_2026-10-18.md"
---

## Domanda

il rapporto netto di acquisto degli insider prevede il rendimento a 21 e 63 giorni?

## Metodo e rubrica

NPR a 30/90 giorni (acquirenti-venditori), classificazione routine/opportunistico (Cohen-Malloy-Pomorski), Newey-West; Prova B nello studio SENT-3 a 4 h e giornaliero. Rubrica prima: sì (L6902+).

## Esito

| Risultato | Fonte |
|---|---|
| "Non vale." | docs/EXECUTION_LEDGER.md#L6939-L6948 |
| NPR 90 giorni contro SPY a 21 giorni rho +0,113 (t 1,31), QQQ +0,071 (t 0,85) | docs/EXECUTION_LEDGER.md#L6939-L6948 |
| a 63 giorni circa zero | docs/EXECUTION_LEDGER.md#L6939-L6948 |

1 righe della scheda non riportate: la prova citata non le contiene.

## Cosa NON dice

- L'insider entra nell'app "solo come informazione descrittiva, non come sentiment"
- dati SEC trimestrali (ultimo 30/06/2026).

## Prove

- runtime/proofs/ins1/ins1.json
- docs/research/INS1_INSIDER_2026-10-18.md
- runtime/history/insider/
