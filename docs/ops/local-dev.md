# Local Development

## Purpose

Explain how to set up, run, and troubleshoot the project locally.

## Audience

- new contributors
- regular developers
- reviewers reproducing a change locally

## Requirements

- **OS:** Linux or macOS are the current baseline; other environments are not yet documented.
- **Runtime(s):** Python 3.12+, Node.js LTS, Docker Engine with Compose v2
- **Package manager(s):** `uv`, `npm`
- **Database/services:** PostgreSQL via Docker or the same-origin Compose stack
- **Other tools:** `make`, `curl`

## Quick Start

1. Open the repo and inspect the stable command surface with `make help`.
2. Install frontend dependencies with `cd apps/web && npm install`.
3. Configure backend env vars only when you need non-default runtime or test DB settings.
4. Start the backend with `make backend-dev` and the frontend with `make web-dev` for the native hot-reload loop, or use `make up` for the same-origin smoke stack.
5. Apply migrations explicitly before workflows that need the schema.
6. Verify health with `curl http://127.0.0.1:8080/healthz` or the equivalent backend-local endpoint.

## Environment Variables

| Variable | Required | Default | Used by | Description |
|---|---|---|---|---|
| `PALIO_ENV` | no | `development` | backend runtime | Selects typed runtime settings |
| `PALIO_LOG_LEVEL` | no | app default | backend runtime | Controls JSON log verbosity |
| `PALIO_REQUEST_ID_HEADER` | no | `X-Request-ID` | backend runtime | Overrides the propagated request-id header name |
| `PALIO_BUILD_VERSION` | no | app default | backend runtime | Overrides `/version` output |
| `PALIO_BUILD_COMMIT_SHA` | no | unset | backend runtime | Adds build metadata to `/version` |
| `PALIO_DB_RUNTIME_URL` | yes for DB-backed runtime paths | unset | backend runtime | Runtime database connection string |
| `PALIO_DB_MIGRATION_URL` | yes for migrations | unset | Alembic and migrate workflow | Admin/migration database connection string |
| `PALIO_TEST_POSTGRES_URL` | no | disposable local Docker Postgres | backend integration tests | Reuses an existing local admin database for integration tests |
| `PALIO_TEST_POSTGRES_IMAGE` | no | `postgres:16-alpine` | backend integration tests | Overrides the Docker image used by the disposable integration-test database |

## Commands

### Install

```bash
cd apps/web && npm install
```

### Start dependencies

```bash
make up
docker compose -f infra/compose/docker-compose.yml --profile ops run --rm migrate
```

### Run backend

```bash
make backend-dev
```

### Run frontend

```bash
make web-dev
```

### Run tests

```bash
make test
```

### Run lint / type checks

```bash
cd apps/api && uv run python -m palio.shared.module_boundaries
cd apps/web && npm run check-boundaries
cd apps/web && npm run typecheck
```

## Common Workflows

### Start from scratch

1. Run `make help`, `cd apps/web && npm install`, and confirm `uv` is available for backend commands.
2. Use the native loop (`make backend-dev`, `make web-dev`) for day-to-day work, or `make up` plus the one-shot `migrate` service for same-origin smoke verification.

### Reset local database

1. Stop the stack with `make down`.
2. Recreate the stack with `make up`, then rerun `docker compose -f infra/compose/docker-compose.yml --profile ops run --rm migrate`.

### Apply migrations

1. Set `PALIO_DB_MIGRATION_URL` for the target database when running locally without Compose.
2. Run `cd apps/api && uv run alembic upgrade head` or use the profiled Compose `migrate` service.

### Seed local data

1. No shared seed workflow is documented yet.
2. Until a task establishes one, keep data setup task-local and document reusable scenarios in `docs/testing/fixtures.md`.

### Run a specific test

1. Use `cd apps/api && uv run pytest tests/unit` or `cd apps/api && uv run pytest tests/integration` for backend layers.
2. Use `cd apps/web && npm test -- --watch=false` for frontend behavior tests or `cd apps/web && npm run e2e` for the browser smoke suite.

## Verification Checklist

- [ ] App starts successfully
- [ ] DB/services reachable
- [ ] Health endpoint works
- [ ] Frontend loads
- [ ] Tests can run locally

## Troubleshooting

Template for each troubleshooting entry: `docs/templates/ops/local-dev-troubleshooting-item.template.md`

### Backend readiness stays unhealthy

- **Symptoms:**
  - `/readyz` returns `503`
- **Likely cause:** The runtime DB is unavailable or migrations have not been applied.
- **How to diagnose:**
  - Check `PALIO_DB_RUNTIME_URL`
  - Run the one-shot migrate command and inspect backend logs
- **How to fix:**
  1. Ensure the DB service is reachable.
  2. Apply migrations explicitly before retrying readiness checks.
- **Prevention:** Keep the migration step explicit in local verification notes.

### Playwright smoke tests cannot reach the shell routes

- **Symptoms:**
  - `npm run e2e` fails on `/`, `/admin`, `/public`, or `/maxi`
- **Likely cause:** The same-origin stack is not up or the SPA build/proxy path is stale.
- **How to diagnose:**
  - Confirm `make up` succeeded
  - Curl `/healthz` and open the shell routes manually
- **How to fix:**
  1. Restart the stack.
  2. Rebuild or rerun the smoke path after the proxy and SPA are healthy.
- **Prevention:** Keep local stack verification tied to `docs/testing/critical-e2e-flows.md`.

---

## FAQ

Template for each FAQ entry: `docs/templates/ops/local-dev-faq-item.template.md`

### Should I use Docker Compose for daily frontend and backend coding?

Use native `make backend-dev` and `make web-dev` for the normal hot-reload loop. Keep full Compose runs for same-origin verification and production-like smoke checks.

### Are migrations run automatically by `make up`?

No. The architecture keeps migrations explicit, so run the profiled `migrate` service or `alembic upgrade head` yourself.
