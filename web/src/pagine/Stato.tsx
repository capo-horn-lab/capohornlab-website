import { useQuery } from '@tanstack/react-query'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { API_BASE } from '@/lib/config'
import { SOGLIA_CANALE_S, SOGLIA_SPENTO_S, type StatoMotore, statoMotore } from '@/ricerche/stato'

const COLORE: Record<StatoMotore, string> = { acceso: 'var(--ch-success)', 'in ritardo': 'var(--ch-warm)', spento: 'var(--ch-danger)' }

// Fetch propria e minima: la pagina Stato non dipende dai moduli della pagina Live.
const CANALI = [
  { chiave: 'scenari', titolo: 'Scenari' },
  { chiave: 'frequenze', titolo: 'Frequenze' },
] as const

type Chiave = (typeof CANALI)[number]['chiave']

interface Busta {
  ricevuto: string | null
  eta_s: number | null
  dati: { generato?: string; principale?: { strumento?: string; contratto?: string | null } } | null
}

async function leggi(chiave: Chiave): Promise<Busta> {
  const r = await fetch(`${API_BASE}/live/${chiave}`, { cache: 'no-store' })
  if (!r.ok) throw new Error(`HTTP ${r.status}`)
  return (await r.json()) as Busta
}

function Canale({ chiave, titolo }: { chiave: Chiave; titolo: string }) {
  const { data, error, isPending } = useQuery({
    queryKey: ['stato', chiave],
    queryFn: () => leggi(chiave),
    refetchInterval: 15_000,
  })
  const stato = statoMotore(data?.eta_s ?? null, SOGLIA_CANALE_S[chiave])
  const p = data?.dati?.principale
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
          <dd className="font-mono">{data.eta_s === null ? '-' : `${data.eta_s} s`}</dd>
          <dt className="text-muted-foreground">Generato</dt>
          <dd className="font-mono">{data.dati?.generato ?? '-'}</dd>
          <dt className="text-muted-foreground">Principale</dt>
          <dd className="font-mono">{p?.strumento ? `${p.strumento}${p.contratto ? ` ${p.contratto}` : ''}` : '-'}</dd>
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
          Il motore invia gli scenari ogni 15 s e le frequenze ogni 60 s. Gli scenari sono «acceso» fino a{' '}
          {SOGLIA_CANALE_S.scenari} s dall'ultimo invio e «in ritardo» fino a {SOGLIA_SPENTO_S} s; le frequenze sono «acceso»
          fino a {SOGLIA_CANALE_S.frequenze} s. Oltre {SOGLIA_SPENTO_S} s il motore e' «spento». La pagina si aggiorna da sola.
        </p>
      </header>
      {CANALI.map((c) => (
        <Canale key={c.chiave} {...c} />
      ))}
    </section>
  )
}
