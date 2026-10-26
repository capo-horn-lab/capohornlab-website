// The 5-minute candles (Bklit CandlestickChart) with the key levels, the scenario tree, da_qui and the live candle drawn as an
// SVG overlay on the chart's own scales (useChartStable: xScale Date->px, yScale price->px, in the plot's inner space).
// The y scale is re-provided (ScalaPrezzi) so candles, grid, axis and overlay share a domain that also holds the tree's heads
// and the levels near the candles (the Trader's rule); the x domain is widened by xDomain/xDomainSlotCount to 36 future slots.
import { scaleLinear } from '@visx/scale'
import { useReducedMotion } from 'motion/react'
import { type ReactNode, useMemo } from 'react'
import { Candlestick, CandlestickChart, ChartTooltip, Grid, YAxis } from '@/components/charts'
import { ChartProvider, useChart, useChartStable } from '@/components/charts/chart-context'
import { DEFAULT_Y_AXIS_ID } from '@/components/charts/y-axis-scales'
import type { Candela } from '@/lib/aggrega'
import { nomeBreve, type Segmento } from '@/lib/albero'
import { num, oraRoma, p, prezzo } from '@/lib/fmt'
import type { Vista } from '@/live/vista'

const MARGINE = { top: 16, right: 64, bottom: 28, left: 8 }
const ALONE = { stroke: 'var(--ch-ink)', strokeWidth: 3, paintOrder: 'stroke' as const, strokeLinejoin: 'round' as const }

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

const CARATTERE = 5.5 // px per character at 10 px (DM Sans): labels that would leave the plot on the left are shortened

/** testa + nome + coda in `px` pixels: the name gives way with '…', the head and the frequency never (the Trader's `adatta`). */
function adatta(testa: string, nome: string, coda: string, px: number): string {
  const posto = Math.floor(px / CARATTERE) - testa.length - coda.length - 1
  return nome.length <= posto ? `${testa}${nome} ${coda}` : `${testa}${nome.slice(0, Math.max(1, posto - 1)).trimEnd()}… ${coda}`
}

const taglia = (s: string, px: number) => (s.length * CARATTERE <= px ? s : `${s.slice(0, Math.max(1, Math.floor(px / CARATTERE) - 1)).trimEnd()}…`)

/** Labels at the same height are stacked upwards, 12 px apart (the indicator's `pila`). */
function impila(): (y: number) => number {
  const usati: number[] = []
  return (y) => {
    let v = y
    while (usati.some((u) => Math.abs(u - v) < 11)) v -= 12
    usati.push(v)
    return v
  }
}

function Sovrapposizione({ v, viva }: { v: Vista; viva: Candela | null }) {
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
  const pilaLivelli = impila()
  const pilaRami = impila()

  const ramo = (s: Segmento, tratteggio?: string, prefisso = '') => {
    const yA = y(s.a.prezzo)
    const colore = s.classe >= 2 ? 'var(--ch-fog)' : 'var(--ch-quiet)'
    const xa = x(s.a.t)
    const yl = pilaRami(yA - 5)
    return (
      <g key={prefisso + s.id}>
        <title>{prefisso + s.etichetta}</title>
        <line x1={x(s.da.t)} y1={y(s.da.prezzo)} x2={xa} y2={yA} stroke={colore} strokeWidth={s.classe} strokeDasharray={tratteggio} strokeOpacity={0.9} />
        <line x1={x(s.q1.t)} y1={yA} x2={x(s.q3.t)} y2={yA} stroke={colore} strokeWidth={1} strokeOpacity={0.45} />
        <circle cx={xa} cy={yA} r={2.5} fill={colore} />
        <text x={xa - 4} y={yl} textAnchor="end" fontSize={10} fill={colore} {...ALONE}>
          {adatta(prefisso, nomeBreve(s.ramo.etichetta), p(s.ramo), xa - 4)}
        </text>
      </g>
    )
  }

  const radice = (r: { t: number; prezzo: number; testo: string; vuota?: boolean }) => (
    <g>
      <title>{r.testo}</title>
      <circle cx={x(r.t)} cy={y(r.prezzo)} r={3.5} fill={r.vuota ? 'var(--ch-ink)' : 'var(--ch-fog)'} stroke="var(--ch-fog)" strokeWidth={1.5} />
      <text x={x(r.t) - 6} y={pilaRami(y(r.prezzo) + 14)} textAnchor="end" fontSize={10} fill="var(--ch-quiet)" {...ALONE}>{taglia(r.testo, x(r.t) - 6)}</text>
    </g>
  )

  const percorso = v.radice.percorso && v.radice.percorso.length > 40 ? `${v.radice.percorso.slice(0, 37)}...` : v.radice.percorso
  return (
    <g className="chl-sovrapposizione">
      {ore.map((t) => (
        <g key={t}>
          <line x1={x(t)} x2={x(t)} y1={0} y2={innerHeight} stroke="var(--ch-line)" strokeOpacity={0.5} />
          <text x={x(t)} y={innerHeight + 18} textAnchor="middle" fontSize={10} fill="var(--ch-quiet)">{oraRoma(t * 1000)}</text>
        </g>
      ))}
      {v.livelli.map((l) => (
        <g key={l.nome}>
          <line x1={0} x2={innerWidth} y1={y(l.prezzo)} y2={y(l.prezzo)} stroke="var(--ch-info)" strokeDasharray="2 4" strokeOpacity={0.8} />
          <text x={4} y={pilaLivelli(y(l.prezzo) - 3)} fontSize={10} fill="var(--ch-info)" {...ALONE}>{`${l.nome} ${p(l.entro_2200)}`}</text>
        </g>
      ))}
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
          {v.g.segmenti.map((s) => ramo(s))}
          {radice({ t: v.g.radiceT, prezzo: v.radice.prezzo, testo: `${v.radice.ora} ${v.radice.fase}${percorso ? ` | ${percorso}` : ''}` })}
        </>
      ) : null}
      {v.daQui && !v.daQui.inTesto && v.daQui.g.radiceT != null ? (
        <>
          {v.daQui.g.segmenti.map((s) => ramo(s, '5 4', 'da qui: '))}
          {radice({ t: v.daQui.g.radiceT, prezzo: v.daQui.radice.prezzo, testo: `da qui ${v.daQui.radice.ora}`, vuota: true })}
        </>
      ) : null}
    </g>
  )
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

export function GraficoLive({ v }: { v: Vista }) {
  const ridotto = useReducedMotion() ?? false
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
          <Sovrapposizione v={v} viva={viva} />
          <YAxis orientation="right" formatValue={prezzo} />
        </ScalaPrezzi>
        <ChartTooltip showDots={false} showDatePill={false} content={({ point }) => <Suggerimento point={point} />} />
      </CandlestickChart>
      <figcaption className="text-muted-foreground mt-2 text-xs">
        {`Candele a 5 minuti in ora di Roma${viva ? ' (l\'ultima, attenuata, e\' in formazione)' : ''}; linee tratteggiate: livelli con la frequenza di tocco entro le 22:00 (nome convenzionale)`}
        {v.fuori.length ? `; fuori dal grafico: ${v.fuori.map((l) => `${l.nome} ${prezzo(l.prezzo)} ${p(l.entro_2200)}`).join(', ')}` : ''}.
      </figcaption>
    </figure>
  )
}
