# Local Development

## Purpose

Explain how to run PalioBoard locally for day-to-day development, debugging, and review.

This starter is tailored to the approved architecture:
- PostgreSQL runs locally in Docker;
- FastAPI and Angular run natively during development;
- the backend is the only business/data API;
- public/maxi/admin behavior should all be testable from the local environment.

## Audience

- contributors implementing features
- reviewers reproducing a PR locally
- operators debugging non-production issues

## Local architecture summary

- **Backend:** FastAPI
- **Frontend:** Angular SPA with admin/public/maxi shells
- **Database:** PostgreSQL
- **Identity:** Supabase Auth in production; local development may use a local/dev-compatible auth setup
- **Reverse proxy in production:** Nginx
- **Preferred local model:** Postgres in Docker, application processes run natively

## Repository-specific TODOs

Replace the placeholder commands and paths in this file with the actual repo commands once they are finalized.

## Requirements

- Docker and Docker Compose available locally
- Python toolchain required by the backend
- Node.js toolchain required by the frontend
- access to the required local environment variables/secrets for development

## Quick start

1. Clone the repository and enter the project root.
2. Copy the local environment example files if the repo uses them.
3. Start PostgreSQL and any required support services in Docker.
4. Apply database migrations.
5. Seed the minimal local data needed to log in and exercise core flows.
6. Start the FastAPI backend natively.
7. Start the Angular frontend natively.
8. Verify admin, public, and maxi routes load against the local backend.

## Environment variables

Populate this table with the real variables used by the repo.

| Variable | Required | Default | Used by | Description |
|---|---|---|---|---|
| `DATABASE_URL` | yes | `<none>` | backend | Postgres connection string |
| `APP_ENV` | yes | `local` | backend/web | Environment selector |
| `AUTH_*` | maybe | `<repo-specific>` | backend/web | Local auth integration values |
| `CORS_ORIGIN_*` | maybe | `<repo-specific>` | backend | Local web origin settings |

## Commands

Replace with the real repository commands.

### Install dependencies

```bash
<repo command for backend install>
<repo command for frontend install>
```

### Start local Postgres/support services

```bash
<repo command or docker compose command>
```

### Apply migrations

```bash
<repo command>
```

### Seed local data

```bash
<repo command>
```

### Run backend

```bash
<repo command>
```

### Run frontend

```bash
<repo command>
```

### Run tests

```bash
<repo command>
```

### Run lint / type checks

```bash
<repo command>
```

## Common workflows

### Start from scratch

1. Remove any previous local containers/volumes only if you intentionally want a clean reset.
2. Start local Postgres.
3. Apply migrations.
4. Seed baseline data.
5. Run backend and frontend.

### Reset local database

1. Stop app processes that actively use the DB.
2. Drop/recreate the local Postgres volume or database.
3. Re-apply migrations.
4. Re-seed baseline data.

### Reproduce a critical ranking flow locally

1. Seed the base season and ranking-game fixtures.
2. Log in as a judge/admin-capable user.
3. Start a ranking game.
4. Enter placements and required fields.
5. Complete the game and verify standings/public update.

### Reproduce a live concurrency issue locally

1. Seed or create an in-progress ranking game.
2. Open two authenticated admin sessions.
3. Acquire a lease in session A.
4. Attempt the same edit in session B.
5. Verify lock and stale-write behavior.

## Verification checklist

- [ ] Backend starts and connects to Postgres.
- [ ] Frontend starts and can reach the backend.
- [ ] Admin routes load after login.
- [ ] Public routes load without login.
- [ ] A seeded ranking game can be completed locally.
- [ ] A seeded tournament game can be progressed locally.

## Troubleshooting

### Database connection fails on startup

- **Symptoms:** backend fails to boot or health checks fail because the database is unreachable.
- **Likely cause:** Postgres container is not running, `DATABASE_URL` is wrong, or migrations have not been applied.
- **How to diagnose:**
  - verify Docker containers are running;
  - check backend logs for connection errors;
  - test DB connectivity with the repo’s normal database tooling.
- **How to fix:**
  1. Start or restart the local Postgres container.
  2. Verify the connection string.
  3. Apply migrations.
- **Prevention:** keep a single documented local DB bootstrap path.

### Login works poorly or local auth is misconfigured

- **Symptoms:** admin pages redirect repeatedly, API calls return 401, or local token validation fails.
- **Likely cause:** missing local auth env vars or mismatch between frontend and backend auth configuration.
- **How to diagnose:**
  - inspect backend auth configuration logs;
  - verify frontend environment values;
  - reproduce with a known seeded local user.
- **How to fix:**
  1. Restore the documented local auth variables.
  2. Recreate any required local auth seed data.
  3. Restart both backend and frontend.
- **Prevention:** keep a minimal tested local-auth bootstrap path.

### Live ranking updates do not sync across two browser sessions

- **Symptoms:** second editor does not see lease/conflict feedback or stale state persists.
- **Likely cause:** realtime channel misconfiguration, backend not serving the live transport, or a stale local client build.
- **How to diagnose:**
  - inspect backend realtime logs;
  - verify the live connection is established in both sessions;
  - test with a known in-progress ranking fixture.
- **How to fix:**
  1. Restart backend and frontend.
  2. Clear stale client state.
  3. Recreate the in-progress ranking fixture and retry.
- **Prevention:** keep a reproducible live-collaboration fixture and smoke test.

## FAQ

### Should local development use production-like Docker for the whole stack?

The architecture baseline prefers local Postgres in Docker with FastAPI/Angular run natively for fast iteration. Full-container local runs may still be useful for smoke verification.

### Is zero-downtime behavior required locally?

No. Planned downtime is acceptable in v1, and local workflows should optimize for clarity and iteration speed rather than complex orchestration.
