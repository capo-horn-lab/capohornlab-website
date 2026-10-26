---
id: "breadth-1"
titolo: "BREADTH-1 — ampiezza di mercato dalle aziende di Nasdaq-100 e S&P 500"
data: "2026-10-19"
strumenti: []
finestra: "518 titoli unici, prezzi Yahoo 2015-01..2026-10-16 (1.463.618 righe, 52 MB)"
verdetto: "misto"
pubblicabilita: "avvertenza"
avvertenza: "sopravvivenza; dati Yahoo/Wikipedia solo aggregati."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L7541-L7541"
prove:
  - "runtime/proofs/breadth1/breadth1.json"
---

## Domanda

indicatori di ampiezza (quota sopra le medie, avanzanti/declinanti, nuovi massimi-minimi, dispersione, divergenza) prevedono il rendimento di QQQ/SPY a 1 e 5 giorni?

## Metodo e rubrica

Spearman + Newey-West, 2015-2020 scoperta / 2021-2026 verifica, BH q≤0,10 su 24 test. Rubrica prima: sì (L7515).

## Esito

| Risultato | Fonte |
|---|---|
| "24 test; 1 AIUTA": S&P 500 nuovi massimi meno nuovi minimi a 52 settimane contro SPY a 5 giorni, verso CONTRARIO (rho -0,101 t -2,09 in scoperta, -0,129 t -3,18 in verifica, q 0,035). | docs/EXECUTION_LEDGER.md#L7541-L7541 |
| Controllo selettivo 10%: scoperta -23 bp di eccesso a 5 giorni, verifica +42: "la coda non è stabile". | docs/EXECUTION_LEDGER.md#L7541-L7541 |

## Cosa NON dice

- "solo informazione per il motore, non un setup"
- limite: costituenti di oggi (distorsione da sopravvivenza).

## Prove

- runtime/proofs/breadth1/breadth1.json
- runtime/research/constituents/
