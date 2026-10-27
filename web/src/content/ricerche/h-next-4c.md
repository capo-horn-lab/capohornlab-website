---
id: "h-next-4c"
titolo: "H-NEXT-4c — la regola IBS su 30 ETF (settori, paesi, stile)"
data: "2026-10-20"
strumenti:
  - "SPY"
  - "QQQ"
finestra: "30 ETF Yahoo giornalieri dal 2006 (149.803 righe): 11 settori SPDR, 11 paesi, 6 stile, controllo SPY e QQQ; scoperta 2006-2019, verifica 2020-2026"
verdetto: "verdetto non estratto: vedi Esito"
pubblicabilita: "avvertenza"
avvertenza: "dati Yahoo solo aggregati"
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9455-L9499"
prove:
  - "runtime/proofs/sig2/ibs_etf_settori.json"
  - "runtime/proofs/sig2/ibs_etf_settori.run.log"
  - "runtime/research/etf_settori_ohlc.csv"
---

## Domanda

l'IBS è un effetto solo degli indici USA a larga capitalizzazione o di tutto il mercato USA e di altri paesi?

## Metodo e rubrica

Regola identica a H-NEXT-4b; CONFERMATO un simbolo solo se ≥30 trade in ciascun periodo, media>0, t≥2 in verifica, sopra il placebo p95, q≤0,10; verdetto di famiglia per quota di simboli. Rubrica prima: sì (L9395).

## Esito

| Risultato | Fonte |
|---|---|
| "CONFERMATI 14/30 (di cui 12 tra i 28 nuovi)" | docs/EXECUTION_LEDGER.md#L9455-L9499 |
| famiglie: settori "PARZIALE (5/11 confermati: XLK, XLF, XLY, XLB, XLC; scoperta forte 6/11)", paesi "PARZIALE (3/11 confermati: EWU, EWY, INDA; scoperta forte 8/11)", stile "CONFERMATA (4/6 confermati: MDY, DIA, IJR, IWF; scoperta forte 6/6)" | docs/EXECUTION_LEDGER.md#L9455-L9499 |
| media>0 in verifica 30/30 | docs/EXECUTION_LEDGER.md#L9455-L9499 |
| t≥2 in verifica 20/30 | docs/EXECUTION_LEDGER.md#L9455-L9499 |
| sopra il placebo p95 in verifica 16/30. | docs/EXECUTION_LEDGER.md#L9455-L9499 |
| Es.: XLK verifica 217 trade +89,4 bp (t 4,83) | docs/EXECUTION_LEDGER.md#L9455-L9499 |
| EWY +85 bp (85.2 nella tabella del ledger). | docs/EXECUTION_LEDGER.md#L9455-L9499 |
| Controllo pipeline: SPY PASS (374 trade, +47,12 bp, t 4,32), QQQ "FAIL letterale" (376 trade, +40,87 bp, t 3,31 contro 375, +40,74, 3,29: 0,13 bp oltre soglia, rumore dei prezzi Yahoo). | docs/EXECUTION_LEDGER.md#L9455-L9499 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Lettura e limiti (dal registro)

- "È un effetto di tutto il mercato azionario USA, più debole nei settori difensivi... Non è universale, coerente con IBS-EU NON confermata"
- i confermati "i CONFERMATI sono tutti correlati con SPY e dal 54% all'81% delle loro entrate di verifica cadono nello stesso giorno di un segnale SPY"
- costo di 2 bp ottimista per i paesi meno liquidi
- 30 test BH non indipendenti.

## Prove

- runtime/proofs/sig2/ibs_etf_settori.json
- runtime/proofs/sig2/ibs_etf_settori.run.log
- runtime/research/etf_settori_ohlc.csv
