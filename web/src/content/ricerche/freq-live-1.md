---
id: "freq-live-1"
titolo: "FREQ-LIVE-1 + documento TEORIA_MOVIMENTO — frequenze condizionate dal vivo (quanto e quando, non dove)"
data: "2026-10-21"
strumenti:
  - "MNQ"
  - "MES"
  - "M2K"
  - "MYM"
finestra: "MNQ (poi MES, M2K, MYM) 1 minuto NinjaTrader 2019-2026, ultime 60-250-500 sessioni, ora di Roma; documento del proprietario `docs/research/TEORIA_MOVIMENTO_2026-10-21.txt` (5.698 byte)"
verdetto: "senza verdetto nel registro"
pubblicabilita: "avvertenza"
avvertenza: "prezzi e VWAP di future CME aggiornati al minuto già pubblicati sul sito con via libera del proprietario del 26/10 (L10849): licenza dati a decisione del proprietario."
fonte_ledger: "docs/EXECUTION_LEDGER.md#L10287-L10303"
prove:
  - "runtime/proofs/freqsito1/locale-step2-nessun-dato.jpg"
  - "runtime/proofs/freqsito1/locale-step3-dati-pubblicati.jpg"
  - "runtime/proofs/freqsito1/locale-step5-backend-giu.jpg"
---

## Domanda

quanto si muove il mercato per finestra oraria, con che frequenza tocca massimo/minimo della notte, che cosa segue al caso dell'apertura (soglia 50 punti)?

## Metodo e rubrica

Frequenze empiriche p, k, n e margine 1,96·√(p(1-p)/n); finestre fisse di Roma; livelli (notte, ieri, VWAP, tondi) per fasce di distanza in frazioni di A (range medio delle 20 sessioni precedenti); condizionamento alla fase del percorso. Rubrica prima: sì, di accettazione (L10271); non è un test di ipotesi (nessun placebo né correzione per prove multiple, dichiarato).

## Esito

| Risultato | Fonte |
|---|---|
| Rubrica di accettazione PASS (5/5 + 4/4 dell'aggiunta; MNQ 1,9 s; ciclo a regime 2,6 s per 4 strumenti). | docs/EXECUTION_LEDGER.md#L10287-L10303 · docs/EXECUTION_LEDGER.md#L10285-L10285 |
| Documento: escursione mediana (60 sessioni, punti) 00:00-08:00 192, 08:00-14:30 195, 14:30-15:30 88, 15:30-16:00 162, 21:00-22:00 82 | docs/EXECUTION_LEDGER.md#L10287-L10303 · docs/research/TEORIA_MOVIMENTO_2026-10-21.txt#L27-L27 · docs/research/TEORIA_MOVIMENTO_2026-10-21.txt#L28-L28 · docs/research/TEORIA_MOVIMENTO_2026-10-21.txt#L29-L29 · docs/research/TEORIA_MOVIMENTO_2026-10-21.txt#L30-L30 · docs/research/TEORIA_MOVIMENTO_2026-10-21.txt#L84-L84 · docs/research/TEORIA_MOVIMENTO_2026-10-21.txt#L35-L35 |
| range medio sessione regolare 361 punti | docs/research/TEORIA_MOVIMENTO_2026-10-21.txt#L37-L37 |
| massimo della notte superato entro le 22:00: 0,00-0,15 A 87% (n 105), 0,15-0,30 A 67% (57), 0,30-0,50 A 59% (39), 0,50-1,00 A 42% (38), oltre 1 A 36% (11) | docs/research/TEORIA_MOVIMENTO_2026-10-21.txt#L69-L69 · docs/research/TEORIA_MOVIMENTO_2026-10-21.txt#L53-L53 · docs/research/TEORIA_MOVIMENTO_2026-10-21.txt#L54-L54 · docs/research/TEORIA_MOVIMENTO_2026-10-21.txt#L55-L55 · docs/research/TEORIA_MOVIMENTO_2026-10-21.txt#L56-L56 · docs/research/TEORIA_MOVIMENTO_2026-10-21.txt#L57-L57 |
| sopra il massimo notturno entro le 15:30 47%, entro le 22:00 69% | docs/research/TEORIA_MOVIMENTO_2026-10-21.txt#L58-L58 |
| minimo rotto 36% e 64%. | docs/research/TEORIA_MOVIMENTO_2026-10-21.txt#L59-L59 |
| Esempio 21/10 21:10 Roma: tondo sotto 29.900 nel 66% ±8 (91/137) | docs/EXECUTION_LEDGER.md#L10287-L10303 |
| caso dell'apertura in fase estensione, chiusura sopra l'apertura 44% ±12 (30/69). | docs/EXECUTION_LEDGER.md#L10287-L10303 |

## Cosa NON dice

- Tesi del proprietario: "QUANTO si muove il mercato è prevedibile... QUANDO si muove è noto... DOVE va (il verso) NON è prevedibile intraday con nessuno strumento provato".
- Nota fissa nel pannello e nel JSON: "frequenze descrittive su dati già visti, non segnali"
- "Nessuna di queste frequenze crea un edge"
- con 40-50 casi circa ±14 punti percentuali.

## Prove

- runtime/proofs/freqsito1/
- runtime/proofs/freqsito1/locale-step2-nessun-dato.jpg
- runtime/proofs/freqsito1/locale-step3-dati-pubblicati.jpg
- runtime/proofs/freqsito1/locale-step5-backend-giu.jpg
