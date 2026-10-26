---
id: "sig-1"
titolo: "SIG-1 — mappa dei segnali per timeframe (modo A \"media\", modo B \"setup rari\")"
data: "2026-10-18"
strumenti:
  - "MES"
  - "MNQ"
  - "MCL"
finestra: "MES, MNQ, MCL a 5 m, 1 h, giornaliero (periodi come SENT-3: addestramento <60%, selezione 60-80%, test >80%)"
verdetto: "confermata"
pubblicabilita: "avvertenza"
avvertenza: "(descrittivo, non un segnale operativo; dati licenziati solo aggregati)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L7140-L7173"
prove:
  - "runtime/proofs/sig1/sig1.json"
  - "runtime/proofs/sig1/engine_mes5m.json"
  - "docs/research/SIG1_SEGNALI_OCS_ICT_ADATTIVO_2026-10-18.md"
---

## Domanda

quali segnali aiutano il motore (A) o funzionano come setup rari (B)?

## Metodo e rubrica

IC di Spearman con t per giorno + BH q≤0,10 (A, 965 test); ingresso nella coda ~1/settimana, netto dopo costo, t per settimana, BH (B, 3.860 test). Rubrica prima: sì (L6964+).

## Esito

| Risultato | Fonte |
|---|---|
| 965 test A e 3.860 test B. 5 m modo A: 102 segnali x strumento aiutano, quasi tutti con verso contrario (inversione), ampiezza 0,03-0,24 bp contro costo 0,8-1,7 bp (MCL 6,7): "nessuno è sfruttabile da solo". | docs/EXECUTION_LEDGER.md#L7140-L7173 |
| MNQ 5 m B: distanza dal VWAP > 132 punti -> corto per 5 minuti: +2,0 bp (selezione, 19 ingressi) e +7,9 bp (test, 41), t 2,54, q 0,071 | docs/EXECUTION_LEDGER.md#L7140-L7173 |
| 2026: 35 ingressi +1,2 bp. | docs/EXECUTION_LEDGER.md#L7140-L7173 |
| MES giornaliero B: "oscillatori in vendita" -> lungo 5 giorni +48,7 bp, t 3,19, ma contro la deriva rialzista l'eccesso è +18,0 bp t 1,18 ("valgono soprattutto per il rialzo del mercato"). | docs/EXECUTION_LEDGER.md#L7140-L7173 |

## Cosa NON dice

- Controllo contro la deriva (sempre lunghi: 6,5 bp a 1 giorno, 32,5 a 5 giorni) aggiunto a posteriori, dichiarato "non in rubrica".

## Prove

- runtime/proofs/sig1/sig1.json
- runtime/proofs/sig1/engine_mes5m.json
- docs/research/SIG1_SEGNALI_OCS_ICT_ADATTIVO_2026-10-18.md
