# Odino External Link Verification Report

**Date:** 2026-07-28 18:55:20
**Site:** Capo Horn Lab Website
**Source:** `D:/CapoHornLab/projects/capohornlab-website/`

## Summary

| Status | Count |
|--------|-------|
| ✅ OK | 18 |
| ⚠️ INFO (not a bug) | 2 |
| ❌ FAIL | 3 |
| **Total** | **25** |

## Results by Category

### 📦 CDN & Google Fonts

| URL | Status | Detail | Pages |
|-----|--------|--------|-------|
| `https://fonts.googleapis.com` | ⚠️ INFO | 404 (bare preconnect URL — expected) | 33 pages |
| `https://fonts.gstatic.com` | ⚠️ INFO | 404 (bare preconnect URL — expected) | 33 pages |
| `https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap` | ✅ OK | 200 | 32 pages (all main site pages) |
| `https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap` | ✅ OK | 200 | `assets/campaigns/funnel.html` |
| `https://cdn.plot.ly/plotly-3.7.0.min.js` | ✅ OK | 200 | 21 research chart pages |
| `https://js.stripe.com/v3/` | ✅ OK | 200 | `checkout.html` |

### 🔗 Social Links

| URL | Status | Detail | Pages |
|-----|--------|--------|-------|
| `https://github.com/capohornlab` | ❌ FAIL | 404 — account/org doesn't exist | 26 pages |
| `https://twitter.com/capohornlab` | ❌ FAIL | 404 — handle doesn't exist | 26 pages |
| `https://linkedin.com/company/capohornlab` | ✅ OK | 200 | 26 pages |
| `https://www.facebook.com/policies/cookies` | ✅ OK | 200 | `cookie-policy.html` |

### 📧 Mailto Links (all well-formatted ✅)

| URL | Status | Detail | Pages |
|-----|--------|--------|-------|
| `mailto:capo.horn.lab@gmail.com` | ✅ OK | Valid format | `contact.html`, `pages/contact.html` |
| `mailto:dpo@capohornlab.com` | ✅ OK | Valid format | `cookie-policy.html`, `privacy-policy.html` |
| `mailto:privacy@capohornlab.com` | ✅ OK | Valid format | `cookie-policy.html`, `privacy-policy.html` |
| `mailto:legal@capohornlab.com` | ✅ OK | Valid format | `disclaimer.html`, `terms-of-service.html` |
| `mailto:institutional@capohornlab.com` | ✅ OK | Valid format | `investors.html` |
| `mailto:billing@capohornlab.com` | ✅ OK | Valid format | `refund-policy.html` |
| `mailto:support@capohornlab.com` | ✅ OK | Valid format | `refund-policy.html`, `terms-of-service.html` |

### 🌐 Other External Links

| URL | Status | Detail | Pages |
|-----|--------|--------|-------|
| `https://policies.google.com/privacy` | ✅ OK | 200 | `cookie-policy.html` |
| `https://policies.google.com/technologies/ads` | ✅ OK | 200 | `cookie-policy.html` |
| `https://support.google.com/chrome/answer/95647` | ✅ OK | 200 | `cookie-policy.html` |
| `https://support.mozilla.org/en-US/kb/enable-and-disable-cookies-website-preferences` | ✅ OK | 200 | `cookie-policy.html` |
| `https://support.apple.com/guide/safari/manage-cookies-and-website-data-sfri11471/mac` | ✅ OK | 200 | `cookie-policy.html` |
| `https://support.microsoft.com/en-us/microsoft-edge/delete-cookies-in-microsoft-edge-63947406-40ac-c3b8-57b9-2a946a29ae09` | ✅ OK | 200 | `cookie-policy.html` |
| `https://ec.europa.eu/consumers/odr` | ✅ OK | 200 | `terms-of-service.html` |
| `https://ec.europa.eu/info/law/law-topic/consumers/consumer-contract-law/standard-withdrawal-form_en` | ❌ FAIL | 404 — EU changed URL structure | `refund-policy.html` |

## ❌ Real Failures (action required)

### 1. `https://github.com/capohornlab` — 404
- **Found in:** 26 pages (all pages with footer/header)
- **Issue:** GitHub organization `capohornlab` does not exist
- **Action:** Create the GitHub org, or update the URL if it should point elsewhere

### 2. `https://twitter.com/capohornlab` — 404
- **Found in:** 26 pages (all pages with footer/header)
- **Issue:** Twitter/X handle `@capohornlab` is not registered
- **Action:** Create the Twitter/X account, or update the link

### 3. `https://ec.europa.eu/info/law/law-topic/consumers/consumer-contract-law/standard-withdrawal-form_en` — 404
- **Found in:** `refund-policy.html`
- **Issue:** European Commission restructured their site; this URL no longer works
- **Action:** Search for the new EU standard withdrawal form URL and update

## ⚠️ Informational (not bugs)

### Google Fonts `preconnect` URLs — 404 on direct fetch
- `https://fonts.googleapis.com` and `https://fonts.gstatic.com` are used as `<link rel="preconnect">` hints.
- These are origin-level URLs for DNS/TCP/TLS pre-warming — they are NOT fetched as resources.
- A 404 on HEAD/GET is **expected and harmless**. The actual font CSS (`/css2?family=...`) and font files (`fonts.gstatic.com/s/inter/...`) work correctly.

## ✅ Verified Working

| Resource | Type |
|----------|------|
| Google Fonts CSS (Inter + JetBrains Mono) | ✅ Returns valid CSS with @font-face rules |
| fonts.gstatic.com woff2 files | ✅ Referenced inside the CSS from Google's CDN |
| js.stripe.com/v3 | ✅ Stripe.js payment library |
| cdn.plot.ly/plotly-3.7.0.min.js | ✅ Plotly charting library |
| linkedin.com/company/capohornlab | ✅ LinkedIn company page exists |
| All 7 mailto: email addresses | ✅ Well-formed, valid email format |
| Facebook cookie policy | ✅ Reachable |
| Google privacy/ad policies | ✅ Reachable |
| 4 browser cookie help pages | ✅ All reachable (Chrome, Firefox, Safari, Edge) |
| EU ODR platform | ✅ Reachable |

---
*Report generated by Odino Agent on 2026-07-28 18:55:20*
*Reviewed and annotated for false positives on Google Fonts preconnect URLs.*
