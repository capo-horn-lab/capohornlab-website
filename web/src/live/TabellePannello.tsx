// The app's "Frequenze live" panel for one instrument (desktop_tools.frequenze_text), same order, columns and text: STATO,
// FINESTRE, LIVELLI, CASO DELL'APERTURA, LENTI, CONCORDANZA. Frequencies in D8 (p% (k/n ±m), "k su n" at the extremes; a
// frequency without cases "n/d (0 casi)" as the panel), quartiles "mediana (q1-q3)". Hours from the payload's `orari`
// (DST-1: 14:30-21:00 in the weeks Europe and the US change clock on different dates), as the panel does.
import type { ReactNode } from 'react'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { finito, type Frequenza, intero, num, p, type Quartili, quart } from '@/lib/fmt'
import type { Orari, Percorso, RigaLente, StrumentoFrequenze } from '@/lib/tipi'

const segnato = (x: unknown) => (finito(x) ? `${x >= 0 ? '+' : ''}${num(x)}` : '-')

function orologio(minuti: number, base: string): string {
  const [h, m] = base.split(':').map(Number)
  const t = h * 60 + m + minuti
  return `${String(Math.floor(t / 60)).padStart(2, '0')}:${String(t % 60).padStart(2, '0')}`
}

/** Today's opening path in words (desktop_tools._percorso). */
export function percorsoTesto(pc: Percorso | null | undefined, S: number, base = '15:30'): string {
  if (!pc) return 'nessuna barra della sessione'
  if (pc.direzione == null)
    return `nessun movimento di ${S} punti finora (${pc.barre} barre); chiusura meno apertura finora ${segnato(pc.chiusura)}`
  const t1 = pc.t1
  const parti = [`primo movimento ${pc.direzione.toUpperCase()} alle ${orologio(t1, base)} (${t1} min dopo le ${base})`]
  if (pc.ritorno == null) parti.push(`non ancora tornato all'apertura; estensione finora ${intero(pc.estensione)}`)
  else {
    const tr = t1 + pc.ritorno
    parti.push(`ritorno all'apertura alle ${orologio(tr, base)} (${pc.ritorno} min dopo), estensione ${intero(pc.estensione)} prima del ritorno`)
    if (pc.opposto == null) parti.push(`${S} opposto: non ancora`)
    else {
      const to = tr + pc.opposto
      parti.push(`${S} opposto alle ${orologio(to, base)} (${pc.opposto} min dopo il ritorno)`)
      if (pc.ritorno2 == null) parti.push(`nuovo ritorno all'apertura: non ancora; estensione opposta finora ${intero(pc.estensione2)}`)
      else parti.push(`nuovo ritorno alle ${orologio(to + pc.ritorno2, base)} (${pc.ritorno2} min dopo), estensione opposta ${intero(pc.estensione2)}`)
    }
  }
  parti.push(`chiusura meno apertura finora ${segnato(pc.chiusura)}`)
  return parti.join('; ')
}

function Sezione({ titolo, nota, children }: { titolo: string; nota?: ReactNode; children?: ReactNode }) {
  return (
    <section className="space-y-2">
      <h3 className="font-mono text-xs font-medium tracking-wider">{titolo}</h3>
      {nota ? <div className="text-muted-foreground text-xs leading-relaxed">{nota}</div> : null}
      {children}
    </section>
  )
}

