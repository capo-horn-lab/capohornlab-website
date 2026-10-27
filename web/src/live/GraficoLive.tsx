// The 5-minute candles (Bklit CandlestickChart) with the key levels, the scenario tree, da_qui and the live candle drawn as an
// SVG overlay on the chart's own scales (useChartStable: xScale Date->px, yScale price->px, in the plot's inner space).
// The y scale is re-provided (ScalaPrezzi) so candles, grid, axis and overlay share a domain that also holds the tree's heads
// and the levels near the candles (the Trader's rule); the x domain is widened by xDomain/xDomainSlotCount to 36 future slots.
// Labels: on a price chart a label's height reads as a price, so no label moves more than one row (12 px) from what it labels.
// From md up the labels are inline and one that finds no place within a row becomes a number; below md the roots and the
// branches are numbers. The numbered legend under the chart (the same rows for screen readers: Bklit's SVG is aria-hidden)
// is visible on phones and, from md up, shows the rows whose label became a number.
import { scaleLinear } from '@visx/scale'
import { useReducedMotion } from 'motion/react'
import { type ReactNode, useEffect, useMemo, useState, useSyncExternalStore } from 'react'
import { Candlestick, CandlestickChart, ChartTooltip, Grid, YAxis } from '@/components/charts'
import { ChartProvider, useChart, useChartStable } from '@/components/charts/chart-context'
import { DEFAULT_Y_AXIS_ID } from '@/components/charts/y-axis-scales'
import type { Candela } from '@/lib/aggrega'
import { nomeBreve, type Segmento } from '@/lib/albero'
import { num, oraRoma, p, prezzo } from '@/lib/fmt'
import { radiceRiga, rigaSegmento, type Vista } from '@/live/vista'

const MARGINE = { top: 16, right: 64, bottom: 28, left: 8 }
const ALONE = { stroke: 'var(--ch-ink)', strokeWidth: 3, paintOrder: 'stroke' as const, strokeLinejoin: 'round' as const }
const FONT = 11
const CARATTERE = 6 // px per character at 11 px (DM Sans): labels that would leave the plot on the left are shortened
const RIGA = 12
const MD = '(min-width: 48rem)' // Tailwind's md, the same breakpoint as the legend's md:sr-only

/** Viewport at md or wider (true where matchMedia is missing). */
function useLargo(): boolean {
  return useSyncExternalStore(
    (avvisa) => {
      const m = typeof window.matchMedia === 'function' ? window.matchMedia(MD) : null
      m?.addEventListener('change', avvisa)
      return () => m?.removeEventListener('change', avvisa)
    },
    () => (typeof window.matchMedia === 'function' ? window.matchMedia(MD).matches : true),
    () => true,
  )
}

function ScalaPrezzi({ dominio, children }: { dominio: [number, number]; children: ReactNode }) {
  const ctx = useChart()
  const [lo, hi] = dominio
  const yScale = useMemo(() => {
    const pad = (hi - lo) * 0.05 || 1
    return scaleLinear<number>({ range: [ctx.innerHeight, 0], domain: [lo - pad, hi + pad], nice: true })
  }, [lo, hi, ctx.innerHeight])
  const yScales = useMemo(() => ({ ...ctx.yScales, [DEFAULT_Y_AXIS_ID]: yScale }), [ctx.yScales, yScale])
  return <ChartProvider value={{ ...ctx, yScale, yScales }}>{children}</ChartProvider>
}

/** testa + nome + coda in `px` pixels: the name gives way with '…', the head and the frequency never (the Trader's `adatta`). */
function adatta(testa: string, nome: string, coda: string, px: number): string {
  const posto = Math.floor(px / CARATTERE) - testa.length - coda.length - 1
  return nome.length <= posto ? `${testa}${nome} ${coda}` : `${testa}${nome.slice(0, Math.max(1, posto - 1)).trimEnd()}… ${coda}`
}

const taglia = (s: string, px: number) => (s.length * CARATTERE <= px ? s : `${s.slice(0, Math.max(1, Math.floor(px / CARATTERE) - 1)).trimEnd()}…`)

/** One stack for every label and number: a place at the anchor, one row up or one row down, inside the plot, not covering
 * a label already placed (horizontal extent included); null when there is none. */
