---
id: "flash-1"
titolo: "FLASH-1 e FLASH-2 — \"dopo un flash crash il mercato è più calmo/fragile/rimbalza?\""
data: "2026-10-19"
strumenti:
  - "MES"
finestra: "MES 1 minuto 2019-2026 (eventi dal 2022 in FLASH-1, dal 2019 in FLASH-2), 4 definizioni (k 1,5/2,5 x m 15/60 minuti)"
verdetto: "senza verdetto nel registro"
audit: {"stato": "nota", "id": ["FLASH-1"]}
pubblicabilita: "avvertenza"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9002-L9002"
prove:
  - "runtime/proofs/flash1/flash1.json"
  - "runtime/proofs/flash2/flash1.json"
---

## Ritiri e correzioni

- FLASH-1 (L9002): "NON VALIDO per un errore del disegno registrato"; sostituito da FLASH-2 (L9010).

## Domanda

dopo un crollo intraday la volatilità cala (tesi del "reset"), aumenta la fragilità, c'è un rimbalzo, rende di più l'IBS?

## Metodo e rubrica

Eventi vs placebo abbinati (terzile di sigma prevista, stato di stress), Bonferroni su 24 (p<0,0021). Rubrica prima: sì (L8989, L9004).

## Esito

| Risultato | Fonte |
|---|---|
| FLASH-1: "NON VALIDO per un errore del disegno registrato, nessuna conclusione" (placebo scelti "senza eventi nelle 20 sessioni prima e dopo"). | docs/EXECUTION_LEDGER.md#L9002-L9002 |
| FLASH-2: "la tesi 'un flash crash stabilizza il mercato' NON è sostenuta dai dati MES 2019-2026": H1 CONFERMATA nel verso OPPOSTO (volatilità delle 20 sessioni dopo più ALTA: log +0,53 / +0,26 / +0,69 / +0,46; p 0,000 / 0,000 / 0,018 / 0,002) | docs/EXECUTION_LEDGER.md#L9010-L9015 |
| H2 fragilità nessuna differenza | docs/EXECUTION_LEDGER.md#L9002-L9002 · docs/EXECUTION_LEDGER.md#L9010-L9015 |
| H3 rimbalzo nessuno significativo | docs/EXECUTION_LEDGER.md#L9002-L9002 · docs/EXECUTION_LEDGER.md#L9010-L9015 |
| grappoli indipendenti 33 / 90 / 8 / 26. | docs/EXECUTION_LEDGER.md#L9010-L9015 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- "dopo i crolli la volatilità resta alta per settimane; non c'è un 'reset'"
- potenza bassa (pochi grappoli)
- "'nessun effetto' non smentisce la tesi, la lascia non dimostrata".

## Prove

- runtime/proofs/flash1/flash1.json
- runtime/proofs/flash2/flash1.json
- prova non trovata su disco: runtime/proofs/flash2/flash2.json
- runtime/proofs/flash2
