// FREQ-SITO-3: the fase 2 Task 7 assertions (tests/js/albero.test.js) ported to vitest, plus the cases they only named.
import { describe, expect, it } from 'vitest'
import { alberoInTesto, esitoTesto, etichetta, geometria, sceltiDaQui, snap5, type Radice, type Ramo } from '@/lib/albero'

const t0 = Date.UTC(2026, 9, 26, 13, 30) / 1000
const radice: Radice = { ora: '14:30', t: new Date(t0 * 1000).toISOString(), prezzo: 29000, fase: 'attesa', percorso: '', omessi: 0 }

function r(id: string, padre: string | null, tipo: string, p: number, mediana: number | null, prezzo = 29000 + p * 100): Ramo {
  return {
    id, padre, tipo, etichetta: id, prezzo, p, k: Math.round(p * 40), n: 40, margine: 0.1, orizzonte: '21:00',
    minuti: mediana == null ? null : { mediana, q1: mediana - 5, q3: mediana + 10 }, tocco: mediana != null, omessi: 0,
  }
}

// radice t0; r1 primo_movimento p .6 mediana 30; r1.1 figlio ritorno p .5 mediana 20 (minore del padre -> capo a t0+31 min);
// r2 chiusura (minuti null, p .7: non conta tra i padri disegnati); r3 estensione mediana 200 (-> testo); r4 p .1 mediana 10;
// r5 p .2 mediana 15: padri disegnati per p r1 .6, r5 .2, r4 .1 -> figli solo di r1 e r5
const rami = [r('r1', null, 'primo_movimento', 0.6, 30), r('r1.1', 'r1', 'ritorno', 0.5, 20), r('r2', null, 'chiusura', 0.7, null),
  r('r3', null, 'estensione', 0.4, 200), r('r4', null, 'primo_movimento', 0.1, 10), r('r5', null, 'primo_movimento', 0.2, 15)]
const opz = { massimoMinuti: 180, padriConFigli: 2 }
const ids = (xs: Ramo[]) => xs.map((x) => x.id)

describe('geometria (fase 2 Task 7)', () => {
  const g = geometria(radice, rami, opz)
  const seg = (id: string) => g.segmenti.find((s) => s.id === id)

  it('esiti e testo', () => {
    expect(ids(g.esiti)).toEqual(['r2'])
    expect(ids(g.testo)).toEqual(['r3'])
  })
  it('capo del padre e del figlio (Review Focus 2: minuti relativi alla radice, figlio >= capo del padre + 1 min)', () => {
    expect(seg('r1')!.a.t).toBe(t0 + 1800)
    expect(seg('r1.1')!.a.t).toBe(t0 + 1800 + 60)
    expect(seg('r1.1')!.da.t).toBe(seg('r1')!.a.t)
    expect(seg('r1.1')!.da.prezzo).toBe(seg('r1')!.a.prezzo)
    expect(seg('r1')!.da).toEqual({ t: t0, prezzo: 29000 })
  })
  it('figlio del terzo padre non disegnato', () => {
    expect(seg('r4.1')).toBeUndefined()
  })
  it('classe', () => {
    expect(seg('r1')!.classe).toBe(2)
  })
  it('Review Focus 3: niente radice, niente rami', () => {
    expect(geometria(null, null, {}).segmenti).toEqual([])
    expect(geometria(null, null, {}).esiti).toEqual([])
  })
  it('q1/q3 relativi alla radice, quelli del figlio non prima del capo del padre', () => {
    expect(seg('r1')!.q1.t).toBe(t0 + 25 * 60)
    expect(seg('r1')!.q3.t).toBe(t0 + 40 * 60)
    expect(seg('r1.1')!.q1.t).toBe(t0 + 1800)
    expect(seg('r1.1')!.q3.t).toBe(t0 + 1800)
    expect(g.radiceT).toBe(t0)
  })
})

describe('geometria: figli fuori dai due padri, nipoti, figli di rami in testo', () => {
  const tutti = [...rami, r('r4.1', 'r4', 'ritorno', 0.9, 12), r('r5.1', 'r5', 'ritorno', 0.3, 25), r('r1.1.1', 'r1.1', 'ritorno', 0.5, 40),
    r('r3.1', 'r3', 'ritorno', 0.5, 210), r('r2.1', 'r2', 'chiusura', 0.5, null)]
  const g = geometria(radice, tutti, opz)
  it('disegnati solo padri e figli dei due padri piu probabili', () => {
    expect(g.segmenti.map((s) => s.id)).toEqual(['r1', 'r1.1', 'r4', 'r5', 'r5.1'])
  })
  it('gli altri in testo o tra gli esiti, nell ordine del file', () => {
    expect(ids(g.testo)).toEqual(['r3', 'r4.1', 'r1.1.1', 'r3.1'])
    expect(ids(g.esiti)).toEqual(['r2', 'r2.1'])
  })
  it('classi ai confini 0.33 e 0.66', () => {
    const c = (p: number) => geometria(radice, [r('x', null, 'primo_movimento', p, 10)], opz).segmenti[0].classe
    expect([c(0.32), c(0.33), c(0.65), c(0.66)]).toEqual([1, 2, 2, 3])
  })
  it('rami senza prezzo non disegnati', () => {
    const g2 = geometria(radice, [{ ...r('x', null, 'primo_movimento', 0.5, 10), prezzo: null }], opz)
    expect(g2.segmenti).toEqual([])
  })
})

