# Camilla-Guided Backtest Intake Implementation Plan

> **For Hermes:** Implement task-by-task with strict RED → GREEN → REFACTOR. Do not expose the internal Hermes agent, credentials, data providers, or raw market data to clients.

**Goal:** Replace the current direct strategy-request checkout path with a controlled Camilla consultation where the client and Camilla jointly formalise the strategy, select a suitable data mode and validation protocol, and receive a server-calculated pre-quote before payment can be initiated.

**Architecture:** Add a durable consultation domain (`Consultation`, `ConsultationMessage`, `BacktestPreQuote`) associated with an authenticated user. The website opens a gated chat workspace before the wizard; an internal consultation service can call an approved, narrowly scoped Camilla runtime. It returns structured, reviewable recommendations—not trading advice—and never starts a backtest, creates a charge, or grants access. Once the conversation reaches a complete strategy specification, the server calculates a pre-quote from a server-side catalog, freezes a versioned test plan, and the client explicitly accepts it before the existing future hosted-checkout flow.

**Tech Stack:** Existing FastAPI + SQLAlchemy async + PostgreSQL + Redis + static HTML/JavaScript; optional approved internal Camilla runtime adapter; pytest; Alembic.

---

## Product contract and hard boundaries

### Client flow

```text
Authenticated client
  → choose Advanced or Simple intake
  → controlled Camilla consultation
  → structured strategy draft
  → joint data/test-plan recommendation
  → client confirms the frozen test plan
  → server-calculated pre-quote
  → client accepts pre-quote
  → hosted checkout (future, only after provider approval)
  → paid request enters backtest queue (future)
```

### Intake modes

- **Advanced — current system:** keeps the present detailed seven-step formulation as the expert mode. The consultation uses its fields as structured evidence and only flags ambiguity or missing parameters.
- **Simple — guided description:** client describes the idea in ordinary language. Camilla asks bounded follow-up questions and produces a structured draft; the client must review/edit/confirm every rule before any quote.

### Data/test-plan decision must be explicit

Camilla and the client jointly choose and freeze:

- instrument and session;
- date range and availability status;
- data mode: `tick_trades`, `depth_10`, or `news_event`;
- required data coverage and known gaps;
- strategy rule formalisation;
- execution/cost assumptions;
- validation: IS/OOS, cost/slippage, parameter stability/Monte Carlo when appropriate;
- special news-event requirements: source, scheduled timestamp, first-public availability, actual/forecast/prior/revision policy;
- exclusions and limitations.

The system may recommend a mode but never silently upgrade data quality, claim exact fills/queue position, promise performance, execute live orders, or fabricate unavailable historical data.

### Controlled-Camilla boundary

- The public browser never connects directly to Hermes or an LLM vendor.
- The site backend invokes only a dedicated consultation adapter using a restricted service identity.
- The adapter receives only the authenticated consultation context and the user’s messages; no secrets, other customer data, admin history, raw private datasets, or host control capability.
- System policy restricts the assistant to clarifying strategy rules, explaining test methodologies/data limits, selecting from authorized data modes, and drafting a test plan.
- The assistant cannot send emails, change pricing, start a backtest, mutate historical data, initiate payment, provide live trading instructions, or make performance promises.
- Every recommendation and version is persisted for audit; a client confirmation is required before quote generation.
- If the runtime is unavailable, the UI must say consultation is unavailable and preserve the draft—never display synthetic/fake Camilla messages.

## Current facts

- `test-strategy.html` currently captures advanced parameters and creates an authenticated `StrategyRequest`, then redirects to a disabled checkout.
- Existing request payload includes `indicators_params`, which can continue holding non-canonical display metadata, but consultation state, quotes and acceptance must use normalized tables/fields rather than client-side query parameters.
- Strategy request, attachments, auth, database and API foundation exist locally; local stack health is green and the latest full suite passed 38 tests.
- The current checkout is intentionally disabled and no payment provider is configured.
- No existing chat/LLM runtime adapter exists in `app/`; a real controlled Camilla connection requires a separately approved internal runtime endpoint/identity. Do not substitute a scripted chatbot and label it Camilla.

---

