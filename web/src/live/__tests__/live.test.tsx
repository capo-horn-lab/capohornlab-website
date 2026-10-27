import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render, screen, waitFor, within } from '@testing-library/react'
import fs from 'node:fs'
import path from 'node:path'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { haErrore, type Frequenze, type Scenari, type StrumentoFrequenze, type StrumentoScenari, validaFrequenze, validaScenari } from '@/lib/tipi'
import { avvisi, etaCorrente } from '@/live/AvvisoFreschezza'
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
const v = (s: string) => vista(sc(s), scen.barre[s], fr(s), s === scen.principale.strumento, scen.orari)
type Rec = Record<string, unknown>
const copia = (x: unknown) => structuredClone(x) as { dati: Rec & { strumenti: Record<string, Rec>; barre: Record<string, Rec> } }

// The Trader's outcomes box (desktop_trader.esiti + esito_ramo, box rows as desktop_trader.py ~2625-2633) on the same fixture, from
// runtime/proofs/freqsito3/task3/strumenti/esiti_trader.py (.venv-quant, 2026-10-27): the site adds only D8's " ±m" and writes the
// children's "  poi " without the indent
const TRADER: Record<string, string[]> = {
  MGC: ["chiusura sotto l'apertura 4022: 52% (46/88) · mediana 3998", "chiusura sopra l'apertura 4022: 48% (42/88) · mediana 4040",
    'da qui: nessun movimento di 5.7 dal punto 4022 (4017-4028) entro 21:00: 55% (131/240)'],
  MNQ: ["chiusura sotto l'apertura 29231: 54% (37/69) · mediana 29099", "chiusura sopra l'apertura 29231: 46% (32/69) · mediana 29391"],
  MES: ["mai ritorno all'apertura 7683 entro 21:00: 19 su 20, pochi casi · mediana dell'estensione 7728"],
  M2K: ["nessun 4.6 sotto l'apertura (2785) entro 21:00: 30 su 31, pochi casi", "  poi chiusura sopra l'apertura 2789: 29 su 30, pochi casi · mediana 2818",
    "chiusura sopra l'apertura 2789: 29 su 31, pochi casi · mediana 2818"],
  MYM: ["chiusura sopra l'apertura 52643: 53% (34/64) · mediana 52752", "chiusura sotto l'apertura 52643: 47% (30/64) · mediana 52517"],
}

