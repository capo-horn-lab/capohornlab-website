// I segni del verdetto e dell'audit, a parte dal Markdown (Testo.tsx): l'indice /ricerche li usa senza caricare react-markdown.
import { Badge } from '@/components/ui/badge'
import { AIUTO_AUDIT, parolaNuda, paroleVerdetto, SENZA_VERDETTO, varianteParola, type Audit, type Verdetto } from './modello'

/** Una voce del registro per badge (con l'ID, se la scheda ha piu' studi); oltre `max` voci il resto va in "+N" (tutte nel title). */
export function VerdettoBadge({ verdetto, max = 3 }: { verdetto: Verdetto; max?: number }) {
  const parole = paroleVerdetto(verdetto)
  if (parole.length === 0) {
    return (
      <Badge variant="outline" className="text-muted-foreground">
        {SENZA_VERDETTO}
      </Badge>
    )
  }
  return (
    <span className="flex flex-wrap gap-1" title={`Verdetto nel registro: ${parole.join(', ')}`}>
      {parole.slice(0, max).map((p) => (
        <Badge key={p} variant={varianteParola(parolaNuda(p))}>
          {p}
        </Badge>
      ))}
      {parole.length > max && <Badge variant="outline">+{parole.length - max}</Badge>}
    </span>
  )
}

/** Secondo segno, a parte dal verdetto: `ritirato` (solo ID dichiarati ritirati) oppure la nota neutra dell'audit. */
export function AuditBadge({ audit }: { audit: Audit['stato'] }) {
  return audit === 'ritirato' ? (
    <Badge variant="destructive" title={AIUTO_AUDIT[audit]}>
      audit: ritirato
    </Badge>
  ) : (
    <Badge variant="outline" title={AIUTO_AUDIT[audit]}>
      nota dell'audit
    </Badge>
  )
}
