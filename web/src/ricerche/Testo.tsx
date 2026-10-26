import type { ComponentProps } from 'react'
import ReactMarkdown from 'react-markdown'
import { Badge } from '@/components/ui/badge'
import { ETICHETTE, type Verdetto } from './modello'

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

export function VerdettoBadge({ verdetto }: { verdetto: Verdetto }) {
  const e = ETICHETTE[verdetto]
  return (
    <Badge variant={e.variante} title={e.aiuto}>
      {e.testo}
    </Badge>
  )
}