## Task 1: Define the consultation state machine and schemas

**Objective:** Create a small, auditable domain model before building UI or assistant calls.

**Files:**
- Create: `app/models/consultation.py`
- Create: `app/models/consultation_message.py`
- Create: `app/models/backtest_prequote.py`
- Modify: `app/models/__init__.py`
- Create: `app/schemas/consultation.py`
- Create: `tests/test_consultation_contract.py`

**Step 1: Write the failing tests**

Test that:
- an authenticated user owns a consultation;
- permitted states are `draft`, `consulting`, `awaiting_client_confirmation`, `confirmed`, `quoted`, `expired`, `cancelled`;
- message roles are only `client`, `camilla`, `system`;
- only a confirmed consultation can create a pre-quote;
- a pre-quote stores immutable test-plan version, selected data mode, price currency/amount, expiry, and acceptance timestamp separately.

**Step 2: Run RED**

```bash
.venv/Scripts/python.exe -m pytest tests/test_consultation_contract.py -q
```

Expected: failure because the consultation domain does not exist.

**Step 3: Implement the minimal models and Pydantic schemas**

Use UUID primary keys, foreign keys to `users` and optional `strategy_requests`, UTC timestamps, JSONB for the canonical strategy/test-plan document, and a monotonically increasing `plan_version`.

**Step 4: Run GREEN**

```bash
.venv/Scripts/python.exe -m pytest tests/test_consultation_contract.py -q
```

**Step 5: Commit**

```bash
git add app/models app/schemas tests/test_consultation_contract.py
git commit -m "feat: add consultation and prequote domain models"
```

---

## Task 2: Add a migration and prove it on fresh PostgreSQL

**Objective:** Persist consultation, messages and pre-quotes safely.

**Files:**
- Create: `migrations/versions/0005_create_consultations_and_prequotes.py`
- Modify: `tests/test_consultation_contract.py`

**Step 1: Write a failing migration/schema test**

Assert that the migration creates the three tables, ownership foreign keys, state constraints/enums, indexes on consultation status/user, and a unique constraint preventing duplicate accepted quote versions for a consultation.

**Step 2: Run RED**

```bash
.venv/Scripts/python.exe -m pytest tests/test_consultation_contract.py -q
```

**Step 3: Implement the migration**

Use the existing migration conventions. Keep state types compatible with the current PostgreSQL/Alembic setup and avoid duplicate enum creation.

**Step 4: Run migration verification**

```bash
docker compose exec -T api alembic upgrade head
docker compose exec -T api alembic current
.venv/Scripts/python.exe -m pytest tests/test_consultation_contract.py -q
```

Expected: `0005 (head)` and tests pass.

**Step 5: Commit**

```bash
git add migrations tests/test_consultation_contract.py
git commit -m "feat: persist consultation workflow"
```

---

## Task 3: Implement a server-side data/test-plan catalog and quote engine

**Objective:** Ensure Camilla recommendations and prices are explainable, server-owned and auditable.

**Files:**
- Create: `app/services/backtest_catalog.py`
- Create: `app/services/prequote.py`
- Create: `tests/test_prequote_service.py`
- Modify: `app/core/config.py` only for non-secret catalog settings if needed

**Step 1: Write failing tests**

Cover:
- valid recommendations for tick, depth-10 and news-event modes;
- rejection when a depth/news mode lacks available/approved coverage;
- required test-plan fields per mode;
- server-calculated price cannot be supplied/overridden by browser input;
- quote expiry and explicit client acceptance;
- recommendation includes limitations, e.g. depth-10 does not mean queue-position/exact-fill modelling.

**Step 2: Run RED**

```bash
.venv/Scripts/python.exe -m pytest tests/test_prequote_service.py -q
```

**Step 3: Implement minimal deterministic policy**

The catalog must use only data modes already available/authorized by Capo Horn Lab. It must produce a test-plan object, itemised scope, and pre-quote amount in EUR. Keep provider acquisition cost, markup and internal portfolio economics strictly server/admin-only and absent from browser/API responses.

**Step 4: Run GREEN + regression suite**

```bash
.venv/Scripts/python.exe -m pytest tests/test_prequote_service.py -q
.venv/Scripts/python.exe -m pytest -q
```

