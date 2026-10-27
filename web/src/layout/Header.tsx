import { lazy, Suspense, useState } from 'react'
import { Link } from 'react-router'
import { Menu } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Nav } from './Nav'

// the phone menu's Radix Dialog is not in the entry: it loads on the first press of the button and then stays mounted
const MenuMobile = lazy(() => import('./MenuMobile'))

export function Header() {
  const [aperto, setAperto] = useState(false)
  const [usato, setUsato] = useState(false)
  return (
    <header className="border-border bg-background/90 sticky top-0 z-40 border-b backdrop-blur">
      <div className="ch-wrap flex h-16 items-center justify-between">
        <Link to="/" className="font-serif text-xl font-semibold tracking-tight">
          Capo Horn Lab
        </Link>
        <Nav className="hidden md:flex" />
        <Button
          variant="ghost"
          size="icon"
          className="md:hidden"
          aria-label="Apri il menu"
          aria-haspopup="dialog"
          aria-expanded={aperto}
          onClick={() => {
            setUsato(true)
            setAperto(true)
          }}
        >
          <Menu />
        </Button>
        {usato ? (
          <Suspense fallback={null}>
            <MenuMobile aperto={aperto} onCambia={setAperto} />
          </Suspense>
        ) : null}
      </div>
    </header>
  )
}
