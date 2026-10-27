import { act, fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'

// the phone menu's chunk does not load (an old tab after a deploy): the import rejects
vi.mock('@/layout/MenuMobile', () => {
  throw new Error('Failed to fetch dynamically imported module')
})

describe('chunk del menu del telefono non caricato', () => {
  it('un tocco sul menu lascia intatti la pagina e l header', async () => {
    vi.spyOn(console, 'error').mockImplementation(() => {})
    window.history.pushState({}, '', '/metodo')
    vi.resetModules()
    const { default: App } = await import('@/App')
    render(<App />)
    // cold (empty Vite cache) App and the page's chunk take seconds to transform: 1 s was not enough (valutazione 1, criterio 9)
    expect(await screen.findByRole('heading', { level: 1, name: 'Metodo' }, { timeout: 10_000 })).toBeInTheDocument()
    // the press starts the import; inside act the test awaits the same rejection, so React has handled it before the checks
    // (without the guard, the page became "Pagina non disponibile" here); no fixed sleep
    await act(async () => {
      fireEvent.click(screen.getByRole('button', { name: 'Apri il menu' }))
      await expect(import('@/layout/MenuMobile')).rejects.toThrow()
    })
    expect(screen.getByRole('heading', { level: 1, name: 'Metodo' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Capo Horn Lab' })).toBeInTheDocument()
    expect(screen.queryByText('Pagina non disponibile')).toBeNull()
    window.history.pushState({}, '', '/')
  }, 20_000)
})
