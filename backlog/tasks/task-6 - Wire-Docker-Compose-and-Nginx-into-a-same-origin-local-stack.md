---
id: TASK-6
title: Wire Docker Compose and Nginx into a same-origin local stack
status: Done
assignee:
  - '@codex'
created_date: '2026-03-12 01:37'
updated_date: '2026-03-14 19:38'
labels: []
milestone: m-0
dependencies:
  - TASK-3
  - TASK-4
  - TASK-5
documentation:
  - docs/architecture/architecture.md
  - docs/qna/architecture/deployment and operations.md
parent_task_id: M-0
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add the local infrastructure needed to boot the stack behind one origin, including Compose services and Nginx routing for SPA paths, `/api`, and later `/realtime`.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Docker Compose can boot the baseline local stack with PostgreSQL and the application-facing containers needed for M1 verification.
- [x] #2 Nginx serves the SPA and proxies backend requests through one origin using the documented route split.
- [x] #3 The backend and frontend skeletons are both reachable through the same-origin proxy in a local smoke run.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Proposed implementation plan for TASK-6 (awaiting user approval before coding):

1. Resolve the API route-prefix contract before wiring the proxy. There is a material mismatch between `docs/qna/architecture/api and contracts.md` and `docs/architecture/adr/ADR-0007-api-and-contract-strategy.md` (which say `/admin/...` and `/public/...`) versus the current architecture doc, task wording, OpenAPI artifact, backend routes, frontend services, and tests (which use `/api/admin/...` and `/api/public/...`). Confirm the intended contract with the user, then update the stale docs in the same change so the proxy config, API contract, and documentation all agree.

2. Populate the reserved infrastructure layout under `infra/` with the minimal assets needed for a same-origin smoke stack:
- `infra/compose/docker-compose.yml` for the local stack services.
- `infra/docker/` image definitions for the backend runtime and the Nginx image that serves the built SPA.
- `infra/nginx/` config for SPA fallback plus backend proxy routing.
Keep the shape aligned with the approved `infra/{docker,nginx,compose}` structure in the architecture docs.

3. Containerize the backend as a thin runtime image without changing the application ownership boundaries. The API container should run the existing FastAPI app, expose an internal HTTP port, receive `PALIO_*` settings through environment variables, and point `PALIO_DB_RUNTIME_URL` at the Compose Postgres service. Keep schema evolution out of the backend startup path: migrations remain an explicit step, implemented either as a documented one-shot Compose command/service or an equivalent clearly separated workflow.

4. Package the Angular SPA for static same-origin delivery through Nginx instead of introducing a separate long-running frontend container. Build the existing `apps/web` SPA into static assets during the image build, copy those assets into the Nginx image, and rely on the current relative `/api/...` and `/realtime/...` frontend base paths so no extra runtime config layer is introduced in this task.

5. Configure Nginx to be the single local origin. It should:
- serve the SPA with `index.html` fallback for client routes such as `/`, `/public/...`, `/admin/...`, and `/maxi/...`;
- proxy `/api/...` to the backend;
- proxy `/realtime/...` with headers/settings that are safe for the current HTTP health route and future SSE/WebSocket traffic;
- surface backend readiness/health smoke checks through the same origin.

6. Make the top-level developer workflow real without disturbing the native hot-reload workflow documented elsewhere. `make up` and `make down` should start/stop the Compose stack via the reserved `infra/compose/docker-compose.yml`, while `make backend-dev` and `make web-dev` remain the preferred day-to-day native commands. The compose stack is for M1 verification and production-like smoke runs, not for replacing the documented native loop.

7. Update the affected docs and tracked-change notes in the same change so the repository truth matches the implementation. Expected touch points are `README.md`, `docs/ops/local-dev.md`, `infra/README.md`, and `REDLINING.md`, plus the conflicting API-contract/Q&A/ADR docs from step 1 if that contract is confirmed. Update app-specific READMEs only where their current guidance becomes stale.

8. Validate the slice with narrow but real same-origin smoke checks. At minimum, verify that the Compose stack builds and boots, the SPA is reachable through Nginx, and the placeholder backend surfaces respond through the proxy at `/api/admin/health`, `/api/public/health`, `/realtime/health`, and the operational endpoints. If the `/realtime` proxy is configured with upgrade support in this slice, include a minimal websocket handshake check against `/realtime/ws`; otherwise leave broader realtime/browser coverage to later tasks.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Research completed before planning: reviewed Backlog workflow overview and task-execution guidance; TASK-3/TASK-4/TASK-5 dependency context; `docs/architecture/architecture.md`; `docs/architecture/adr/ADR-0001-system-boundary-and-core-stack.md`, `ADR-0007-api-and-contract-strategy.md`, and `ADR-0008-deployment-and-operational-model.md`; `docs/qna/architecture/deployment and operations.md`, `api and contracts.md`, and `realtime and live entry.md`; `docs/qna/data/schema and migrations.md`; `docs/ops/local-dev.md`; `docs/testing/test-strategy.md`; `docs/product/acceptance-scenarios.md`; `docs/milestones.md`; `README.md`; `infra/README.md`; `apps/api/README.md`; `apps/web/README.md`; the top-level `Makefile`; and the current API/web bootstrap code plus smoke tests.

