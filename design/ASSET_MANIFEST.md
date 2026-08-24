# Capo Horn Lab — Observatory Visual Asset Manifest

> Generated: 2026-08-24
> Agent: Dioniso (Hermes Agent / Capo Horn Lab)
> Task: chl-20260824-0006
> Purpose: Production integration readiness — full provenance, licensing, and format audit of every visual asset under `design/` and `design/assets/`.

---

## 1. Logo & Wordmark Assets

### 1.1 Orbit Mark
- **File:** `design/assets/capo-horn-lab-orbit-mark.svg`
- **Format:** SVG 1.1 (vector, 240×240 viewBox)
- **Role:** Primary brand mark — navigational orbit enclosing CH monogram with signal dot (warm orange at 183,58).
- **Source:** Hand-crafted by Camilla / Capo Horn Lab design team.
- **Provenance:** Original work. Created in the Capo Horn Lab design system. Not derived from any stock or third-party asset.
- **License:** Proprietary — Capo Horn Lab. All rights reserved.
- **Accessibility:** `role="img"`, `aria-labelledby="title desc"`, with `<title>` and `<desc>` elements.
- **Technique:** Layered `<circle>`, `<path>`, and `<linearGradient>` strokes. Uses `#E33B2F` (signal red core), `#FF9B64` (warm dot), `#F7E8E2` (monogram text). Includes `feDropShadow` filter for depth.
- **Fallback:** CSS-only equivalent exists in `observatory-components.html` as `.logo-orbit` (lines 407–438). Renders without external dependencies.

### 1.2 Wordmark
- **File:** `design/assets/capo-horn-lab-wordmark.svg`
- **Format:** SVG 1.1 (vector, 760×180 viewBox)
- **Role:** Horizontal brand lockup — orbit mark (left) + "CAPO HORN LAB" text + "BEYOND THE HEDGE OF THE MARKET" motto + "RESEARCH OBSERVATORY · STRATEGY TESTING · NO LIVE TRADING" tagline.
- **Source:** Hand-crafted by Camilla / Capo Horn Lab design team.
- **Provenance:** Original work. Integrates the orbit mark as an inline SVG group (scaled down to 108×108 region). Text rendered via SVG `<text>` with system font stack.
- **License:** Proprietary — Capo Horn Lab. All rights reserved.
- **Accessibility:** `role="img"`, `aria-labelledby="title desc"`, with `<title>` and `<desc>` elements.
- **Technique:** Dark background rect (`#080d14`, rx=28), integrated orbit mark group, three-tier typography. Primary brand type rendered as Inter/Arial fallback (42px, weight 750, letter-spacing 2). Motto in signal red (17px, weight 600, letter-spacing 4.8). Tagline in quiet grey (11px, JetBrains Mono/Consolas, letter-spacing 2.4).
- **Note on font rendering:** As a standalone SVG, text falls back to system-installed fonts. When embedded in the Observatory HTML pages (which load Google Fonts), the surrounding page's font stack provides richer rendering. This is standard SVG behavior and not a defect.

---

## 2. Design System Core

### 2.1 Observatory Design Tokens
- **File:** `design/observatory-tokens.css`
- **Format:** CSS3 custom properties (221 lines)
- **Role:** Canonical design token system — the single source of truth for all Observatory visual decisions.
- **Source:** Authored by Camilla / Capo Horn Lab design team.
- **Provenance:** Original work. Design references cited inline: BMW (weight extremes, sharp geometry), Sanity (colorimetric depth). No code copied from external design systems.
- **License:** Proprietary — Capo Horn Lab. All rights reserved.
- **Sections:**
  1. Color palette (11 surface tokens, 4 text tokens, 4 signal accent tokens, 2 warm tokens, 4 semantic tokens, 6 surface overlay tokens)
  2. Typography (3 font families, 11-size modular scale at 1.25 ratio, 4 fluid clamp sizes, 6 line heights, 4 font weights, 4 letter-spacing values)
  3. Spacing (4px grid, 18 spacing stops, 2 fluid section padding variables)
  4. Radii (6 stops: none → pill)
  5. Shadows & glow (6 definitions including signal and warm glows)
  6. Motion (4 easing curves, 4 duration stops)
  7. Z-index (6 layers)
  8. Layout (max-width, wrap padding, nav height)
  9. Dark mode (default; the Observatory is dark-first)
  10. Reduced motion (`prefers-reduced-motion: reduce` kills all animations to 0.001ms)
  11. Global reset (`.ch-reset` opt-in class)
  12. Utility classes (`.ch-wrap`, `.ch-sr-only`, `.ch-grid-2`, `.ch-grid-3`)