function impila(fondo: number) {
  const usate: { y: number; x0: number; x1: number }[] = []
  const libero = (y: number, x0: number, x1: number) => y >= FONT && y <= fondo && !usate.some((u) => Math.abs(u.y - y) < RIGA && u.x0 < x1 && x0 < u.x1)
  const metti = (y: number, x0: number, x1: number) => {
    usate.push({ y, x0, x1 })
    return y
  }
  return {
    posto(y: number, x0: number, x1: number): number | null {
      const v = [y, y - RIGA, y + RIGA].find((c) => libero(c, x0, x1))
      return v == null ? null : metti(v, x0, x1)
    },
    forza: (y: number, x0: number, x1: number) => metti(Math.min(fondo, Math.max(FONT, y)), x0, x1),
  }
}

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

function Sovrapposizione({ v, viva, numeri, largo, avvisa }: {
  v: Vista
  viva: Candela | null
  numeri: Map<string, number>
  largo: boolean
  avvisa: (numerati: string) => void
}) {
  const { xScale, yScale, innerWidth, innerHeight, columnWidth } = useChartStable()
  // a time inside a 5-minute slot falls on its candle: the candle's date is the slot start, drawn at the slot's centre
  const x = (t: number) => xScale(new Date(t * 1000 - 150_000)) ?? 0
  const y = (prezzo: number) => yScale(prezzo) ?? 0
  const [d0, d1] = xScale.domain().map((d) => d.getTime() / 1000)
  // full Rome hours at the slot boundary (x(t) of a slot start is its candle's left edge); on narrow charts every 2nd/3rd hour,
  // so the labels stay >= 44 px apart
  const passo = Math.max(1, Math.ceil(44 / Math.max(1, x(d0 + 3600) - x(d0))))
  const ore: number[] = []
  for (let t = Math.ceil(d0 / 3600) * 3600; t <= d1 + 300; t += 3600) if (Number(oraRoma(t * 1000).slice(0, 2)) % passo === 0) ore.push(t)
  const pila = impila(innerHeight + 6)
  const largoTesto = (s: string) => s.length * CARATTERE
  const numerati: string[] = []

  /** The label at its anchor (within one row), else the item's number next to its point (within one row, or forced there). */
  const scritta = (id: string, testo: string | null, ancora: { x: number; y: number; fine: boolean }, punto: { x: number; y: number }, colore: string) => {
    if (testo != null) {
      const [x0, x1] = ancora.fine ? [ancora.x - largoTesto(testo), ancora.x] : [ancora.x, ancora.x + largoTesto(testo)]
      const yy = pila.posto(ancora.y, x0, x1)
      if (yy != null)
        return <text x={ancora.x} y={yy} data-ancora={ancora.y} textAnchor={ancora.fine ? 'end' : 'start'} fontSize={FONT} fill={colore} {...ALONE}>{testo}</text>
    }
    numerati.push(id)
    const n = String(numeri.get(id) ?? '')
    const w = largoTesto(n)
    const ya = punto.y + 4
    const destra = pila.posto(ya, punto.x + 5, punto.x + 5 + w)
    const sinistra = destra == null ? pila.posto(ya, punto.x - 5 - w, punto.x - 5) : null
    const [xn, yn, fine] = destra != null ? [punto.x + 5, destra, false] : sinistra != null ? [punto.x - 5, sinistra, true] : [punto.x + 5, pila.forza(ya, punto.x + 5, punto.x + 5 + w), false]
    return <text x={xn} y={yn} data-ancora={ya} textAnchor={fine ? 'end' : 'start'} fontSize={FONT} fontWeight={600} fill={colore} {...ALONE}>{n}</text>
  }

  const livello = (l: Vista['livelli'][number]) => {
    const yl = y(l.prezzo)
    return (
      <g key={l.nome}>
        <line x1={0} x2={innerWidth} y1={yl} y2={yl} stroke="var(--ch-info)" strokeDasharray="2 4" strokeOpacity={0.8} />
        {scritta(`livello:${l.nome}`, `${l.nome} ${p(l.entro_2200)}`, { x: 4, y: yl - 3, fine: false }, { x: 4, y: yl }, 'var(--ch-info)')}
      </g>
    )
  }

  const ramo = (s: Segmento, id: string, tratteggio?: string, prefisso = '') => {
    const yA = y(s.a.prezzo)
    const colore = s.classe >= 2 ? 'var(--ch-fog)' : 'var(--ch-quiet)'
    const xa = x(s.a.t)
    const testo = largo ? adatta(prefisso, nomeBreve(s.ramo.etichetta), p(s.ramo), xa - 4) : null
    return (
      <g key={id}>
        <title>{prefisso + s.etichetta}</title>
        <line x1={x(s.da.t)} y1={y(s.da.prezzo)} x2={xa} y2={yA} stroke={colore} strokeWidth={s.classe} strokeDasharray={tratteggio} strokeOpacity={0.9} />
        <line x1={x(s.q1.t)} y1={yA} x2={x(s.q3.t)} y2={yA} stroke={colore} strokeWidth={1} strokeOpacity={0.45} />
        <circle cx={xa} cy={yA} r={2.5} fill={colore} />
        {scritta(id, testo, { x: xa - 4, y: yA - 5, fine: true }, { x: xa, y: yA }, colore)}
      </g>
    )
  }

  const radice = (id: string, r: { t: number; prezzo: number; testo: string; vuota?: boolean }) => {
    const xr = x(r.t)
    const yr = y(r.prezzo)
    return (
      <g key={id}>
        <title>{r.testo}</title>
        <circle cx={xr} cy={yr} r={3.5} fill={r.vuota ? 'var(--ch-ink)' : 'var(--ch-fog)'} stroke="var(--ch-fog)" strokeWidth={1.5} />
        {scritta(id, largo ? taglia(r.testo, xr - 6) : null, { x: xr - 6, y: yr + 14, fine: true }, { x: xr, y: yr }, 'var(--ch-quiet)')}
      </g>
    )
  }

  const percorso = v.radice.percorso && v.radice.percorso.length > 40 ? `${v.radice.percorso.slice(0, 37)}...` : v.radice.percorso
  const disegno = (
    <g className="chl-sovrapposizione">
      {ore.map((t) => (
        <g key={t}>
          <line x1={x(t)} x2={x(t)} y1={0} y2={innerHeight} stroke="var(--ch-line)" strokeOpacity={0.5} />
          <text x={x(t)} y={innerHeight + 18} textAnchor="middle" fontSize={FONT} fill="var(--ch-quiet)">{oraRoma(t * 1000)}</text>
        </g>
      ))}
      {v.livelli.map(livello)}
      {viva ? (
        <g opacity={0.5}>
          <rect x={x(viva.date.getTime() / 1000 + 150) - 0.75} width={1.5} y={y(viva.high)} height={Math.max(1, y(viva.low) - y(viva.high))}
            fill={viva.close >= viva.open ? 'var(--ch-mist)' : 'var(--ch-signal-deep)'} />
          <rect x={x(viva.date.getTime() / 1000 + 150) - columnWidth * 0.4} width={columnWidth * 0.8} y={Math.min(y(viva.open), y(viva.close))}
            height={Math.max(1, Math.abs(y(viva.open) - y(viva.close)))} rx={1} fill={viva.close >= viva.open ? 'var(--ch-mist)' : 'var(--ch-signal-deep)'} />
        </g>
      ) : null}
      {!v.inTesto && v.g.radiceT != null ? (
        <>
          {v.g.segmenti.map((s) => ramo(s, `ramo:${s.id}`))}
          {radice('radice', { t: v.g.radiceT, prezzo: v.radice.prezzo, testo: `${v.radice.ora} ${v.radice.fase}${percorso ? ` | ${percorso}` : ''}` })}
        </>
      ) : null}
      {v.daQui && !v.daQui.inTesto && v.daQui.g.radiceT != null ? (
        <>
          {v.daQui.g.segmenti.map((s) => ramo(s, `qui:${s.id}`, '5 4', 'da qui: '))}
          {radice('qui:radice', { t: v.daQui.g.radiceT, prezzo: v.daQui.radice.prezzo, testo: `da qui ${v.daQui.radice.ora}`, vuota: true })}
        </>
      ) : null}
    </g>
  )
  const chiave = numerati.join('|')
  useEffect(() => avvisa(chiave), [avvisa, chiave])
  return disegno
}

