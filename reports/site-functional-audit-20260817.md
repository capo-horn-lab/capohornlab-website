# Capo Horn Lab — Functional Audit
Date: 2026-08-17
Scope: local working copy `D:/CapoHornLab/projects/capohornlab-website`

## Executive verdict

The static pages render and the local FastAPI/PostgreSQL/Redis stack is alive, but the product is not yet functionally complete. Authentication is the strongest implemented path. Contact, newsletter, strategy submission, dashboard data, admin mutations, transactional email, password reset, and payment are not production-connected.

This report is based on source inspection plus executed checks. No live deployment was modified.

## Verified green

- Docker services: API up, PostgreSQL healthy, Redis healthy.
- Alembic database revision: `0003 (head)`.
- `/health`: HTTP 200.
- Full Python suite: `22 passed`.
- Inline JavaScript syntax: 0 errors when extracted with a script-aware regex.
- Authentication frontend wiring exists in `assets/js/account-client.js`.
- Signup/login/me/refresh were previously verified against the local API with real PostgreSQL state.
- Refresh token is HttpOnly and is not returned in the login JSON.
- Database and Redis Docker ports bind to `127.0.0.1`.
- Checkout correctly refuses to pretend that payment succeeded while the provider is not configured.
- Research JSON, local pilot results, and research charts exist locally.

## Confirmed red / incomplete

### 1. Contact support form — not connected

`contact.html` and `pages/contact.html` validate the form, wait 1.5 seconds, then show `Message Sent`. There is no `fetch()`, form action, API endpoint, database model, or email dispatch. A visitor can lose a message while seeing a false success confirmation.

Required implementation:

1. Add `ContactMessage` database model and Alembic migration.
2. Add `POST /api/v1/contact` with Pydantic validation and Redis rate limiting.
3. Store the message before sending email.
4. Send notification to `support@capohornlab.com` (or the confirmed support mailbox).
5. Send an acknowledgement to the visitor.
6. Replace the timeout in both contact pages with a real `fetch()` call and success/error states.
7. Add anti-spam protection: rate limit, honeypot, max lengths, and optionally Cloudflare Turnstile.
8. Add a support inbox/admin view or a reliable mailbox workflow.

### 2. Newsletter — every public form is currently cosmetic

The public pages use an inline `onsubmit` that only changes the button text to `Subscribed!`. None of the public forms call `/api/v1/newsletter`.

The backend newsletter routes exist and the migration exists, but `app/services/email.py` is still a stub. It logs `[EMAIL STUB]` and returns success.

Required implementation:

- Add one shared `assets/js/newsletter-client.js`.
- Post `{email, name?, source?}` to `/api/v1/newsletter/subscribe`.
- Display “Check your inbox to confirm” only after the API returns success.
- Handle duplicate/429/server errors visibly.
- Verify and unsubscribe through the backend URLs.
- Configure real transactional email before announcing the feature.

### 3. Transactional email — not real

`app/services/email.py` has `self._enabled = False`; `_send()` logs the message and returns `True`. `_send_via_resend()` raises `NotImplementedError` and is never enabled.

Signup calls `send_verification_code()`, but that function only stores a six-digit code in process memory. It does not send it.

Password reset behaves the same way: codes are process-memory only and no email is sent. Restarting the API loses the codes. Multiple API workers would not share them.

Required implementation:

- Use Resend, Postmark, Mailgun, or SMTP through a transactional provider.
- Make sending provider-backed and fail visibly if production email is unavailable.
- Store verification/reset challenges in Redis or PostgreSQL with TTL, hashed code values, attempt limits, and one-time consumption.
- Add separate templates for verification, password reset, contact acknowledgement, status changes, and newsletter confirmation.
- Never log full HTML containing personal data or reset links in production.

### 4. Strategy wizard — not connected to the request API

`test-strategy.html` contains the seven-step UI and client-side file list, but:

- no `fetch()` call exists;
- no `/api/v1/requests` call exists;
- uploaded files remain only in browser memory;
- `submitStrategy()` redirects to `checkout.html` with tier, months, price, and discount in the URL;
- the price is client-controlled and cannot be trusted;
- no StrategyRequest is created before checkout;
- `?auth=1` only reveals the wizard and does not enforce a real session;
- the button text is `Submit & Pay`, although payment and submission are not implemented.

Required flow:

1. Require a valid access token before showing submission.
2. Create the request server-side with `POST /api/v1/requests`.
3. Upload attachments to `POST /api/v1/requests/{id}/attachments` using multipart/form-data.
4. Server calculates the price from a product/tier catalog; never trust `price` in a query string.
5. Create a hosted checkout session server-side.
6. Activate data/backtest access only after a signed payment webhook.
7. Persist the request ID and show it in the dashboard.

### 5. Dashboard — authentication gate exists, data integration does not

The dashboard calls `/auth/me`, but does not call `/api/v1/requests`. It renders an empty-state/static presentation and contains a change-password function labelled `Mock success` that does not call an API.

Required implementation:

- Load `/api/v1/requests` after `/auth/me`.
- Render actual statuses, dates, request IDs, attachments, and result links.
- Add request detail loading from `/api/v1/requests/{id}`.
- Add real change-password endpoint and frontend handling.
- Add refresh-token recovery when the access token expires.
- Remove or clearly label all static example rows and demo metrics.

### 6. Admin panel — mostly presentation/demo actions

The backend has admin routes, but `admin.html` still contains many `backend pending`, `mock`, and toast-only actions, including status changes, notes, clarification, research editing/publication, newsletter campaigns, client actions, and file upload.

