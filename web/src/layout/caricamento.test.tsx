import { cleanup, render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'

// A page chunk that does not load (an old tab after a deploy, a network blip): the dynamic import rejects.
vi.mock('@/pagine/Live', () => {
  throw new Error('Failed to fetch dynamically imported module')
})
vi.mock('@/pagine/Ricerche', () => {
  throw new Error('Failed to fetch dynamically imported module')
})
// A page that loads but fails to render.
vi.mock('@/pagine/Metodo', () => ({
  default: () => {
    throw new Error('contenuto inatteso')
  },
}))

const NOTA = "Frequenze descrittive su dati gia' visti, non segnali."

/** The router reads the address when App is imported: set it first, then import. */
async function apri(percorso: string) {
  window.history.pushState({}, '', percorso)
  vi.resetModules()
  const { default: App } = await import('@/App')
  render(<App />)
}

describe('pagina che non si carica o non si mostra', () => {
  afterEach(() => {
    cleanup()
    vi.restoreAllMocks()
    window.history.pushState({}, '', '/')
  })

  it('/ con il chunk della pagina live rifiutato: messaggio della pagina live nel layout, con la nota fissa', async () => {
    await apri('/')
    const avviso = await screen.findByRole('alert')
    expect(avviso.textContent).toMatch(/La pagina live non si puo' mostrare in questo momento/)
    expect(screen.getByRole('heading', { level: 1, name: 'Frequenze live' })).toBeInTheDocument()
    expect(screen.getByText(NOTA)).toBeInTheDocument()
    expect(screen.queryByText(/Unexpected Application Error/)).toBeNull()
  })

  it('/ricerche con il chunk rifiutato: messaggio neutro nel layout, con la nota fissa', async () => {
    await apri('/ricerche')
    const avviso = await screen.findByRole('alert')
    expect(avviso.textContent).toMatch(/non si puo' mostrare in questo momento/)
    expect(screen.getByRole('heading', { level: 1, name: 'Pagina non disponibile' })).toBeInTheDocument()
    expect(screen.getByText(NOTA)).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Capo Horn Lab' })).toBeInTheDocument() // the header stays
    expect(screen.queryByText(/Unexpected Application Error/)).toBeNull()
  })

  it('/metodo che fallisce nel rendering: lo stesso messaggio nel layout, con la nota fissa', async () => {
    vi.spyOn(console, 'error').mockImplementation(() => {})
    await apri('/metodo')
    expect(await screen.findByRole('alert')).toBeInTheDocument()
    expect(screen.getByRole('heading', { level: 1, name: 'Pagina non disponibile' })).toBeInTheDocument()
    expect(screen.getByText(NOTA)).toBeInTheDocument()
    expect(screen.queryByText(/Unexpected Application Error/)).toBeNull()
  })
})
