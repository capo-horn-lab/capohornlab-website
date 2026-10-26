import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render, screen, within } from '@testing-library/react'
import fs from 'node:fs'
import path from 'node:path'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { haErrore, type Frequenze, type Scenari, type StrumentoFrequenze, type StrumentoScenari, validaFrequenze, validaScenari } from '@/lib/tipi'
import { avvisi } from '@/live/AvvisoFreschezza'
import { Esiti } from '@/live/Esiti'
import { GraficoLive } from '@/live/GraficoLive'
import { sessioneAperta } from '@/live/StatoLive'
import { ordineStrumenti } from '@/live/StrumentoTabs'
import { percorsoTesto, TabellePannello } from '@/live/TabellePannello'
import { righeEsiti, righeTesto, vista } from '@/live/vista'
import Live from '@/pagine/Live'
import frequenzeJson from '@/test/fixtures/frequenze.json'
import scenariJson from '@/test/fixtures/scenari.json'

const scen = validaScenari(scenariJson).dati as Scenari
const freq = validaFrequenze(frequenzeJson).dati as Frequenze
const sc = (s: string) => scen.strumenti[s] as StrumentoScenari
const fr = (s: string) => freq.strumenti[s] as StrumentoFrequenze
const v = (s: string) => vista(sc(s), scen.barre[s], fr(s), s === scen.principale.strumento)

// desktop_trader.esito_ramo on the same fixture (.venv-quant, 2026-10-27): the site adds only D8's " ±m" when the engine gives it
const TRADER: Record<string, string[]> = {
  MGC: ["chiusura sotto l'apertura 4022: 52% (46/88) · mediana 3998", "chiusura sopra l'apertura 4022: 48% (42/88) · mediana 4040"],
  MNQ: ["chiusura sotto l'apertura 29231: 54% (37/69) · mediana 29099", "chiusura sopra l'apertura 29231: 46% (32/69) · mediana 29391"],
  MES: ["mai ritorno all'apertura 7683 entro 21:00: 19 su 20, pochi casi · mediana dell'estensione 7728"],
  M2K: ["nessun 4.6 sotto l'apertura (2785) entro 21:00: 30 su 31, pochi casi", "poi chiusura sopra l'apertura 2789: 29 su 30, pochi casi · mediana 2818",
    "chiusura sopra l'apertura 2789: 29 su 31, pochi casi · mediana 2818"],
  MYM: ["chiusura sopra l'apertura 52643: 53% (34/64) · mediana 52752", "chiusura sotto l'apertura 52643: 47% (30/64) · mediana 52517"],
}

describe('vista sulle fixture reali', () => {
  it('esiti come il Trader (riferimento, arrotondamento, pochi casi), con ±m D8', () => {
    for (const [s, attesi] of Object.entries(TRADER)) {
      const righe = righeEsiti(v(s)).filter((r) => !r.id.startsWith('da-qui-')).map((r) => r.testo)
      expect(righe.map((t) => t.replace(/ ±\d+/, ''))).toEqual(attesi)
    }
    expect(righeEsiti(v('MGC'))[0].testo).toBe("chiusura sotto l'apertura 4022: 52% (46/88 ±10) · mediana 3998")
  })
  it('rami disegnati: gli stessi del Trader (MES r2; da qui q2, q3, q3.2) e nessun ramo senza minuti sul grafico', () => {
    expect(v('MES').g.segmenti.map((x) => [x.id, x.etichetta])).toEqual([['r2', 'estensione +65 25% (5/20 ±19)']])
    expect(v('MGC').g.segmenti).toEqual([])
    expect(v('MGC').daQui!.g.segmenti.map((x) => x.id)).toEqual(['q2', 'q3', 'q3.2'])
    expect(righeEsiti(v('MGC')).find((r) => r.id === 'da-qui-q1')!.testo)
      .toBe('da qui: nessun movimento di 5.7 dal punto 4022 (4017-4028) entro 21:00: 55% (131/240 ±6)')
    for (const s of Object.keys(TRADER)) for (const x of v(s).g.segmenti) expect(x.ramo.minuti).not.toBeNull()
    expect(v('MNQ').daQui).toBeNull()
  })
  it('dominio y su candele e capi, livelli divisi tra dentro e fuori', () => {
    const x = v('MGC')
    const [lo, hi] = x.dominio!
    for (const c of x.candele) expect(c.low >= lo && c.high <= hi).toBe(true)
    expect(x.livelli.length + x.fuori.length).toBe(fr('MGC').livelli.length)
    expect(x.inTesto).toBe(false)
    expect(righeTesto(x)).toEqual([])
  })
  it('albero in testo quando la radice e oltre 2 ore dopo l ultima barra', () => {
    const s = { ...sc('MES'), radice: { ...sc('MES').radice, t: '2026-10-27T14:30+01:00' } }
    const x = vista(s, scen.barre.MES, fr('MES'), false)
    expect(x.inTesto).toBe(true)
    expect(righeTesto(x)[0]).toMatch(/^radice 20:08 primo movimento a 7711.*albero in testo$/)
    expect(righeTesto(x)[1]).toMatch(/^ {2}estensione \+65 25% \(5\/20 ±19\) a 7748.69 verso le /)
  })
  it('principale per primo nelle schede', () => {
    expect(ordineStrumenti(scen, freq)).toEqual(['MGC', 'MNQ', 'MES', 'M2K', 'MYM'])
    expect(ordineStrumenti(null, freq)[0]).toBe(freq.principale.strumento)
  })
})

