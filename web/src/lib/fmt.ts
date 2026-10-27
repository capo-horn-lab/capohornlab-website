// D8 formatting, as the Trader (desktop_trader._pct/_estremo/_p) and the panel (desktop_tools._num/_quart): Python's rounding
// (round half to even on the exact float) so the site prints the same digits as the app; anything not a finite number prints "-".

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

export const finito = (x: unknown): x is number => typeof x === 'number' && Number.isFinite(x)

/** Python's round(x) on a float: halves go to the even neighbour (7728.5 -> 7728, 0.125*100 -> 12). */
function tondo(x: number): number {
  const r = Math.round(x)
  return Math.abs(x - Math.trunc(x)) === 0.5 && r % 2 !== 0 ? r - 1 : r
}

/**
 * f"{x:.{nd}f}". toFixed rounds the exact binary value like Python, except on an exact tie (0.125, 52.125, 7728.5), which it
 * rounds up where Python goes to the even digit: the tie is read from the exact expansion (toFixed with 30 more digits).
 */
function fisso(x: number, nd: number): string {
  const a = Math.abs(x)
  const lungo = a.toFixed(Math.min(100, nd + 30))
  const punto = lungo.indexOf('.')
  const tenuto = lungo.slice(0, nd ? punto + 1 + nd : punto)
  const pari = /^50*$/.test(lungo.slice(punto + 1 + nd)) && Number(tenuto.at(-1)) % 2 === 0
  return (x < 0 ? '-' : '') + (pari ? tenuto : a.toFixed(nd))
}

/** f"{x:.0f}" */
export const intero = (x: unknown): string => (finito(x) ? fisso(x, 0) : '-')

/** f"{x:.{nd}f}" (desktop_tools._num), "-" without a number. */
export const num = (x: unknown, nd = 2): string => (finito(x) ? fisso(x, nd) : '-')

/** A price at the tick: 29416.25, 29008, 4022.4 (desktop_trader._p). */
export const prezzo = (x: unknown): string => (finito(x) ? fisso(x, 2).replace(/0+$/, '').replace(/\.$/, '') : '-')

/** A frequency that would read 0% or 100% (also by rounding: 249/250): said as "k su n" (D8). */
export const estremo = (f: Frequenza): boolean => Boolean(f.n) && finito(f.p) && [0, 100].includes(tondo(f.p * 100))

/** D8: "73% (22/30 ±16)", "21 su 21" at the extremes, "-" without a frequency. */
export function p(f: Frequenza | null | undefined): string {
  if (!f || !finito(f.p)) return '-'
  if (estremo(f)) return `${f.k} su ${f.n}`
  return `${tondo(f.p * 100)}% (${f.k}/${f.n}${finito(f.margine) ? ` ±${tondo(f.margine * 100)}` : ''})`
}

/** "mediana (q1-q3)", "n/d" without cases. */
export const quart = (q: Quartili | null | undefined, nd = 0): string => (q ? `${num(q.mediana, nd)} (${num(q.q1, nd)}-${num(q.q3, nd)})` : 'n/d')

const ROMA = new Intl.DateTimeFormat('it-IT', { timeZone: 'Europe/Rome', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' })

/** HH:MM in Rome time of a Date / epoch ms. */
export const oraRoma = (t: Date | number): string => ROMA.format(t)
