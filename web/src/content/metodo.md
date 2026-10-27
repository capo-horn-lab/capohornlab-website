# Metodo

Questa pagina descrive come sono condotte le ricerche pubblicate sul sito. Ogni regola riportata cita il file e la riga da cui e' presa. `docs/EXECUTION_LEDGER.md` e' il registro di esecuzione del motore; `docs/research/TEORIA_MOVIMENTO_2026-10-21.txt` e' il documento del proprietario sulla tesi del movimento.

## La rubrica prima dei risultati, dove la scheda lo dice

Dove la scheda del registro lo dice, la rubrica (soglie, test e verdetti) e' fissata prima dei risultati: «Rubrica congelata PRIMA dei risultati» (`docs/EXECUTION_LEDGER.md` riga 6101, ripetuta alle righe 6541, 6588, 6625) e, per LAB-2, «rubrica congelata PRIMA di qualsiasi backtest» (riga 6177). Non vale per ogni scheda: la sezione «Metodo e rubrica» di ogni pagina riporta se la rubrica era fissata prima. La regola comune del progetto e' che «il verificatore applica la rubrica fissata prima dei risultati» (`AGENTS.md` riga 14).

## Scoperta e verifica nel laboratorio LAB-1

Nel laboratorio LAB-1 i dati di ogni strumento sono divisi in ordine di tempo: scoperta = primo 60% delle sessioni, verifica = ultimo 40% (`docs/EXECUTION_LEDGER.md` righe 6106-6107); la stessa divisione e' scritta per LAB-2 (riga 6199). Il giudizio sulla regola (media, t, placebo, correzione per test multipli) si fa sulla verifica.

## Quando una strategia e' adottata nel laboratorio LAB-1

Una strategia e' ADOTTATA solo se valgono tutte queste condizioni; altrimenti e' NON ADOTTATA (`docs/EXECUTION_LEDGER.md` righe 6108-6111):

- almeno 50 trade in scoperta e 30 in verifica;
- media netta maggiore di zero in scoperta e in verifica;
- t almeno 2,0 in verifica;
- in verifica la media supera il 95% di 200 placebo (stesso numero di trade, stessi lati, stesse mezz'ore, entrate a caso);
- correzione di Benjamini-Hochberg con q non oltre 0,10 su tutti i test di verifica.

Il metodo di LAB-2 aggiunge: regole prese dal claim e mai ottimizzate, conteggio di ogni test fatto, fuori campione cronologico, placebo, correzione per test multipli, costi realistici e controllo di lookahead (`docs/EXECUTION_LEDGER.md` righe 6179-6182).

## Esito dell'esecuzione: PASS, FAIL, BLOCKED_ENV, NOT_RUN

Ogni consegna distingue quattro esiti di esecuzione (`AGENTS.md` riga 14). Due regole del progetto ne fissano il confine: uno strumento assente e' `BLOCKED_ENV`, «mai un PASS né una failure del codice» (`docs/ERROR_RULES.md` riga 2317); un output che non contiene né un difetto né la negazione esplicita di difetti si registra come `NOT_RUN`, «mai come assenza di difetti» (`docs/ERROR_RULES.md` righe 2579-2581). L'esito di esecuzione non e' il verdetto della ricerca: uno script puo' essere PASS e il verdetto NON CONFERMATA.

## Verdetto nel registro

Nell'elenco e in ogni pagina il verdetto e' una parola scritta nel registro, e solo se sta in una frase di verdetto del registro, nelle righe di `docs/EXECUTION_LEDGER.md` indicate dal locatore principale della scheda (`fonte_ledger`). Le frasi che il registro usa davvero sono «Esito …: PAROLA» (riga 8481: «Esito ENS-1 (…): CONFERMATO»; riga 1653: «Esito: BLOCKED_ENV»), «Esito PAROLA» solo a inizio riga o di punto elenco (riga 9721: «Esito PASS, verdetto NON CONFERMATA»; a meta' riga e' una frase ipotetica, come alla riga 9282), «Verdetto: PAROLA» (riga 9247: «Verdetto: NON CONFERMATA») e «verdetto PAROLA» (riga 9309: «verdetto NON CONFERMATA»); «Outcome: PAROLA» e' ammessa ma il registro non la usa. Altre due forme: «Esito ID (provenienza lunga come si vuole): PAROLA», con i due punti subito dopo la parentesi chiusa (riga 8628: «Esito ALLOC-1 (runtime/proofs/alloc1/alloc1.json; … sessioni, fuori campione dalla 501a): NON CONFERMATO»; riga 9766), e «ID = PAROLA», solo per gli ID della scheda (righe 8968-8969: «VOLREV-1 = NON CONFERMATO»). Dopo un PASS o un FAIL cosi' ancorati, la virgola puo' portare anche il verdetto di ricerca (riga 9863: «PASS, NON CONFERMATA»), mai un conteggio. Le parole sono PASS, FAIL, CONFERMATA, CONFERMATO, CONFERMATI, CONFERMATE, NON CONFERMATA, NON CONFERMATO, PARZIALE, ADOTTATA, ADOTTATI, ADOTTATE, NON ADOTTATA, DESCRITTIVO, RITIRATA, RITIRATO, BLOCKED_ENV, NOT_RUN (dopo NON la parola puo' essere anche in minuscolo).

