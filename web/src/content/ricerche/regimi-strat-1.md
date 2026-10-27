---
id: "regimi-strat-1"
titolo: "REGIMI-STRAT-1 — le strategie rendono solo in certi regimi del classificatore k-means?"
data: "2026-10-25"
strumenti: []
finestra: "60 unità famiglia x strumento (6 x 10) con P&L OPT-ALL, 180 celle (60 x 3 regimi), 2.184 giorni (oos dalla 501ª)"
verdetto: "non confermato"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L10691-L10697"
prove:
  - "runtime/proofs/regimistrat1/regimistrat1.json"
  - "docs/research/REGIMI_RICERCA_2026-10-25.md"
---

## Domanda

accendere o pesare le strategie secondo il regime di REGIMI-1 migliora il libro?

## Metodo e rubrica

Domanda 1: Spearman tra le due metà sulle 180 differenze con nullo a spostamento circolare (500); Domanda 2: walk-forward 500/60, ACC e PESO contro B senza regimi, placebo. Rubrica prima: sì, "congelata PRIMA dei risultati" (L10682).

## Esito

| Risultato | Fonte |
|---|---|
| "NON CONFERMATO; il regime k-means nuovo non aggiunge nulla di utile." | docs/EXECUTION_LEDGER.md#L10691-L10697 |
| Domanda 1: Spearman fra le due metà d = 0,069 (p 0,334, p95 nullo 0,20), segni concordi 56%. | docs/EXECUTION_LEDGER.md#L10691-L10697 |
| Domanda 2: ACC Sharpe 1,09 contro B 1,39 (diff -0,29, p 0,78) | docs/EXECUTION_LEDGER.md#L10691-L10697 |
| PESO Sharpe 1,19 contro 1,08 (diff +0,07, p 0,38), sotto il placebo | docs/EXECUTION_LEDGER.md#L10691-L10697 |
| casi singoli credibili: MGC IBS -> crisi (d +5,96; m_crisi +8,47 contro calma +0,60 / trend +0,13). | docs/EXECUTION_LEDGER.md#L10691-L10697 |
| Regime per strumento (secondario): Spearman -0,09, NON CONFERMATO. | docs/EXECUTION_LEDGER.md#L10691-L10697 |

## Cosa NON dice

- "il 'crisi' del k-means è per lo più ALTA VOLATILITÀ (P(VOL\|crisi)=0,64), non lo STRESS VIX (P(STRESS\|crisi)=0,17)"
- "mean-reversion sui micro USA sempre accesa, non ridurre in volatilità/crisi".

## Prove

- runtime/proofs/regimistrat1/regimistrat1.json
- prova non trovata su disco: docs/research/REGIMI_STRAT_2026-10-25.md
- docs/research/REGIMI_RICERCA_2026-10-25.md