function Suggerimento({ point }: { point: Record<string, unknown> }) {
  const c = point as unknown as Candela
  return (
    <div className="space-y-0.5 px-1 font-mono text-xs tabular-nums">
      <div className="text-muted-foreground">{`${oraRoma(c.date)}-${oraRoma(c.date.getTime() + 300_000)} Roma`}</div>
      <div>{`apertura ${prezzo(c.open)} · massimo ${prezzo(c.high)}`}</div>
      <div>{`minimo ${prezzo(c.low)} · chiusura ${prezzo(c.close)}`}</div>
      <div className="text-muted-foreground">{`volume ${num(c.volume, 0)}`}</div>
    </div>
  )
}

/** The numbered legend: visible below md; from md up only the rows whose label became a number (the rest for screen readers). */
function Legenda({ righe, numerati }: { righe: Voce[]; numerati: Set<string> }) {
  return (
    <ul className="text-muted-foreground mt-2 space-y-0.5 font-mono text-xs leading-relaxed tabular-nums">
      {righe.map((r) => <li key={r.id} className={numerati.has(r.id) ? undefined : 'md:sr-only'}>{`${r.n} · ${r.testo}`}</li>)}
    </ul>
  )
}

export function GraficoLive({ v }: { v: Vista }) {
  const ridotto = useReducedMotion() ?? false
  const largo = useLargo()
  const [numerati, setNumerati] = useState('')
  const righe = useMemo(() => voci(v), [v])
  const numeri = useMemo(() => new Map(righe.map((r) => [r.id, r.n])), [righe])
  const chiuse = useMemo(() => v.candele.filter((c) => !c.viva), [v.candele])
  const viva = v.candele.find((c) => c.viva) ?? null
  const xDomain = useMemo((): [Date, Date] | null => {
    if (!v.candele.length) return null
    const ultimo = v.futuri.at(-1) ?? v.candele.at(-1)!.date
    // a tree that starts after the last bar but within 2 h may reach past the 36 slots: the domain follows its drawn heads
    const disegnati = [v.inTesto ? null : v.g, v.daQui && !v.daQui.inTesto ? v.daQui.g : null]
    const capi = disegnati.flatMap((g) => g?.segmenti ?? []).map((s) => Math.max(s.a.t, s.q3.t) * 1000 - 150_000)
    return [v.candele[0].date, new Date(Math.max(ultimo.getTime(), ...capi))]
  }, [v.candele, v.futuri, v.g, v.inTesto, v.daQui])

  if (!xDomain || !v.dominio || !chiuse.length) {
    return <p className="text-muted-foreground text-sm">Nessuna barra a 5 minuti per questo strumento.</p>
  }
  const slot = Math.round((xDomain[1].getTime() - xDomain[0].getTime()) / 300_000) + 1
  return (
    <figure className="m-0">
      <CandlestickChart
        data={chiuse}
        xDomain={xDomain}
        xDomainSlotCount={slot}
        margin={MARGINE}
        aspectRatio="auto"
        className="h-[50vh] max-h-[44rem] min-h-72 md:h-[60vh]"
        animationDuration={ridotto ? 0 : 900}
      >
        <ScalaPrezzi dominio={v.dominio}>
          <Grid numTicksRows={6} fadeHorizontal={false} />
          <Candlestick animate={!ridotto} showHoverFade={false} />
          <Sovrapposizione v={v} viva={viva} numeri={numeri} largo={largo} avvisa={setNumerati} />
          <YAxis orientation="right" formatValue={prezzo} />
        </ScalaPrezzi>
        <ChartTooltip showDots={false} showDatePill={false} content={({ point }) => <Suggerimento point={point} />} />
      </CandlestickChart>
      <Legenda righe={righe} numerati={new Set(numerati.split('|'))} />
      <figcaption className="text-muted-foreground mt-2 text-xs">
        {`Candele a 5 minuti in ora di Roma${viva ? ' (l\'ultima, attenuata, e\' in formazione)' : ''}; linee tratteggiate: livelli con la frequenza di tocco entro le ${v.chiusura}`}
        {v.fuori.length ? `; fuori dal grafico: ${v.fuori.map((l) => `${l.nome} ${prezzo(l.prezzo)} ${p(l.entro_2200)}`).join(', ')}` : ''}.
      </figcaption>
    </figure>
  )
}
