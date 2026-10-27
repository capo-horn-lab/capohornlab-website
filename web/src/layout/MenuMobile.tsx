// The phone menu (Radix Dialog as a sheet): its own chunk, loaded the first time the menu button is pressed.
import type { RefObject } from 'react'
import { Sheet, SheetContent, SheetDescription, SheetTitle } from '@/components/ui/sheet'
import { Nav } from './Nav'

export default function MenuMobile({ aperto, onCambia, bottone }: {
  aperto: boolean
  onCambia: (aperto: boolean) => void
  /** The button that opened it: Radix returns focus only to its own Trigger, and here the trigger is a plain button. */
  bottone: RefObject<HTMLButtonElement | null>
}) {
  return (
    <Sheet open={aperto} onOpenChange={onCambia}>
      <SheetContent
        id="menu-telefono"
        side="right"
        className="w-64"
        onCloseAutoFocus={(e) => {
          e.preventDefault()
          bottone.current?.focus()
        }}
      >
        <SheetTitle className="px-4 pt-4 font-serif">Capo Horn Lab</SheetTitle>
        <SheetDescription className="sr-only">Navigazione del sito</SheetDescription>
        <Nav className="flex-col px-2" onNavigate={() => onCambia(false)} />
      </SheetContent>
    </Sheet>
  )
}
