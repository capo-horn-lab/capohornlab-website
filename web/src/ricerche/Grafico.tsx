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
import { colonnaValori, type Dati } from './modello'

const numero = (x: unknown): number | null => (typeof x === 'number' && Number.isFinite(x) ? x : null)

/** Il grafico dipende dal `tipo` di dati.json: serie -> linea, tabella -> barre, matrice -> celle ombreggiate. */
export function Grafico({ dati }: { dati: Dati }) {
  if (dati.tipo === 'serie') return <GraficoSerie dati={dati} />
  if (dati.tipo === 'matrice') return <Matrice dati={dati} />
  return <GraficoTabella dati={dati} />
}

function GraficoSerie({ dati }: { dati: Dati }) {
  const c = colonnaValori(dati)
  const punti = useMemo(
    () =>
      dati.righe.map((r) => ({
        date: new Date(Date.UTC(Number(r[0]), 0, 1)),
        valore: numero(r[c]) ?? 0,
      })),
    [dati, c],
  )
  if (c < 0 || punti.length < 2) return null
  return (
    <figure aria-label={`Serie per anno, colonna ${dati.colonne[c]}`}>
      <LineChart data={punti} aspectRatio="2.6 / 1" margin={{ top: 24, right: 24, bottom: 36, left: 48 }}>
        <Grid horizontal numTicksRows={4} />
        <Line dataKey="valore" curve={curveLinear} showMarkers />
        <XAxis labels={dati.righe.map((r) => String(r[0]))} numTicks={Math.min(8, punti.length)} />
        <YAxis numTicks={4} />
        <ChartTooltip showDatePill={false} />
      </LineChart>
    </figure>
  )
}

const MAX_BARRE = 60

function GraficoTabella({ dati }: { dati: Dati }) {
  const c = colonnaValori(dati)
  const iEt = dati.colonne.indexOf('r') >= 0 ? dati.colonne.indexOf('r') : 0
  const barre = useMemo(
    () => dati.righe.map((r) => ({ etichetta: String(r[iEt]), valore: numero(r[c]) ?? 0 })),
    [dati, c, iEt],
  )
  if (c < 0 || barre.length < 2 || barre.length > MAX_BARRE) return null
  const unita = new Set(dati.righe.map((r) => String(r[dati.colonne.indexOf('u')] ?? '')))
  return (
    <figure aria-label={`Barre della colonna ${dati.colonne[c]}`}>
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
      {unita.size > 1 && (
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
                {String(v ?? '')}
              </TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
