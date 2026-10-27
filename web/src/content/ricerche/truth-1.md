---
id: "truth-1"
titolo: "TRUTH-1 e TICK-1 — prova di verità della pipeline e tenuta dei risultati a 1 minuto sui tick"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MGC"
  - "M6E"
  - "MNQ"
finestra: "TRUTH-1: dati sintetici (passeggiata casuale con volatilità oraria reale) su MES, MGC, M6E e motore indipendente su dati reali; TICK-1: tick NinjaTrader 21/09-16/10/2026 su 11 contratti (da 159.569 tick su M6E a 42,2 milioni su MNQ), 2,47 milioni di trade"
verdetto: "senza verdetto nel registro"
audit: {"stato": "nota", "id": ["TRUTH-1"]}
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8928-L8943"
prove:
  - "runtime/proofs/truth1/truth1.json"
  - "runtime/proofs/truth1/t3.json"
  - "runtime/proofs/truth1/truth1_generatore_v1.json"
  - "runtime/proofs/tick1/tick1.json"
---

## Ritiri e correzioni

- TRUTH-1 T1 non passa al primo giro (generatore sintetico difettoso, L8981) e, anche col generatore v2, "NON PASSA" il criterio p95 dei placebo (L9026): il criterio è stato ristretto (placebo abbinato).

## Domanda

la pipeline trova un edge che c'è e non ne inventa uno che non c'è? I risultati a 1 minuto reggono sui tick?

## Metodo e rubrica

T1 nessun edge (72 walk), T2 edge piantato, T3 motore indipendente; TICK-1: confronto barre da tick contro barre NT, esiti dei trade. Rubrica prima: sì (L8899, L8920).

## Esito

| Risultato | Fonte |
|---|---|
| TRUTH-1: T3 "PASSA con un'eccezione dichiarata" (M6E ingressi uguali 98,6%, sotto la soglia 99%) | docs/EXECUTION_LEDGER.md#L8928-L8943 |
| T1 (v2) "candidati 0 (soglia <= 1 per seme: PASSA), t >= 2 nello 0% (soglia 5%: PASSA)" ma "media fuori campione sopra il p95 dei placebo nel 37,5% dei walk (soglia 10%: NON PASSA)" -> criterio ristretto con placebo abbinato | docs/EXECUTION_LEDGER.md#L9025-L9028 |
| T2 "trovato con ampio margine" (+249 bp t 18,2) e controllo negativo PASSA. | docs/EXECUTION_LEDGER.md#L9025-L9028 |
| TICK-1: "il motore a 1 minuto è ATTENDIBILE su tutti gli 11 contratti": barre da tick identiche a quelle NT nel 99,99-100% dei minuti | docs/EXECUTION_LEDGER.md#L8928-L8943 |
| esito diverso tra 0,15% (ZN) e 0,74% (MNQ) | docs/EXECUTION_LEDGER.md#L8928-L8943 |
| differenza media per trade da -0,19 bp (MBT) a +0,08 bp (MCL) | docs/EXECUTION_LEDGER.md#L8928-L8943 |
| segno del mese uguale tra 95,1% e 99,8%. | docs/EXECUTION_LEDGER.md#L8928-L8943 |

## Grafico

Test della scheda dal file runtime/research/sa-report/summary.json (r riga, n campioni, m media nell'unita' u, t statistica t, p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).

## Cosa NON dice

- Il test T1 "mostra che il criterio del p95 dei placebo va ristretto" (correzione 26-27)
- la prima versione di T1/T2 era invalidata da un generatore sintetico difettoso.

## Prove

- runtime/proofs/truth1/truth1.json
- runtime/proofs/truth1/t3.json
- runtime/proofs/truth1/truth1_generatore_v1.json
- runtime/proofs/tick1/tick1.json
