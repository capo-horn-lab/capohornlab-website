// The two live channels as the backend serves them (GET /live/scenari, /live/frequenze): {ricevuto, eta_s, dati}.
// `dati` is the engine's JSON after its own cleaning (pubblicabile); the shapes below are the fields the site reads.
import { finito, type Frequenza, type Quartili } from '@/lib/fmt'
import type { Radice, Ramo } from '@/lib/albero'

export interface Busta<T> {
  ricevuto: string | null
  eta_s: number | null
  dati: T | null
}

export interface StrumentoErrore {
  contratto?: string | null
  errore: string
}

export interface Principale {
  strumento: string
  contratto: string | null
  timeframe?: number | null
  ultima_barra?: string | null
  fresco?: boolean
  tick?: number
  valore_punto?: number
}

export interface Orari {
  giorno: string
  apertura: string
  chiusura: string
  fuso: string
}

/** [t_close (UTC s), open, high, low, close, volume] */
export type Riga = [number, number, number, number, number, number]

export interface Barre {
  tf: number
  fuso: string
  righe: Riga[]
  viva: Riga | null
}

export interface EscursioneResidua {
  finestra: string
  fatta: number | null
  resta: Quartili | null
  n?: number
  criterio?: string
}

export interface DaQui {
  radice: Radice & { soglia?: number | null }
  rami: Ramo[]
}

export interface StrumentoScenari {
  contratto: string
  prezzo: number | null
  A: number | null
  cadenza: string
  eta_min: number | null
  apertura_prezzo: number | null
  radice: Radice
  rami: Ramo[]
  livelli: { nome: string; prezzo: number; p_1530: number | null; p_2200: number | null; n: number }[]
  da_qui?: DaQui | null
  escursione_residua?: EscursioneResidua | null
}

export interface Scenari {
  generato: string
  ora_roma: string
  nota?: string
  principale: Principale
  orari: Orari
  strumenti: Record<string, StrumentoScenari | StrumentoErrore>
  barre: Record<string, Barre>
}

export interface Livello {
  nome: string
  prezzo: number
  distanza: number
  distanza_A: number
  lato: string
  fascia: string | null
  entro_1530: Frequenza | null
  entro_2200: Frequenza | null
}

export interface Finestra {
  finestra: string
  nome: string
  corrente: boolean
  n: number
  escursione: Quartili | null
  netto: Quartili | null
  oggi: number | null
}

export interface Percorso {
  apertura?: number
  barre: number
  direzione: string | null
  t1: number
  ritorno: number | null
  estensione: number
  opposto: number | null
  estensione2: number
  ritorno2: number | null
  chiusura: number
}

export interface RigaLente {
  lente: string
  tipo?: string
  stato?: string | null
  valore?: string | null
  n: number
  chiusura_sopra?: Frequenza | null
  nuovo_minimo?: Frequenza | null
  nuovo_massimo?: Frequenza | null
  arrivo_sopra?: Frequenza | null
  arrivo_sotto?: Frequenza | null
  estensione_sopra_A?: Quartili | null
  estensione_sotto_A?: Quartili | null
  pende?: Record<string, string>
}

export interface StrumentoFrequenze {
  contratto: string
  cadenza: string
  eta_min: number | null
  A: number | null
  A_sessioni: number | null
  soglia: number | null
  passo_tondo: number | null
  n_storiche: number | null
  barre_oggi: Record<string, number> | number | null
  stato: Record<string, number | string | null>
  finestre: Finestra[]
  livelli: Livello[]
  apertura: {
    soglia: number | null
    fase: string | null
    minuti: number | null
    barre?: string
    percorso: Percorso | null
    storico: { n: number | null; n_totale: number | null; riferimento: string | null; frequenze: Record<string, Frequenza | Quartili | null> | null } | null
  } | null
  lenti?: {
    riferimento?: Record<string, unknown>
    campione?: { n?: number }
    base?: RigaLente | null
    righe?: RigaLente[]
    concordanza?: { frase?: string } | null
  } | null
}

export interface Frequenze {
  generato: string
  ora_roma: string
  principale: Principale
  orari?: Orari
  strumenti: Record<string, StrumentoFrequenze | StrumentoErrore>
  limiti: string[]
}

export const haErrore = (r: unknown): r is StrumentoErrore => typeof (r as StrumentoErrore | null)?.errore === 'string'

type Rec = Record<string, unknown>
const oggetto = (x: unknown): x is Rec => typeof x === 'object' && x !== null && !Array.isArray(x)

function fallisci(dove: string): never {
  throw new Error(`risposta del motore non valida: ${dove}`)
}

/** An instrument that cannot be shown becomes an error record of that instrument only, never of the page. */
const rotto = (r: Rec, campo: string): StrumentoErrore => ({ contratto: typeof r.contratto === 'string' ? r.contratto : null, errore: `dati non validi dal motore (${campo})` })

