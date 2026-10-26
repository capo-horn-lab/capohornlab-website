# Metodo

Questa pagina descrive come sono condotte le ricerche pubblicate sul sito. Ogni regola e' scritta dal progetto prima di eseguire gli script e cita il file e la riga da cui e' presa. `docs/EXECUTION_LEDGER.md` e' il registro di esecuzione del motore; `docs/research/TEORIA_MOVIMENTO_2026-10-21.txt` e' il documento del proprietario sulla tesi del movimento.

## La rubrica viene prima dei risultati

Per ogni ricerca soglie, test e verdetti sono scritti nel registro prima di lanciare lo script: «Rubrica congelata PRIMA dei risultati» (`docs/EXECUTION_LEDGER.md` riga 6101, ripetuta alle righe 6541, 6588, 6625) e, per LAB-2, «rubrica congelata PRIMA di qualsiasi backtest» (riga 6177). La regola comune del progetto e' che «il verificatore applica la rubrica fissata prima dei risultati» (`AGENTS.md` riga 14).

## Scoperta e verifica

I dati di ogni strumento sono divisi in ordine di tempo: scoperta = primo 60% delle sessioni, verifica = ultimo 40% (`docs/EXECUTION_LEDGER.md` righe 6106-6107). Le regole si scelgono sulla scoperta e si giudicano sulla verifica.

## Quando una regola e' adottata

Una strategia e' ADOTTATA solo se valgono tutte queste condizioni; altrimenti e' NON ADOTTATA (`docs/EXECUTION_LEDGER.md` righe 6108-6111):

- almeno 50 trade in scoperta e 30 in verifica;
- media netta maggiore di zero in scoperta e in verifica;
- t almeno 2,0 in verifica;
- in verifica la media supera il 95% di 200 placebo (stesso numero di trade, stessi lati, stesse mezz'ore, entrate a caso);
- correzione di Benjamini-Hochberg con q non oltre 0,10 su tutti i test di verifica.

Il metodo di LAB-2 aggiunge: regole prese dal claim e mai ottimizzate, conteggio di ogni test fatto, fuori campione cronologico, placebo, correzione per test multipli, costi realistici e controllo di lookahead (`docs/EXECUTION_LEDGER.md` righe 6179-6182).

## Esito dell'esecuzione: PASS, FAIL, BLOCKED_ENV, NOT_RUN

Ogni consegna distingue quattro esiti di esecuzione (`AGENTS.md` riga 14). Due regole del progetto ne fissano il confine: uno strumento assente e' `BLOCKED_ENV`, «mai un PASS né una failure del codice» (`docs/ERROR_RULES.md` riga 2317); un output che non contiene né un difetto né la negazione esplicita di difetti si registra come `NOT_RUN`, «mai come assenza di difetti» (`docs/ERROR_RULES.md` righe 2579-2581). L'esito di esecuzione non e' il verdetto della ricerca: uno script puo' essere PASS e il verdetto NON CONFERMATA.

## Verdetto della ricerca

Il registro usa CONFERMATA, PARZIALE, NON CONFERMATA e DESCRITTIVO. Per una famiglia di simboli: CONFERMATA se almeno meta' dei simboli e' confermata, PARZIALE se almeno uno, NON CONFERMATA se nessuno (`docs/EXECUTION_LEDGER.md` riga 9406). DESCRITTIVO vale quando la scheda riporta misure e frequenze senza un test di ipotesi: per FREQ-LIVE-1 il registro dichiara «frequenze descrittive su sessioni gia' viste, nessun placebo ne' correzione per prove multiple» (`docs/EXECUTION_LEDGER.md` riga 10292). Le etichette dell'elenco delle ricerche sono una guida alla lettura: il testo esatto del verdetto e' nella pagina di ogni ricerca.

## Ritiri e correzioni

Quando un controllo successivo smentisce una conferma, la pagina lo dice. Due conferme (VOLREV-1 e GEX-1) sono state ritirate dall'audit: «CONFERMA RITIRATA» e ora NON CONFERMATO (`docs/EXECUTION_LEDGER.md` righe 8968-8970). Le pagine con ritiri o correzioni portano il verdetto `ritirato` o `corretto` e le parole dell'audit in evidenza.

## La tesi: quanto e quando, non dove

Il documento del proprietario sintetizza il risultato di fondo (`docs/research/TEORIA_MOVIMENTO_2026-10-21.txt` righe 5-12):

- QUANTO si muove il mercato e' prevedibile, e la previsione e' confermata su dati mai usati;
- QUANDO si muove e' noto: il movimento si concentra in finestre fisse della giornata;
- DOVE va (il verso) non e' prevedibile intraday con nessuno strumento provato;
- l'unico verso provato e' da chiusura a chiusura: la mean reversion di breve (regola IBS) sugli indici USA.

## Cosa sono le frequenze pubblicate

Le sezioni descrittive del documento riguardano tutto il periodo o le ultime 60-250 sessioni, quindi dati gia' visti: «nessuna e' una regola confermata con rubrica, placebo e correzione per prove multiple». E ancora: «Nessuna di queste frequenze crea un edge» (`docs/research/TEORIA_MOVIMENTO_2026-10-21.txt` righe 73-80). Per questo ogni pagina del sito porta la nota fissa: frequenze descrittive su dati gia' visti, non segnali.

## Come si leggono i numeri

Ogni numero delle tabelle «Esito» e' copiato dal registro o dal file di prova indicato nella colonna Fonte, senza arrotondamenti ne' conversioni. Un numero che non si ritrova nelle fonti citate non entra in tabella ed e' elencato come non verificabile. Se un file di prova citato non e' sul disco, la pagina dice «prova non trovata su disco». I costi di transazione usati nelle prove sono provvisori, come dichiarato nelle singole schede.
