import { useMemoria } from '@/lib/api'
import { AvvisoFreschezza } from '@/live/AvvisoFreschezza'
import { testoAvviso } from '@/memoria/avviso'
import { ErroreCanale, Eventi, Riconosce, Verifica } from '@/memoria/Sezioni'
import { SOGLIA_CANALE_S, SOGLIA_SPENTO_CANALE_S } from '@/ricerche/stato'

export default function Memoria() {
  const q = useMemoria()
  const d = q.data?.dati ?? null
  const canale = { d, errore: q.error, attesa: q.isPending }
  return (
    <section className="flex max-w-4xl flex-col gap-8">
      <header className="flex flex-col gap-3">
        <h1 className="font-serif text-3xl font-semibold tracking-tight md:text-4xl">Memoria del mercato</h1>
        {/* sempre visibile, prima di qualunque numero, anche senza dati */}
        <aside role="note" className="border-border bg-card rounded-md border p-4" style={{ borderColor: 'var(--ch-warm-deep)' }}>
          <p className="text-foreground leading-relaxed font-medium">{testoAvviso(d?.verdetti.verdetti)}</p>
        </aside>
      </header>
      <AvvisoFreschezza canale="Memoria" q={q} sogliaS={SOGLIA_CANALE_S.memoria} spentoS={SOGLIA_SPENTO_CANALE_S.memoria} />
      {q.error && !d && <ErroreCanale errore={q.error} />}
      <Riconosce />
      <Eventi {...canale} />
      <Verifica {...canale} />
    </section>
  )
}
