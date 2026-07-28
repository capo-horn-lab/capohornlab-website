# QA Stress Test Report — Capo Horn Lab

**Date**: 2026-07-28
**Agent**: Cratos (QA & Reliability)
**Base URL**: `http://127.0.0.1:8000`
**Total pages discovered**: 34 (24 root + 10 in `pages/`)

---

## 1. Page Status Overview

| Metric | Value |
|--------|-------|
| Pages tested | **34** |
| ✅ Passed (200 OK) | **34** |
| ❌ Failed | **0** |

All 34 pages return HTTP 200. Zero failures.

### All Tested Pages

| # | Page | Status |
|---|------|--------|
| 1 | `/` | ✅ 200 |
| 2 | `/about.html` | ✅ 200 |
| 3 | `/admin.html` | ✅ 200 |
| 4 | `/checkout.html` | ✅ 200 |
| 5 | `/contact.html` | ✅ 200 |
| 6 | `/cookie-policy.html` | ✅ 200 |
| 7 | `/crypto-cards.html` | ✅ 200 |
| 8 | `/crypto-price-cards.html` | ✅ 200 |
| 9 | `/crypto-prices.html` | ✅ 200 |
| 10 | `/dashboard.html` | ✅ 200 |
| 11 | `/disclaimer.html` | ✅ 200 |
| 12 | `/documentation.html` | ✅ 200 |
| 13 | `/faq.html` | ✅ 200 |
| 14 | `/investors.html` | ✅ 200 |
| 15 | `/login.html` | ✅ 200 |
| 16 | `/method.html` | ✅ 200 |
| 17 | `/pricing.html` | ✅ 200 |
| 18 | `/privacy-policy.html` | ✅ 200 |
| 19 | `/refund-policy.html` | ✅ 200 |
| 20 | `/research.html` | ✅ 200 |
| 21 | `/research-detail.html` | ✅ 200 |
| 22 | `/signup.html` | ✅ 200 |
| 23 | `/terms-of-service.html` | ✅ 200 |
| 24 | `/test-strategy.html` | ✅ 200 |
| 25 | `/pages/home.html` | ✅ 200 |
| 26 | `/pages/about.html` | ✅ 200 |
| 27 | `/pages/admin.html` | ✅ 200 |
| 28 | `/pages/contact.html` | ✅ 200 |
| 29 | `/pages/dashboard.html` | ✅ 200 |
| 30 | `/pages/method.html` | ✅ 200 |
| 31 | `/pages/pricing.html` | ✅ 200 |
| 32 | `/pages/research.html` | ✅ 200 |
| 33 | `/pages/research-detail.html` | ✅ 200 |
| 34 | `/pages/test-strategy.html` | ✅ 200 |

---

## 2. Link Analysis

| Metric | Value |
|--------|-------|
| Total unique href URLs found | **67** |
| ✅ Internal links working | **39** |
| ❌ Broken internal links | **3** |
| External links (found, not tested) | **12** |
| Same-page anchor links (intra-page only) | **~80+** |

### 2.1 Broken Internal Links ⛔

Three URLs resolve to **404 Not Found**. These are referenced from real navigation/footer elements and will produce broken user experiences.

| URL | HTTP Status | Referenced From |
|-----|-------------|-----------------|
| `cookies.html` | 404 | `documentation.html` (footer), `faq.html` (body + footer), `investors.html` (footer) |
| `home.html` | 404 | ALL `pages/*.html` files (nav Home link), `research-detail.html` (nav Home link) |
| `terms.html` | 404 | `documentation.html` (footer), `faq.html` (footer), `investors.html` (footer) |

**Root causes:**
- `cookies.html` → should be `cookie-policy.html`
- `home.html` → should be `index.html` or `/`
- `terms.html` → should be `terms-of-service.html`

### 2.2 `href="#"` Placeholders ⚠️

Genuine **dead placeholders** (links that lead nowhere even with JS enabled):

