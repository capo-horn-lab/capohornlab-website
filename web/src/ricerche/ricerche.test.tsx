import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router'
import Ricerca from '@/pagine/Ricerca'
import Ricerche from '@/pagine/Ricerche'
import { indice } from './archivio'
import { dividiFonti, leggiElenco, leggiRicerca, leggiTabella } from './modello'
import { statoMotore } from './stato'

const RAW = `---
id: "x-1"
titolo: "X-1 — prova"
data: "2026-10-12"
strumenti:
  - "MES"
  - "MNQ"
finestra: "MES e MNQ"
verdetto: "ritirato"
pubblicabilita: "avvertenza"
avvertenza: "solo aggregati"
fonte_ledger: "docs/EXECUTION_LEDGER.md#L3-L4"
prove: []
---

## Domanda

la regola guadagna?

## Esito

| Risultato | Fonte |
|---|---|
| MES 120 trade +12,34 USD \\| t 1,50 | docs/EXECUTION_LEDGER.md#L3-L4 · runtime/proofs/x/x.json |

Non verificabile (restano fuori dalla tabella):

- 80 trade — non verificabile: 80
`

describe('lettura delle pagine generate', () => {
  it('frontmatter a valori JSON, liste a blocco e sezioni', () => {
    const { fm, sezioni } = leggiRicerca(RAW)
    expect(fm.id).toBe('x-1')
    expect(fm.strumenti).toEqual(['MES', 'MNQ'])
    expect(fm.prove).toEqual([])
    expect(fm.verdetto).toBe('ritirato')
    expect(Object.keys(sezioni)).toEqual(['Domanda', 'Esito'])
  })

  it('tabella Esito con \\| e fonti separate', () => {
    const { sezioni } = leggiRicerca(RAW)
    const t = leggiTabella(sezioni['Esito'])
    expect(t.testata).toEqual(['Risultato', 'Fonte'])
    expect(t.righe).toHaveLength(1)
    expect(t.righe[0][0]).toBe('MES 120 trade +12,34 USD | t 1,50')
    expect(dividiFonti(t.righe[0][1])).toEqual(['docs/EXECUTION_LEDGER.md#L3-L4', 'runtime/proofs/x/x.json'])
    expect(leggiElenco(sezioni['Esito'])).toEqual(['80 trade — non verificabile: 80'])
  })
})

describe('stato del motore', () => {
  it('soglie 60 s e 180 s', () => {
    expect(statoMotore(0)).toBe('acceso')
    expect(statoMotore(60)).toBe('acceso')
    expect(statoMotore(61)).toBe('in ritardo')
    expect(statoMotore(180)).toBe('in ritardo')
    expect(statoMotore(181)).toBe('spento')
    expect(statoMotore(null)).toBe('spento')
  })
})

function conRouter(percorso: string) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  return render(
    <QueryClientProvider client={client}>
      <MemoryRouter initialEntries={[percorso]}>
        <Routes>
          <Route path="/ricerche" element={<Ricerche />} />
          <Route path="/ricerche/:id" element={<Ricerca />} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>,
  )
}

describe('pagine', () => {
  it("l'indice ha le voci fissate e una pagina per ognuna", () => {
    expect(indice.length).toBeGreaterThan(100)
    for (const v of indice.slice(0, 5)) {
      expect(Object.keys(v).sort()).toEqual(
        ['data', 'grafico', 'id', 'pubblicabilita', 'strumenti', 'titolo', 'verdetto'].sort(),
      )
    }
  })

  it('/ricerche mostra la tabella e il conteggio', () => {
    conRouter('/ricerche')
    expect(screen.getByRole('heading', { name: 'Ricerche' })).toBeInTheDocument()
    expect(screen.getByText(new RegExp(`${indice.length} di ${indice.length} ricerche`))).toBeInTheDocument()
    expect(screen.getAllByRole('link').some((a) => a.getAttribute('href') === '/ricerche/bt-sim-1')).toBe(true)
  })

  it('/ricerche/:id mostra le sezioni, la colonna Fonte e le prove', async () => {
    conRouter('/ricerche/bt-sim-1')
    expect(await screen.findByRole('heading', { name: 'Esito' })).toBeInTheDocument()
    for (const s of ['Domanda', 'Metodo e rubrica', 'Cosa NON dice', 'Prove']) {
      expect(screen.getByRole('heading', { name: s })).toBeInTheDocument()
    }
    expect(screen.getByRole('columnheader', { name: 'Fonte' })).toBeInTheDocument()
    expect(screen.getAllByText(/docs\/EXECUTION_LEDGER\.md#L\d+-L\d+/).length).toBeGreaterThan(0)
  })

  it('una ricerca ritirata mostra il riquadro in evidenza con le parole dell\'audit', async () => {
    conRouter('/ricerche/gex-1')
    expect(await screen.findByText("Ritirato dall'audit")).toBeInTheDocument()
    expect(screen.getAllByText(/RITIRATE dall'audit/).length).toBeGreaterThan(0)
  })

  it('id sconosciuto: pagina non trovata', async () => {
    conRouter('/ricerche/non-esiste')
    expect(await screen.findByText('Ricerca non trovata')).toBeInTheDocument()
  })
})
