/**
 * Soglie del dato "vecchio" per canale (design §4.2): scenari 60 s, frequenze 180 s, memoria 180 s. Oltre la soglia di spento del
 * canale dall'ultimo invio, o senza dati, il motore risulta spento: 180 s per scenari e frequenze (stessa soglia della fase 1),
 * 600 s per la memoria (il pubblicatore invia almeno ogni 300 s).
 */
export const SOGLIA_CANALE_S = { scenari: 60, frequenze: 180, memoria: 180 } as const
export const SOGLIA_SPENTO_CANALE_S = { scenari: 180, frequenze: 180, memoria: 600 } as const
export const SOGLIA_SPENTO_S = 180

export type StatoMotore = 'acceso' | 'in ritardo' | 'spento'

export function statoMotore(etaS: number | null, sogliaS: number = SOGLIA_CANALE_S.scenari, spentoS: number = SOGLIA_SPENTO_S): StatoMotore {
  if (etaS === null || !Number.isFinite(etaS) || etaS > spentoS) return 'spento'
  return etaS <= sogliaS ? 'acceso' : 'in ritardo'
}
