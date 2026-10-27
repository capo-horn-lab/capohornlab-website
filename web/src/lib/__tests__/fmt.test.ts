import { describe, expect, it } from 'vitest'
import { intero, num, p, prezzo, quart } from '@/lib/fmt'

describe('fmt (D8)', () => {
  it('p: k su n agli estremi, altrimenti p% (k/n ±m)', () => {
    expect(p({ p: 1, k: 21, n: 21 })).toBe('21 su 21')
    expect(p({ p: 0.73, k: 22, n: 30, margine: 0.16 })).toBe('73% (22/30 ±16)')
    expect(p({ p: 0, k: 0, n: 68, margine: 0 })).toBe('0 su 68')
    expect(p({ p: 0.996, k: 249, n: 250, margine: 0.01 })).toBe('249 su 250')
    expect(p({ p: 0.5, k: 20, n: 40 })).toBe('50% (20/40)')
    expect(p(null)).toBe('-')
    expect(p({ p: null, k: 0, n: 0 })).toBe('-')
  })
  it('arrotonda come Python (meta pari)', () => {
    expect(p({ p: 0.125, k: 5, n: 40, margine: 0.105 })).toBe('12% (5/40 ±10)')
    expect(intero(7728.5)).toBe('7728')
    expect(intero(7729.5)).toBe('7730')
    expect(intero(2784.6000000000004)).toBe('2785')
  })
  it('pareggi a 2 decimali al pari come Python (f"{x:.2f}")', () => {
    expect(num(0.125)).toBe('0.12')
    expect(num(52.125)).toBe('52.12')
    expect(num(0.375)).toBe('0.38')
    expect(num(-0.125)).toBe('-0.12')
    expect(num(2.675)).toBe('2.67') // 2.67499999... in binario: nessun pareggio, come Python
    expect(prezzo(29416.125)).toBe('29416.12')
    expect(quart({ mediana: 0.125, q1: 0.375, q3: 0.625 }, 2)).toBe('0.12 (0.38-0.62)')
  })
  it('valori non numerici: un trattino, mai NaN', () => {
    expect(num('x' as unknown as number)).toBe('-')
    expect(num(Number.NaN)).toBe('-')
    expect(prezzo('29000' as unknown as number)).toBe('-')
    expect(p({ p: 'x' as unknown as number, k: 1, n: 2 })).toBe('-')
  })
  it('num, quart, prezzo', () => {
    expect(num(4021.072551314183)).toBe('4021.07')
    expect(num(41.8, 0)).toBe('42')
    expect(num(null)).toBe('-')
    expect(quart({ mediana: 48, q1: 39.17, q3: 60.35, n: 60 })).toBe('48 (39-60)')
    expect(quart({ mediana: 0.09, q1: 0.04, q3: 0.16, n: 490 }, 2)).toBe('0.09 (0.04-0.16)')
    expect(quart(null)).toBe('n/d')
    expect(prezzo(29416.25)).toBe('29416.25')
    expect(prezzo(29008)).toBe('29008')
    expect(prezzo(4022.4)).toBe('4022.4')
    expect(prezzo(null)).toBe('-')
  })
})