- **Verification gate:** All custom properties use the `--ch-` namespace to avoid collisions. No `!important` outside the reduced-motion block. Responsive grid breakpoint at 820px.

### 2.2 Observatory Component Library
- **File:** `design/observatory-components.html`
- **Format:** HTML5 (720 lines, self-contained with inline `<style>` + tokens CSS link)
- **Role:** Component showcase and reference implementation — 15 reusable building blocks.
- **Source:** Authored by Camilla / Capo Horn Lab design team.
- **Provenance:** Original work. All components are custom implementations referencing the observatory-tokens.css token system.
- **License:** Proprietary — Capo Horn Lab. All rights reserved.
- **Components catalogued:**
  1. Brand Lockup — inline orbit mark + name + motto, bordered, backdrop-blurred
  2. Status Eyebrow — pulsing dot + mono label, 4 color variants (signal/warm/success/danger/info)
  3. Research Card — numbered card with hover-to-signal transition, arrow reveal, `.current` state
  4. Data Panel — tall bordered panel with tag + heading + body + 5-segment completeness strip
  5. Instrument Field — research canvas placeholder with coordinates overlay and legend
  6. Ticker Bar — infinite scroll marquee (30s linear, CSS animation)
  7. Action Buttons — primary (signal fill), secondary (bordered), ghost (signal-bordered transparent)
  8. Section Kicker — mono label with `data-num "XX / "` prefix
  9. Navigation Switcher — bordered tab bar, `.active` state, `role="tablist"`
  10. Closing CTA — oversized heading with "CHL" watermark, warm italic emphasis
  11. Completeness Strip — 5-segment progress bar with filled/warm/empty states
  12. CSS-Only Logo Orbit — pure CSS concentric circles + warm dot, rotated -18°
  13. Orbital Canvas Placeholder — radial-gradient crosshair cursor background
  14. Depth Plane Stack — 4-plane 3D perspective stack with hover parallax
  15. Info Chips — compact mono badges, signal and warm variants
- **Responsive:** Two breakpoints — 820px (tablet) and 520px (mobile). Instruments collapse to single-column. Buttons reduce to 44px min-height.
- **Accessibility:** Switcher uses `role="tablist"`. Footer uses semantic `<footer>`. All interactive demos are wrapped in `<script>` with no external dependencies.
- **Motion compliance:** Ticker animation disabled via `@media (prefers-reduced-motion: reduce)`.

### 2.3 Observatory Evolution Page (v03)
- **File:** `design/observatory-evolution.html`
- **Format:** HTML5 (860 lines, self-contained with inline `<style>` + tokens CSS link)
- **Role:** Full-page reference implementation with interactive orbital canvas.
- **Source:** Authored by Camilla / Capo Horn Lab design team.
- **Provenance:** Original work. Evolution 03 builds on the component library with interaction, scroll-driven depth, and a Canvas-based research node placement system.
- **License:** Proprietary — Capo Horn Lab. All rights reserved.
- **Sections:** Masthead (nav + hero + instrument panel), Ticker bar, Thesis section, Systems section (with interactive room switcher + system detail panel), Closing CTA, Footer.
- **Interactive features:**
  - Canvas orbital field: 130 deterministic particles (seeded PRNG, seed=1847) orbiting in 3D projected space with mouse-driven tilt/lift. Click to place research nodes (warm diamond markers, max 12, FIFO eviction).
  - Room switcher: 3-room tab navigation updating tag/title/text via JS.
  - Scroll-driven depth: smooth scroll behavior.
