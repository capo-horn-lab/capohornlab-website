import ReactMarkdown from 'react-markdown'
import metodo from '@/content/metodo.md?raw'

export default function Metodo() {
  return (
    <article className="flex max-w-3xl flex-col gap-4">
      <ReactMarkdown
        components={{
          h1: ({ children }) => (
            <h1 className="font-serif text-4xl font-semibold tracking-tight">{children}</h1>
          ),
          h2: ({ children }) => (
            <h2 className="mt-6 font-serif text-2xl font-semibold tracking-tight">{children}</h2>
          ),
          p: ({ children }) => <p className="text-foreground/90 leading-relaxed">{children}</p>,
          ul: ({ children }) => (
            <ul className="text-foreground/90 flex list-disc flex-col gap-1.5 pl-5 leading-relaxed">{children}</ul>
          ),
          code: ({ children }) => (
            <code className="bg-muted rounded px-1 py-0.5 font-mono text-[0.85em] break-words">{children}</code>
          ),
        }}
      >
        {metodo}
      </ReactMarkdown>
    </article>
  )
}