describe('vista sulle fixture reali', () => {
  it('esiti come il riquadro del Trader, righe da qui comprese (riferimento, arrotondamento, pochi casi), con ±m D8', () => {
    for (const [s, attesi] of Object.entries(TRADER)) {
      const righe = righeEsiti(v(s)).map((r) => r.testo.replace(/ ±\d+/, ''))
      expect(righe).toEqual(attesi.map((t) => t.replace(/^(da qui: )? {2}poi /, '$1poi ')))
    }
    expect(righeEsiti(v('MGC')).filter((r) => r.id.startsWith('da-qui-')).map((r) => r.id)).toEqual(['da-qui-q1'])
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
    const x = vista(s, scen.barre.MES, fr('MES'), false, scen.orari)
    expect(x.inTesto).toBe(true)
    expect(righeTesto(x)[0]).toMatch(/^radice 20:08 primo movimento a 7711.*albero in testo$/)
    expect(righeTesto(x)[1]).toMatch(/^ {2}estensione \+65 25% \(5\/20 ±19\) a 7748.69 verso le /)
  })
  it('albero in testo di da qui: la radice di da_qui non ha `fase`, la riga non stampa "undefined"', () => {
    const dq = sc('MGC').da_qui!
    expect('fase' in dq.radice).toBe(false) // il payload reale: la radice di da_qui non porta la fase
    const s = { ...sc('MGC'), da_qui: { ...dq, radice: { ...dq.radice, t: '2026-10-27T14:30+01:00' } } }
    const x = vista(s, scen.barre.MGC, fr('MGC'), true, scen.orari)
    expect(x.daQui!.inTesto).toBe(true)
    const riga = righeTesto(x).find((r) => r.startsWith('da qui: radice'))
    expect(riga).toBe("da qui: radice 20:08 a 4022.4: oltre 2 ore dopo l'ultima barra, albero in testo")
    expect(righeTesto(x).join('\n')).not.toContain('undefined')
  })
  it('ora degli esiti senza orizzonte = chiusura del payload (21:00), mai 22:00', () => {
    const s = structuredClone(sc('MES'))
    delete s.rami[0].orizzonte
    const righe = righeEsiti(vista(s, scen.barre.MES, fr('MES'), false, scen.orari))
    expect(righe[0].testo).toBe("mai ritorno all'apertura 7683 entro 21:00: 19 su 20, pochi casi · mediana dell'estensione 7728")
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
    expect(screen.getAllByRole('heading', { level: 2 }).map((h) => h.textContent)).toEqual(['STATO', 'FINESTRE', 'LIVELLI', "CASO DELL'APERTURA", 'LENTI', 'CONCORDANZA'])
    const riga = (nome: string) => screen.getAllByRole('row').find((r) => within(r).queryAllByRole('cell')[0]?.textContent === nome)!
    expect(within(riga('massimo notte')).getAllByRole('cell').map((c) => c.textContent))
      .toEqual(['massimo notte', '4039.40', '+16.20', '+0.38', '0.30-0.50 A', '-', '10% (3/31 ±10)'])
    expect(within(riga('minimo notte')).getAllByRole('cell')[6].textContent).toBe('0 su 68')
    expect(within(riga('L1 VWAP notte')).getAllByRole('cell')[7].textContent).toBe('3% (8/271 ±2) v')
    expect(screen.getByText(fr('MGC').lenti!.concordanza!.frase!)).toBeInTheDocument()
    const corrente = fr('MGC').finestre.find((w) => w.corrente)!
    expect(screen.getByText(`> ${corrente.finestra}`, { exact: false })).toBeInTheDocument()
  })
  it('orari del payload nei titoli e nelle note (14:30-21:00 questa settimana), testo del pannello completo', () => {
    const { container } = render(<TabellePannello r={fr('MGC')} orari={freq.orari} />)
    const teste = screen.getAllByRole('columnheader').map((h) => h.textContent)
    expect(teste).toContain('entro 14:30')
    expect(teste).toContain('entro 21:00')
    expect(teste.some((t) => /15:30|22:00/.test(t ?? ''))).toBe(false)
    const testo = container.textContent ?? ''
    expect(testo).toContain('tocco entro le 14:30 e le 21:00 nelle ultime 250 sessioni')
    expect(testo).toContain('entro le 21:00, 0.3 A = 13 punti; margine = max(1,96 sqrt(p(1-p)/n), 3/n)')
    expect(testo).toContain('range medio 14:30-21:00 delle ultime 20 sessioni')
    expect(teste).toContain('oggi dalle 00:00 max / min')
    expect(teste).toContain('notte 00:00-14:29 max / min')
    expect(teste).toContain('sessione dalle 14:30 max / min')
  })
  it('campi malformati del pannello (percorso, storico, lenti) ripuliti in validazione: la tabella si mostra', () => {
    const f = copia(frequenzeJson)
    const ap = f.dati.strumenti.MGC.apertura as Rec
    ;(ap.percorso as Rec).direzione = 5
    ;((ap.storico as Rec).frequenze as Rec)["chiusura sopra l'apertura"] = 3
    ;(f.dati.strumenti.MGC.lenti as Rec).righe = 'x'
    const r = validaFrequenze(f).dati!.strumenti.MGC as StrumentoFrequenze
    render(<TabellePannello r={r} orari={freq.orari} />)
    expect(screen.getByText('oggi: nessuna barra della sessione')).toBeInTheDocument()
    const riga = screen.getAllByRole('row').find((x) => within(x).queryAllByRole('cell')[0]?.textContent === "chiusura sopra l'apertura")!
    expect(within(riga).getAllByRole('cell')[1].textContent).toBe('n/d (0 casi)')
    expect(screen.queryByText('L1 VWAP notte')).toBeNull()
    expect(screen.getByText('tutte le sessioni')).toBeInTheDocument()
  })
  it('frequenza senza casi: "n/d (0 casi)" come il pannello', () => {
    const r = structuredClone(fr('MGC'))
    r.lenti!.base!.nuovo_minimo = { p: null, k: 0, n: 0, margine: null }
    render(<TabellePannello r={r} orari={freq.orari} />)
    const base = screen.getAllByRole('row').find((x) => within(x).queryAllByRole('cell')[0]?.textContent === 'tutte le sessioni')!
    expect(within(base).getAllByRole('cell')[4].textContent).toBe('n/d (0 casi)')
  })
})

