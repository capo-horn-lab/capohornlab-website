import { describe, expect, it } from 'vitest'
import { haErrore, validaFrequenze, validaScenari } from '@/lib/tipi'
import frequenze from '@/test/fixtures/frequenze.json'
import scenari from '@/test/fixtures/scenari.json'

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const copia = (x: unknown): any => JSON.parse(JSON.stringify(x))

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
  })
  it('frequenze valida', () => {
    const v = validaFrequenze(frequenze)
    const r = v.dati!.strumenti[v.dati!.principale.strumento]
    expect(haErrore(r)).toBe(false)
    if (!haErrore(r)) expect(r.livelli.length).toBeGreaterThan(0)
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
  it('motore senza dati e risposte malformate', () => {
    expect(validaScenari({ ricevuto: null, eta_s: null, dati: null }).dati).toBeNull()
    expect(() => validaScenari({})).toThrow()
    expect(() => validaScenari({ ricevuto: null, eta_s: 3, dati: { strumenti: 1 } })).toThrow()
    expect(() => validaScenari({ ricevuto: null, eta_s: 3, dati: { strumenti: { MNQ: { contratto: 'x', radice: {}, rami: 3 } } } })).toThrow()
    expect(() => validaFrequenze('x')).toThrow()
  })
})
