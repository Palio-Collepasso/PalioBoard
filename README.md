# PalioBoard

Open-source web application for configuring, running, and publishing the Collepasso Palio tournament.

## Current status

This repository is currently an implementation baseline for v1 with the first backend and frontend scaffolds in place.

What is already in the repo:
- approved product scope
- architecture baseline and ADRs
- domain model and rules
- testing strategy
- milestone plan
- backend FastAPI scaffold with explicit module facades and a minimal app factory
- backend PostgreSQL + SQLAlchemy + Alembic baseline with an empty `palio_board` schema migration
- backend unit and real-Postgres integration smoke harnesses under `apps/api/tests/`
- Angular 21 SPA scaffold under `apps/web/`
- a committed OpenAPI export artifact at `docs/api/openapi.yaml`

What is not in the repo yet:
- `.env.example` files
- real backend business workflows and domain tables
- a production-ready end-to-end application stack

That means the repository now has a baseline same-origin local stack for smoke checks, but most application behavior and deeper infrastructure concerns still land in later M0 tasks.


## Overview

PalioBoard is an operations dashboard for the “Palio Collepassese“, where four teams (“rioni“) compete across multiple games and accumulate points toward final standings.

The product supports three competition contexts:
- **Palio**
- **Prepalio**
- **Giocasport**

It is designed for a small operational team that needs:
- fast result entry during live events
- automatic standings calculation
- immediate public visibility
- auditable post-completion changes
- simple self-hosted operations

## v1 scope

The approved v1 scope includes:
- one active season per database
- exactly four teams
- two game formats: `ranking` and fixed 4-team `tournament_1v1`
- automatic leaderboard calculation
- Jolly validation and scoring
- separate public read-only views
- separate maxi-screen mode
- audit logging for authoritative changes
- post-completion review and under-examination flows

The product is intentionally not a generic sports platform. Details live in [docs/product/prd.md](docs/product/prd.md) and [docs/product/functional-requirements.md](docs/product/functional-requirements.md).

## Architecture baseline

PalioBoard follows an approved modular-monolith baseline:
- **Frontend:** Angular SPA
- **Backend:** FastAPI
- **Database:** PostgreSQL
- **Identity provider:** Supabase Auth
- **Edge:** Nginx

Core architectural rules:
- Python is the only business/data API
- official state lives in PostgreSQL
- standings logic lives in the backend, not in the frontend
- authoritative writes, audit, and projection updates succeed or fail together
- realtime draft state is never official truth by itself

See [docs/architecture/architecture.md](docs/architecture/architecture.md) for the full baseline and [docs/architecture/adr/README.md](docs/architecture/adr/README.md) for the decision log.

## Repository structure

The repository now mixes planning material with early executable app scaffolds.

```text
palio/
├─ AGENTS.md
├─ Makefile
├─ README.md
├─ .github/
│  └─ workflows/
├─ apps/
│  ├─ api/
│  └─ web/
├─ docs/
│  ├─ api/
│  ├─ architecture/
│  ├─ domain/
│  ├─ ops/
│  ├─ product/
│  ├─ qna/
│  ├─ testing/
│  └─ milestones.md
├─ infra/
├─ tools/
├─ evals/
└─ note.md
```

## Read this first

If you are starting work in this repo, use these documents in order:

1. [docs/product/prd.md](docs/product/prd.md)
2. [docs/architecture/architecture.md](docs/architecture/architecture.md)
3. [docs/domain/er-schema.md](docs/domain/er-schema.md)
4. [docs/testing/test-strategy.md](docs/testing/test-strategy.md)
5. [docs/qna/README.md](docs/qna/README.md)
6. [docs/milestones.md](docs/milestones.md)

Additional high-signal references:
- [docs/product/acceptance-scenarios.md](docs/product/acceptance-scenarios.md)
- [docs/domain/game-catalog.md](docs/domain/game-catalog.md)
- [docs/domain/palio-rules.md](docs/domain/palio-rules.md)

## Working in this repo today

The canonical top-level implementation skeleton has landed, and `apps/api/` plus `apps/web/` now contain the first runnable app scaffolds. The repo is still mid-bootstrap, but it now includes a baseline same-origin local stack under `infra/` for M1 smoke verification.

Today, useful work in this repository is:
- using `make help` to discover the stable top-level command surface
- iterating on the FastAPI and Angular scaffolds under `apps/api/` and `apps/web/`
- refining product, domain, and architecture decisions
- validating missing requirements and edge cases in Q&A
- planning thin slices for Milestone 1
- reviewing ADRs and test expectations before implementation
- populating the remaining infrastructure and deeper app slices through their dedicated M0 tasks

