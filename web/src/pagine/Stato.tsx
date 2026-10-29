import { useQuery } from '@tanstack/react-query'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { carica, OPZIONI_COMUNI } from '@/lib/api'
import { etaCorrente, useAdesso } from '@/live/AvvisoFreschezza'
import { SOGLIA_CANALE_S, SOGLIA_SPENTO_CANALE_S, type StatoMotore, statoMotore } from '@/ricerche/stato'

const COLORE: Record<StatoMotore, string> = { acceso: 'var(--ch-success)', 'in ritardo': 'var(--ch-warm)', spento: 'var(--ch-danger)' }

// Fetch propria e minima: la pagina Stato non dipende dai moduli della pagina Live.
const CANALI = [
  { chiave: 'scenari', titolo: 'Scenari' },
  { chiave: 'frequenze', titolo: 'Frequenze' },
  { chiave: 'memoria', titolo: 'Memoria' },
] as const

type Chiave = (typeof CANALI)[number]['chiave']

interface Busta {
  ricevuto: string | null
  eta_s: number | null
  dati: {
    generato?: string
    principale?: { strumento?: string; contratto?: string | null }
    stato?: { strumento?: string | null }
    verdetti?: { generato?: string | null }
  } | null
}

/** Lo strumento del canale: il principale per scenari e frequenze, quello della memoria per la memoria. */
function strumentoDi(chiave: Chiave, dati: Busta['dati']): string {
  if (chiave === 'memoria') return dati?.stato?.strumento || '-'
  const p = dati?.principale
  return p?.strumento ? `${p.strumento}${p.contratto ? ` ${p.contratto}` : ''}` : '-'
}

// Same conditional poll as the live channels (If-None-Match / 304), without their payload validation.
const comeArriva = (x: unknown) => x as Busta

function Canale({ chiave, titolo }: { chiave: Chiave; titolo: string }) {
  const q = useQuery({
    queryKey: ['stato', chiave],
    queryFn: ({ signal, client, queryKey }) => carica(client, queryKey, chiave, comeArriva, signal),
    ...OPZIONI_COMUNI,
  })
  const { data, error, isPending } = q
  const adesso = useAdesso()
  // the age keeps growing between the polls, and after a 304 the envelope's own eta_s is the old one
  const eta = data ? etaCorrente({ data, isError: q.isError, dataUpdatedAt: q.dataUpdatedAt, errorUpdatedAt: q.errorUpdatedAt }, adesso) : null
  const stato = statoMotore(eta ?? data?.eta_s ?? null, SOGLIA_CANALE_S[chiave], SOGLIA_SPENTO_CANALE_S[chiave])
  return (
    <section aria-labelledby={`c-${chiave}`} className="border-border bg-card flex flex-col gap-3 rounded-md border p-5">
      <div className="flex items-center justify-between gap-3">
        <h2 id={`c-${chiave}`} className="font-serif text-2xl font-semibold tracking-tight">
          {titolo}
        </h2>
        {!isPending && !error && (
          // semaforo con i colori dei token: acceso = verificato, in ritardo = caldo, spento = errore (il rosso del brand e' il primario)
          <Badge variant="outline" style={{ color: COLORE[stato], borderColor: COLORE[stato] }}>
            motore {stato}
          </Badge>
        )}
      </div>
      {isPending && <Skeleton className="h-20 w-full" />}
      {error && <p className="text-destructive text-sm">Servizio non raggiungibile ({String(error.message)}).</p>}
      {data && (
        <dl className="grid grid-cols-[auto_1fr] gap-x-6 gap-y-2 text-sm">
          <dt className="text-muted-foreground">Ricevuto</dt>
          <dd className="font-mono">{data.ricevuto ?? 'mai'}</dd>
          <dt className="text-muted-foreground">Eta'</dt>
          {/* after a failed refresh the server's age of the last answer would stay frozen next to the error: not known */}
          <dd className="font-mono">{error ? 'n/d' : (eta ?? data.eta_s) === null ? '-' : `${Math.round((eta ?? data.eta_s)!)} s`}</dd>
          <dt className="text-muted-foreground">Generato</dt>
          <dd className="font-mono">{data.dati?.generato ?? '-'}</dd>
          <dt className="text-muted-foreground">{chiave === 'memoria' ? 'Strumento' : 'Principale'}</dt>
          <dd className="font-mono">{strumentoDi(chiave, data.dati)}</dd>
          {chiave === 'memoria' && (
            <>
              <dt className="text-muted-foreground">Verifica del</dt>
              <dd className="font-mono">{data.dati?.verdetti?.generato ?? '-'}</dd>
            </>
          )}
        </dl>
      )}
    </section>
  )
}

export default function Stato() {
  return (
    <section className="flex max-w-3xl flex-col gap-6">
      <header className="flex flex-col gap-3">
        <h1 className="font-serif text-4xl font-semibold tracking-tight">Stato</h1>
        <p className="text-muted-foreground">
          Il motore invia gli scenari ogni 15 s, le frequenze ogni 60 s e la memoria del mercato almeno ogni 120 s. Gli scenari sono «acceso» fino a{' '}
          {SOGLIA_CANALE_S.scenari} s dall'ultimo invio e «in ritardo» fino a {SOGLIA_SPENTO_CANALE_S.scenari} s; le frequenze sono «acceso»
          fino a {SOGLIA_CANALE_S.frequenze} s e «in ritardo» fino a {SOGLIA_SPENTO_CANALE_S.frequenze} s; la memoria e' «acceso» fino a{' '}
          {SOGLIA_CANALE_S.memoria} s e «in ritardo» fino a {SOGLIA_SPENTO_CANALE_S.memoria} s. Oltre, il motore e' «spento». La pagina si
          aggiorna da sola.
        </p>
      </header>
      {CANALI.map((c) => (
        <Canale key={c.chiave} {...c} />
      ))}
    </section>
  )
}
