// The page's status line: time of the computation, age at the server (advancing with the clock), main instrument, regular
// session open or closed.
import type { Orari, Principale } from '@/lib/tipi'
import { etaCorrente, type StatoCanale, useAdesso } from '@/live/AvvisoFreschezza'

const GIORNO = new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/Rome', year: 'numeric', month: '2-digit', day: '2-digit' })
const ORA = new Intl.DateTimeFormat('it-IT', { timeZone: 'Europe/Rome', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' })

/** Regular session (orari, Rome clock) open at the computation's time `generato` (ISO with offset). */
export function sessioneAperta(generato: string, orari: Orari | null | undefined): boolean | null {
  const t = Date.parse(generato)
  if (!orari || !Number.isFinite(t)) return null
  const hhmm = ORA.format(t)
  return GIORNO.format(t) === orari.giorno && hhmm >= orari.apertura && hhmm < orari.chiusura
}

type Dati = { generato: string; principale: Principale; orari?: Orari }

export function StatoLive({ q }: { q: StatoCanale }) {
  const adesso = useAdesso()
  const d = q.data?.dati as Dati | null | undefined
  if (!d) return null
  const aperta = sessioneAperta(d.generato, d.orari)
  const eta = etaCorrente(q, adesso)
  const parti = [
    `calcolo delle ${ORA.format(Date.parse(d.generato))} Roma`,
    eta == null ? null : `ricevuto ${Math.round(eta)} s fa`,
    `principale ${d.principale.strumento}${d.principale.contratto ? ` (${d.principale.contratto})` : ''}${d.principale.fresco === false ? ', dati non freschi' : ''}`,
    d.orari ? `sessione regolare ${d.orari.apertura}-${d.orari.chiusura} Roma: ${aperta ? 'aperta' : 'chiusa'}` : null,
  ]
  return <p className="text-muted-foreground font-mono text-xs leading-relaxed">{parti.filter(Boolean).join(' · ')}</p>
}
