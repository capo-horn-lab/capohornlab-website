---
id: "phase-1"
titolo: "PHASE-1 — 12 fasi cicliche di mercato e assegnazione delle strategie"
data: "2026-10-19"
strumenti: []
finestra: "221 strategie x 12 fasi (tendenza x volatilità x carattere)"
verdetto: "verdetto non estratto: vedi Esito"
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L7643-L7643"
prove:
  - "runtime/proofs/phase1/phase1.json"
---

## Domanda

ogni strategia ha fasi in cui funziona e si può accenderla solo lì?

## Metodo e rubrica

Fase nota a chiusura precedente; assegnazione n≥30, media>0, t≥2; walk-forward ancorato (blocchi di 20 sessioni), BH q≤0,10. Rubrica prima: sì (titolo "rubrica PRIMA dei risultati", L7609).

## Esito

| Risultato | Fonte |
|---|---|
| "221 strategie x 12 fasi; 0 CONFERMATE." | docs/EXECUTION_LEDGER.md#L7643-L7643 |
| Solo 3 strategie con almeno una fase significativa in scoperta (verifica +5,10 t 0,68, +1,80 t 0,19, -2,45) | docs/EXECUTION_LEDGER.md#L7643-L7643 |
| walk-forward 5 strategie positive, nessuna significativa | docs/EXECUTION_LEDGER.md#L7643-L7643 |
| media di verifica negativa in 11 fasi su 12. | docs/EXECUTION_LEDGER.md#L7643-L7643 |

## Lettura e limiti (dal registro)

- "Il filtro esiste... ma con le strategie attuali non assegna edge provati."

## Prove

- runtime/proofs/phase1/phase1.json
