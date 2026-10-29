// The channels' freshness: no data from the engine, data older than the channel's limit (60 s scenari, 180 s frequenze,
// 180 s memoria, which is "spento" after 600 s),
// a failed refresh (the last data stay on screen). The age is the server's eta_s plus the time since that response arrived,
// so it keeps growing while a request hangs or fails.
import { useEffect, useState } from 'react'
import { scartoBusta } from '@/lib/api'
import { oraRoma } from '@/lib/fmt'
import type { Busta } from '@/lib/tipi'

export interface StatoCanale {
  data?: Busta<unknown>
  isError: boolean
  dataUpdatedAt: number
  errorUpdatedAt: number
}

/** A clock that ticks every `ms`: only the components showing an age re-render with it, never the chart. */
export function useAdesso(ms = 5000): number {
  const [adesso, setAdesso] = useState(() => Date.now())
  useEffect(() => {
    const id = setInterval(() => setAdesso(Date.now()), ms)
    return () => clearInterval(id)
  }, [ms])
  return adesso
}

/** Seconds since the engine's last data reached the server, at `adesso`; null without data. After a 304 the envelope is the
 * old one (its eta_s is frozen), so the age is `ricevuto` plus the local clock, offset by the skew measured at the 200: it
 * never depends on the PC's clock being right and never goes below the eta_s of the 200. Without a measured skew (data not
 * from a 200 of ours) it is eta_s plus the time since dataUpdatedAt. */
export function etaCorrente(q: StatoCanale, adesso: number): number | null {
  if (!q.data?.dati || q.data.eta_s == null) return null
  const scarto = scartoBusta(q.data)
  const t = q.data.ricevuto == null ? NaN : Date.parse(q.data.ricevuto)
  if (scarto != null && Number.isFinite(t)) return Math.max(q.data.eta_s, (adesso - scarto - t) / 1000)
  return q.data.eta_s + Math.max(0, (adesso - q.dataUpdatedAt) / 1000)
}

/** `spentoS`: beyond `sogliaS` the data are "vecchi"; only beyond `spentoS` the engine is "spento o scollegato" (default: the same
 * limit, as for the live channels). */
export function avvisi(q: StatoCanale, sogliaS: number, adesso = Date.now(), spentoS = sogliaS): string[] {
  const out: string[] = []
  if (q.isError)
    out.push(q.data
      ? `Aggiornamento fallito alle ${oraRoma(q.errorUpdatedAt)}; ultimo caricamento riuscito alle ${oraRoma(q.dataUpdatedAt)}`
      : `Aggiornamento fallito alle ${oraRoma(q.errorUpdatedAt)}; nessun caricamento riuscito finora`)
  const eta = etaCorrente(q, adesso)
  if (q.data && q.data.dati == null) out.push("Nessun dato dal motore (spento, o non ha ancora pubblicato).")
  else if (eta != null && eta > sogliaS) {
    const m = Math.max(1, Math.round(eta / 60))
    const unita = m === 1 ? 'minuto' : 'minuti'
    // a failed request may be the network or the site's server, not the engine: then only the data's age is said
    out.push(q.isError || eta <= spentoS ? `Dati vecchi di ${m} ${unita}` : `Motore spento o scollegato da ${m} ${unita}`)
  }
  return out
}

export function AvvisoFreschezza({ canale, q, sogliaS, spentoS }: { canale: string; q: StatoCanale; sogliaS: number; spentoS?: number }) {
  const adesso = useAdesso()
  const righe = avvisi(q, sogliaS, adesso, spentoS)
  if (!righe.length) return null
  return (
    <div role="status" className="border-border text-muted-foreground rounded-md border px-3 py-2 text-sm" style={{ borderColor: 'var(--ch-warm-deep)' }}>
      <span className="text-foreground font-medium">{canale}: </span>
      {righe.join('. ')}
    </div>
  )
}
