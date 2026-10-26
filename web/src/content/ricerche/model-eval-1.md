---
id: "model-eval-1"
titolo: "MODEL-EVAL-1 — modelli locali: utilità del Qwen3.8 2.4T e confronto"
data: "2026-10-17"
strumenti: []
finestra: "non è uno studio di mercato: valutazione di modelli linguistici locali (Qwen3.8-2.4T, Qwen3.8-27B, LFM2.5-24B-A2B, gpt-oss-120b)."
verdetto: "descrittivo"
pubblicabilita: "avvertenza"
avvertenza: "è un confronto di modelli di terzi su prove interne di 20 domande, non un benchmark generale; percorsi locali da omettere."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L6282-L6282"
prove:
  - "runtime/research/llm_eval/bench.md"
  - "docs/research/MODELLI_LOCALI_2026-10-17.md"
---

## Domanda

non è uno studio di mercato: valutazione di modelli linguistici locali (Qwen3.8-2.4T, Qwen3.8-27B, LFM2.5-24B-A2B, gpt-oss-120b).

## Metodo e rubrica

Prove locali una alla volta (llama-server Vulkan, temperatura 0): MMLU-20, calcoli, JSON, commenti; llama-bench. Rubrica prima: no (nessun criterio numerico congelato nel testo).

## Esito

| Risultato | Fonte |
|---|---|
| "gpt-oss-120b il migliore (MMLU-20 19/20, calcoli ragionando 12/12 in 7,5 s, JSON 11/12, commenti 6/6, 37-40 tok/s)" | docs/EXECUTION_LEDGER.md#L6335-L6341 · docs/EXECUTION_LEDGER.md#L6282-L6282 |
| 2.4T: decode 0,355 tok/s. | docs/EXECUTION_LEDGER.md#L6282-L6282 · docs/EXECUTION_LEDGER.md#L6335-L6341 |

## Cosa NON dice

- Nessuna modifica all'app
- Qwen3.8-Flash-Next NOT_RUN.

## Prove

- runtime/research/llm_eval/*.json
- runtime/research/llm_eval/bench.md
- docs/research/MODELLI_LOCALI_2026-10-17.md
