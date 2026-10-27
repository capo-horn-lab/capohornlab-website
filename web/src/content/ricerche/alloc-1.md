---
id: "alloc-1"
titolo: "ALLOC-1, PERSIST-1, ALLOC-2, STRESS-OOS-1 — allocazione per condizioni di mercato e l'effetto \"stress\""
data: "2026-10-19"
strumenti:
  - "SPY"
  - "QQQ"
  - "IWM"
  - "DIA"
finestra: "857 strategie (≥30 trade) su 10 strumenti, 60 unità famiglia x strumento, 2.184 sessioni (fuori campione dalla 501ª); STRESS-OOS-1: SPY/QQQ (e IWM, DIA) 2009-2018, 2.336 sessioni, 192 giorni di stress in 65 episodi."
verdetto: "non confermato · confermato"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8628-L8633"
prove: []
---

## Domanda

accendere le strategie solo negli stati in cui hanno reso (ALLOC-1) o pesarle per stato (ALLOC-2) migliora? Le strategie rendono diversamente per condizione e la differenza si ripete (PERSIST-1)? Lo stress VIX (VIX>VIX3M) migliora la mean reversion in un periodo mai usato (STRESS-OOS-1)?

## Metodo e rubrica

Walk-forward 500/60, bootstrap a blocchi, placebo con stati spostati circolarmente (200-1.000). Rubrica prima: sì (L8610, L8635, L8652, L8669).

## Esito

| Risultato | Fonte |
|---|---|
| ALLOC-1: "NON CONFERMATO": A tutte accese +1,34 bp/sessione (t 4,16, Sharpe 1,61); C +1,70 (t 4,15, Sharpe 1,61) | docs/EXECUTION_LEDGER.md#L8628-L8633 |
| Sharpe(C)-Sharpe(B) +0,08, bootstrap p 0,105. | docs/EXECUTION_LEDGER.md#L8628-L8633 |
| PERSIST-1: "CONFERMATO, la premessa regge": Spearman tra le due metà sulle 180 coppie 0,30 (p 0,006), 30 coppie con q≤0,10 | docs/EXECUTION_LEDGER.md#L8646-L8650 |
| condizione che conta lo STRESS (7% delle sessioni, 128 giorni): IBS MES d +17,0 bp/sessione, MNQ +23,5, M2K +19,9. | docs/EXECUTION_LEDGER.md#L8646-L8650 |
| ALLOC-2: "NON CONFERMATO, nessuna delle due varianti": B +0,59 (t 2,81, Sharpe 1,09) | docs/EXECUTION_LEDGER.md#L8662-L8667 |
| C8 +0,64 (Sharpe 1,25), C8 contro B +0,15 di Sharpe, p 0,26. | docs/EXECUTION_LEDGER.md#L8662-L8667 |
| STRESS-OOS-1: A mean reversion "NON CONFERMATO per poco, direzione confermata": +77,9 bp in stress contro +18,1 bp (318 e 1.861 trade), d +59,8, p unilaterale 0,034 (serviva <0,025) | docs/EXECUTION_LEDGER.md#L8679-L8682 |
| B trend: nei giorni di stress -10,0 bp contro -0,1 (p 0,98). | docs/EXECUTION_LEDGER.md#L8679-L8682 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "la mean reversion sui micro USA resta accesa in ogni stato e NON va ridotta nello stress"
- il vantaggio dello stress è reale ma con il 7% di giorni "non si traduce in un libro migliore"
- il trend nello stress "dipendeva dal periodo (crolli 2020 e 2022)".

## Prove

- runtime/proofs/alloc1/*.json
- runtime/proofs/persist1/*.json
- runtime/proofs/alloc2/*.json
- runtime/proofs/stressoos1/*.json
