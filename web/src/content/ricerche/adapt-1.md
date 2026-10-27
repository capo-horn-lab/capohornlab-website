---
id: "adapt-1"
titolo: "ADAPT-1 — bot adattivo: regime -> strategia, oppure nessuna"
data: "2026-10-18"
strumenti:
  - "MES"
  - "MNQ"
  - "MCL"
finestra: "MES (70 strategie, 1.191 sessioni fuori campione), MNQ (118, 313), MCL (112)"
verdetto: "verdetto non estratto: vedi Esito"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L7187-L7200"
prove:
  - "runtime/proofs/adapt1/adapt1.json"
---

## Domanda

scegliere ogni giorno la strategia vincente nel regime di mercato dà vantaggio?

## Metodo e rubrica

Selettore walk-forward (macchina di COND-2) per cella di regime (tendenza, volatilità, giorno con evento), confronto con rotazione senza regime e con "sempre accese". Rubrica prima: sì.

## Esito

| Risultato | Fonte |
|---|---|
| "0 confermati su 3, q 0,93". | docs/EXECUTION_LEDGER.md#L7187-L7200 |
| MES: selettore 781 trade -2,64 USD t -0,67, fermo il 32,8% dei giorni | docs/EXECUTION_LEDGER.md#L7187-L7200 |
| MNQ: 719 trade -3,27 t -1,03, fermo 46,6% | docs/EXECUTION_LEDGER.md#L7187-L7200 |
| MCL: 119 trade -3,96, fermo 82,4%. | docs/EXECUTION_LEDGER.md#L7187-L7200 |

## Lettura e limiti (dal registro)

- "Il vantaggio non continua nel blocco successivo"
- restare fermi riduce le perdite (MCL) "ma non le trasforma in guadagni".

## Prove

- runtime/proofs/adapt1/adapt1.json
- runtime/research/adapt1/
