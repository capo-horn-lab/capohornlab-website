import { lazy, Suspense, useRef, useState } from 'react'
import { Link } from 'react-router'
import { Menu } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Nav } from './Nav'

// the phone menu's Radix Dialog is not in the entry: it loads on the first press of the button and then stays mounted; if its
// chunk does not load, the press does nothing (the page and the header stay, the desktop nav and the page links still work)
const MenuMobile = lazy(() => import('./MenuMobile').catch(() => ({ default: () => <></> })))

/** `inAttesa`: the header of the first load's placeholder layout (the router's HydrateFallback). Its menu button is disabled,
 * because that header is replaced by the page's own as soon as the page's code arrives, and a press would be lost. */
export function Header({ inAttesa = false }: { inAttesa?: boolean }) {
  const [aperto, setAperto] = useState(false)
  const [usato, setUsato] = useState(false)
  const bottone = useRef<HTMLButtonElement>(null)
  return (
    <header className="border-border bg-background/90 sticky top-0 z-40 border-b backdrop-blur">
      <div className="ch-wrap flex h-16 items-center justify-between">
        <Link to="/" className="font-serif text-xl font-semibold tracking-tight">
          Capo Horn Lab
        </Link>
        <Nav className="hidden md:flex" />
        <Button
          ref={bottone}
          variant="ghost"
          size="icon"
          className="md:hidden"
          aria-label="Apri il menu"
          aria-haspopup="dialog"
          aria-expanded={aperto}
          aria-controls={usato ? 'menu-telefono' : undefined}
          disabled={inAttesa}
          onClick={() => {
            setUsato(true)
            setAperto(true)
          }}
        >
          <Menu />
        </Button>
        {usato ? (
          <Suspense fallback={null}>
            <MenuMobile aperto={aperto} onCambia={setAperto} bottone={bottone} />
          </Suspense>
        ) : null}
      </div>
    </header>
  )
}
