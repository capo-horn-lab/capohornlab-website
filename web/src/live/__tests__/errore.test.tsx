import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import App from '@/App'

// a render error inside the Live page must not take the site down: the route's errorElement says it in Italian and the layout
// (header, footer with the fixed note) stays
vi.mock('@/pagine/Live', () => ({
  default: () => {
    throw new Error('payload inatteso')
  },
}))

describe('rotta Live: errorElement', () => {
  it('messaggio in italiano e footer con la nota fissa', async () => {
    vi.spyOn(console, 'error').mockImplementation(() => {})
    render(<App />)
    expect(await screen.findByText(/La pagina live non si puo' mostrare/)).toBeInTheDocument()
    expect(screen.getByText("Frequenze descrittive su dati gia' visti, non segnali.")).toBeInTheDocument()
  })
})
