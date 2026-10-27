---
id: "cot-1"
titolo: "COT-1 — posizionamento CFTC (Traders in Financial Futures) come segnale settimanale"
data: "2026-10-19"
strumenti: []
finestra: "CFTC TFF 2010-2026 (17 file, 7,2 MB), E-mini S&P 500 e Nasdaq mini, gruppi Asset Manager e Leveraged Funds"
verdetto: "senza verdetto nel registro"
audit: {"stato": "corretto", "id": ["COT-1"]}
pubblicabilita: "ok"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L7572-L7572"
prove:
  - "runtime/proofs/cot1/cot1.json"
---

## Ritiri e correzioni

- COT-1: primo giro scartato (L7570)

## Domanda

la posizione netta (z a 156 settimane, variazione) prevede il rendimento settimanale di SPY/QQQ?

## Metodo e rubrica

Spearman + Newey-West lag 1, scoperta 2010-2018 / verifica 2019-2026, BH q≤0,10 su 8 test. Rubrica prima: sì (L7543). Correzione prima del verdetto: primo giro scartato per abbinamento sbagliato dei mercati (L7570).

## Esito

| Risultato | Fonte |
|---|---|
| "0 su 8. Nessun segnale tiene il segno tra scoperta e verifica" (il migliore: Nasdaq asset manager, variazione settimanale, -0,032 in scoperta e +0,106 t 2,19 in verifica). | docs/EXECUTION_LEDGER.md#L7572-L7572 |

## Cosa NON dice

- Posizionamento al 13/10/2026 riportato solo come descrittivo.

## Prove

- runtime/proofs/cot1/cot1.json
- runtime/research/cot/
