import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import path from 'node:path'
import { defineConfig } from 'vite'

export default defineConfig({
  base: '/',
  plugins: [react(), tailwindcss()],
  resolve: { alias: { '@': path.resolve(import.meta.dirname, 'src') } },
  build: {
    assetsDir: 'app',
    // Nessun gruppo manuale di chunk: i gruppi "motion"/"bklit" catturavano anche le dipendenze (react, utils) e l'entry li
    // importava staticamente su OGNI rotta (modulepreload di ~130 kB gz). Lo split per rotta (React.lazy) basta.
  },
})
