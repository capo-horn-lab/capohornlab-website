---
id: "leak-1"
titolo: "LEAK-1 — controllo di anticipazione (look-ahead) sui dati Cboe"
data: "2026-10-19"
strumenti: []
finestra: "ripetizione di OPT-1 e del gruppo backwardation di L38 con il valore del giorno prima"
verdetto: "senza verdetto nel registro"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8377-L8381"
prove: []
---

## Domanda

le conclusioni dipendono da un look-ahead (chiusura Cboe 16:15 ET contro decisioni 15:59)?

## Metodo e rubrica

Ritardo di una sessione degli indicatori; segnalato dalla revisione di un agente. Rubrica prima: sì (L8372).

## Esito

| Risultato | Fonte |
|---|---|
| "nessuna conclusione cambia": OPT-1 confermati gli stessi 6 su 10 (PC_EQ SPY IC 0,125 t 2,37; TS9 SPY 0,108 t 2,56) | docs/EXECUTION_LEDGER.md#L8377-L8381 |
| IBS in backwardation con valore precedente: 61 trade, +179,3 bp (t 5,04), contro 881 trade +29,8 (stesso giorno: 77 trade, +147,4). | docs/EXECUTION_LEDGER.md#L8377-L8381 |

## Cosa NON dice

- "Da ora le variabili Cboe si usano sempre con il valore della chiusura precedente".
- Revisione di `robust.py`/`meta_label.py`: nessun errore.

## Prove

- Nessun file di prova indicato dall'inventario: Nessun file proprio indicato (ripetizioni nel ledger).
