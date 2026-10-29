import type { GruppoVerdetto } from '@/lib/tipi'

export const DESCRITTIVO = 'DESCRITTIVO'
export const CONFERMATO = 'CONFERMATO'
export const NON_CONFERMATO = 'NON CONFERMATO'

/**
 * L'avviso fisso in testa alla pagina, vero in ogni stato del payload; i numeri sono conteggi dei verdetti (contare non e' calcolare).
 * (a) senza dati o con tutti i gruppi DESCRITTIVI: "tutti i gruppi sono DESCRITTIVI";
 * (b) nessun CONFERMATO ma qualche NON CONFERMATO: "N gruppi su M sono DESCRITTIVI, K NON CONFERMATI";
 * (c) almeno un CONFERMATO: "K gruppi su M CONFERMATI secondo la rubrica registrata (vedi tabella), N DESCRITTIVI[, J NON CONFERMATI]", senza indicazione operativa.
 * Ogni conteggio uguale a 1 concorda al singolare (gruppo, è, DESCRITTIVO, CONFERMATO, NON CONFERMATO).
 */
export function testoAvviso(verdetti?: Record<string, Pick<GruppoVerdetto, 'verdetto'>> | null): string {
  const tutti = Object.values(verdetti ?? {})
  const conta = (v: string) => tutti.filter((g) => g.verdetto === v).length
  const [descrittivi, confermati, nonConfermati] = [conta(DESCRITTIVO), conta(CONFERMATO), conta(NON_CONFERMATO)]
  const dati = 'Conteggi e verifiche descrivono dati già visti, non segnali'
  const uno = (n: number, singolare: string, plurale: string) => (n === 1 ? singolare : plurale)
  const descr = uno(descrittivi, 'DESCRITTIVO', 'DESCRITTIVI')
  const non = nonConfermati > 0 ? `, ${nonConfermati} ${uno(nonConfermati, 'NON CONFERMATO', 'NON CONFERMATI')}` : ''
  if (confermati > 0)
    return `Verifica statistica: ${confermati} ${uno(confermati, 'gruppo', 'gruppi')} su ${tutti.length} ${uno(confermati, 'CONFERMATO', 'CONFERMATI')} secondo la rubrica registrata (vedi tabella), ${descrittivi} ${descr}${non}. ${dati}: nessuna indicazione operativa.`
  const quali = descrittivi === tutti.length ? 'tutti i gruppi sono' : `${descrittivi} ${uno(descrittivi, 'gruppo', 'gruppi')} su ${tutti.length} ${uno(descrittivi, 'è', 'sono')}`
  return `Nessun valore predittivo dimostrato: ${quali} ${descr}${non}. ${dati}.`
}
