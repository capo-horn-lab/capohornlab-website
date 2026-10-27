// A chart whose chunk did not load (an old tab after a deploy, a network blip): one line in its place, the rest of the page stays.
export function GraficoNonDisponibile() {
  return (
    <p role="alert" className="text-muted-foreground text-sm">
      Il grafico non si puo' mostrare in questo momento: ricarica la pagina tra qualche secondo.
    </p>
  )
}
