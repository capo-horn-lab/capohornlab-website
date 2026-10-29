import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { act, render, screen, waitFor, within } from '@testing-library/react'
import Stato from '@/pagine/Stato'

function busta(eta_s: number | null, chiave = 'scenari') {
  const dati =
    chiave === 'memoria'
      ? { generato: '2026-10-29T10:03:19+00:00', stato: { strumento: 'MNQ 12-26' }, verdetti: { generato: '2026-10-29T07:12:39+00:00' } }
      : { generato: '2026-10-27T08:59:58Z', principale: { strumento: 'MNQ', contratto: '12-26' } }
  return {
    ricevuto: eta_s === null ? null : '2026-10-27T09:00:00Z',
    eta_s,
    dati: eta_s === null ? null : dati,
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
  it('legge scenari, frequenze e memoria e applica le soglie 60 s / 180 s / 180 s (spento a 600 s)', async () => {
    const eta: Record<string, number | null> = { scenari: 30, frequenze: 400, memoria: 100 }
    const fetchMock = vi.fn(async (url: string) => {
      const chiave = url.split('/live/')[1]
      return { ok: true, status: 200, json: async () => busta(eta[chiave], chiave) }
    })
    vi.stubGlobal('fetch', fetchMock)
    monta()
    // findAllBy* si risolve al primo badge: il conteggio dei due canali accesi va atteso
    await waitFor(() => expect(screen.getAllByText('motore acceso')).toHaveLength(2))
    expect(await screen.findByText('motore spento')).toBeInTheDocument()
    expect(fetchMock.mock.calls.map((c) => c[0] as string).sort()).toEqual([
      expect.stringMatching(/\/live\/frequenze$/),
      expect.stringMatching(/\/live\/memoria$/),
      expect.stringMatching(/\/live\/scenari$/),
    ])
    expect(screen.getAllByText('MNQ 12-26')).toHaveLength(3)
    expect(screen.getByText('30 s')).toBeInTheDocument()
  })

  it('soglia per canale: a 100 s gli scenari sono in ritardo, frequenze e memoria (180 s) sono accese', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async (url: string) => ({ ok: true, status: 200, json: async () => busta(100, url.split('/live/')[1]) })),
    )
    monta()
    const scenari = (await screen.findByRole('heading', { name: 'Scenari' })).closest('section') as HTMLElement
    const frequenze = screen.getByRole('heading', { name: 'Frequenze' }).closest('section') as HTMLElement
    const memoria = screen.getByRole('heading', { name: 'Memoria' }).closest('section') as HTMLElement
    await waitFor(() => expect(within(scenari).getByText('motore in ritardo')).toBeInTheDocument())
    expect(within(frequenze).getByText('motore acceso')).toBeInTheDocument()
    expect(within(memoria).getByText('motore acceso')).toBeInTheDocument()
  })

  it('memoria: in ritardo fra 181 e 600 s, spento oltre 600 s; scenari e frequenze restano spenti oltre 180 s', async () => {
    for (const [eta, atteso] of [[181, 'motore in ritardo'], [600, 'motore in ritardo'], [601, 'motore spento']] as const) {
      vi.stubGlobal('fetch', vi.fn(async (url: string) => ({ ok: true, status: 200, json: async () => busta(eta, url.split('/live/')[1]) })))
      const { unmount } = render(
        <QueryClientProvider client={new QueryClient({ defaultOptions: { queries: { retry: false } } })}>
          <Stato />
        </QueryClientProvider>,
      )
      const sezione = (n: string) => screen.getByRole('heading', { name: n }).closest('section') as HTMLElement
      await screen.findByRole('heading', { name: 'Memoria' })
      await waitFor(() => expect(within(sezione('Memoria')).getByText(atteso)).toBeInTheDocument())
      await waitFor(() => expect(within(sezione('Frequenze')).getByText('motore spento')).toBeInTheDocument())
      expect(within(sezione('Scenari')).getByText('motore spento')).toBeInTheDocument()
      unmount()
    }
  })

  it('memoria: mostra lo strumento e la data della verifica dei verdetti', async () => {
    vi.stubGlobal('fetch', vi.fn(async (url: string) => ({ ok: true, status: 200, json: async () => busta(5, url.split('/live/')[1]) })))
    monta()
    const memoria = (await screen.findByRole('heading', { name: 'Memoria' })).closest('section') as HTMLElement
    await waitFor(() => expect(within(memoria).getByText('MNQ 12-26')).toBeInTheDocument())
    expect(within(memoria).getByText('Verifica del')).toBeInTheDocument()
    expect(within(memoria).getByText('2026-10-29T07:12:39+00:00')).toBeInTheDocument()
  })

  it('errore di rete: messaggio visibile, nessun badge', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: false, status: 503, json: async () => ({}) })))
    monta()
    await waitFor(() => expect(screen.getAllByText(/Servizio non raggiungibile/)).toHaveLength(3))
    expect(screen.queryByText(/^motore (acceso|spento|in ritardo)$/)).toBeNull()
  })

  it('aggiornamento fallito dopo un dato riuscito: l eta non resta ferma accanto all errore (n/d)', async () => {
    let giro = 0
    vi.stubGlobal('fetch', vi.fn(async (url: string) => {
      giro += 1
      return giro <= 3 ? { ok: true, status: 200, json: async () => busta(0, url.split('/live/')[1]) } : { ok: false, status: 503, json: async () => ({}) }
    }))
    const client = new QueryClient({ defaultOptions: { queries: { retry: false } } })
    render(
      <QueryClientProvider client={client}>
        <Stato />
      </QueryClientProvider>,
    )
    await waitFor(() => expect(screen.getAllByText('0 s')).toHaveLength(3))
    await act(() => client.refetchQueries())
    await waitFor(() => expect(screen.getAllByText(/Servizio non raggiungibile/)).toHaveLength(3))
    expect(screen.queryAllByText('0 s')).toHaveLength(0)
    expect(screen.getAllByText('n/d')).toHaveLength(3)
  })
})
