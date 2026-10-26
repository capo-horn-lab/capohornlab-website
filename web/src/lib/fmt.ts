// D8 formatting, as the Trader (desktop_trader._pct/_estremo/_p) and the panel (desktop_tools._num/_quart): Python's rounding
// (round half to even on the float) so the site prints the same digits as the app.

export interface Frequenza {
  p: number | null
  k: number
  n: number
  margine?: number | null
}

export interface Quartili {
  mediana: number
  q1: number
  q3: number
  n?: number
}

/** Python's round(x) on a float: halves go to the even neighbour (7728.5 -> 7728, 0.125*100 -> 12). */
function tondo(x: number): number {
  const r = Math.round(x)
  return Math.abs(x - Math.trunc(x)) === 0.5 && r % 2 !== 0 ? r - 1 : r
}

/** f"{x:.0f}" */
export const intero = (x: number): string => String(tondo(x))

/** f"{x:.{nd}f}" (Python and toFixed agree away from exact halves; the halves of the panel's 2 decimals are not exact floats). */
export const num = (x: number | null | undefined, nd = 2): string => (x == null ? '-' : nd === 0 ? intero(x) : x.toFixed(nd))

/** A price at the tick: 29416.25, 29008, 4022.4 (desktop_trader._p). */
export const prezzo = (x: number | null | undefined): string => (x == null ? '-' : x.toFixed(2).replace(/0+$/, '').replace(/\.$/, ''))

/** A frequency that would read 0% or 100% (also by rounding: 249/250): said as "k su n" (D8). */
export const estremo = (f: Frequenza): boolean => Boolean(f.n) && f.p != null && [0, 100].includes(tondo(f.p * 100))

/** D8: "73% (22/30 ±16)", "21 su 21" at the extremes, "-" without a frequency. */
export function p(f: Frequenza | null | undefined): string {
  if (!f || f.p == null) return '-'
  if (estremo(f)) return `${f.k} su ${f.n}`
  return `${tondo(f.p * 100)}% (${f.k}/${f.n}${f.margine == null ? '' : ` ±${tondo(f.margine * 100)}`})`
}

/** "mediana (q1-q3)", "n/d" without cases. */
export const quart = (q: Quartili | null | undefined, nd = 0): string => (q ? `${num(q.mediana, nd)} (${num(q.q1, nd)}-${num(q.q3, nd)})` : 'n/d')

const ROMA = new Intl.DateTimeFormat('it-IT', { timeZone: 'Europe/Rome', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' })

/** HH:MM in Rome time of a Date / epoch ms. */
export const oraRoma = (t: Date | number): string => ROMA.format(t)
