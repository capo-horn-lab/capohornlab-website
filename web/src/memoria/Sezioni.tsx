// Le sezioni 2-4 della pagina /memoria. I numeri sono quelli del payload, solo formattati (D8: intero/num); le percentuali solo da
// quozienti gia' nel payload; i testi delle definizioni vengono da contenuto.ts, mai scritti a mano qui.
import type { ReactNode } from 'react'
import { Skeleton } from '@/components/ui/skeleton'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { intero, num } from '@/lib/fmt'
import { type Memoria, RispostaNonValida } from '@/lib/tipi'
import { idSezione } from '@/ricerche/modello'
import { DATA_INIZIO_DATABASE, FAMIGLIE, QUANDO, type Citazione } from './contenuto'
import { dataItaliana, dataOraRoma } from './formato'
import { VerdettoGruppoBadge } from './VerdettoGruppoBadge'

const H2 = 'font-serif text-2xl font-semibold tracking-tight'
const H3 = 'font-serif text-xl font-semibold tracking-tight'

function Sezione({ titolo, livello = 2, children }: { titolo: string; livello?: 2 | 3; children: ReactNode }) {
  const id = `s-${idSezione(titolo)}`
  const Titolo = livello === 2 ? 'h2' : 'h3'
  return (
    <section aria-labelledby={id} className="flex flex-col gap-3">
      <Titolo id={id} className={livello === 2 ? H2 : H3}>
        {titolo}
      </Titolo>
      {children}
    </section>
  )
}

function Fonte({ fonte }: { fonte: string }) {
  return (
    <p className="text-muted-foreground text-xs">
      Fonte: <span className="font-mono break-all">{fonte}</span>
    </p>
  )
}

function Citato({ c }: { c: Citazione }) {
  return (
    <blockquote className="border-border flex flex-col gap-1.5 border-l-2 pl-4">
      {c.etichetta && <p className="text-muted-foreground text-xs font-medium">{c.etichetta}</p>}
      <p className="text-foreground/90 text-sm leading-relaxed">{c.testo}</p>
      <Fonte fonte={c.fonte} />
    </blockquote>
  )
}

export function Riconosce() {
  return (
    <Sezione titolo="Che cosa riconosce">
      <div className="flex flex-col gap-5">
        {FAMIGLIE.map((f) => (
          <article key={f.id} className="flex flex-col gap-2">
            <h3 className={H3}>{f.titolo}</h3>
            {f.definizioni.map((d) => (
              <Citato key={d.fonte} c={d} />
            ))}
            {f.nota && <p className="text-muted-foreground text-sm">{f.nota}</p>}
          </article>
        ))}
      </div>
    </Sezione>
  )
}

const Voce = ({ etichetta, valore }: { etichetta: string; valore: string }) => (
  <>
    <dt className="text-muted-foreground">{etichetta}</dt>
    <dd className="font-mono">{valore}</dd>
  </>
)

const Elenco = ({ children }: { children: ReactNode }) => (
  <dl className="grid grid-cols-[auto_1fr] gap-x-6 gap-y-1.5 text-sm">{children}</dl>
)

/** Un quoziente gia' nel payload (0..1) in percentuale, solo formattato; assente -> "-". */
const percentuale = (quota: number | null) => (quota == null ? '-' : `${num(quota * 100, 1)}%`)

/** "famiglia/tipo" -> [famiglia, tipo] (la chiave del payload, spezzata alla prima barra). */
const chiave2 = (k: string): [string, string] => {
  const i = k.indexOf('/')
  return i < 0 ? [k, '-'] : [k.slice(0, i), k.slice(i + 1)]
}

function TabellaConteggi({ nome, conteggi }: { nome: string; conteggi: Record<string, number> }) {
  return (
    <Table aria-label={nome}>
      <TableHeader>
        <TableRow>
          <TableHead>Famiglia</TableHead>
          <TableHead>Tipo</TableHead>
          <TableHead className="text-right">Eventi</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {Object.entries(conteggi).map(([k, n]) => {
          const [famiglia, tipo] = chiave2(k)
          return (
            <TableRow key={k}>
              <TableCell className="font-mono">{famiglia}</TableCell>
              <TableCell className="font-mono">{tipo}</TableCell>
              <TableCell className="text-right font-mono">{intero(n)}</TableCell>
            </TableRow>
          )
        })}
      </TableBody>
    </Table>
  )
}

/** Il messaggio dell'errore di canale, una volta sola in testa alla pagina (le sezioni dicono solo che mancano i dati). */
export function ErroreCanale({ errore }: { errore: Error }) {
  return (
    <p role="alert" className="text-muted-foreground text-sm">
      {errore instanceof RispostaNonValida ? 'Dati non validi dal motore' : 'Servizio non raggiungibile'} ({errore.message}).
    </p>
  )
}

/** Il contenuto di una sezione che dipende dal canale: scheletro in attesa, messaggio senza dati, altrimenti i dati. */
function ConDati({ d, errore, attesa, children }: { d: Memoria | null; errore: Error | null; attesa: boolean; children: (d: Memoria) => ReactNode }) {
  if (d) return <>{children(d)}</>
  if (attesa) return <Skeleton className="h-40 w-full" />
  return (
    <p className="text-muted-foreground text-sm">
      {errore ? 'Dati non disponibili.' : 'Nessun dato disponibile: il motore non ha ancora pubblicato.'}
    </p>
  )
}

