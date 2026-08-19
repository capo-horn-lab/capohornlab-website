# Computer Use — Velocità e Fluidità: Ricerca da Reddit e GitHub

**Capo Horn Lab — Research Note · 2026-08-19**
**Oggetto:** come rendere il computer use (cua-driver/Hermes su Windows) più veloce e fluido.

## Sintesi (2 righe)
Il collo di bottiglia NON è l'input (click/type: 3–20 ms) ma la **percezione**: ogni ciclo costa 1 screenshot + 1-4 chiamate LLM. Le ottimizzazioni a maggior impatto: albero accessibilità come targeting primario (elimina 1–3 s/azione), screenshot più piccoli, e meno re-capture tra le azioni.

## Fonti verificate

### GitHub
1. **simular-ai/Agent-S issue #181** (mar 2026) — discussione AX tree vs vision grounding:
   - "Accessibility trees give you free coordinates. That eliminates 1-3 seconds per action."
   - "One LLM call decides the action, and the accessibility tree resolves the target — one call per step, sub-100ms target resolution."
   - "Vision-based grounding: 2-4 LLM calls per single GUI action... that's 3-8x faster per action [with AX]."
   - Il maintainer di Agent-S conferma: "The OS needs time to render the accessibility tree, which introduces significant latency on large or complex webpages" — MA vision grounding aggiunge 2-4 chiamate LLM. Trade-off reale; ibrido consigliato.
   - https://github.com/simular-ai/Agent-S/issues/181

2. **actionstatelabs/android-action-kernel** (repo README, tabella costi/latenza):
   - Screenshots: $0.15/azione, 3-5s, 70-80% accuratezza (desktop)
   - Accessibility Tree: $0.01/azione, <1s, 99% accuratezza (Android)
   - https://github.com/actionstatelabs/android-action-kernel

3. **vm0-ai/vm0 issue #21798** — "perf(computer-use): align Zero App State and batching": batching delle osservazioni di stato per ridurre il numero di snapshot per azione.
   - https://github.com/vm0-ai/vm0/issues/21798

### Reddit
4. r/AI_Agents — "Computer Use Agents Help" (1q95qd5): "latency stacks as well. first, make the tasks much smaller. come back in 1–3 seconds, reliability improves a lot." → granularità del task, non solo velocità del driver.
5. r/AgentsOfAI — "AI Computer/Phone use" (1rzz2nr): "The bottleneck isn't vision or control — it's latency and state recovery." → lo stato (re-capture) domina il costo.
6. developersdigest.tech (FAQ Claude Computer Use): "Expect 2-5 seconds per action depending on the model and screenshot resolution." → la risoluzione dello screenshot scala la latenza.

### Documentazione Hermes (locale, v0.20.2)
7. `website/docs/user-guide/features/computer-use.md` — limiti performance: eventi AX 3–20 ms (Windows UIA 3–10 ms); il tipo di input NON è il collo di bottiglia.
8. Config `computer_use.*`: `max_image_dimension` (default 1456) → riscala gli screenshot; `capture_after_mode` (som); `cua_telemetry` (false).

## Raccomandazioni applicabili (sistema attuale)

| # | Azione | Impatto atteso | Rischio |
|---|--------|---------------|---------|
| 1 | `computer_use.max_image_dimension` 1456 → 1024 | Vision più veloce, meno token | Testo piccolo meno leggibile; gli overlay SOM compensano |
| 2 | Usare `mode='ax'` (solo albero, zero immagine) per target testuali | Elimina la chiamata vision dal ciclo | Niente contesto visivo |
| 3 | Click per **element index**, mai pixel a caso | Zero grounding vision, targeting deterministico | — |
| 4 | Batch: 1 capture → più azioni → 1 verifica (non capture dopo ogni click) | -40/60% cicli | Verifica a tappe, non dopo ogni micro-azione |
| 5 | Capture con `app='Chrome'`/window specifica | Albero più piccolo, meno rumore | — |
| 6 | Task piccoli (1-3s per passo) | Affidabilità ↑, retry ↓ | — |
| 7 | `capture_after=true` solo quando serve la verifica immediata | Meno immagini nel contesto | — |

## Verifica empirica (sessione deploy Aruba, 2026-08-19)
Durante l'upload su Aruba ho applicato 3-4-5: 46 elementi analizzati in ~15 azioni guidate; i soli punti lenti sono stati (a) i dialoghi nativi (file picker) e (b) il context-menu di elFinder che non risponde ai click in background (limite PostMessage, non velocità). Confermato: il problema non è il driver, è il numero di cicli percezione/azione.

## Fonti e data accesso
Tutte le fonti consultate il 2026-08-19. Reddit via snippet di ricerca (API pubblica bloccata); GitHub via API/issue pubbliche.
