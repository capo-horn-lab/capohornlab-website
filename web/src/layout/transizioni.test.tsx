import { act, fireEvent, render, screen } from '@testing-library/react'
import { createMemoryRouter, Link } from 'react-router'
import { RouterProvider } from 'react-router/dom'
import { describe, expect, it } from 'vitest'
import { Shell, ShellInAttesa } from './Shell'

function Pagina({ nome, verso }: { nome: string; verso: string }) {
  return (
    <section>
      <h1>{nome}</h1>
      <Link to={verso}>vai</Link>
    </section>
  )
}

function monta() {
  const router = createMemoryRouter([
    {
      element: <Shell />,
      children: [
        { path: '/', element: <Pagina nome="Uno" verso="/due" /> },
        { path: '/due', element: <Pagina nome="Due" verso="/lenta" /> },
        // a page whose code never arrives: the navigation stays pending
        { path: '/lenta', lazy: () => new Promise<never>(() => {}) },
      ],
    },
  ], { initialEntries: ['/'] })
  render(<RouterProvider router={router} />)
}

const involucro = (h1: HTMLElement) => h1.closest('[data-transizione]') as HTMLElement

describe('transizioni di pagina (design 4.4)', () => {
  it('ogni pagina raggiunta navigando entra con una dissolvenza di 200 ms (nessuna con reduced-motion); la prima no', async () => {
    monta()
    const primo = involucro(await screen.findByRole('heading', { name: 'Uno' }))
    expect(primo).not.toBeNull()
    expect(primo.className).not.toContain('animate-in') // the first page of the visit: no delay to its first paint
    fireEvent.click(screen.getByRole('link', { name: 'vai' }))
    const secondo = involucro(await screen.findByRole('heading', { name: 'Due' }))
    expect(secondo).not.toBe(primo) // keyed on the path: a new wrapper, the animation runs again
    for (const c of ['animate-in', 'fade-in', 'duration-200', 'motion-reduce:animate-none']) expect(secondo.className).toContain(c)
  })

  it('navigazione in corso: main aria-busy e una barra sottile, la pagina vecchia resta', async () => {
    monta()
    fireEvent.click(await screen.findByRole('link', { name: 'vai' }))
    await screen.findByRole('heading', { name: 'Due' })
    expect(screen.getByRole('main').getAttribute('aria-busy')).toBe('false')
    await act(async () => fireEvent.click(screen.getByRole('link', { name: 'vai' })))
    expect(screen.getByRole('main').getAttribute('aria-busy')).toBe('true')
    expect(document.querySelector('[data-navigazione]')).not.toBeNull()
    expect(screen.getByRole('heading', { name: 'Due' })).toBeInTheDocument()
  })

  it('primo caricamento (HydrateFallback): skeleton nel main, bottone del menu disattivato', () => {
    const router = createMemoryRouter([{ path: '/', element: <ShellInAttesa /> }])
    render(<RouterProvider router={router} />)
    expect(screen.getByRole('main').querySelector('[data-slot="skeleton"]')).not.toBeNull()
    expect((screen.getByRole('button', { name: 'Apri il menu' }) as HTMLButtonElement).disabled).toBe(true)
  })
})
