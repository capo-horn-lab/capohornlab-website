# Implementation progress — 2026-08-17

## Completed and verified locally

- Added `ContactMessage` model and migration `0004_create_contact_messages.py`.
- Added `POST /api/v1/contact` with validation, rate limiting, honeypot, persistence and provider handoff.
- Added fail-closed HTTPX Resend adapter; no provider key means no fake delivery success.
- Configured defaults for `contact@capohornlab.com` and `noreply@capohornlab.com`.
- Account verification/reset now call transactional email adapter; delivery remains blocked until Resend is configured.
- Replaced contact-page timed fake success with real API calls in root and legacy pages.
- Added shared `assets/js/newsletter-client.js` and connected public newsletter forms to the API.
- Added request list/create/upload methods to `assets/js/account-client.js`.
- Dashboard now loads real authenticated requests and no longer reports mock password success.
- Strategy wizard now creates an authenticated StrategyRequest and uploads selected files before the checkout handoff.
- Updated legacy `pages/test-strategy.html` wiring.
- Added `.env.example` email/upload configuration.
- Added contact-flow regression tests.

## Verification evidence

- `.venv/Scripts/python.exe -m pytest -q`: `26 passed`.
- Inline JavaScript scan with `node --check`: `0 errors`.
- `docker compose exec -T api alembic current`: `0004 (head)`.
- `curl http://127.0.0.1:8000/health`: HTTP 200.
- OpenAPI includes `/api/v1/contact`.
- Contact delivery gate test without Resend: HTTP 503, record cleaned afterwards.
- No real email sent; no DNS changed; no deploy performed.

## Current blocker

Resend domain verification and API key are not configured. Signup verification, password reset, newsletter confirmation and contact acknowledgement intentionally remain unavailable until the provider is configured.

## Next external gates

1. Add `capohornlab.com` in Resend.
2. Copy exact SPF/DKIM/MX/CNAME records into `reports/RESEND_ARUBA_DNS_SETUP.txt`.
3. Francesco applies them in Aruba DNS or authorizes browser-assisted application after reviewing the exact payload.
4. Insert Resend API key through a secure secret channel, never into Git or this report.
5. Send test to `tester@capohornlab.com` and verify the original mailbox.
6. Only then rerun full signup → verify → login and live contact/newsletter tests.
7. Payment and Aruba deployment remain separate gates.
