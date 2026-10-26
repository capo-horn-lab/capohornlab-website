#!/usr/bin/env node
// Lancia Lighthouse (mobile, performance + accessibilita') su un URL, salva il JSON, stampa i punteggi.
//   node scripts/lighthouse.mjs <url> [--out file.json] [--min-perf 80] [--min-a11y 90]
//   node scripts/lighthouse.mjs --da-json file.json [--min-perf 80] [--min-a11y 90]   (valuta un rapporto gia' salvato)
// Esegue: npx -y lighthouse@12 <url> --only-categories=performance,accessibility --form-factor=mobile
//   --screenEmulation.mobile --output=json --output-path=<file> --chrome-flags="--headless=new"
// Serve Chrome installato (o CHROME_PATH). Uscita: 0 sopra le soglie, 1 sotto, 2 Lighthouse fallito / uso errato.
import { spawnSync } from 'node:child_process'
import { existsSync, readFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { parseArgs } from 'node:util'

const { values: a, positionals } = parseArgs({
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
  file = a.out ?? join(tmpdir(), `lighthouse-${Date.now()}.json`)
  const q = (s) => (/[\s&|<>^"]/.test(s) ? `"${s}"` : s) // npx e' npx.cmd su Windows: serve la shell
  const args = ['-y', 'lighthouse@12', url, '--only-categories=performance,accessibility', '--form-factor=mobile', '--screenEmulation.mobile', '--output=json', `--output-path=${file}`, '--chrome-flags="--headless=new"', '--quiet']
  const r = spawnSync('npx', args.map(q), { shell: true, stdio: ['ignore', 'inherit', 'inherit'] })
  if (r.status !== 0 || !existsSync(file)) {
    console.error(`Lighthouse fallito (codice ${r.status}); nessun rapporto in ${file}`)
    process.exit(2)
  }
}

const rapporto = JSON.parse(readFileSync(file, 'utf8'))
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
