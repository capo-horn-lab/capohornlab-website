---
id: "aperture-mondo-1"
titolo: "APERTURE-MONDO-1 — aperture e caso d'apertura dei future europei (DAX, EURO STOXX 50)"
data: "2026-10-23"
strumenti:
  - "FDXM"
  - "FDXS"
  - "FESX"
  - "FSXE"
finestra: "FDXM/FDXS (1.071.095 barre dal 19/04/2021), FESX, FSXE (370.504 barre), 2019-2026"
verdetto: "senza verdetto nel registro"
pubblicabilita: "avvertenza"
avvertenza: "orari ufficiali di terzi"
fonte_ledger: "docs/EXECUTION_LEDGER.md#L10615-L10620"
prove:
  - "docs/research/APERTURE_MONDO_2026-10-23.md"
---

## Domanda

il caso d'apertura (soglia scalata su A) ha frequenze stabili sui mercati europei?

## Metodo e rubrica

Soglia S = 50 x A_indice/A_MNQ, ultime 10 sessioni; verifica congelata 2019-2023 contro 2024-2026; test 6 PASS, 5 mutanti su 5 uccisi. Rubrica prima: sì (L10607).

## Esito

| Risultato | Fonte |
|---|---|
| "Verifica congelata 2019-2023 contro 2024-2026: FAIL (cambiano 8 rami su 10 per il DAX e 7 su 10 per l'EURO STOXX 50)." | docs/EXECUTION_LEDGER.md#L10615-L10620 |
| Orari d'apertura in ora di Roma: Sydney 01:00, Tokyo 02:00, Hong Kong 03:30, Eurex 08:00, Xetra/Euronext/SIX/LSE 09:00, New York 15:30 (14:30 dal 26 al 30/10). | docs/EXECUTION_LEDGER.md#L10615-L10620 |

## Cosa NON dice

- Diagnosi scritta DOPO i risultati: "50 punti di MNQ valevano 0,56 A nel 2019 e 0,13 A nel 2026"
- con frazione di A costante i rami restano stabili (DAX 2/10, ESX 0/10): ipotesi da verificare solo su sessioni future.
- Lettura live NOT_RUN.

## Prove

- docs/research/APERTURE_MONDO_2026-10-23.md
- runtime/proofs/aperturemondo1/
