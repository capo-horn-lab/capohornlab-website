// The channels' freshness: no data from the engine, data older than the channel's limit (60 s scenari, 180 s frequenze),
// a failed refresh (the last data stay on screen).
import { oraRoma } from '@/lib/fmt'
import type { Busta } from '@/lib/tipi'

export interface StatoCanale {
  data?: Busta<unknown>
  isError: boolean
  dataUpdatedAt: number
  errorUpdatedAt: number
}

export function avvisi(q: StatoCanale, sogliaS: number): string[] {
  const out: string[] = []
  if (q.isError)
    out.push(q.data
      ? `Aggiornamento fallito alle ${oraRoma(q.errorUpdatedAt)}; ultimo caricamento riuscito alle ${oraRoma(q.dataUpdatedAt)}`
      : `Aggiornamento fallito alle ${oraRoma(q.errorUpdatedAt)}; nessun caricamento riuscito finora`)
  if (q.data && q.data.dati == null) out.push("Nessun dato dal motore (spento, o non ha ancora pubblicato).")
  else if (q.data?.eta_s != null && q.data.eta_s > sogliaS) {
    const m = Math.max(1, Math.round(q.data.eta_s / 60))
    out.push(`Motore spento o scollegato da ${m} ${m === 1 ? 'minuto' : 'minuti'}`)
  }
  return out
}

export function AvvisoFreschezza({ canale, q, sogliaS }: { canale: string; q: StatoCanale; sogliaS: number }) {
  const righe = avvisi(q, sogliaS)
  if (!righe.length) return null
  return (
    <div role="status" className="border-border text-muted-foreground rounded-md border px-3 py-2 text-sm" style={{ borderColor: 'var(--ch-warm-deep)' }}>
      <span className="text-foreground font-medium">{canale}: </span>
      {righe.join('. ')}
    </div>
  )
}
