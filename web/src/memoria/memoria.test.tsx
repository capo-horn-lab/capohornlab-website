import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { existsSync, readFileSync } from 'node:fs'
import { render, renderHook, screen, waitFor, within } from '@testing-library/react'
import type { ReactNode } from 'react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { useMemoria } from '@/lib/api'
import { type Memoria, RispostaNonValida, validaMemoria } from '@/lib/tipi'
import { avvisi } from '@/live/AvvisoFreschezza'
import { testoAvviso } from '@/memoria/avviso'
import { FAMIGLIE, QUANDO } from '@/memoria/contenuto'
import { VerdettoGruppoBadge } from '@/memoria/VerdettoGruppoBadge'
import Memoria_ from '@/pagine/Memoria'
import fixture from '@/test/fixtures/memoria.json'

const AVVISO =
  'Nessun valore predittivo dimostrato: tutti i gruppi sono DESCRITTIVI. Conteggi e verifiche descrivono dati già visti, non segnali.'

type Rec = Record<string, unknown>
/** Scende nel JSON per chiavi (cast mirato: il payload di prova e' un albero di oggetti). */
const nodo = (b: Rec, ...percorso: string[]) => percorso.reduce<Rec>((o, k) => o[k] as Rec, b)
const verdettiDi = (b: Rec) => nodo(b, 'dati', 'verdetti', 'verdetti')
const gruppoDi = (b: Rec, k: string) => verdettiDi(b)[k] as Rec
// classi di colore direzionale o di allarme (le varianti aria-invalid del Badge non contano: sono dello stato di un campo)
const COLORE_VIETATO = /(^|[-:/])(destructive|success|danger|green|red|emerald|rose|warm)([-/]|$)|^bg-primary/
const colori = (classe: string) => classe.split(/\s+/).filter((c) => !c.includes('aria-invalid') && COLORE_VIETATO.test(c))
const copia = () => structuredClone(fixture) as unknown as Rec
const gruppi = Object.entries(fixture.dati.verdetti.verdetti as unknown as Record<string, Rec & { verdetto: string; n: number; orizzonte: number; metrica: string; p_minimo: number; frase: string }>)
const LEDGER = 'C:\\Users\\farne\\TradingAgent-NinjaTrader\\docs\\EXECUTION_LEDGER.md'
const MOTORE_PY = 'C:\\Users\\farne\\TradingAgent-NinjaTrader\\src\\trading_stack\\memoria_mercato.py'
const COMUNE = 'Conteggi e verifiche descrivono dati già visti, non segnali.'
/** Imposta il verdetto di alcuni gruppi (per indice) sulla copia della fixture. */
function conVerdetti(b: Rec, assegna: Record<number, string>) {
  for (const [i, v] of Object.entries(assegna)) gruppoDi(b, gruppi[Number(i)][0]).verdetto = v
  return b
}

function monta(risposta: (() => Promise<unknown>) | unknown) {
  const fetchMock = vi.fn(async () => {
    const corpo = typeof risposta === 'function' ? await (risposta as () => Promise<unknown>)() : risposta
    return { ok: true, status: 200, json: async () => corpo }
  })
  vi.stubGlobal('fetch', fetchMock)
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  const r = render(
    <QueryClientProvider client={client}>
      <Memoria_ />
    </QueryClientProvider>,
  )
  return { ...r, fetchMock, client }
}

const regione = (nome: string) => screen.getByRole('region', { name: nome })
const voce = (radice: HTMLElement, etichetta: string) => within(radice).getByText(etichetta).nextElementSibling?.textContent

afterEach(() => vi.unstubAllGlobals())

