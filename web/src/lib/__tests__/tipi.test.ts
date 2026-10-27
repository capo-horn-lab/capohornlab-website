import { describe, expect, it } from 'vitest'
import { haErrore, type StrumentoFrequenze, type StrumentoScenari, validaFrequenze, validaScenari } from '@/lib/tipi'
import frequenze from '@/test/fixtures/frequenze.json'
import scenari from '@/test/fixtures/scenari.json'

/** A mutable deep copy of a fixture, typed loosely enough to break it on purpose. */
type Rec = Record<string, unknown>
interface Copia { ricevuto: unknown; eta_s: unknown; dati: Rec & { strumenti: Record<string, Rec>; barre: Record<string, Rec> } }
const copia = (x: unknown) => structuredClone(x) as Copia

describe('tipi: fixture reali', () => {
  it('le fixture non portano percorsi locali', () => {
    for (const f of [scenari, frequenze]) {
      const s = JSON.stringify(f)
      for (const vietato of ['C:\\', 'Users', 'farne']) expect(s.includes(vietato)).toBe(false)
    }
  })
  it('scenari valida, ogni strumento ha radice, rami e livelli, barre a 5 minuti', () => {
    const v = validaScenari(scenari)
    expect(v.dati).not.toBeNull()
    for (const r of Object.values(v.dati!.strumenti)) {
      if (haErrore(r)) continue
      expect(typeof r.radice.t).toBe('string')
      expect(Array.isArray(r.rami)).toBe(true)
      expect(Array.isArray(r.livelli)).toBe(true)
    }
    expect(v.dati!.barre[v.dati!.principale.strumento].tf).toBe(5)
    expect(v.dati!.barre.MNQ.righe.length).toBe(96)
    expect((v.dati!.strumenti.MGC as StrumentoScenari).rami.length).toBe(2)
  })
  it('frequenze valida', () => {
    const v = validaFrequenze(frequenze)
    const r = v.dati!.strumenti[v.dati!.principale.strumento]
    expect(haErrore(r)).toBe(false)
    if (!haErrore(r)) expect(r.livelli.length).toBe(11)
    expect(v.dati!.limiti.length).toBeGreaterThan(0)
  })
  it('uno strumento con errore e da_qui null non lancia', () => {
    const s = copia(scenari)
    s.dati.strumenti.MNQ = { contratto: 'MNQ 12-26', errore: 'nessuno storico per MNQ' }
    s.dati.strumenti.MGC.da_qui = null
    s.dati.strumenti.MGC.escursione_residua = null
    const v = validaScenari(s)
    expect(haErrore(v.dati!.strumenti.MNQ)).toBe(true)
    const f = copia(frequenze)
    f.dati.strumenti.MES = { contratto: 'MES 12-26', errore: 'OSError: file' }
    expect(haErrore(validaFrequenze(f).dati!.strumenti.MES)).toBe(true)
  })
  it('motore senza dati e buste malformate', () => {
    expect(validaScenari({ ricevuto: null, eta_s: null, dati: null }).dati).toBeNull()
    expect(() => validaScenari({})).toThrow()
    expect(() => validaScenari({ ricevuto: null, eta_s: 3, dati: { strumenti: 1 } })).toThrow()
    expect(() => validaFrequenze('x')).toThrow()
  })
})

describe('tipi: payload rotti non fanno cadere la pagina (Important 3)', () => {
  it('principale mancante o senza strumento: errore del canale', () => {
    const s = copia(scenari)
    delete s.dati.principale
    expect(() => validaScenari(s)).toThrow(/principale/)
    const f = copia(frequenze)
    f.dati.principale = { contratto: 'x' }
    expect(() => validaFrequenze(f)).toThrow(/principale/)
  })
  it('barre: righe non lista -> strumento senza barre; righe e viva malformate scartate', () => {
    const s = copia(scenari)
    s.dati.barre.MNQ.righe = {}
    const righe = s.dati.barre.MES.righe as unknown[]
    righe[0] = [1, 2, 3]
    righe[1] = [1793013300, 'x', 1, 1, 1, 1]
    s.dati.barre.MES.viva = [1, 2]
    s.dati.barre.M2K = 'x' as unknown as Rec
    const v = validaScenari(s)
    expect(v.dati!.barre.MNQ).toBeUndefined()
    expect(v.dati!.barre.M2K).toBeUndefined()
    expect(v.dati!.barre.MES.righe.length).toBe(94)
    expect(v.dati!.barre.MES.viva).toBeNull()
    expect(v.dati!.barre.MGC.righe.length).toBe(96)
  })
  it('rami e livelli con prezzo o p non finiti scartati', () => {
    const s = copia(scenari)
    const rami = s.dati.strumenti.MES.rami as Rec[]
    rami[0].prezzo = 'x'
    const livelli = s.dati.strumenti.MES.livelli as Rec[]
    livelli[0].prezzo = null
    const q = (s.dati.strumenti.MGC.da_qui as Rec).rami as Rec[]
    q[0].p = 'NaN'
    const v = validaScenari(s)
    const mes = v.dati!.strumenti.MES as StrumentoScenari
    expect(mes.rami.map((r) => r.id)).toEqual(['r2'])
    expect(mes.livelli.length).toBe(10)
    expect((v.dati!.strumenti.MGC as StrumentoScenari).da_qui!.rami.length).toBe(15)
  })
  it('radice malformata o rami non lista: errore di quello strumento, gli altri restano', () => {
    const s = copia(scenari)
    ;(s.dati.strumenti.MES.radice as Rec).prezzo = 'x'
    s.dati.strumenti.M2K.rami = 3
    ;(s.dati.strumenti.MGC.da_qui as Rec).radice = { t: 5 }
    const v = validaScenari(s)
    expect(haErrore(v.dati!.strumenti.MES)).toBe(true)
    expect(haErrore(v.dati!.strumenti.M2K)).toBe(true)
    expect(haErrore(v.dati!.strumenti.MNQ)).toBe(false)
    expect((v.dati!.strumenti.MGC as StrumentoScenari).da_qui).toBeNull()
  })
  it('frequenze: strumento senza stato in errore, livelli senza prezzo scartati, p non finita -> null', () => {
    const f = copia(frequenze)
    delete f.dati.strumenti.MES.stato
    const livelli = f.dati.strumenti.MGC.livelli as Rec[]
    livelli[0].prezzo = 'x'
    ;(livelli[1].entro_2200 as Rec).p = 'x'
    const v = validaFrequenze(f)
    expect(haErrore(v.dati!.strumenti.MES)).toBe(true)
    const mgc = v.dati!.strumenti.MGC as StrumentoFrequenze
    expect(mgc.livelli.length).toBe(10)
    expect(mgc.livelli[0].entro_2200!.p).toBeNull()
  })
})