**Step 5: Commit**

```bash
git add app/services tests/test_prequote_service.py app/core/config.py
git commit -m "feat: add server-side backtest prequote policy"
```

---

## Task 4: Build a restricted Camilla consultation adapter

**Objective:** Provide a real integration seam without exposing the agent runtime or pretending a local script is Camilla.

**Files:**
- Create: `app/services/camilla_consultation.py`
- Create: `app/services/camilla_policy.py`
- Create: `tests/test_camilla_consultation_policy.py`
- Modify: `app/core/config.py`

**Step 1: Write failing tests**

Assert that the policy:
- accepts client strategy text and allowed structured context;
- redacts/rejects secrets and unsupported content fields;
- constrains outputs to `assistant_message`, `draft_patch`, `open_questions`, `recommended_test_plan`, `limitations`, and `ready_for_confirmation`;
- rejects commands/actions requesting trading, payment, email, external publishing, provider purchasing, host control, or raw-data disclosure;
- returns an explicit unavailable result when the adapter endpoint/identity is not configured.

**Step 2: Run RED**

```bash
.venv/Scripts/python.exe -m pytest tests/test_camilla_consultation_policy.py -q
```

**Step 3: Implement the adapter boundary**

- Use a private service URL/identity configured only in server secrets.
- Require structured JSON response validation.
- Add timeout, correlation ID and narrowly scoped retry behavior.
- Persist only an error-safe summary; never log prompts containing personal data in production.
- Do not implement a browser-to-Hermes direct connection.
- Do not enable the adapter until Francesco approves the runtime endpoint and service identity.

**Step 4: Run GREEN**

```bash
.venv/Scripts/python.exe -m pytest tests/test_camilla_consultation_policy.py -q
```

**Step 5: Commit**

```bash
git add app/services app/core/config.py tests/test_camilla_consultation_policy.py
git commit -m "feat: add restricted Camilla consultation adapter"
```

---

## Task 5: Add authenticated consultation APIs

**Objective:** Make consultation state durable and ownership-safe.

**Files:**
- Create: `app/api/v1/consultations.py`
- Modify: `app/main.py`
- Modify: `app/schemas/consultation.py`
- Create: `tests/test_consultation_api.py`

**Endpoints:**

```text
POST   /api/v1/consultations
GET    /api/v1/consultations/{id}
POST   /api/v1/consultations/{id}/messages
PATCH  /api/v1/consultations/{id}/draft
POST   /api/v1/consultations/{id}/confirm-plan
POST   /api/v1/consultations/{id}/prequote
POST   /api/v1/prequotes/{id}/accept
```

**Step 1: Write failing API tests**

Cover authentication, ownership isolation, input length/rate limits, state transitions, unavailable Camilla adapter, no quote before confirmation, no browser price field, idempotent pre-quote generation, and quote acceptance expiry.

**Step 2: Run RED**

```bash
.venv/Scripts/python.exe -m pytest tests/test_consultation_api.py -q
```

**Step 3: Implement endpoints minimally**

- Rate limit message posting in Redis.
- Persist each message and structured plan patch atomically.
- Re-fetch/validate state after each mutation.
- Return only client-safe test-plan and quote data.
- Keep any automated assistant response inert until the restricted adapter is configured; return a truthful unavailable state otherwise.

**Step 4: Run GREEN + full suite**

```bash
.venv/Scripts/python.exe -m pytest tests/test_consultation_api.py -q
.venv/Scripts/python.exe -m pytest -q
```

**Step 5: Commit**

```bash
git add app/api/v1 app/main.py app/schemas tests/test_consultation_api.py
git commit -m "feat: add authenticated consultation API"
```

---

## Task 6: Add the Advanced/Simple entry choice to Test Your Strategy

**Objective:** Let clients intentionally choose the existing detailed wizard or plain-language guided intake.

**Files:**
- Modify: `test-strategy.html`
- Modify: `assets/js/account-client.js`
- Modify: `tests/test_test_strategy_data_modes.py`
- Create: `tests/test_consultation_ui_contract.py`

**Step 1: Write failing UI contract test**

