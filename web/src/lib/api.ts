// The live channels, polled every 15 s each: scenari (bars, tree, levels), frequenze (panel tables, levels' k/n), memoria.
// The poll is cheap because it is conditional: every 200 carries an ETag (W/"<channel>-<ricevuto>"), the next request sends it
// back as If-None-Match and, when nothing new arrived, the server answers 304 with no body. The ETag and the validated envelope
// of the last 200 are kept per query key (the envelope is the query's data; its ETag and clock offset sit in a WeakMap keyed by
// the envelope). On a 304 the same envelope object is returned: it is not validated again and, with structuralSharing off and
// notifyOnChangeProps limited to data/error, nobody re-renders. A new 200 (new ETag) replaces it and the page shows it within
// one poll. A 304 with no envelope in memory should not happen: it is an error ("risposta inattesa") and the next poll retries.
// The age of the data is not the envelope's eta_s (frozen at the last 200) but derived from `ricevuto` plus the local clock, with
// the offset measured at the 200 (see etaCorrente), so it does not depend on the PC's clock being right.
// A request gives up after 20 s (a stalled one would otherwise block every later poll: TanStack reuses the request in flight);
// on a failed refresh TanStack keeps the last data (isError + dataUpdatedAt/errorUpdatedAt say when). Scenari: no retry, the
// next poll (15 s) is the retry. Frequenze and memoria: one retry after 3 s, so a single blip does not show a failure for a
// whole poll (each attempt has its own 20 s: a stalled channel still shows within 43 s, under every freshness limit). No retry
// on a 304 (it is a success) nor, for memoria, on a payload the site cannot show.
import { keepPreviousData, type QueryClient, type QueryKey, queryOptions, useQuery } from '@tanstack/react-query'
import { API_BASE } from '@/lib/config'
import { RispostaNonValida, validaFrequenze, validaMemoria, validaScenari } from '@/lib/tipi'

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

/** What is known of an envelope from its 200: the ETag to send back, and the offset between the local clock and the server's
 * (local now at the response minus ricevuto + eta_s; null when the envelope carries no age). */
interface MetaBusta {
  etag: string | null
  scarto: number | null
}
const metaBusta = new WeakMap<object, MetaBusta>()

/** Offset of the local clock from the server's, measured when `busta` arrived; null if unknown. */
export const scartoBusta = (busta: object | undefined): number | null => (busta ? (metaBusta.get(busta)?.scarto ?? null) : null)

/** Conditional GET of one channel. The previous envelope is the query's data in `client` under `chiaveQuery`. */
export async function carica<T extends object>(
  client: QueryClient,
  chiaveQuery: QueryKey,
  canale: 'scenari' | 'frequenze' | 'memoria',
  valida: (x: unknown) => T,
  signal: AbortSignal,
): Promise<T> {
  const prima = client.getQueryData<T>(chiaveQuery)
  const etagPrima = prima ? metaBusta.get(prima)?.etag : null
  const s = segnale(signal)
  try {
    const r = await fetch(`${API_BASE}/live/${canale}`, {
      signal: s.signal,
      cache: 'no-store',
      ...(etagPrima ? { headers: { 'If-None-Match': etagPrima } } : {}),
    })
    if (r.status === 304) {
      if (!prima || !etagPrima) throw new Error('Risposta inattesa (304 senza dati in memoria)')
      return prima
    }
    if (!r.ok) throw new Error(`HTTP ${r.status}`)
    const arrivo = Date.now()
    const busta = valida(await r.json())
    const { ricevuto, eta_s } = busta as { ricevuto?: unknown; eta_s?: unknown }
    const t = typeof ricevuto === 'string' ? Date.parse(ricevuto) : NaN
    const scarto = Number.isFinite(t) && typeof eta_s === 'number' ? arrivo - (t + eta_s * 1000) : null
    metaBusta.set(busta, { etag: r.headers?.get('ETag') ?? null, scarto })
    return busta
  } finally {
    s.fine()
  }
}

/** Options every channel shares: a 304 hands back the same envelope, so only data/error changes re-render (the age is the
 * components' own clock), and a new envelope is never swapped for a deep-equal old one (its clock offset would be lost). */
export const OPZIONI_COMUNI = {
  refetchInterval: 15_000,
  structuralSharing: false,
  notifyOnChangeProps: ['data', 'error', 'isError', 'errorUpdatedAt'] as Array<'data' | 'error' | 'isError' | 'errorUpdatedAt'>,
}

/** Data younger than this are not fetched again when the page mounts (staleTime stays 0, so the polls and a focus still
 * refetch): on load, one request per channel, the prefetch's, instead of the prefetch plus the mount's. */
export const APPENA_LETTO_MS = 5_000
const vecchiAlMontaggio = (q: { state: { dataUpdatedAt: number } }) => Date.now() - q.state.dataUpdatedAt > APPENA_LETTO_MS

const opzioniScenari = queryOptions({
  queryKey: ['live', 'scenari'],
  queryFn: ({ signal, client, queryKey }) => carica(client, queryKey, 'scenari', validaScenari, signal),
  ...OPZIONI_COMUNI,
  refetchOnMount: vecchiAlMontaggio,
  placeholderData: keepPreviousData,
  retry: false,
})

const opzioniFrequenze = queryOptions({
  queryKey: ['live', 'frequenze'],
  queryFn: ({ signal, client, queryKey }) => carica(client, queryKey, 'frequenze', validaFrequenze, signal),
  ...OPZIONI_COMUNI,
  refetchOnMount: vecchiAlMontaggio,
  placeholderData: keepPreviousData,
  retry: 1,
  retryDelay: 3000,
})

// Memoria del mercato: the publisher sends at least every 300 s. Like frequenze: one retry after 3 s,
// except for a payload the site cannot show (the same payload would come back: the next poll is the retry).
const opzioniMemoria = queryOptions({
  queryKey: ['live', 'memoria'],
  queryFn: ({ signal, client, queryKey }) => carica(client, queryKey, 'memoria', validaMemoria, signal),
  ...OPZIONI_COMUNI,
  refetchOnMount: vecchiAlMontaggio,
  placeholderData: keepPreviousData,
  retry: (tentativi, errore) => tentativi < 1 && !(errore instanceof RispostaNonValida),
  retryDelay: 3000,
})

export const useScenari = () => useQuery(opzioniScenari)
export const useFrequenze = () => useQuery(opzioniFrequenze)
export const useMemoria = () => useQuery(opzioniMemoria)

/** On the live page the two requests start with the entry, while the page's chunk is still loading (not after it). */
export function precaricaLive(client: QueryClient) {
  void client.prefetchQuery(opzioniScenari)
  void client.prefetchQuery(opzioniFrequenze)
}
