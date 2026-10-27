---
id: "sent-3"
titolo: "SENT-3 — loop di miglioramento del motore di sentiment (5 giri, voto 1-100)"
data: "2026-10-18"
strumenti:
  - "MES"
  - "MNQ"
  - "MCL"
finestra: "MES, MNQ, MCL"
verdetto: "verdetto non estratto: vedi Esito"
pubblicabilita: "avvertenza"
avvertenza: "riferimenti a Investing.com/Barchart/TipRanks solo come descrizione (non ricostruiti)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L6730-L6860"
prove:
  - "runtime/proofs/sent3/valutazioni.json"
  - "docs/research/PIANO_OPERATIVO_SENTIMENT_2026-10-18.md"
  - "docs/research/SENT3_SENTIMENT_PUBBLICI_2026-10-18.md"
---

## Domanda

aggiungere famiglie di input (flusso ordini, mercati collegati, sessione, eventi, VIX, formule) alza il voto di veridicità e funzionamento del motore di SENT-2?

## Metodo e rubrica

Rubrica a voto (V1-V4 verità 55 + F1-F4 funzionamento 45), bootstrap a blocchi di giorni 1000 ricampionamenti; modifiche dichiarate PRIMA di ogni giro; il test non decide nulla. Rubrica prima: sì.

## Esito

| Risultato | Fonte |
|---|---|
| Voti: giro 1 = 54 | docs/EXECUTION_LEDGER.md#L6730-L6860 |
| giro 2 = 53 | docs/EXECUTION_LEDGER.md#L6730-L6860 |
| giro 3 = 64,5 | docs/EXECUTION_LEDGER.md#L6730-L6860 |
| giro 4 = 64,5 | docs/EXECUTION_LEDGER.md#L6730-L6860 |
| giro 5 = 64,5. | docs/EXECUTION_LEDGER.md#L6730-L6860 |
| "FINE DEL LOOP: tre valutazioni consecutive uguali... Voto finale 64,5/100." | docs/EXECUTION_LEDGER.md#L6730-L6860 |
| Affidabili solo MES 5 m (strong sell, sell, buy), MNQ 5 m (sell, buy) e MCL 5 m (sell, buy) | docs/EXECUTION_LEDGER.md#L6730-L6860 |
| gli altri timeframe "non affidabile". | docs/EXECUTION_LEDGER.md#L6730-L6860 |
| Test: veritiero MES 5 m | docs/EXECUTION_LEDGER.md#L6730-L6860 |
| MNQ 5 m buy "dice 53,7%, succede il 56,7%". | docs/EXECUTION_LEDGER.md#L6730-L6860 |

## Lettura e limiti (dal registro)

- Spostamenti previsti 0,1-0,4 punti base sotto il costo di andata e ritorno (0,8-5,6 punti base)
- "F1 2/15 e F2 0/10 sono strutturali con i dati disponibili".

## Prove

- runtime/proofs/sent3/round0..round5.json
- runtime/proofs/sent3/valutazioni.json
- docs/research/PIANO_OPERATIVO_SENTIMENT_2026-10-18.md
- docs/research/SENT3_SENTIMENT_PUBBLICI_2026-10-18.md
