// The two live channels, polled: scenari (bars, tree, levels) every 15 s, frequenze (panel tables, levels' k/n) every 60 s.
// A request gives up after 20 s (a stalled one would otherwise block every later poll: TanStack reuses the request in flight);
// on a failed refresh TanStack keeps the last data (isError + dataUpdatedAt/errorUpdatedAt say when). No retry: the next poll
// is the retry, and the failure shows at once.
import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { API_BASE } from '@/lib/config'
import { validaFrequenze, validaScenari } from '@/lib/tipi'

export const TIMEOUT_MS = 20_000

async function carica<T>(chiave: 'scenari' | 'frequenze', valida: (x: unknown) => T, signal: AbortSignal): Promise<T> {
  const r = await fetch(`${API_BASE}/live/${chiave}`, { signal: AbortSignal.any([signal, AbortSignal.timeout(TIMEOUT_MS)]), cache: 'no-store' })
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
    retry: false,
  })
