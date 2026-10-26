// The page's status line: time of the computation, age at the server, main instrument, regular session open or closed.
import type { Busta, Orari, Principale } from '@/lib/tipi'

const GIORNO = new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/Rome', year: 'numeric', month: '2-digit', day: '2-digit' })
const ORA = new Intl.DateTimeFormat('it-IT', { timeZone: 'Europe/Rome', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' })

/** Regular session (orari, Rome clock) open at the computation's time `generato` (ISO with offset). */
export function sessioneAperta(generato: string, orari: Orari | null | undefined): boolean | null {
  const t = Date.parse(generato)
  if (!orari || !Number.isFinite(t)) return null
  const hhmm = ORA.format(t)
  return GIORNO.format(t) === orari.giorno && hhmm >= orari.apertura && hhmm < orari.chiusura
}

export function StatoLive({ busta }: { busta: Busta<{ generato: string; principale: Principale; orari?: Orari }> | undefined }) {
  const d = busta?.dati
  if (!d) return null
  const aperta = sessioneAperta(d.generato, d.orari)
  const parti = [
    `calcolo delle ${ORA.format(Date.parse(d.generato))} Roma`,
    busta.eta_s == null ? null : `ricevuto ${busta.eta_s} s fa`,
    `principale ${d.principale.strumento}${d.principale.contratto ? ` (${d.principale.contratto})` : ''}${d.principale.fresco === false ? ', dati non freschi' : ''}`,
    d.orari ? `sessione regolare ${d.orari.apertura}-${d.orari.chiusura} Roma: ${aperta ? 'aperta' : 'chiusa'}` : null,
  ]
  return <p className="text-muted-foreground font-mono text-xs leading-relaxed">{parti.filter(Boolean).join(' · ')}</p>
}