describe('avviso fisso', () => {
  it('testo esatto, in testa alla pagina, prima di qualunque sezione, con i dati assenti (richiesta che non risponde)', async () => {
    monta(() => new Promise(() => {}))
    const avviso = screen.getByText(AVVISO)
    expect(avviso).toBeInTheDocument()
    const primaSezione = screen.getAllByRole('heading', { level: 2 })[0]
    expect(avviso.compareDocumentPosition(primaSezione) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy()
    expect(screen.getByRole('heading', { level: 1, name: 'Memoria del mercato' })).toBeInTheDocument()
    // le definizioni (testo statico) ci sono anche senza dati
    expect(screen.getByRole('region', { name: 'Che cosa riconosce' })).toBeInTheDocument()
  })

  // il 503 passa dal nuovo tentativo dopo 3 s (retryDelay della query): il test ha un tempo proprio, piu' lungo del default
  it('presente anche con errore di rete (503) e con dati nulli (motore mai connesso)', { timeout: 15_000 }, async () => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: false, status: 503, json: async () => ({}) })))
    const { unmount } = render(
      <QueryClientProvider client={new QueryClient({ defaultOptions: { queries: { retry: false } } })}>
        <Memoria_ />
      </QueryClientProvider>,
    )
    expect(await screen.findByText(/Servizio non raggiungibile/)).toBeInTheDocument()
    expect(screen.getByText(AVVISO)).toBeInTheDocument()
    unmount()
    monta({ ricevuto: null, eta_s: null, dati: null })
    expect(await screen.findByText(/Nessun dato dal motore/)).toBeInTheDocument()
    expect(screen.getByText(AVVISO)).toBeInTheDocument()
  })

  const verdettiCon = (assegna: Record<number, string>) => verdettiDi(conVerdetti(copia(), assegna)) as never

  it('(a) tutti DESCRITTIVI, senza dati o con un elenco vuoto: "tutti i gruppi sono DESCRITTIVI"', () => {
    expect(testoAvviso(null)).toBe(AVVISO)
    expect(testoAvviso(undefined)).toBe(AVVISO)
    expect(testoAvviso({})).toBe(AVVISO)
    expect(testoAvviso(verdettiCon({}))).toBe(AVVISO)
  })

  it('(b) nessun CONFERMATO ma qualche NON CONFERMATO: "N gruppi su M sono DESCRITTIVI, K NON CONFERMATI"', () => {
    expect(testoAvviso(verdettiCon({ 0: 'NON CONFERMATO', 3: 'NON CONFERMATO' }))).toBe(
      `Nessun valore predittivo dimostrato: 8 gruppi su 10 sono DESCRITTIVI, 2 NON CONFERMATI. ${COMUNE}`,
    )
  })

  it('(c) almeno un CONFERMATO: "Verifica statistica: K gruppi su M CONFERMATI secondo la rubrica registrata (vedi tabella), N DESCRITTIVI"', () => {
    expect(testoAvviso(verdettiCon({ 0: 'NON CONFERMATO', 1: 'CONFERMATO' }))).toBe(
      `Verifica statistica: 1 gruppo su 10 CONFERMATO secondo la rubrica registrata (vedi tabella), 8 DESCRITTIVI, 1 NON CONFERMATO. Conteggi e verifiche descrivono dati già visti, non segnali: nessuna indicazione operativa.`,
    )
    expect(testoAvviso(verdettiCon({ 1: 'CONFERMATO', 2: 'CONFERMATO', 4: 'NON CONFERMATO', 5: 'NON CONFERMATO' }))).toBe(
      `Verifica statistica: 2 gruppi su 10 CONFERMATI secondo la rubrica registrata (vedi tabella), 6 DESCRITTIVI, 2 NON CONFERMATI. ${COMUNE.replace('segnali.', 'segnali: nessuna indicazione operativa.')}`,
    )
    expect(testoAvviso(verdettiCon({ 0: 'CONFERMATO' }))).toBe(
      `Verifica statistica: 1 gruppo su 10 CONFERMATO secondo la rubrica registrata (vedi tabella), 9 DESCRITTIVI. ${COMUNE.replace('segnali.', 'segnali: nessuna indicazione operativa.')}`,
    )
  })

  it('concordanza singolare: 1 DESCRITTIVO, 1 NON CONFERMATO', () => {
    const nove = { 0: 'NON CONFERMATO', 1: 'NON CONFERMATO', 2: 'NON CONFERMATO', 3: 'NON CONFERMATO', 4: 'NON CONFERMATO', 5: 'NON CONFERMATO', 6: 'NON CONFERMATO', 7: 'NON CONFERMATO', 8: 'NON CONFERMATO' }
    expect(testoAvviso(verdettiCon(nove))).toBe(
      `Nessun valore predittivo dimostrato: 1 gruppo su 10 è DESCRITTIVO, 9 NON CONFERMATI. ${COMUNE}`,
    )
    expect(testoAvviso(verdettiCon({ 0: 'NON CONFERMATO' }))).toBe(
      `Nessun valore predittivo dimostrato: 9 gruppi su 10 sono DESCRITTIVI, 1 NON CONFERMATO. ${COMUNE}`,
    )
  })

  it('nella pagina: caso (a) con la fixture, caso (b) e caso (c) con la fixture modificata in memoria', async () => {
    const a = monta(fixture)
    await screen.findByRole('table', { name: 'Verdetti per gruppo' })
    expect(screen.getByText(AVVISO)).toBeInTheDocument()
    a.unmount()

    const b = monta(conVerdetti(copia(), { 0: 'NON CONFERMATO' }))
    expect(await screen.findByText(`Nessun valore predittivo dimostrato: 9 gruppi su 10 sono DESCRITTIVI, 1 NON CONFERMATO. ${COMUNE}`)).toBeInTheDocument()
    expect(screen.queryByText(/tutti i gruppi sono DESCRITTIVI/)).toBeNull()
    b.unmount()

    monta(conVerdetti(copia(), { 0: 'CONFERMATO' }))
    expect(await screen.findByText(/^Verifica statistica: 1 gruppo su 10 CONFERMATO secondo la rubrica registrata \(vedi tabella\), 9 DESCRITTIVI\./)).toBeInTheDocument()
    expect(screen.queryByText(/Nessun valore predittivo dimostrato/)).toBeNull()
  })
})

