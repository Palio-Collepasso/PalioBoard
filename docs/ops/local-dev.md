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
- **Other tools:** `make`, `curl`, `pre-commit`

## Quick Start

1. Open the repo and inspect the stable command surface with `make help`.
2. Install frontend dependencies with `cd apps/web && npm install`.
3. Install Git hooks from `apps/api` with `uv run --group dev pre-commit install --hook-type pre-commit --hook-type pre-push`.
4. Install the Playwright Chromium browser once from `apps/web` with `npm run e2e:install`.
5. Configure backend env vars only when you need non-default runtime or test DB settings.
6. Start the backend with `make backend-dev` and the frontend with `make web-dev` for the native hot-reload loop, or use `make up` for the same-origin smoke stack.
7. Apply migrations explicitly before workflows that need the schema.
8. Verify health with `curl http://127.0.0.1:8080/healthz` or the equivalent backend-local endpoint.

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
| `PALIO_TEST_POSTGRES_URL` | no | disposable Postgres test container matching `infra/compose/docker-compose.yml` | backend integration tests | Reuses an existing local admin database for integration tests |
| `PALIO_TEST_POSTGRES_IMAGE` | no | DB image from `infra/compose/docker-compose.yml` | backend integration tests | Overrides the image used by the disposable integration-test database |

## Commands

### Install

```bash
cd apps/web && npm install
cd ../api && uv run --group dev pre-commit install --hook-type pre-commit --hook-type pre-push
cd ../web && npm run e2e:install
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

### Run quality gates

```bash
make format
make lint
make typecheck
make check-boundaries
make check-openapi
make build
make verify
```

## Common Workflows

### Start from scratch

1. Follow [Quick Start](#quick-start)
2. Choose either:
  - the native loop: `make backend-dev`, `make web-dev`, or
  - the same-origin smoke path: `make up` plus the one-shot `migrate` service.

### Reset local database

1. Stop the stack with `make down`.
2. Recreate the stack with `make up`, then rerun `docker compose -f infra/compose/docker-compose.yml --profile ops run --rm migrate`.

### Apply migrations

1. Set `PALIO_DB_MIGRATION_URL` for the target database when running locally without Compose.
2. Run `cd apps/api && uv run alembic upgrade head` or use the profiled Compose `migrate` service.

### Seed local data

1. No shared seed workflow is documented yet.
2. Until a shared seed workflow is established, keep data setup local to the change and document reusable scenarios in `docs/testing/fixtures.md`.

### Run a specific test

1. Use `cd apps/api && uv run --group dev pytest tests/unit` or `cd apps/api && uv run --group dev pytest tests/integration` for backend layers.
2. Use `cd apps/web && npm test -- --watch=false` for frontend behavior tests or `cd apps/web && npm run e2e` for the browser smoke suite.

### Run the Git hooks manually

1. Use `cd apps/api && uv run --group dev pre-commit run --all-files --hook-stage pre-commit` for the fast local hooks.
2. Use `cd apps/api && uv run --group dev pre-commit run --all-files --hook-stage pre-push` for the heavier type/test/build/OpenAPI path.

## Verification Checklist

- [ ] App starts successfully
- [ ] DB/services reachable
- [ ] Health endpoint works
- [ ] Frontend loads
- [ ] `make verify` passes
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

### Git hooks fail because `pre-commit` is unavailable or not installed

- **Symptoms:**
  - `.git/hooks/pre-commit` or `.git/hooks/pre-push` exits immediately
  - `uv run --group dev pre-commit ...` fails before the repo checks run
- **Likely cause:** The backend dev tooling group was not installed through `uv run`, or the hooks were never installed for this clone/worktree.
- **How to diagnose:**
  - Re-run `cd apps/api && uv run --group dev pre-commit --version`
  - Check whether `.git/hooks/pre-commit` and `.git/hooks/pre-push` exist
- **How to fix:**
  1. Run `cd apps/api && uv run --group dev pre-commit install --hook-type pre-commit --hook-type pre-push`.
  2. Re-run the desired hook stage with `uv run --group dev pre-commit run --all-files --hook-stage ...`.
- **Prevention:** Install the hooks as part of the initial local bootstrap.

### `make check-openapi` fails after backend or contract changes

- **Symptoms:**
  - `make check-openapi` exits non-zero
  - `docs/api/openapi.yaml` changes unexpectedly after export
- **Likely cause:** The committed OpenAPI artifact is stale, or frontend type generation cannot complete from the committed spec.
- **How to diagnose:**
  - Run `make openapi-export`
  - Inspect `git diff -- docs/api/openapi.yaml`
  - Re-run `make openapi-types`
- **How to fix:**
  1. Regenerate the spec with `make openapi-export` and review the diff.
  2. Ensure `cd apps/web && npm install` has been run, then rerun `make openapi-types`.
- **Prevention:** Keep contract changes and `docs/api/openapi.yaml` updates in the same change.

---

## FAQ

Template for each FAQ entry: `docs/templates/ops/local-dev-faq-item.template.md`

### Should I use Docker Compose for daily frontend and backend coding?

Use native `make backend-dev` and `make web-dev` for the normal hot-reload loop. Keep full Compose runs for same-origin verification and production-like smoke checks.

### Are migrations run automatically by `make up`?

No. The architecture keeps migrations explicit, so run the profiled `migrate` service or `alembic upgrade head` yourself.

### Which command should I run before opening a PR?

Run `make verify` from the repo root. That matches the full local quality-gate baseline behind the installed Git hooks and CI workflow.
