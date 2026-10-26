// Contenuti generati (web/src/content/ricerche): l'indice e' nel bundle dell'elenco, ogni pagina e' un chunk a parte.
import indiceJson from '@/content/ricerche/indice.json'
import { leggiRicerca, type Dati, type Ricerca, type VoceIndice } from './modello'

export const indice = indiceJson as VoceIndice[]

const pagine = import.meta.glob('../content/ricerche/*.md', { query: '?raw', import: 'default' }) as Record<
  string,
  () => Promise<string>
>
const dati = import.meta.glob('../content/ricerche/*.dati.json', { import: 'default' }) as Record<
  string,
  () => Promise<Dati>
>

const percorso = (id: string, estensione: string) => `../content/ricerche/${id}.${estensione}`

export async function caricaRicerca(id: string): Promise<Ricerca | null> {
  const f = pagine[percorso(id, 'md')]
  return f ? leggiRicerca(await f()) : null
}

export async function caricaDati(id: string): Promise<Dati | null> {
  const f = dati[percorso(id, 'dati.json')]
  return f ? await f() : null
}
