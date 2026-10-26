import { useParams } from 'react-router'

export default function Ricerca() {
  const { id } = useParams()
  return (
    <section>
      <h1 className="font-serif text-4xl font-semibold tracking-tight">Ricerca</h1>
      <p className="text-muted-foreground mt-3">Segnaposto: dettaglio della ricerca {id}.</p>
    </section>
  )
}
