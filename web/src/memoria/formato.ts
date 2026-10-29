// Formattazione soltanto (nessun calcolo): data e ora di Roma come nel resto del sito (Intl con Europe/Rome).
const ROMA = new Intl.DateTimeFormat('it-IT', {
  timeZone: 'Europe/Rome', day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', hourCycle: 'h23',
})

/** "29/10/2026 11:03" in ora di Roma di un istante ISO; "-" se manca o non e' una data. */
export function dataOraRoma(iso: string | null | undefined): string {
  const t = iso ? Date.parse(iso) : NaN
  if (!Number.isFinite(t)) return '-'
  const p = Object.fromEntries(ROMA.formatToParts(t).map((x) => [x.type, x.value]))
  return `${p.day}/${p.month}/${p.year} ${p.hour}:${p.minute}`
}

/** "2026-10-29" -> "29/10/2026" (solo riordino delle parti); un altro formato resta com'e'. */
export const dataItaliana = (iso: string | null | undefined): string => {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso ?? '')
  return m ? `${m[3]}/${m[2]}/${m[1]}` : (iso ?? '-')
}
