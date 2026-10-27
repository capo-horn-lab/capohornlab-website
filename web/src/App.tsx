import { lazy } from 'react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { createBrowserRouter } from 'react-router'
import { RouterProvider } from 'react-router/dom'
import { TooltipProvider } from '@/components/ui/tooltip'
import { Shell } from '@/layout/Shell'
import { ErroreLive } from '@/live/ErroreLive'

const Live = lazy(() => import('@/pagine/Live'))
const Ricerche = lazy(() => import('@/pagine/Ricerche'))
const Ricerca = lazy(() => import('@/pagine/Ricerca'))
const Metodo = lazy(() => import('@/pagine/Metodo'))
const Stato = lazy(() => import('@/pagine/Stato'))

const router = createBrowserRouter([
  {
    element: <Shell />,
    children: [
      { path: '/', element: <Live />, errorElement: <ErroreLive /> },
      { path: '/ricerche', element: <Ricerche /> },
      { path: '/ricerche/:id', element: <Ricerca /> },
      { path: '/metodo', element: <Metodo /> },
      { path: '/stato', element: <Stato /> },
    ],
  },
])

const queryClient = new QueryClient()

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <RouterProvider router={router} />
      </TooltipProvider>
    </QueryClientProvider>
  )
}
