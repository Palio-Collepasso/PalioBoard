# API / backend instructions

## Scope
This file applies to backend work under `apps/api/`.

Follow `docs/README.md` for:
- documentation source precedence
- base reading sets by task type
- archive and proposal-doc policy
- stop/flag conditions that come from doc conflicts

This file adds **backend-only deltas**.

## Backend code roots
Use these paths when placing code:
- `apps/api/src/palio/api/` — FastAPI routers, request/response DTO wiring, HTTP semantics
- `apps/api/src/palio/bootstrap/` — composition root and dependency wiring
- `apps/api/src/palio/shared/` — low-level technical helpers only
- `apps/api/src/palio/modules/<module>/application/` — use cases, orchestration, transaction sequencing
- `apps/api/src/palio/modules/<module>/domain/` — business rules, validation, state transitions, value objects
- `apps/api/src/palio/modules/<module>/infrastructure/` — repositories, SQL queries, adapters
- `apps/api/tests/unit/` — pure logic tests
- `apps/api/tests/integration/` — DB-backed and workflow tests

## Backend-specific extra reads
Always also read:
- `docs/architecture/module-map.md` when choosing the owning module
- `docs/architecture/runtime-flows.md` for transaction, projection, lifecycle, or live-entry changes

## Stable backend commands
- Backend unit tests: `make test-api-unit`
- Backend integration tests: `make test-api-integration`
- Full backend checks: `make lint`, `make typecheck`, `make check-boundaries`, `make test`
- Export committed OpenAPI: `make openapi-export`
- Regenerate API-derived web types: `make openapi-types`
- Verify contract drift: `make check-openapi`
- Full local gate: `make verify`

## Placement rules
- Keep business logic in Python, not in the frontend, database views, SQL triggers, or migrations.
- Preserve modular-monolith boundaries. Cross-module work should go through public facades and explicit orchestrators.
- Keep the write model authoritative and treat projections or read models as derived data.
- Route handlers should own HTTP semantics only; do not move workflow rules into routers.
- Repositories and query services may use raw SQL, but ownership still follows the module map.

## Python conventions
- no `from __future__ import annotations` unless necessary
- prefer PEP 695 modern typing
- prefer `Annotated`
- prefer `typer` over `argparse`
- update related docstrings with Google style when code changes
- use `is` for enum identity comparisons; use `==` only when intentional value-level comparisons
- prefer `Sequence[T]` to `tuple[T, ...]`

## Backend-specific validation expectations
- Pure domain logic: add or update unit tests.
- DB-backed behavior, projections, or transactions: add or update integration tests against real PostgreSQL.
- Live entry or realtime behavior: add or update targeted integration coverage where the state and conflict semantics live.
- API contract change: update committed OpenAPI, generated client types, and any affected API docs.
- Critical user-visible flow change: update the relevant acceptance scenario and, if automated in browser, the relevant E2E flow.

## Backend-specific stop rules
- Do not bypass module boundaries for convenience.
- Do not silently change error codes or API shapes.
- Do not let read-model shortcuts become sources of truth.
- Do not mix unrelated refactors into correctness-sensitive changes.
