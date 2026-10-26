// What one instrument's chart, outcomes box and text box show, from the two channels (pure: no React, tested on the fixtures).
import { type Candela, candele as aggregaCandele } from '@/lib/aggrega'
import { alberoInTesto, esitoTesto, etichetta, type Geometria, geometria, type Radice, type Ramo, riferimento, sceltiDaQui, segnoPrimo } from '@/lib/albero'
import { oraRoma, prezzo } from '@/lib/fmt'
import type { Barre, Livello, StrumentoFrequenze, StrumentoScenari } from '@/lib/tipi'

export const OPZIONI = { massimoMinuti: 180, padriConFigli: 2 }

export interface Vista {
  candele: Candela[]
  futuri: Date[]
  /** close of the last bar (live one included), UTC s */
  ultimaT: number | null
  radice: Radice
  g: Geometria
  inTesto: boolean
  daQui: { radice: Radice & { soglia?: number | null }; g: Geometria; inTesto: boolean } | null
  rif: number | null
  rifNome: string
  S: number | null
  segno: number | null
  /** y domain: candles, root and drawn heads, plus the levels near them (Trader: 15% of the span) */
  dominio: [number, number] | null
  livelli: Livello[]
  fuori: Livello[]
}

export function vista(s: StrumentoScenari, barre: Barre | null | undefined, f: StrumentoFrequenze | null | undefined, principale: boolean): Vista {
  const { candele, futuri } = aggregaCandele(barre)
  const ultimaT = candele.length ? candele.at(-1)!.date.getTime() / 1000 + 300 : null
  const g = geometria(s.radice, s.rami, OPZIONI)
  const testo = (radiceT: number | null) => radiceT != null && (ultimaT == null || alberoInTesto(radiceT, ultimaT))
  const inTesto = testo(g.radiceT)
  const dq = principale && s.da_qui?.radice ? s.da_qui : null
  const gq = dq ? geometria(dq.radice, sceltiDaQui(dq.rami, 3, 2), { massimoMinuti: 180, padriConFigli: 3 }) : null
  const daQui = dq && gq ? { radice: dq.radice, g: gq, inTesto: testo(gq.radiceT) } : null
  const [rif, rifNome] = riferimento(s)

  const valori = candele.flatMap((c) => [c.low, c.high])
  if (!inTesto) valori.push(s.radice.prezzo, ...g.segmenti.map((x) => x.a.prezzo))
  if (daQui && !daQui.inTesto) valori.push(daQui.radice.prezzo, ...daQui.g.segmenti.map((x) => x.a.prezzo))
  const tutti = (f?.livelli ?? []).filter((x) => x && x.prezzo != null)
  let dominio: [number, number] | null = null
  let livelli: Livello[] = []
  let fuori: Livello[] = []
  if (valori.length) {
    const lo = Math.min(...valori)
    const hi = Math.max(...valori)
    const m = (hi - lo) * 0.15
    livelli = tutti.filter((x) => x.prezzo >= lo - m && x.prezzo <= hi + m)
    fuori = tutti.filter((x) => !livelli.includes(x))
    const lp = livelli.map((x) => x.prezzo)
    dominio = [Math.min(lo, ...lp), Math.max(hi, ...lp)]
  }
  return {
    candele, futuri, ultimaT, radice: s.radice, g, inTesto, daQui, rif, rifNome, S: f?.soglia ?? f?.apertura?.soglia ?? null,
    segno: segnoPrimo(s.radice.percorso), dominio, livelli, fuori,
  }
}

const poi = (r: Ramo) => (r.padre ? 'poi ' : '')

/** The outcomes box (D8): the tree's branches without minutes, then da_qui's, one line each (Trader esito_ramo). */
export function righeEsiti(v: Vista): { id: string; testo: string }[] {
  const righe = v.g.esiti.map((r) => ({ id: r.id, testo: poi(r) + esitoTesto(r, v.rif, v.rifNome, v.S, v.segno) }))
  if (v.daQui) {
    const rq = v.daQui.radice
    righe.push(...v.daQui.g.esiti.map((r) => ({ id: `da-qui-${r.id}`, testo: `da qui: ${poi(r)}${esitoTesto(r, rq.prezzo, 'il punto', rq.soglia ?? v.S, null)}` })))
  }
  return righe
}

const minuti = (r: Ramo) => (r.minuti ? ` · mediana ${r.minuti.mediana} min dalla radice` : '')

function radiceRiga(r: Radice): string {
  return `radice ${r.ora} ${r.fase} a ${prezzo(r.prezzo)}${r.percorso ? ` | ${r.percorso}` : ''}`
}

/** The text box: the whole tree when it is in text (root > last bar + 2 h), else the branches not drawn. */
export function righeTesto(v: Vista): string[] {
  const out: string[] = []
  const parte = (g: Geometria, radice: Radice, inTesto: boolean, pre: string) => {
    if (inTesto) {
      out.push(`${pre}${radiceRiga(radice)}: oltre 2 ore dopo l'ultima barra, albero in testo`)
      for (const x of g.segmenti) out.push(`${pre}  ${poi(x.ramo)}${x.etichetta} a ${prezzo(x.a.prezzo)} verso le ${oraRoma(x.a.t * 1000)}`)
    }
    if (g.testo.length) {
      out.push(`${pre}rami non disegnati (oltre 180 min dalla radice, o figli dei padri meno probabili):`)
      for (const r of g.testo) out.push(`${pre}  ${poi(r)}${etichetta(r)}${minuti(r)}`)
    }
  }
  parte(v.g, v.radice, v.inTesto, '')
  if (v.daQui) parte(v.daQui.g, v.daQui.radice, v.daQui.inTesto, 'da qui: ')
  return out
}