describe('pannello', () => {
  it('percorso di oggi con gli orari dell apertura del payload (14:30 questa settimana)', () => {
    const ap = fr('MGC').apertura!
    expect(percorsoTesto(ap.percorso, ap.soglia!, '14:30')).toBe("primo movimento GIU alle 14:34 (4 min dopo le 14:30); ritorno all'apertura alle 15:18 (44 min dopo), "
      + "estensione 19 prima del ritorno; 5.7 opposto alle 15:19 (1 min dopo il ritorno); nuovo ritorno alle 15:26 (7 min dopo), estensione opposta 8; chiusura meno apertura finora +1.70")
  })
  it('cinque sezioni e concordanza nell ordine del pannello, numeri D8', () => {
    render(<TabellePannello r={fr('MGC')} orari={freq.orari} />)
    expect(screen.getAllByRole('heading', { level: 3 }).map((h) => h.textContent)).toEqual(['STATO', 'FINESTRE', 'LIVELLI', "CASO DELL'APERTURA", 'LENTI', 'CONCORDANZA'])
    const riga = (nome: string) => screen.getAllByRole('row').find((r) => within(r).queryAllByRole('cell')[0]?.textContent === nome)!
    expect(within(riga('massimo notte')).getAllByRole('cell').map((c) => c.textContent))
      .toEqual(['massimo notte', '4039.40', '+16.20', '+0.38', '0.30-0.50 A', '-', '10% (3/31 ±10)'])
    expect(within(riga('minimo notte')).getAllByRole('cell')[6].textContent).toBe('0 su 68')
    expect(within(riga('L1 VWAP notte')).getAllByRole('cell')[7].textContent).toBe('3% (8/271 ±2) v')
    expect(screen.getByText(fr('MGC').lenti!.concordanza!.frase!)).toBeInTheDocument()
    const corrente = fr('MGC').finestre.find((w) => w.corrente)!
    expect(screen.getByText(`> ${corrente.finestra}`, { exact: false })).toBeInTheDocument()
  })
})

describe('stato e freschezza', () => {
  const base = { isError: false, dataUpdatedAt: Date.UTC(2026, 9, 26, 19, 8), errorUpdatedAt: Date.UTC(2026, 9, 26, 19, 9) }
  it('messaggi', () => {
    expect(avvisi({ ...base, data: { ricevuto: null, eta_s: null, dati: null } }, 60)).toEqual(['Nessun dato dal motore (spento, o non ha ancora pubblicato).'])
    expect(avvisi({ ...base, data: { ricevuto: 'x', eta_s: 60, dati: {} } }, 60)).toEqual([])
    expect(avvisi({ ...base, data: { ricevuto: 'x', eta_s: 61, dati: {} } }, 60)).toEqual(['Motore spento o scollegato da 1 minuto'])
    expect(avvisi({ ...base, data: { ricevuto: 'x', eta_s: 600, dati: {} } }, 180)).toEqual(['Motore spento o scollegato da 10 minuti'])
    expect(avvisi({ ...base, isError: true, data: { ricevuto: 'x', eta_s: 5, dati: {} } }, 60))
      .toEqual(['Aggiornamento fallito alle 20:09; ultimo caricamento riuscito alle 20:08'])
  })
  it('sessione regolare aperta o chiusa all ora del calcolo', () => {
    expect(sessioneAperta(scen.generato, scen.orari)).toBe(true)
    expect(sessioneAperta('2026-10-26T21:00+01:00', scen.orari)).toBe(false)
    expect(sessioneAperta('2026-10-27T15:00+01:00', scen.orari)).toBe(false)
  })
  it('riquadro esiti', () => {
    render(<Esiti righe={righeEsiti(v('M2K'))} />)
    expect(screen.getByText('Esiti a fine sessione (non livelli da toccare)')).toBeInTheDocument()
    expect(screen.getAllByRole('listitem').length).toBe(3)
  })
})

