---
id: "vxprem-2"
titolo: "VXPREM-2 — robustezza della regola \"corto VX1 quando il premio P2 è nel terzo alto\""
data: "2026-10-20"
strumenti:
  - "VX"
  - "VIX"
finestra: "stessi dati di VXPREM-1 (174 CSV Cboe VX, VIX)"
verdetto: "verdetto non estratto: vedi Esito"
pubblicabilita: "avvertenza"
avvertenza: "Avvertenza forte: strategia a rischio illimitato sulla volatilità (corto VX)"
fonte_ledger: "docs/EXECUTION_LEDGER.md#L10077-L10087"
prove:
  - "runtime/proofs/vxprem2/vxprem2.json"
---

## Domanda

la regola confermata alla lettera in VXPREM-1 è robusta a 5 varianti (soglia, contratto, periodo, ritardo)?

## Metodo e rubrica

ROBUSTA se l'originale passa e ≥4 delle 5 varianti hanno in verifica media positiva con t≥1,5; altrimenti FRAGILE. Rubrica prima: sì (L10071).

## Esito

| Risultato | Fonte |
|---|---|
| "ROBUSTA (l'originale passa; 4 varianti su 5 con media positiva e t ≥ 1,5; cede solo il ritardo di un giorno)": originale +109,1 USD/giorno (t 2,50, 709 giorni, p95 91,8) | docs/EXECUTION_LEDGER.md#L10077-L10087 |
| soglia mediana +66,8 (t 1,96) | docs/EXECUTION_LEDGER.md#L10077-L10087 |
| quartile alto +85,2 (t 1,65) | docs/EXECUTION_LEDGER.md#L10077-L10087 |
| VX2 +59,2 (t 1,58, p95 55,9) | docs/EXECUTION_LEDGER.md#L10077-L10087 |
| senza 15/2-30/4/2020 +81,3 (t 2,27) | docs/EXECUTION_LEDGER.md#L10077-L10087 |
| ritardo di un giorno +52,3 (t 1,39). | docs/EXECUTION_LEDGER.md#L10077-L10087 |
| Controllo P1 +4,1 (t 0,16). | docs/EXECUTION_LEDGER.md#L10077-L10087 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Lettura e limiti (dal registro)

- "il segno è stabile in verifica, l'ampiezza e la tempistica no; resta una pista sul premio dei future VIX, non una regola"
- stare sempre corti rende già +48 USD/giorno
- in scoperta 2014-2018 tutte le varianti valgono circa zero
- il VX non è tra gli strumenti del bot.

## Prove

- runtime/proofs/vxprem2/vxprem2.json
