import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { act, render, renderHook, screen } from '@testing-library/react'
import type { ReactNode } from 'react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { scartoBusta, useFrequenze, useMemoria, useScenari } from '@/lib/api'
import { API_BASE } from '@/lib/config'
import * as tipi from '@/lib/tipi'
import { AvvisoFreschezza, etaCorrente } from '@/live/AvvisoFreschezza'
import { StatoLive } from '@/live/StatoLive'
import Stato from '@/pagine/Stato'
import frequenzeJson from '@/test/fixtures/frequenze.json'
import memoriaJson from '@/test/fixtures/memoria.json'
import scenariJson from '@/test/fixtures/scenari.json'

vi.mock('@/lib/tipi', async (importOriginal) => {
  const o = await importOriginal<typeof import('@/lib/tipi')>()
  return { ...o, validaScenari: vi.fn(o.validaScenari), validaFrequenze: vi.fn(o.validaFrequenze), validaMemoria: vi.fn(o.validaMemoria) }
})

const cliente = () => {
  const client = new QueryClient()
  const wrapper = ({ children }: { children: ReactNode }) => <QueryClientProvider client={client}>{children}</QueryClientProvider>
  return { client, wrapper }
}

const ok = (corpo: unknown, etag: string) => new Response(JSON.stringify(corpo), { status: 200, headers: { ETag: etag } })
const nonModificato = () => new Response(null, { status: 304 })
const intestazione = (init: RequestInit | undefined) => new Headers(init?.headers).get('If-None-Match')
const A = 'W/"scenari-A"'
const B = 'W/"scenari-B"'
const scenariB = { ...scenariJson, ricevuto: '2026-10-26T19:09:08Z', eta_s: 0, dati: { ...scenariJson.dati, generato: '2026-10-26T20:09:08+01:00' } }

afterEach(() => {
  vi.useRealTimers()
  vi.restoreAllMocks()
  vi.mocked(tipi.validaScenari).mockClear()
})

