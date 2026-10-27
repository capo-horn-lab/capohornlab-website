import { curveLinear } from '@visx/curve'
import { useMemo } from 'react'
import {
  Bar,
  BarChart,
  ChartTooltip,
  Grid,
  Line,
  LineChart,
  XAxis,
  YAxis,
} from '@/components/charts'
import { BarXAxis } from '@/components/charts/bar-x-axis'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { barreTabella, puntiSerie } from './grafico-dati'
import type { Dati } from './modello'

const numero = (x: unknown): number | null => (typeof x === 'number' && Number.isFinite(x) ? x : null)

/** Il grafico dipende dal `tipo` di dati.json: serie -> linea, tabella -> barre, matrice -> celle ombreggiate. */
export function Grafico({ dati }: { dati: Dati }) {
  if (dati.tipo === 'serie') return <GraficoSerie dati={dati} />
  if (dati.tipo === 'matrice') return <Matrice dati={dati} />
  return <GraficoTabella dati={dati} />
}

function GraficoSerie({ dati }: { dati: Dati }) {
  const { colonna, punti, buchi } = useMemo(() => puntiSerie(dati), [dati])
  const dateX = useMemo(
    () => punti.map((p) => ({ date: new Date(Date.UTC(Number(p.anno), 0, 1)), valore: p.valore })),
    [punti],
  )
  if (colonna < 0) return null
  if (buchi > 0) {
    // un anno senza valore: niente linea (unirebbe due punti attraverso il buco), solo la tabella dei valori della prova
    return (
      <figure aria-label={`Serie per anno, colonna ${dati.colonne[colonna]}`}>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>{dati.colonne[0]}</TableHead>
              <TableHead>{dati.colonne[colonna]}</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {dati.righe.map((r, i) => (
              <TableRow key={i}>
                <TableCell className="font-mono text-xs">{String(r[0])}</TableCell>
                <TableCell className="font-mono text-xs">{numero(r[colonna]) ?? 'senza valore'}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <figcaption className="text-muted-foreground mt-2 text-xs">
          {buchi} anni senza valore nella prova: non disegnati.
        </figcaption>
      </figure>
    )
  }
  if (dateX.length < 2) return null
  return (
    <figure aria-label={`Serie per anno, colonna ${dati.colonne[colonna]}`}>
      <LineChart data={dateX} aspectRatio="2.6 / 1" margin={{ top: 24, right: 24, bottom: 36, left: 48 }}>
        <Grid horizontal numTicksRows={4} />
        <Line dataKey="valore" curve={curveLinear} showMarkers />
        <XAxis labels={punti.map((p) => p.anno)} numTicks={Math.min(8, punti.length)} />
        <YAxis numTicks={4} />
        <ChartTooltip showDatePill={false} />
      </LineChart>
    </figure>
  )
}

const MAX_BARRE = 60

function GraficoTabella({ dati }: { dati: Dati }) {
  const { colonna, barre, omesse, unitaMiste } = useMemo(() => barreTabella(dati), [dati])
  if (colonna < 0 || barre.length < 2 || barre.length > MAX_BARRE) return null
  return (
    <figure aria-label={`Barre della colonna ${dati.colonne[colonna]}`}>
      <BarChart
        data={barre}
        xDataKey="etichetta"
        aspectRatio="2.6 / 1"
        margin={{ top: 24, right: 24, bottom: 40, left: 48 }}
      >
        <Grid horizontal numTicksRows={4} />
        <Bar dataKey="valore" />
        <BarXAxis maxLabels={6} />
        <YAxis numTicks={4} />
        <ChartTooltip />
      </BarChart>
      {omesse > 0 && (
        <figcaption className="text-muted-foreground mt-2 text-xs">
          {omesse} righe senza valore nella prova: senza barra.
        </figcaption>
      )}
      {unitaMiste && (
        <figcaption className="text-muted-foreground mt-2 text-xs">
          Le righe hanno unita' diverse (colonna u): il confronto tra barre non e' omogeneo.
        </figcaption>
      )}
    </figure>
  )
}

/** Nessuna matrice e' generata oggi dalle prove; se arriva, celle ombreggiate con i token dei grafici. */
function Matrice({ dati }: { dati: Dati }) {
  const valori = dati.righe.flatMap((r) => r.slice(1).map(numero)).filter((x): x is number => x !== null)
  const minimo = Math.min(...valori)
  const massimo = Math.max(...valori)
  const intensita = (v: number | null) =>
    v === null || massimo === minimo ? 0 : Math.round(((v - minimo) / (massimo - minimo)) * 80)
  return (
    <Table>
      <TableHeader>
        <TableRow>
          {dati.colonne.map((c) => (
            <TableHead key={c}>{c}</TableHead>
          ))}
        </TableRow>
      </TableHeader>
      <TableBody>
        {dati.righe.map((r, i) => (
          <TableRow key={i}>
            {r.map((v, j) => (
              <TableCell
                key={j}
                className="font-mono text-xs"
                style={
                  j > 0 && numero(v) !== null
                    ? { background: `color-mix(in oklab, var(--chart-1) ${intensita(numero(v))}%, var(--card))` }
                    : undefined
                }
              >
                {v === null ? 'senza valore' : String(v)}
              </TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