describe('che cosa riconosce', () => {
  it('tre famiglie, definizioni copiate dal registro con la Fonte accanto, nessun testo a mano nel JSX', async () => {
    monta(fixture)
    const sez = regione('Che cosa riconosce')
    expect(FAMIGLIE.map((f) => f.titolo)).toEqual(['Assorbimento', 'Liquidità: muro e ritiro', 'Order flow: flusso con esito e senza esito'])
    for (const f of FAMIGLIE) {
      expect(within(sez).getByRole('heading', { level: 3, name: f.titolo })).toBeInTheDocument()
      expect(f.definizioni.length).toBeGreaterThan(0)
      for (const d of f.definizioni) {
        expect(within(sez).getByText(d.testo)).toBeInTheDocument()
        expect(d.fonte).toMatch(/^(docs\/EXECUTION_LEDGER\.md#L\d+|src\/trading_stack\/memoria_mercato\.py#L\d+(-L\d+)?)$/)
        expect(within(sez).getAllByText(d.fonte).length).toBeGreaterThan(0)
      }
    }
    expect(FAMIGLIE[0].definizioni[0].testo).toMatch(/^Definizione dichiarata: finestra 30 s valutata ogni 5 s,/)
    expect(FAMIGLIE[0].definizioni[0].fonte).toBe('docs/EXECUTION_LEDGER.md#L10998')
  })

  it('liquidità: prima la docstring del codice (ritiro L71-L79, muro L80-L81), poi la registrazione L11002 e le ricalibrazioni L11009', async () => {
    monta(fixture)
    const sez = regione('Che cosa riconosce')
    const liq = FAMIGLIE.find((f) => f.id === 'liquidita')!
    const fonti = liq.definizioni.map((d) => d.fonte)
    expect(fonti).toEqual([
      'src/trading_stack/memoria_mercato.py#L71-L79',
      'src/trading_stack/memoria_mercato.py#L80-L81',
      'docs/EXECUTION_LEDGER.md#L11002',
      'docs/EXECUTION_LEDGER.md#L11009',
    ])
    expect(liq.definizioni.some((d) => d.fonte.startsWith('src/trading_stack/memoria_mercato.py#L'))).toBe(true)
    expect(liq.definizioni[0].testo).toContain("A PARITA' DI PREZZO")
    expect(liq.definizioni[2].etichetta).toBe('registrazione prima del codice')
    // docstring e ricalibrazione concordano (MURO_MIN_SIZE 25 dal 29/10/2026): nessuna nota di discrepanza
    expect(liq.nota).toBeUndefined()
    expect(within(sez).queryByText(/docstring riporta/)).toBeNull()
    expect(within(sez).getByText('registrazione prima del codice')).toBeInTheDocument()
    expect(within(sez).getByText(/A PARITA' DI PREZZO/)).toBeInTheDocument()
    expect(liq.definizioni[1].testo).toContain('MURO_MIN_SIZE (25)')
    expect(liq.definizioni[1].testo).not.toContain('(100)')
    expect(liq.definizioni[3].testo).toContain('MURO_MIN_SIZE 25')
  })

  const righe = (percorso: string) => (existsSync(percorso) ? readFileSync(percorso, 'utf8').split(/\r?\n/) : null)
  // il testo delle definizioni = le righe citate del file sorgente, con a-capo e rientri ridotti a uno spazio
  const norm = (s: string) => s.replace(/\s+/g, ' ').trim()

  it.skipIf(!existsSync(LEDGER))('le definizioni da registro stanno alla riga citata del registro', () => {
    const r = righe(LEDGER)!
    for (const d of FAMIGLIE.flatMap((f) => f.definizioni).concat(QUANDO)) {
      const m = d.fonte.match(/^docs\/EXECUTION_LEDGER\.md#L(\d+)$/)
      if (!m) continue
      expect(norm(r[Number(m[1]) - 1]), d.fonte).toContain(norm(d.testo))
    }
  })

  it.skipIf(!existsSync(MOTORE_PY))('le citazioni della docstring sono le righe citate del codice del motore', () => {
    const r = righe(MOTORE_PY)!
    const citazioni = FAMIGLIE.flatMap((f) => f.definizioni).filter((d) => d.fonte.startsWith('src/trading_stack/memoria_mercato.py#L'))
    expect(citazioni).toHaveLength(2)
    for (const d of citazioni) {
      const [, da, a] = d.fonte.match(/#L(\d+)-L(\d+)$/)!
      expect(norm(r.slice(Number(da) - 1, Number(a)).join(' ')), d.fonte).toContain(norm(d.testo))
    }
  })
})

describe('eventi nella memoria (fixture reale)', () => {
  it('strumento, ultimo giro in ora di Roma, nuovi e diagnostica come nel payload', async () => {
    monta(fixture)
    const sez = await screen.findByRole('region', { name: 'Eventi nella memoria' })
    await within(sez).findByText('MNQ 12-26')
    expect(voce(sez, 'Strumento')).toBe('MNQ 12-26')
    expect(voce(sez, 'Ultimo giro (ora di Roma)')).toBe('29/10/2026 11:03') // 10:03 UTC, CET dal 25/10
    expect(voce(sez, "Eventi nuovi nell'ultimo giro")).toBe('1')
    expect(voce(sez, 'Libro caldo')).toBe('98.5%')
    expect(voce(sez, 'Scambi con verso')).toBe('841784')
    expect(voce(sez, 'Scambi ambigui')).toBe('0')
    expect(voce(sez, 'Record L2')).toBe('41987359')
    expect(voce(sez, 'Salti a freddo')).toBe('2683')
    expect(voce(sez, 'Quota scambi ambigui')).toBe('0.0%') // quota_ambigui del payload
  })

  it('la quota di scambi ambigui e il libro caldo vengono dal payload, mai da un rapporto calcolato nel sito; assenti -> "-"', async () => {
    // interi che darebbero 0% se il codice facesse il rapporto: la quota del payload (0.5) deve comparire comunque
    const b = copia()
    const diag = nodo(b, 'dati', 'stato', 'diagnostica')
    diag.quota_ambigui = 0.5
    diag.scambi_ambigui = 0
    const { unmount } = monta(b)
    const sez = await screen.findByRole('region', { name: 'Eventi nella memoria' })
    await within(sez).findByText('MNQ 12-26')
    expect(voce(sez, 'Quota scambi ambigui')).toBe('50.0%')
    expect(voce(sez, 'Scambi ambigui')).toBe('0')
    unmount()

    const senza = copia()
    const d2 = nodo(senza, 'dati', 'stato', 'diagnostica')
    delete d2.quota_ambigui
    delete d2.quota_libro_caldo
    monta(senza)
    const sez2 = await screen.findByRole('region', { name: 'Eventi nella memoria' })
    await within(sez2).findByText('MNQ 12-26')
    expect(voce(sez2, 'Quota scambi ambigui')).toBe('-')
    expect(voce(sez2, 'Libro caldo')).toBe('-')
  })

  it('diagnostica assente: tutte le voci "-" (interi compresi), pagina in piedi', async () => {
    const b = copia()
    delete nodo(b, 'dati', 'stato').diagnostica
    monta(b)
    const sez = await screen.findByRole('region', { name: 'Eventi nella memoria' })
    await within(sez).findByText('MNQ 12-26')
    for (const e of ['Libro caldo', 'Quota scambi ambigui', 'Scambi con verso', 'Scambi ambigui', 'Record L2', 'Salti a freddo']) expect(voce(sez, e), e).toBe('-')
  })

  it('totale nel database: 5 righe con i numeri della fixture; oggi: 4 righe e totale 446', async () => {
    monta(fixture)
    const totale = await screen.findByRole('table', { name: 'Totale nel database dal 19/10/2026' })
    const righe = [...totale.querySelectorAll('tbody tr')].map((r) => [...r.querySelectorAll('td')].map((c) => c.textContent))
    expect(righe).toEqual(
      Object.entries(fixture.dati.stato.conteggi).map(([k, n]) => [...k.split('/'), String(n)]),
    )
    expect(righe).toHaveLength(5)
    expect(righe[0]).toEqual(['assorbimento', 'assorbimento', '652'])
    const oggi = screen.getByRole('table', { name: 'Oggi (29/10/2026)' })
    const righeOggi = [...oggi.querySelectorAll('tbody tr')].map((r) => [...r.querySelectorAll('td')].map((c) => c.textContent))
    expect(righeOggi).toEqual(Object.entries(fixture.dati.oggi.conteggi).map(([k, n]) => [...k.split('/'), String(n)]))
    expect(righeOggi).toHaveLength(4)
    expect(voce(regione('Eventi nella memoria'), 'Totale oggi')).toBe('446')
  })

  it('avviso di freschezza: nessuno a 179 s; "dati vecchi" a 181 s; "motore spento o scollegato" a 601 s', async () => {
    const adesso = 1_000_000
    const q = (eta: number) => ({
      data: { ricevuto: 'x', eta_s: eta, dati: {} }, isError: false, dataUpdatedAt: adesso, errorUpdatedAt: 0,
    })
    expect(avvisi(q(179), 180, adesso, 600)).toEqual([])
    expect(avvisi(q(180), 180, adesso, 600)).toEqual([])
    expect(avvisi(q(181), 180, adesso, 600)).toEqual(['Dati vecchi di 3 minuti'])
    expect(avvisi(q(600), 180, adesso, 600)).toEqual(['Dati vecchi di 10 minuti'])
    expect(avvisi(q(601), 180, adesso, 600)).toEqual(['Motore spento o scollegato da 10 minuti'])
    // senza soglia di spento il comportamento degli altri canali non cambia
    expect(avvisi(q(181), 180, adesso)).toEqual(['Motore spento o scollegato da 3 minuti'])

    const b = copia()
    b.eta_s = 181
    const { unmount } = monta(b)
    expect(await screen.findByText(/Dati vecchi di 3 minuti/)).toBeInTheDocument()
    unmount()
    b.eta_s = 601
    monta(b)
    expect(await screen.findByText(/Motore spento o scollegato da 10 minuti/)).toBeInTheDocument()
  })

  it('dato fresco: nessun avviso di freschezza', async () => {
    monta(fixture)
    await screen.findByRole('table', { name: 'Totale nel database dal 19/10/2026' })
    expect(screen.queryByRole('status')).toBeNull()
  })
})

describe('verifica statistica (fixture reale)', () => {
  it('intestazione: divisione, generato, test BH e rubrica del blocco', async () => {
    monta(fixture)
    const sez = await screen.findByRole('region', { name: 'Verifica statistica' })
    await within(sez).findAllByText('DESCRITTIVO')
    expect(voce(sez, 'Divisione')).toBe('2026-10-21')
    expect(voce(sez, 'Verifica del')).toBe('29/10/2026 08:12') // 07:12 UTC, CET
    expect(voce(sez, 'Test (Benjamini-Hochberg)')).toBe('150')
    expect(voce(sez, 'Controlli')).toBe('5')
    expect(voce(sez, 'Placebo')).toBe('200')
    expect(voce(sez, 'Bootstrap')).toBe('2000')
    expect(voce(sez, 'q (BH)')).toBe('0.1')
  })

  it('10 gruppi con famiglia, tipo, lato, verdetto, n, orizzonte, metrica e p minimo come nel JSON', async () => {
    monta(fixture)
    const tabella = await screen.findByRole('table', { name: 'Verdetti per gruppo' })
    const corpi = [...tabella.querySelectorAll('tbody')]
    expect(corpi).toHaveLength(10)
    corpi.forEach((corpo, i) => {
      const [chiave, g] = gruppi[i]
      const celle = [...corpo.querySelectorAll('tr')[0].querySelectorAll('td')].map((c) => c.textContent)
      expect(celle).toEqual([...chiave.split('/'), g.verdetto, String(g.n), String(g.orizzonte), g.metrica, String(g.p_minimo)])
    })
  })

  it('sotto ogni riga la frase esatta del payload (confronto stringa per stringa, monospace)', async () => {
    monta(fixture)
    const tabella = await screen.findByRole('table', { name: 'Verdetti per gruppo' })
    const frasi = [...tabella.querySelectorAll('p[data-frase]')]
    expect(frasi.map((p) => p.textContent)).toEqual(gruppi.map(([, g]) => g.frase))
    expect(frasi).toHaveLength(10)
    for (const p of frasi) expect(p.className).toContain('font-mono')
    expect(frasi[0].getAttribute('data-frase')).toBe('assorbimento/assorbimento/acquisto')
  })

  it('badge neutri: nessun verde/rosso/primario; tre toni distinti per DESCRITTIVO / NON CONFERMATO / CONFERMATO', () => {
    const classi = ['DESCRITTIVO', 'NON CONFERMATO', 'CONFERMATO'].map((v) => {
      const { container, unmount } = render(<VerdettoGruppoBadge verdetto={v} />)
      const b = container.querySelector('[data-slot="badge"]') as HTMLElement
      const c = b.className
      expect(b.textContent).toBe(v)
      unmount()
      return c
    })
    expect(new Set(classi).size).toBe(3)
    for (const c of classi) expect(colori(c)).toEqual([])
  })

  it('i badge dei 10 gruppi nella pagina hanno la classe neutra (outline) quando il verdetto è DESCRITTIVO', async () => {
    monta(fixture)
    const tabella = await screen.findByRole('table', { name: 'Verdetti per gruppo' })
    const badge = [...tabella.querySelectorAll('[data-slot="badge"]')]
    expect(badge).toHaveLength(10)
    for (const b of badge) {
      expect(b.getAttribute('data-variant')).toBe('outline')
      expect(colori(b.className)).toEqual([])
    }
  })

  it('quando saranno possibili verdetti reali: la frase del registro con la Fonte (riga 11051)', async () => {
    monta(fixture)
    const sez = await screen.findByRole('region', { name: 'Quando saranno possibili verdetti reali' })
    expect(QUANDO.testo).toContain('8 sessioni = 30/10')
    expect(QUANDO.testo).toContain('10 = 3/11, 12 = 5/11')
    expect(QUANDO.fonte).toBe('docs/EXECUTION_LEDGER.md#L11051')
    expect(within(sez).getByText(QUANDO.testo)).toBeInTheDocument()
    expect(within(sez).getByText(QUANDO.fonte)).toBeInTheDocument()
  })
})

describe('nessun percorso locale nel render', () => {
  it('né "C:\\" né "Users\\" nel DOM con la fixture intera', async () => {
    const { container } = monta(fixture)
    await screen.findByRole('table', { name: 'Verdetti per gruppo' })
    const testo = container.textContent ?? ''
    expect(testo).not.toContain('C:\\')
    expect(testo).not.toContain('Users\\')
    // il nome dei file dello storico non si mostra: nessun .zip
    expect(testo).not.toMatch(/\.zip/)
  })
})

describe('validazione del payload (canale in errore, pagina in piedi)', () => {
  it('la fixture è valida e il resto del payload passa invariato', () => {
    const v = validaMemoria(fixture)
    expect(v.dati?.stato.conteggi['liquidita/ritiro']).toBe(5026)
    expect(Object.keys(v.dati?.verdetti.verdetti ?? {})).toHaveLength(10)
  })

  it('dati nulli: busta valida', () => {
    expect(validaMemoria({ ricevuto: null, eta_s: null, dati: null })).toEqual({ ricevuto: null, eta_s: null, dati: null })
  })

  const guasti: [string, (b: Rec) => void][] = [
    ['busta non oggetto', (b) => { b.dati = 5 }],
    ['verdetti.verdetti non è un oggetto', (b) => { nodo(b, 'dati', 'verdetti').verdetti = [1, 2] }],
    ['verdetti.verdetti stringa', (b) => { nodo(b, 'dati', 'verdetti').verdetti = 'x' }],
    ['stato.conteggi con un valore non intero', (b) => { nodo(b, 'dati', 'stato', 'conteggi')['liquidita/muro'] = 1.5 }],
    ['stato.conteggi con una stringa', (b) => { nodo(b, 'dati', 'stato', 'conteggi')['liquidita/muro'] = '5' }],
    ['stato.conteggi assente', (b) => { delete nodo(b, 'dati', 'stato').conteggi }],
    ['oggi.conteggi non oggetto', (b) => { nodo(b, 'dati', 'oggi').conteggi = null }],
    ['oggi.conteggi con un valore non intero', (b) => { nodo(b, 'dati', 'oggi', 'conteggi')['liquidita/ritiro'] = 'x' }],
    ['gruppo senza verdetto', (b) => { delete gruppoDi(b, 'liquidita/muro/ask').verdetto }],
    ['frase non stringa', (b) => { gruppoDi(b, 'liquidita/muro/ask').frase = { x: 1 } }],
    ['n stringa', (b) => { gruppoDi(b, 'liquidita/muro/ask').n = '3' }],
    ['orizzonte oggetto', (b) => { gruppoDi(b, 'liquidita/muro/ask').orizzonte = {} }],
    ['p_minimo stringa', (b) => { gruppoDi(b, 'liquidita/muro/ask').p_minimo = 'x' }],
    ['metrica numero', (b) => { gruppoDi(b, 'liquidita/muro/ask').metrica = 7 }],
    ['un gruppo non è un oggetto', (b) => { verdettiDi(b)['liquidita/muro/ask'] = 'DESCRITTIVO' }],
  ]

  it.each(guasti)('%s -> validaMemoria lancia', (_nome, guasta) => {
    const b = copia()
    guasta(b)
    expect(() => validaMemoria(b)).toThrow(/risposta del motore non valida/)
  })

  it('n, orizzonte, metrica, p_minimo null sono ammessi', () => {
    const b = copia()
    Object.assign(gruppoDi(b, 'liquidita/muro/ask'), { n: null, orizzonte: null, metrica: null, p_minimo: null })
    expect(() => validaMemoria(b)).not.toThrow()
  })

  it.each(guasti)('%s -> la pagina resta in piedi: avviso, titolo e definizioni, messaggio di errore del canale', async (_nome, guasta) => {
    vi.spyOn(console, 'error').mockImplementation(() => {})
    const b = copia()
    guasta(b)
    monta(b)
    expect(await screen.findByText(/^Dati non validi dal motore \(risposta del motore non valida: .+\)\.$/)).toBeInTheDocument()
    expect(screen.queryByText(/Servizio non raggiungibile/)).toBeNull()
    expect(screen.getByText(AVVISO)).toBeInTheDocument()
    expect(screen.getByRole('heading', { level: 1, name: 'Memoria del mercato' })).toBeInTheDocument()
    expect(screen.getByRole('region', { name: 'Che cosa riconosce' })).toBeInTheDocument()
    expect(screen.queryByRole('table', { name: 'Verdetti per gruppo' })).toBeNull()
  })
})

describe('useMemoria', () => {
  it('legge GET /live/memoria e restituisce la busta validata', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation(async () => new Response(JSON.stringify(fixture), { status: 200 }))
    const client = new QueryClient()
    const wrapper = ({ children }: { children: ReactNode }) => <QueryClientProvider client={client}>{children}</QueryClientProvider>
    const { result } = renderHook(() => useMemoria(), { wrapper })
    await waitFor(() => expect(result.current.data?.dati?.stato.strumento).toBe('MNQ 12-26'))
    expect((fetchMock.mock.calls[0][0] as string)).toMatch(/\/live\/memoria$/)
    const m: Memoria | null | undefined = result.current.data?.dati
    expect(m?.oggi.totale).toBe(446)
    client.clear()
    fetchMock.mockRestore()
  })

  // il predicato di nuovo tentativo: una risposta che il sito non sa mostrare tornerebbe uguale (nessun nuovo tentativo),
  // un errore di rete o un 503 ha un nuovo tentativo dopo 3 s (retryDelay)
  const provaChiamate = async (risposta: () => Response) => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation(async () => risposta())
    const client = new QueryClient()
    const wrapper = ({ children }: { children: ReactNode }) => <QueryClientProvider client={client}>{children}</QueryClientProvider>
    const { result } = renderHook(() => useMemoria(), { wrapper })
    return { fetchMock, client, result }
  }

  it('RispostaNonValida: fetch chiamato una volta sola, nessun nuovo tentativo', { timeout: 15_000 }, async () => {
    const { fetchMock, client, result } = await provaChiamate(() => new Response(JSON.stringify({ ricevuto: null, eta_s: null, dati: 5 }), { status: 200 }))
    await waitFor(() => expect(result.current.isError).toBe(true), { timeout: 2_000 })
    expect(result.current.error).toBeInstanceOf(RispostaNonValida)
    await new Promise((r) => setTimeout(r, 3_500)) // oltre il retryDelay: se ci fosse un tentativo sarebbe gia' partito
    expect(fetchMock).toHaveBeenCalledTimes(1)
    client.clear()
    fetchMock.mockRestore()
  })

  it('HTTP 503: fetch chiamato due volte (un nuovo tentativo dopo 3 s), poi errore', { timeout: 15_000 }, async () => {
    const { fetchMock, client, result } = await provaChiamate(() => new Response('{}', { status: 503 }))
    await waitFor(() => expect(result.current.isError).toBe(true), { timeout: 8_000 })
    expect(fetchMock).toHaveBeenCalledTimes(2)
    expect(result.current.error).not.toBeInstanceOf(RispostaNonValida)
    expect(result.current.error?.message).toBe('HTTP 503')
    client.clear()
    fetchMock.mockRestore()
  })
})

describe('rotta /memoria', () => {
  it('la pagina si carica dal router (lazy) con titolo, avviso e nota fissa del sito', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true, status: 200, json: async () => fixture })))
    window.history.pushState({}, '', '/memoria')
    vi.resetModules()
    const { default: App } = await import('@/App')
    render(<App />)
    expect(await screen.findByRole('heading', { level: 1, name: 'Memoria del mercato' })).toBeInTheDocument()
    expect(screen.getByText(AVVISO)).toBeInTheDocument()
    expect(screen.getByText("Frequenze descrittive su dati gia' visti, non segnali.")).toBeInTheDocument()
    window.history.pushState({}, '', '/')
  })
})
