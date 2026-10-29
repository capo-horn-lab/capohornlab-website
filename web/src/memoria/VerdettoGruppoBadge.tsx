// Il verdetto di un gruppo come badge neutro: tre toni dei token del tema (nessun verde/rosso, nessun colore direzionale),
// distinguibili anche dal solo testo. Un verdetto che il sito non conosce si mostra com'e' nel tono piu' sobrio.
import { Badge } from '@/components/ui/badge'

const TONI: Record<string, { variant: 'outline' | 'secondary'; className?: string }> = {
  DESCRITTIVO: { variant: 'outline', className: 'text-muted-foreground' },
  'NON CONFERMATO': { variant: 'secondary' },
  CONFERMATO: { variant: 'outline', className: 'border-foreground bg-accent text-foreground font-semibold' },
}

export function VerdettoGruppoBadge({ verdetto }: { verdetto: string }) {
  const tono = TONI[verdetto] ?? TONI.DESCRITTIVO
  return (
    <Badge variant={tono.variant} className={tono.className}>
      {verdetto}
    </Badge>
  )
}
