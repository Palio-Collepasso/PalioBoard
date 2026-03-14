---
id: TASK-5
title: 'Add env-based settings, JSON logging, and operational health/version endpoints'
status: Done
assignee:
  - '@codex'
created_date: '2026-03-12 01:37'
updated_date: '2026-03-14 17:09'
labels: []
milestone: m-0
dependencies:
  - TASK-2
documentation:
  - docs/architecture/architecture.md
  - docs/qna/architecture/deployment and operations.md
parent_task_id: M-0
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add the runtime settings and operational baseline expected by the architecture, including typed env-based configuration, structured logging, correlation-id propagation, and the minimal health/version endpoints.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Backend runtime configuration is driven by typed environment settings rather than hard-coded values.
- [x] #2 HTTP requests emit structured JSON logs that include a request or correlation identifier suitable for local debugging and production operations.
- [x] #3 The backend exposes liveness, readiness, and build/version endpoints that can be consumed by Compose, Nginx, and CI smoke checks.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Introduce a centralized typed settings layer in `apps/api/src/palio/app/settings.py` and thread it through the composition root so runtime behavior is driven by environment variables instead of scattered `os.getenv` calls. This should cover the existing database URLs plus the minimal app/logging/build metadata needed by TASK-5, while keeping `.env` support limited to local development and preserving the explicit migration-vs-runtime split already established in `palio.db.config` and `apps/api/migrations/env.py`.
2. Add an application observability module and HTTP middleware that configures structured JSON logging once, creates or propagates a request/correlation id per request, returns that id in the response header, and emits one request log event with method, path, status, and duration. Expose the correlation id through a small shared helper/context so later audit and realtime work can reuse the same primitive without reshaping the baseline.
3. Replace the current scaffold-only health contract with the documented operational endpoints at the app root: keep `/healthz` as liveness, add `/readyz` for readiness, and add a small `/version` build/version endpoint backed by package/build metadata from settings. Keep readiness honest by reflecting runtime DB availability instead of forcing startup failure when the DB is absent, and leave the realtime websocket placeholder intact.
4. Update the backend smoke tests and contract artifacts at TASK-5 scope: add coverage for typed settings resolution, liveness/readiness/version responses, and correlation-id logging/header behavior; update the OpenAPI export test and committed `docs/api/openapi.yaml` to match the new operational surface. Keep the readiness checks testable without expanding into TASK-8’s full live-Postgres harness.
5. Update all docs whose current truth would change, at minimum `apps/api/README.md`, `README.md`, `docs/ops/local-dev.md`, and any architecture/Q&A text that now needs concrete env keys or endpoint names. If the new settings surface is large enough to justify it, add the corresponding `.env.example` template/documentation in the same change rather than leaving the local-dev story implicit.
6. Validate the slice with the narrowest honest checks for this task: backend pytest coverage, OpenAPI export, and a local app smoke path under explicit env settings. Do not absorb TASK-6 infrastructure work or TASK-8’s broader backend harness into this change.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Research completed before planning: reviewed the Backlog workflow overview and task-execution guide, TASK-5 and adjacent TASK-2/TASK-4/TASK-8 context, `apps/api/AGENTS.md`, `docs/architecture/architecture.md`, `docs/architecture/adr/ADR-0008-deployment-and-operational-model.md`, `docs/qna/architecture/deployment and operations.md`, `docs/qna/architecture/api and contracts.md`, `docs/qna/architecture/consistency and projections.md`, `docs/product/functional-requirements.md`, `docs/testing/test-strategy.md`, `docs/ops/local-dev.md`, `docs/milestones.md`, `README.md`, and the current `apps/api` scaffold.

Created the dedicated worktree at `/home/simone/codex-worktrees/palio-board/tasks/task-5-add-env-based-settings-json-logging-and-operational-health-version-endpoints` on branch `tasks/task-5-add-env-based-settings-json-logging-and-operational-health-version-endpoints`.

Current scaffold findings: backend configuration is still split across narrow DB helpers in `apps/api/src/palio/db/config.py` with direct environment access; there is no typed settings object, no JSON logging setup, no correlation-id middleware/context helper, and no readiness or build/version endpoint yet. The current app only exposes `/healthz` plus placeholder `/api/admin/health`, `/api/public/health`, and `/realtime/health` routes.

