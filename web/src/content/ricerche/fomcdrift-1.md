---
id: "fomcdrift-1"
titolo: "FOMCDRIFT-1 — deriva post-FOMC su ZN (Brooks-Katz-Lustig)"
data: "2026-10-20"
strumenti:
  - "ZN"
  - "MES"
finestra: "ZN 1 minuto 2019-02-25..2026-10-16 (1.969 sessioni), 60 riunioni (36 scoperta, 24 verifica), controllo MES"
verdetto: "pass · non confermata"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9729-L9734"
prove:
  - "runtime/proofs/fomcdrift1/fomcdrift1.json"
---

## Domanda

dopo il FOMC il prezzo dei Treasury continua nel verso del movimento del giorno?

## Metodo e rubrica

20 varianti (movimento A/B x h 1,2,5,10,15), BH q 0,10 dentro lo strumento, placebo. Rubrica prima: sì (L9695).

## Esito

| Risultato | Fonte |
|---|---|
| "Esito PASS (script eseguito), verdetto NON CONFERMATA su 20 varianti (0 scelte, 0 confermate, 0 parziali)". | docs/EXECUTION_LEDGER.md#L9729-L9734 |
| ZN scoperta tutta negativa (inversione): h=1 -127,5 USD/contratto (t -1,20), q 0,88 | docs/EXECUTION_LEDGER.md#L9729-L9734 |
| verifica h=1 +61,8 USD (t 0,72, placebo p95 99,4) | docs/EXECUTION_LEDGER.md#L9729-L9734 |
| MES verifica negativa su tutte le varianti (h=1 -52,9 USD). | docs/EXECUTION_LEDGER.md#L9729-L9734 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "Il segno della deriva cambia tra le fasi... con 24 eventi di verifica l'errore standard è 90-300 USD per contratto, la deriva del paper... non si distingue dal rumore"
- costo andata/ritorno 31,95 USD (≈2,9 bp).

## Prove

- runtime/proofs/fomcdrift1/fomcdrift1.json