describe('stato e freschezza', () => {
  const base = { isError: false, dataUpdatedAt: Date.UTC(2026, 9, 26, 19, 8), errorUpdatedAt: Date.UTC(2026, 9, 26, 19, 9) }
  const t0 = base.dataUpdatedAt
  it('messaggi', () => {
    expect(avvisi({ ...base, data: { ricevuto: null, eta_s: null, dati: null } }, 60, t0)).toEqual(['Nessun dato dal motore (spento, o non ha ancora pubblicato).'])
    expect(avvisi({ ...base, data: { ricevuto: 'x', eta_s: 60, dati: {} } }, 60, t0)).toEqual([])
    expect(avvisi({ ...base, data: { ricevuto: 'x', eta_s: 61, dati: {} } }, 60, t0)).toEqual(['Motore spento o scollegato da 1 minuto'])
    expect(avvisi({ ...base, data: { ricevuto: 'x', eta_s: 600, dati: {} } }, 180, t0)).toEqual(['Motore spento o scollegato da 10 minuti'])
    expect(avvisi({ ...base, isError: true, data: { ricevuto: 'x', eta_s: 5, dati: {} } }, 60, t0))
      .toEqual(['Aggiornamento fallito alle 20:09; ultimo caricamento riuscito alle 20:08'])
  })
  it('richiesta fallita e dati oltre la soglia: "dati vecchi", non "motore spento" (il guasto puo essere della rete)', () => {
    expect(avvisi({ ...base, isError: true, data: { ricevuto: 'x', eta_s: 600, dati: {} } }, 60, t0))
      .toEqual(['Aggiornamento fallito alle 20:09; ultimo caricamento riuscito alle 20:08', 'Dati vecchi di 10 minuti'])
  })
  it('l eta avanza con l orologio dall ultimo caricamento riuscito, anche se la richiesta resta appesa', () => {
    const q = { ...base, data: { ricevuto: 'x', eta_s: 10, dati: {} } }
    expect(etaCorrente(q, t0 + 30_000)).toBe(40)
    expect(avvisi(q, 60, t0 + 30_000)).toEqual([])
    expect(avvisi(q, 60, t0 + 120_000)).toEqual(['Motore spento o scollegato da 2 minuti'])
    expect(etaCorrente({ ...base, data: { ricevuto: null, eta_s: null, dati: null } }, t0)).toBeNull()
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
  it('righe esiti con chiave stabile: un numero che cambia aggiorna la riga, non la rimonta', () => {
    const { rerender } = render(<Esiti righe={[{ id: 'r1', testo: 'chiusura sopra: 52% (46/88 ±10)' }]} />)
    const prima = screen.getByRole('listitem')
    rerender(<Esiti righe={[{ id: 'r1', testo: 'chiusura sopra: 53% (47/88 ±10)' }]} />)
    expect(screen.getByRole('listitem')).toBe(prima)
    expect(prima.textContent).toBe('chiusura sopra: 53% (47/88 ±10)')
  })
})

/** The chart's width (ParentSize reads clientWidth in jsdom) and the viewport's md breakpoint (matchMedia), together. */
function schermo(largo: number, alto: number) {
  vi.spyOn(HTMLElement.prototype, 'clientWidth', 'get').mockReturnValue(largo)
  vi.spyOn(HTMLElement.prototype, 'clientHeight', 'get').mockReturnValue(alto)
  vi.stubGlobal('matchMedia', (q: string) => ({ matches: largo >= 768, media: q, addEventListener() {}, removeEventListener() {} }))
}

/** Every overlay label or number: within one row (12 px) of its anchor, never above the plot. */
function ancorate(container: HTMLElement) {
  const testi = [...container.querySelectorAll('.chl-sovrapposizione text[data-ancora]')]
  expect(testi.length).toBeGreaterThan(0)
  for (const t of testi) {
    const y = Number(t.getAttribute('y'))
    expect(Math.abs(y - Number(t.getAttribute('data-ancora'))), t.textContent ?? '').toBeLessThanOrEqual(12)
    expect(y, t.textContent ?? '').toBeGreaterThanOrEqual(0)
  }
}

const legenda = () => within(within(screen.getByRole('figure')).getByRole('list')).getAllByRole('listitem')

describe('grafico e pagina', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    vi.unstubAllGlobals()
  })

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

  it('telefono: rami e radici come numeri accanto ai capi, legenda visibile con una riga per segmento disegnato', () => {
    schermo(343, 400)
    const { container } = render(<GraficoLive v={v('MGC')} />)
    const testi = [...container.querySelectorAll('.chl-sovrapposizione text')].map((t) => t.textContent ?? '')
    expect(testi.some((t) => t.startsWith('da qui: ') || t.startsWith('20:08 '))).toBe(false)
    const numeri = testi.filter((t) => /^\d+$/.test(t))
    expect(numeri.length).toBe(2 + 3)
    const voci = legenda()
    expect(within(screen.getByRole('figure')).getByRole('list').className).not.toMatch(/(^| )sr-only/)
    for (const n of numeri) expect(voci.some((li) => li.textContent?.startsWith(`${n} · `)), n).toBe(true)
    const segmenti = voci.map((li) => li.textContent ?? '').filter((t) => / verso le \d\d:\d\d$/.test(t))
    expect(segmenti).toEqual(v('MGC').daQui!.g.segmenti.map((s) => expect.stringMatching(new RegExp(`^\\d+ · da qui: .* a ${s.a.prezzo} verso le `))))
    expect(segmenti).toContain('5 · da qui: poi estensione +6 76% (40/53 ±12) a 4028.88 verso le 20:31')
    ancorate(container)
    const ore = [...container.querySelectorAll('.chl-sovrapposizione text')].filter((t) => /^\d\d:\d\d$/.test(t.textContent ?? '')).map((t) => Number(t.getAttribute('x')))
    expect(ore.length).toBeGreaterThan(2)
    for (let i = 1; i < ore.length; i++) expect(ore[i] - ore[i - 1]).toBeGreaterThanOrEqual(44)
  })

  it('telefono: etichette e numeri mai sovrapposti, tutti >= 11 px, orari del payload nella didascalia', () => {
    schermo(343, 400)
    const { container } = render(<GraficoLive v={v('MGC')} />)
    const testi = [...container.querySelectorAll('.chl-sovrapposizione text')]
    for (const t of testi) expect(Number(t.getAttribute('font-size'))).toBeGreaterThanOrEqual(11)
    const scatole = testi.filter((t) => !/^\d\d:\d\d$/.test(t.textContent ?? '')).map((t) => {
      const x = Number(t.getAttribute('x'))
      const w = (t.textContent ?? '').length * 6
      const a = t.getAttribute('text-anchor')
      const x0 = a === 'end' ? x - w : a === 'middle' ? x - w / 2 : x
      return { y: Number(t.getAttribute('y')), x0, x1: x0 + w, testo: t.textContent }
    })
    for (let i = 0; i < scatole.length; i++) {
      for (let j = i + 1; j < scatole.length; j++) {
        const [a, b] = [scatole[i], scatole[j]]
        expect(Math.abs(a.y - b.y) < 11 && a.x0 < b.x1 && b.x0 < a.x1, `${a.testo} | ${b.testo}`).toBe(false)
      }
    }
    expect(container.querySelector('figcaption')!.textContent).toContain('entro le 21:00')
    ancorate(container)
  })

  it('da md in su: etichette in linea come prima, nessun numero, legenda solo per i lettori di schermo', () => {
    schermo(900, 450)
    const { container } = render(<GraficoLive v={v('MGC')} />)
    const testi = [...container.querySelectorAll('.chl-sovrapposizione text')].map((t) => t.textContent ?? '')
    expect(testi).toContain('da qui: estensione +6 76% (40/53 ±12)')
    expect(testi.filter((t) => /^\d+$/.test(t))).toEqual([])
    for (const li of legenda()) expect(li.className).toContain('md:sr-only')
    ancorate(container)
  })

  it('da md in su: un etichetta che dovrebbe salire di piu di una riga diventa un numero, visibile in legenda', () => {
    schermo(900, 450)
    const s = structuredClone(sc('MES'))
    s.rami = [0, 1, 2, 3].map((i) => ({ id: `x${i}`, padre: null, tipo: 'primo_movimento', etichetta: 'primo movimento di 8 su', prezzo: 7720, p: 0.5 - i * 0.05,
      k: 10 - i, n: 20, margine: 0.2, orizzonte: '21:00', minuti: { mediana: 30 + i, q1: 20, q3: 40 }, tocco: true, omessi: 0 }))
    const { container } = render(<GraficoLive v={vista(s, scen.barre.MES, fr('MES'), false, scen.orari)} />)
    const testi = [...container.querySelectorAll('.chl-sovrapposizione text')].map((t) => t.textContent ?? '')
    const numeri = testi.filter((t) => /^\d+$/.test(t))
    expect(numeri.length).toBeGreaterThan(0)
    expect(testi.filter((t) => t.startsWith('8 su ')).length).toBeLessThan(4)
    const visibili = legenda().filter((li) => !li.className.includes('md:sr-only')).map((li) => li.textContent ?? '')
    expect(visibili.map((t) => t.split(' · ')[0]).sort()).toEqual([...numeri].sort())
    expect(visibili.some((t) => /^\d+ · 8 su \d+% \(\d+\/20 ±20\) a 7720 verso le /.test(t))).toBe(true)
    ancorate(container)
  })

  it('accessibile: legenda con radice, rami disegnati e livelli (l SVG di Bklit e aria-hidden); in linea = pallino, nessun numero', () => {
    schermo(900, 450)
    render(<GraficoLive v={v('MGC')} />)
    const voci = legenda().map((li) => li.textContent)
    expect(voci).toContain('• da qui: primo movimento di 5.7 su da qui 22% (53/240 ±5) a 4028.1 verso le 20:28')
    expect(voci).toContain('• livello massimo notte 4039.4: 10% (3/31 ±10)')
    expect(voci[0]?.startsWith('• radice 20:08 estensione a 4022.4')).toBe(true)
  })

  it('telefono (343 px): ogni numero della legenda compare anche sul grafico; i livelli in linea hanno il pallino', () => {
    schermo(343, 400)
    const { container } = render(<GraficoLive v={v('MGC')} />)
    const sulGrafico = [...container.querySelectorAll('.chl-sovrapposizione text')].map((t) => t.textContent ?? '').filter((t) => /^\d+$/.test(t))
    const voci = legenda().map((li) => li.textContent ?? '')
    const numeriLegenda = voci.map((t) => /^(\d+) · /.exec(t)?.[1]).filter((n): n is string => n != null)
    expect(numeriLegenda.length).toBeGreaterThan(0)
    expect([...numeriLegenda].sort()).toEqual([...sulGrafico].sort())
    const livelli = voci.filter((t) => t.includes('livello '))
    expect(livelli.length).toBe(v('MGC').livelli.length)
    for (const t of livelli) expect(t, t).toMatch(sulGrafico.some((n) => t.startsWith(`${n} · `)) ? /^\d+ · livello / : /^• livello /)
  })

  it('telefono: 8 capi sullo stesso punto, i numeri senza posto restano all ancora, dentro il plot', () => {
    schermo(343, 400)
    const s = structuredClone(sc('MES'))
    s.rami = Array.from({ length: 8 }, (_, i) => ({ id: `y${i}`, padre: null, tipo: 'primo_movimento', etichetta: 'primo movimento di 8 su', prezzo: 7720,
      p: 0.5 - i * 0.02, k: 10 - i, n: 20, margine: 0.2, orizzonte: '21:00', minuti: { mediana: 30, q1: 20, q3: 40 }, tocco: true, omessi: 0 }))
    const { container } = render(<GraficoLive v={vista(s, scen.barre.MES, fr('MES'), false, scen.orari)} />)
    const numeri = [...container.querySelectorAll('.chl-sovrapposizione text')].filter((t) => /^\d+$/.test(t.textContent ?? ''))
    // radice + 8 rami: tutti come numeri, anche quelli che non trovano posto (forzati all'ancora)
    expect(numeri.length).toBeGreaterThanOrEqual(9)
    const fondo = 400 - 16 - 28 + 6 // innerHeight + 6, come impila(): altezza meno margini top/bottom
    for (const t of numeri) {
      const y = Number(t.getAttribute('y'))
      expect(y, t.textContent ?? '').toBeGreaterThanOrEqual(11)
      expect(y, t.textContent ?? '').toBeLessThanOrEqual(fondo)
    }
    ancorate(container)
    const voci = legenda().map((li) => li.textContent ?? '')
    for (const t of numeri) expect(voci.some((x) => x.startsWith(`${t.textContent} · `)), t.textContent ?? '').toBe(true)
  })

  it('payload con prezzi non numerici: il ramo non e disegnato, nessun NaN nel grafico', () => {
    vi.spyOn(HTMLElement.prototype, 'clientWidth', 'get').mockReturnValue(900)
    vi.spyOn(HTMLElement.prototype, 'clientHeight', 'get').mockReturnValue(450)
    const s = copia(scenariJson)
    ;(s.dati.strumenti.MES.rami as Rec[])[1].prezzo = 'x'
    ;(s.dati.strumenti.MES.livelli as Rec[])[0].prezzo = 'y'
    const d = validaScenari(s).dati!
    const { container } = render(<GraficoLive v={vista(d.strumenti.MES as StrumentoScenari, d.barre.MES, fr('MES'), false, d.orari)} />)
    expect([...container.querySelectorAll('.chl-sovrapposizione text')].some((t) => t.textContent?.includes('estensione +65'))).toBe(false)
    for (const el of container.querySelectorAll('svg *')) {
      for (const a of el.getAttributeNames()) expect(el.getAttribute(a), `${el.tagName} ${a}`).not.toMatch(/NaN/)
    }
  })

  it('albero in testo: niente rami disegnati e asse dei tempi fermo ai 36 slot futuri', () => {
    vi.spyOn(HTMLElement.prototype, 'clientWidth', 'get').mockReturnValue(900)
    vi.spyOn(HTMLElement.prototype, 'clientHeight', 'get').mockReturnValue(450)
    const s = { ...sc('MES'), radice: { ...sc('MES').radice, t: '2026-10-27T14:30+01:00' } }
    const { container } = render(<GraficoLive v={vista(s, scen.barre.MES, fr('MES'), false, scen.orari)} />)
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

  it('pagina con barre del principale non lista: le schede restano, il grafico dice che mancano le barre', async () => {
    const s = copia(scenariJson)
    s.dati.barre.MGC.righe = {}
    s.dati.barre.MGC.viva = null
    vi.spyOn(globalThis, 'fetch').mockImplementation(async (u) =>
      new Response(JSON.stringify(String(u).endsWith('/live/scenari') ? s : frequenzeJson), { status: 200 }))
    render(<QueryClientProvider client={new QueryClient()}><Live /></QueryClientProvider>)
    expect(await screen.findByRole('tab', { name: /MGC/ })).toBeInTheDocument()
    expect(await screen.findByText('Nessuna barra a 5 minuti per questo strumento.')).toBeInTheDocument()
  })

  it('pagina con scenari senza principale: le tabelle restano, il canale dice che il caricamento e fallito', async () => {
    const s = copia(scenariJson)
    delete s.dati.principale
    vi.spyOn(globalThis, 'fetch').mockImplementation(async (u) =>
      new Response(JSON.stringify(String(u).endsWith('/live/scenari') ? s : frequenzeJson), { status: 200 }))
    render(<QueryClientProvider client={new QueryClient()}><Live /></QueryClientProvider>)
    await waitFor(() => expect(screen.getByText(/Grafico e albero:/).parentElement!.textContent).toMatch(/Aggiornamento fallito/))
    expect(await screen.findByText('STATO')).toBeInTheDocument()
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
