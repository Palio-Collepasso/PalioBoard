# Test Strategy

## Purpose

Describe the testing approach, test layers, ownership, and minimum expectations for change types.

## Goals

- Catch regressions in trust-critical workflows early.
- Keep feedback fast for common backend and frontend changes.
- Match test depth to the layer where the risk actually lives.
- Keep Playwright intentionally small and focused on operationally critical flows.

## Test Layers

| Layer | Purpose | Scope | Speed | Typical owner |
|---|---|---|---|---|
| Unit | Prove pure, deterministic business or utility logic | calculations, validation helpers, ranking derivation helpers, DTO mappers | fast | backend or frontend feature author |
| Integration | Prove workflow correctness across real infrastructure boundaries | FastAPI workflows, Postgres transactions, migrations, audit/projection side effects | medium | backend feature author |
| API contract | Prove committed client/server shape stays stable | OpenAPI export, generated types, endpoint/status surface | medium | backend author with frontend consumer validation |
| E2E | Prove must-not-break user-visible flows through the deployed stack | same-origin shell reachability today; broader operational flows later | slow | frontend or full-stack feature author |
| Manual verification | Cover risky operational checks not yet automated | deploy smoke, migration review, incident recovery checks | variable | change owner or reviewer |

## Guiding Principles

- Prefer the cheapest test that can reliably catch the real risk.
- DB-centric workflows belong in real Postgres integration tests, not mocks.
- Official result, audit, and projection behavior must be proven together when they share one transaction.
- Frontend tests should protect rendering and interaction wiring, not re-implement backend-owned business rules.
- Critical flows can be covered end-to-end, but the suite must stay small and high-signal.
- Static checks complement behavior tests; they do not replace them.

## Change-Type Matrix

| Change type | Unit | Integration | API contract | E2E | Manual |
|---|---|---|---|---|---|
| Pure UI refactor | required | optional | no | optional | optional |
| Domain rule change | required | required | maybe | maybe | optional |
| Persistence/query change | optional | required | maybe | optional | optional |
| API response change | optional | required | required | optional | optional |
| Auth/capability change | required | required | maybe | maybe | optional |
| Critical flow change | required | required | maybe | required | optional |
| Infra/deploy change | no | maybe | no | no | required |

## Layer Expectations

Template for each test-layer entry: `docs/templates/testing/test-layer-expectation.template.md`

> Next-pass guidance: keep this document as a compact decision policy. If future revisions add more examples or scenario detail, trim aggressively so the file stays a decision aid rather than turning into a large policy manual.

### Unit Tests

- **Purpose:** Prove pure logic deterministically without database, HTTP, or realtime transport involvement.
- **What to test:**
  - placement and scoring helpers
  - configuration parsing and small pure mappers
  - focused frontend component behavior
- **What not to test:**
  - transactional workflow semantics
  - proxying, migrations, or container orchestration
- **Preferred test style:** Table-driven backend cases and focused frontend behavior specs.
- **Fixtures/mocks guidance:** Keep fixtures minimal and explicit; avoid repository mocks for DB-backed workflows.

### Integration Tests

- **Purpose:** Prove authoritative workflows and environment wiring against real infrastructure.
- **Boundary under test:** FastAPI plus PostgreSQL, migrations, and related task-owned support code.
- **What to test:**
  - migration/bootstrap behavior
  - readiness and health behavior against a real migrated database
  - transactional or persistence-heavy workflows as they land
- **Required setup:**
  - real Postgres
  - real Alembic migrations
  - task-owned support such as `apps/api/tests/support/postgres.py`
- **Failure signals:**
  - schema mismatch
  - migration failure
  - readiness/health behavior diverging from the documented runtime contract

### API Contract Tests

- **Purpose:** Protect the committed API artifact and the generated consumer surface.
- **Focus:**
  - OpenAPI export stability
  - generated type compatibility
  - endpoint/status shape changes
- **Required for:**
  - OpenAPI changes
  - response or request payload changes
  - committed contract workflow changes

