// The Live route's errorElement: a render error (an unexpected payload) replaces only the page's body; the layout, with the
// footer's fixed note, stays.
export function ErroreLive() {
  return (
    <section className="space-y-3" role="alert">
      <h1 className="font-serif text-3xl font-semibold tracking-tight md:text-4xl">Frequenze live</h1>
      <p className="text-muted-foreground text-sm leading-relaxed">
        La pagina live non si puo' mostrare: i dati ricevuti dal motore hanno una forma inattesa. Ricarica la pagina tra qualche
        secondo; le pagine delle ricerche e del metodo restano disponibili.
      </p>
    </section>
  )
}