interface Canale {
  d: Memoria | null
  errore: Error | null
  attesa: boolean
}

export function Eventi({ d, errore, attesa }: Canale) {
  return (
    <Sezione titolo="Eventi nella memoria">
      <ConDati d={d} errore={errore} attesa={attesa}>
        {({ stato, oggi }) => (
          <>
            <Elenco>
              <Voce etichetta="Strumento" valore={stato.strumento ?? '-'} />
              <Voce etichetta="Ultimo giro (ora di Roma)" valore={dataOraRoma(stato.ultimo_giro)} />
              <Voce etichetta="Eventi nuovi nell'ultimo giro" valore={intero(stato.eventi_nuovi)} />
            </Elenco>
            <h3 className={H3}>Totale nel database dal {DATA_INIZIO_DATABASE}</h3>
            <TabellaConteggi nome={`Totale nel database dal ${DATA_INIZIO_DATABASE}`} conteggi={stato.conteggi} />
            <h3 className={H3}>Oggi ({dataItaliana(oggi.data)})</h3>
            <p className="text-muted-foreground text-sm">
              Conteggio (COUNT) dal database della memoria da mezzanotte di Roma, calcolato dal pubblicatore: il sito non calcola nulla.
            </p>
            <TabellaConteggi nome={`Oggi (${dataItaliana(oggi.data)})`} conteggi={oggi.conteggi} />
            <Elenco>
              <Voce etichetta="Totale oggi" valore={intero(oggi.totale)} />
            </Elenco>
            <h3 className={H3}>Diagnostica</h3>
            <Elenco>
              <Voce etichetta="Libro caldo" valore={percentuale(stato.diagnostica.quota_libro_caldo)} />
              <Voce etichetta="Scambi con verso" valore={intero(stato.diagnostica.scambi_verso)} />
              <Voce etichetta="Scambi ambigui" valore={intero(stato.diagnostica.scambi_ambigui)} />
              <Voce etichetta="Quota scambi ambigui" valore={percentuale(stato.diagnostica.quota_ambigui)} />
              <Voce etichetta="Record L2" valore={intero(stato.diagnostica.l2_record)} />
              <Voce etichetta="Salti a freddo" valore={intero(stato.diagnostica.salti_a_freddo)} />
            </Elenco>
          </>
        )}
      </ConDati>
    </Sezione>
  )
}

const campo = (x: unknown) => (x == null ? '-' : String(x))

export function Verifica({ d, errore, attesa }: Canale) {
  return (
    <Sezione titolo="Verifica statistica">
      <ConDati d={d} errore={errore} attesa={attesa}>
        {({ verdetti: v }) => (
          <>
            <Elenco>
              <Voce etichetta="Divisione" valore={campo(v.divisione)} />
              <Voce etichetta="Verifica del" valore={dataOraRoma(v.generato)} />
              <Voce etichetta="Test (Benjamini-Hochberg)" valore={campo(v.n_test_bh)} />
              <Voce etichetta="Controlli" valore={campo(v.rubrica?.controlli)} />
              <Voce etichetta="Placebo" valore={campo(v.rubrica?.placebo)} />
              <Voce etichetta="Bootstrap" valore={campo(v.rubrica?.bootstrap)} />
              <Voce etichetta="q (BH)" valore={campo(v.rubrica?.q_bh)} />
            </Elenco>
            <Table aria-label="Verdetti per gruppo">
              <TableHeader>
                <TableRow>
                  <TableHead>Famiglia</TableHead>
                  <TableHead>Tipo</TableHead>
                  <TableHead>Lato</TableHead>
                  <TableHead>Verdetto</TableHead>
                  <TableHead className="text-right">n</TableHead>
                  <TableHead className="text-right">Orizzonte (s)</TableHead>
                  <TableHead>Metrica</TableHead>
                  <TableHead className="text-right">p minimo</TableHead>
                </TableRow>
              </TableHeader>
              {Object.entries(v.verdetti).map(([k, g]) => {
                const [famiglia, tipo = '-', lato = '-'] = k.split('/')
                return (
                  <TableBody key={k}>
                    <TableRow className="border-b-0">
                      <TableCell className="font-mono">{famiglia}</TableCell>
                      <TableCell className="font-mono">{tipo}</TableCell>
                      <TableCell className="font-mono">{lato}</TableCell>
                      <TableCell>
                        <VerdettoGruppoBadge verdetto={g.verdetto} />
                      </TableCell>
                      <TableCell className="text-right font-mono">{campo(g.n)}</TableCell>
                      <TableCell className="text-right font-mono">{campo(g.orizzonte)}</TableCell>
                      <TableCell className="font-mono">{campo(g.metrica)}</TableCell>
                      <TableCell className="text-right font-mono">{campo(g.p_minimo)}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell colSpan={8} className="pt-0 whitespace-normal">
                        <p data-frase={k} className="text-muted-foreground max-w-[calc(100vw-2.5rem)] font-mono text-xs leading-relaxed md:max-w-3xl">
                          {g.frase}
                        </p>
                      </TableCell>
                    </TableRow>
                  </TableBody>
                )
              })}
            </Table>
          </>
        )}
      </ConDati>
      <Sezione titolo="Quando saranno possibili verdetti reali" livello={3}>
        <Citato c={QUANDO} />
      </Sezione>
    </Sezione>
  )
}