describe('sceltiDaQui, alberoInTesto, snap5', () => {
  it('3 padri per p, 2 figli ciascuno, ogni figlio dopo il padre', () => {
    const ramiDaQui = [0.5, 0.4, 0.3, 0.2].flatMap((p, i) => [r(`q${i}`, null, 'primo_movimento', p, 10),
      ...[0.9, 0.1, 0.5].map((pf, j) => r(`q${i}.${j}`, `q${i}`, 'estensione', pf, 20))])
    const s = sceltiDaQui(ramiDaQui)
    expect(s.length).toBe(3 + 2 + 2 + 2)
    expect(ids(s)).toEqual(['q0', 'q0.0', 'q0.2', 'q1', 'q1.0', 'q1.2', 'q2', 'q2.0', 'q2.2'])
  })
  it('albero in testo oltre 2 ore dopo l ultima barra', () => {
    expect(alberoInTesto(t0 + 7201, t0) && !alberoInTesto(t0 + 7199, t0)).toBe(true)
    expect(alberoInTesto(t0 + 7200, t0)).toBe(false)
  })
  it('snap5', () => {
    expect(snap5(t0 + 149)).toBe(t0)
    expect(snap5(t0 + 151)).toBe(t0 + 300)
  })
})

describe('etichetta ed esitoTesto (D8, desktop_trader nome_breve / esito_ramo)', () => {
  it('etichette brevi', () => {
    expect(etichetta({ etichetta: 'primo movimento di 50 giu', p: 1, k: 21, n: 21, margine: 0.14 })).toBe('50 giu 21 su 21')
    expect(etichetta({ etichetta: "ritorno all'apertura entro 30 min dal primo movimento", p: 0.73, k: 22, n: 30, margine: 0.16 }))
      .toBe("ritorno all'apertura 30' 73% (22/30 ±16)")
    expect(etichetta({ etichetta: 'estensione a +65.44 (q3) prima del ritorno (pochi casi)', p: 0.25, k: 5, n: 20, margine: 0.19 }))
      .toBe('estensione +65 25% (5/20 ±19)')
    expect(etichetta({ etichetta: "ritorno all'apertura piu' tardi, entro le 21:00", p: 0.4, k: 8, n: 20, margine: 0.2 }))
      .toBe("ritorno all'apertura piu' tardi 40% (8/20 ±20)")
  })
  it('chiusura', () => {
    expect(esitoTesto({ etichetta: "chiusura sopra l'apertura", prezzo: 29246, p: 0.95, k: 20, n: 21 }, 29030, "l'apertura"))
      .toBe("chiusura sopra l'apertura 29030: 95% (20/21) · mediana 29246")
  })
  it('mai, con pochi casi (k su n) e arrotondamento come Python (7728.5 -> 7728)', () => {
    expect(esitoTesto({ etichetta: "ritorno all'apertura mai entro le 21:00 (pochi casi)", prezzo: 7728.5, p: 0.95, k: 19, n: 20, margine: 0.15, orizzonte: '21:00' },
      7683.25, "l'apertura")).toBe("mai ritorno all'apertura 7683 entro 21:00: 19 su 20, pochi casi · mediana dell'estensione 7728")
  })
  it('nessun opposto e nessun movimento', () => {
    expect(esitoTesto({ etichetta: 'nessun 4.6 opposto entro le 21:00 (pochi casi)', prezzo: 2789.2, p: 0.968, k: 30, n: 31, margine: 0.097, orizzonte: '21:00' },
      2789.2, "l'apertura", 4.6, 1)).toBe("nessun 4.6 sotto l'apertura (2785) entro 21:00: 30 su 31, pochi casi")
    expect(esitoTesto({ etichetta: 'nessun movimento di 5.7 entro le 21:00', prezzo: 4022.4, p: 0.546, k: 131, n: 240, margine: 0.063, orizzonte: '21:00' },
      4022.4, 'il punto', 5.7)).toBe('nessun movimento di 5.7 dal punto 4022 (4017-4028) entro 21:00: 55% (131/240 ±6)')
  })
})
