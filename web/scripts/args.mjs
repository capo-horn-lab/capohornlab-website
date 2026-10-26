// parseArgs che, su opzione sconosciuta o valore mancante, stampa il messaggio ed esce con 2 (uso errato) invece di uno stack trace con 1.
import { parseArgs } from 'node:util'

export function leggiArgomenti(config) {
  try {
    return parseArgs(config)
  } catch (e) {
    console.error(`uso errato: ${e.message}`)
    process.exit(2)
  }
}
