---
id: "sig-2"
titolo: "SIG-2 — setup rari da blog e forum (IBS, Gao-Han-Li-Zhou)"
data: "2026-10-18"
strumenti:
  - "MES"
  - "ES"
  - "MNQ"
  - "NQ"
finestra: "MES (ES 1m 2020-2024), MNQ (NQ 1s 2023-01..2024-08)"
verdetto: "non confermata"
pubblicabilita: "avvertenza"
avvertenza: "(regole pubbliche di terzi, citare fonti)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L7202-L7211"
prove:
  - "runtime/proofs/sig2/sig2.json"
---

## Domanda

le regole concrete di QuantifiedStrategies/QuantRocket (IBS<0,20, ultima mezz'ora che segue la prima) superano la rubrica di LAB-2?

## Metodo e rubrica

8 test, scoperta 60/verifica 40, placebo, BH q≤0,10, +1 tick, tenuta max 5 sessioni. Rubrica prima: sì (L7119).

## Esito

| Risultato | Fonte |
|---|---|
| "0 ADOTTATE su 8". | docs/EXECUTION_LEDGER.md#L7202-L7211 |
| MES IBS<0,20 -> lungo fino a IBS>0,90: scoperta 104 trade +113,5 USD, verifica 65 trade +96,2 USD t 2,28, sopra il p95 dei placebo (91,6), "bloccata solo da BH q 0,105" | docs/EXECUTION_LEDGER.md#L7202-L7211 |
| Gao: MES -5,37 e MNQ -18,17 in verifica. | docs/EXECUTION_LEDGER.md#L7202-L7211 |

## Cosa NON dice

- Ipotesi H-NEXT-4 dichiarata per sessioni future MES dopo il 18/10/2026.

## Prove

- runtime/proofs/sig2/sig2.json
