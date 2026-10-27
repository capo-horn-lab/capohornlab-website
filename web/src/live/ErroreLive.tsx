// The Live route's errorElement: a render error or a page chunk that failed to load (an old tab after a deploy) replaces only
// the page's body; the layout, with the footer's fixed note, stays. Neutral wording: the cause is not known here.
export function ErroreLive() {
  return (
    <section className="space-y-3" role="alert">
      <h1 className="font-serif text-3xl font-semibold tracking-tight md:text-4xl">Frequenze live</h1>
      <p className="text-muted-foreground text-sm leading-relaxed">
        La pagina live non si puo' mostrare in questo momento. Ricarica la pagina tra qualche secondo; le pagine delle ricerche
        e del metodo restano disponibili.
      </p>
    </section>
  )
}
