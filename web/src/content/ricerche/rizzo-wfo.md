---
id: "rizzo-wfo"
titolo: "RIZZO-WFO — il modello locale RizzoFlow dentro l'ottimizzatore (passo 1: ha informazione?)"
data: "2026-10-19"
strumenti:
  - "MES"
finestra: "400 trade MES (periodo di verifica, un trade per strategia e giorno)"
verdetto: "verdetto non estratto: vedi Esito"
pubblicabilita: "avvertenza"
avvertenza: "esito negativo su un modello proprietario locale."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L7768-L7768"
prove:
  - "runtime/proofs/rizzo_wfo/step1.json"
  - "runtime/research/wfo/rizzo_cache.jsonl"
---

## Domanda

la probabilità P(TAKE) del modello locale predice il netto del trade?

## Metodo e rubrica

Spearman e AUC con bootstrap 95%; "informativo" solo se rho>0 con t≥2 e AUC>0,5. Rubrica prima: sì (L7746).

## Esito

| Risultato | Fonte |
|---|---|
| "NON INFORMATIVO": Spearman -0,084 (t -1,60), AUC 0,488 (IC 0,43-0,55) | docs/EXECUTION_LEDGER.md#L7768-L7768 |
| P(TAKE) media 0,67, TAKE nel 78,5% dei casi | docs/EXECUTION_LEDGER.md#L7768-L7768 |
| netto medio sopra la mediana di P(TAKE) -10,51 USD, sotto -8,10. | docs/EXECUTION_LEDGER.md#L7768-L7768 |
| Passo 2 non eseguito. | docs/EXECUTION_LEDGER.md#L7768-L7768 |

## Lettura e limiti (dal registro)

- "approva quasi tutto" (come ER-279)
- RizzoFlow resta come opzione dell'ottimizzatore, spenta di default.

## Prove

- runtime/proofs/rizzo_wfo/step1.json
- runtime/research/wfo/rizzo_cache.jsonl
