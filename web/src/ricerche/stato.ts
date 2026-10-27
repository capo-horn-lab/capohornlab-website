/**
 * Soglie del dato "vecchio" per canale (design §4.2): scenari 60 s, frequenze 180 s. Oltre 180 s dall'ultimo invio, o
 * senza dati, il motore risulta spento (stessa soglia della fase 1).
 */
export const SOGLIA_CANALE_S = { scenari: 60, frequenze: 180 } as const
export const SOGLIA_SPENTO_S = 180

export type StatoMotore = 'acceso' | 'in ritardo' | 'spento'

export function statoMotore(etaS: number | null, sogliaS: number = SOGLIA_CANALE_S.scenari): StatoMotore {
  if (etaS === null || !Number.isFinite(etaS) || etaS > SOGLIA_SPENTO_S) return 'spento'
  return etaS <= sogliaS ? 'acceso' : 'in ritardo'
}
