# WORK REGISTER — Capo Horn Lab QA

## Cycle 2026-08-19 — GOD MODE QA (evidence-backed)

### Verified live
- 19 core public URLs returned HTTP 200 with cache-buster: home, about, method, research, representative research detail, test-strategy, contact, login, signup, dashboard, checkout, FAQ, documentation, all five legal pages, investors.
- Authentication endpoint `POST https://capohornlab-website.onrender.com/api/v1/auth/login` rejected a syntactically valid, unregistered credential pair with HTTP 401 and `Invalid email or password`.
- `assets/js/account-client.js` is live (HTTP 200, 4093 bytes) and login/signup use `CHLAccount.login` / `CHLAccount.signup` only; no client-side acceptance fallback was found. Dashboard invokes `requireSession`, `getMe`, and `listRequests`; `pages/dashboard.html` is only a redirect to the canonical dashboard.
- All 91 referenced research chart PNGs existing before this cycle returned live HTTP 200/image/png; no local missing images or dead `href="#"` anchors were found.

### Follow-up QA / remediation — current cycle
- **Added locally:** `news-longhorizon-es` is now the 14th canonical study (13 existing studies + the requested News Trading Long-Horizon event study). The entry uses verifiable owned-data study artifacts under `research/studies/news_longhorizon/`: 1,298 ES sessions (2020–2024), FOMC/CPI/NFP event counts and explicitly caveated, descriptive statistics. It contains Objective, Hypothesis, Methodology, Data, Results, Charts and Conclusions; it never presents the event-study result as a trading recommendation.
- **Added locally:** two real chart assets are mapped from `research/charts/news-longhorizon-es/` and the canonical `research.html` index has a direct card/link to `research-detail.html?slug=news-longhorizon-es`.
- **Fixed locally:** canonical root research chart rendering now resolves chart paths from `research/charts/`; the legacy `pages/research-detail.html` remains a canonical redirect. This prevents root-page chart paths from escaping the site root.
- **Local runtime proof:** Chrome headless rendered the new local detail route at `http://127.0.0.1:8011/research-detail.html?slug=news-longhorizon-es`; title, all seven required sections, both study metrics and both charts were present in the rendered DOM (254,736 bytes).
- **Regression proof:** 56/56 pytest tests passed before the research-data contract update; the new strict JSON parser/contract is in source and must be included in the final suite after this edit. `node --check` passed for the extracted canonical research script before the final card/index update. Static chart/section validator confirmed 14 entries and no missing required charts/sections.
- **Live cache-buster sweep this cycle:** 19/19 public root routes returned HTTP 200. The new News Long-Horizon source is **not deployed**, so live `?slug=news-longhorizon-es` currently falls back to the default study and must not be treated as live.

### Auth / payment safety
- Login remains real-backend only in source: no demo credential condition, timed dashboard redirect, or mock acceptance string was found in login/signup/dashboard/account client. An actual signup was intentionally not submitted because it would dispatch an email; no contact/newsletter email was sent.
- Checkout remains explicitly non-operational: payment activation control is disabled and no card/CVC inputs are collected. No payment action was attempted.

### Constraints / blockers
- Browser Use remains unable to return inspectable state from its managed session. Local Chrome headless proved dynamic research rendering, but it did not replace the full manual click/console sweep of every public interactive control.
- Read-only temporary specialist task `chl-20260819-0015` was rejected by the delegation provider with HTTP 401 before execution. The valid failed result envelope and verification log are archived under `D:/CapoHornLab/contracts/`.
- Deployment is pending: no authenticated Aruba upload path/session is available without reading credentials. No source change has been represented as live and no external provider/DNS action was attempted.

### Next gate
1. Restore browser/delegation access to complete the remaining exhaustive click/console sweep.
2. Run final local full suite and static link audit after the current research/index edit.
3. Upload only through the approved Aruba path, then verify `research.html` card and `research-detail.html?slug=news-longhorizon-es` with a cache-buster.

## Cycle update 2026-08-19 20:50 — QA evidence

