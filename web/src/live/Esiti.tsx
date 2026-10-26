// D8: the branches without minutes are outcomes at the session's end, listed here, never drawn as levels; and the tree's text
// box (branches not drawn, or the whole tree when its root is > 2 h after the last bar). Rows fade in when their text changes.
import { motion, useReducedMotion } from 'motion/react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export function Esiti({ righe }: { righe: { id: string; testo: string }[] }) {
  const ridotto = useReducedMotion()
  if (!righe.length) return null
  return (
    <Card className="gap-2 py-4">
      <CardHeader className="px-4">
        <CardTitle className="text-sm font-medium">Esiti a fine sessione (non livelli da toccare)</CardTitle>
      </CardHeader>
      <CardContent className="px-4">
        <ul className="space-y-1 font-mono text-xs leading-relaxed tabular-nums">
          {righe.map((r) => (
            <motion.li key={`${r.id}:${r.testo}`} initial={ridotto ? false : { opacity: 0.35 }} animate={{ opacity: 1 }} transition={{ duration: 0.4 }}>
              {r.testo}
            </motion.li>
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