const radiceOk = (x: unknown): x is Rec => oggetto(x) && typeof x.t === 'string' && finito(x.prezzo)
const minutiOk = (m: unknown) => m == null || (oggetto(m) && finito(m.mediana) && finito(m.q1) && finito(m.q3))
const ramoOk = (r: unknown): r is Rec =>
  oggetto(r) && typeof r.id === 'string' && typeof r.etichetta === 'string' && finito(r.prezzo) && finito(r.p) && finito(r.k) && finito(r.n) && minutiOk(r.minuti)
const rigaOk = (r: unknown): r is Riga => Array.isArray(r) && r.length === 6 && r.every(finito)

/**
 * The envelope (an error of the whole channel: TanStack keeps the last good data) and, per instrument, either {errore} or what
 * `strumento` keeps of it (or an error record of that instrument when something it needs is missing).
 */
function valida<T>(x: unknown, strumento: (r: Rec) => Rec | StrumentoErrore): Busta<T> {
  if (!oggetto(x) || !('dati' in x) || !('eta_s' in x) || !('ricevuto' in x)) fallisci('busta')
  if (x.eta_s != null && !finito(x.eta_s)) fallisci('eta_s')
  if (x.dati == null) return { ricevuto: (x.ricevuto as string) ?? null, eta_s: (x.eta_s as number) ?? null, dati: null }
  const d = x.dati
  if (!oggetto(d) || !oggetto(d.strumenti)) fallisci('strumenti')
  if (!oggetto(d.principale) || typeof d.principale.strumento !== 'string') fallisci('principale')
  if (typeof d.generato !== 'string') fallisci('generato')
  for (const [s, r] of Object.entries(d.strumenti)) {
    if (haErrore(r)) continue
    d.strumenti[s] = oggetto(r) ? strumento(r) : { contratto: null, errore: 'dati non validi dal motore' }
  }
  if (!oggetto(d.orari) || typeof d.orari.apertura !== 'string' || typeof d.orari.chiusura !== 'string') delete d.orari
  return x as unknown as Busta<T>
}

export function validaScenari(x: unknown): Busta<Scenari> {
  const v = valida<Scenari>(x, (r) => {
    if (!radiceOk(r.radice)) return rotto(r, 'radice')
    if (!Array.isArray(r.rami)) return rotto(r, 'rami')
    if (!Array.isArray(r.livelli)) return rotto(r, 'livelli')
    const dq = r.da_qui
    return {
      ...r, prezzo: finito(r.prezzo) ? r.prezzo : null, rami: r.rami.filter(ramoOk), livelli: r.livelli.filter((l) => oggetto(l) && finito(l.prezzo)),
      da_qui: oggetto(dq) && radiceOk(dq.radice) && Array.isArray(dq.rami) ? { ...dq, rami: dq.rami.filter(ramoOk) } : null,
    }
  })
  if (v.dati) {
    const barre: Record<string, Barre> = {}
    for (const [s, b] of Object.entries(oggetto(v.dati.barre) ? v.dati.barre : {}))
      if (oggetto(b) && Array.isArray(b.righe)) barre[s] = { ...(b as unknown as Barre), righe: b.righe.filter(rigaOk), viva: rigaOk(b.viva) ? b.viva : null }
    v.dati.barre = barre
  }
  return v
}

const frequenzaOk = (f: unknown) => (oggetto(f) ? { ...f, p: finito(f.p) ? f.p : null } : null)
const o = (x: unknown): Rec | null => (oggetto(x) ? x : null)

/** Today's opening path as the panel reads it: a direction (a word, or null before the first move) and, with one, a minute. */
const percorsoOk = (p: unknown) => (oggetto(p) && (p.direzione === null || (typeof p.direzione === 'string' && finito(p.t1))) ? p : null)

function aperturaOk(a: unknown) {
  if (!oggetto(a)) return null
  const h = o(a.storico)
  const fr = h && oggetto(h.frequenze) ? Object.fromEntries(Object.entries(h.frequenze).map(([k, f]) => [k, o(f)])) : null
  return { ...a, percorso: percorsoOk(a.percorso), storico: h && { ...h, frequenze: fr } }
}

function lentiOk(l: unknown) {
  if (!oggetto(l)) return null
  return { ...l, riferimento: o(l.riferimento) ?? {}, campione: o(l.campione), base: o(l.base), righe: Array.isArray(l.righe) ? l.righe.filter(oggetto) : [],
    concordanza: o(l.concordanza) }
}

export function validaFrequenze(x: unknown): Busta<Frequenze> {
  const v = valida<Frequenze>(x, (r) => {
    if (!oggetto(r.stato)) return rotto(r, 'stato')
    if (!Array.isArray(r.finestre)) return rotto(r, 'finestre')
    if (!Array.isArray(r.livelli)) return rotto(r, 'livelli')
    return {
      ...r, finestre: r.finestre.filter((w) => oggetto(w) && typeof w.finestra === 'string'),
      livelli: r.livelli.filter((l): l is Rec => oggetto(l) && finito(l.prezzo))
        .map((l) => ({ ...l, entro_1530: frequenzaOk(l.entro_1530), entro_2200: frequenzaOk(l.entro_2200) })),
      apertura: aperturaOk(r.apertura), lenti: lentiOk(r.lenti),
    }
  })
  if (v.dati && !Array.isArray(v.dati.limiti)) v.dati.limiti = []
  return v
}
