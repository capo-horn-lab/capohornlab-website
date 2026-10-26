#!/usr/bin/env node
// Verifica che nessun link del sito sia rotto: crawl di web/dist (servito in locale con fallback SPA) o di un URL.
//   node scripts/verifica_link.mjs [--dist dist] [--statici ..] [--base https://sito] [--timeout 30] [--no-esterni]
//
// Parte da: /, /ricerche, /metodo, /stato, /ricerche/<id> (da src/content/ricerche/indice.json, se c'e')
// e da ogni .html di --dist. Da HTML estrae href/src/action; dal JS compilato i letterali tra apici
// che sono URL http(s), percorsi con estensione di asset o .html, rotte note e chunk relativi (./x.js);
// dal CSS url(...); dai .md di src/content i link ](url). Poi controlla ogni URL (2xx/3xx = ok,
// redirect seguiti; interni con GET, esterni con HEAD e GET di riserva); mailto/tel/javascript/data saltati.
// API: GET {API_BASE}/live/frequenze e /live/scenari, con API_BASE da $VITE_API_BASE (default Render) e ogni
// letterale ".../api/v1" trovato nel bundle; la risposta 200 deve essere JSON valido.
// --statici <dir> (ripetibile): cartelle di riserva per i file che dist non ha (favicon, pagine legali del
// sito) come nel deploy; di quei file si verifica che esistano, ma non li si esplora. Uscita: 0 nessun link rotto, 1 almeno uno rotto, 2 uso errato.
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { parseArgs } from 'node:util'
import { creaServer } from './servi_dist.mjs'

const QUI = dirname(fileURLToPath(import.meta.url))
const API_DEFAULT = 'https://capohornlab-website.onrender.com/api/v1'
const API_PERCORSI = ['/live/frequenze', '/live/scenari']
const ROTTE = ['/', '/ricerche', '/metodo', '/stato']
const IGNORA = [/^https?:\/\/www\.w3\.org\//, /^https?:\/\/localhost(:\d+)?(\/|$)/, /^https:\/\/react\.dev\/errors/] // namespace XML, segnaposto, messaggi di errore
const ASSET = /\.(?:js|mjs|css|json|html|woff2?|png|jpe?g|svg|webp|ico|txt|xml|webmanifest|map)$/i
const SALTA = /^(?:mailto|tel|javascript|data|blob|about):/i

const { values: a } = parseArgs({
  options: {
    base: { type: 'string' }, dist: { type: 'string' }, statici: { type: 'string', multiple: true }, indice: { type: 'string' },
    contenuto: { type: 'string' }, timeout: { type: 'string', default: '30' }, 'no-esterni': { type: 'boolean' }, 'no-contenuto': { type: 'boolean' }, help: { type: 'boolean', short: 'h' },
  },
})
if (a.help) {
  console.log(readFileSync(fileURLToPath(import.meta.url), 'utf8').split('\n').filter((r) => r.startsWith('//')).map((r) => r.slice(3)).join('\n'))
  process.exit(0)
}

const dist = a.dist ?? (a.base ? undefined : join(QUI, '..', 'dist'))
if (dist && !existsSync(join(dist, 'index.html'))) {
  console.error(`dist non trovato: ${resolve(dist)}/index.html (eseguire npm run build)`)
  process.exit(2)
}
const timeoutMs = Number(a.timeout) * 1000
let server
let base = a.base?.replace(/\/$/, '')
if (!base) {
  server = creaServer([dist, ...(a.statici ?? [])])
  await new Promise((r) => server.listen(0, '127.0.0.1', r))
  base = `http://127.0.0.1:${server.address().port}`
}
const origine = new URL(base).origin

// ---- sorgenti di partenza
const trovati = new Map() // url -> { da, tipo }
const saltati = []
const ignorati = new Set()
const apiBase = new Set([(process.env.VITE_API_BASE ?? API_DEFAULT).replace(/\/$/, '')])
const contenuto = []

function aggiungi(raw, rispettoA, da, tipo) {
  if (!raw || raw.startsWith('#')) return
  if (SALTA.test(raw)) return saltati.push(raw)
  let u
  try {
    u = new URL(raw, rispettoA)
  } catch {
    return contenuto.push({ ok: false, stato: 'URL non valido', tipo: 'interno', url: raw, da })
  }
  if (!/^https?:$/.test(u.protocol)) return saltati.push(raw)
  u.hash = ''
  if (IGNORA.some((r) => r.test(u.href))) return ignorati.add(u.href)
  const url = u.href
  if (!trovati.has(url)) trovati.set(url, { da, tipo: tipo ?? (u.origin === origine ? 'interno' : 'esterno') })
}

for (const r of ROTTE) aggiungi(r, base + '/', 'rotte SPA')
function htmlDi(dir, rel = '') {
  for (const f of readdirSync(join(dir, rel))) {
    const p = join(rel, f)
    if (statSync(join(dir, p)).isDirectory()) htmlDi(dir, p)
    else if (f.endsWith('.html')) aggiungi('/' + p.replaceAll('\\', '/'), base + '/', 'file .html di dist')
  }
}
if (dist) htmlDi(dist)

const indice = a.indice ?? join(QUI, '..', 'src', 'content', 'ricerche', 'indice.json')
if (indice && existsSync(indice)) {
  const ids = []
  const raccogli = (v) => {
    if (Array.isArray(v)) v.forEach(raccogli)
    else if (v && typeof v === 'object') {
      if (typeof v.id === 'string') ids.push(v.id)
      Object.values(v).forEach((x) => typeof x === 'object' && raccogli(x))
    } else if (typeof v === 'string') ids.push(v)
  }
  raccogli(JSON.parse(readFileSync(indice, 'utf8')))
  for (const id of ids) {
    aggiungi(`/ricerche/${id}`, base + '/', 'indice.json')
    const md = join(dirname(indice), `${id}.md`)
    if (!existsSync(md)) contenuto.push({ ok: false, stato: 'assente', tipo: 'contenuto', url: md, da: 'indice.json' })
  }
}

const dirMd = a.contenuto ?? join(QUI, '..', 'src', 'content')
if (!a['no-contenuto'] && existsSync(dirMd)) {
  const md = (d) => readdirSync(d, { withFileTypes: true }).flatMap((e) => (e.isDirectory() ? md(join(d, e.name)) : e.name.endsWith('.md') ? [join(d, e.name)] : []))
  for (const f of md(dirMd)) {
    const t = readFileSync(f, 'utf8')
    for (const m of t.matchAll(/\]\(\s*(https?:\/\/[^)\s]+|\/[^)\s]*)/g)) aggiungi(m[1], base + '/', f.slice(dirMd.length + 1))
  }
}

