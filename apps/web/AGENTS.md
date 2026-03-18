# Web / frontend instructions

## Scope
This file applies to frontend work under `apps/web/`.

Follow `docs/README.md` for:
- documentation source precedence
- base reading sets by task type
- archive policy
- the authoritative status of `docs/ui/*` proposal docs

This file adds **frontend-only deltas**.

## Frontend-specific extra reads
For frontend work, also read only the relevant subset of:
- `docs/ui/*` proposal docs for the task
- `docs/product/acceptance-scenarios.md` when the change affects an observable workflow
- `docs/api/README.md` / `docs/api/openapi.yaml` / `docs/api/error-contract.md` when the page depends on API data

## Core frontend rules
- Keep business rules in backend-owned docs and backend code.
- Frontend code owns rendering, interaction wiring, local UI state, and user feedback only.
- Do not invent API shapes; use committed OpenAPI and API docs.
- If a UI proposal implies behavior not supported by authoritative docs, flag it instead of implementing it.
- If the user-visible workflow changes, update the relevant acceptance scenario and browser tests when appropriate.

## Stable frontend commands
- Unit or component tests: `make test-web`
- E2E tests: `make test-e2e`
- Repo-level verification: `make lint`, `make typecheck`, `make test`, `make build`, `make verify`
