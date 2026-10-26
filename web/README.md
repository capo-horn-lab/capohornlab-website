# web/ — sito finale capohornlab.com (FREQ-SITO-3)

App Vite + React + shadcn/ui + Bklit + Motion sui token Observatory. Export statico (`dist/`, asset in `dist/app/`) caricato su Aruba.

## Comandi

- `npm run dev` — server di sviluppo
- `npm run build` — controllo tipi + build in `dist/`
- `npm run preview` — serve `dist/`
- `npm test` — vitest

Task 5 aggiunge gli script `verifica` (non ancora presenti in `package.json`).

## Struttura

- `src/styles/observatory-tokens.css` — copia di `../design/observatory-tokens.css` (non modificarla qui; un test controlla che coincidano)
- `src/styles/theme.css` — mappa i token `--ch-*` sulle variabili shadcn e Bklit (solo tema scuro, `html.dark` fisso)
- `public/fonts/` — DM Sans, DM Mono, Playfair Display in locale (licenza OFL, vedi `LICENZE.md`); nessun CDN
- `src/components/ui/` — shadcn; `src/components/charts/` — Bklit, import da `@/components/charts`
- `src/lib/config.ts` — `API_BASE` (override con `VITE_API_BASE`)
- `src/layout/`, `src/pagine/` — shell e pagine (rotte `/`, `/ricerche`, `/ricerche/:id`, `/metodo`, `/stato`)

## Aggiungere componenti

`npx shadcn@latest add <nome>` oppure `npx shadcn@latest add @bklit/<nome>`. Dopo ogni add controllare:

1. `git diff src/styles/theme.css`: la CLI di Bklit riaccoda blocchi `:root` / `.dark` con colori `oklch(...)` che sovrascrivono i nostri `--chart-*`. Vanno rimossi (le variabili sono gia' definite in `theme.css` sui token Observatory).
2. `git diff src/lib/utils.ts` e gli import `from "cn"` nei file di `src/components/ui/`: la CLI 4.x scrive `import { cn } from "cn"` e installa il pacchetto `cn`; qui si usa `@/lib/utils` (sostituire e `npm uninstall cn`).
3. Nessun colore fuori dai token (`text-white`, `bg-black`, `#hex`, `rgb(...)`, `zinc`): il test del tema controlla `theme.css`, il resto va guardato a mano.