Scope boundary confirmed from adjacent tasks: TASK-4 intentionally stopped at DB-specific env access and deferred broad typed settings/logging/operational endpoints to TASK-5. TASK-8 owns the fuller live-Postgres backend test harness, so TASK-5 should keep readiness/logging validation honest without turning into the larger integration-test task.

No coding or dependency changes have started yet. Plan recorded here for user review; waiting for explicit approval before implementation.

User changed the workflow on 2026-03-14: the dedicated worktree was removed, and TASK-5 is now attached to the normal repo branch `tasks/task-5-add-env-based-settings-json-logging-and-operational-health-version-endpoints` in `/home/simone/projects/palio`.

Implemented the typed backend settings layer in `apps/api/src/palio/settings.py` and threaded it through `palio.app.bootstrap`, `palio.db.config`, and the operational endpoints so runtime behavior no longer depends on scattered direct environment lookups.

Added `palio.app.observability` with JSON log formatting, request-id context propagation, HTTP request logging middleware, and disabled the default unstructured Uvicorn access log stream. HTTP responses now echo the configured request-id header and request completion/failure logs include method/path/status/duration metadata.

Added `/readyz` and `/version` while keeping `/healthz` as liveness, plus a DB-backed readiness probe in `palio.db.runtime`. Updated backend smoke tests, OpenAPI export expectations, `docs/api/openapi.yaml`, `apps/api/README.md`, `README.md`, `docs/ops/local-dev.md`, and `REDLINING.md` to match the new baseline.

Validation completed from the current branch with `cd apps/api && uv run pytest` and `make openapi-export`; both passed after adding the explicit `503` OpenAPI response for `/readyz`.

User requested a follow-up refinement on 2026-03-14 before final acceptance: replace hardcoded HTTP status numbers with FastAPI status constants, switch structured logging implementation to Loguru, and require UUIDv7 for generated request ids.

Applied the requested follow-up refinement on 2026-03-14: replaced hardcoded readiness HTTP status numbers with `fastapi.status` constants, swapped the custom stdlib JSON formatter for Loguru structured logging, and changed generated request ids from UUIDv4-style values to UUIDv7 via `uuid6.uuid7()`.

Updated backend dependencies/lockfile to include `loguru` and `uuid6`, adjusted request-logging tests to assert Loguru JSON payloads plus UUIDv7 request ids, and reran `cd apps/api && uv run pytest` plus `make openapi-export` successfully after the change.

Post-review refactor on 2026-03-14: split request-context config out of `LoggingSettings` into `RequestContextSettings`, stopped loading settings inside `palio.db.config`/`palio.db.runtime`, moved liveness/readiness/version into `palio.app.routes.meta`, and split the old monolithic observability module into `palio.app.observability.logging`, `.request_context`, and `.request_logging` while keeping middleware registration centralized in `palio.app.factory`.

Validation rerun after the structural refactor: `cd apps/api && uv run pytest` and `make openapi-export` both still pass.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented TASK-5 by adding a typed backend settings layer, JSON HTTP request logging with propagated request ids, and the operational `/healthz`, `/readyz`, and `/version` endpoints. The FastAPI composition root now loads typed settings once, reuses them for runtime DB configuration and build metadata, and emits structured request logs instead of relying on ad hoc environment reads or unstructured access logs.

Added a DB-backed readiness probe to `palio.db.runtime`, kept liveness separate at `/healthz`, and exposed build/runtime version metadata at `/version`. The committed OpenAPI artifact and backend smoke tests were updated to cover the new operational surface, including the `503` readiness contract and request-id/header behavior.

Updated the affected docs (`apps/api/README.md`, `README.md`, `docs/ops/local-dev.md`, `REDLINING.md`) so the current env vars, logging behavior, and operational endpoints are documented alongside the implementation. Validation run: `cd apps/api && uv run pytest` and `make openapi-export`.

Follow-up refinement requested after review: the backend now uses `fastapi.status` constants for readiness responses, Loguru for native JSON structured request logging, and UUIDv7 for generated request identifiers. The dependency lockfile and docs were updated accordingly, and the existing backend/OpenAPI validation commands still pass.
<!-- SECTION:FINAL_SUMMARY:END -->
