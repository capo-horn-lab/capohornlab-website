---
id: "dir-1"
titolo: "DIR-1 — long contro short: perché gli short perdono e quando spegnerli"
data: "2026-10-18"
strumenti:
  - "MNQ"
finestra: "216 test di COND-1 (MNQ ORB 60m come caso guida)"
verdetto: "non confermata"
pubblicabilita: "avvertenza"
avvertenza: "dati licenziati solo aggregati."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L6604-L6620"
prove:
  - "runtime/proofs/dir1/dir1.json"
  - "runtime/proofs/dir1/regime.json"
---

## Domanda

gli short perdono sistematicamente e possono essere spenti con una regola causale?

## Metodo e rubrica

5 regole (R0 long+short, R1 solo long, R2-R4 per trend 4h/regime giornaliero), verifica con BH su 864 e periodi mai usati. Rubrica prima: sì (L6583+).

## Esito

| Risultato | Fonte |
|---|---|
| "0 regole adottate su 864, nessuna condizione in cui gli short siano positivi secondo la rubrica." MNQ ORB 60m: short scoperta 106 trade -4,32 USD, verifica 81 trade +36,73 | docs/EXECUTION_LEDGER.md#L6604-L6620 |
| R3: verifica +60,96 (99 trade, t 2,44) ma NQ 16/08-31/12/2024 -9,63 contro -3,29, q 1,0. 24 test long in utile e short in perdita, 11 il contrario | docs/EXECUTION_LEDGER.md#L6604-L6620 |
| short con regime su: media delle medie -5,75 USD, positivi in 13 test su 150. | docs/EXECUTION_LEDGER.md#L6604-L6620 |

## Cosa NON dice

- R3 su MNQ ORB 60m dichiarata H-NEXT-2: da provare solo su sessioni future (nessun nuovo parametro).

## Prove

- runtime/proofs/dir1/dir1.json
- runtime/proofs/dir1/regime.json
