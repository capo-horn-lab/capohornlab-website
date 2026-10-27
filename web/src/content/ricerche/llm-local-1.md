---
id: "llm-local-1"
titolo: "LLM-LOCAL-1/2, RAG-2/3, EVAL-2, PROMPT-1, NOISE-1, LAT-2, NOTA-1 — il modello linguistico locale dell'app (LFM2.5-24B-A2B)"
data: "2026-10-19"
strumenti: []
finestra: "modello LiquidAI LFM2.5-24B-A2B (Q6_K) e variante uncensored/Heretic; prova di riferimento di 50"
verdetto: "non confermata · confermata · pass · blocked_env"
pubblicabilita: "avvertenza"
avvertenza: "valutazione di un modello di terzi su domande interne; non è un benchmark generale."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L9326-L9373"
prove:
  - "runtime/llm/valutazione.json"
---

## Domanda

specializzare il modello con RAG, LoRA, sistema/prompt o quantizzazione lo rende migliore per l'app?

## Metodo e rubrica

Stessa prova, stesso giudice a parole chiave (mai un altro modello), 1-2 tentativi; criteri di adozione fissati prima (es. +10 punti su 50, o +3 contro il modello di riferimento). Rubrica prima: sì (L9268, L9412, L9620, L9627, L9647, L9653, L9661).

## Esito

| Risultato | Fonte |
|---|---|
| Base 16/50 (progetto 0/30, generali 16/20) | docs/EXECUTION_LEDGER.md#L9326-L9373 |
| +RAG 42-44/50 (progetto 24/30) | docs/EXECUTION_LEDGER.md#L9326-L9373 · docs/EXECUTION_LEDGER.md#L9576-L9667 |
| LoRA v1 20/50 (NON CONFERMATA: costa 2-5 punti sulle generali) | docs/EXECUTION_LEDGER.md#L9326-L9373 |
| uncensored + RAG 2 tentativi 46/50 contro 44 (+2, "nessuna variante raggiunge i +3"): NON ADOTTATO | docs/EXECUTION_LEDGER.md#L9326-L9373 · docs/EXECUTION_LEDGER.md#L9576-L9667 |
| RAG-2 BM25: "50 su 50 (progetto 30 su 30, generali 20 su 20)", ADOTTATO | docs/EXECUTION_LEDGER.md#L9326-L9373 |
| EVAL-2 partenza 53/80 (lettura 5/30) -> RAG-3 55/80 -> PROMPT-1 57/80 (NON ADOTTATA) | docs/EXECUTION_LEDGER.md#L9326-L9373 · docs/EXECUTION_LEDGER.md#L9576-L9667 |
| NOISE-1: due corse identiche 55 e 60 su 80, "rumore di corsa: circa 5 punti su 80" | docs/EXECUTION_LEDGER.md#L9326-L9373 · docs/EXECUTION_LEDGER.md#L9576-L9667 |
| LAT-2: Q6_K 52,2 token/s, Q4_K_M 60,6 (+16%, sotto il +20%): NON ADOTTATA. | docs/EXECUTION_LEDGER.md#L9576-L9667 |
| NOTA-1: nota serale 78,8 s, 0 numeri inventati. | docs/EXECUTION_LEDGER.md#L9576-L9667 |

## Cosa NON dice

- "il modello non sbagliava le domande di progetto, le mancava il pezzo giusto" (recupero BM25)
- la prova è satura a 50/50
- regola di misura: due corse e confronto delle medie, differenze sotto ~5/80 non contano.

## Prove

- runtime/llm/risultati_*.json
- runtime/llm/valutazione.json
