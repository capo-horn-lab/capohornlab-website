---
id: "jev-swap-1"
titolo: "JEV-SWAP-1 — RizzoFlow al posto del cancello Jev (installato e misurato, non sostituito)"
data: "2026-09-28"
strumenti:
  - "ES"
finestra: "replay di 39 intenti costruiti da barre ES 2024 reali con evidenza dello screener"
verdetto: "senza verdetto nel registro"
pubblicabilita: "avvertenza"
avvertenza: "modello e codici interni"
fonte_ledger: "docs/EXECUTION_LEDGER.md#L2059-L2073"
prove:
  - "docs/ERROR_RULES.md"
---

## Domanda

il modello locale RizzoFlow (Spark-X2.5-4B Q8) può fare da veto fail-closed al posto di Jev?

## Metodo e rubrica

Decisione singola e replay su intenti; revisione Codex indipendente. Rubrica prima: criteri di accettazione scritti all'apertura (L2045-L2057); nessun test statistico.

## Esito

| Risultato | Fonte |
|---|---|
| "INSTALLATO E MISURATO, NON SOSTITUITO". | docs/EXECUTION_LEDGER.md#L2059-L2073 |
| Decisione singola ALLOW conf=0,956, 652 ms | docs/EXECUTION_LEDGER.md#L2059-L2073 |
| replay 39 intenti "36/39 ALLOW", mediana 793 ms. | docs/EXECUTION_LEDGER.md#L2059-L2073 |
| con i criteri iniziali approvava 39 su 39 e un intento BUY contro evidenza 24 short su 26. | docs/EXECUTION_LEDGER.md#L2059-L2073 |
| Revisione Codex: FAIL sul contratto end-to-end. | docs/EXECUTION_LEDGER.md#L2059-L2073 |

1 righe della scheda non riportate: la prova citata non le contiene.

## Cosa NON dice

- "Non promuovere rizzo-flow a veto finche non rifiuta da solo su un corpus congelato di casi da respingere"
- è un replay del cancello, "non un backtest economico".

## Prove

- docs/ERROR_RULES.md
