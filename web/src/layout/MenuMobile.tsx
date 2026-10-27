// The phone menu (Radix Dialog as a sheet): its own chunk, loaded the first time the menu button is pressed.
import { Sheet, SheetContent, SheetDescription, SheetTitle } from '@/components/ui/sheet'
import { Nav } from './Nav'

export default function MenuMobile({ aperto, onCambia }: { aperto: boolean; onCambia: (aperto: boolean) => void }) {
  return (
    <Sheet open={aperto} onOpenChange={onCambia}>
      <SheetContent side="right" className="w-64">
        <SheetTitle className="px-4 pt-4 font-serif">Capo Horn Lab</SheetTitle>
        <SheetDescription className="sr-only">Navigazione del sito</SheetDescription>
        <Nav className="flex-col px-2" onNavigate={() => onCambia(false)} />
      </SheetContent>
    </Sheet>
  )
}