The first implementation milestone is documented in [docs/milestones.md](docs/milestones.md): stand up the monorepo skeleton, schema/migrations, auth plumbing, seeded catalogs, and season-setup flows.


## Quick start

The repository now exposes the canonical top-level command names, and the backend/frontend scaffolds make a subset of them runnable today.

### Prerequisites

* Python 3.12+
* Node.js LTS + npm
* Docker + Docker Compose
* Make
* uv
* pre-commit

### Discover the command surface

```bash
make help
```

### Task worktree helper

```bash
./tools/task-worktree-codex.sh 6
```

This creates the standard task worktree under `~/codex-worktrees/palio-board/tasks/` and opens `codex` in that worktree, reusing the existing branch/worktree when present.

### Install dependencies and hooks

```bash
cd apps/web
npm install
cd ../api
uv run --group dev pre-commit install --hook-type pre-commit --hook-type pre-push
cd ../web
npm run e2e:install
```

### Native app loop

```bash
make backend-dev
make web-dev
```

### Same-origin local stack

```bash
make up
docker compose -f infra/compose/docker-compose.yml --profile ops run --rm migrate
curl http://127.0.0.1:8080/healthz
curl http://127.0.0.1:8080/api/admin/health
curl http://127.0.0.1:8080/api/public/health
curl http://127.0.0.1:8080/realtime/health
make down
```

The Compose stack exposes one local origin at `http://127.0.0.1:8080`:
- Nginx serves the built Angular SPA and falls back to `index.html` for `/`, `/admin`, `/public`, and `/maxi` client routes.
- `/api/admin/...` and `/api/public/...` proxy to the backend through that same origin.
- `/realtime/...` is routed through Nginx with upgrade-friendly proxy settings so the placeholder health route and websocket path can use the same prefix.

Migrations remain explicit by architecture rule and are not run automatically when `make up` starts the stack. Use the one-shot `migrate` Compose service before verification work that depends on the schema.

The Angular SPA currently exposes three lazy route areas:
- `/admin`
- `/public`
- `/maxi`

`make backend-dev` starts the placeholder FastAPI app. `make test-backend` runs the split backend harness: `apps/api/tests/unit/` first, then `apps/api/tests/integration/` against a real local Postgres database. By default the integration layer now reuses the database image and bootstrap settings defined in `infra/compose/docker-compose.yml`; set `PALIO_TEST_POSTGRES_URL` to reuse an existing local Postgres admin database instead. Alembic uses `PALIO_DB_MIGRATION_URL`, while runtime DB access uses `PALIO_DB_RUNTIME_URL`.

Current backend operational baseline:
- typed env-based runtime settings via `PALIO_ENV`, `PALIO_LOG_LEVEL`, `PALIO_REQUEST_ID_HEADER`, `PALIO_BUILD_VERSION`, `PALIO_BUILD_COMMIT_SHA`, `PALIO_DB_RUNTIME_URL`, and `PALIO_DB_MIGRATION_URL`
- backend integration-test settings via `PALIO_TEST_POSTGRES_URL` and `PALIO_TEST_POSTGRES_IMAGE`
- Loguru-backed structured JSON HTTP request logs with propagated `X-Request-ID` response headers by default
- `/healthz`, `/readyz`, and `/version` endpoints for local smoke checks and future infra wiring

Contract workflow baseline:
- `make openapi-export` commits the FastAPI-owned OpenAPI artifact to `docs/api/openapi.yaml`
- `make openapi-types` regenerates ignored frontend TS declarations from that committed spec
- Angular services stay hand-written even when types are generated

### Quality gates

The repository-level quality-gate surface is stable and is what local hooks plus CI should call:

- `make format`
- `make format-check`
- `make lint`
- `make typecheck`
- `make check-boundaries`
- `make check-openapi`
- `make test`
- `make build`
- `make verify`

`make format` applies the backend formatter, while `make verify` runs the full baseline gate set: formatting checks, linting, typing, architectural boundary checks, OpenAPI verification, tests, and frontend build validation. The installed Git hooks use `pre-commit` for fast local checks and `pre-push` for the heavier type/test/build/contract path.

For the current local-development baseline, see [docs/ops/local-dev.md](docs/ops/local-dev.md).

## Usage

The target product has three user-facing surfaces:

### Admin and judge UI

The private operational UI is intended to support:
- season setup
- game configuration
- result entry
- Jolly management
- manual standings adjustments
- post-completion review
- audit inspection

