import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router'
import { Footer } from './Footer'
import { Nav } from './Nav'
import * as charts from '@/components/charts'

describe('layout', () => {
  it('il footer ha la nota fissa e i link legali assoluti', () => {
    render(<Footer />)
    expect(screen.getByText("Frequenze descrittive su dati gia' visti, non segnali.")).toBeInTheDocument()
    for (const href of ['/disclaimer.html', '/privacy-policy.html', '/cookie-policy.html']) {
      expect(document.querySelector(`a[href="${href}"]`)).not.toBeNull()
    }
  })

  it('la nav ha le quattro voci', () => {
    render(
      <MemoryRouter>
        <Nav />
      </MemoryRouter>,
    )
    expect(screen.getAllByRole('link').map((a) => a.textContent)).toEqual(['Live', 'Ricerche', 'Metodo', 'Stato'])
  })

  it('i grafici Bklit si importano da @/components/charts', () => {
    for (const nome of ['LineChart', 'Line', 'BarChart', 'CandlestickChart', 'LineSparkline', 'ReferenceArea', 'ProjectionLine', 'Deadline', 'ChartMarkers', 'HeatmapChart']) {
      expect(charts).toHaveProperty(nome)
    }
  })
})
