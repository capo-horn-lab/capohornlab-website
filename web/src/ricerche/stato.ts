/** Motore acceso fino a 60 s dall'ultimo invio, in ritardo fino a 180 s, spento oltre (o senza dati). */
export const SOGLIA_ACCESO_S = 60
export const SOGLIA_SPENTO_S = 180

export type StatoMotore = 'acceso' | 'in ritardo' | 'spento'

export function statoMotore(etaS: number | null): StatoMotore {
  if (etaS === null || !Number.isFinite(etaS) || etaS > SOGLIA_SPENTO_S) return 'spento'
  return etaS <= SOGLIA_ACCESO_S ? 'acceso' : 'in ritardo'
}
