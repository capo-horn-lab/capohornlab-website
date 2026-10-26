import { describe, expect, it } from 'vitest'
import { candele } from '@/lib/aggrega'
import type { Barre } from '@/lib/tipi'
import scenari from '@/test/fixtures/scenari.json'

const barre = (scenari.dati.barre as unknown as Record<string, Barre>).MNQ

describe('candele', () => {
  it('righe chiuse + candela viva marcata, data = inizio dello slot', () => {
    const { candele: c } = candele(barre)
    expect(c.length).toBe(barre.righe.length + 1)
    expect(c[0].date.getTime()).toBe((barre.righe[0][0] - 300) * 1000)
    expect(c[0]).toMatchObject({ open: barre.righe[0][1], high: barre.righe[0][2], low: barre.righe[0][3], close: barre.righe[0][4], volume: barre.righe[0][5], viva: false })
    expect(c.at(-1)!.viva).toBe(true)
    expect(c.filter((x) => x.viva).length).toBe(1)
  })
  it('36 slot futuri da 5 minuti dopo l ultima candela', () => {
    const { candele: c, futuri } = candele(barre)
    const ultima = c.at(-1)!.date.getTime()
    expect(futuri.length).toBe(36)
    expect(futuri[0].getTime()).toBe(ultima + 300_000)
    expect(futuri[35].getTime()).toBe(ultima + 36 * 300_000)
  })
  it('senza viva e senza barre', () => {
    const { candele: c, futuri } = candele({ ...barre, viva: null })
    expect(c.every((x) => !x.viva)).toBe(true)
    expect(futuri[0].getTime()).toBe(barre.righe.at(-1)![0] * 1000)
    expect(candele(null)).toEqual({ candele: [], futuri: [] })
  })
})
