import type { ComponentType } from 'react'
import { QueryClientProvider } from '@tanstack/react-query'
import { createBrowserRouter, Link } from 'react-router'
import { RouterProvider } from 'react-router/dom'
import { Footer } from '@/layout/Footer'
import { Shell, ShellInAttesa } from '@/layout/Shell'
import { queryClient } from '@/lib/query'
import { ErroreLive } from '@/live/ErroreLive'

/** A page whose code did not load (an old tab after a deploy, a network blip) or that failed to render: a neutral message in
 * the layout, with the footer's fixed note. The cause is not known here. */
function PaginaNonDisponibile() {
  return (
    <section className="space-y-3" role="alert">
      <h1 className="font-serif text-3xl font-semibold tracking-tight md:text-4xl">Pagina non disponibile</h1>
      <p className="text-muted-foreground text-sm leading-relaxed">
        Questa pagina non si puo' mostrare in questo momento. Ricarica la pagina tra qualche secondo.
      </p>
    </section>
  )
}

/** The layout itself failed: the message and the fixed note without the header (which may be what failed). */
function ErroreLayout() {
  return (
    <div className="flex min-h-screen flex-col">
      <main id="contenuto" className="ch-wrap flex-1 py-10">
        <PaginaNonDisponibile />
      </main>
      <Footer />
    </div>
  )
}

// Each page is its own chunk, loaded by the router (route `lazy`) before the page is shown: no Suspense fallback for the
// page, so React does not hold the page back for its fallback's minimum time (it painted the text ~300 ms later on the home).
// The import never rejects: a rejected route `lazy` leaves the router showing only the HydrateFallback (a blank page), so a
// chunk that does not load becomes the page's own message, inside the layout.
const pagina = (carica: () => Promise<{ default: ComponentType }>, riserva: ComponentType = PaginaNonDisponibile) => async () => {
  try {
    return { Component: (await carica()).default }
  } catch {
    return { Component: riserva }
  }
}

/** A path the app does not know (e.g. /metodo/x, served index.html by the SPA rewrite): a page in the layout, with the fixed note. */
function NonTrovata() {
  return (
    <section className="space-y-3">
      <h1 className="font-serif text-3xl font-semibold tracking-tight md:text-4xl">Pagina non trovata</h1>
      <p className="text-muted-foreground text-sm">
        Questo indirizzo non corrisponde a nessuna pagina. <Link to="/" className="underline underline-offset-4">Torna alla pagina live</Link>.
      </p>
    </section>
  )
}

const router = createBrowserRouter([
  {
    element: <Shell />,
    HydrateFallback: ShellInAttesa,
    errorElement: <ErroreLayout />,
    children: [
      {
        // a render error in any page: its message replaces only the page, inside the layout
        errorElement: <PaginaNonDisponibile />,
        children: [
          { path: '/', lazy: pagina(() => import('@/pagine/Live'), ErroreLive), errorElement: <ErroreLive /> },
          { path: '/ricerche', lazy: pagina(() => import('@/pagine/Ricerche')) },
          { path: '/ricerche/:id', lazy: pagina(() => import('@/pagine/Ricerca')) },
          { path: '/metodo', lazy: pagina(() => import('@/pagine/Metodo')) },
          { path: '/stato', lazy: pagina(() => import('@/pagine/Stato')) },
          { path: '*', element: <NonTrovata /> },
        ],
      },
    ],
  },
])

export default function App() {
  return (
    // no TooltipProvider: no page uses the shadcn Tooltip (the charts have their own), and it put Radix + Floating UI in the entry
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  )
}