### Public UI

The public interface is read-only and exposes:
- standings
- results
- notes and status labels
- history relevant to the current event

### Maxi-screen UI

The maxi-screen is a presentation-oriented route for event display.

## Business rules highlights

Important v1 rules include:
- only completed games affect leaderboard recomputation
- `pending_admin_review` still counts in standings
- `under_examination` remains visible but does not count
- Jolly is allowed only for Palio games
- each team may use Jolly at most once across Palio games
- Giocasport has a separate leaderboard
- Prepalio subgames roll up into a final Prepalio ranking, which then feeds Palio standings
- once official result data exists, game setup becomes immutable

See [docs/domain/palio-context.md](docs/domain/palio-context.md), [docs/domain/palio-rules.md](docs/domain/palio-rules.md), and [docs/qna/product/README.md](docs/qna/product/README.md).

## Development

### Tooling

* `make` is the top-level command surface
* `uv` for Python dependency management / execution
* `npm` for frontend
* `ruff`, `pyright`, and `pytest` for backend quality gates
* `dependency-cruiser`, Angular type checks, Angular tests, and Angular build validation for frontend quality gates
* `pre-commit` hooks on `pre-commit` and `pre-push`
* automated CI for the same repo-level gate set
* manual production deploy

### Recommended workflow

1. Read the relevant docs before implementing a change
2. Implement a vertical thin slice
3. Add the matching tests at the correct layer
4. Update docs when behavior or architecture changes
5. Add an ADR if the change affects long-lived technical direction
## Testing

The repository already defines the required test depth for implementation work.

Expected layers:
- unit tests for pure rules such as placement validation, scoring, Jolly math, and Prepalio aggregation
- Postgres-backed integration tests for authoritative workflows, audit, projections, immutability, and state transitions
- realtime integration tests for leases, stale writes, reconnects, and restart recovery
- a small number of frontend behavior tests
- a very small Playwright suite for critical operational flows

Read [docs/testing/test-strategy.md](docs/testing/test-strategy.md) before implementing backend, realtime, or UI flows.

For the current scaffold details, see [apps/api/README.md](apps/api/README.md), [apps/web/README.md](apps/web/README.md), and [docs/ops/local-dev.md](docs/ops/local-dev.md).

### Local quality-gate workflow

Use the repo-level `make` targets for the stable command surface:

```bash
make format
make lint
make typecheck
make check-boundaries
make check-openapi
make test
make build
make verify
```

Install the hooks once from `apps/api/` so the local Git workflow runs the same gates automatically:

```bash
cd apps/api
uv run --group dev pre-commit install --hook-type pre-commit --hook-type pre-push
```

### Run tests

The stable top-level test entrypoints are:
```bash
make test
make test-backend
make test-web
make test-e2e
```

Install the Playwright Chromium browser once with `cd apps/web && npm run e2e:install` before relying on the browser suite locally.

## Contributing

Contributions are welcome.

Before opening a PR:

* keep changes aligned with the current product scope
* avoid introducing architectural shortcuts
* add or update tests for the changed behavior
* update docs when relevant
* write a new ADR when changing architectural boundaries or long-lived decisions

For larger changes, open an issue or design discussion first.

## Roadmap

The current roadmap is defined by these milestones:

1. **M1 — Delivery foundation and architecture skeleton**  
   Establish the monorepo skeleton, app shells, database/migrations, local delivery rails, and CI guardrails.
2. **M2 — Identity, authorization, and season setup**  
   Add auth integration, roles/capabilities, user provisioning, and the full season/team/game configuration flow.
3. **M3 — Trusted ranking result backbone**  
   Deliver authoritative ranking result entry, validation, audit, projection recompute, and initial public reads.
4. **M4 — Live ranking operations and collaboration safety**  
   Add in-progress ranking workflows, live drafts, leases, stale-write protection, and reconnect/restart recovery.
5. **M5 — Advanced standings rules: Jolly, Prepalio, Giocasport, adjustments**  
   Implement competition-specific scoring rules, Jolly constraints, Prepalio roll-up, Giocasport separation, and manual adjustments.
6. **M6 — 1v1 tournament workflow**  
   Deliver semifinal pairings, match progression, derived final ranking, override handling, and leaderboard impact on completion.

Dependencies, exit criteria, and risks for each milestone live in [docs/milestones.md](docs/milestones.md).

## License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE).

## Acknowledgments

Built around the operational needs of the “Palio Collepassese“.
