import type { ComponentProps } from 'react'
import ReactMarkdown from 'react-markdown'

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
