// Test di servi_dist.mjs, verifica_link.mjs e lighthouse.mjs (--da-json).
// Uso: node web/scripts/test_verifica_link.mjs   (esce con codice diverso da 0 se un test fallisce)
import assert from 'node:assert/strict'
import { spawn } from 'node:child_process'
import http from 'node:http'
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { dirname, join } from 'node:path'
import { after, describe, it } from 'node:test'
import { fileURLToPath } from 'node:url'
import { gunzipSync } from 'node:zlib'

const QUI = dirname(fileURLToPath(import.meta.url))
const SERVI = join(QUI, 'servi_dist.mjs')
const LINK = join(QUI, 'verifica_link.mjs')
const LIGHTHOUSE = join(QUI, 'lighthouse.mjs')
const radice = mkdtempSync(join(tmpdir(), 'verifica-link-'))
after(() => rmSync(radice, { recursive: true, force: true }))

/** Crea una cartella con i file dati ({percorso: contenuto}). */
let n = 0
function sito(files, nome = `sito${n++}`) {
  const dir = join(radice, nome)
  for (const [p, c] of Object.entries(files)) {
    mkdirSync(dirname(join(dir, p)), { recursive: true })
    writeFileSync(join(dir, p), c)
  }
  return dir
}

function esegui(script, args = [], env = {}) {
  return new Promise((risolvi) => {
    const p = spawn(process.execPath, [script, ...args], { env: { ...process.env, ...env } })
    let out = ''
    p.stdout.on('data', (d) => (out += d))
    p.stderr.on('data', (d) => (out += d))
    p.on('close', (code) => risolvi({ code, out }))
  })
}

/** Server finto in-process (API ed esterni). `gestore(req) -> [stato, corpo]`. */
async function finto(gestore) {
  const s = http.createServer((req, res) => {
    const [stato, corpo = ''] = gestore(req)
    res.writeHead(stato, { 'content-type': 'application/json' })
    res.end(req.method === 'HEAD' ? undefined : corpo)
  })
  await new Promise((r) => s.listen(0, '127.0.0.1', r))
  return { url: `http://127.0.0.1:${s.address().port}`, chiudi: () => new Promise((r) => s.close(r)) }
}

const apiOk = () => finto(() => [200, '{"ok":true}'])
const ISOLA = ['--indice', '', '--no-contenuto'] // niente indice/contenuto reali del repo: test ermetici
const HTML = (corpo) => `<!doctype html><html><body>${corpo}</body></html>`

describe('servi_dist', () => {
  async function avvia(...dirs) {
    const args = dirs.flatMap((d) => ['--dir', d]).concat(['--port', '0'])
    const p = spawn(process.execPath, [SERVI, ...args])
    const url = await new Promise((ok, ko) => {
      p.stdout.on('data', (d) => /(http:\/\/127\.0\.0\.1:\d+)/.test(String(d)) && ok(RegExp.$1))
      p.on('close', () => ko(new Error('servi_dist chiuso')))
    })
    return { url, ferma: () => p.kill() }
  }

  it('serve file con MIME corretti, fallback SPA solo per le rotte, 404 altrove, HEAD, niente uscita dalla cartella', async () => {
    const dir = sito({ 'index.html': HTML('home'), 'app/a.js': 'x', 'app/a.css': 'x', 'f.woff2': 'x', 'd.json': '{}', 'i.svg': '<svg/>', 'favicon.ico': 'x', 'public/legale.html': HTML('legale') }, 'servito/site')
    writeFileSync(join(dir, '..', 'segreto.txt'), 'segreto')
    writeFileSync(join(dir, '.env'), 'TOKEN=x')
    const s = await avvia(dir)
    try {
      const get = (p, o) => fetch(s.url + p, o)
      const tipo = async (p) => (await get(p)).headers.get('content-type')
      assert.match(await tipo('/'), /text\/html/)
      assert.match(await tipo('/app/a.js'), /javascript/)
      assert.match(await tipo('/app/a.css'), /text\/css/)
      assert.match(await tipo('/d.json'), /application\/json/)
      assert.match(await tipo('/f.woff2'), /font\/woff2/)
      assert.match(await tipo('/i.svg'), /image\/svg\+xml/)
      assert.match(await tipo('/favicon.ico'), /icon/)
      for (const rotta of ['/ricerche', '/ricerche/phase-1', '/metodo', '/stato/']) {
        const r = await get(rotta)
        assert.equal(r.status, 200, rotta)
        assert.match(await r.text(), /home/, rotta)
      }
      assert.equal((await get('/non-esiste')).status, 404)
      assert.equal((await get('/app/mancante.js')).status, 404)
      assert.equal((await get('/ricerche/x.js')).status, 404)
      const h = await get('/', { method: 'HEAD' })
      assert.equal(h.status, 200)
      assert.equal(await h.text(), '')
      const fuori = await new Promise((r) => http.get(s.url + '/%2e%2e/segreto.txt', { agent: false }, (res) => (res.resume(), r(res.statusCode))))
      assert.notEqual(fuori, 200)
      assert.equal((await get('/.env')).status, 403)
    } finally {
      s.ferma()
    }
  })

  it('gzip se il client lo accetta (js/css/html/json), mai per i font', async () => {
    const dir = sito({ 'index.html': HTML('home'), 'app/a.js': 'const x = 1;'.repeat(50), 'f.woff2': 'x' })
    const s = await avvia(dir)
    const chiedi = (p, codifica) => new Promise((r) => http.get(s.url + p, { agent: false, headers: { 'accept-encoding': codifica } }, (res) => {
      const pezzi = []
      res.on('data', (d) => pezzi.push(d)).on('end', () => r({ codifica: res.headers['content-encoding'], corpo: Buffer.concat(pezzi) }))
    }))
    try {
      const g = await chiedi('/app/a.js', 'gzip')
      assert.equal(g.codifica, 'gzip')
      assert.equal(gunzipSync(g.corpo).toString(), 'const x = 1;'.repeat(50))
      assert.equal((await chiedi('/app/a.js', 'identity')).codifica, undefined)
      assert.equal((await chiedi('/f.woff2', 'gzip')).codifica, undefined)
    } finally {
      s.ferma()
    }
  })

  it('--dir ripetuto: il primo che ha il file vince, gli altri fanno da riserva', async () => {
    const a = sito({ 'index.html': HTML('A') })
    const b = sito({ 'index.html': HTML('B'), 'legale.html': HTML('legale') })
    const s = await avvia(a, b)
    try {
      assert.match(await (await fetch(s.url + '/')).text(), />A</)
      assert.match(await (await fetch(s.url + '/legale.html')).text(), /legale/)
    } finally {
      s.ferma()
    }
  })
})

