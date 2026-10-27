import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { fireEvent, render, screen, within } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router'
import Ricerca from '@/pagine/Ricerca'
import Ricerche from '@/pagine/Ricerche'
import { indice } from './archivio'
import { barreTabella, disegnaUnGrafico, puntiSerie, valoriSerie } from './grafico-dati'
import {
  dividiFonti,
  idSezione,
  leggiElenco,
  leggiPrefazio,
  leggiRicerca,
  leggiTabella,
  parolaNuda,
  paroleNude,
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
  it("in una scheda con piu' studi la voce porta l'ID; la parola nuda resta quella del registro", () => {
    const v = 'OVN-1: confermati · GOLDN-1: non confermato'
    expect(paroleVerdetto(v)).toEqual(['OVN-1: confermati', 'GOLDN-1: non confermato'])
    expect(paroleVerdetto(v).map(parolaNuda)).toEqual(['confermati', 'non confermato'])
    expect(paroleNude(v)).toEqual(['confermati', 'non confermato'])
    expect(paroleNude('ENS-1: pass · LASTHALF-OOS: pass')).toEqual(['pass']) // una parola nuda una volta sola
    expect(parolaNuda('non confermata')).toBe('non confermata') // senza ID resta com'e'
    expect(paroleNude(SENZA_VERDETTO)).toEqual([])
    expect(varianteParola('confermati')).toBe('secondary')
    expect(varianteParola('adottate')).toBe('secondary')
    expect(varianteParola(parolaNuda('OVN-1: confermati'))).toBe('secondary')
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

  it('riquadro del grafico solo dove Grafico disegna un grafico (serie piena, 2..60 barre)', () => {
    const serie = (righe: unknown[][]): Dati => ({ tipo: 'serie', colonne: ['anno', 'v'], righe, fonte: 'x' }) as Dati
    expect(disegnaUnGrafico(serie([['2019', 1], ['2020', 2]]))).toBe(true)
    expect(disegnaUnGrafico(serie([['2019', 1], ['2020', null], ['2021', 2]]))).toBe(false) // buco: tabella
    expect(disegnaUnGrafico(serie([['2019', 1]]))).toBe(false)
    const tabella = (n: number): Dati => ({ tipo: 'tabella', colonne: ['r', 'm'], righe: Array.from({ length: n }, (_, i) => [`r${i}`, i + 1]), fonte: 'x' }) as Dati
    expect(disegnaUnGrafico(tabella(2))).toBe(true)
    expect(disegnaUnGrafico(tabella(60))).toBe(true)
    expect(disegnaUnGrafico(tabella(61))).toBe(false)
  })
})

describe('sparkline', () => {
  it('un anno senza valore salta il punto: non diventa 0', () => {
    const dati: Dati = {
      tipo: 'serie',
      colonne: ['anno', 'anni'],
      righe: [['2019', 1.5], ['2020', null], ['2021', 2.0]],
      fonte: 'x.json#/anni',
    }
    expect(valoriSerie(dati)).toEqual([1.5, 2.0])
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
    const base = ['data', 'grafico', 'id', 'pubblicabilita', 'serie', 'strumenti', 'titolo', 'verdetto']
    for (const v of indice) {
      expect(Object.keys(v).filter((k) => k !== 'audit').sort()).toEqual(base)
    }
    // l'indice carica i dati.json solo delle serie (sparkline): oggi 3, non le 62 ricerche con grafico
    expect(indice.filter((v) => v.serie).map((v) => v.id).sort()).toEqual(['crypto-1', 'ibs-nt', 'res2-2'])
    expect(indice.filter((v) => v.grafico).length).toBeGreaterThan(50)
    const stati = new Set(indice.filter((v) => v.audit).map((v) => v.audit))
    expect([...stati].sort()).toEqual(['nota', 'ritirato']) // nessun "corretto": l'audit non lo dice
    expect(indice.filter((v) => v.audit === 'ritirato').map((v) => v.id).sort()).toEqual(['gex-1', 'volrev-1'])
  })

  it('/ricerche: verdetto nel registro, filtro con le parole del registro e senza verdetto', () => {
    conRouter('/ricerche')
    expect(screen.getByRole('heading', { name: 'Ricerche' })).toBeInTheDocument()
    expect(screen.getByText(new RegExp(`${indice.length} di ${indice.length} ricerche`))).toBeInTheDocument()
    expect(screen.getByRole('columnheader', { name: 'Verdetto nel registro' })).toBeInTheDocument()
    expect(screen.getAllByText(/locatore principale della scheda/).length).toBeGreaterThan(0)
    expect(screen.queryByText(/righe del registro che la pagina cita/)).toBeNull()
    const filtro = screen.getByLabelText('Verdetto nel registro')
    const opzioni = within(filtro).getAllByRole('option').map((o) => o.textContent)
    expect(opzioni).toContain(SENZA_VERDETTO)
    expect(opzioni).toContain('non confermata')
    for (const inventata of ['misto', 'ritirato', 'corretto']) expect(opzioni).not.toContain(inventata)
    expect(opzioni).toContain('confermati') // il plurale e' una parola del registro
    expect(opzioni.filter((o) => /^[A-Z0-9]+(-[A-Za-z0-9]+)+: /.test(o ?? ''))).toEqual([]) // mai un ID nel filtro
    expect(screen.getAllByRole('link').some((a) => a.getAttribute('href') === '/ricerche/bt-sim-1')).toBe(true)
  })

  it("/ricerche: filtrare per una parola nuda trova anche le schede con piu' studi (ovn-1)", () => {
    conRouter('/ricerche')
    const filtro = screen.getByLabelText('Verdetto nel registro')
    const ha = (id: string) => screen.queryAllByRole('link').some((a) => a.getAttribute('href') === `/ricerche/${id}`)
    fireEvent.change(filtro, { target: { value: 'confermati' } })
    expect(ha('ovn-1')).toBe(true)
    expect(ha('bt-sim-1')).toBe(false)
    fireEvent.change(filtro, { target: { value: 'non confermato' } })
    expect(ha('ovn-1')).toBe(true) // GOLDN-1: non confermato
  })

  it("ovn-1: l'etichetta dice quale studio ha quale verdetto", async () => {
    conRouter('/ricerche/ovn-1')
    expect(await screen.findByRole('heading', { name: 'Esito' })).toBeInTheDocument()
    expect(screen.getByText('OVN-1: confermati')).toBeInTheDocument()
    expect(screen.getByText('GOLDN-1: non confermato')).toBeInTheDocument()
    expect(screen.queryByText('non confermato', { exact: true })).toBeNull() // niente parola nuda senza l'ID
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

  it("`ritirato` copre solo l'ID dichiarato ritirato: volrev-1 non copre STBOND-1 e FXHEDGE-1", async () => {
    conRouter('/ricerche/volrev-1')
    expect(await screen.findByText("Ritirato dall'audit: VOLREV-1")).toBeInTheDocument()
    expect(screen.queryByText(/Ritirato dall'audit:.*(STBOND|FXHEDGE)/)).toBeNull()
    expect(screen.getAllByText(/STBOND-1/).length).toBeGreaterThan(0) // le righe degli studi non ritirati restano
  })

  it("gli altri ID dell'audit hanno un badge neutro `nota dell'audit`, mai ritirato ne' corretto", async () => {
    const { container } = conRouter('/ricerche/ibs-nt')
    expect(await screen.findByText("Nota dell'audit: IBS-NT")).toBeInTheDocument()
    expect(screen.getByText("nota dell'audit")).toBeInTheDocument()
    expect(container.textContent).not.toMatch(/ritirato|corretto|I numeri della conferma ritirata/i)
  })

  it('/ricerche: i segni audit in elenco sono `audit: ritirato` e `nota dell\'audit`', () => {
    conRouter('/ricerche')
    expect(screen.getAllByText('audit: ritirato')).toHaveLength(indice.filter((v) => v.audit === 'ritirato').length)
    expect(screen.getAllByText("nota dell'audit")).toHaveLength(indice.filter((v) => v.audit === 'nota').length)
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
