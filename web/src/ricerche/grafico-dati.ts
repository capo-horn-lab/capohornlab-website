// Dati dei grafici: un valore mancante (null) non e' zero. Non si disegna mai un valore che la prova non contiene.
import { colonnaValori, type Dati } from './modello'

const numero = (x: unknown): number | null => (typeof x === 'number' && Number.isFinite(x) ? x : null)

export interface PuntiSerie {
  colonna: number
  punti: { anno: string; valore: number }[]
  /** Anni senza valore: con almeno uno la serie non si disegna come linea (la linea unirebbe due punti attraverso il buco). */
  buchi: number
}

export function puntiSerie(dati: Dati): PuntiSerie {
  const colonna = colonnaValori(dati)
  const punti: PuntiSerie['punti'] = []
  let buchi = 0
  for (const r of dati.righe) {
    const v = colonna < 0 ? null : numero(r[colonna])
    if (v === null) buchi += 1
    else punti.push({ anno: String(r[0]), valore: v })
  }
  return { colonna, punti, buchi }
}

export interface BarreTabella {
  colonna: number
  barre: { etichetta: string; valore: number }[]
  /** Righe con valore nullo: senza barra. */
  omesse: number
  unitaMiste: boolean
}

export function barreTabella(dati: Dati): BarreTabella {
  const colonna = colonnaValori(dati)
  const iEtichetta = dati.colonne.indexOf('r') >= 0 ? dati.colonne.indexOf('r') : 0
  const iUnita = dati.colonne.indexOf('u')
  const barre: BarreTabella['barre'] = []
  let omesse = 0
  for (const r of dati.righe) {
    const v = colonna < 0 ? null : numero(r[colonna])
    if (v === null) omesse += 1
    else barre.push({ etichetta: String(r[iEtichetta]), valore: v })
  }
  const unita = new Set(dati.righe.map((r) => (iUnita < 0 ? '' : String(r[iUnita] ?? ''))))
  return { colonna, barre, omesse, unitaMiste: unita.size > 1 }
}

/** Valori della colonna numerica di una serie per la sparkline: i null saltano il punto, non diventano 0. */
export function valoriSerie(dati: Dati): number[] {
  const c = colonnaValori(dati)
  return c < 0 ? [] : dati.righe.map((r) => numero(r[c])).filter((v): v is number => v !== null)
}
