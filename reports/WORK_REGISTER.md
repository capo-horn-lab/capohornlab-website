# Capo Horn Lab Website — Work Register

**Updated:** 2026-08-19
**Scope:** God Mode complete-site QA, with production verification separate from local source validation.

## Current release state

| Gate | Status | Evidence |
|---|---|---|
| Local HTML/link QA | 🟢 Pass | 34 root + `pages/` HTML files; zero dead `href="#"`, unresolved fragments, missing local relative links/assets, or visible TODO/lorem/SPLIT_MARKER findings — `reports/godmode_static_postfix_qa_20260819.json` |
| JavaScript syntax | 🟢 Pass | Inline scripts for login, signup, dashboard, research detail, strategy wizard, contact, checkout, FAQ plus shared account/newsletter scripts pass `node --check` |
| Local backend/test suite | 🟢 Pass | `.venv/Scripts/python.exe -m pytest -q` → **53 passed** |
| Account invalid-login boundary | 🟢 Pass | Render `POST https://capohornlab-website.onrender.com/api/v1/auth/login` using a syntactically valid unregistered address returned **401** and `{"detail":"Invalid email or password"}`; no credentials persisted or account created |
| Public static live pages | 🟡 Partial | Earlier cache-busted sweep recorded HTTP 200 across 31 root/legacy URLs in `reports/godmode_qa_probe.json`; current local QA fixes are not yet deployed/read back |
| Live research quarantine/chart fixes | 🔴 Pending release | Production is known to expose stale research metadata/quarantined slug until reviewed archive extraction and cache-busted validation complete |

## Current-cycle QA — 2026-08-19

### Completed and verified locally

- **Authentication:** `assets/js/account-client.js` calls only backend `/auth/signup`, `/auth/login`, `/auth/me`, attaches a bearer token for authenticated calls, and contains no client-side credential acceptance branch. Live negative login returned 401. No real signup or email dispatch was attempted.
- **Dashboard:** root `dashboard.html` no longer displays fabricated NQ holdings or a non-functional Browse Data control. The data tab is an account-backed empty state until real completed-purchase holdings are returned. The legacy `pages/dashboard.html` is a canonical redirect to the root dashboard, eliminating its mock copy.
- **Research detail:** `reports/research_detail_qa.js` verified **13 studies**, **13 dual result sets**, all required Objective/Hypothesis/Methodology/Data/Results/Charts/Conclusions sections populated, and no placeholder matches. `reports/local_chart_qa.py` verified **91/91** configured chart PNG assets present locally.
- **Navigation/link repairs:** corrected the stale root detail Documentation fragment; replaced four root dashboard inert anchors with real dashboard/profile/logout routes; fixed legacy `pages/` Home and Documentation relative paths so all mirrors resolve to canonical root files; removed two obsolete admin TODO comments.
- **Regression:** static link/asset/placeholder audit passed with zero findings; `node --check` passed for all targeted inline/shared scripts; pytest passed 53/53; `git diff --check` passed.
- **Prepared payload:** `dist/godmode-full-qa-fixes-20260819.zip`, **218,534 bytes**, SHA-256 `fab4c10c6930eba07fde7d8b2dbee986c34ff2ce9a336532b69fc8315a6b95d3`. It contains exactly the 12 reviewed HTML files listed in `reports/godmode-full-qa-fixes-20260819-manifest.json`, with forward-slash archive entries.

### Explicitly not performed

- No signup with a deliverable email, contact submission, newsletter subscription, payment, order, DNS change, secret access, cache purge, or deletion.
- No Aruba upload/extract/overwrite occurred in this cycle. The prepared payload therefore remains **local only** and production cannot be called remediated.

### Specialist status

- `chl-20260819-0006` (Cratos static QA) and `chl-20260819-0007` (Odino live QA) were dispatched read-only. The provider failed before any tool call with HTTP 401. Result envelopes and verification-fail logs were stored under `D:/CapoHornLab/contracts/envelopes/` and `D:/CapoHornLab/contracts/logs/`; no specialist output was accepted.

## Next acceptance gates

1. Upload and extract only the reviewed archive in the Aruba hosting root; do not include unreviewed files.
2. Cache-busted live readback of every changed page, chart URL set, and research slug state.
3. Browser QA of deployed controls and navigation; leave contact/newsletter/signup in non-delivery validation mode unless Francesco explicitly authorizes real email.
4. Only pause God Mode after deployed-page, browser-interaction, and route checks are all verified.

### Current cron pass — 2026-08-19 (production read-back)

- **Live route sweep:** cache-busted GET verification returned HTTP 200 with a non-empty title across all 30 required root/legacy routes (`/`, public pages, five legal pages, and `pages/` mirrors).
- **Login browser test:** on `https://www.capohornlab.com/login.html?next=dashboard.html`, a syntactically valid unregistered address with a dummy password displayed **“Invalid email or password”** and remained on login; the direct Render API probe also returned 401. No email, signup, or payment was initiated.
- **Regression re-run:** `pytest -q` = **53 passed**; targeted inline JavaScript syntax validation = pass; `git diff --check` = pass. Research static verifier confirms **13/13** studies with all required sections and dual results; local chart verifier confirms **91/91** configured PNGs.
- **Release gate:** reviewed local archive remains pending Aruba upload/extract and cache-busted deployed-file read-back. No deployment has occurred during this pass yet.