Current repo findings: `make up`/`make down` already reserve `infra/compose/docker-compose.yml`; `infra/README.md` already reserves `infra/{compose,nginx,docker}`; no Dockerfiles or Compose/Nginx assets exist yet; the frontend already uses relative `/api/...` and `/realtime/...` paths; the backend already exposes `/healthz`, `/readyz`, `/version`, `/api/admin/health`, `/api/public/health`, `/realtime/health`, and `/realtime/ws`; and the architecture/local-dev docs explicitly keep native FastAPI/Angular dev as the default day-to-day loop while allowing full Compose runs for production-like verification.

Material documentation conflict found during research: `docs/qna/architecture/api and contracts.md` and `docs/architecture/adr/ADR-0007-api-and-contract-strategy.md` describe backend surfaces as `/admin/...` and `/public/...`, but the architecture doc, TASK-6 wording, OpenAPI artifact, backend implementation/tests, and frontend services consistently use `/api/admin/...` and `/api/public/...`. This affects the Nginx route split for TASK-6, so it must be resolved explicitly before implementation.

User approved the implementation plan on 2026-03-14 and clarified that the proxy/API contract should use `/api/admin/...` plus the existing `/api/public/...` route shape. Proceeding with implementation under that contract and treating the `/api/pulic` message as a typo because it conflicts with the current codebase and task wording.

Implemented TASK-6 by adding `.dockerignore`, `infra/compose/docker-compose.yml`, `infra/docker/api.Dockerfile`, `infra/docker/nginx.Dockerfile`, and `infra/nginx/default.conf`. The stack now runs PostgreSQL plus an API container and an Nginx container that builds and serves the Angular SPA through one local origin at `http://127.0.0.1:8080`. The Compose file also adds a profiled one-shot `migrate` service so Alembic stays explicit and out of backend startup.

Updated the repo docs to match the new local-stack truth in `README.md`, `docs/ops/local-dev.md`, `infra/README.md`, and `REDLINING.md`, and corrected the stale API-surface wording in `docs/qna/architecture/api and contracts.md`, `docs/architecture/adr/ADR-0007-api-and-contract-strategy.md`, and `docs/_raw/architecture qna.md` so they now match `/api/admin/...`, `/api/public/...`, and `/realtime/...`.

Validation required two incidental baseline repairs discovered while exercising TASK-6: `apps/api/src/palio/db/config.py` now re-exports the DB constants still expected by the existing backend tests, and the frontend Angular dependency set was pinned/refreshed in `apps/web/package.json` plus `apps/web/package-lock.json` so `npm ci` succeeds in the Docker/Nginx build and the npm audit warning is cleared (`npm audit` now reports zero vulnerabilities).

Validation completed with `docker compose -f infra/compose/docker-compose.yml config`, `cd apps/api && uv run pytest`, `cd apps/web && npm run build`, `cd apps/web && npm run check-boundaries`, `cd apps/web && npm audit --json` (0 vulnerabilities), `docker compose -f infra/compose/docker-compose.yml build api nginx`, `docker compose -f infra/compose/docker-compose.yml up -d`, `docker compose -f infra/compose/docker-compose.yml --profile ops run --rm migrate`, and same-origin smoke requests to `/healthz`, `/readyz`, `/version`, `/api/admin/health`, `/api/public/health`, `/realtime/health`, `/`, and `/admin` before bringing the stack back down.

User requested follow-up investigation/fix for severe vulnerabilities reported on the Docker Nginx image used in TASK-6. Starting a focused hardening pass on the local-stack container choice and image contents.

Follow-up hardening after initial completion: the runtime stage in `infra/docker/nginx.Dockerfile` now uses `nginx:1.29.4-alpine3.23-slim` instead of `nginx:1.27-alpine` to reduce the severe vulnerability exposure reported on the older image. Docker Scout was available locally but could not produce a signed quickview/CVE report without Docker Hub authentication, so the fix used a newer slim official Nginx base plus a rebuilt/smoke-tested stack rather than an authenticated CVE export.

Post-hardening validation: rebuilt `compose-nginx`, restarted the stack, confirmed `/admin` still serves the Angular SPA and `/api/admin/health` still proxies correctly through Nginx, then brought the stack back down.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added the first same-origin local stack under `infra/` so Docker Compose now boots PostgreSQL, the FastAPI container, and an Nginx container that builds and serves the Angular SPA behind one local origin at `http://127.0.0.1:8080`. Nginx proxies `/healthz`, `/readyz`, `/version`, `/api/...`, and `/realtime/...`, while SPA routes such as `/`, `/admin`, `/public`, and `/maxi` fall back to the Angular `index.html`.

Kept migrations explicit by adding a profiled one-shot `migrate` service instead of hiding Alembic inside backend startup, and updated the repo docs plus the stale API-surface ADR/Q&A text so the documented contract now matches the implemented `/api/admin/...`, `/api/public/...`, and `/realtime/...` paths.

To make the TASK-6 validation honest, I also fixed two pre-existing baseline issues uncovered during the smoke run: the backend DB-config module now re-exports the constants that the current tests import, and the frontend Angular dependency set is pinned/refreshed so `npm ci` works inside the Docker/Nginx build and `npm audit` reports zero vulnerabilities.
<!-- SECTION:FINAL_SUMMARY:END -->