function Tabella({ teste, righe }: { teste: string[]; righe: { chiave: string; celle: ReactNode[] }[] }) {
  return (
    <Table className="font-mono text-xs tabular-nums">
      <TableHeader>
        <TableRow>
          {teste.map((t) => <TableHead key={t} className="h-8 text-xs">{t}</TableHead>)}
        </TableRow>
      </TableHeader>
      <TableBody>
        {righe.map((r) => (
          <TableRow key={r.chiave}>
            {r.celle.map((c, i) => <TableCell key={teste[i] ?? i} className="py-1.5">{c}</TableCell>)}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}

const barreOggi = (b: StrumentoFrequenze['barre_oggi']) =>
  b == null ? '-' : typeof b === 'number' ? String(b) : Object.entries(b).map(([k, v]) => `${k} ${v}`).join(', ')

const isP = (v: Frequenza | Quartili | null): v is Frequenza | null => v == null || 'p' in v

/** desktop_tools._pct's empty case: a frequency without cases reads "n/d (0 casi)". */
const pp = (f: Frequenza | null | undefined) => (f && finito(f.p) ? p(f) : 'n/d (0 casi)')

export function TabellePannello({ r, orari }: { r: StrumentoFrequenze; orari?: Orari | null }) {
  const st = r.stato ?? {}
  const n = (k: string) => num(st[k])
  const ap = orari?.apertura ?? '15:30'
  const ch = orari?.chiusura ?? '22:00'
  const caso = r.apertura
  const S = caso?.soglia ?? 0
  const h = caso?.storico
  const L = r.lenti
  const rif = L?.riferimento ?? {}
  const pende = (x: RigaLente, e: keyof RigaLente) => pp(x[e] as Frequenza | null) + ({ su: ' ^', giu: ' v' }[x.pende?.[e] ?? ''] ?? '')
  return (
    <div className="space-y-8">
      <Sezione titolo="STATO">
        <Tabella
          teste={['contratto', 'cadenza', "eta' del dato (min)", 'barre di oggi', 'prezzo', `A (range medio ${ap}-${ch} delle ultime ${r.A_sessioni ?? '-'} sessioni)`,
            'soglia (punti)', 'tondo', 'sessioni regolari nello storico']}
          righe={[{ chiave: 'stato', celle: [r.contratto, r.cadenza, r.eta_min ?? '-', barreOggi(r.barre_oggi), n('prezzo'), num(r.A), r.soglia ?? '-', r.passo_tondo ?? '-', r.n_storiche ?? '-'] }]}
        />
        <Tabella
          teste={['oggi dalle 00:00 max / min', `notte 00:00-${orologio(-1, ap)} max / min`, `apertura ${ap}`, `sessione dalle ${ap} max / min`, 'VWAP giorno',
            'VWAP sessione', `ieri ${typeof st.ieri === 'string' ? st.ieri : ''} max / min`, 'chiusura ieri']}
          righe={[{ chiave: 'livelli', celle: [`${n('massimo_oggi')} / ${n('minimo_oggi')}`, `${n('massimo_notte')} / ${n('minimo_notte')}`, n('apertura_1530'),
            `${n('massimo_sessione')} / ${n('minimo_sessione')}`, n('vwap_giorno'), n('vwap_sessione'), `${n('massimo_ieri')} / ${n('minimo_ieri')}`, n('chiusura_ieri')] }]}
        />
      </Sezione>

      <Sezione titolo="FINESTRE" nota="FINESTRE di Roma (ultime 60 sessioni): escursione max-min (mediana, quartili), netto |fine-inizio| (mediana), oggi finora; > = corrente">
        <Tabella
          teste={['finestra', 'n', 'escursione', 'netto', 'oggi']}
          righe={(r.finestre ?? []).map((w) => ({
            chiave: w.finestra,
            celle: [<span key="f">{`${w.corrente ? '> ' : ''}${w.finestra} `}<span className="text-muted-foreground">{w.nome}</span></span>,
              w.n ?? 0, quart(w.escursione), num(w.netto?.mediana, 0), num(w.oggi, 0)],
          }))}
        />
      </Sezione>

      <Sezione titolo="LIVELLI" nota={`tocco entro le ${ap} e le ${ch} nelle ultime 250 sessioni allo stesso minuto, stesso livello, stesso lato e stessa fascia di distanza in A`}>
        <Tabella
          teste={['livello', 'prezzo', 'dist', 'in A', 'fascia', `entro ${ap}`, `entro ${ch}`]}
          righe={(r.livelli ?? []).map((x) => ({
            chiave: x.nome,
            celle: [x.nome, num(x.prezzo), segnato(x.distanza), segnato(x.distanza_A), x.fascia || '-', x.entro_1530 ? pp(x.entro_1530) : '-', x.entro_2200 ? pp(x.entro_2200) : '-'],
          }))}
        />
      </Sezione>

      <Sezione titolo="CASO DELL'APERTURA" nota={caso ? `soglia ${S} punti dall'apertura delle ${ap}; fase: ${caso.fase}; ${caso.minuti} minuti dalle ${ap}${caso.barre === '5 min' ? "; ATTENZIONE: oggi barre a 5 minuti (il feed a 1 minuto manca): tempi a 5 minuti e piu' fasi possono cadere nella stessa barra" : ''}` : 'n/d'}>
        {caso ? (
          <>
            <p className="font-mono text-xs leading-relaxed">{`oggi: ${percorsoTesto(caso.percorso, S, ap)}`}</p>
            <p className="font-mono text-xs leading-relaxed">{`storico: ${h?.n ?? '-'} sessioni su ${h?.n_totale ?? '-'} nella stessa fase con lo stesso verso a questo minuto; tempi ${h?.riferimento ?? '-'}`}</p>
            <Tabella
              teste={['frequenza', 'valore']}
              righe={Object.entries(h?.frequenze ?? {}).map(([nome, v]) => ({ chiave: nome, celle: [nome, isP(v) ? pp(v) : `${quart(v)} (n ${v.n ?? '-'})`] }))}
            />
          </>
        ) : null}
      </Sezione>

      <Sezione titolo="LENTI" nota={L?.base ? `ciascuna DA SOLA sulle ultime ${L.campione?.n ?? '-'} sessioni regolari allo stesso minuto di Roma (${String(rif.ora ?? '-')}), mai in intersezione; esiti dal prezzo ${num(rif.prezzo)} entro le ${ch}, 0.3 A = ${num(0.3 * (r.A ?? 0), 0)} punti; margine = max(1,96 sqrt(p(1-p)/n), 3/n); ^ pende su, v pende giu' (oltre il proprio margine dalla base)${rif.mercato === 'chiuso' ? `; ${String(rif.nota ?? '').toUpperCase()}` : ''}` : 'n/d'}>
        {L?.base ? (
          <Tabella
            teste={['lente', 'stato', 'n', 'chiusura sopra', 'nuovo min notte', 'nuovo max notte', '+0.3 A', '-0.3 A', 'est. sopra (A)', 'est. sotto (A)']}
            righe={[L.base, ...(L.righe ?? [])].map((x) => ({
              chiave: x.lente,
              celle: [x.lente, x.stato == null ? '-' : `${x.stato}${x.valore ? ` (${x.valore})` : ''}`, x.n ?? 0, pende(x, 'chiusura_sopra'),
                pp(x.nuovo_minimo), pp(x.nuovo_massimo), pende(x, 'arrivo_sopra'), pende(x, 'arrivo_sotto'), quart(x.estensione_sopra_A, 2), quart(x.estensione_sotto_A, 2)],
            }))}
          />
        ) : null}
      </Sezione>

      <Sezione titolo="CONCORDANZA">
        <p className="font-mono text-xs leading-relaxed">{L?.concordanza?.frase ?? 'n/d'}</p>
      </Sezione>
    </div>
  )
}
