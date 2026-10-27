// The two live channels, polled: scenari (bars, tree, levels) every 15 s, frequenze (panel tables, levels' k/n) every 60 s.
// A request gives up after 20 s (a stalled one would otherwise block every later poll: TanStack reuses the request in flight);
// on a failed refresh TanStack keeps the last data (isError + dataUpdatedAt/errorUpdatedAt say when). Scenari: no retry, the
// next poll (15 s) is the retry. Frequenze: one retry after 3 s, so a single blip does not show a failure for a whole minute
// (each attempt has its own 20 s: a stalled channel still shows within 43 s, under both freshness limits).
import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { API_BASE } from '@/lib/config'
import { validaFrequenze, validaScenari } from '@/lib/tipi'

export const TIMEOUT_MS = 20_000

/** TanStack's signal plus the timeout; without AbortSignal.any (Safari < 17.4, Firefox < 124) a local controller does the same. */
function segnale(signal: AbortSignal): AbortSignal {
  if (typeof AbortSignal.any === 'function' && typeof AbortSignal.timeout === 'function') return AbortSignal.any([signal, AbortSignal.timeout(TIMEOUT_MS)])
  const c = new AbortController()
  const t = setTimeout(() => c.abort(new DOMException('timeout', 'TimeoutError')), TIMEOUT_MS)
  signal.addEventListener('abort', () => c.abort(signal.reason), { once: true })
  c.signal.addEventListener('abort', () => clearTimeout(t), { once: true })
  return c.signal
}

async function carica<T>(chiave: 'scenari' | 'frequenze', valida: (x: unknown) => T, signal: AbortSignal): Promise<T> {
  const r = await fetch(`${API_BASE}/live/${chiave}`, { signal: segnale(signal), cache: 'no-store' })
  if (!r.ok) throw new Error(`HTTP ${r.status}`)
  return valida(await r.json())
}

export const useScenari = () =>
  useQuery({
    queryKey: ['live', 'scenari'],
    queryFn: ({ signal }) => carica('scenari', validaScenari, signal),
    refetchInterval: 15_000,
    placeholderData: keepPreviousData,
    retry: false,
  })

export const useFrequenze = () =>
  useQuery({
    queryKey: ['live', 'frequenze'],
    queryFn: ({ signal }) => carica('frequenze', validaFrequenze, signal),
    refetchInterval: 60_000,
    placeholderData: keepPreviousData,
    retry: 1,
    retryDelay: 3000,
  })