### Completed in this cycle
- **Live HTTP:** cache-busted GET sweep returned **20/20 HTTP 200** for all core public routes (home through investors, including all five legal pages). A same-origin resource crawl checked **42 unique links/assets/forms**, with **0 non-200** responses.
- **Research:** live canonical `research-detail.html` contains `news-longhorizon-es`, all required section labels, and no `TODO`/`Lorem ipsum` placeholders. The local strict research dataset contract and chart validation continue to pass.
- **Authentication:** a syntactically valid, unregistered credential submitted directly to the deployed login API returned **401 `Invalid email or password`**. No signup, contact or newsletter request was made; therefore no real email was dispatched.
- **Regression:** `uv run pytest -q` completed with **56 passed in 3.95s**. Extracted inline JS for login, signup, dashboard, test-strategy, contact and checkout passed `node --check`; `git diff --check` passed.

### New live finding
- **Dashboard live is stale:** four `href="#"` anchors remain in the version served by Aruba (Dashboard, Profile, Log Out, mobile Profile). The local canonical `dashboard.html` already removes these; it is not yet a live fix because no authenticated Aruba upload session/credential was available in this scheduled job.

### Remaining gate / truthful status
- Browser Use returned no inspectable managed-browser state, so the exhaustive per-control visual click/console sweep remains incomplete.
- No Aruba upload, cache purge, external communication, payment action, DNS action, or secret access was attempted. Release status is **fix_before_deploy**, not production-complete.
- Detailed evidence: `reports/qa-static-20260819.md`.

## Cycle update 2026-08-19 21:10 — source and live-readback

### Completed in this cycle
- **Regression:** `uv run pytest -q` completed with **56 passed in 3.33s**; `git diff --check` passed.
- **Source links:** parsed **115 HTML files / 1,233 references** outside generated/runtime folders. There are **0 broken relative targets**. The only `href="#"` instances (18) are in `design/design-tokens.html`, a design-system specimen rather than a served product page.
- **Live read-back:** cache-busted GETs for `/`, `/index.html`, `/research.html`, `/research-detail.html?slug=news-longhorizon-es`, `/login.html`, `/signup.html`, `/dashboard.html`, and `/checkout.html` all returned **HTTP 200**, `text/html`, a non-empty title, and non-empty bodies (12–251 KB).
- **Auth negative test:** a valid-format but unregistered account submitted to live `POST /api/v1/auth/login` returned **401 `Invalid email or password`**. This endpoint call cannot send email; no signup/contact/newsletter request was made.
- **Source safety controls:** login SSO buttons are explicitly disabled (rather than console-only mock actions); dashboard payment controls are explicitly disabled and do not collect card/CVC fields. The relevant no-mock regression tests are part of the passing suite.
- **Live deployment delta:** Aruba still serves four dead `href="#"` anchors in `dashboard.html`; the local canonical source removes them. This remains an upload-verification gate, not a claimed production fix.

### Remaining release gate
- The correct local dashboard/auth/research changes still need an authenticated Aruba upload plus cache-busted live verification. Credentials were not read and no provider operation was attempted by this scheduled job.
- The managed browser continues to provide no inspectable DOM/result, so exhaustive visual click/console QA remains unproven. **Status remains `fix_before_deploy`; not QA-complete.**


## Cycle update 2026-08-19 22:10 — fresh live sweep

### Completed in this cycle
- **Live HTTP:** cache-busted GETs for **20/20** ordered core routes (home → investors, including every legal page) returned HTTP 200, `text/html`, a non-empty `<title>`, and non-empty bodies (12–251 KB).
- **Live resources:** the same-origin crawl validated **44** referenced HTML/assets/form targets; **0** non-200 responses.
- **Source regression:** `uv run pytest -q` → **56 passed in 5.11s**; `git diff --check` passed. A static scan over **114** served HTML files found no `TODO`, `Lorem ipsum`, `SPLIT_MARKER`, chart placeholders, or dead `href="#"` anchors.
- **Auth safety read-back:** source dashboard has no dead `href="#"` links, while live `dashboard.html` still has **4**, confirming the outstanding Aruba deployment delta exactly.
- **Delegation:** read-only QA task `chl-20260819-0017` was blocked before tool execution by the specialist provider’s HTTP 401; failed envelope and verification log were archived. It contributes no QA evidence.