describe('richieste condizionali (ETag / 304)', () => {
  it('invia If-None-Match col valore giusto dal secondo giro, non al primo', async () => {
    vi.useFakeTimers()
    const viste: (string | null)[] = []
    vi.spyOn(globalThis, 'fetch').mockImplementation(async (_u, init) => {
      viste.push(intestazione(init))
      return viste.length === 1 ? ok(scenariJson, A) : nonModificato()
    })
    const { client, wrapper } = cliente()
    renderHook(() => useScenari(), { wrapper })
    await act(() => vi.advanceTimersByTimeAsync(31_000))
    expect(viste).toEqual([null, A, A])
    client.clear()
  })

  it('su 304 restituisce la stessa busta, senza validarla e senza ridisegnare', async () => {
    vi.useFakeTimers()
    let n = 0
    vi.spyOn(globalThis, 'fetch').mockImplementation(async () => (++n === 1 ? ok(scenariJson, A) : nonModificato()))
    const { client, wrapper } = cliente()
    let render_ = 0
    const { result } = renderHook(() => { render_ += 1; return useScenari() }, { wrapper })
    await act(() => vi.advanceTimersByTimeAsync(0))
    const prima = result.current.data
    expect(prima?.dati?.principale.strumento).toBe('MGC')
    const resi = render_
    const validazioni = vi.mocked(tipi.validaScenari).mock.calls.length
    await act(() => vi.advanceTimersByTimeAsync(46_000))
    expect(n).toBe(4)
    expect(vi.mocked(tipi.validaScenari).mock.calls.length).toBe(validazioni)
    expect(result.current.data).toBe(prima)
    expect(render_).toBe(resi)
    client.clear()
  })

  it('un dato nuovo (200 con ETag B) compare entro un giro, senza ricaricare', async () => {
    vi.useFakeTimers()
    let n = 0
    vi.spyOn(globalThis, 'fetch').mockImplementation(async (_u, init) => {
      n += 1
      if (n === 1) return ok(scenariJson, A)
      if (n <= 4) return nonModificato()
      if (n === 5) {
        expect(intestazione(init)).toBe(A)
        return ok(scenariB, B)
      }
      expect(intestazione(init)).toBe(B)
      return nonModificato()
    })
    const { client, wrapper } = cliente()
    const { result } = renderHook(() => useScenari(), { wrapper })
    await act(() => vi.advanceTimersByTimeAsync(46_000))
    expect(result.current.data?.ricevuto).toBe('2026-10-26T19:08:08Z')
    await act(() => vi.advanceTimersByTimeAsync(15_000))
    expect(result.current.data?.ricevuto).toBe('2026-10-26T19:09:08Z')
    expect(result.current.data?.dati?.generato).toBe('2026-10-26T20:09:08+01:00')
    // la busta nuova e' quella registrata (ETag B e scarto), non una copia
    expect(scartoBusta(result.current.data)).not.toBeNull()
    const nuova = result.current.data
    await act(() => vi.advanceTimersByTimeAsync(15_000))
    expect(n).toBe(6)
    expect(result.current.data).toBe(nuova)
    expect(scartoBusta(result.current.data)).not.toBeNull()
    client.clear()
  })

  it('un 304 senza ETag in memoria e un errore "risposta inattesa", riprovato al giro dopo', async () => {
    vi.useFakeTimers()
    let n = 0
    vi.spyOn(globalThis, 'fetch').mockImplementation(async (_u, init) => {
      n += 1
      if (n === 1) {
        expect(intestazione(init)).toBeNull()
        return nonModificato()
      }
      return ok(scenariJson, A)
    })
    const { client, wrapper } = cliente()
    const { result } = renderHook(() => useScenari(), { wrapper })
    await act(() => vi.advanceTimersByTimeAsync(1_000))
    expect(result.current.isError).toBe(true)
    expect(String(result.current.error)).toMatch(/inattesa/)
    expect(n).toBe(1)
    await act(() => vi.advanceTimersByTimeAsync(15_000))
    expect(n).toBe(2)
    expect(result.current.isError).toBe(false)
    expect(result.current.data?.dati?.principale.strumento).toBe('MGC')
    client.clear()
  })

  it('cadenza 15 s per scenari, frequenze e memoria; un solo giro per canale (nessun ritentativo sui 304)', async () => {
    vi.useFakeTimers()
    const per: Record<string, number> = { scenari: 0, frequenze: 0, memoria: 0 }
    vi.spyOn(globalThis, 'fetch').mockImplementation(async (u) => {
      const k = String(u).split('/live/')[1]
      per[k] += 1
      const corpo = { scenari: scenariJson, frequenze: frequenzeJson, memoria: memoriaJson }[k]
      return per[k] === 1 ? ok(corpo, `W/"${k}-1"`) : nonModificato()
    })
    const { client, wrapper } = cliente()
    renderHook(() => ({ s: useScenari(), f: useFrequenze(), m: useMemoria() }), { wrapper })
    await act(() => vi.advanceTimersByTimeAsync(31_000))
    expect(per).toEqual({ scenari: 3, frequenze: 3, memoria: 3 })
    client.clear()
  })

  it('nessuna richiesta a host diversi dall API', async () => {
    vi.useFakeTimers()
    const url: string[] = []
    vi.spyOn(globalThis, 'fetch').mockImplementation(async (u) => {
      url.push(String(u))
      return url.length === 1 ? ok(scenariJson, A) : nonModificato()
    })
    const { client, wrapper } = cliente()
    renderHook(() => useScenari(), { wrapper })
    await act(() => vi.advanceTimersByTimeAsync(31_000))
    expect(url).toHaveLength(3)
    expect(url.every((u) => u === `${API_BASE}/live/scenari`)).toBe(true)
    client.clear()
  })
})