Assert presence of:
- two clear cards/buttons: `Advanced — Detailed strategy setup` and `Simple — Explain your idea to Camilla`;
- accessible radio/button semantics and keyboard focus;
- client-side function creating an authenticated consultation before chat/workflow access;
- no claims that a conversation starts a backtest or causes payment;
- mobile responsive behavior and no data cost/provider disclosure.

**Step 2: Run RED**

```bash
.venv/Scripts/python.exe -m pytest tests/test_consultation_ui_contract.py -q
```

**Step 3: Implement the intake selector**

- Keep the current seven-step UI as Advanced.
- For Simple, send the client into the consultation workspace with a clean first prompt: describe the idea, instrument if known, and when/why it trades.
- Advanced opens the same consultation in “review detailed fields” mode before final confirmation, so all clients pass the controlled preflight.

**Step 4: Run GREEN**

```bash
.venv/Scripts/python.exe -m pytest tests/test_consultation_ui_contract.py -q
```

**Step 5: Commit**

```bash
git add test-strategy.html assets/js/account-client.js tests
git commit -m "feat: add advanced and simple strategy intake"
```

---

## Task 7: Build the controlled consultation workspace

**Objective:** Give client and Camilla a transparent, editable space to form the test specification.

**Files:**
- Create: `strategy-consultation.html`
- Create: `assets/js/consultation-client.js`
- Modify: `test-strategy.html`
- Create: `tests/test_consultation_workspace.py`

**Step 1: Write failing UI contract test**

Verify:
- authenticated access gate;
- transcript renders client/Camilla/system roles safely using `textContent`, never raw `innerHTML` for messages;
- persistent draft panel shows instrument, rules, data mode, validation plan, limitations, and unanswered questions;
- only client confirmation enables the “Generate pre-quote” action;
- an adapter-unavailable state is visible and does not invent a response;
- page has desktop/tablet/mobile layouts, focus management, status/live-region accessibility, and loading/error/retry states.

**Step 2: Run RED**

```bash
.venv/Scripts/python.exe -m pytest tests/test_consultation_workspace.py -q
```

**Step 3: Implement workspace**

Use existing Capo Horn design tokens and public-page navigation. The UI must contain:

1. chat transcript;
2. message composer with client-side length limit;
3. `What Camilla is deciding with you` side panel;
4. editable structured rule/test-plan review;
5. limitations/risk disclosure;
6. explicit `Confirm this test plan` button;
7. post-confirmation pre-quote card.

The workspace must say: “This consultation structures a historical research request. It does not provide investment advice, initiate live trading, or guarantee results.”

**Step 4: Run GREEN + JS syntax check**

```bash
.venv/Scripts/python.exe -m pytest tests/test_consultation_workspace.py -q
node --check C:/Users/farne/AppData/Local/Temp/chl-consultation-inline.js
```

Use a temporary extractor for inline scripts and remove it after the check.

**Step 5: Commit**

```bash
git add strategy-consultation.html assets/js/consultation-client.js test-strategy.html tests
git commit -m "feat: add controlled Camilla strategy consultation"
```

---

## Task 8: Freeze plan, generate pre-quote, and gate checkout

**Objective:** Make payment a consequence of client-approved scope, not an editable browser amount.

**Files:**
- Modify: `strategy-consultation.html`
- Modify: `assets/js/consultation-client.js`
- Modify: `checkout.html`
- Modify: `assets/js/account-client.js`
- Create: `tests/test_prequote_checkout_contract.py`

**Step 1: Write failing tests**

Assert:
- checkout requires an accepted pre-quote ID and fetches its server-owned summary;
- client URL cannot specify a price/discount/entitlement;
- expired/unaccepted quote cannot continue;
- quote summary displays selected data mode, test protocol, data coverage qualification, scope and limitations—not internal provider cost/markup;
- payment remains disabled until a hosted payment provider is implemented and webhook verified.

**Step 2: Run RED**

```bash
.venv/Scripts/python.exe -m pytest tests/test_prequote_checkout_contract.py -q
```

**Step 3: Implement minimal gate**

Remove tier/month/price as authority. Preserve the safe disabled payment state until a separate provider-approved payment workstream creates server checkout sessions and signed webhook verification.

