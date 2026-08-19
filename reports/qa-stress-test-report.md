# QA Stress Test Report — Capo Horn Lab (Live)

**Date (UTC):** 2026-08-19 03:33:17
**Base URL:** `https://www.capohornlab.com/`
**Sitemap:** HTTP 200

## 1. Page Status Overview

| Pages tested | 14 |
| ✅ Passed | 14 |
| ❌ Failed | 0 |

| Path | HTTP | Bytes |
|---|---:|---:|
| `/` | 200 | 60917 |
| `/about.html` | 200 | 49505 |
| `/admin.html` | 200 | 139791 |
| `/checkout.html` | 200 | 12283 |
| `/contact.html` | 200 | 52042 |
| `/dashboard.html` | 200 | 63207 |
| `/index.html` | 200 | 60917 |
| `/login.html` | 200 | 36513 |
| `/method.html` | 200 | 53422 |
| `/pricing.html` | 200 | 54979 |
| `/research-detail.html` | 200 | 250863 |
| `/research.html` | 200 | 62121 |
| `/signup.html` | 200 | 25102 |
| `/test-strategy.html` | 200 | 97885 |

### Default document
- `/`: HTTP 200, title **Capo Horn Lab — Beyond the Market Edge**.

## 2. Link Analysis

| Internal targets | 21 |
| Internal OK | 20 |
| Broken internal | 1 |
| Dead placeholders | 4 |
| Unresolved anchors | 1 |
| External URLs | 3 |

### Broken Internal Links

- `capo.horn.lab@gmail.com` → HTTP 404; referenced from /contact.html

## 3. HTML Quality

No missing DOCTYPE/UTF-8/viewport/title finding.

## 4. Research Publication Governance

- Quarantined slug `news-event-long-horizon-es`: **FAIL — exposed on /research.html, /research-detail.html**.

## 5. Recommendation

- **fix_before_deploy** — remove stale preliminary research from production before release approval.