| Page | Tag/Context | Issue |
|------|-------------|-------|
| `/about.html`, `/contact.html`, `/method.html` | Newsletter "Privacy Policy" | `href="#"` should link to `/privacy-policy.html` |
| `/pages/about.html`, `/pages/contact.html`, `/pages/method.html`, `/pages/research-detail.html` | Newsletter "Privacy Policy" | `href="#"` should link to `/privacy-policy.html` |
| `/research-detail.html` | Newsletter "Privacy Policy" | `href="#"` should link to `/privacy-policy.html` |
| `/dashboard.html`, `/pages/dashboard.html` | Nav links: Dashboard, Profile, Log Out | `href="#"` with onclick handlers (SPA-like, breaks if JS fails) |
| `/pages/about.html`, `/pages/contact.html`, `/pages/home.html`, `/pages/method.html`, `/pages/pricing.html`, `/pages/research.html`, `/pages/research-detail.html`, `/pages/test-strategy.html`, `/research-detail.html` | Footer LEGAL section | `href="#docs"`, `href="#faq"`, `href="#privacy"`, `href="#terms"`, `href="#cookies"`, `href="#disclaimer"` — anchor only, should be full page URLs |

**Note**: All `pages/*.html` files use fragment-only links (`#privacy`, `#terms`, etc.) in their footer LEGAL section instead of linking to the actual pages like the root-level HTML files do.

**Legitimate same-page anchors** are NOT included in the above — cookie-policy, disclaimer, documentation, terms-of-service, privacy-policy, refund-policy all have valid intra-page anchor navigation to sections within the same document.

### 2.3 External Links (not tested)

- `https://github.com/capohornlab`
- `https://twitter.com/capohornlab`
- `https://linkedin.com/company/capohornlab`
- Google Fonts CDN links (fonts.googleapis.com, fonts.gstatic.com)
- Google Privacy / Ads policies
- EU consumer ODR platform
- Browser help pages (Chrome, Safari, Firefox, Edge)
- Facebook cookies policy

---

## 3. HTML Quality Checks

| Metric | Value |
|--------|-------|
| HTML structural issues | **0** |
| JavaScript console errors | **0** (tested across all interactive pages) |

**All pages pass:**
- ✅ `<!DOCTYPE html>` declaration present
- ✅ UTF-8 charset declared
- ✅ `<title>` present and non-empty
- ✅ Viewport meta tag present
- ✅ No unclosed HTML tags detected via parser scan
- ✅ Zero JavaScript runtime errors on root, about, dashboard, admin, research-detail, login, signup, contact pages

---

## 4. Issues Summary

### ❌ BLOCKER — 3 Broken Internal Links
Navigation/footer links to `cookies.html`, `home.html`, and `terms.html` return 404. These affect:
- **5 root-level pages** (documentation.html, faq.html, investors.html, research-detail.html)
- **All 10 pages/ files** (nav "Home" link is broken)
- Users clicking these will hit a dead end.

### ⚠️ CRITICAL — Footer Fragment Anchors in `pages/*`
The LEGAL footer section in ALL `pages/*.html` files uses `href="#privacy"`, `href="#terms"`, etc. instead of proper page URLs (`privacy-policy.html`, `terms-of-service.html`). The root-level HTML files do this correctly. This appears to be a copy-paste issue from the design template.

### ⚠️ WARNING — Newsletter "Privacy Policy" Placeholder
7 pages link the newsletter Privacy Policy text to `href="#"` instead of `/privacy-policy.html`.

### 📝 MINOR — Dashboard SPA-style Nav
Dashboard navigation uses `href="#"` with onclick JavaScript handlers. Works when JS is enabled, but breaks gracefully if JS fails. Acceptable pattern for dashboard UI.

---

## 5. Recommendation

### ⛔ **fix_before_deploy**

**Reason:** 3 broken internal links + 8+ pages with footer fragment anchors instead of real URLs. These are structural navigation issues that directly impact user experience.

### Required fixes before deploy:
1. **`cookies.html` → `cookie-policy.html`** — fix in `documentation.html`, `faq.html`, `investors.html`
2. **`home.html` → `index.html`** — fix in all `pages/*.html` navigation
3. **`terms.html` → `terms-of-service.html`** — fix in `documentation.html`, `faq.html`, `investors.html`
4. **Footer fragment anchors** in `pages/*.html` — replace `#docs`→`documentation.html`, `#faq`→`faq.html`, `#privacy`→`privacy-policy.html`, `#terms`→`terms-of-service.html`, `#cookies`→`cookie-policy.html`, `#disclaimer`→`disclaimer.html`
5. **Newsletter Privacy Policy links** — replace `href="#"` with `href="privacy-policy.html"` in about.html, contact.html, method.html, research-detail.html and their pages/* counterparts

### Estimated effort: ~30 min (find-and-replace in ~18 HTML files)

---

*Report generated by Cratos — QA & Reliability Agent*
