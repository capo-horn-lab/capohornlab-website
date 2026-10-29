// Testo della pagina /memoria che non viene dal motore: le definizioni delle famiglie e la frase dei tempi, COPIATE alla lettera
// da docs/EXECUTION_LEDGER.md del repo del motore (numeri di riga = quelli del registro al 29/10/2026), ciascuna con la sua Fonte;
// la liquidita' cita anche la docstring di src/trading_stack/memoria_mercato.py (righe 71-81), che e' la definizione in vigore.
// Niente riformulazioni: se il registro cambia si ricopia. Una definizione non trovata nel registro si scrive come tale, non si inventa.

export interface Citazione {
  testo: string
  fonte: string
  /** Che cosa e' la citazione, quando non e' la definizione in vigore (es. la registrazione fatta prima del codice). */
  etichetta?: string
}

export interface Famiglia {
  id: string
  titolo: string
  definizioni: Citazione[]
  /** Una riga di fatti verificabili fra le citazioni (es. due fonti che riportano valori diversi). */
  nota?: string
}

/** Il database della memoria conta gli eventi da questa data (design MEMORIA-SITO-1, §4.3). */
export const DATA_INIZIO_DATABASE = '19/10/2026'

export const FAMIGLIE: Famiglia[] = [
  {
    id: 'assorbimento',
    titolo: 'Assorbimento',
    definizioni: [
      {
        testo:
          "Definizione dichiarata: finestra 30 s valutata ogni 5 s, volume aggressivo >= 3x la mediana delle 10 finestre precedenti (ciascuna con almeno uno scambio) e >= 50 contratti, movimento <= 4 tick contro l'aggressore fra gli estremi della finestra; episodi (pausa <= 60 s, durata <= 300 s) contati una volta; riscaldamento azzerato dopo 30 s di silenzio, esito None con un buco > 60 s dentro l'orizzonte; esiti a 30/120/600 s (MFE/MAE/ritorno in tick); kNN solo su eventi finiti prima dell'istante, standardizzazione sul solo pool; margine max(1,96 sqrt(p(1-p)/n), 3/n) limitato a 1; scoperta/verifica per data; file vivo rifiutato senza intervallo <= 200 MB.",
        fonte: 'docs/EXECUTION_LEDGER.md#L10998',
      },
    ],
  },
  {
    id: 'liquidita',
    titolo: 'Liquidità: muro e ritiro',
    definizioni: [
      // copiate dalla docstring di memoria_mercato.py (righe 71-79 e 80-81), a-capo ridotti a uno spazio
      {
        testo: `FAMIGLIA "liquidita'" (famiglia = 'liquidita', tipo = 'ritiro' | 'muro'; lato = 'bid' | 'ask' = lato del book): "ritiro": la profondita' entro N_LIVELLI di un lato cala di almeno RITIRO_PCT (50%) A PARITA' DI PREZZO (stessi prezzi, visibili sia a t_rif sia ora: lo spostamento del prezzo non e' un ritiro; candidato annullato se il miglior prezzo del lato e' migliorato; alla conferma la profondita' deve essere ancora <= (1-RITIRO_PCT) x massimo) rispetto al suo massimo negli ultimi RITIRO_FINESTRA_S (10 s; massimo >= RITIRO_MIN_DEPTH = 50 contratti), mentre il volume scambiato su quel lato fra quel massimo e la conferma e' < RITIRO_FRAZ_SCAMBI (25%) della quantita' sparita. Lato scambiato: sul bid contano le vendite aggressive, sull'ask gli acquisti, e gli scambi di verso ignoto (prudenza: nel dubbio e' consumo, non ritiro). Il consumo per scambi NON e' un ritiro. CONFERMA ritardata di RITIRO_ATTESA_S (1 s): uno scambio puo' arrivare dopo l'L2 che lo riflette; l'evento ha l'istante della conferma. Verso favorevole: ritiro del bid = GIU', ritiro dell'ask = SU.`,
        fonte: 'src/trading_stack/memoria_mercato.py#L71-L79',
      },
      {
        testo: `"muro": un livello fra le prime N_LIVELLI con size >= MURO_K (5) volte la mediana delle size di quei livelli e >= MURO_MIN_SIZE (25), che persiste >= MURO_T_S (10 s); l'evento ha l'istante del primo record dopo T.`,
        fonte: 'src/trading_stack/memoria_mercato.py#L80-L81',
      },
      {
        etichetta: 'registrazione prima del codice',
        testo:
          'nuova famiglia "liquidita\'" con due tipi dichiarati: "ritiro" (la profondita\' entro N livelli di un lato cala di almeno X% in W s con volume scambiato su quel lato inferiore a una frazione dichiarata della quantita\' sparita) e "muro" (un livello con quantita\' >= K volte la mediana dei livelli visibili per almeno T s; esito del muro: toccato, ritirato prima del tocco, consumato); esiti agli stessi orizzonti con le stesse regole di buchi ed episodi',
        fonte: 'docs/EXECUTION_LEDGER.md#L11002',
      },
      {
        testo: 'Ricalibrazioni dichiarate dopo i dati veri: MURO_MIN_SIZE 25, N_CALDO 5, isteresi del muro.',
        fonte: 'docs/EXECUTION_LEDGER.md#L11009',
      },
    ],
    // docstring (riga 81) e ricalibrazione registrata (L11009) concordano su MURO_MIN_SIZE 25 dal 29/10/2026: nessuna nota
  },
  {
    id: 'order-flow',
    titolo: 'Order flow: flusso con esito e senza esito',
    definizioni: [
      {
        testo:
          'OFI alla Cont-Kukanov-Stoikov sul miglior livello L1 (variazioni di bid/ask e quantita\' con i cambi di prezzo come nel lavoro originale), finestra 10 s valutata ogni 2 s; soglia causale: |OFI| >= quantile 97 della distribuzione delle finestre precedenti della stessa sessione (riscaldamento minimo dichiarato); due tipi: "flusso_senza_esito" (prezzo medio mosso < 2 tick nella finestra) e "flusso_con_esito" (>= 8 tick); lato = segno di OFI; esiti agli stessi orizzonti e regole (buchi, episodi); bid/ask nel record Last usati quando presenti. Parametri fissati qui prima dei dati.',
        fonte: 'docs/EXECUTION_LEDGER.md#L11031',
      },
      {
        testo:
          'famiglia order flow (OFI Cont-Kukanov-Stoikov sul miglior livello, finestra 10 s ogni 2 s, soglia al 97o percentile causale della sessione dopo 300 valutazioni, tipi flusso_senza_esito < 2 tick e flusso_con_esito >= 8 tick).',
        fonte: 'docs/EXECUTION_LEDGER.md#L11037',
      },
    ],
  },
]

/** La riga del registro sui tempi della verifica ("Prossimi passi (revisione)", sezione «28/10 — installazione esportatore»). */
export const QUANDO: Citazione = {
  testo:
    "una sessione di verifica per giorno di borsa; 8 sessioni = 30/10 (NON CONFERMATO possibile, CONFERMATO solo in teoria: servono 12 test al minimo), 10 = 3/11, 12 = 5/11 (anche un test isolato).",
  fonte: 'docs/EXECUTION_LEDGER.md#L11051',
}