Required implementation:

- Require admin role through the API, not just by opening `admin.html`.
- Replace toast-only actions with authenticated API calls.
- Reload state from the backend after every mutation.
- Add CSRF strategy if cookie-authenticated mutations are introduced.
- Add audit log reads for status changes and internal notes.
- Make research publication server-backed or explicitly keep it as a local content-generation tool.

### 7. Checkout/payment — intentionally disabled, not production-ready

The current page correctly says the payment provider is not configured and disables the button. That is safe, but it is not a working purchase flow.

The current URL accepts `price` from the browser. This is acceptable only for display; it must never determine the amount charged or entitlements.

Required implementation:

- Choose one provider: bank-hosted POS, Stripe Checkout, Mollie, or another PCI-compliant hosted flow.
- Create checkout sessions on the backend from a server-side price/product catalog.
- Receive and verify signed webhooks.
- Persist orders, payment status, refunds, and entitlements.
- Make success/cancel pages informational only; do not grant access from query parameters.
- Keep card/CVC fields out of this site unless using a provider-hosted/PCI-compliant component.

### 8. Links and duplicate page tree

The root pages are mostly self-contained. The legacy `pages/` copy contains broken relative links such as `index.html` and `documentation.html` because those files are one directory above. There are also `href="#"` placeholders in dashboard/legacy pages.

The audit found 24 missing local references under `pages/` and multiple hash-only placeholders. The audit intentionally treats query strings correctly; links with `?auth=1` are not themselves missing files.

Required decision:

- Choose one canonical public tree, preferably root pages.
- Either remove/archive `pages/` or repair every relative path with `../`.
- Run link checks against the actual deployment root, not both trees accidentally.

### 9. Security/configuration

Good local guards exist, but production still requires:

- non-placeholder `SECRET_KEY`, `JWT_ACCESS_SECRET`, `JWT_REFRESH_SECRET`;
- `APP_ENV=production`, `DEBUG=false`;
- exact production `ALLOWED_ORIGINS`;
- HTTPS and Secure cookies;
- real domain and email provider configuration;
- external upload storage or durable mounted storage;
- backups and restore testing;
- monitoring and error alerting;
- removal of development `/docs` and `/redoc` exposure;
- fresh PostgreSQL migration test before deployment.

## How to connect the support email correctly

Recommended architecture:

1. Create a domain mailbox such as `support@capohornlab.com` for human support.
2. Create a transactional sender such as `noreply@capohornlab.com` or `mail@capohornlab.com` through Resend/Postmark/Mailgun.
3. Verify the domain in the provider dashboard.
4. Add the provider's DNS records:
   - SPF TXT
   - DKIM TXT/CNAME
   - DMARC TXT, initially monitoring policy (`p=none`), then tighten after validation
5. Keep `support@...` as the Reply-To destination and use the verified sender as From.
6. Add server environment variables, never HTML or Git:

```env
APP_ENV=production
DEBUG=false
FRONTEND_URL=https://capohornlab.com
ALLOWED_ORIGINS=https://capohornlab.com
RESEND_API_KEY=<secret stored in deployment secret manager>
NEWSLETTER_FROM_EMAIL=mail@capohornlab.com
NEWSLETTER_FROM_NAME=Capo Horn Lab
SUPPORT_EMAIL=support@capohornlab.com
SUPPORT_FROM_EMAIL=mail@capohornlab.com
```

7. Implement `POST /api/v1/contact` with:
   - `name`, `email`, `subject`, `message` validation;
   - max lengths;
   - rate limiting;
   - honeypot/Turnstile;
   - database persistence;
   - notification to support;
   - acknowledgement to the visitor.
8. Update `contact.html` and `pages/contact.html` to call the API and show errors returned by the server.
9. Test with a dedicated test mailbox and verify both received messages in the original mailbox/provider, not just an HTTP 200.

A human mailbox connector such as Gmail/IMAP is useful for reading and replying to support tickets, but it is not a replacement for the website's transactional send path. SMTP/IMAP credentials must remain in the server secret manager or a dedicated mail connector, never in browser code.

## Priority order

P0 — do before public launch:

1. Connect contact form to a real API and support mailbox.
2. Implement real transactional email for verification/reset/newsletter.
3. Connect wizard to authenticated request creation and attachment upload.
4. Remove client-controlled pricing and implement server-side checkout/webhooks.
5. Replace dashboard static state with real request API state.
6. Fix or retire the duplicate `pages/` tree.
7. Production secrets, HTTPS, CORS, backups, monitoring.

P1 — before calling the admin product complete:

1. Wire admin requests/status/notes/clarifications to API.
2. Wire newsletter admin to API and provider.
3. Wire research publication/upload or explicitly keep publication manual.
4. Add real change-password and account lifecycle endpoints.
5. Add browser E2E tests for signup → login → dashboard → request → attachment → admin status.

P2 — after core flow works:

1. Payment refunds and entitlement lifecycle.
2. Email deliverability analytics and bounce handling.
3. Research downloads/PDF generation.
4. Advanced chart and report delivery.
5. Monitoring dashboards and operational runbooks.

## Verification commands executed

- `docker compose ps` — API up; DB and Redis healthy.
- `docker compose exec -T api alembic current` — `0003 (head)`.
- `curl http://127.0.0.1:8000/health` — HTTP 200.
- `.venv/Scripts/python.exe -m pytest -q` — `22 passed in 0.31s`.
- Regex-based extraction and `node --check` for all inline scripts — 0 syntax errors.
- Source-level form/API scan — confirmed contact/newsletter/wizard gaps above.
