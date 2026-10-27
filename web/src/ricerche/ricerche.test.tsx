import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render, screen, within } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router'
import Ricerca from '@/pagine/Ricerca'
import Ricerche from '@/pagine/Ricerche'
import { indice } from './archivio'
import { barreTabella, puntiSerie } from './grafico-dati'
import {
  dividiFonti,
  idSezione,
  leggiElenco,
  leggiPrefazio,
  leggiRicerca,
  leggiTabella,
  paroleVerdetto,
  SENZA_VERDETTO,
  varianteParola,
  type Dati,
} from './modello'
import { statoMotore } from './stato'

const RAW = `---
id: "x-1"
titolo: "X-1 — prova"
data: "2026-10-12"
strumenti:
  - "MES"
  - "MNQ"
finestra: "MES e MNQ"
verdetto: "pass · non confermata"
audit: {"stato": "ritirato", "id": ["X-1"]}
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

1 righe della scheda non riportate: la prova citata non le contiene.
`

describe('lettura delle pagine generate', () => {
  it('frontmatter a valori JSON, liste a blocco, audit a oggetto e sezioni', () => {
    const { fm, sezioni } = leggiRicerca(RAW)
    expect(fm.id).toBe('x-1')
    expect(fm.strumenti).toEqual(['MES', 'MNQ'])
    expect(fm.prove).toEqual([])
    expect(fm.verdetto).toBe('pass · non confermata')
    expect(fm.audit).toEqual({ stato: 'ritirato', id: ['X-1'] })
    expect(Object.keys(sezioni)).toEqual(['Domanda', 'Esito'])
  })

  it('tabella Esito con \\| e fonti separate; la riga delle righe non riportate sta fuori', () => {
    const { sezioni } = leggiRicerca(RAW)
    const t = leggiTabella(sezioni['Esito'])
    expect(t.testata).toEqual(['Risultato', 'Fonte'])
    expect(t.righe).toHaveLength(1)
    expect(t.righe[0][0]).toBe('MES 120 trade +12,34 USD | t 1,50')
    expect(dividiFonti(t.righe[0][1])).toEqual(['docs/EXECUTION_LEDGER.md#L3-L4', 'runtime/proofs/x/x.json'])
    expect(leggiElenco(sezioni['Esito'])).toEqual([])
    expect(leggiPrefazio(sezioni['Esito'])).toBe('1 righe della scheda non riportate: la prova citata non le contiene.')
  })
})

describe('verdetto dal registro', () => {
  it('parole separate da " · "; senza verdetto = nessuna parola', () => {
    expect(paroleVerdetto('pass · non confermata')).toEqual(['pass', 'non confermata'])
    expect(paroleVerdetto(SENZA_VERDETTO)).toEqual([])
  })

  it("l'aspetto dipende solo dalla parola del registro", () => {
    expect(varianteParola('ritirata')).toBe('destructive')
    expect(varianteParola('fail')).toBe('destructive')
    expect(varianteParola('confermata')).toBe('secondary')
    expect(varianteParola('non confermata')).toBe('outline')
    expect(varianteParola('pass')).toBe('outline')
  })
})

describe('stato del motore', () => {
  it('soglia per canale e spento oltre 180 s', () => {
    expect(statoMotore(0, 60)).toBe('acceso')
    expect(statoMotore(60, 60)).toBe('acceso')
    expect(statoMotore(61, 60)).toBe('in ritardo')
    expect(statoMotore(100, 180)).toBe('acceso')
    expect(statoMotore(180, 180)).toBe('acceso')
    expect(statoMotore(181, 180)).toBe('spento')
    expect(statoMotore(181, 60)).toBe('spento')
    expect(statoMotore(null, 60)).toBe('spento')
  })
})

