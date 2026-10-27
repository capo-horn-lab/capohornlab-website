---
id: "ovn-1"
titolo: "OVN-1 e GOLDN-1 — da dove viene il guadagno della famiglia MR (notte o giorno); oro di notte"
data: "2026-10-19"
strumenti:
  - "MES"
  - "MNQ"
  - "M2K"
  - "MYM"
  - "MGC"
finestra: "MES, MNQ, M2K, MYM 2019-2026 (OVN-1); MGC 2019-2026 (GOLDN-1)"
verdetto: "OVN-1: confermati · GOLDN-1: non confermato"
pubblicabilita: "avvertenza"
avvertenza: "(decadimento dal 2021; stessi dati usati per l'IBS)."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L8572-L8579"
prove:
  - "runtime/proofs/ovn1/ovn1.json"
  - "runtime/proofs/goldn1/goldn1.json"
---

## Domanda

TT, 3WEAK e IBS guadagnano nella notte (15:59-9:29 ET) o il giorno dopo? L'oro rende di notte?

## Metodo e rubrica

3 prove (una per regola), t giorni≥2, placebo 200, DSR. Rubrica prima: sì (L8559).

## Esito

| Risultato | Fonte |
|---|---|
| OVN-1: "CONFERMATI TT e 3WEAK tenuti solo di notte; IBS no": TT notte 161 trade +33,8 bp (t giorni 2,23, placebo p95 12,6, DSR 0,996, q 0,022) | docs/EXECUTION_LEDGER.md#L8572-L8579 |
| 3WEAK notte 189 trade +26,4 (t 2,33, p95 9,8) | docs/EXECUTION_LEDGER.md#L8572-L8579 |
| IBS notte 1.408 trade +4,3 (t 1,10, sotto il p95 5,8). | docs/EXECUTION_LEDGER.md#L8572-L8579 |
| GOLDN-1: "NON CONFERMATO": notte lungo 1.898 trade +3,17 bp (t giorni 1,60, p95 4,62, DSR 0,72). | docs/EXECUTION_LEDGER.md#L8572-L8579 |

## Cosa NON dice

- "il rimbalzo avviene in gran parte nelle prime ore della sessione notturna (prima delle 2:00 ET)"
- "Calo forte dal 2021 per entrambe le versioni" (TT metà 2019-2020 +80,0, 2021-2026 +15,3).

## Prove

- runtime/proofs/ovn1/ovn1.json
- runtime/proofs/goldn1/goldn1.json
