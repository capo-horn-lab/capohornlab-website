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
    // Vite 8 usa Rolldown: rolldownOptions al posto di rollupOptions, codeSplitting.groups al posto di manualChunks.
    rolldownOptions: {
      output: {
        codeSplitting: {
          groups: [
            { name: 'motion', test: /node_modules[\\/](motion|motion-dom|motion-utils|framer-motion)[\\/]/, priority: 30 },
            { name: 'bklit', test: /node_modules[\\/](@visx|d3-[a-z-]+|internmap|@number-flow)[\\/]|src[\\/]components[\\/]charts[\\/]/, priority: 20 },
          ],
        },
      },
    },
  },
})
