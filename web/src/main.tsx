import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './styles/theme.css'
import App from './App'
import { precaricaLive } from './lib/api'
import { queryClient } from './lib/query'

// the live page: its two API requests and the chart's chunk start now, in parallel with the page's chunk, not after it
// (a chunk that fails here is only a missed head start: the page imports it again, and says so if it fails there)
if (window.location.pathname === '/') {
  precaricaLive(queryClient)
  import('./live/GraficoLive').catch(() => {})
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
