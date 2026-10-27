import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import Live from '@/pagine/Live'
import frequenzeJson from '@/test/fixtures/frequenze.json'
import scenariJson from '@/test/fixtures/scenari.json'

// the chart's chunk does not load (an old tab after a deploy): the import rejects
vi.mock('@/live/GraficoLive', () => {
  throw new Error('Failed to fetch dynamically imported module')
})

describe('chunk del grafico non caricato', () => {
  it('una riga al posto del grafico; testo, esiti e tabelle restano', async () => {
    vi.spyOn(globalThis, 'fetch').mockImplementation(async (u) =>
      new Response(JSON.stringify(String(u).endsWith('/live/scenari') ? scenariJson : frequenzeJson), { status: 200 }))
    render(<QueryClientProvider client={new QueryClient()}><Live /></QueryClientProvider>)
    expect(await screen.findByText(/Il grafico non si puo' mostrare in questo momento/)).toBeInTheDocument()
    expect(screen.getByText('STATO')).toBeInTheDocument()
    expect(screen.getByText('Esiti a fine sessione (non livelli da toccare)')).toBeInTheDocument()
    expect(screen.queryByText(/La pagina live non si puo' mostrare/)).toBeNull()
  })
})
