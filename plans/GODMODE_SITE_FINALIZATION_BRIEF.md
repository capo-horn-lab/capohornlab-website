# Capo Horn Lab — GODMODE Site Finalization Brief

Date: 2026-08-24
Coordinator: Camilla
Execution model: DeepSeek V4 Pro via OpenRouter for site team

## User directive
Francesco approved the new Observatory direction and said: finish this site once and for all. God Mode active for the site team.

## Scope
Finish the website locally and reversibly first. Produce verified artifacts, screenshots and QA. Do not declare production complete until live deploy/backend/email/payment gates are actually verified.

## Hard boundaries
- No trading live.
- No broker/order execution.
- No DNS changes.
- No payment activation or fake payment success.
- No secret access, secret printing, or credential changes.
- No destructive deletes.
- No external publishing/deploy unless Camilla creates a frozen deployment payload and Francesco confirms again.

## Current high-value design assets
- `D:/CapoHornLab/projects/capohornlab-website/design/capo-horn-observatory-concept-v2-unified.html`
- `D:/CapoHornLab/projects/capohornlab-website/design/observatory-tokens.css`
- `D:/CapoHornLab/projects/capohornlab-website/design/observatory-components.html`
- `D:/CapoHornLab/projects/capohornlab-website/design/observatory-evolution.html`
- `D:/CapoHornLab/projects/capohornlab-website/design/assets/capo-horn-lab-orbit-mark.svg`
- `D:/CapoHornLab/projects/capohornlab-website/design/assets/capo-horn-lab-wordmark.svg`

## Identity that must remain
- Name: Capo Horn Lab
- Motto: Beyond the hedge of the market
- Design language: dark ocean + disciplined signal red `#E33B2F`
- Positioning: quantified strategy research and backtesting, not live trading.

## Finalization priorities
1. Integrate the Observatory visual direction into the actual site homepage while preserving navigation and real CTAs.
2. Align copy with the stronger brand: concise, no fake metrics, no performance guarantees, no motivational fluff.
3. Keep client-visible pricing/provider/data-cost boundaries intact. Internal data/provider economics stay admin-only.
4. Verify static structure, responsive behavior, links, JS parse, asset paths, reduced motion and no unsafe placeholders.
5. Produce a reviewable local build package and screenshot for Francesco.

## Expected deliverables this sprint
- Updated local site files under `D:/CapoHornLab/projects/capohornlab-website/`.
- Agent result envelopes in `D:/CapoHornLab/contracts/envelopes/`.
- QA log/report in `D:/CapoHornLab/contracts/logs/` and/or `reports/`.
- Screenshot/package for Telegram review.