describe('eta del dato dopo un 304', () => {
  it('0 s al 200; dopo due giri da 304 e 31 s di orologio l eta e 31 s (da ricevuto + orologio locale)', async () => {
    vi.useFakeTimers()
    let n = 0
    vi.spyOn(globalThis, 'fetch').mockImplementation(async () => (++n === 1 ? ok(scenariJson, A) : nonModificato()))
    const { client, wrapper } = cliente()
    const { result } = renderHook(() => useScenari(), { wrapper })
    await act(() => vi.advanceTimersByTimeAsync(0))
    expect(etaCorrente(result.current, Date.now())).toBe(0)
    await act(() => vi.advanceTimersByTimeAsync(31_000))
    expect(n).toBe(3)
    expect(etaCorrente(result.current, Date.now())).toBe(31)
    client.clear()
  })

  it('l eta non dipende dall orologio del PC: ricevuto lontano dall ora locale, eta_s 7 -> 7 s al 200', async () => {
    vi.useFakeTimers()
    vi.setSystemTime(new Date('2030-01-01T00:00:00Z'))
    vi.spyOn(globalThis, 'fetch').mockImplementation(async () => ok({ ...scenariJson, eta_s: 7 }, A))
    const { client, wrapper } = cliente()
    const { result } = renderHook(() => useScenari(), { wrapper })
    await act(() => vi.advanceTimersByTimeAsync(0))
    expect(etaCorrente(result.current, Date.now())).toBe(7)
    expect(etaCorrente(result.current, Date.now() + 10_000)).toBe(17)
    client.clear()
  })

  it('StatoLive mostra l eta che avanza anche con i 304 (nessun nuovo dataUpdatedAt utile)', async () => {
    vi.useFakeTimers()
    let n = 0
    vi.spyOn(globalThis, 'fetch').mockImplementation(async () => (++n === 1 ? ok(scenariJson, A) : nonModificato()))
    const { client, wrapper } = cliente()
    function Pagina() {
      const q = useScenari()
      return <StatoLive q={q} />
    }
    render(<Pagina />, { wrapper })
    await act(() => vi.advanceTimersByTimeAsync(0))
    expect(screen.getByText(/ricevuto 0 s fa/)).toBeInTheDocument()
    await act(() => vi.advanceTimersByTimeAsync(35_000))
    expect(screen.getByText(/ricevuto 35 s fa/)).toBeInTheDocument()
    client.clear()
  })

  it('AvvisoFreschezza scatta alla soglia sull eta calcolata dopo i 304', async () => {
    vi.useFakeTimers()
    let n = 0
    vi.spyOn(globalThis, 'fetch').mockImplementation(async () => (++n === 1 ? ok(scenariJson, A) : nonModificato()))
    const { client, wrapper } = cliente()
    function Pagina() {
      return <AvvisoFreschezza canale="Scenari" q={useScenari()} sogliaS={60} />
    }
    render(<Pagina />, { wrapper })
    await act(() => vi.advanceTimersByTimeAsync(55_000))
    expect(screen.queryByRole('status')).toBeNull()
    await act(() => vi.advanceTimersByTimeAsync(10_000))
    expect(screen.getByRole('status')).toHaveTextContent('Motore spento o scollegato da 1 minuto')
    client.clear()
  })
})

describe('/stato con richieste condizionali', () => {
  it('invia If-None-Match e l eta cresce dopo i 304', async () => {
    vi.useFakeTimers()
    const viste: (string | null)[] = []
    vi.spyOn(globalThis, 'fetch').mockImplementation(async (u, init) => {
      const k = String(u).split('/live/')[1]
      viste.push(intestazione(init))
      return viste.length <= 3 ? ok({ ...scenariJson, dati: { ...scenariJson.dati, k } }, `W/"${k}-1"`) : nonModificato()
    })
    const { client, wrapper } = cliente()
    render(<Stato />, { wrapper })
    await act(() => vi.advanceTimersByTimeAsync(0))
    expect(screen.getAllByText('0 s')).toHaveLength(3)
    await act(() => vi.advanceTimersByTimeAsync(31_000))
    expect(viste.slice(3).every((v) => v?.endsWith('-1"'))).toBe(true)
    expect(screen.getAllByText('30 s')).toHaveLength(3)
    act(() => client.clear())
  })
})
