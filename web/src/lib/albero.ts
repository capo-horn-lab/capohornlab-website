// The scenario tree's geometry and texts: the rules of the NinjaTrader indicator (TradingAgentScenari.cs) as the fase 2
// contract fixed them (D8: branches without `minuti` are outcomes, never on the chart), and the Trader's texts
// (desktop_trader.nome_breve / esito_ramo / scelti_da_qui / residua / riferimento_albero).
import { type Frequenza, intero, p as pct, estremo } from '@/lib/fmt'

export interface Radice {
  ora: string
  t: string
  prezzo: number
  /** absent on da_qui's root */
  fase?: string
  percorso?: string
  omessi?: number
}

export interface Ramo extends Frequenza {
  id: string
  padre: string | null
  tipo: string
  etichetta: string
  prezzo: number | null
  orizzonte?: string
  minuti: { mediana: number; q1: number; q3: number } | null
  tocco?: boolean
  omessi?: number
}

export interface Punto {
  t: number
  prezzo: number
}

export interface Segmento {
  id: string
  ramo: Ramo
  da: Punto
  a: Punto
  q1: { t: number }
  q3: { t: number }
  p: number
  k: number
  n: number
  margine: number | null
  etichetta: string
  padre: string | null
  classe: 1 | 2 | 3
}

export interface Geometria {
  segmenti: Segmento[]
  esiti: Ramo[]
  testo: Ramo[]
  radiceT: number | null
}

export interface Opzioni {
  massimoMinuti?: number
  padriConFigli?: number
}

const classe = (p: number): 1 | 2 | 3 => (p < 0.33 ? 1 : p < 0.66 ? 2 : 3)

/** Epoch seconds of an ISO time with offset ("2026-10-26T20:08+01:00"), null if unreadable. */
export function secondi(iso: string | null | undefined): number | null {
  const ms = iso ? Date.parse(iso) : NaN
  return Number.isFinite(ms) ? ms / 1000 : null
}

/** A branch realized by touching its price (the Trader's `tocca`, DAQUI-1 `tocco`); one without minutes is never touched. */
export const tocca = (r: Ramo): boolean => r.tocco !== false && r.minuti != null

/**
 * The outcomes are the Trader's esiti() (D8): first-level branches without a touch and every descendant of a listed branch;
 * a child without a touch of a touched branch is neither listed nor drawn (it comes when the engine's bridge promotes it).
 * The touched ones: head at radiceT + minuti.mediana (minutes from the ROOT, children too), a child at least 1 min after its
 * parent's head; q1/q3 likewise, a child's never before its parent's head; beyond `massimoMinuti` (median, or a child's head
 * pushed past it) -> testo; children drawn only for the `padriConFigli` most probable drawn parents, any other child (a
 * child of a branch in testo, deeper levels) -> testo.
 */
export function geometria(radice: Radice | null | undefined, rami: Ramo[] | null | undefined, opzioni: Opzioni = {}): Geometria {
  const { massimoMinuti = 180, padriConFigli = 2 } = opzioni
  const radiceT = secondi(radice?.t)
  const out: Geometria = { segmenti: [], esiti: [], testo: [], radiceT }
  if (!radice || radiceT == null || !rami) return out
  const validi = rami.filter((r) => r && r.prezzo != null && r.p != null)
  const capi = new Map<string, Segmento>()
  const segmento = (r: Ramo, da: Punto, capoPadre: number | null): Segmento => {
    const m = r.minuti!
    const t = (x: number, dopo: number) => (capoPadre == null ? radiceT + x * 60 : Math.max(radiceT + x * 60, capoPadre + dopo))
    return {
      id: r.id, ramo: r, da, a: { t: t(m.mediana, 60), prezzo: r.prezzo! }, q1: { t: t(m.q1, 0) }, q3: { t: t(m.q3, 0) },
      p: r.p!, k: r.k, n: r.n, margine: r.margine ?? null, etichetta: etichetta(r), padre: r.padre, classe: classe(r.p!),
    }
  }
  const limite = radiceT + massimoMinuti * 60
  const padri = validi.filter((r) => r.padre == null && tocca(r) && r.minuti!.mediana <= massimoMinuti)
  const conFigli = new Set([...padri].sort((a, b) => b.p! - a.p!).slice(0, padriConFigli).map((r) => r.id))
  for (const r of padri) capi.set(r.id, segmento(r, { t: radiceT, prezzo: radice.prezzo }, null))
  const elencati = new Set<string>()
  for (const r of validi) {
    if ((r.padre == null && !tocca(r)) || (r.padre != null && elencati.has(r.padre))) {
      out.esiti.push(r)
      elencati.add(r.id)
    } else if (!tocca(r)) continue
    else if (r.padre == null) {
      if (capi.has(r.id)) out.segmenti.push(capi.get(r.id)!)
      else out.testo.push(r)
    } else {
      const padre = capi.get(r.padre)
      const s = padre && conFigli.has(r.padre) ? segmento(r, padre.a, padre.a.t) : null
      if (s && s.a.t <= limite) out.segmenti.push(s)
      else out.testo.push(r)
    }
  }
  return out
}

/** The `da_qui` branches to draw (Trader scelti_da_qui): at most `primi` first-level by p, `figli` children each by p. */
export function sceltiDaQui(rami: Ramo[] | null | undefined, primi = 3, figli = 2): Ramo[] {
  const ok = (rami ?? []).filter((r) => r && r.prezzo != null && r.p != null)
  const perP = (a: Ramo, b: Ramo) => b.p! - a.p!
  return ok.filter((r) => r.padre == null).sort(perP).slice(0, primi)
    .flatMap((r) => [r, ...ok.filter((x) => x.padre === r.id).sort(perP).slice(0, figli)])
}

