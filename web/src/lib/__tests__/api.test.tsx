import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { renderHook } from '@testing-library/react'
import type { ReactNode } from 'react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { precaricaLive, TIMEOUT_MS, useFrequenze, useScenari } from '@/lib/api'
import { avvisi } from '@/live/AvvisoFreschezza'
import frequenzeJson from '@/test/fixtures/frequenze.json'
import scenariJson from '@/test/fixtures/scenari.json'

const cliente = () => {
  const client = new QueryClient()
  const wrapper = ({ children }: { children: ReactNode }) => <QueryClientProvider client={client}>{children}</QueryClientProvider>
  return { client, wrapper }
}

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

  it('browser senza AbortSignal.any (Safari < 17.4): la richiesta parte lo stesso e carica', async () => {
    const any = AbortSignal.any
    // @ts-expect-error -- an older browser without the API
    delete AbortSignal.any
    try {
      const chiamate: (AbortSignal | null | undefined)[] = []
      vi.spyOn(globalThis, 'fetch').mockImplementation(async (_u, init) => {
        chiamate.push(init?.signal)
        return new Response(JSON.stringify(scenariJson), { status: 200 })
      })
      const { client, wrapper } = cliente()
      const { result } = renderHook(() => useScenari(), { wrapper })
      await vi.waitFor(() => expect(result.current.data?.dati?.principale.strumento).toBe('MGC'))
      expect(chiamate[0]).toBeInstanceOf(AbortSignal)
      client.clear()
    } finally {
      AbortSignal.any = any
    }
  })

  it('browser senza AbortSignal.any: il timeout di 20 s vale lo stesso', async () => {
    const any = AbortSignal.any
    // @ts-expect-error -- an older browser without the API
    delete AbortSignal.any
    try {
      vi.useFakeTimers()
      vi.spyOn(globalThis, 'fetch').mockImplementation((_u, init) => new Promise((_, rifiuta) => {
        init?.signal?.addEventListener('abort', () => rifiuta(init.signal!.reason))
      }))
      const { client, wrapper } = cliente()
      const { result } = renderHook(() => useScenari(), { wrapper })
      await vi.advanceTimersByTimeAsync(19_000)
      expect(result.current.isError).toBe(false)
      await vi.advanceTimersByTimeAsync(2_000)
      expect(result.current.isError).toBe(true)
      client.clear()
    } finally {
      AbortSignal.any = any
    }
  })

  it('browser senza AbortSignal.any: dopo una risposta riuscita il timer di riserva e azzerato (nessun abort 20 s dopo)', async () => {
    const any = AbortSignal.any
    // @ts-expect-error -- an older browser without the API
    delete AbortSignal.any
    try {
      vi.useFakeTimers()
      const segnali: AbortSignal[] = []
      vi.spyOn(globalThis, 'fetch').mockImplementation(async (_u, init) => {
        segnali.push(init!.signal!)
        return new Response(JSON.stringify(scenariJson), { status: 200 })
      })
      const { client, wrapper } = cliente()
      const { result } = renderHook(() => useScenari(), { wrapper })
      await vi.advanceTimersByTimeAsync(0)
      expect(result.current.data?.dati?.principale.strumento).toBe('MGC')
      await vi.advanceTimersByTimeAsync(TIMEOUT_MS + 1_000)
      expect(segnali[0].aborted).toBe(false)
      client.clear()
    } finally {
      AbortSignal.any = any
    }
  })

  it('precaricaLive: le due richieste partono subito e la pagina trova i dati senza un altra attesa', async () => {
    const url: string[] = []
    vi.spyOn(globalThis, 'fetch').mockImplementation(async (u) => {
      url.push(String(u))
      return new Response(JSON.stringify(String(u).endsWith('/scenari') ? scenariJson : frequenzeJson), { status: 200 })
    })
    const { client, wrapper } = cliente()
    precaricaLive(client)
    expect(url.map((u) => u.split('/live/')[1])).toEqual(['scenari', 'frequenze'])
    await vi.waitFor(() => expect(client.getQueryData(['live', 'frequenze'])).toBeDefined())
    const { result } = renderHook(() => useScenari(), { wrapper })
    expect(result.current.data?.dati?.principale.strumento).toBe('MGC')
    client.clear()
  })

  it('frequenze: un errore isolato si riprova dopo 3 s e non accende l avviso', async () => {
    vi.useFakeTimers()
    let n = 0
    vi.spyOn(globalThis, 'fetch').mockImplementation(async () => {
      n += 1
      if (n === 1) throw new TypeError('rete')
      return new Response(JSON.stringify(frequenzeJson), { status: 200 })
    })
    const { client, wrapper } = cliente()
    const { result } = renderHook(() => useFrequenze(), { wrapper })
    await vi.advanceTimersByTimeAsync(3_500)
    expect(n).toBe(2)
    expect(result.current.isError).toBe(false)
    expect(result.current.data?.dati?.principale.strumento).toBe('MGC')
    client.clear()
  })
})
