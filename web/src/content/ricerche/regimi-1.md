---
id: "regimi-1"
titolo: "REGIMI-1 — classificatore k-means (calma / trend / crisi) sull'indice azionario"
data: "2026-10-25"
strumenti:
  - "QQQ"
  - "MNQ"
finestra: "QQQ rettificato 03/01/2006..16/10/2026 prolungato con MNQ 12-26 fino al 23/10"
verdetto: "descrittivo"
pubblicabilita: "avvertenza"
avvertenza: "pubblicabile come classificazione descrittiva; i PNG di pagina mostrano l'interfaccia dell'app (valutare se esporla)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L10651-L10654"
prove:
  - "runtime/proofs/regimi1/regimi.json"
  - "runtime/proofs/regimi1/RISULTATI.md"
  - "runtime/proofs/regimi1/PIANO.md"
  - "runtime/proofs/regimi1/pannello_300x110.png"
  - "runtime/proofs/regimi1/pannello_520x160.png"
  - "runtime/proofs/regimi1/pannello_dettaglio.png"
  - "runtime/proofs/regimi1/pagina_con_volreg.png"
  - "runtime/proofs/regimi1/pagina_con_volreg_5120.png"
  - "docs/research/REGIMI_RICERCA_2026-10-25.md"
---

## Domanda

tre regimi di mercato (k=3) da rendimento medio annualizzato e volatilità a 20 giorni, riaddestrati ogni mese sul solo passato (rodaggio 756 giorni), sono stabili e informativi?

## Metodo e rubrica

k-means k=3, verifiche V1-V5 con soglie fissate nel PIANO PRIMA dei risultati; confronto con silhouette k=2/3 e mistura gaussiana. Rubrica prima: sì (L10644, PIANO).

## Esito

| Risultato | Fonte |
|---|---|
| Centroidi: calma +30,6% / 12,1% (53% dei giorni, durata media 21 g), trend +68,8% / 22,1% (30%, 9 g), crisi -72,8% / 26,6% (17%, 8 g). | docs/EXECUTION_LEDGER.md#L10651-L10654 |
| Silhouette k=2 0,44, k=3 0,38 | docs/EXECUTION_LEDGER.md#L10651-L10654 |
| ARI 0,73. | docs/EXECUTION_LEDGER.md#L10651-L10654 |
| V1 stabilità PASS (89,6%), V2 persistenza FAIL (P(resta) 0,953 / 0,887 / 0,875 contro 0,90), V3 VIX PASS (Spearman 0,57), V4 volatilità futura PASS (crisi +11,2 e +8,5 punti annui contro la base) "ma il regime spiega la volatilità futura meno della volatilità corrente da sola (R² 0,25 contro 0,32-0,33): nessuna informazione in più". | docs/EXECUTION_LEDGER.md#L10651-L10654 |
| Oggi (23/10): CRISI da 2 giorni, per il calo (-69,9% annuo). | docs/EXECUTION_LEDGER.md#L10651-L10654 · docs/EXECUTION_LEDGER.md#L10660-L10668 |

## Cosa NON dice

- "i dati preferiscono k=2; k=3 per richiesta del proprietario".

## Prove

- runtime/proofs/regimi1/regimi.json
- runtime/proofs/regimi1/RISULTATI.md
- runtime/proofs/regimi1/PIANO.md
- runtime/proofs/regimi1/pannello_300x110.png
- runtime/proofs/regimi1/pannello_520x160.png
- runtime/proofs/regimi1/pannello_dettaglio.png
- runtime/proofs/regimi1/pagina_con_volreg.png
- runtime/proofs/regimi1/pagina_con_volreg_5120.png
- docs/research/REGIMI_RICERCA_2026-10-25.md
