---
id: "sniper-1"
titolo: "SNIPER-1 — strategia \"cecchino\": trend Ichimoku, limite al bordo della nuvola all'apertura, stop stretto, obiettivo lontano"
data: "2026-10-21"
strumenti:
  - "MNQ"
  - "MES"
  - "M2K"
  - "MYM"
finestra: "MNQ, MES, M2K, MYM 1 minuto 2019-05..2026-10-20 (MES 1.780 sessioni, MNQ 1.790, M2K 1.762, MYM 1.774; scoperta 2019-05..2023-12, verifica 2024-01..2026-10)"
verdetto: "non confermata"
pubblicabilita: "avvertenza"
avvertenza: "esito negativo ben documentato; `sniper1_trades.csv` contiene tracce di trade derivate da dati licenziati (solo aggregati)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L10200-L10213"
prove:
  - "runtime/proofs/sniper1/sniper1.json"
  - "runtime/proofs/sniper1/sniper1_trades.csv"
  - "runtime/proofs/sniper1/truth.json"
  - "runtime/proofs/sniper1/run.log"
  - "runtime/proofs/sniper1/PIANO.md"
---

## Domanda

"una strategia con winrate del 50% deve avere un rr di 1:1,5 e più"; sell limit al bordo della nuvola, stop ~100 tick, obiettivo ~800 tick, pareggio al 12,5% di vincenti): la geometria stop stretto/obiettivo lontano, con trend Ichimoku, ha edge?

## Metodo e rubrica

Ichimoku 9/26/52 a 5 minuti letta in modo causale; 36 righe per strumento (3 stop x 4 obiettivi x 3 letture); BH q 0,10; placebo 200; costi 1,90 USD a giro + 1 tick. Rubrica prima: sì ("rubrica PRIMA del codice e dei risultati", L10176); controlli di verità PRIMA dei risultati.

## Esito

| Risultato | Fonte |
|---|---|
| "Esecuzione PASS, verdetto NON CONFERMATA: nessuna delle 36 righe passa BH q 0,10 in scoperta (q = 1,00 ovunque, 8 righe su 36 con media positiva)". | docs/EXECUTION_LEDGER.md#L10200-L10213 |
| In tutte le righe la quota di vincenti sta attorno al pareggio p*: obiettivo 8 S vincenti 13-20% contro p* 12-13% | docs/EXECUTION_LEDGER.md#L10200-L10213 |
| 4 S 20-23% contro 22-25%. | docs/EXECUTION_LEDGER.md#L10200-L10213 |
| Riga più vicina: S 0,10 T 8S short scoperta +0,0122 A (t +0,76; 541 trade, vincenti 13,7%) -> verifica -0,0150 (t -0,95). | docs/EXECUTION_LEDGER.md#L10200-L10213 |
| Netto USD sui 4 strumenti negativo in ogni riga e fase (da -418 a -8.272 USD) | docs/EXECUTION_LEDGER.md#L10200-L10213 |
| per anno 2019 -364, 2020 +327, 2021 -753, 2022 -1.000, 2023 +102, 2024 -836, 2025 -112, 2026 -1.695. | docs/EXECUTION_LEDGER.md#L10200-L10213 |
| Trend Ichimoku alle 9:29: RIBASSO 425-458, RIALZO 592-626 sessioni per strumento. | docs/EXECUTION_LEDGER.md#L10200-L10213 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "la geometria 'stop 100 tick, obiettivo 800 tick' vince esattamente quanto serve al pareggio e non di più... Per avere edge non basta il rapporto: serve che il livello d'ingresso o la zona obiettivo contengano informazione." Nota di onestà: la media "per giorno con trade" nasce dal 46% dei giorni con un solo strumento in trade (media per trade -0,0135 A, -3,12 USD)
- da SNIPER-2 la misura è per trade con t sui giorni.
- Sensibilità barra d'ingresso: fermati nella barra d'ingresso S 0,05 A 25,0% / 27,1%
- 0 righe su 36 passano BH in lettura ottimistica.

## Prove

- runtime/proofs/sniper1/sniper1.json
- runtime/proofs/sniper1/sniper1_trades.csv
- runtime/proofs/sniper1/truth.json
- runtime/proofs/sniper1/run.log
- runtime/proofs/sniper1/PIANO.md
