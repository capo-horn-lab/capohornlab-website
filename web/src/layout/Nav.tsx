import { NavLink } from 'react-router'
import { cn } from '@/lib/utils'

const VOCI = [
  { to: '/', label: 'Live', end: true },
  { to: '/memoria', label: 'Memoria', end: false },
  { to: '/ricerche', label: 'Ricerche', end: false },
  { to: '/metodo', label: 'Metodo', end: false },
  { to: '/stato', label: 'Stato', end: false },
]

export function Nav({
  className,
  onNavigate,
}: {
  className?: string
  onNavigate?: () => void
}) {
  return (
    <nav aria-label="Principale" className={cn('flex gap-1', className)}>
      {VOCI.map((v) => (
        <NavLink
          key={v.to}
          to={v.to}
          end={v.end}
          onClick={onNavigate}
          className={({ isActive }) =>
            cn(
              'rounded-md px-3 py-2 font-mono text-xs tracking-[0.12em] uppercase transition-colors',
              isActive
                ? 'text-foreground bg-accent'
                : 'text-muted-foreground hover:text-foreground',
            )
          }
        >
          {v.label}
        </NavLink>
      ))}
    </nav>
  )
}
