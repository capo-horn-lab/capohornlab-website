// The engine's 5-minute bars (scenari-live barre_5m: [t_close, o, h, l, c, v], UTC s) as chart candles: `date` = slot start,
// the live candle marked, plus 36 empty 5-minute slots (the 180 future minutes the tree may reach).
import type { Barre, Riga } from '@/lib/tipi'

export interface Candela {
  date: Date
  open: number
  high: number
  low: number
  close: number
  volume: number
  viva: boolean
}

export const SLOT_FUTURI = 36

const candela = ([t, open, high, low, close, volume]: Riga, viva: boolean): Candela =>
  ({ date: new Date((t - 300) * 1000), open, high, low, close, volume, viva })

export function candele(barre: Barre | null | undefined): { candele: Candela[]; futuri: Date[] } {
  if (!barre?.righe) return { candele: [], futuri: [] }
  const c = barre.righe.map((r) => candela(r, false))
  if (barre.viva && (!c.length || barre.viva[0] - 300 > c.at(-1)!.date.getTime() / 1000)) c.push(candela(barre.viva, true))
  if (!c.length) return { candele: [], futuri: [] }
  const ultima = c.at(-1)!.date.getTime()
  return { candele: c, futuri: Array.from({ length: SLOT_FUTURI }, (_, i) => new Date(ultima + (i + 1) * 300_000)) }
}
