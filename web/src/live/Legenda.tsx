// The chart's legend and caption, without Bklit or Motion: the live page draws them (with a box of the chart's height) while
// the chart's own chunk is still loading, so the text and the tables under it do not move when the chart arrives.
import type { Candela } from '@/lib/aggrega'
import { p, prezzo } from '@/lib/fmt'
import { radiceRiga, rigaSegmento, type Vista } from '@/live/vista'

/** The chart's box: the same classes on the chart and on its placeholder. */
export const ALTEZZA_GRAFICO = 'h-[50vh] max-h-[44rem] min-h-72 md:h-[60vh]'
export const MD = '(min-width: 48rem)' // Tailwind's md, the same breakpoint as the legend's md:sr-only

export interface Voce {
  id: string
  n: number
  testo: string
}

/** The legend's rows (numbered in this order): root, branches, da_qui's root and branches, levels. */
export function voci(v: Vista): Voce[] {
  const r: Omit<Voce, 'n'>[] = []
  if (!v.inTesto) r.push({ id: 'radice', testo: radiceRiga(v.radice) }, ...v.g.segmenti.map((s) => ({ id: `ramo:${s.id}`, testo: rigaSegmento(s) })))
  if (v.daQui && !v.daQui.inTesto)
    r.push({ id: 'qui:radice', testo: `da qui: radice ${v.daQui.radice.ora} a ${prezzo(v.daQui.radice.prezzo)}` },
      ...v.daQui.g.segmenti.map((s) => ({ id: `qui:${s.id}`, testo: `da qui: ${rigaSegmento(s)}` })))
  r.push(...v.livelli.map((l) => ({ id: `livello:${l.nome}`, testo: `livello ${l.nome} ${prezzo(l.prezzo)}: ${p(l.entro_2200)}` })))
  return r.map((x, i) => ({ ...x, n: i + 1 }))
}

/** The legend: visible below md; from md up only the rows whose label became a number (the rest for screen readers).
 * Only a row drawn as a number carries its number; a row labelled inline gets a dot, so every number here is on the chart. */
export function Legenda({ righe, numerati }: { righe: Voce[]; numerati: Set<string> }) {
  return (
    <ul className="text-muted-foreground mt-2 space-y-0.5 font-mono text-xs leading-relaxed tabular-nums">
      {righe.map((r) => (
        <li key={r.id} className={numerati.has(r.id) ? undefined : 'md:sr-only'}>{`${numerati.has(r.id) ? `${r.n} · ` : '• '}${r.testo}`}</li>
      ))}
    </ul>
  )
}

export function Didascalia({ v, viva }: { v: Vista; viva: Candela | null }) {
  return (
    <figcaption className="text-muted-foreground mt-2 text-xs">
      {`Candele a 5 minuti in ora di Roma${viva ? ' (l\'ultima, attenuata, e\' in formazione)' : ''}; linee tratteggiate: livelli con la frequenza di tocco entro le ${v.chiusura}`}
      {v.fuori.length ? `; fuori dal grafico: ${v.fuori.map((l) => `${l.nome} ${prezzo(l.prezzo)} ${p(l.entro_2200)}`).join(', ')}` : ''}.
    </figcaption>
  )
}

/** While the chart loads: its box, then the same legend and caption. Below md the roots and branches will be numbers (the
 * chart's rule), from md up nothing is numbered yet: a level that later becomes a number adds one line, nothing else moves. */
export function SegnapostoGrafico({ v }: { v: Vista }) {
  const largo = typeof window.matchMedia === 'function' ? window.matchMedia(MD).matches : true
  const righe = voci(v)
  const numerati = new Set(largo ? [] : righe.filter((r) => !r.id.startsWith('livello:')).map((r) => r.id))
  const chiuse = v.candele.some((c) => !c.viva)
  if (!chiuse) return null
  return (
    <figure className="m-0">
      <div className={`relative w-full ${ALTEZZA_GRAFICO}`} aria-hidden="true" />
      <Legenda righe={righe} numerati={numerati} />
      <Didascalia v={v} viva={v.candele.find((c) => c.viva) ?? null} />
    </figure>
  )
}
