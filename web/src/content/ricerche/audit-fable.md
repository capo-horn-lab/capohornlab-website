---
id: "audit-fable"
titolo: "AUDIT-FABLE e REVIEW-FABLE-MAX — revisioni di tutto il codice e di tutte le analisi (ritiri di conferme)"
data: "2026-10-19"
strumenti: []
finestra: "4 agenti Fable 5.1 in sola lettura sui motori, indicatori, prove del giorno e risultati confermati"
verdetto: "confermato · ritirata · non confermato · adottata"
pubblicabilita: "avvertenza"
avvertenza: ""
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8945-L8973"
prove: []
---

## Domanda

i risultati confermati e il codice reggono?

## Metodo e rubrica

Revisione indipendente; correzioni numerate (17)-(27) applicate prima dei risultati v2. Rubrica prima: no (revisione, non studio).

## Esito

| Risultato | Fonte |
|---|---|
| "IBS-NT RIPRODOTTO identico (333 trade, +28,8 bp, t 2,43)". | docs/EXECUTION_LEDGER.md#L8945-L8973 |
| "DUE CONFERME RITIRATE": VOLREV-1 e GEX-1 -> "NON CONFERMATO" (artefatto di cambio contratto; terzili in dollari separano gli anni). | docs/EXECUTION_LEDGER.md#L8945-L8973 · docs/EXECUTION_LEDGER.md#L9035-L9046 |
| Nota: "IBS-NT regge con la rubrica registrata ma con margine sottile: t sui giorni d'ingresso 2,22, placebo p95 27,3 contro media 28,8... poggia soprattutto su M2K (MES t 1,48, MNQ 0,77)". | docs/EXECUTION_LEDGER.md#L8945-L8973 |
| REVIEW-FABLE-MAX: il criterio "sopra il p95 dei placebo" non distingue veri da nulli (39,3% contro 37,5%) | docs/EXECUTION_LEDGER.md#L8945-L8973 · docs/EXECUTION_LEDGER.md#L9035-L9046 |
| H-NEXT-6 "sottodimensionata" (t attesa 0,84 a 40 trade, serve test sequenziale SPRT). | docs/EXECUTION_LEDGER.md#L9035-L9046 |

## Cosa NON dice

- PERSIST-1 regge sulla condizione STRESS (21 delle 30 coppie)
- OVN-1 "dimezzato dal 2021"
- "F3 il solo confermato" è superato.

## Prove

- Nessun file di prova indicato dall'inventario: Rapporti nella trascrizione di sessione (non in file di proofs).
