// The two live channels as the backend serves them (GET /live/scenari, /live/frequenze): {ricevuto, eta_s, dati}.
// `dati` is the engine's JSON after its own cleaning (pubblicabile); the shapes below are the fields the site reads.
import type { Frequenza, Quartili } from '@/lib/fmt'
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

const oggetto = (x: unknown): x is Record<string, unknown> => typeof x === 'object' && x !== null && !Array.isArray(x)

function fallisci(dove: string): never {
  throw new Error(`risposta del motore non valida: ${dove}`)
}

/** The envelope and the instruments' skeleton; per instrument either {errore} or `campi` arrays/objects present. */
function valida<T>(x: unknown, campi: Record<string, 'lista' | 'oggetto'>): Busta<T> {
  if (!oggetto(x) || !('dati' in x) || !('eta_s' in x) || !('ricevuto' in x)) fallisci('busta')
  if (x.eta_s != null && typeof x.eta_s !== 'number') fallisci('eta_s')
  if (x.dati == null) return { ricevuto: (x.ricevuto as string) ?? null, eta_s: (x.eta_s as number) ?? null, dati: null }
  const d = x.dati
  if (!oggetto(d) || !oggetto(d.strumenti)) fallisci('strumenti')
  for (const [s, r] of Object.entries(d.strumenti)) {
    if (haErrore(r)) continue
    if (!oggetto(r)) fallisci(s)
    for (const [c, tipo] of Object.entries(campi))
      if (tipo === 'lista' ? !Array.isArray(r[c]) : !oggetto(r[c])) fallisci(`${s}.${c}`)
  }
  return x as unknown as Busta<T>
}

export function validaScenari(x: unknown): Busta<Scenari> {
  const v = valida<Scenari>(x, { radice: 'oggetto', rami: 'lista', livelli: 'lista' })
  if (v.dati && !oggetto(v.dati.barre)) v.dati.barre = {}
  return v
}

export function validaFrequenze(x: unknown): Busta<Frequenze> {
  const v = valida<Frequenze>(x, { stato: 'oggetto', finestre: 'lista', livelli: 'lista' })
  if (v.dati && !Array.isArray(v.dati.limiti)) v.dati.limiti = []
  return v
}
