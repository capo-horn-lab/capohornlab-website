// The two live channels, polled: scenari (bars, tree, levels) every 15 s, frequenze (panel tables, levels' k/n) every 60 s.
// A request gives up after 20 s (a stalled one would otherwise block every later poll: TanStack reuses the request in flight);
// on a failed refresh TanStack keeps the last data (isError + dataUpdatedAt/errorUpdatedAt say when). Scenari: no retry, the
// next poll (15 s) is the retry. Frequenze: one retry after 3 s, so a single blip does not show a failure for a whole minute
// (each attempt has its own 20 s: a stalled channel still shows within 43 s, under both freshness limits).
import { keepPreviousData, type QueryClient, queryOptions, useQuery } from '@tanstack/react-query'
import { API_BASE } from '@/lib/config'
import { validaFrequenze, validaScenari } from '@/lib/tipi'

export const TIMEOUT_MS = 20_000

/** TanStack's signal plus the timeout; without AbortSignal.any (Safari < 17.4, Firefox < 124) a local controller does the same,
 * and `fine` clears its timer once the request is over (success or failure), so no timer outlives the request. */
function segnale(signal: AbortSignal): { signal: AbortSignal; fine: () => void } {
  if (typeof AbortSignal.any === 'function' && typeof AbortSignal.timeout === 'function')
    return { signal: AbortSignal.any([signal, AbortSignal.timeout(TIMEOUT_MS)]), fine: () => {} }
  const c = new AbortController()
  const t = setTimeout(() => c.abort(new DOMException('timeout', 'TimeoutError')), TIMEOUT_MS)
  signal.addEventListener('abort', () => c.abort(signal.reason), { once: true })
  return { signal: c.signal, fine: () => clearTimeout(t) }
}

async function carica<T>(chiave: 'scenari' | 'frequenze', valida: (x: unknown) => T, signal: AbortSignal): Promise<T> {
  const s = segnale(signal)
  try {
    const r = await fetch(`${API_BASE}/live/${chiave}`, { signal: s.signal, cache: 'no-store' })
    if (!r.ok) throw new Error(`HTTP ${r.status}`)
    return valida(await r.json())
  } finally {
    s.fine()
  }
}

const opzioniScenari = queryOptions({
  queryKey: ['live', 'scenari'],
  queryFn: ({ signal }) => carica('scenari', validaScenari, signal),
  refetchInterval: 15_000,
  placeholderData: keepPreviousData,
  retry: false,
})

const opzioniFrequenze = queryOptions({
  queryKey: ['live', 'frequenze'],
  queryFn: ({ signal }) => carica('frequenze', validaFrequenze, signal),
  refetchInterval: 60_000,
  placeholderData: keepPreviousData,
  retry: 1,
  retryDelay: 3000,
})

export const useScenari = () => useQuery(opzioniScenari)
export const useFrequenze = () => useQuery(opzioniFrequenze)

/** On the live page the two requests start with the entry, while the page's chunk is still loading (not after it). */
export function precaricaLive(client: QueryClient) {
  void client.prefetchQuery(opzioniScenari)
  void client.prefetchQuery(opzioniFrequenze)
}