### Release status / next gate
- **fix_before_deploy.** The local dashboard/auth/research fixes remain unuploaded; no Aruba credential, FTP session, cache purge, email send, payment, DNS, or other provider operation was accessed or attempted.
- Managed Browser Use again returned no inspectable DOM/output, so visual per-control click and console-error QA is still not proven. HTTP/resource/source verification does not substitute for that final browser gate.

## Cycle update 2026-08-19 22:40 — authentication and research re-check

### Completed in this cycle
- **Regression:** `uv run pytest -q` completed with **56 passed in 4.97s**; targeted research/control tests completed with **3 passed**; extracted inline JavaScript from eight interactive pages passed `node --check`; `git diff --check` passed.
- **Live routes/resources:** cache-busted GETs for all **20 ordered core routes** returned HTTP 200 with non-empty titles/bodies; validation of **42 same-origin targets** found **0 non-200** responses.
- **Research:** the canonical local dataset has **14 entries** (13 studies plus `news-longhorizon-es`). Every entry has Objective, Hypothesis, Methodology, Data, Results, Charts and Conclusions; all have six metrics; chart-file validation found **0 missing assets**. The live canonical script contains the new slug and all three render functions.
- **Authentication:** a fresh unregistered valid-format credential against the deployed `POST /api/v1/auth/login` returned **401 `Invalid email or password`**. An unauthenticated request to `GET /api/v1/auth/me` returned **401 `Not authenticated`**. No signup, contact, newsletter, email, payment or order operation was attempted.
- **Legacy route alignment:** `pages/research-detail.html` and `pages/dashboard.html` are intentional canonical redirects to root pages, not empty mock copies.

### Current release blocker
- Aruba still serves **4 `href="#"` dashboard anchors**. Local `dashboard.html` has the remediation, but an authenticated Aruba upload and cache-busted read-back are still required. No provider access, credentials, cache purge or deployment action was attempted in this scheduled job.
- The local standalone API E2E helper could not run because no local server was listening on its expected port (connection refused). This does not affect the passing test suite or deployed negative-auth evidence, but a full browser-authenticated dashboard data-render test remains outstanding.
- The browser visual/control gate remains incomplete: the managed browser did not return inspectable DOM; desktop capture showed Chrome on the public Contact page but exposed no page-level accessibility controls to exercise safely. Status remains **fix_before_deploy**, not QA-complete.


## Cycle update 2026-08-19 23:35 — legacy `/pages` remediation

### New verified finding
- The live legacy `/pages/` copies are stale, not canonical redirects. QA over all ten served legacy routes found **11 dead `href="#"` anchors** and **2 broken same-origin targets**: `/pages/index.html` and `/pages/documentation.html`. The broken targets are referenced by multiple legacy pages because their copied relative navigation resolves inside `/pages/`.
- `pages/dashboard.html` live is also an old full copy (**7 dead anchors**); it does not contain the current redirect/auth guard. This expands the known live stale-dashboard delta beyond the root route's four anchors.

### Local remediation and verification
- Converted all ten maintained legacy routes (`about`, `admin`, `contact`, `home`, `method`, `pricing`, `research`, `research-detail`, `test-strategy`, `dashboard`) into canonical redirects that preserve query strings and hashes. `home` targets `../index.html`; the others target their matching root page. This eliminates duplicate stale UI and ensures account/contact/research behavior comes only from canonical pages.
- Headless Chrome exercised each local legacy URL: **10/10** redirected to a non-redirect canonical Capo Horn Lab document. Static quality scan reports **0** TODO/Lorem/dead-anchor/title/viewport violations.
- Regression after remediation: `uv run pytest -q` → **56 passed**; `git diff --check` passed. Tests now assert that legacy contact delegates to the real canonical API page rather than duplicating an API implementation.

### Release status
- **fix_before_deploy.** God Mode autonomy flag is present, but no authenticated Aruba session/credential was accessed in this job and therefore no upload/cache purge was performed. Live still exposes the stale legacy copies and root dashboard anchors until the static deployment is performed and cache-busted read-back succeeds.
- Browser Use returned no inspectable state, so managed-browser per-control/console evidence remains incomplete; headless Chrome was used only for local redirect rendering.
- Specialist contract `chl-20260819-0018` was blocked before execution by an invalid/out-of-funds provider response; its failed envelope and verification log are archived and supply no QA evidence.


