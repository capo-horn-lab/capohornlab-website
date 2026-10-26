// The app's "Frequenze live" panel for one instrument (desktop_tools.frequenze_text), same order and columns: STATO, FINESTRE,
// LIVELLI, CASO DELL'APERTURA, LENTI, CONCORDANZA. Frequencies in D8 (p% (k/n ±m), "k su n" at the extremes), quartiles
// "mediana (q1-q3)". The clock times of the opening path count from the payload's own open (orari.apertura).
import type { ReactNode } from 'react'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { type Frequenza, intero, num, p, type Quartili, quart } from '@/lib/fmt'
import type { Orari, Percorso, RigaLente, StrumentoFrequenze } from '@/lib/tipi'

const segnato = (x: number) => `${x >= 0 ? '+' : ''}${x.toFixed(2)}`

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

export function TabellePannello({ r, orari }: { r: StrumentoFrequenze; orari?: Orari | null }) {
  const st = r.stato ?? {}
  const n = (k: string) => num(st[k] as number | null)
  const base = orari?.apertura ?? '15:30'
  const ap = r.apertura
  const S = ap?.soglia ?? 0
  const h = ap?.storico
  const L = r.lenti
  const pende = (x: RigaLente, e: keyof RigaLente) => p(x[e] as Frequenza | null) + ({ su: ' ^', giu: ' v' }[x.pende?.[e] ?? ''] ?? '')
  return (
    <div className="space-y-8">
      <Sezione titolo="STATO" nota={orari && base !== '15:30' ? `Questa settimana la sessione regolare e' ${orari.apertura}-${orari.chiusura} Roma: "15:30" e "22:00" nelle colonne sono nomi convenzionali.` : undefined}>
        <Tabella
          teste={['contratto', 'cadenza', "eta' (min)", 'barre di oggi', 'prezzo', `A (${r.A_sessioni ?? '-'} sessioni)`, 'soglia', 'tondo', 'sessioni storiche']}
          righe={[{ chiave: 'stato', celle: [r.contratto, r.cadenza, r.eta_min ?? '-', barreOggi(r.barre_oggi), n('prezzo'), num(r.A), r.soglia ?? '-', r.passo_tondo ?? '-', r.n_storiche ?? '-'] }]}
        />
        <Tabella
          teste={['oggi max / min', 'notte max / min', 'sessione max / min', `apertura ${base}`, 'VWAP giorno', 'VWAP sessione', `ieri ${st.ieri ?? ''} max / min`, 'chiusura ieri']}
          righe={[{ chiave: 'livelli', celle: [`${n('massimo_oggi')} / ${n('minimo_oggi')}`, `${n('massimo_notte')} / ${n('minimo_notte')}`,
            `${n('massimo_sessione')} / ${n('minimo_sessione')}`, n('apertura_1530'), n('vwap_giorno'), n('vwap_sessione'),
            `${n('massimo_ieri')} / ${n('minimo_ieri')}`, n('chiusura_ieri')] }]}
        />
      </Sezione>

      <Sezione titolo="FINESTRE" nota="Finestre di Roma (ultime 60 sessioni): escursione massimo-minimo (mediana, quartili), netto |fine-inizio| (mediana), oggi finora; > = corrente.">
        <Tabella
          teste={['finestra', 'n', 'escursione', 'netto', 'oggi']}
          righe={(r.finestre ?? []).map((w) => ({
            chiave: w.finestra,
            celle: [<span key="f">{`${w.corrente ? '> ' : ''}${w.finestra} `}<span className="text-muted-foreground">{w.nome}</span></span>,
              w.n ?? 0, quart(w.escursione), num(w.netto?.mediana, 0), num(w.oggi, 0)],
          }))}
        />
      </Sezione>

      <Sezione titolo="LIVELLI" nota="Tocco entro le 15:30 e le 22:00 nelle ultime 250 sessioni allo stesso minuto, stesso livello, stesso lato e stessa fascia di distanza in A.">
        <Tabella
          teste={['livello', 'prezzo', 'dist', 'in A', 'fascia', 'entro 15:30', 'entro 22:00']}
          righe={(r.livelli ?? []).map((x) => ({
            chiave: x.nome,
            celle: [x.nome, num(x.prezzo), segnato(x.distanza), segnato(x.distanza_A), x.fascia || '-', p(x.entro_1530), p(x.entro_2200)],
          }))}
        />
      </Sezione>

      <Sezione titolo="CASO DELL'APERTURA" nota={ap ? `Soglia ${S} punti dall'apertura delle ${base}; fase: ${ap.fase}; ${ap.minuti} minuti dalle ${base}${ap.barre === '5 min' ? "; ATTENZIONE: oggi barre a 5 minuti (il feed a 1 minuto manca): tempi a 5 minuti e piu' fasi possono cadere nella stessa barra" : ''}.` : 'n/d'}>
        {ap ? (
          <>
            <p className="font-mono text-xs leading-relaxed">{`oggi: ${percorsoTesto(ap.percorso, S, base)}`}</p>
            <p className="font-mono text-xs leading-relaxed">{`storico: ${h?.n ?? '-'} sessioni su ${h?.n_totale ?? '-'} nella stessa fase con lo stesso verso a questo minuto; tempi ${h?.riferimento ?? '-'}`}</p>
            <Tabella
              teste={['frequenza', 'valore']}
              righe={Object.entries(h?.frequenze ?? {}).map(([nome, v]) => ({ chiave: nome, celle: [nome, isP(v) ? p(v) : `${quart(v)} (n ${v.n ?? '-'})`] }))}
            />
          </>
        ) : null}
      </Sezione>

      <Sezione titolo="LENTI" nota={L?.base ? `Ciascuna da sola sulle ultime ${L.campione?.n ?? '-'} sessioni regolari allo stesso minuto di Roma (${String(L.riferimento?.ora ?? '-')}), mai in intersezione; esiti dal prezzo ${num(L.riferimento?.prezzo as number | null)} entro le 22:00, 0.3 A = ${num(0.3 * (r.A ?? 0), 0)} punti; ^ pende su, v pende giu' (oltre il proprio margine dalla base)${L.riferimento?.mercato === 'chiuso' ? `; ${String(L.riferimento?.nota ?? '').toUpperCase()}` : ''}.` : 'n/d'}>
        {L?.base ? (
          <Tabella
            teste={['lente', 'stato', 'n', 'chiusura sopra', 'nuovo min notte', 'nuovo max notte', '+0.3 A', '-0.3 A', 'est. sopra (A)', 'est. sotto (A)']}
            righe={[L.base, ...(L.righe ?? [])].map((x) => ({
              chiave: x.lente,
              celle: [x.lente, x.stato == null ? '-' : `${x.stato}${x.valore ? ` (${x.valore})` : ''}`, x.n ?? 0, pende(x, 'chiusura_sopra'),
                p(x.nuovo_minimo), p(x.nuovo_massimo), pende(x, 'arrivo_sopra'), pende(x, 'arrivo_sotto'), quart(x.estensione_sopra_A, 2), quart(x.estensione_sotto_A, 2)],
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
