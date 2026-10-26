import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render, screen, waitFor } from '@testing-library/react'
import Stato from '@/pagine/Stato'

function busta(eta_s: number | null) {
  return {
    ricevuto: eta_s === null ? null : '2026-10-27T09:00:00Z',
    eta_s,
    dati: eta_s === null ? null : { generato: '2026-10-27T08:59:58Z', principale: { strumento: 'MNQ', contratto: '12-26' } },
  }
}

function monta() {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  render(
    <QueryClientProvider client={client}>
      <Stato />
    </QueryClientProvider>,
  )
}

afterEach(() => vi.unstubAllGlobals())

describe('/stato', () => {
  it('legge scenari e frequenze e applica le soglie 60 s / 180 s', async () => {
    const eta: Record<string, number | null> = { scenari: 30, frequenze: 400 }
    const fetchMock = vi.fn(async (url: string) => {
      const chiave = url.split('/live/')[1]
      return { ok: true, status: 200, json: async () => busta(eta[chiave]) }
    })
    vi.stubGlobal('fetch', fetchMock)
    monta()
    expect(await screen.findByText('motore acceso')).toBeInTheDocument()
    expect(await screen.findByText('motore spento')).toBeInTheDocument()
    expect(fetchMock.mock.calls.map((c) => c[0] as string).sort()).toEqual([
      expect.stringMatching(/\/live\/frequenze$/),
      expect.stringMatching(/\/live\/scenari$/),
    ])
    expect(screen.getAllByText('MNQ 12-26')).toHaveLength(2)
    expect(screen.getByText('30 s')).toBeInTheDocument()
  })

  it('errore di rete: messaggio visibile, nessun badge', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: false, status: 503, json: async () => ({}) })))
    monta()
    await waitFor(() => expect(screen.getAllByText(/Servizio non raggiungibile/)).toHaveLength(2))
    expect(screen.queryByText(/^motore (acceso|spento|in ritardo)$/)).toBeNull()
  })
})
