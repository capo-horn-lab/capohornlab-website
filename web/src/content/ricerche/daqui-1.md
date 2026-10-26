---
id: "daqui-1"
titolo: "DAQUI-1 — \"da qui\" (vicini storici) ed escursione residua"
data: "2026-10-22"
strumenti:
  - "MNQ"
finestra: "MNQ; k=240 vicini scelto sulla scoperta 2019-2023 tra 60/120/240 (Brier base 0,224286, k60 0,225614, k120 0,224052, k240 0,223408); verifica congelata 2024-2026 (697 giorni, 8.361 punti)"
verdetto: "descrittivo"
pubblicabilita: "avvertenza"
avvertenza: "verifica solo su MNQ; esito descrittivo (l'intervallo contiene lo zero)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L10530-L10533"
prove:
  - "docs/research/DAQUI_RICERCA_2026-10-22.md"
---

## Domanda

guardare le sessioni storiche più simili alla situazione attuale (da_qui) migliora la frequenza di base?

## Metodo e rubrica

Brier dei vicini contro la base, bootstrap per giorno al 95%; prova di verità su passeggiata casuale. Rubrica prima: sì (L10523).

## Esito

| Risultato | Fonte |
|---|---|
| "descrittivo: non migliora la frequenza di base": Brier vicini 0,237796 contro base 0,237992, differenza -0,000196, intervallo [-0,001186, +0,000699] contiene lo 0. | docs/EXECUTION_LEDGER.md#L10530-L10533 |

## Cosa NON dice

- `escursione_residua` "senza verifica propria (descrittiva)"
- verifica solo su MNQ
- prova all'apertura di lunedì 26/10 NOT_RUN.

## Prove

- runtime/proofs/daqui1/
- docs/research/DAQUI_RICERCA_2026-10-22.md
