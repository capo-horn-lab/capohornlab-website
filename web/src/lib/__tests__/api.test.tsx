import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { renderHook } from '@testing-library/react'
import type { ReactNode } from 'react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { TIMEOUT_MS, useScenari } from '@/lib/api'
import { avvisi } from '@/live/AvvisoFreschezza'

describe('api: timeout delle richieste (Important 4)', () => {
  afterEach(() => {
    vi.useRealTimers()
    vi.restoreAllMocks()
  })

  it('una richiesta che non risponde fallisce dopo 20 s e la pagina dice "Aggiornamento fallito"', async () => {
    vi.useFakeTimers()
    // jsdom's AbortSignal.timeout runs on real timers: the same signal on the faked clock
    vi.spyOn(AbortSignal, 'timeout').mockImplementation((ms) => {
      const c = new AbortController()
      setTimeout(() => c.abort(new DOMException('timeout', 'TimeoutError')), ms)
      return c.signal
    })
    vi.spyOn(globalThis, 'fetch').mockImplementation((_u, init) => new Promise((_, rifiuta) => {
      init?.signal?.addEventListener('abort', () => rifiuta(init.signal!.reason))
    }))
    const client = new QueryClient()
    const wrapper = ({ children }: { children: ReactNode }) => <QueryClientProvider client={client}>{children}</QueryClientProvider>
    const { result } = renderHook(() => useScenari(), { wrapper })
    expect(TIMEOUT_MS).toBe(20_000)
    await vi.advanceTimersByTimeAsync(19_000)
    expect(result.current.isError).toBe(false)
    await vi.advanceTimersByTimeAsync(2_000)
    expect(result.current.isError).toBe(true)
    expect(avvisi(result.current, 60)[0]).toMatch(/^Aggiornamento fallito alle \d\d:\d\d; nessun caricamento riuscito finora$/)
    client.clear()
  })
})
