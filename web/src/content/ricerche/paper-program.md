---
id: "paper-program"
titolo: "PAPER-PROGRAM (20/10/2026) — 13 studi dai paper e dalla domanda del proprietario: bilancio"
data: "2026-10-20"
strumenti: []
finestra: "programma indirizzato dal proprietario (indici, tassi, valute, energia, metalli, volatilità, crypto): rubriche per gruppo (INDICI-1, TASSI-FX-1, COMM-1) e prove VPIN-1, KRT-1, FOMCDRIFT-1, TUGWAR-1, GHLZ-1, CRYPTOMOM-1, MACROWIN-1, FXFOMC-1, VIXTS-2, SAFEHAVEN-1, CP-1, VXPREM-1, GAPFILL-1."
verdetto: "confermata · parziale · non confermata"
audit: {"stato": "corretto", "id": ["PAPER-PROGRAM"]}
pubblicabilita: "avvertenza"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9931-L9932"
prove: []
---

## Ritiri e correzioni

- PAPER-PROGRAM bilancio rettificato: 13 studi (non 14), 3 PARZIALI (L9932).

## Domanda

programma indirizzato dal proprietario (indici, tassi, valute, energia, metalli, volatilità, crypto): rubriche per gruppo (INDICI-1, TASSI-FX-1, COMM-1) e prove VPIN-1, KRT-1, FOMCDRIFT-1, TUGWAR-1, GHLZ-1, CRYPTOMOM-1, MACROWIN-1, FXFOMC-1, VIXTS-2, SAFEHAVEN-1, CP-1, VXPREM-1, GAPFILL-1.

## Metodo e rubrica

Per ogni studio una rubrica con verdetti CONFERMATA/PARZIALE/NON CONFERMATA fissati prima, scoperta 60% / verifica 40%, BH q≤0,10, placebo 200. Rubrica prima: sì, ciascuna scritta prima dello script (L9669).

## Esito

| Risultato | Fonte |
|---|---|
| Bilancio (con rettifica): "gli studi sono 13, non 14; PARZIALE sono 3 (MACROWIN-1, VIXTS-2, CRYPTOMOM-1)... FXFOMC-1 è tra le 9 NON CONFERMATE. Totale 1 + 3 + 9 = 13." | docs/EXECUTION_LEDGER.md#L9931-L9932 |
| CONFERMATA alla lettera 1 (VXPREM-1, "con riserve forti") | docs/EXECUTION_LEDGER.md#L9931-L9932 |
| NON CONFERMATA 9 (VPIN-1, TUGWAR-1, GHLZ-1, FOMCDRIFT-1, FXFOMC-1, CP-1, KRT-1, SAFEHAVEN-1, GAPFILL-1). | docs/EXECUTION_LEDGER.md#L9931-L9932 |

## Cosa NON dice

- "Nessun cambiamento in carta o nel bot"
- restano non misurabili con i dati in casa: Hasbrouck, carry FX multi-valuta, Ranaldo-Somogyi, curve dei future, Makarov-Schoar.

## Prove

- runtime/proofs/vpin1/
- runtime/proofs/krt1/
- runtime/proofs/fomcdrift1/
- runtime/proofs/tugwar1/
- runtime/proofs/ghlz1/
- runtime/proofs/cryptomom1/
- runtime/proofs/macrowin1/
- runtime/proofs/fxfomc1/
- runtime/proofs/vixts2/
- runtime/proofs/safehaven1/
- runtime/proofs/cp1/
- runtime/proofs/vxprem1/
- runtime/proofs/gapfill1/
- runtime/proofs/cp1
- runtime/proofs/krt1
