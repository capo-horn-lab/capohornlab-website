import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './styles/theme.css'
import App, { queryClient } from './App'
import { precaricaLive } from './lib/api'

// the live page: its two API requests and the chart's chunk start now, in parallel with the page's chunk, not after it
if (window.location.pathname === '/') {
  precaricaLive(queryClient)
  void import('./live/GraficoLive')
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