describe('verifica_link --dist', () => {
  const base = { 'index.html': HTML('<a href="/pagina.html">p</a><link rel="stylesheet" href="/app/s.css"><script type="module" src="/app/i.js"></script>'), 'pagina.html': HTML('ok'), 'app/s.css': '@font-face{src:url(/fonts/f.woff2)}', 'fonts/f.woff2': 'x', 'app/i.js': 'import("./chunk.js");' + 'fetch(`${B}/live/frequenze`)', 'app/chunk.js': 'export{}' }

  async function lancia(files, args = [], env = {}) {
    const api = await apiOk()
    try {
      return await esegui(LINK, ['--dist', sito({ ...base, ...files }), '--no-esterni', ...ISOLA, ...args], { VITE_API_BASE: api.url + '/api/v1', ...env })
    } finally {
      await api.chiudi()
    }
  }

  it('tutto presente (mailto/tel saltati, API ok) -> 0', async () => {
    const r = await lancia({ 'pagina.html': HTML('<a href="mailto:a@b.it">m</a><a href="tel:+390">t</a><a href="#x">x</a>') })
    assert.equal(r.code, 0, r.out)
    assert.match(r.out, /0 rotti/)
  })

  it('link HTML rotto -> 1 e lo nomina', async () => {
    const r = await lancia({ 'pagina.html': HTML('<a href="/mancante.html">x</a>') })
    assert.equal(r.code, 1, r.out)
    assert.match(r.out, /\/mancante\.html/)
    assert.match(r.out, /404/)
  })

  it('letterale rotto dentro il JS (percorso e chunk relativo) -> 1', async () => {
    let r = await lancia({ 'app/i.js': 'fetch("/dati-mancanti.json")' })
    assert.equal(r.code, 1, r.out)
    assert.match(r.out, /dati-mancanti\.json/)
    r = await lancia({ 'app/i.js': 'import(`./chunk-mancante.js`)' })
    assert.equal(r.code, 1, r.out)
    assert.match(r.out, /chunk-mancante\.js/)
  })

  it('url() rotto nel CSS -> 1', async () => {
    const r = await lancia({ 'app/s.css': '@font-face{src:url(/fonts/assente.woff2)}' })
    assert.equal(r.code, 1, r.out)
    assert.match(r.out, /assente\.woff2/)
  })

  it('rotte SPA e id di indice.json: ricerca senza contenuto -> 1', async () => {
    const dir = sito({ 'indice.json': '[{"id":"a"},{"id":"b"}]', 'a.md': '#', 'b.md': '#' }, 'contenuto-ok')
    let r = await lancia({}, ['--indice', join(dir, 'indice.json')])
    assert.equal(r.code, 0, r.out)
    assert.match(r.out, /\/ricerche\/a/)
    const dir2 = sito({ 'indice.json': '[{"id":"a"},{"id":"b"}]', 'a.md': '#' }, 'contenuto-ko')
    r = await lancia({}, ['--indice', join(dir2, 'indice.json')])
    assert.equal(r.code, 1, r.out)
    assert.match(r.out, /b\.md/)
  })

  it('API /live/frequenze e /live/scenari: 503 -> 1; stesso host del bundle controllato in piu\'', async () => {
    const ko = await finto((req) => (req.url.endsWith('/scenari') ? [503, 'giu'] : [200, '{}']))
    try {
      const r = await esegui(LINK, ['--dist', sito(base), '--no-esterni', ...ISOLA], { VITE_API_BASE: ko.url + '/api/v1' })
      assert.equal(r.code, 1, r.out)
      assert.match(r.out, /\/live\/scenari/)
      assert.match(r.out, /503/)
    } finally {
      await ko.chiudi()
    }
  })

  it('API_BASE trovato nel bundle (…/api/v1) e controllato anche se diverso dall\'env', async () => {
    const dalBundle = await finto((req) => (req.url.endsWith('/frequenze') ? [404, ''] : [200, '{}']))
    try {
      const r = await lancia({ 'app/i.js': `const B="${dalBundle.url}/api/v1";fetch(B+"/live/frequenze")` })
      assert.equal(r.code, 1, r.out)
      assert.match(r.out, new RegExp(`${dalBundle.url.replace(/\./g, '\\.')}/api/v1/live/frequenze`))
    } finally {
      await dalBundle.chiudi()
    }
  })

  it('link esterni: rotto -> 1, --no-esterni li salta', async () => {
    const ext = await finto((req) => (req.url === '/ko' ? [404, ''] : [200, 'ok']))
    const api = await apiOk()
    try {
      const dir = sito({ ...base, 'pagina.html': HTML(`<a href="${ext.url}/ok">ok</a><a href="${ext.url}/ko">ko</a>`) })
      const env = { VITE_API_BASE: api.url + '/api/v1' }
      let r = await esegui(LINK, ['--dist', dir, ...ISOLA], env)
      assert.equal(r.code, 1, r.out)
      assert.match(r.out, /\/ko/)
      r = await esegui(LINK, ['--dist', dir, '--no-esterni', ...ISOLA], env)
      assert.equal(r.code, 0, r.out)
    } finally {
      await ext.chiudi()
      await api.chiudi()
    }
  })

  it('--statici: una cartella di riserva fornisce le pagine legali', async () => {
    const legale = sito({ 'cookie.html': HTML('c') })
    const files = { 'pagina.html': HTML('<a href="/cookie.html">c</a>') }
    let r = await lancia(files)
    assert.equal(r.code, 1, r.out)
    r = await lancia(files, ['--statici', legale])
    assert.equal(r.code, 0, r.out)
    // i file delle statiche si verificano ma non si esplorano: i loro link interni non contano
    const legale2 = sito({ 'cookie.html': HTML('<a href="/vecchia-pagina.html">v</a>') })
    r = await lancia(files, ['--statici', legale2])
    assert.equal(r.code, 0, r.out)
  })

  it('--dist inesistente -> 2', async () => {
    const r = await esegui(LINK, ['--dist', join(radice, 'non-esiste')])
    assert.equal(r.code, 2, r.out)
  })
})