describe('grafico e pagina', () => {
  afterEach(() => vi.restoreAllMocks())

  it('overlay: radice, rami, livelli, candela viva sulle scale del grafico', () => {
    vi.spyOn(HTMLElement.prototype, 'clientWidth', 'get').mockReturnValue(900)
    vi.spyOn(HTMLElement.prototype, 'clientHeight', 'get').mockReturnValue(450)
    const { container } = render(<GraficoLive v={v('MGC')} />)
    const testi = [...container.querySelectorAll('.chl-sovrapposizione text')].map((t) => t.textContent)
    // "di 5.7" is not shortened: the Trader's BREVI match whole points only ("di 50 giu" -> "50 giu"), reproduced as is
    expect(testi).toContain('da qui: primo movimento di 5.7 su da qui 22% (53/240 ±5)')
    expect(testi.some((t) => t?.startsWith('20:08 estensione | apertura 4021.5'))).toBe(true)
    expect(testi).toContain('massimo notte 10% (3/31 ±10)')
    for (const l of container.querySelectorAll('.chl-sovrapposizione line')) {
      for (const a of ['x1', 'x2', 'y1', 'y2']) expect(Number.isFinite(Number(l.getAttribute(a)))).toBe(true)
    }
    expect(container.querySelectorAll('.chart-candlesticks g').length).toBeGreaterThan(90)
  })

  it('su telefono le etichette dei rami accorciano il nome, mai la frequenza', () => {
    vi.spyOn(HTMLElement.prototype, 'clientWidth', 'get').mockReturnValue(343)
    vi.spyOn(HTMLElement.prototype, 'clientHeight', 'get').mockReturnValue(400)
    const { container } = render(<GraficoLive v={v('MGC')} />)
    const rami = [...container.querySelectorAll('.chl-sovrapposizione text')].map((t) => t.textContent ?? '').filter((t) => t.startsWith('da qui: '))
    expect(rami.length).toBe(3)
    expect(rami.some((t) => t.includes('…'))).toBe(true)
    for (const t of rami) expect(t).toMatch(/\d+% \(\d+\/\d+ ±\d+\)$/)
    const ore = [...container.querySelectorAll('.chl-sovrapposizione text')].filter((t) => /^\d\d:\d\d$/.test(t.textContent ?? '')).map((t) => Number(t.getAttribute('x')))
    expect(ore.length).toBeGreaterThan(2)
    for (let i = 1; i < ore.length; i++) expect(ore[i] - ore[i - 1]).toBeGreaterThanOrEqual(44)
  })

  it('albero in testo: niente rami disegnati e asse dei tempi fermo ai 36 slot futuri', () => {
    vi.spyOn(HTMLElement.prototype, 'clientWidth', 'get').mockReturnValue(900)
    vi.spyOn(HTMLElement.prototype, 'clientHeight', 'get').mockReturnValue(450)
    const s = { ...sc('MES'), radice: { ...sc('MES').radice, t: '2026-10-27T14:30+01:00' } }
    const { container } = render(<GraficoLive v={vista(s, scen.barre.MES, fr('MES'), false)} />)
    const testi = [...container.querySelectorAll('.chl-sovrapposizione text')].map((t) => t.textContent ?? '')
    expect(testi.filter((t) => /^\d\d:\d\d$/.test(t)).at(-1)).toBe('23:00')
    expect(testi.some((t) => t.includes('estensione +65'))).toBe(false)
  })

  it('pagina con i due canali (fetch delle fixture)', async () => {
    vi.spyOn(globalThis, 'fetch').mockImplementation(async (u) =>
      new Response(JSON.stringify(String(u).endsWith('/live/scenari') ? scenariJson : frequenzeJson), { status: 200 }))
    render(<QueryClientProvider client={new QueryClient()}><Live /></QueryClientProvider>)
    expect(await screen.findByRole('tab', { name: /MGC/ })).toBeInTheDocument()
    expect(screen.getAllByRole('tab').map((t) => t.textContent)).toEqual(['MGCprincipale', 'MNQ', 'MES', 'M2K', 'MYM'])
    expect(await screen.findByText('STATO')).toBeInTheDocument()
    expect(screen.getByText(/sessione regolare 14:30-21:00 Roma: aperta/)).toBeInTheDocument()
    expect(screen.getByText('LIMITI')).toBeInTheDocument()
  })

  it('pagina con il motore senza dati', async () => {
    vi.spyOn(globalThis, 'fetch').mockImplementation(async () => new Response(JSON.stringify({ ricevuto: null, eta_s: null, dati: null }), { status: 200 }))
    render(<QueryClientProvider client={new QueryClient()}><Live /></QueryClientProvider>)
    expect((await screen.findAllByText(/Nessun dato dal motore/)).length).toBe(2)
  })
})

describe('cablaggio', () => {
  const radice = path.resolve(import.meta.dirname, '../..')
  const file = [...fs.readdirSync(path.join(radice, 'live')).filter((f) => /\.tsx?$/.test(f)).map((f) => path.join(radice, 'live', f)),
    ...['tipi', 'api', 'albero', 'fmt', 'aggrega'].map((f) => path.join(radice, 'lib', `${f}.ts`)), path.join(radice, 'pagine', 'Live.tsx')]
  it('niente innerHTML, niente colori fuori dai token, niente verde/rosso', () => {
    for (const f of file) {
      const s = fs.readFileSync(f, 'utf8')
      expect(s, f).not.toMatch(/innerHTML|dangerouslySetInnerHTML/)
      expect(s, f).not.toMatch(/#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(|oklch\(/)
      expect(s, f).not.toMatch(/\b(green|red|emerald)\b|(text|bg|fill|stroke)-(green|red|emerald)-/)
    }
  })
  it('errore di uno strumento nei due canali', () => {
    expect(haErrore({ errore: 'x' }) && !haErrore(sc('MGC'))).toBe(true)
  })
})
