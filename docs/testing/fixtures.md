# Test Fixtures

## Purpose

Document the named fixtures, seeds, and canonical data scenarios used by tests.

Good fixture documentation helps agents and humans answer:
- which scenario already exists;
- when a shared fixture is safe to modify;
- which tests depend on a given dataset;
- whether a failure is caused by product logic or by broken fixture assumptions.

## Principles

- Fixtures should be deterministic.
- Fixtures should be minimal but realistic.
- Shared fixtures should model recognizable business scenarios.
- If multiple suites depend on a fixture, document it here.

## Fixture Index

| Fixture ID | Name | Scope | Used by | Source |
|---|---|---|---|---|
| `FX-001` | Disposable Postgres integration database | integration | backend integration suite | `apps/api/tests/support/postgres.py` |
| `FX-002` | Same-origin shell smoke routes | e2e | Playwright shell smoke suite | `apps/web/e2e/shell-smoke.spec.ts` |

---

## Fixture Definitions

Template for each fixture entry: `docs/templates/testing/fixture.template.md`

> Next-pass guidance: keep this file limited to shared fixture definitions. Do not document every test dataset here; add entries only when a fixture is reused across suites or carries important shared constraints that future changes must preserve.

## Current Coverage Note

The shared fixture catalog currently covers only the technical fixtures reused by the baseline harnesses.

Future note:
- promote named business-scenario fixtures here when stable seeded season, ranking, review, tournament, or live-collaboration datasets exist across multiple suites
- drop this note once the shared fixture catalog is no longer foundation-stage


### `FX-001` — Disposable Postgres integration database

- **Status:** active
- **Scope:** integration
- **Purpose:** Support real-Postgres backend integration tests with isolated databases and real Alembic migrations.
- **Defined in:** `apps/api/tests/support/postgres.py`
- **Used by:**
  - `apps/api/tests/integration/`
  - `make test-backend`

#### Scenario represented

The backend integration layer proves migration/bootstrap and runtime readiness against a real PostgreSQL instance instead of SQLite or fake persistence.

#### Contents

- disposable Postgres container or reused local admin DB
- isolated test database per run
- real Alembic migration application
- disposable container defaults loaded from `infra/compose/docker-compose.yml`

#### Important values / assumptions

- The default disposable image matches the `db` service image in `infra/compose/docker-compose.yml`.
- The application schema is `palio_board`.
- `PALIO_TEST_POSTGRES_URL` can override the disposable server path.
- `PALIO_TEST_POSTGRES_IMAGE` can override only the disposable image while keeping the compose-backed bootstrap values.

#### Setup instructions

1. Run `cd apps/api && uv run --group dev pytest tests/integration`.
2. Let the harness start a disposable Postgres container automatically, or set `PALIO_TEST_POSTGRES_URL` first.

#### Reset / cleanup instructions

1. Let the test harness drop the isolated database after the run.
2. Stop the disposable Docker container if the harness had to create one.

#### Safe to modify?

- **Yes/No:** no
- **Constraints:** Keep the schema name, migration application flow, and override env vars consistent with the backend harness docs.

#### Common consumers

- backend smoke/integration coverage
- migration and readiness verification

#### Related business rules

- None yet. This fixture protects infrastructure correctness rather than business-rule behavior.

#### Related E2E flows

- None

#### Notes

- Update `docs/testing/test-strategy.md` and `docs/ops/local-dev.md` if the harness contract changes.
- Keep the disposable-test defaults aligned with `infra/compose/docker-compose.yml` so the integration harness and local stack do not drift.
- Promote additional fixture IDs here when the backend adds stable seeded scenarios.

### `FX-002` — Same-origin shell smoke routes

- **Status:** active
- **Scope:** e2e
- **Purpose:** Verify that the browser can still reach the scaffolded shells through the Nginx same-origin stack.
- **Defined in:** `apps/web/e2e/shell-smoke.spec.ts`
- **Used by:**
  - `cd apps/web && npm run e2e`
  - `make test-e2e`

#### Scenario represented

The current Playwright smoke suite proves that `/`, `/admin`, `/public`, and `/maxi`

#### Contents

- root-to-public redirect expectation
- scaffold headings for admin, public, and maxi routes
- placeholder-card count assertions per shell

#### Important values / assumptions

- The default base URL is `http://127.0.0.1:8080`.
- The suite can reuse `PLAYWRIGHT_BASE_URL` when provided.
- The Nginx proxy and built SPA must be available.

#### Setup instructions

1. Run `cd apps/web && npm run e2e:install` once to install the browser.
2. Run `cd apps/web && npm run e2e`.

#### Reset / cleanup instructions

1. Let `apps/web/tools/run-playwright.mjs` stop the Compose stack when it started it.
2. Use `make down` if the stack was started separately for manual verification.

#### Safe to modify?

- **Yes/No:** yes
- **Constraints:** Keep the route list aligned with `docs/testing/critical-e2e-flows.md` and the actual scaffold headings.

#### Common consumers

- browser smoke validation
- same-origin stack verification

#### Related business rules

- None yet. This fixture covers route reachability rather than business semantics.

#### Related E2E flows

- `E2E-001`

#### Notes

- Keep this fixture intentionally small until real operational browser journeys land.
- If route expectations change, update the Playwright spec and `docs/testing/critical-e2e-flows.md` together.

---

## Canonical Scenario Sets

Template for each scenario-set entry: `docs/templates/testing/canonical-scenario-set.template.md`

### m-0 smoke verification

- **Purpose:** Provide the minimum reusable scenarios needed to validate the current backend and browser scaffolds honestly.
- **Fixtures included:**
  - `FX-001`
  - `FX-002`
- **Used for:**
  - `TASK-8` and `TASK-9` baseline verification
  - local regression checks for the current scaffolded stack