describe('verifica_link --base', () => {
  it('controlla un URL gia\' servito (servi_dist in un altro processo)', async () => {
    const dir = sito({ 'index.html': HTML('<a href="/manca.html">x</a>') })
    const p = spawn(process.execPath, [SERVI, '--dir', dir, '--port', '0'])
    const url = await new Promise((ok) => p.stdout.on('data', (d) => /(http:\/\/127\.0\.0\.1:\d+)/.test(String(d)) && ok(RegExp.$1)))
    const api = await apiOk()
    try {
      const r = await esegui(LINK, ['--base', url, '--no-esterni', '--timeout', '5', ...ISOLA], { VITE_API_BASE: api.url + '/api/v1' })
      assert.equal(r.code, 1, r.out)
      assert.match(r.out, /\/manca\.html/)
    } finally {
      p.kill()
      await api.chiudi()
    }
  })
})

describe('lighthouse --da-json', () => {
  const rapporto = (perf, a11y) => JSON.stringify({ categories: { performance: { score: perf }, accessibility: { score: a11y } }, audits: { 'largest-contentful-paint': { displayValue: '1.8 s' } } })
  const file = (nome, perf, a11y) => {
    const f = join(radice, nome)
    writeFileSync(f, rapporto(perf, a11y))
    return f
  }

  it('sopra soglia -> 0 e stampa i due punteggi', async () => {
    const r = await esegui(LIGHTHOUSE, ['--da-json', file('ok.json', 0.91, 0.95)])
    assert.equal(r.code, 0, r.out)
    assert.match(r.out, /91/)
    assert.match(r.out, /95/)
  })

  it('sotto soglia -> 1, soglie regolabili', async () => {
    const f = file('basso.json', 0.5, 0.95)
    let r = await esegui(LIGHTHOUSE, ['--da-json', f])
    assert.equal(r.code, 1, r.out)
    assert.match(r.out, /performance/i)
    r = await esegui(LIGHTHOUSE, ['--da-json', f, '--min-perf', '40'])
    assert.equal(r.code, 0, r.out)
    r = await esegui(LIGHTHOUSE, ['--da-json', file('a11y.json', 0.95, 0.8)])
    assert.equal(r.code, 1, r.out)
  })
})
