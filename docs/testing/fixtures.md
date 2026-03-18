# Test Fixtures

## Purpose
Document the shared fixtures and canonical seeded scenarios that multiple suites depend on.

## Document boundary
This file owns **shared fixture inventory**.
It does not document one-off test data or decide test depth.
- Test depth lives in `docs/testing/test-strategy.md`.
- Browser-critical flow mapping lives in `docs/testing/critical-e2e-flows.md`.

## Add a fixture here only when
- more than one suite depends on it, or
- it represents a canonical scenario reused across tasks, or
- changing it can break multiple tests or workflows at once

## Fixture index
| Fixture ID | Fixture | Owner | Lifecycle | Common consumers |
|---|---|---|---|---|
| `FX-001` | Disposable Postgres integration database | backend owner | recreate per integration run | backend integration tests |
| `FX-002` | Same-origin shell smoke routes | web/app owner | keep stable while shell smoke remains critical | Playwright shell smoke |
| `FX-003` | Auth-linked application user seed | backend owner | maintain when auth/session semantics change | protected admin route tests, auth error semantics |

## Fixture definitions
### `FX-001` — Disposable Postgres integration database
- **Owner:** backend owner
- **Lifecycle:** disposable; recreate for each honest integration run
- **Use when:** validating DB-backed workflows, migrations, readiness, audit, or projections
- **Safe to modify:** only with matching updates to integration tests and docs that rely on the schema/setup
- **Common consumers:** `apps/api/tests/integration/*`
- **Related docs:** `docs/domain/er-schema.md`, `docs/testing/test-strategy.md`

### `FX-002` — Same-origin shell smoke routes
- **Owner:** web/app owner
- **Lifecycle:** keep stable while `E2E-001` remains the shell/proxy smoke gate
- **Use when:** validating same-origin routing and shell bootstrap
- **Safe to modify:** only with matching updates to the Playwright spec and local-dev guidance
- **Common consumers:** `apps/web/e2e/smoke/*`
- **Related E2E flows:** `E2E-001`

### `FX-003` — Auth-linked application user seed
- **Owner:** backend owner
- **Lifecycle:** update when session/auth semantics or required capabilities change
- **Use when:** validating `401` vs `403` behavior for protected admin routes and linked-application-user expectations
- **Safe to modify:** only with matching updates to protected-route tests and `docs/api/error-contract.md`
- **Common consumers:** admin session/auth integration tests
- **Related business rules:** `BR-009`

## Rule
If a fixture stops being shared or canonical, remove it from this file and keep it local to the tests that own it.
