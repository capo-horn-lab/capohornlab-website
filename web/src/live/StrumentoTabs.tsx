// One tab per instrument (the main one first, then the JSON's order); the selected one shows its status, chart, outcomes,
// tree text and panel tables. The chart is keyed by instrument: recreated only when the instrument changes.
import NumberFlow from '@number-flow/react'
import { lazy, Suspense, useMemo } from 'react'
import { GraficoNonDisponibile } from '@/components/grafico-non-disponibile'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { residua } from '@/lib/albero'
import { useDopoIlPrimoPaint } from '@/lib/dopo-paint'
import { num } from '@/lib/fmt'
import { type Frequenze, haErrore, type Scenari, type StrumentoFrequenze, type StrumentoScenari } from '@/lib/tipi'
import { AlberoTesto, Esiti } from '@/live/Esiti'
import { SegnapostoGrafico } from '@/live/Legenda'
import { TabellePannello } from '@/live/TabellePannello'
import { radiceRiga, righeEsiti, righeTesto, vista } from '@/live/vista'

// the chart (Bklit + Motion, the heaviest code of the page) in its own chunk: the text and the tables paint first, the chart's
// box, legend and caption are already in place (SegnapostoGrafico), so nothing moves when it arrives; if the chunk does not
// load, one line takes the chart's place and the text and tables stay
const GraficoLive = lazy(() =>
  import('@/live/GraficoLive').then((m) => ({ default: m.GraficoLive }), () => ({ default: GraficoNonDisponibile })),
)

/** Instruments of both channels, the main one first, then scenari's order, then frequenze's. */
export function ordineStrumenti(scen: Scenari | null | undefined, freq: Frequenze | null | undefined): string[] {
  const principale = scen?.principale.strumento ?? freq?.principale.strumento
  return [...new Set([principale, ...Object.keys(scen?.strumenti ?? {}), ...Object.keys(freq?.strumenti ?? {})].filter((s): s is string => Boolean(s)))]
}

function Grafico({ s, sc, scen, fr }: { s: string; sc: StrumentoScenari; scen: Scenari; fr: StrumentoFrequenze | null }) {
  const barre = scen.barre[s]
  const v = useMemo(() => vista(sc, barre, fr, s === scen.principale.strumento, scen.orari), [sc, barre, fr, s, scen.principale.strumento, scen.orari])
  const esiti = useMemo(() => righeEsiti(v), [v])
  const testo = useMemo(() => righeTesto(v), [v])
  const er = residua(sc.escursione_residua)
  const pronto = useDopoIlPrimoPaint()
  return (
    <div className="space-y-4">
      <p className="font-mono text-xs leading-relaxed tabular-nums">
        <span className="text-foreground">{sc.contratto} </span>
        {sc.prezzo != null ? <NumberFlow value={sc.prezzo} locales="en-US" format={{ useGrouping: false, maximumFractionDigits: 2 }} /> : '-'}
        <span className="text-muted-foreground">{` · ${sc.cadenza} · A ${num(sc.A)}`}</span>
        <br />
        <span className="text-muted-foreground">{radiceRiga(sc.radice)}</span>
        {er ? <><br /><span className="text-muted-foreground">{er}</span></> : null}
      </p>
      <Suspense fallback={<SegnapostoGrafico v={v} />}>
        {pronto ? <GraficoLive key={s} v={v} /> : <SegnapostoGrafico v={v} />}
      </Suspense>
      <Esiti righe={esiti} />
      <AlberoTesto righe={testo} />
    </div>
  )
}

export function StrumentoTabs({ scen, freq, valore, onCambia }: {
  scen: Scenari | null | undefined
  freq: Frequenze | null | undefined
  valore: string | null
  onCambia: (s: string) => void
}) {
  const strumenti = ordineStrumenti(scen, freq)
  const principale = strumenti[0]
  const s = valore && strumenti.includes(valore) ? valore : principale
  if (!s) return null
  const sc = scen?.strumenti[s]
  const fr = freq?.strumenti[s]
  return (
    <Tabs value={s} onValueChange={onCambia}>
      <TabsList className="h-auto flex-wrap">
        {strumenti.map((x) => (
          <TabsTrigger key={x} value={x} className="gap-1.5">
            {x}
            {x === principale ? <Badge variant="outline" className="px-1 py-0 text-[11px]">principale</Badge> : null}
          </TabsTrigger>
        ))}
      </TabsList>
      <TabsContent value={s} className="min-w-0 space-y-8 pt-2">
        {!sc ? <p className="text-muted-foreground text-sm">Nessun grafico: il canale scenari non ha questo strumento.</p>
          : haErrore(sc) ? <p className="text-muted-foreground text-sm">{`${s}: ${sc.errore}`}</p>
          : <Grafico s={s} sc={sc} scen={scen!} fr={fr && !haErrore(fr) ? fr : null} />}
        {!fr ? <p className="text-muted-foreground text-sm">Tabelle del pannello non ancora caricate.</p>
          : haErrore(fr) ? <p className="text-muted-foreground text-sm">{`${s}: ${fr.errore}`}</p>
          : <TabellePannello r={fr} orari={freq?.orari} />}
      </TabsContent>
    </Tabs>
  )
}
