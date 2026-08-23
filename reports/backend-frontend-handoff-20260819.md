# Backend ↔ Frontend connection handoff — 2026-08-19

## Verified compose-backed state

- Docker Desktop daemon: `29.6.2`.
- PostgreSQL 16: healthy and accepting loopback connections.
- Redis: healthy and reachable from the API container (`redis_ping=True`).
- FastAPI: active on `127.0.0.1:8000`; `GET /health` returned HTTP 200.
- Alembic: `0004 (head)` against PostgreSQL.

## Verified user journeys

### Local authenticated request flow

The compose-backed smoke test completed: signup → login → `/auth/me` → strategy-request creation → attachment upload → request list → request detail. The detail response returned exactly one uploaded attachment.

### Real transactional email and account verification

- Resend was configured without reading or exposing its API key.
- An authorized email delivery test to the company Gmail returned `delivery_result=True`; Francesco confirmed it arrived.
- An authorized signup test sent an account verification email to a unique company Gmail alias and returned HTTP 201.
- The code supplied by Francesco was accepted by `POST /api/v1/auth/verify`, which returned HTTP 200 with `Email verified successfully`.

## Functional fixes in working tree

1. `app/services/auth.py`
   - Converts JWT string subjects to `UUID` before current-user and refresh-token database queries.
   - Invalid claims fail closed as HTTP 401 instead of raising HTTP 500.

2. `app/models/strategy_request.py`
   - Uses async-compatible `selectin` relationship loading for request history, attachments, and internal notes.

3. `research-detail.html`
   - Repaired the embedded `researchData` array terminator: it is now strict JSON-compatible and explicitly terminated as JavaScript.
   - Regression test confirms 13 records and the final `market-cycle-analysis` study.

4. `login.html` and `dashboard.html`
   - Removed console-only social-login mock actions.
   - Disabled unimplemented social-login and payment controls with accessible `aria-disabled` state rather than presenting inert clickable actions.

5. Tests added
   - `tests/run_local_api_e2e.py` supports standalone and compose API URLs through `CHL_E2E_BASE`.
   - `tests/test_research_detail_dataset.py` validates the embedded research dataset.
   - `tests/test_nonoperational_controls.py` prevents console-only auth/payment controls from returning.

## Verification results

- Full Python suite: `56 passed in 2.60s`.
- `node --check assets/js/account-client.js`: passed.
- `git diff --check`: passed.

## Release boundary

- No commit, push, deployment, payment provider configuration, or external message was performed.
- Payment functionality remains honestly unavailable until a provider and server-side payment/webhook/entitlement workflow are implemented.
- The current source tree contains pre-existing/untracked QA artifacts. Before a release, stage only intentionally reviewed source, tests, and reports.

## Next gate

1. Perform browser-level QA of public/static pages against the intended API deployment target.
2. Independently review the narrow source diff.
3. Present the commit/deployment preview to Francesco and wait for explicit approval before any push/Render deployment.
