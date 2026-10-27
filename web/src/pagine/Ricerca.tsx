import { useQuery } from '@tanstack/react-query'
import type { ReactNode } from 'react'
import { Link, useParams } from 'react-router'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { caricaDati, caricaRicerca } from '@/ricerche/archivio'
import { Grafico } from '@/ricerche/Grafico'
import { dividiFonti, idSezione, leggiElenco, leggiPrefazio, leggiTabella } from '@/ricerche/modello'
import { AuditBadge, InLinea, Paragrafi, VerdettoBadge } from '@/ricerche/Testo'

function Sezione({ titolo, children }: { titolo: string; children: ReactNode }) {
  const id = `s-${idSezione(titolo)}`
  return (
    <section aria-labelledby={id} className="flex flex-col gap-3">
      <h2 id={id} className="font-serif text-2xl font-semibold tracking-tight">
        {titolo}
      </h2>
      {children}
    </section>
  )
}

function Elenco({ voci }: { voci: string[] }) {
  return (
    <ul className="text-foreground/90 flex list-disc flex-col gap-1.5 pl-5 leading-relaxed">
      {voci.map((v, i) => (
        <li key={i}>
          <InLinea testo={v} />
        </li>
      ))}
    </ul>
  )
}

export default function Ricerca() {
  const { id = '' } = useParams()
  const { data: r, isPending } = useQuery({ queryKey: ['ricerca', id], queryFn: () => caricaRicerca(id), staleTime: Infinity })
  const { data: dati } = useQuery({ queryKey: ['dati', id], queryFn: () => caricaDati(id), staleTime: Infinity })

  if (isPending) return <Skeleton className="h-10 w-96" />
  if (!r) {
    return (
      <section className="flex flex-col gap-3">
        <h1 className="font-serif text-3xl font-semibold">Ricerca non trovata</h1>
        <p className="text-muted-foreground">Nessuna pagina per «{id}».</p>
        <Link to="/ricerche" className="underline underline-offset-4">
          Torna all'elenco
        </Link>
      </section>
    )
  }

  const { fm, sezioni } = r
  const esito = leggiTabella(sezioni['Esito'] ?? '')
  const nonRiportate = leggiPrefazio(sezioni['Esito'] ?? '')
  const note = leggiElenco(sezioni['Ritiri e correzioni'] ?? '')
  const stato = fm.audit?.stato
  const titoloNota = stato
    ? `${stato === 'ritirato' ? "Ritirato dall'audit" : "Corretto dall'audit"}: ${fm.audit?.id.join(', ')}`
    : "Nota dell'audit"

  return (
    <article className="flex max-w-4xl flex-col gap-8">
      <header className="flex flex-col gap-3">
        <Link to="/ricerche" className="text-muted-foreground text-sm underline-offset-4 hover:underline">
          ← Ricerche
        </Link>
        <h1 className="font-serif text-3xl leading-tight font-semibold tracking-tight sm:text-4xl">{fm.titolo}</h1>
        <div className="text-muted-foreground flex flex-wrap items-center gap-x-4 gap-y-2 text-sm">
          <span className="font-mono">{fm.data}</span>
          {fm.strumenti.length > 0 && <span className="font-mono">{fm.strumenti.join(' · ')}</span>}
          <VerdettoBadge verdetto={fm.verdetto} max={6} />
          {stato && <AuditBadge audit={stato} />}
          {fm.avvertenza && <Badge variant="outline">con avvertenza</Badge>}
        </div>
        {fm.finestra && <p className="text-muted-foreground text-sm">Dati: {fm.finestra.replace(/`/g, '')}</p>}
      </header>

      {note.length > 0 && (
        <aside
          role="note"
          className={`rounded-md border p-4 ${stato ? 'border-destructive bg-destructive/10' : 'border-border bg-card'}`}
        >
          <h2 className="mb-2 font-mono text-xs tracking-[0.12em] uppercase">{titoloNota}</h2>
          <Elenco voci={note} />
          {stato === 'ritirato' && (
            <p className="text-muted-foreground mt-3 text-sm">
              I numeri della conferma ritirata non sono riportati su questa pagina.
            </p>
          )}
        </aside>
      )}

      {fm.avvertenza && (
        <aside role="note" className="border-border bg-card rounded-md border p-4">
          <h2 className="text-muted-foreground mb-2 font-mono text-xs tracking-[0.12em] uppercase">Avvertenza</h2>
          <p className="text-foreground/90 leading-relaxed">{fm.avvertenza}</p>
        </aside>
      )}

      <Sezione titolo="Domanda">
        <Paragrafi testo={sezioni['Domanda'] ?? ''} />
      </Sezione>

      <Sezione titolo="Metodo e rubrica">
        <Paragrafi testo={sezioni['Metodo e rubrica'] ?? ''} />
      </Sezione>

      <Sezione titolo="Esito">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Risultato</TableHead>
              <TableHead>Fonte</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {esito.righe.map((riga, i) => (
              <TableRow key={i}>
                <TableCell className="w-3/5 min-w-56 whitespace-normal">
                  <InLinea testo={riga[0]} />
                </TableCell>
                <TableCell className="text-muted-foreground min-w-48 font-mono text-xs whitespace-normal">
                  {dividiFonti(riga[1] ?? '').map((f) => (
                    <div key={f} className="mb-1 last:mb-0">
                      {f.split(/(?<=[/#])/).map((pezzo, k) => (
                        <span key={k}>
                          {pezzo}
                          <wbr />
                        </span>
                      ))}
                    </div>
                  ))}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        {nonRiportate && <p className="text-muted-foreground text-sm">{nonRiportate}</p>}
        {dati && (
          <div className="flex flex-col gap-2">
            <Grafico dati={dati} />
            {sezioni['Grafico'] && <p className="text-muted-foreground text-xs">{sezioni['Grafico']}</p>}
          </div>
        )}
      </Sezione>

      <Sezione titolo="Cosa NON dice">
        <Elenco voci={leggiElenco(sezioni['Cosa NON dice'] ?? '')} />
      </Sezione>

      <Sezione titolo="Prove">
        <ul className="flex flex-col gap-1 font-mono text-xs">
          {leggiElenco(sezioni['Prove'] ?? '').map((p, i) => (
            <li
              key={i}
              className={`break-all ${p.startsWith('prova non trovata') ? 'text-destructive' : 'text-muted-foreground'}`}
            >
              {p}
            </li>
          ))}
        </ul>
        {fm.fonte_ledger && <p className="text-muted-foreground font-mono text-xs break-all">Ledger: {fm.fonte_ledger}</p>}
      </Sezione>
    </article>
  )
}