- **Responsive:** 820px (hero → single column, thesis → single column, system grid → stacked, nav links collapse to `.enter` only), 520px (reduced hero size, compact buttons and nav).
- **Accessibility:** `aria-label` on nav, instrument section, and canvas. Field hint text fades after first node placement. All interactive elements keyboard-accessible via standard `<button>` and `<a>` elements.
- **Motion:** `prefers-reduced-motion: reduce` kills all animations and transitions. Canvas loop stops via `matchMedia` check.

### 2.4 Unified Concept Page (v2)
- **File:** `design/capo-horn-observatory-concept-v2-unified.html`
- **Format:** HTML5 (1031 lines, self-contained with inline `<style>` + tokens CSS link)
- **Role:** Full design direction showcase with palette variants (default signal red, cobalt blue, coral yellow).
- **Source:** Authored by Camilla / Capo Horn Lab design team.
- **Provenance:** Original work. Palette variants are CSS custom property overrides applied via `data-palette` attribute on `<body>`.
- **License:** Proprietary — Capo Horn Lab. All rights reserved.
- **Palette variants:** Three complete color schemes — default (`#E33B2F` signal red), `cobalt` (`#66A8FF` signal blue), `coral` (`#FFD452` signal yellow/gold). All variants preserve the same structural tokens (spacing, typography, motion, layout).
- **Screenshot preview:** `design/preview-observatory-v2-unified.png` (raster reference image, generated during design review).

---

## 3. Font Stack

| Font | Source | License | Format | Usage |
|------|--------|---------|--------|-------|
| Playfair Display | Google Fonts (fonts.google.com) | SIL Open Font License 1.1 | WOFF2 | Serif headings, hero text, display typography |
| DM Sans | Google Fonts (fonts.google.com) | SIL Open Font License 1.1 | WOFF2 | Primary body, navigation, UI text |
| DM Mono | Google Fonts (fonts.google.com) | SIL Open Font License 1.1 | WOFF2 | Technical labels, coordinates, buttons, monospace data |

**Loading method:** All pages use `<link rel="preconnect">` to `fonts.googleapis.com` and `fonts.gstatic.com` with a combined Google Fonts URL. No self-hosted font files exist under `design/assets/` — this is by design; the production build may choose to self-host for performance. All three fonts are OFL-licensed and permit self-hosting, modification, and commercial use.

**System fallbacks:**
- Serif: `Georgia, "Times New Roman", serif`
- Sans: `system-ui, -apple-system, "Segoe UI", sans-serif`
- Mono: `"JetBrains Mono", "Fira Code", monospace`

---

## 4. Motion & Interaction Catalog

| Motion Asset | Location | Type | Duration | Easing | Reduced Motion |
|-------------|----------|------|----------|--------|----------------|
| Ticker drift | `components.html:261`, `evolution.html:301` | CSS `@keyframes` (translateX -35%) | 30s linear infinite | linear | animation: none |
| Particle orbit | `evolution.html:735-822` | JS `requestAnimationFrame` | continuous (60fps) | smooth interpolation | loop stops via matchMedia |
| Logo hover rotate | `evolution.html:79-81` | CSS `transform: rotate(12deg) scale(1.06)` | var(--ch-duration-slow) 450ms | var(--ch-ease-orbit) | duration → 0.001ms |
| Card hover arrow | `components.html:149-151` | CSS `transform: translateX(4px)` | var(--ch-duration-fast) 120ms | var(--ch-ease-out) | duration → 0.001ms |
| Depth stack hover | `components.html:480-483` | CSS `transform: translateZ()` | var(--ch-duration-slow) 450ms | var(--ch-ease-out) | duration → 0.001ms |
| Button hover lift | `components.html:290` | CSS `transform: translateY(-3px)` | var(--ch-duration-fast) 120ms | var(--ch-ease-out) | duration → 0.001ms |

**Easing functions (defined in tokens.css):**
- `--ch-ease-out`: cubic-bezier(0.16, 1, 0.3, 1) — deceleration
- `--ch-ease-in-out`: cubic-bezier(0.65, 0, 0.35, 1) — symmetric
- `--ch-ease-spring`: cubic-bezier(0.34, 1.56, 0.64, 1) — overshoot
- `--ch-ease-orbit`: cubic-bezier(0.2, 0.8, 0.2, 1) — orbital (smooth entry/exit)

---

## 5. External Dependencies

