# UI Migration Log — Observatory Design System

Scope: assessment + approved migration pass. No deploy change. No commit.

Decision inputs:
- Deploy unchanged.
- Use shared CSS import: `design/observatory-tokens.css` linked by migrated root pages.
- `crypto-*.html` are experiments: skipped and flagged for Francesco.
- `pages/research-detail.html` is non-canonical: keep as compatibility redirect to root `research-detail.html`, but style fallback with Observatory tokens.

Design source of truth:
- `design/observatory-tokens.css`
- `design/capo-horn-observatory-concept-v2-unified.html`
- `design/observatory-components.html`

## Migration executed

| Page | Result | Notes |
|---|---|---|
| `admin.html` | migrated | Added shared Observatory token import; switched font import to DM Sans / DM Mono / Playfair Display; added Observatory override layer mapping legacy admin variables to Observatory tokens. Existing admin layout preserved. |
| `pages/research-detail.html` | migrated as redirect | Confirmed non-canonical compatibility route; kept redirect to `../research-detail.html` preserving query/hash; added Observatory token import and styled fallback card. |
| `checkout.html` | consolidated | Added shared `design/observatory-tokens.css` import. Existing layout preserved. |
| `investors.html` | consolidated | Added shared `design/observatory-tokens.css` import. Existing layout preserved. |
| `privacy-policy.html` | consolidated | Added shared `design/observatory-tokens.css` import. Existing layout preserved. |
| `terms-of-service.html` | consolidated | Added shared `design/observatory-tokens.css` import. Existing layout preserved. |
| `refund-policy.html` | consolidated | Added shared `design/observatory-tokens.css` import. Existing layout preserved. |
| `cookie-policy.html` | consolidated | Added shared `design/observatory-tokens.css` import. Existing layout preserved. |
| `disclaimer.html` | consolidated | Added shared `design/observatory-tokens.css` import. Existing layout preserved. |

## Skipped by decision

| Page | Status | Reason |
|---|---|---|
| `crypto-prices.html` | skipped | Experiment / utility page. Flag for Francesco instead of migrating now. |
| `crypto-price-cards.html` | skipped | Experiment / utility page. Flag for Francesco instead of migrating now. |
| `crypto-cards.html` | skipped | Experiment / utility page. Flag for Francesco instead of migrating now. |

## Current page assessment after migration

### Aligned / already using Observatory markers

- `index.html`
- `research.html`
- `research-detail.html`
- `method.html`
- `pricing.html`
- `test-strategy.html`
- `documentation.html`
- `faq.html`
- `login.html`
- `signup.html`
- `dashboard.html`
- `about.html`
- `contact.html`

### Migrated/consolidated in this pass

- `admin.html`
- `pages/research-detail.html`
- `checkout.html`
- `investors.html`
- `privacy-policy.html`
- `terms-of-service.html`
- `refund-policy.html`
- `cookie-policy.html`
- `disclaimer.html`

### Compatibility redirects

Most `pages/*.html` files are redirect stubs rather than canonical visual pages:
- `pages/index.html`
- `pages/home.html`
- `pages/about.html`
- `pages/contact.html`
- `pages/method.html`
- `pages/pricing.html`
- `pages/research.html`
- `pages/documentation.html`
- `pages/dashboard.html`
- `pages/admin.html`
- `pages/test-strategy.html`

`pages/research-detail.html` is now also treated as compatibility redirect, with Observatory fallback styling.

## Verification performed

Local static verification only, per instruction. No npm, no network, no deploy.

Checked files for:
- presence of `observatory-tokens.css` import;
- DM typography import/availability;
- redirect preservation for `pages/research-detail.html`;
- git status to confirm changed files and no commit.

Verification result:
- `admin.html`: `observatory-tokens.css` present; DM typography present; Observatory override present.
- `pages/research-detail.html`: `observatory-tokens.css` present; DM typography present; redirect present.
- `checkout.html`: `observatory-tokens.css` present.
- `investors.html`: `observatory-tokens.css` present.
- `privacy-policy.html`: `observatory-tokens.css` present.
- `terms-of-service.html`: `observatory-tokens.css` present.
- `refund-policy.html`: `observatory-tokens.css` present.
- `cookie-policy.html`: `observatory-tokens.css` present.
- `disclaimer.html`: `observatory-tokens.css` present.

## Problems / residual risks

- `admin.html` was migrated conservatively with a CSS override layer; it still contains a large legacy inline stylesheet. A later cleanup pass can reduce duplication once visual QA is allowed.
- Consolidated legal/checkout/investor pages now link shared tokens but still retain inline legacy token definitions for compatibility. A later refactor can remove duplicate token blocks after browser QA.
- Crypto experiment pages remain unmigrated by explicit decision and should be either archived, hidden, or separately approved for public migration.
- No visual/browser QA was run in this pass.

## Git status note

This pass intentionally does not commit. Expected changed files from this pass:
- `admin.html`
- `checkout.html`
- `cookie-policy.html`
- `disclaimer.html`
- `investors.html`
- `pages/research-detail.html`
- `privacy-policy.html`
- `refund-policy.html`
- `terms-of-service.html`
- `reports/UI_MIGRATION_LOG.md`

Pre-existing unrelated changes observed before this pass remain untouched:
- `research/backtest_engine.py`
- `tests/test_backtest_execution_assumptions.py`
- `reports/PC_HANDOFF_COMPLETE_2026-08-25.md`