### End-to-End Tests

- **Purpose:** Prove the browser can still reach the highest-risk user-visible flows through the real stack.
- **Critical journeys covered in:** `docs/testing/critical-e2e-flows.md`
- **Execution cadence:** Small per-PR smoke coverage plus broader coverage only when the product slice justifies it.
- **Data setup approach:** Prefer the existing same-origin Compose stack, minimal fixture assumptions, and explicit test-owned setup.

### Manual Verification

- **Use when:**
  - the change affects deploy or rollback procedure
  - the risk is operational but not yet worth permanent automation
- **Checklist format:** Record the exact commands, endpoints, and expected results in task notes or deployment docs.

## Coverage Expectations

Template for each coverage-expectation entry: `docs/templates/testing/coverage-expectation.template.md`

### Backend workflow and persistence changes

- **Minimum required tests:**
  - integration coverage against real Postgres
  - unit coverage for any extracted pure calculation rules
- **Nice-to-have tests:**
  - API contract coverage when payloads or status codes change
- **Notes:** Audit, projections, migrations, and readiness semantics should be validated at the workflow boundary, not by isolated mocks.

### Frontend-only rendering changes

- **Minimum required tests:**
  - focused frontend behavior tests
- **Nice-to-have tests:**
  - Playwright coverage only when the affected path is already considered critical
- **Notes:** Avoid large snapshots and keep business-rule ownership in backend tests.

### Realtime or browser critical-flow changes

- **Minimum required tests:**
  - targeted integration coverage where the state/conflict semantics live
  - E2E coverage when the user-visible flow is release-blocking
- **Nice-to-have tests:**
  - manual verification notes for recovery or incident paths
- **Notes:** Live collaboration behavior must never silently replace official correctness checks.

### Infra or deploy changes

- **Minimum required tests:**
  - the narrowest honest smoke check for the changed path
  - explicit manual verification of build/deploy/rollback expectations
- **Nice-to-have tests:**
  - follow-up automation when the workflow stabilizes
- **Notes:** Deployment and operational truth should stay aligned with `docs/ops/local-dev.md`, `docs/ops/deploy.md`, and `docs/ops/runbook.md`.

## Non-Goals

- Broad UI snapshot coverage.
- SQLite substitutes for backend integration tests.
- Large browser suites before the corresponding user journeys exist.

## Flaky Test Policy

- **Definition of flaky:** A test that can fail without a product or environment change that should matter to the assertion.
- **How to handle:**
  - fix or quarantine quickly
  - record the failure mode and the follow-up owner
  - do not silently normalize intermittent failures
- **Can flaky tests block merge?:** Yes, when they are part of the required quality gate.
- **Escalation path:** Record the issue in the active task or follow-up work and update the relevant docs if the failure changes required local/deploy workflow.

## Test Data Policy

- Canonical fixtures live in: `apps/api/tests/support/` and `apps/web/e2e/`, with shared documentation in `docs/testing/fixtures.md`.
- Shared seed assumptions: Prefer minimal task-owned fixtures that model one narrow scenario honestly.
- Sensitive/production-derived data policy: Do not use production-derived datasets in repo fixtures.

## Tooling and Commands

- **Run all tests:** `make test`
- **Run unit tests:** `cd apps/api && uv run pytest tests/unit` or `cd apps/web && npm test -- --watch=false`
- **Run integration tests:** `cd apps/api && uv run pytest tests/integration`
- **Run E2E tests:** `cd apps/web && npm run e2e`
- **Run lint/type checks:** `cd apps/api && uv run python -m palio.shared.module_boundaries`, `cd apps/web && npm run check-boundaries`, `cd apps/web && npm run typecheck`

## Review Checklist

- [ ] The chosen test depth matches the risk.
- [ ] Critical rule changes have direct tests.
- [ ] New bug fixes include regression protection when practical.
- [ ] Fixtures or seed assumptions were updated if necessary.
- [ ] E2E flows were updated if a critical journey changed.
