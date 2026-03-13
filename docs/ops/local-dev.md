# Local development

## Current baseline

TASK-1 establishes the canonical top-level monorepo layout and the repository `Makefile`.

At this stage:
- `make help` is the only fully runnable target
- `make up`, `make backend-dev`, `make web-dev`, and the test targets are intentionally reserved entrypoints
- those reserved targets fail fast with a message that points to the milestone task that will make them runnable

## Stable top-level targets

Use these target names going forward:
- `make help`
- `make up`
- `make down`
- `make backend-dev`
- `make web-dev`
- `make test`
- `make test-backend`
- `make test-web`
- `make test-e2e`

## Expected follow-up tasks

- TASK-2 will add the backend application scaffold under `apps/backend/`
- TASK-3 will add the Angular scaffold under `apps/web/`
- TASK-6 will add Docker Compose and Nginx assets under `infra/`
- TASK-8 and TASK-9 will make the test targets runnable
- TASK-10 will replace this baseline note with the full local bootstrap and verification guide
