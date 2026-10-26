#!/usr/bin/env node
// Server statico senza dipendenze per web/dist, con fallback SPA a index.html per le rotte dell'app.
//   node scripts/servi_dist.mjs [--dir dist] [--dir ..] [--port 3000] [--host 127.0.0.1]
// --dir si puo' ripetere: vince la prima cartella che ha il file (le altre fanno da riserva,
// per esempio il repo del sito con favicon e pagine legali accanto a dist).
// Comprime in gzip html/js/css/json/svg se il client lo accetta (come fa un hosting reale: Lighthouse locale resta attendibile).
// Fallback: percorsi sconosciuti sotto /ricerche, /metodo, /stato (senza estensione) -> index.html.
import { createReadStream, statSync } from 'node:fs'
import http from 'node:http'
import { pipeline } from 'node:stream'
import { createGzip } from 'node:zlib'
import { dirname, extname, join, resolve, sep } from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'
import { leggiArgomenti } from './args.mjs'

export const ROTTE_SPA = ['ricerche', 'metodo', 'stato']
const MIME = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8', '.woff2': 'font/woff2', '.woff': 'font/woff',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp',
  '.ico': 'image/x-icon', '.txt': 'text/plain; charset=utf-8', '.xml': 'application/xml', '.map': 'application/json',
  '.webmanifest': 'application/manifest+json',
}

const fileEsiste = (p) => {
  try {
    return statSync(p).isFile()
  } catch {
    return false
  }
}

export function creaServer(dirs) {
  const radici = dirs.map((d) => resolve(d))
  const trova = (percorso) => {
    for (const r of radici) {
      let f = resolve(r, '.' + percorso)
      if (f !== r && !f.startsWith(r + sep)) continue
      if (percorso.endsWith('/')) f = join(f, 'index.html')
      if (fileEsiste(f)) return f
    }
  }
  return http.createServer((req, res) => {
    let p
    try {
      p = decodeURIComponent(new URL(req.url, 'http://x').pathname)
    } catch {
      res.writeHead(400).end('richiesta non valida')
      return
    }
    // niente ../ ne' file nascosti (.env, .git): --dir puo' puntare alla radice di un repo
    if (p.includes('\0') || p.split('/').some((x) => x === '..' || (x.startsWith('.') && x !== '.well-known'))) {
      res.writeHead(403).end('vietato')
      return
    }
    let file = trova(p)
    const [primo, ...resto] = p.split('/').filter(Boolean)
    if (!file && (p === '/' || (ROTTE_SPA.includes(primo) && !extname(resto.at(-1) ?? primo)))) file = trova('/index.html')
    if (!file || (req.method !== 'GET' && req.method !== 'HEAD')) {
      res.writeHead(file ? 405 : 404, { 'content-type': 'text/plain; charset=utf-8' }).end(file ? 'metodo non consentito' : 'non trovato')
      return
    }
    const tipo = MIME[extname(file).toLowerCase()] ?? 'application/octet-stream'
    const gzip = /\b(?:html|javascript|css|json|svg|xml|text\/plain)\b/.test(tipo) && /\bgzip\b/.test(req.headers['accept-encoding'] ?? '')
    const intestazioni = { 'content-type': tipo, 'cache-control': 'no-cache', ...(gzip && { 'content-encoding': 'gzip', vary: 'accept-encoding' }) }
    if (req.method === 'HEAD') return res.writeHead(200, intestazioni).end()
    // si risponde 200 solo a file aperto: se l'apertura fallisce (permessi, file sparito) e' un 500 pulito, non un processo morto;
    // un errore a meta' lettura chiude la connessione (pipeline distrugge res) senza far cadere il server
    const flusso = createReadStream(file)
    flusso.on('error', () => res.headersSent || res.writeHead(500, { 'content-type': 'text/plain; charset=utf-8' }).end('errore di lettura'))
    flusso.on('open', () => {
      res.writeHead(200, intestazioni)
      pipeline(...(gzip ? [flusso, createGzip(), res] : [flusso, res]), () => {})
    })
  })
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const { values } = leggiArgomenti({ options: { dir: { type: 'string', multiple: true }, port: { type: 'string', default: '3000' }, host: { type: 'string', default: '127.0.0.1' } } })
  const dirs = values.dir?.length ? values.dir : [join(dirname(fileURLToPath(import.meta.url)), '..', 'dist')]
  const server = creaServer(dirs)
  server.listen(Number(values.port), values.host, () => console.log(`Servo ${dirs.map((d) => resolve(d)).join(' + ')} su http://${values.host}:${server.address().port}`))
}
