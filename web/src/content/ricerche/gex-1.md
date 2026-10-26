---
id: "gex-1"
titolo: "GEX-1, GEXOC-1, H-NEXT-9 — gamma dei market maker (GEX/DIX SqueezeMetrics) e IBS"
data: "2026-10-19"
strumenti:
  - "SPY"
  - "QQQ"
finestra: "CSV SqueezeMetrics 02/05/2011-16/10/2026 (download autorizzato dal proprietario), IBS-NT sui 4 micro 2019-2026 (942 trade) e SPY/QQQ 2011-2018 (450 trade); GEXOC-1: SPY 2011-05-03..2018-12-31 (1.929 sessioni)."
verdetto: "ritirato"
pubblicabilita: "avvertenza"
avvertenza: "pubblicare solo il verdetto finale (NON CONFERMATO); il CSV SqueezeMetrics non va ridistribuito."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8969-L8969"
prove:
  - "runtime/proofs/gex1/gex1.json"
  - "runtime/proofs/gexoc1/gexoc1.json"
---

## Ritiri e correzioni

- VOLREV-1 e GEX-1 (L8968-L8970): due conferme registrate come CONFERMATO sono state RITIRATE dall'audit (artefatto di cambio contratto; terzili in dollari = epoche): ora "NON CONFERMATO". H-NEXT-8/9 solo descrittivi.

## Domanda

l'IBS rende di più con gamma basso? Il GEX del giorno prima prevede apertura->chiusura?

## Metodo e rubrica

Terzili del GEX del giorno prima, bootstrap, BH; GEXOC-1: Spearman Newey-West lag 5 + z-score a 250 giorni. Rubrica prima: sì (L8860, L9084).

## Esito

| Risultato | Fonte |
|---|---|
| GEX-1 registrato "CONFERMATO sui future": GEX alto +13,6 bp, medio +35,2, basso +70,0 | docs/EXECUTION_LEDGER.md#L8868-L8873 |
| basso-alto +56,4, p 0,019, q 0,039 | docs/EXECUTION_LEDGER.md#L8868-L8873 |
| ETF diff +37,1, p 0,100. | docs/EXECUTION_LEDGER.md#L8868-L8873 |
| RITIRATO dall'audit: con misura relativa +18,8 / +43,0 / +56,9, diff +38,1, p 0,068: "CONFERMA RITIRATA, GEX-1 = NON CONFERMATO". | docs/EXECUTION_LEDGER.md#L8969-L8969 |
| GEXOC-1: "NON CONFERMATA": Spearman -0,054, t NW -2,23 sul GEX grezzo ma z-score a 250 giorni t -1,41, spread +1,3 bp (segno opposto): "la stessa trappola di GEX-1 (terciles = epoche); tolta la tendenza non resta nulla". | docs/EXECUTION_LEDGER.md#L8868-L8873 · docs/EXECUTION_LEDGER.md#L8969-L8969 · docs/EXECUTION_LEDGER.md#L9090-L9090 |

## Cosa NON dice

- H-NEXT-8 e H-NEXT-9 "restano solo come osservazione descrittiva".

## Prove

- runtime/proofs/gex1/gex1.json
- runtime/proofs/gexoc1/gexoc1.json
- runtime/research/squeezemetrics/
