---
id: "assorb-1"
titolo: "ASSORB-1 e ASSORB-2 — l'assorbimento a un prezzo riduce la probabilità che il prezzo lo superi? (mappa del book come controllo)"
data: "2026-10-22"
strumenti:
  - "MNQ"
  - "ES"
finestra: "cattura L1/L2 dell'app dal 14/10/2026 (MNQ 12-26: una sola sessione regolare completa, 21/10; ES 12-26 una, 15/10; letti 88.530.242.981 byte, 270.131.798 righe)"
verdetto: "descrittivo · pass · confermato · non confermato"
audit: {"stato": "nota", "id": ["ASSORB-1"]}
pubblicabilita: "avvertenza"
avvertenza: "ASSORB-2: NOT_RUN."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L10394-L10416"
prove:
  - "runtime/proofs/assorb1/heatmap-2026-10-21.png"
  - "docs/research/ASSORB_RICERCA_2026-10-22.md"
---

## Ritiri e correzioni

- ASSORB-1: definizione incompatibile con MNQ, 0 eventi, "DESCRITTIVO" (L10397)

## Domanda

un livello con volume aggressivo molto sopra la norma "assorbito" regge più di un livello normale?

## Metodo e rubrica

Evento: finestra di 60 s con volume aggressivo ≥ q95 per prezzo/minuto/fascia oraria (lasciando fuori il giorno) e bid fermo ≥80%; esito "tiene" X tick (4/8/20) entro 30 minuti contro controllo e placebo (200); CONFERMATO/NON CONFERMATO/DESCRITTIVO (se <50 eventi o <5 giorni: "l'esito più probabile, dichiarato prima"). ASSORB-2: definizione ridisegnata (fascia di 4 tick, 20 s, volume ≥3x la mediana causale, corsa +16/-4 tick), da eseguire con ≥5 sessioni complete. Rubrica prima: sì (L10373, L10409).

## Esito

| Risultato | Fonte |
|---|---|
| ASSORB-1: "Esito: DESCRITTIVO con 0 eventi e 0 controlli. La definizione congelata (bid fermo su un solo prezzo per l'80% di 60 s) è incompatibile con la granularità di MNQ": escursione mediana di un minuto 53 tick | docs/EXECUTION_LEDGER.md#L10394-L10416 |
| su 789 finestre regolari il bid sta al minimo del minuto per lo 0,07% del tempo (massimo 3,7%). | docs/EXECUTION_LEDGER.md#L10394-L10416 |
| Verità PASS: book ricostruito uguale al bid L1 nel 97,11% dei secondi del 21/10 (98,71% su tutti i secondi MNQ). | docs/EXECUTION_LEDGER.md#L10394-L10416 |
| Descrittivo: 27.488 "muri" MNQ (3 sessioni): il 95,7% di quelli raggiunti ritirato prima del tocco | docs/EXECUTION_LEDGER.md#L10394-L10416 |
| dopo il tocco rimbalzo 494 contro rottura 501 (49,6%) contro il 49,5% dei livelli normali. | docs/EXECUTION_LEDGER.md#L10394-L10416 |
| ASSORB-2: rubrica registrata, NON eseguita (in attesa di ≥5 sessioni MNQ complete). | docs/EXECUTION_LEDGER.md#L10394-L10416 |

## Cosa NON dice

- "La domanda resta senza risposta; la definizione non è stata cambiata dopo i dati"
- "i muri visibili non tengono più di un prezzo qualsiasi"
- rischio nella cattura: lato dell'aggressore ambiguo nell'8,9% degli scambi MNQ del 21/10 e nel 31% di ES del 15/10.

## Prove

- runtime/proofs/assorb1/
- runtime/proofs/assorb1/heatmap-2026-10-21.png
- runtime/research/capture/
- docs/research/ASSORB_RICERCA_2026-10-22.md
