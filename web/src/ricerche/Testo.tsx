import type { ComponentProps } from 'react'
import ReactMarkdown from 'react-markdown'
import { Badge } from '@/components/ui/badge'
import { AIUTO_AUDIT, paroleVerdetto, SENZA_VERDETTO, varianteParola, type Audit, type Verdetto } from './modello'

/** Markdown in riga (grassetto, codice) dentro una cella o una voce di elenco. */
export function InLinea({ testo }: { testo: string }) {
  return (
    <ReactMarkdown
      components={{
        p: ({ children }) => <>{children}</>,
        code: ({ children }) => <code className="font-mono text-[0.85em]">{children}</code>,
      }}
    >
      {testo}
    </ReactMarkdown>
  )
}

/** Paragrafi di una sezione. */
export function Paragrafi({ testo }: { testo: string }) {
  return (
    <ReactMarkdown
      components={{
        p: (p: ComponentProps<'p'>) => <p className="text-foreground/90 leading-relaxed" {...p} />,
        code: ({ children }) => <code className="font-mono text-[0.85em]">{children}</code>,
      }}
    >
      {testo}
    </ReactMarkdown>
  )
}

/** Una parola del registro per badge; oltre `max` parole il resto va in "+N" (tutte nel title). */
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
    <span className="flex flex-wrap gap-1" title={`Parole del registro: ${parole.join(', ')}`}>
      {parole.slice(0, max).map((p) => (
        <Badge key={p} variant={varianteParola(p)}>
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
