# Local development

## Current baseline

TASK-1 established the canonical top-level monorepo layout and the repository `Makefile`.
TASK-2 adds the first runnable backend scaffold under `apps/api/`.
TASK-3 adds the Angular SPA scaffold under `apps/web/`.
TASK-4 adds the PostgreSQL + SQLAlchemy + Alembic backend baseline with the empty `palio_board` schema migration.
TASK-5 adds typed backend runtime settings, Loguru-based structured JSON request logging, and the operational `/healthz`, `/readyz`, and `/version` endpoints.
TASK-8 adds the split backend unit/integration harness and the real-Postgres smoke-test baseline.
TASK-6 adds the local same-origin Docker Compose stack under `infra/`.

At this stage:
- `make help`, `make backend-dev`, `make test-backend`, `make web-dev`, `make openapi-export`, and `make openapi-types` are runnable
- `make test-web` and `make test-e2e` now run the frontend behavior and browser smoke harnesses added in TASK-9
- `make up` and `make down` now boot and stop the baseline same-origin Docker Compose stack on `http://127.0.0.1:8080`
- `make test` now depends on the frontend harnesses plus a one-time Playwright browser install in `apps/web`

Backend commands currently available:
- `make backend-dev` starts the placeholder FastAPI app from `apps/api/src/palio/app/main.py`
- `make test-backend` runs `apps/api/tests/unit/` first and then `apps/api/tests/integration/`
- `cd apps/api && uv run pytest tests/unit` runs the fast backend unit/smoke layer directly
- `cd apps/api && uv run pytest tests/integration` runs the Postgres-backed integration smoke layer directly
- `cd apps/api && PALIO_DB_MIGRATION_URL=postgresql+psycopg://... uv run alembic upgrade head` applies the baseline empty-schema migration explicitly
- `docker compose -f infra/compose/docker-compose.yml --profile ops run --rm migrate` applies that same migration inside the local stack
- `make openapi-export` exports `docs/api/openapi.yaml` directly from the FastAPI app without starting a server
- `cd apps/api && uv run python -m palio.shared.module_boundaries` runs the facade-only import check locally

Database configuration currently available:
- `PALIO_ENV` selects the typed runtime environment (`development`, `test`, or `production`)
- `PALIO_LOG_LEVEL` controls backend JSON log verbosity
- `PALIO_REQUEST_ID_HEADER` overrides the HTTP request-id header name (defaults to `X-Request-ID`)
- `PALIO_BUILD_VERSION` overrides the `/version` payload version string
- `PALIO_BUILD_COMMIT_SHA` adds optional build metadata to `/version`
- `PALIO_DB_RUNTIME_URL` is the runtime connection string for normal app access
- `PALIO_DB_MIGRATION_URL` is the Alembic/admin connection string for schema changes
- `PALIO_TEST_POSTGRES_URL` optionally points backend integration tests at an existing local Postgres admin database; when unset, the suite starts a disposable Docker Postgres container
- `PALIO_TEST_POSTGRES_IMAGE` optionally overrides the Docker image used by that disposable integration-test container
- application tables belong to the fixed Postgres schema `palio_board`
- migrations remain an explicit command and are not run automatically on backend startup

Operational backend behavior currently available:
- `/healthz` is the liveness endpoint
- `/readyz` reports DB readiness and returns `503` when the runtime DB is not configured or unavailable
- `/version` returns build/runtime version metadata
- every HTTP response includes a request id header, generated ids use UUIDv7, and backend request logs are emitted as structured JSON through Loguru

Frontend commands currently available:
- `cd apps/web && npm install` installs the Angular 21 scaffold dependencies
- `make web-dev` starts the Angular SPA with lazy `/admin`, `/public`, and `/maxi` routes
- `make openapi-types` regenerates ignored TS declarations from the committed `docs/api/openapi.yaml` artifact
- `cd apps/web && npm run generate:api-types` runs the app-local type-generation command
- `cd apps/web && npm run check-boundaries` runs the dependency-cruiser import-boundary check
- `make test-web` runs `cd apps/web && npm test -- --watch=false`
- `cd apps/web && npm run e2e:install` installs the Chromium browser used by the Playwright smoke suite
- `make test-e2e` runs `cd apps/web && npm run e2e`, reusing `PLAYWRIGHT_BASE_URL` when set and otherwise starting/stopping the local same-origin stack around the smoke run

Compose smoke-run behavior currently available:
- `make up` builds and starts PostgreSQL, the FastAPI container, and the Nginx same-origin proxy
- the same-origin stack is reachable at `http://127.0.0.1:8080`
- `http://127.0.0.1:8080/healthz`, `/readyz`, and `/version` proxy to the backend operational endpoints
- `http://127.0.0.1:8080/api/admin/health`, `/api/public/health`, and `/realtime/health` proxy to the placeholder backend surfaces
- Nginx serves the built SPA and falls back to `index.html` for `/`, `/admin`, `/public`, and `/maxi`
- `/realtime/...` is proxied with upgrade-friendly settings so the placeholder websocket route can stay under the same origin

Compose smoke-run behavior currently available:
- `make up` builds and starts PostgreSQL, the FastAPI container, and the Nginx same-origin proxy
- the same-origin stack is reachable at `http://127.0.0.1:8080`
- `http://127.0.0.1:8080/healthz`, `/readyz`, and `/version` proxy to the backend operational endpoints
- `http://127.0.0.1:8080/api/admin/health`, `/api/public/health`, and `/realtime/health` proxy to the placeholder backend surfaces
- Nginx serves the built SPA and falls back to `index.html` for `/`, `/admin`, `/public`, and `/maxi`
- `/realtime/...` is proxied with upgrade-friendly settings so the placeholder websocket route can stay under the same origin

## Stable top-level targets

Use these target names going forward:
- `make help`
- `make up`
- `make down`
- `make backend-dev`
- `make web-dev`
- `make openapi-export`
- `make openapi-types`
- `make test`
- `make test-backend`
- `make test-web`
- `make test-e2e`

## Expected follow-up tasks

- TASK-10 will replace this baseline note with the full local bootstrap and verification guide
