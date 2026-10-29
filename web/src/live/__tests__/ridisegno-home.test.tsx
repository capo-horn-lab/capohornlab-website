// The home (/, Frequenze live) with the conditional polls: the 304s of scenari and frequenze re-render nothing (not the page,
// not the tabs, not the chart), while the age in the status line keeps advancing with the clock; a new 200 (new ETag) re-renders
// the page within one poll. The render counts come from the real components wrapped in vi.fn (hooks run as usual).
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { act, render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import * as grafico from '@/live/GraficoLive'
import * as schede from '@/live/StrumentoTabs'
import Live from '@/pagine/Live'
import frequenzeJson from '@/test/fixtures/frequenze.json'
import scenariJson from '@/test/fixtures/scenari.json'

vi.mock('@/live/GraficoLive', async (importOriginal) => {
  const o = await importOriginal<typeof import('@/live/GraficoLive')>()
  return { ...o, GraficoLive: vi.fn(o.GraficoLive) }
})
vi.mock('@/live/StrumentoTabs', async (importOriginal) => {
  const o = await importOriginal<typeof import('@/live/StrumentoTabs')>()
  return { ...o, StrumentoTabs: vi.fn(o.StrumentoTabs) }
})
vi.mock('@/pagine/Live', async (importOriginal) => {
  const o = await importOriginal<typeof import('@/pagine/Live')>()
  return { ...o, default: vi.fn(o.default) }
})

const resi = () => ({
  pagina: vi.mocked(Live).mock.calls.length,
  schede: vi.mocked(schede.StrumentoTabs).mock.calls.length,
  grafico: vi.mocked(grafico.GraficoLive).mock.calls.length,
})
const ok = (corpo: unknown, etag: string) => new Response(JSON.stringify(corpo), { status: 200, headers: { ETag: etag } })
const nonModificato = () => new Response(null, { status: 304 })
const scenariNuovi = { ...scenariJson, ricevuto: '2026-10-26T19:09:08Z', eta_s: 0, dati: { ...scenariJson.dati, generato: '2026-10-26T20:09:08+01:00' } }

/** Virtual time in small steps until `cond` (the lazy chart chunk, the first-paint frame and the Suspense retry are promises
 * and faked timers, not one timer): at most `passi` x 25 ms, well under the first poll (15 s). */
async function finoA(cond: () => boolean, passi = 80) {
  for (let i = 0; i < passi && !cond(); i++) await act(() => vi.advanceTimersByTimeAsync(25))
  expect(cond()).toBe(true)
}

afterEach(() => {
  vi.useRealTimers()
  vi.restoreAllMocks()
  vi.unstubAllGlobals()
})

describe('home senza ridisegni sui 304', () => {
  it('tre giri da 304 su entrambi i canali: pagina, schede e grafico non si ridisegnano, l eta avanza; un 200 nuovo ridisegna entro un giro', async () => {
    vi.useFakeTimers({ toFake: ['setTimeout', 'clearTimeout', 'setInterval', 'clearInterval', 'setImmediate', 'clearImmediate', 'Date', 'requestAnimationFrame', 'cancelAnimationFrame'] })
    vi.spyOn(HTMLElement.prototype, 'clientWidth', 'get').mockReturnValue(900)
    vi.spyOn(HTMLElement.prototype, 'clientHeight', 'get').mockReturnValue(450)
    vi.stubGlobal('matchMedia', (q: string) => ({ matches: true, media: q, addEventListener() {}, removeEventListener() {} }))
    const per: Record<string, number> = { scenari: 0, frequenze: 0 }
    const etag: Record<string, string | null> = { scenari: null, frequenze: null }
    let nuovi = false
    vi.spyOn(globalThis, 'fetch').mockImplementation(async (u, init) => {
      const k = String(u).split('/live/')[1]
      per[k] += 1
      etag[k] = new Headers(init?.headers).get('If-None-Match')
      if (per[k] === 1) return ok(k === 'scenari' ? scenariJson : frequenzeJson, `W/"${k}-1"`)
      if (k === 'scenari' && nuovi) return ok(scenariNuovi, 'W/"scenari-2"')
      return nonModificato()
    })
    const client = new QueryClient()
    render(<QueryClientProvider client={client}><Live /></QueryClientProvider>)
    await finoA(() => resi().grafico > 0 && per.frequenze === 1 && screen.queryByText('STATO') != null)
    expect(screen.getByText(/calcolo delle 20:08 Roma · ricevuto 0 s fa/)).toBeInTheDocument()
    const prima = resi()

    await act(() => vi.advanceTimersByTimeAsync(46_000))
    expect(per).toEqual({ scenari: 4, frequenze: 4 })
    expect(etag).toEqual({ scenari: 'W/"scenari-1"', frequenze: 'W/"frequenze-1"' })
    expect(resi()).toEqual(prima)
    expect(screen.getByText(/ricevuto 4\d s fa/)).toBeInTheDocument()
    expect(screen.queryByRole('status')).toBeNull()

    nuovi = true
    await act(() => vi.advanceTimersByTimeAsync(15_000))
    expect(per.scenari).toBe(5)
    expect(screen.getByText(/calcolo delle 20:09 Roma · ricevuto \d s fa/)).toBeInTheDocument()
    const dopo = resi()
    expect(dopo.pagina).toBeGreaterThan(prima.pagina)
    expect(dopo.grafico).toBeGreaterThan(prima.grafico)
    expect(screen.getByRole('tab', { name: /MGC/ })).toHaveAttribute('aria-selected', 'true')
    act(() => client.clear())
  })
})
