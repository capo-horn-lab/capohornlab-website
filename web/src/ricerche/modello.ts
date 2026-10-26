// Lettura delle pagine generate da scripts/estrai_ricerche.py (frontmatter a valori JSON, sezioni "## ...", tabella pipe).

export type Verdetto =
  | 'ritirato'
  | 'corretto'
  | 'confermata'
  | 'parziale'
  | 'misto'
  | 'non confermata'
  | 'descrittivo'

export interface VoceIndice {
  id: string
  titolo: string
  data: string
  strumenti: string[]
  verdetto: Verdetto
  pubblicabilita: 'ok' | 'avvertenza'
  grafico: boolean
}

export interface Frontmatter {
  id: string
  titolo: string
  data: string
  strumenti: string[]
  finestra: string
  verdetto: Verdetto
  pubblicabilita: 'ok' | 'avvertenza'
  avvertenza: string
  fonte_ledger: string
  prove: string[]
}

export type Cella = string | number | boolean | null

export interface Dati {
  tipo: 'tabella' | 'serie' | 'matrice'
  colonne: string[]
  righe: Cella[][]
  fonte: string
}

export interface Ricerca {
  fm: Frontmatter
  sezioni: Record<string, string>
}

export function leggiRicerca(raw: string): Ricerca {
  const righe = raw.replace(/\r\n/g, '\n').split('\n')
  const fine = righe.indexOf('---', 1)
  const fm: Record<string, unknown> = {}
  let chiave = ''
  for (const r of righe.slice(1, fine)) {
    const m = /^([A-Za-z_]\w*):\s*(.*)$/.exec(r)
    if (m) {
      chiave = m[1]
      fm[chiave] = m[2] ? JSON.parse(m[2]) : []
    } else if (chiave && Array.isArray(fm[chiave])) {
      const v = /^\s+-\s+(.*)$/.exec(r)
      if (v) (fm[chiave] as unknown[]).push(JSON.parse(v[1]))
    }
  }
  const sezioni: Record<string, string> = {}
  let nome = ''
  let buf: string[] = []
  const chiudi = () => {
    if (nome) sezioni[nome] = buf.join('\n').trim()
  }
  for (const r of righe.slice(fine + 1)) {
    if (r.startsWith('## ')) {
      chiudi()
      nome = r.slice(3).trim()
      buf = []
    } else buf.push(r)
  }
  chiudi()
  return { fm: fm as unknown as Frontmatter, sezioni }
}

/** Tabella pipe (| a | b |, |---|---|) di una sezione -> intestazioni e righe; `\|` vale `|`. */
export function leggiTabella(testo: string): { testata: string[]; righe: string[][] } {
  const celle = (r: string) =>
    r
      .trim()
      .replace(/^\||\|$/g, '')
      .split(/(?<!\\)\|/)
      .map((c) => c.trim().replace(/\\\|/g, '|'))
  const linee = testo.split('\n').filter((l) => l.trim().startsWith('|'))
  if (linee.length < 2) return { testata: [], righe: [] }
  return { testata: celle(linee[0]), righe: linee.slice(2).map(celle) }
}

/** Righe "- voce" di una sezione (fuori dalle tabelle) -> voci. */
export function leggiElenco(testo: string): string[] {
  return testo
    .split('\n')
    .filter((l) => l.startsWith('- '))
    .map((l) => l.slice(2).trim())
}

/** Il testo di una sezione senza tabella ne' elenco: i paragrafi. */
export function leggiPrefazio(testo: string): string {
  return testo
    .split('\n')
    .filter((l) => !l.startsWith('|') && !l.startsWith('- '))
    .join('\n')
    .trim()
}

export function dividiFonti(cella: string): string[] {
  return cella.split(' · ').map((f) => f.trim()).filter(Boolean)
}

export type VarianteBadge = 'default' | 'secondary' | 'destructive' | 'outline'

export const ETICHETTE: Record<Verdetto, { testo: string; variante: VarianteBadge; aiuto: string }> = {
  ritirato: { testo: 'ritirato', variante: 'destructive', aiuto: "Conferma ritirata dall'audit: i numeri restano per trasparenza." },
  corretto: { testo: 'corretto', variante: 'destructive', aiuto: "Misura o conclusione corretta in seguito: leggere l'audit." },
  confermata: { testo: 'confermata', variante: 'secondary', aiuto: 'Confermata secondo la rubrica fissata prima.' },
  parziale: { testo: 'parziale', variante: 'secondary', aiuto: 'PARZIALE nel vocabolario del ledger.' },
  misto: { testo: 'misto', variante: 'secondary', aiuto: 'Alcune prove confermate, altre no.' },
  'non confermata': { testo: 'non confermata', variante: 'outline', aiuto: 'Nessuna prova confermata dalla rubrica.' },
  descrittivo: { testo: 'descrittivo', variante: 'outline', aiuto: 'Misure e frequenze senza verdetto di ipotesi.' },
}

export const anno = (data: string) => data.slice(0, 4)

/** Colonna dei valori per un grafico: la prima colonna numerica dopo la colonna etichetta. */
export function colonnaValori(dati: Dati): number {
  if (dati.tipo === 'tabella') {
    const m = dati.colonne.indexOf('m')
    if (m >= 0) return m
  }
  for (let c = 1; c < dati.colonne.length; c++) {
    if (dati.righe.every((r) => r[c] === null || typeof r[c] === 'number')) return c
  }
  return -1
}
