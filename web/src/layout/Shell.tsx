import { Suspense } from 'react'
import { Outlet, useLocation, useNavigation } from 'react-router'
import { Skeleton } from '@/components/ui/skeleton'
import { Footer } from './Footer'
import { Header } from './Header'

const TRANSIZIONE = 'animate-in fade-in slide-in-from-bottom-1 duration-200 motion-reduce:animate-none'

export function Shell() {
  // the first page of a visit (location key "default") appears without the transition: it would only delay its first paint
  const { pathname, key } = useLocation()
  // a client navigation waits for the next page's chunk (route `lazy`) with the old page on screen: say it is loading
  const inCorso = useNavigation().state !== 'idle'
  return (
    <div className="flex min-h-screen flex-col">
      {inCorso ? (
        <div data-navigazione aria-hidden="true" className="bg-primary fixed inset-x-0 top-0 z-50 h-0.5 animate-pulse motion-reduce:animate-none" />
      ) : null}
      <a
        href="#contenuto"
        className="bg-primary text-primary-foreground sr-only z-50 rounded-md px-3 py-2 focus:not-sr-only focus:absolute focus:top-2 focus:left-2"
      >
        Vai al contenuto
      </a>
      <Header />
      <main id="contenuto" className="ch-wrap flex-1 py-10" aria-busy={inCorso}>
        {/* while a page's chunk loads the footer stays below the fold: otherwise the page pushes it down (layout shift) */}
        <Suspense fallback={<div className="min-h-svh"><Skeleton className="h-10 w-64" /></div>}>
          {/* page transition (design 4.4): each page reached by navigating fades and rises in over 200 ms, keyed on the path so
              it runs on every page change; none with reduced motion. CSS only (tw-animate-css): Motion stays out of the entry. */}
          <div key={pathname} data-transizione className={key === 'default' ? undefined : TRANSIZIONE}>
            <Outlet />
          </div>
        </Suspense>
      </main>
      <Footer />
    </div>
  )
}

/** Before the first page's code arrives (the router's HydrateFallback): the same layout with a skeleton, the footer below the
 * fold, the menu button disabled (this header is replaced by the page's own: a press here would be lost). */
export function ShellInAttesa() {
  return (
    <div className="flex min-h-screen flex-col">
      <Header inAttesa />
      <main id="contenuto" className="ch-wrap flex-1 py-10" aria-busy="true">
        <div className="min-h-svh">
          <Skeleton className="h-10 w-64" />
        </div>
      </main>
      <Footer />
    </div>
  )
}