for (const p of API_PERCORSI) aggiungi([...apiBase][0] + p, base + '/', 'API', 'api')

// ---- estrazione
function nuovaApi(b) {
  if (apiBase.has(b)) return
  apiBase.add(b)
  for (const p of API_PERCORSI) aggiungi(b + p, base + '/', 'API nel bundle', 'api')
}
const LETTERALE = (re) => new RegExp(`["'\`]${re}["'\`]`, 'g')
function estrai(testo, tipo, url) {
  const da = url.startsWith(base) ? url.slice(base.length) || '/' : url
  const vai = (raw) => aggiungi(raw, url, da)
  if (tipo === 'html') {
    for (const m of testo.matchAll(/\b(?:href|src|action|poster)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>"']+))/gi)) vai((m[1] ?? m[2] ?? m[3]).trim())
  } else if (tipo === 'css') {
    for (const m of testo.matchAll(/url\(\s*(["']?)([^"')\s]+)\1\s*\)/g)) vai(m[2])
  } else if (tipo === 'js') {
    for (const [, l] of testo.matchAll(LETTERALE('(https?:\\/\\/[^\\s"\'`\\\\$<>{}()]+)'))) {
      if (/\/api\/v1\/?$/.test(l)) nuovaApi(l.replace(/\/$/, ''))
      else vai(l)
    }
    for (const [, l] of testo.matchAll(LETTERALE('(\\/[A-Za-z0-9_\\-.~%/]*)'))) {
      if (l.startsWith('//') || l.startsWith('/live/') || l === '/') continue // /live/* = API, controllata con API_BASE
      if (ASSET.test(l) || ROTTE.some((r) => r !== '/' && (l === r || l.startsWith(r + '/')))) vai(l)
    }
    for (const [, l] of testo.matchAll(LETTERALE('(\\.{1,2}\\/[A-Za-z0-9_\\-./]+\\.(?:js|mjs|css|json|woff2?|png|jpe?g|svg|webp|ico))'))) vai(l) // chunk relativi al file
    for (const [, l] of testo.matchAll(LETTERALE('([A-Za-z0-9_\\-]+\\/[A-Za-z0-9_\\-./]+\\.(?:js|css|woff2?|png|jpe?g|svg|webp|ico))'))) aggiungi('/' + l, base + '/', da) // dipendenze di Vite, relative alla radice
  }
}

// ---- controllo
const tipoDi = (ct, url) => (/html/.test(ct) ? 'html' : /javascript/.test(ct) || /\.m?js$/.test(url) ? 'js' : /text\/css/.test(ct) ? 'css' : null)
const ritenta = async (f) => {
  try {
    return await f()
  } catch {
    return await f() // un solo nuovo tentativo sugli errori di rete (non sugli stati HTTP)
  }
}
const chiedi = (url, metodo, json) => fetch(url, { method: metodo, signal: AbortSignal.timeout(timeoutMs), headers: { 'user-agent': 'capohornlab-verifica-link/1.0', ...(json && { accept: 'application/json' }) } })

// file serviti da --statici (non da dist): se ne verifica l'esistenza, non si esplorano (e' il sito vecchio)
const soloEsiste = (url) => {
  if (!dist || !a.statici?.length) return false
  const p = decodeURIComponent(new URL(url).pathname)
  return /\.[A-Za-z0-9]+$/.test(p) && !existsSync(join(dist, '.' + p))
}

async function controlla(url, { da, tipo }) {
  const r = { ok: false, stato: '', tipo, url, da }
  try {
    if (tipo === 'esterno' && a['no-esterni']) return { ...r, ok: true, stato: 'saltato', tipo: 'esterno' }
    let res = await ritenta(() => chiedi(url, tipo === 'esterno' ? 'HEAD' : 'GET', tipo === 'api'))
    if (tipo === 'esterno' && res.status >= 400) {
      await res.body?.cancel()
      res = await ritenta(() => chiedi(url, 'GET'))
    }
    r.stato = String(res.status)
    r.ok = res.status < 400
    const ct = res.headers.get('content-type') ?? ''
    const t = r.ok && tipo === 'interno' && !soloEsiste(url) ? tipoDi(ct, url) : null
    if (tipo === 'api' && res.status === 200) {
      try {
        JSON.parse(await res.text())
      } catch {
        Object.assign(r, { ok: false, stato: '200 ma JSON non valido' })
      }
    } else if (t) estrai(await res.text(), t, url)
    else await res.body?.cancel()
  } catch (e) {
    r.stato = e.name === 'TimeoutError' ? `timeout ${a.timeout}s` : `errore ${e.cause?.code ?? e.message}`
  }
  return r
}

const risultati = [...contenuto]
const fatti = new Set()
while (fatti.size < trovati.size) {
  const lotto = [...trovati].filter(([u]) => !fatti.has(u)).slice(0, 8)
  lotto.forEach(([u]) => fatti.add(u))
  risultati.push(...(await Promise.all(lotto.map(([u, m]) => controlla(u, m)))))
}
if (server) {
  server.closeAllConnections()
  server.close()
}

// ---- rapporto
const corto = (u) => (u.startsWith(base) ? u.slice(base.length) || '/' : u)
const righe = risultati.filter((r) => r.stato !== 'saltato').sort((x, y) => x.ok - y.ok || x.tipo.localeCompare(y.tipo) || x.url.localeCompare(y.url))
console.log(`Base: ${base}${dist ? `  (dist: ${resolve(dist)})` : ''}\nAPI: ${[...apiBase].join(', ')}\n`)
console.log(['ESITO'.padEnd(6), 'CODICE'.padEnd(10), 'TIPO'.padEnd(9), 'URL'.padEnd(60), 'TROVATO IN'].join(' '))
for (const r of righe) console.log([(r.ok ? 'ok' : 'ROTTO').padEnd(6), r.stato.padEnd(10), r.tipo.padEnd(9), corto(r.url).padEnd(60), corto(r.da)].join(' '))
const rotti = righe.filter((r) => !r.ok).length
const esterniSaltati = risultati.length - righe.length
console.log(`\n${righe.length} URL controllati, ${saltati.length} saltati (mailto/tel/...)${esterniSaltati ? `, ${esterniSaltati} esterni saltati (--no-esterni)` : ''}, ${ignorati.size} ignorati (namespace/segnaposto), ${rotti} rotti`)
process.exitCode = rotti ? 1 : 0
