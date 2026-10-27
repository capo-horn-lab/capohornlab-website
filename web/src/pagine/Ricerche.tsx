import { useQueries } from '@tanstack/react-query'
import { useMemo, useState } from 'react'
import { Link } from 'react-router'
import { LineSparkline } from '@/components/charts'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { caricaDati, indice } from '@/ricerche/archivio'
import { valoriSerie } from '@/ricerche/grafico-dati'
import { anno, paroleNude, SENZA_VERDETTO } from '@/ricerche/modello'
import { AuditBadge, VerdettoBadge } from '@/ricerche/Testo'

const TUTTI = ''

/** Le voci del filtro di una pagina: le parole nude del registro (mai l'ID), o "senza verdetto". */
const vociFiltro = (verdetto: string) => {
  const parole = paroleNude(verdetto)
  return parole.length ? parole : [SENZA_VERDETTO]
}

function Filtro({
  etichetta,
  valore,
  opzioni,
  onChange,
}: {
  etichetta: string
  valore: string
  opzioni: string[]
  onChange: (v: string) => void
}) {
  return (
    <label className="text-muted-foreground flex flex-col gap-1 text-xs tracking-[0.12em] uppercase">
      {etichetta}
      <select
        value={valore}
        onChange={(e) => onChange(e.target.value)}
        className="border-input bg-card text-foreground focus-visible:ring-ring/50 h-9 rounded-md border px-2 text-sm tracking-normal normal-case focus-visible:ring-[3px] focus-visible:outline-none"
      >
        <option value={TUTTI}>Tutti</option>
        {opzioni.map((o) => (
          <option key={o} value={o}>
            {o}
          </option>
        ))}
      </select>
    </label>
  )
}

/** Valori della prima colonna numerica per le ricerche il cui dati.json e' una serie (le altre: nessuna sparkline). */
function useSerie(ids: string[]) {
  const risultati = useQueries({
    queries: ids.map((id) => ({ queryKey: ['dati', id], queryFn: () => caricaDati(id), staleTime: Infinity })),
  })
  return useMemo(() => {
    const mappa: Record<string, number[]> = {}
    ids.forEach((id, i) => {
      const d = risultati[i]?.data
      if (d?.tipo !== 'serie') return
      const valori = valoriSerie(d) // un anno senza valore salta il punto: mai 0
      if (valori.length > 0) mappa[id] = valori
    })
    return mappa
  }, [ids, risultati])
}

export default function Ricerche() {
  const [strumento, setStrumento] = useState(TUTTI)
  const [verdetto, setVerdetto] = useState(TUTTI)
  const [annoSel, setAnnoSel] = useState(TUTTI)

  const strumenti = useMemo(() => [...new Set(indice.flatMap((r) => r.strumenti))].sort(), [])
  const anni = useMemo(() => [...new Set(indice.map((r) => anno(r.data)))].sort().reverse(), [])
  // le parole nude del registro presenti nell'indice (piu' "senza verdetto nel registro"), una per voce di filtro
  const verdetti = useMemo(
    () =>
      [...new Set(indice.flatMap((r) => vociFiltro(r.verdetto)))].sort(),
    [],
  )

  const righe = indice.filter(
    (r) =>
      (strumento === TUTTI || r.strumenti.includes(strumento)) &&
      (verdetto === TUTTI || vociFiltro(r.verdetto).includes(verdetto)) &&
      (annoSel === TUTTI || anno(r.data) === annoSel),
  )
  const conGrafico = useMemo(() => indice.filter((r) => r.grafico).map((r) => r.id), [])
  const serie = useSerie(conGrafico)

  return (
    <section className="flex flex-col gap-6">
      <header className="flex flex-col gap-3">
        <h1 className="font-serif text-4xl font-semibold tracking-tight">Ricerche</h1>
        <p className="text-muted-foreground max-w-3xl">
          Ogni pagina riporta una ricerca fatta sul motore, con i numeri copiati dalle prove e il verdetto nel
          registro: la parola scritta in una frase di verdetto alle righe del locatore principale della scheda,
          oppure «{SENZA_VERDETTO}». Frequenze e misure su dati gia' visti: nessuna e' un segnale.
        </p>
      </header>

      <div className="flex flex-wrap items-end gap-4">
        <Filtro etichetta="Strumento" valore={strumento} opzioni={strumenti} onChange={setStrumento} />
        <Filtro etichetta="Verdetto nel registro" valore={verdetto} opzioni={verdetti} onChange={setVerdetto} />
        <Filtro etichetta="Anno" valore={annoSel} opzioni={anni} onChange={setAnnoSel} />
        <p className="text-muted-foreground ml-auto text-sm" aria-live="polite">
          {righe.length} di {indice.length} ricerche
        </p>
      </div>

      {righe.length === 0 ? (
        <p className="text-muted-foreground border-border rounded-md border p-6">
          Nessuna ricerca con questi filtri.
        </p>
      ) : (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Data</TableHead>
              <TableHead>Ricerca</TableHead>
              <TableHead>Strumenti</TableHead>
              <TableHead>Verdetto nel registro</TableHead>
              <TableHead className="text-right">Serie</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {righe.map((r) => (
              <TableRow key={r.id}>
                <TableCell className="font-mono text-xs whitespace-nowrap">{r.data}</TableCell>
                <TableCell className="max-w-xl whitespace-normal">
                  <Link to={`/ricerche/${r.id}`} className="text-foreground underline-offset-4 hover:underline">
                    {r.titolo}
                  </Link>
                </TableCell>
                <TableCell className="text-muted-foreground font-mono text-xs">{r.strumenti.join(' ')}</TableCell>
                <TableCell>
                  <div className="flex flex-col items-start gap-1">
                    <VerdettoBadge verdetto={r.verdetto} />
                    {r.audit && <AuditBadge audit={r.audit} />}
                  </div>
                </TableCell>
                <TableCell className="w-28 text-right">
                  {serie[r.id] && (
                    <LineSparkline data={serie[r.id].map((v) => ({ v }))} dataKey="v" width={96} height={24} />
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
      <p className="text-muted-foreground text-xs">
        Il verdetto e' la parola scritta in una frase di verdetto del registro («Esito …: PAROLA», «Verdetto: PAROLA»,
        elencate nella pagina Metodo) alle righe del locatore principale della scheda; senza una frase cosi' la pagina
        dice «{SENZA_VERDETTO}». «audit: ritirato» e' un segno a parte, solo per gli studi che l'inventario dichiara
        ritirati; «nota dell'audit» e' neutra e non cambia il verdetto.
      </p>
    </section>
  )
}
