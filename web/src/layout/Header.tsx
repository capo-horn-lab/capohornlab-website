import { useState } from 'react'
import { Link } from 'react-router'
import { Menu } from 'lucide-react'
import { Button } from '@/components/ui/button'
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetTitle,
  SheetTrigger,
} from '@/components/ui/sheet'
import { Nav } from './Nav'

export function Header() {
  const [aperto, setAperto] = useState(false)
  return (
    <header className="border-border bg-background/90 sticky top-0 z-40 border-b backdrop-blur">
      <div className="ch-wrap flex h-16 items-center justify-between">
        <Link to="/" className="font-serif text-xl font-semibold tracking-tight">
          Capo Horn Lab
        </Link>
        <Nav className="hidden md:flex" />
        <Sheet open={aperto} onOpenChange={setAperto}>
          <SheetTrigger asChild>
            <Button variant="ghost" size="icon" className="md:hidden" aria-label="Apri il menu">
              <Menu />
            </Button>
          </SheetTrigger>
          <SheetContent side="right" className="w-64">
            <SheetTitle className="px-4 pt-4 font-serif">Capo Horn Lab</SheetTitle>
            <SheetDescription className="sr-only">Navigazione del sito</SheetDescription>
            <Nav className="flex-col px-2" onNavigate={() => setAperto(false)} />
          </SheetContent>
        </Sheet>
      </div>
    </header>
  )
}