/** The tree goes to text when its root is more than 2 h after the last bar (the indicator's rule). */
export const alberoInTesto = (radiceT: number, ultimaBarraT: number): boolean => radiceT > ultimaBarraT + 7200

export const snap5 = (t: number): number => Math.round(t / 300) * 300

// desktop_trader.BREVI (Python re.sub replaces every match: the JS patterns carry `g`)
const BREVI: [RegExp, string][] = [
  [/^primo movimento di (\d+) (su|giu)( da qui)?/g, '$1 $2'], [/ entro (\d+) min dal primo movimento/g, " $1'"],
  [/^ritorno all.apertura mai.*/g, 'mai ritorno'], [/^ritorno al punto mai.*/g, 'mai ritorno al punto'],
  [/ piu. tardi, entro le \d\d:\d\d/g, " piu' tardi"], [/ entro le \d\d:\d\d/g, ''], [/ entro (\d+) min$/g, " $1'"],
  [/^estensione a ([+-]\d+)\.\d+ \((q1|mediana|q3)\) prima del ritorno/g, 'estensione $1'], [/^chiusura (sopra|sotto).*/g, 'chiude $1'],
  [/^nessun movimento di (\d+)/g, 'nessun $1'], [/ \(pochi casi\)/g, ''],
]
const POCHI = ' (pochi casi)'

export const nomeBreve = (e: string | null | undefined): string => BREVI.reduce((s, [a, b]) => s.replace(a, b), String(e ?? '')).trim()

/** The label at a branch's head: "<short name> p (k/n ±m)", D8. */
export const etichetta = (r: Pick<Ramo, 'etichetta' | 'p' | 'k' | 'n' | 'margine'>): string => `${nomeBreve(r.etichetta)} ${pct(r)}`

const AL: Record<string, string> = { "l'apertura": "all'apertura", 'il punto': 'al punto', 'il prezzo attuale': 'al prezzo attuale' }
const DA: Record<string, string> = { "l'apertura": "dall'apertura", 'il punto': 'dal punto', 'il prezzo attuale': 'dal prezzo attuale' }

/**
 * A branch without minutes as an outcome at the session's end (Trader esito_ramo), its reference and its median said, never a
 * level to touch. The frequency is D8 (with ±m when the engine gives it); "pochi casi" -> "k su n, pochi casi".
 */
export function esitoTesto(r: Pick<Ramo, 'etichetta' | 'prezzo' | 'p' | 'k' | 'n' | 'margine' | 'orizzonte'>, rif: number | null, rifNome: string,
  S?: number | null, segno?: number | null, ora = '22:00'): string {
  const pochi = r.etichetta.includes(POCHI)
  const e = r.etichetta.replace(POCHI, '')
  const fino = r.orizzonte || ora
  let testo = e
  let coda = ''
  const m = /^chiusura (sopra|sotto)/.exec(e)
  if (m && rif != null) {
    testo = `chiusura ${m[1]} ${rifNome} ${intero(rif)}`
    coda = r.prezzo == null ? '' : ` · mediana ${intero(r.prezzo)}`
  } else if (e.includes(' mai ') && rif != null) {
    const al = AL[rifNome] ?? rifNome
    const nome = e.split(' mai ')[0].replace("all'apertura", al).replace('al punto', al)
    testo = `mai ${nome} ${intero(rif)} entro ${fino}`
    coda = r.prezzo == null ? '' : ` · mediana dell'estensione ${intero(r.prezzo)}`
  } else if (/^nessun \S+ opposto/.test(e) && rif != null && S && segno) {
    testo = `nessun ${S} ${segno > 0 ? 'sotto' : 'sopra'} ${rifNome} (${intero(rif - segno * S)}) entro ${fino}`
  } else if (e.startsWith('nessun movimento') && rif != null && S) {
    testo = `nessun movimento di ${S} ${DA[rifNome] ?? `da ${rifNome}`} ${intero(rif)} (${intero(rif - S)}-${intero(rif + S)}) entro ${fino}`
  }
  const freq = pochi || estremo(r) ? `${r.k} su ${r.n}` : pct(r)
  return `${testo}: ${freq}${pochi ? ', pochi casi' : ''}${coda}`
}

/** D8 reference of the opening tree's closes and 'nessun' branches (Trader riferimento_albero): the open, or the root's price
 * in the phases conditioned on nothing (closed, before the open, no bar at the open). */
export function riferimento(r: { radice: Radice; apertura_prezzo: number | null }): [number | null, string] {
  const f = String(r.radice?.fase ?? '')
  const libera = f === 'chiusa' || f.startsWith('prima delle') || f.startsWith('senza barra') || r.apertura_prezzo == null
  return libera ? [r.radice?.prezzo ?? null, 'il prezzo attuale'] : [r.apertura_prezzo, "l'apertura"]
}

/** +1 / -1 from the root's path ("primo 50 giu alle ..."), null without a first move (Trader). */
export function segnoPrimo(percorso: string | null | undefined): number | null {
  const m = /primo \S+ (su|giu)/.exec(String(percorso ?? ''))
  return m ? (m[1] === 'su' ? 1 : -1) : null
}

/** DAQUI-1's escursione_residua in words (Trader residua), '' when absent. */
export function residua(er: { finestra: string; fatta: number | null; resta: { mediana: number; q1: number; q3: number } | null; n?: number; criterio?: string } | null | undefined): string {
  if (!er || er.fatta == null || !er.resta || er.resta.mediana == null) return ''
  const rs = er.resta
  return `escursione della finestra ${er.finestra}: fatta ${intero(er.fatta)} + resta ${intero(rs.mediana)} (${intero(rs.q1)}-${intero(rs.q3)}, n ${er.n}) punti; ${er.criterio || '-'}`
}
