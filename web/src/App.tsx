import type { ComponentType } from 'react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { createBrowserRouter, Link } from 'react-router'
import { RouterProvider } from 'react-router/dom'
import { Shell, ShellInAttesa } from '@/layout/Shell'
import { ErroreLive } from '@/live/ErroreLive'

// Each page is its own chunk, loaded by the router (route `lazy`) before the page is shown: no Suspense fallback for the
// page, so React does not hold the page back for its fallback's minimum time (it painted the text ~300 ms later on the home).
const pagina = (carica: () => Promise<{ default: ComponentType }>) => async () => ({ Component: (await carica()).default })

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
    children: [
      { path: '/', lazy: pagina(() => import('@/pagine/Live')), errorElement: <ErroreLive /> },
      { path: '/ricerche', lazy: pagina(() => import('@/pagine/Ricerche')) },
      { path: '/ricerche/:id', lazy: pagina(() => import('@/pagine/Ricerca')) },
      { path: '/metodo', lazy: pagina(() => import('@/pagine/Metodo')) },
      { path: '/stato', lazy: pagina(() => import('@/pagine/Stato')) },
      { path: '*', element: <NonTrovata /> },
    ],
  },
])

export const queryClient = new QueryClient()

export default function App() {
  return (
    // no TooltipProvider: no page uses the shadcn Tooltip (the charts have their own), and it put Radix + Floating UI in the entry
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  )
}