describe('grafici: un valore mancante non e\' zero', () => {
  const tabella = (m: (number | null)[]): Dati => ({
    tipo: 'tabella',
    colonne: ['r', 'n', 'm', 't', 'u'],
    righe: m.map((v, i) => [`riga ${i}`, 10, v, 1.1, 'USD']),
    fonte: 'runtime/research/sa-report/summary.json',
  })

  it('tabella: la riga con m nullo non ha barra', () => {
    const { barre, omesse } = barreTabella(tabella([1.5, null, -0.5]))
    expect(barre.map((b) => b.valore)).toEqual([1.5, -0.5])
    expect(omesse).toBe(1)
    expect(barre.some((b) => b.valore === 0)).toBe(false)
  })

  it('serie: un anno senza valore e\' un buco, mai 0', () => {
    const dati: Dati = {
      tipo: 'serie',
      colonne: ['anno', 'anni'],
      righe: [['2019', 1.5], ['2020', null], ['2021', 2.0]],
      fonte: 'x.json#/anni',
    }
    const { punti, buchi } = puntiSerie(dati)
    expect(buchi).toBe(1)
    expect(punti.map((p) => p.valore)).toEqual([1.5, 2.0])
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
  it("l'indice ha le voci fissate (e `audit` solo dove c'e')", () => {
    expect(indice.length).toBeGreaterThan(100)
    const base = ['data', 'grafico', 'id', 'pubblicabilita', 'strumenti', 'titolo', 'verdetto']
    for (const v of indice) {
      expect(Object.keys(v).filter((k) => k !== 'audit').sort()).toEqual(base)
    }
    expect(indice.filter((v) => v.audit).map((v) => v.audit)).toContain('ritirato')
  })

  it('/ricerche: verdetto nel registro, filtro con le parole del registro e senza verdetto', () => {
    conRouter('/ricerche')
    expect(screen.getByRole('heading', { name: 'Ricerche' })).toBeInTheDocument()
    expect(screen.getByText(new RegExp(`${indice.length} di ${indice.length} ricerche`))).toBeInTheDocument()
    expect(screen.getByRole('columnheader', { name: 'Verdetto nel registro' })).toBeInTheDocument()
    const filtro = screen.getByLabelText('Verdetto nel registro')
    const opzioni = within(filtro).getAllByRole('option').map((o) => o.textContent)
    expect(opzioni).toContain(SENZA_VERDETTO)
    expect(opzioni).toContain('non confermata')
    for (const inventata of ['misto', 'ritirato', 'corretto']) expect(opzioni).not.toContain(inventata)
    expect(screen.getAllByRole('link').some((a) => a.getAttribute('href') === '/ricerche/bt-sim-1')).toBe(true)
  })

  it('/ricerche/:id mostra le sezioni, la colonna Fonte, le prove e id di sezione validi', async () => {
    const { container } = conRouter('/ricerche/bt-sim-1')
    expect(await screen.findByRole('heading', { name: 'Esito' })).toBeInTheDocument()
    for (const s of ['Domanda', 'Metodo e rubrica', 'Cosa NON dice', 'Prove']) {
      expect(screen.getByRole('heading', { name: s })).toBeInTheDocument()
    }
    expect(screen.getByRole('columnheader', { name: 'Fonte' })).toBeInTheDocument()
    expect(screen.getAllByText(/docs\/EXECUTION_LEDGER\.md#L\d+-L\d+/).length).toBeGreaterThan(0)
    for (const el of container.querySelectorAll('[aria-labelledby]')) {
      const id = el.getAttribute('aria-labelledby') ?? ''
      expect(id).not.toMatch(/\s/)
      expect(container.querySelector(`#${id}`)).not.toBeNull()
    }
    expect(idSezione('Cosa NON dice')).toBe('cosa-non-dice')
  })

  it("una ricerca ritirata: riquadro con le parole dell'audit, senza i numeri ritirati", async () => {
    const { container } = conRouter('/ricerche/gex-1')
    expect(await screen.findByText("Ritirato dall'audit: GEX-1")).toBeInTheDocument()
    expect(screen.getByText('audit: ritirato')).toBeInTheDocument()
    expect(screen.getAllByText(/RITIRATE dall'audit/).length).toBeGreaterThan(0)
    expect(screen.getByText(/I numeri della conferma ritirata non sono riportati/)).toBeInTheDocument()
    for (const ritirato of ['+13,6', '+70,0', '+56,4']) expect(container.textContent).not.toContain(ritirato)
  })

  it('la scheda senza parola di verdetto nelle righe citate dice senza verdetto nel registro', async () => {
    conRouter('/ricerche/sig-1')
    expect(await screen.findByRole('heading', { name: 'Esito' })).toBeInTheDocument()
    expect(screen.getByText(SENZA_VERDETTO)).toBeInTheDocument()
  })

  it('nessuna pagina pubblica un elenco "non verificabile" e nessuna cita gli studi esclusi', async () => {
    const { container } = conRouter('/ricerche/keylim-1')
    expect(await screen.findByRole('heading', { name: 'Esito' })).toBeInTheDocument()
    expect(container.textContent).not.toMatch(/non verificabile|LIMALL|OPT-COND/)
    expect(container.querySelectorAll('tbody tr').length).toBeGreaterThan(0) // l'Esito non e' vuoto
  })

  it('id sconosciuto: pagina non trovata', async () => {
    conRouter('/ricerche/non-esiste')
    expect(await screen.findByText('Ricerca non trovata')).toBeInTheDocument()
  })
})
