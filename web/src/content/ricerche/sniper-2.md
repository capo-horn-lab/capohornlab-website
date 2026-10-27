---
id: "sniper-2"
titolo: "SNIPER-2 — i setup \"cecchino\" con informazione nel livello (sweep-and-reclaim, FVG della mattina, ORB 5 minuti a 10 R)"
data: "2026-10-21"
strumenti:
  - "MNQ"
  - "MES"
  - "M2K"
  - "MYM"
finestra: "MNQ, MES, M2K, MYM 1 minuto 2019-05..2026-10-20 (1.762-1.790 sessioni)"
verdetto: "non confermata"
pubblicabilita: "avvertenza"
avvertenza: "(trades.csv derivati da dati licenziati; solo aggregati). Insieme a SNIPER-1 forma lo studio a rapporto rendimento/rischio alto e winrate basso richiesto dal proprietario."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L10252-L10261"
prove:
  - "runtime/proofs/sniper2/sniper2.json"
  - "runtime/proofs/sniper2/sniper2_trades.csv"
  - "runtime/proofs/sniper2/truth.json"
  - "runtime/proofs/sniper2/run.log"
  - "runtime/proofs/sniper2/PIANO.md"
---

## Domanda

se il livello d'ingresso porta informazione (estremo della notte o di ieri violato e rientrato, gap della mattina, ORB 5 minuti con obiettivo 10 R), la geometria 1:6-1:10 ha edge?

## Metodo e rubrica

32 righe per strumento (128 p unilaterali), BH q 0,10; placebo doppio (lato a caso; livello spostato di 0,3-0,7 A); misura per trade con t sui giorni; CONFERMATA solo se tutti i criteri in verifica. Rubrica prima: sì (L10227); controlli di verità (passeggiata casuale 0 righe BH; edge piantato 0,10 A trovato con t 7-12).

## Esito

| Risultato | Fonte |
|---|---|
| "Esecuzione PASS, verdetto NON CONFERMATA: nessuna delle 128 p... passa BH q 0,10 in scoperta (q = 1,00 ovunque)", 2 righe su 32 con media positiva, t da -4,06 a +0,18 | docs/EXECUTION_LEDGER.md#L10252-L10261 |
| vincenti meno pareggio mediana -1,0 punti in scoperta e -1,1 in verifica. | docs/EXECUTION_LEDGER.md#L10252-L10261 |
| Riga più vicina S5 ORB stop strutturale obiettivo 10 S: scoperta +0,0015 A (t +0,18; 1.830 trade; vincenti 17,3% contro p* 10,2%) -> verifica -0,0135 A (t -1,45; 1.112 trade; 1 strumento su 4 positivo). | docs/EXECUTION_LEDGER.md#L10252-L10261 |
| Netto USD delle 32 righe negativo in ogni anno 2019-2026. | docs/EXECUTION_LEDGER.md#L10252-L10261 |
| MNQ da solo: verifica t massima +2,20 (S4 FVG) e +2,11 (S5): "osservazioni a posteriori... non prove". | docs/EXECUTION_LEDGER.md#L10252-L10261 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "anche i livelli con informazione... vincono quanto serve al pareggio e non di più... La famiglia 'stop stretto, obiettivo lontano' è esaurita su questi dati" (68 righe in due studi)
- potenza: vantaggi sotto circa +0,05 A per trade non rilevabili
- raccomandazione C2: FERMARE la famiglia.

## Prove

- runtime/proofs/sniper2/sniper2.json
- runtime/proofs/sniper2/sniper2_trades.csv
- runtime/proofs/sniper2/truth.json
- runtime/proofs/sniper2/run.log
- runtime/proofs/sniper2/PIANO.md