**Step 4: Run GREEN + full suite**

```bash
.venv/Scripts/python.exe -m pytest tests/test_prequote_checkout_contract.py -q
.venv/Scripts/python.exe -m pytest -q
git diff --check
```

**Step 5: Commit**

```bash
git add strategy-consultation.html checkout.html assets/js tests
git commit -m "feat: gate checkout behind accepted backtest prequote"
```

---

## Task 9: End-to-end local verification and operational documentation

**Objective:** Prove the new flow, document the external activation boundary, and avoid a false production claim.

**Files:**
- Create: `tests/test_consultation_e2e_contract.py`
- Modify: `reports/WORK_REGISTER.md`
- Create: `reports/camilla-consultation-production-gate.md`

**Step 1: Write failing E2E contract test**

Model the sequence:

```text
create consultation → client message → unavailable/allowed adapter result → draft update
→ confirm plan → generate pre-quote → accept quote → checkout gate
```

Test both data-mode selection and news-event required fields.

**Step 2: Run RED then implement any minimal missing integration**

```bash
.venv/Scripts/python.exe -m pytest tests/test_consultation_e2e_contract.py -q
```

**Step 3: Run all local gates**

```bash
docker compose ps
curl -fsS -i http://127.0.0.1:8000/health
docker compose exec -T api alembic current
.venv/Scripts/python.exe -m pytest -q
```

**Step 4: Browser QA**

Run authenticated local browser E2E only after a test account and browser-accessible local origin are available. Verify desktop and mobile widths, keyboard navigation, assistant-unavailable state, plan confirmation, quote expiry/error state and no direct backend/secret exposure.

**Step 5: Update work register and commit**

Record actual test output, artifact paths, the fact that payment is still disabled, and whether the restricted Camilla runtime is actually configured. Do not call the site autonomous or production-ready until all external gates below pass.

---

## Production activation gates — require Francesco approval

1. **Dedicated Camilla runtime:** approved private endpoint/service identity, capability allowlist, authentication, quotas, audit logging and data-retention policy.
2. **Transactional email:** verified sender domain, DNS records, production provider key stored outside Git, original-mailbox delivery test.
3. **Payment:** selected provider, server checkout, signed webhook, order/entitlement/refund lifecycle, sandbox E2E; no client-side payment success.
4. **Deployment:** public API runtime, HTTPS, production secrets, exact CORS origin, secure cookies, persistent uploads, backup/restore test and monitoring.
5. **Legal/privacy:** update policy/terms for conversational intake, AI-assisted processing, retention, support contact and payment provider.
6. **Data licensing:** confirm the provider license covers the intended internal research use and client report delivery; do not redistribute raw data.

## Acceptance criteria

- The client can choose Advanced or Simple intake.
- Every request receives a controlled consultation before a quote; Simple supports plain language, Advanced preserves detailed fields.
- Camilla can only produce structured strategy/test-plan guidance under an enforced policy boundary.
- Client and Camilla explicitly agree data mode/test scope, with visible limitations.
- The test plan is versioned, immutable after confirmation, and client-confirmed.
- A pre-quote is computed only server-side from the confirmed plan; it expires and requires client acceptance.
- No backtest runs, money is charged, email is sent, raw data is exposed or external purchase occurs as a result of chat alone.
- Adapter failure is truthful and preserves the draft.
- Full suite, migration, API ownership/state-transition tests, static UI contracts and browser E2E pass before delivery.

## Key risks and decisions

- **Do not fake Camilla:** a static decision tree can improve form UX but must never be branded as a live Camilla consultation. The feature needs the dedicated runtime activation gate.
- **Prompt injection/data separation:** client messages are untrusted data. They cannot alter system policy, access other consultations or instruct server tooling.
- **Scope creep:** initial version should guide and quote a single strategy/request. Do not add automatic strategy coding/backtesting execution in the chat workstream.
- **Pricing authority:** price belongs to the server catalog; user-visible values are final service prices only. Internal provider cost and data-portfolio economics stay admin-only.
- **Autonomy:** the client may approve a quote; payment and backtest initiation remain gated by separate verified systems.
