import { readFileSync } from 'node:fs'
import path from 'node:path'

const read = (...p: string[]) => readFileSync(path.resolve(import.meta.dirname, ...p), 'utf8').replace(/\r\n/g, '\n')
const theme = read('theme.css')

describe('tema Observatory', () => {
  it('mappa le variabili shadcn sui token --ch-*', () => {
    expect(theme).toContain('--background: var(--ch-ink)')
    expect(theme).toContain('--foreground: var(--ch-fog)')
    expect(theme).toContain('--primary: var(--ch-signal)')
    expect(theme).toContain('--chart-negative: var(--ch-signal-deep)')
  })

  it('importa i token locali e non contiene colori fuori dai token', () => {
    expect(theme).toContain('@import "./observatory-tokens.css"')
    expect(theme).not.toMatch(/#[0-9a-fA-F]{3,8}\b|rgba?\(|hsl\(|oklch\(/)
  })

  it('la copia dei token coincide con design/observatory-tokens.css', () => {
    expect(read('observatory-tokens.css')).toBe(read('../../../design/observatory-tokens.css'))
  })
})
