# Local Development

## Purpose
Document the canonical local developer workflow: setup, common commands, environment variables, and high-signal troubleshooting.

## Document boundary
This file owns **local setup and commands**.
It does not own architecture rules, test-depth policy, or deployment procedure.
- Architecture rules live in `docs/architecture/*`.
- Test-depth policy lives in `docs/testing/test-strategy.md`.
- Deployment procedure lives in `docs/ops/deploy.md`.

## Most common commands
Use these first before digging into the longer sections:

- bootstrap local dependencies: `make up`
- stop local dependencies: `make down`
- reset local dependencies and volumes: `make reset`
- apply migrations: `make migrate`
- backend dev server: `make api-dev`
- frontend dev server: `make web-dev`
- repo quality gates: `make lint`, `make typecheck`, `make test`, `make verify`
- export OpenAPI: `make openapi-export`
- verify contract drift: `make check-openapi`

## Requirements
- Docker and Docker Compose support
- Python and `uv` for backend development
- Node.js and npm for frontend development
- repo `.env` values required by the current stack

## Quick start
1. Start local infrastructure with `make up`.
2. Apply migrations with `make migrate`.
3. Start the backend with `make api-dev`.
4. Start the frontend with `make web-dev`.
5. Verify the stack with `/healthz`, `/readyz`, `/version`, `/api/public/health`, and `/realtime/health`.

## Environment variables
Keep the authoritative local values in the repo `.env` and compose files.
Document at least these variables when they change:
- database connection values
- frontend origin / backend API origin
- Supabase Auth integration values used locally
- build/version metadata used by `/version`

## Command reference
### Backend
- unit tests: `make test-api-unit`
- integration tests: `make test-api-integration`
- run git hooks manually: `cd apps/api && uv run --group dev pre-commit run --all-files --hook-stage pre-commit`
- pre-push equivalent: `cd apps/api && uv run --group dev pre-commit run --all-files --hook-stage pre-push`

### Frontend
- unit/component tests: `make test-web`
- browser E2E: `make test-e2e`

### Repo-level verification
- `make format`
- `make format-check`
- `make lint`
- `make typecheck`
- `make check-boundaries`
- `make check-openapi`
- `make test`
- `make build`
- `make verify`

## Common workflows
### Start from scratch
1. `make down`
2. `make reset`
3. `make up`
4. `make migrate`
5. start the app processes with `make api-dev` and `make web-dev`

### Apply a schema change locally
1. update the migration
2. run `make migrate`
3. run the relevant backend integration tests
4. run `make check-openapi` if the API contract changed

### Verify a PR before review
1. run the narrowest honest tests for the change
2. run `make lint`, `make typecheck`, and `make check-openapi` when relevant
3. run `make verify` before opening or updating the PR when the change is broad enough to justify it

## Verification checklist
- [ ] `/healthz` responds
- [ ] `/readyz` is healthy after migrations
- [ ] `/version` reports build metadata
- [ ] frontend shell loads through the same-origin path
- [ ] `/api/public/health` and `/realtime/health` respond
- [ ] required tests for the change pass

## Troubleshooting
### Backend readiness stays unhealthy
Check:
1. the migration state with `make migrate`
2. backend logs from the running process or compose stack
3. DB connectivity and credentials in the local environment
4. whether the latest schema matches the code expectations

### Protected admin routes keep returning `401`
Check:
1. whether the bearer token is present
2. whether the local auth values are configured correctly
3. whether the identity resolves to a linked application user
4. `docs/api/error-contract.md` for `unauthenticated` semantics

### Browser smoke tests cannot reach the shell routes
Check:
1. frontend dev server availability
2. same-origin proxy wiring in the local stack
3. backend/public health endpoints
4. the E2E flow notes in `docs/testing/critical-e2e-flows.md`

### `make check-openapi` fails
Check:
1. whether the backend endpoint/status shape changed
2. whether `make openapi-export` was run after the change
3. whether generated consumer types need regeneration
4. `docs/api/README.md` for contract workflow expectations

## FAQ
### Which commands are the canonical entrypoints?
Use the repo `make` targets first. Drop to app-level commands only when you need a narrower loop.

### Are migrations run automatically by `make up`?
No. Keep migrations explicit with `make migrate` so failures stay visible.

### Which command should I run before opening a PR?
Run the narrowest honest checks for the change, then the repo-level verification steps needed by that risk, ending with `make verify` for broader changes.
