#!/usr/bin/env node
// Lancia Lighthouse (mobile, performance + accessibilita') su un URL, salva il JSON, stampa i punteggi.
//   node scripts/lighthouse.mjs <url> [--out file.json] [--min-perf 80] [--min-a11y 90]
//   node scripts/lighthouse.mjs --da-json file.json [--min-perf 80] [--min-a11y 90]   (valuta un rapporto gia' salvato)
// Esegue: npx -y lighthouse@12 <url> --only-categories=performance,accessibility --form-factor=mobile
//   --screenEmulation.mobile --output=json --output-path=<file> --chrome-flags="--headless=new"
// Nessuna shell: l'URL deve essere http(s) senza virgolette, spazi, % o caratteri di controllo, altrimenti uscita 2 prima di lanciare qualsiasi cosa.
// Serve Chrome installato (o CHROME_PATH). Uscita: 0 sopra le soglie, 1 sotto, 2 Lighthouse fallito / uso errato / URL o rapporto non validi.
import { spawnSync } from 'node:child_process'
import { existsSync, readFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { leggiArgomenti } from './args.mjs'

const { values: a, positionals } = leggiArgomenti({
  allowPositionals: true,
  options: { out: { type: 'string' }, 'min-perf': { type: 'string', default: '80' }, 'min-a11y': { type: 'string', default: '90' }, 'da-json': { type: 'string' }, help: { type: 'boolean', short: 'h' } },
})
if (a.help) {
  console.log(readFileSync(fileURLToPath(import.meta.url), 'utf8').split('\n').filter((r) => r.startsWith('//')).map((r) => r.slice(3)).join('\n'))
  process.exit(0)
}

let file = a['da-json']
if (!file) {
  const url = positionals[0]
  if (!url) {
    console.error('uso: node scripts/lighthouse.mjs <url> [--out file.json] [--min-perf 80] [--min-a11y 90]')
    process.exit(2)
  }
  // solo http(s), senza virgolette, spazi, % o caratteri di controllo (l'URL finisce in una riga di comando)
  let valido = !/[\s"%\u0000-\u001f\u007f]/.test(url)
  try {
    valido &&= /^https?:$/.test(new URL(url).protocol)
  } catch {
    valido = false
  }
  if (!valido) {
    console.error(`URL non valido: ${JSON.stringify(url)} (serve http:// o https://, senza virgolette, spazi, % o caratteri di controllo)`)
    process.exit(2)
  }
  file = a.out ?? join(tmpdir(), `lighthouse-${Date.now()}.json`)
  const args = ['-y', 'lighthouse@12', url, '--only-categories=performance,accessibility', '--form-factor=mobile', '--screenEmulation.mobile', '--output=json', `--output-path=${file}`, '--chrome-flags=--headless=new', '--quiet']
  // niente shell: su Windows npx e' npx.cmd e Node >= 20.12 rifiuta di avviare i .cmd senza shell (EINVAL), quindi si lancia npx-cli.js di npm con node
  const cli = [join(dirname(process.execPath), 'node_modules', 'npm', 'bin', 'npx-cli.js'), join(dirname(process.execPath), '..', 'lib', 'node_modules', 'npm', 'bin', 'npx-cli.js')].find(existsSync)
  const r = cli ? spawnSync(process.execPath, [cli, ...args], { shell: false, stdio: ['ignore', 'inherit', 'inherit'] }) : spawnSync('npx', args, { shell: false, stdio: ['ignore', 'inherit', 'inherit'] })
  if (r.status !== 0 || !existsSync(file)) {
    console.error(`Lighthouse fallito (${r.error?.message ?? `codice ${r.status}`}); nessun rapporto in ${file}`)
    process.exit(2)
  }
}

let rapporto
try {
  rapporto = JSON.parse(readFileSync(file, 'utf8'))
} catch (e) {
  console.error(`rapporto non leggibile: ${file} (${e.code ?? e.message})`)
  process.exit(2)
}
const punteggio = (c) => Math.round((rapporto.categories?.[c]?.score ?? NaN) * 100)
const soglie = [['performance', Number(a['min-perf'])], ['accessibility', Number(a['min-a11y'])]]
console.log(`Rapporto: ${file}${rapporto.finalDisplayedUrl ? `  (${rapporto.finalDisplayedUrl})` : ''}`)
let sotto = 0
for (const [cat, min] of soglie) {
  const p = punteggio(cat)
  const ok = p >= min
  sotto += ok ? 0 : 1
  console.log(`${cat.padEnd(14)} ${String(p).padStart(3)}  (minimo ${min})  ${ok ? 'ok' : 'SOTTO SOGLIA'}`)
}
const extra = [['largest-contentful-paint', 'LCP'], ['total-blocking-time', 'TBT'], ['cumulative-layout-shift', 'CLS']].map(([k, n]) => (rapporto.audits?.[k] ? `${n} ${rapporto.audits[k].displayValue}` : null)).filter(Boolean)
if (extra.length) console.log(extra.join('  '))
process.exitCode = sotto ? 1 : 0
