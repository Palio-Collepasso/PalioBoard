# Infrastructure

This directory is the canonical home for local and deployment-facing infrastructure assets.

Current ownership:
- `compose/` for Docker Compose files, including the baseline same-origin local stack at `compose/docker-compose.yml`
- `nginx/` for same-origin reverse-proxy configuration
- `docker/` for container build assets

TASK-6 populates the first local-stack baseline:
- PostgreSQL in Docker for the app datastore
- a FastAPI container built from `apps/api/`
- an Nginx container that builds and serves the Angular SPA from `apps/web/`
- same-origin proxying for `/healthz`, `/readyz`, `/version`, `/api/...`, and `/realtime/...`

Typical local commands:
- `make up`
- `docker compose -f infra/compose/docker-compose.yml --profile ops run --rm migrate`
- `make down`
