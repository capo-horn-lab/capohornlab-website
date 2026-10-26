import { useState } from 'react'
import { Skeleton } from '@/components/ui/skeleton'
import { useFrequenze, useScenari } from '@/lib/api'
import { AvvisoFreschezza } from '@/live/AvvisoFreschezza'
import { StatoLive } from '@/live/StatoLive'
import { StrumentoTabs } from '@/live/StrumentoTabs'

export default function Live() {
  const scenari = useScenari()
  const frequenze = useFrequenze()
  const [strumento, setStrumento] = useState<string | null>(null)
  const scen = scenari.data?.dati
  const freq = frequenze.data?.dati
  const attesa = scenari.isPending && frequenze.isPending
  return (
    <section className="space-y-6">
      <header className="space-y-2">
        <h1 className="font-serif text-3xl font-semibold tracking-tight md:text-4xl">Frequenze live</h1>
        <StatoLive busta={scenari.data?.dati ? scenari.data : frequenze.data} />
      </header>
      <div className="space-y-2">
        <AvvisoFreschezza canale="Grafico e albero" q={scenari} sogliaS={60} />
        <AvvisoFreschezza canale="Tabelle" q={frequenze} sogliaS={180} />
      </div>
      {attesa ? <Skeleton className="h-[50vh] w-full" /> : <StrumentoTabs scen={scen} freq={freq} valore={strumento} onCambia={setStrumento} />}
      {freq?.limiti?.length ? (
        <section className="space-y-2">
          <h2 className="font-mono text-xs font-medium tracking-wider">LIMITI</h2>
          <ul className="text-muted-foreground list-disc space-y-1 pl-5 text-xs leading-relaxed">
            {freq.limiti.map((l) => <li key={l}>{l}</li>)}
          </ul>
        </section>
      ) : null}
    </section>
  )
}
