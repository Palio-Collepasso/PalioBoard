# Local development

## Current baseline

TASK-1 established the canonical top-level monorepo layout and the repository `Makefile`.
TASK-2 adds the first runnable backend scaffold under `apps/api/`.
TASK-3 adds the Angular SPA scaffold under `apps/web/`.

At this stage:
- `make help`, `make backend-dev`, `make test-backend`, `make web-dev`, `make openapi-export`, and `make openapi-types` are runnable
- `make test-web` and `make test-e2e` now reach explicit frontend placeholder scripts for TASK-9
- `make up` and `make down` are still reserved entrypoints
- `make test` still fails overall until the web and e2e harnesses land

Backend commands currently available:
- `make backend-dev` starts the placeholder FastAPI app from `apps/api/src/palio/app/main.py`
- `make test-backend` runs the narrow backend smoke suite currently in the scaffold
- `make openapi-export` exports `docs/api/openapi.yaml` directly from the FastAPI app without starting a server
- `cd apps/api && uv run python -m palio.shared.module_boundaries` runs the facade-only import check locally

Frontend commands currently available:
- `cd apps/web && npm install` installs the Angular 21 scaffold dependencies
- `make web-dev` starts the Angular SPA with lazy `/admin`, `/public`, and `/maxi` routes
- `make openapi-types` regenerates ignored TS declarations from the committed `docs/api/openapi.yaml` artifact
- `cd apps/web && npm run generate:api-types` runs the app-local type-generation command
- `cd apps/web && npm run check-boundaries` runs the dependency-cruiser import-boundary check

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

- TASK-6 will add Docker Compose and Nginx assets under `infra/`
- TASK-8 will expand `make test-backend` from scaffold smoke coverage into the full backend harness
- TASK-9 will replace the frontend test/e2e placeholders with the real behavior and Playwright harnesses
- TASK-10 will replace this baseline note with the full local bootstrap and verification guide
