# God Mode QA — 2026-08-24

## Scope and evidence

- Live origin core route HEAD checks: 18/18 routes returned HTTP 200 with a cache-buster.
- Safe live authentication negative test: `POST https://capohornlab-website.onrender.com/api/v1/auth/login` using a non-existent, syntactically valid address returned `401 {"detail":"Invalid email or password"}`.
- Local test suite: `56 passed`.
- Static internal file and fragment audit: 116 HTML pages checked, 0 unresolved local references/anchors.

## Corrected locally

1. Restored the index newsletter form removed by the Observatory home replacement. It uses `assets/js/newsletter-client.js` and the real `/newsletter/subscribe` endpoint; it never displays success before the API confirms it.
2. Repaired five dead fragments: documentation now points to `documentation.html`, FAQ to `faq.html`.
3. Audited the embedded public research dataset. Two entries were incomplete and had no PNG chart assets:
   - `quantum-computing-quant-finance`
   - `systematic-research-methodology`

   They were removed only from the public renderer; no source/research data was deleted. The public detail renderer now exposes 14 complete entries (13 research entries plus `news-longhorizon-es`). Every one has Objective, Hypothesis, Methodology, Data, Results, Charts and Conclusions, six metrics, and local chart PNG assets.

## Unresolved / release gate

- No safe, non-secret deployment helper exists in the tracked working tree, so this cycle did **not** perform an Aruba upload. Local fixes are verified but are not claimed live.
- BrowserUse has no CDP endpoint in this cron runtime. A background Chrome capture showed the user’s existing personal browsing tab, so it was not reused for QA.
- Real contact/signup/newsletter email dispatch was intentionally not tested: it would cause an external email send and requires Francesco’s explicit confirmation.
- `pages/*.html` are canonical redirect stubs; all 12 were confirmed to delegate to their root page rather than preserve mock duplicates.