| Dependency | URL | Role | License | Risk |
|-----------|-----|------|---------|------|
| Google Fonts CSS API | `fonts.googleapis.com` | Font loading (Playfair Display, DM Sans, DM Mono) | OFL-1.1 (fonts) | Low — Google Fonts CDN is stable; fonts are OFL and can be self-hosted if needed. |
| Google Fonts Static | `fonts.gstatic.com` | Font file delivery | OFL-1.1 | Low — standard CDN. Production should consider self-hosting for performance and GDPR compliance. |
| `observatory-tokens.css` | Local file (`design/observatory-tokens.css`) | Design token import | Proprietary | None — local file. |
| `assets/capo-horn-lab-orbit-mark.svg` | Local file (`design/assets/`) | Brand mark | Proprietary | None — local file. |

**No external JavaScript dependencies.** All interactivity is vanilla JS with no frameworks. The orbital canvas uses only the standard Canvas 2D API.

---

## 6. Verification Summary

| Check | Result |
|-------|--------|
| All SVG assets have valid XML structure | PASS — both SVGs parse cleanly with proper `xmlns`, `viewBox`, and closing tags |
| Accessibility attributes on SVGs | PASS — `role="img"`, `aria-labelledby`, `<title>`, `<desc>` present on both |
| CSS tokens use `--ch-` namespace | PASS — no collisions, consistent naming convention |
| Reduced motion respected | PASS — `prefers-reduced-motion: reduce` blocks all animations (tokens.css:164-176, components.html:527-529, evolution.html:520-525) |
| Responsive breakpoints defined | PASS — 820px and 520px breakpoints with single-column fallbacks |
| No unsafe placeholders | PASS — no fake metrics, no performance guarantees, no AI-generated testimonials |
| Font licenses documented | PASS — all three fonts are SIL OFL 1.1, free for commercial use |
| No external asset provenance gaps | PASS — every asset is original Capo Horn Lab work or a freely-licensed web font |
| Asset paths resolve within design/ | PASS — relative paths `assets/...` and `observatory-tokens.css` resolve correctly from HTML files in `design/` |
| No live trading language | PASS — all copy uses "research observatory," "strategy testing," "no live trading" |

---

## 7. Production Integration Notes

1. **Self-host fonts before go-live.** The three Google Fonts (Playfair Display, DM Sans, DM Mono) are OFL-licensed and should be self-hosted for performance and to avoid third-party requests on the production site.
2. **Wordmark SVG font rendering.** The standalone SVG wordmark falls back to system fonts. For production headers, render the lockup via HTML/CSS (as done in the evolution page's `.mark` component) for consistent typography, using the SVG as a secondary format for social sharing / OG images.
3. **Token file is the single source of truth.** Any new component or page must import `observatory-tokens.css` and use `--ch-*` variables exclusively. Do not hardcode color hex values or spacing values outside the token file.
4. **Canvas performance.** The orbital canvas in `observatory-evolution.html` uses `devicePixelRatio` capping at 1.5 and a deterministic particle system — performance is bounded and predictable. Test on low-end mobile before production.
5. **Palette variants** (cobalt, coral) are defined in the unified concept page only. Promote them to the token file if they become official brand variants.

---

---

## 8. Archive / Legacy Artifacts (not part of current Observatory direction)

The following files exist under `design/` but predate the current Observatory design system. They are retained for reference only and should not be used as production sources:

| File | Description | Status |
|------|-------------|--------|
| `design-tokens.html` | Older v1.0 token system (1839 lines, Inter + JetBrains Mono font stack, navy-palette primitives). Not aligned with current Observatory tokens. | Legacy |
| `capo-horn-observatory-concept.html` | Original concept page (pre-unified). | Superseded by v2-unified |
| `capo-horn-observatory-concept-v2.html` | Intermediate concept page. | Superseded by v2-unified |
| `OBSERVATORY_EVOLUTION_BRIEF.md` | Design brief for Evolution 03 iteration. | Reference only |
| `*.zip` files (6 archives) | Prior design iteration snapshots and mockup packages. | Archive — do not extract for production |

---

*End of manifest. File: `design/ASSET_MANIFEST.md`*
*Provenance: All assets reviewed by Dioniso, 2026-08-24. No external assets introduced.*