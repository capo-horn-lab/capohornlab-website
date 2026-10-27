import { fireEvent, render, screen } from '@testing-library/react'
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
    expect(await screen.findByRole('heading', { level: 1, name: 'Metodo' })).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: 'Apri il menu' }))
    // time for the rejected import to reach React (without the guard, the page became "Pagina non disponibile" here)
    await new Promise((r) => setTimeout(r, 1000))
    expect(screen.getByRole('heading', { level: 1, name: 'Metodo' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Capo Horn Lab' })).toBeInTheDocument()
    expect(screen.queryByText('Pagina non disponibile')).toBeNull()
    window.history.pushState({}, '', '/')
  })
})
