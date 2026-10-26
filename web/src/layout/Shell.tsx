import { Suspense } from 'react'
import { Outlet } from 'react-router'
import { Skeleton } from '@/components/ui/skeleton'
import { Footer } from './Footer'
import { Header } from './Header'

export function Shell() {
  return (
    <div className="flex min-h-screen flex-col">
      <a
        href="#contenuto"
        className="bg-primary text-primary-foreground sr-only z-50 rounded-md px-3 py-2 focus:not-sr-only focus:absolute focus:top-2 focus:left-2"
      >
        Vai al contenuto
      </a>
      <Header />
      <main id="contenuto" className="ch-wrap flex-1 py-10">
        <Suspense fallback={<Skeleton className="h-10 w-64" />}>
          <Outlet />
        </Suspense>
      </main>
      <Footer />
    </div>
  )
}