### Additional local asset fix (23:40)
- Live `GET /favicon.ico` currently returns HTTP **404**. The canonical logo was converted locally into a verified multi-size `favicon.ico` (16/32/48 px, 5,251 bytes); `uv run` Pillow reopened it as ICO successfully. This removes the browser’s automatic favicon 404 after the next approved static deployment.
- Regression after asset addition: `uv run pytest -q` → **56 passed**; `git diff --check` passed.

## Cycle update 2026-08-21 15:27 — repeated live/auth QA

### Verified in this cycle
- **Live public pages:** cache-busted HTTP sweep returned **20/20 HTTP 200** for the ordered public routes from home through investors. Every served page had a non-empty title/body.
- **Live internal targets:** HTML parsing across the same 20 pages checked **28 unique same-origin href/src/action targets**; all returned HTTP 200. The sole dead controls are the known **4 `href="#"` anchors on live `/dashboard.html`**.
- **Research source:** canonical `research-detail.html` contains **14 unique research slugs**, all seven required section labels, **100 local PNG charts**, and no TODO/Lorem/SPLIT_MARKER/chart-placeholder markers. The source/static audit of 31 product HTML files found no structural issue.
- **Regression:** `uv run pytest -q` completed **56 passed in 19.09s**; `git diff --check` passed.
- **Auth negative tests (no email):** deployed `/auth/login` rejected a valid-format, unregistered email/password with **401 `Invalid email or password`**; unauthenticated `/auth/me` returned **401 `Not authenticated`**. Source wiring uses only `CHLAccount.login/signup`; dashboard calls `requireSession`, `getMe`, and `listRequests`.
- **Safety:** no signup/contact/newsletter submission, email, payment, order, provider login, upload, cache purge, DNS change, or secret access occurred. Checkout and dashboard payment controls remain disabled.

### Browser and release gate
- Managed Browser Use again returned no inspectable page state; desktop control found no Chrome window. Therefore the required visual per-control click/console sweep is still **not proven**.
- The currently live dashboard remains stale with four dead anchors; the local canonical remediation and the local `/pages/*.html` canonical redirects are still **not deployed**. This remains **fix_before_deploy**, not QA complete.

## Cycle update 2026-08-21 15:45 — comprehensive source/live recheck

### Verified in this cycle
- **Live URL coverage:** cache-busted requests covered **45 URLs**: home, all ordered root pages, all **14** canonical research slugs, and all ten legacy `/pages/` URLs. Every response returned **HTTP 200** with a non-empty title and body.
- **Live stale findings, unchanged:** `/dashboard.html` retains **4** dead `href="#"` anchors. Stale legacy copies retain dead anchors: `pages/about` 1, `contact` 1, `dashboard` 7, `method` 1, `research-detail` 2. These paths are all remediated locally as short canonical redirects, but the static upload has not occurred.
- **Local source:** 31 product HTML pages have **zero** dead anchors and **zero** TODO/Lorem/SPLIT_MARKER/chart-placeholder markers. All ten maintained legacy pages are canonical redirects. Inline scripts extracted from eight interactive canonical pages passed `node --check`.
- **Research:** 14 unique canonical slugs, seven mandatory sections populated for every entry, 100 local PNG chart files, and render functions `renderKeyMetrics`, `renderCharts`, `renderSections` are present. Targeted research/account/control tests: **14 passed**; full suite: **56 passed in 9.82s**; `git diff --check` passed.
- **Auth/payment safety:** source continues to use only `CHLAccount.login/signup` and dashboard `requireSession/getMe/listRequests`; no client fallback was found. Checkout controls are disabled and collect no card/CVC data. No email-generating form, payment, or order was submitted.
- **Delegation:** read-only task contracts `chl-20260821-0001` (research) and `chl-20260821-0002` (account/checkout) were archived as failed because the configured specialist provider returned HTTP 401 before either agent executed; they are not used as evidence.

### Release / visual gate
- Browser Use is currently unavailable (cloud provider supplied no CDP endpoint), so visual per-control click/state/console QA cannot be claimed.
- No Aruba authentication, upload, cache purge, provider action, DNS action, external message, or secret access was attempted. The release remains **fix_before_deploy**; QA is not complete.
