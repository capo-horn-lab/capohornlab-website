// D8: the outcomes at the session's end (the Trader's esiti()), listed here, never drawn as levels; and the tree's text box
// (branches not drawn, or the whole tree when its root is > 2 h after the last bar). A row is keyed by its branch: a number
// that changes updates the row in place; only a new row fades in (a CSS animation on mount, none with reduced motion: no
// Motion here, so the text of the live page does not wait for the chart's libraries).
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export function Esiti({ righe }: { righe: { id: string; testo: string }[] }) {
  if (!righe.length) return null
  return (
    <Card className="gap-2 py-4">
      <CardHeader className="px-4">
        <CardTitle className="text-sm font-medium">Esiti a fine sessione (non livelli da toccare)</CardTitle>
      </CardHeader>
      <CardContent className="px-4">
        <ul className="space-y-1 font-mono text-xs leading-relaxed tabular-nums">
          {righe.map((r) => (
            <li key={r.id} className="animate-in fade-in-35 duration-400 motion-reduce:animate-none">
              {r.testo}
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  )
}

export function AlberoTesto({ righe }: { righe: string[] }) {
  if (!righe.length) return null
  return (
    <div className="border-border text-muted-foreground rounded-md border px-4 py-3 font-mono text-xs leading-relaxed whitespace-pre-wrap tabular-nums">
      {righe.join('\n')}
    </div>
  )
}