Non e' un verdetto una parola preceduta da un conteggio («3643 PASS, 0 FAIL», riga 6330), seguita da «se», «quando» o «dopo» (la definizione di una rubrica: «CONFERMATA dopo 60 giorni-segnale se …», riga 9081) o fuori da quelle frasi. Se in quelle righe non c'e' nessuna frase di verdetto in queste forme, la pagina dice «verdetto non estratto: vedi Esito»: il registro puo' scrivere il verdetto in un'altra forma (riga 7277: «Esito H-NEXT-4b (…). CONFERMATA su 2006-2019 per entrambi»), che non si estrae, e il testo e' nella sezione «Esito» della pagina. Nessuna etichetta e' dedotta dal testo, e nel dubbio vale questa. Le parole delle altre righe citate nella tabella (rubriche, esiti di altri studi) non entrano nell'etichetta. Se il locatore contiene piu' frasi di verdetto, ciascuna parola e' elencata una volta, nell'ordine in cui compare (nelle pagine con piu' studi: prima le parole senza ID, poi quelle con l'ID, nell'ordine degli ID della scheda); il testo esatto e' nella sezione «Esito» della pagina. Quando una pagina raccoglie piu' studi e la frase nomina lo studio, l'etichetta porta l'ID («OVN-1: confermati · GOLDN-1: non confermato»); il filtro dell'elenco usa sempre la parola nuda. Una frase che nomina uno studio estraneo alla scheda non conta, e un plurale preceduto da un conteggio («0 CONFERMATE») nemmeno.

Per una famiglia di simboli il registro scrive: CONFERMATA se almeno meta' dei simboli e' confermata, PARZIALE se almeno uno, NON CONFERMATA se nessuno (`docs/EXECUTION_LEDGER.md` riga 9406). Per FREQ-LIVE-1 dichiara «frequenze descrittive su sessioni gia' viste, nessun placebo ne' correzione per prove multiple» (`docs/EXECUTION_LEDGER.md` riga 10292).

## Ritiri e correzioni

Quando un controllo successivo smentisce una conferma, la pagina lo dice. Due conferme (VOLREV-1 e GEX-1) sono state ritirate dall'audit: «CONFERMA RITIRATA» e ora NON CONFERMATO (`docs/EXECUTION_LEDGER.md` righe 8968-8970). Le pagine con voci in quella sezione portano, accanto al verdetto del registro, un secondo segno: `ritirato` solo per gli studi che l'inventario dichiara ritirati (VOLREV-1 e GEX-1), per tutti gli altri la nota neutra «nota dell'audit». Il segno vale solo per gli studi nominati nella sezione «Ritiri e correzioni» della pagina e non cambia il verdetto. Le parole dell'audit sono in evidenza; di una conferma ritirata la pagina non riporta i numeri.

## La tesi: quanto e quando, non dove

Il documento del proprietario sintetizza il risultato di fondo (`docs/research/TEORIA_MOVIMENTO_2026-10-21.txt` righe 5-12):

- QUANTO si muove il mercato e' prevedibile, e la previsione e' confermata su dati mai usati;
- QUANDO si muove e' noto: il movimento si concentra in finestre fisse della giornata;
- DOVE va (il verso) non e' prevedibile intraday con nessuno strumento provato;
- l'unico verso provato e' da chiusura a chiusura: la mean reversion di breve (regola IBS) sugli indici USA.

## Cosa sono le frequenze pubblicate

Le sezioni descrittive del documento riguardano tutto il periodo o le ultime 60-250 sessioni, quindi dati gia' visti: «nessuna e' una regola confermata con rubrica, placebo e correzione per prove multiple». E ancora: «Nessuna di queste frequenze crea un edge» (`docs/research/TEORIA_MOVIMENTO_2026-10-21.txt` righe 73-80). Per questo ogni pagina del sito porta la nota fissa: frequenze descrittive su dati gia' visti, non segnali.

## Come si leggono i numeri

Ogni numero delle tabelle «Esito» e' copiato dal registro o dal file di prova indicato nella colonna Fonte, senza arrotondamenti ne' conversioni. Una riga con un numero che non si ritrova nella fonte citata non e' pubblicata: sotto la tabella la pagina dice quante righe della scheda non sono riportate. I numeri della fonte si leggono come quelli della tabella: un orario («20:47») e' un numero solo e «47» non vi si ritrova dentro, «30/69» sono due numeri, le cifre di un codice o di un numero piu' lungo non contano. La Fonte di una riga e' il punto dove stanno insieme il numero e le parole della riga, non il primo posto in cui compaiono le stesse cifre. Si accetta un numero fuori dall'intervallo citato dal registro solo se sta entro 3 righe e la stessa riga che porta il numero ha anche le parole della riga della tabella; la Fonte indica allora la riga vera. Per un documento citato basta che il numero stia nella stessa sezione o tabella delle parole della riga (fino a 12 righe sotto l'intestazione). In un file di prova JSON un numero conta solo come valore, insieme agli altri numeri della riga nello stesso record. Se un file di prova citato non e' sul disco, la pagina dice «prova non trovata su disco». I costi di transazione usati nelle prove sono provvisori, come dichiarato nelle singole schede.
