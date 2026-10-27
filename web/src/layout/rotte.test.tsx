import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'

// The router reads the address when App is imported: set it first, then import.
describe('rotta sconosciuta', () => {
  it('pagina "non trovata" nel layout, con la nota fissa (non l errore di React Router)', async () => {
    window.history.pushState({}, '', '/metodo/xyz')
    vi.resetModules()
    const { default: App } = await import('@/App')
    render(<App />)
    expect(await screen.findByRole('heading', { level: 1, name: 'Pagina non trovata' })).toBeInTheDocument()
    expect(screen.queryByText(/Unexpected Application Error/)).toBeNull()
    expect(screen.getByText("Frequenze descrittive su dati gia' visti, non segnali.")).toBeInTheDocument()
    window.history.pushState({}, '', '/')
  })
})
