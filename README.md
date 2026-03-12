# PalioBoard

Open-source web application for configuring, running, and publishing the Collepasso Palio tournament.

## Current status

This repository is currently a documentation-first implementation baseline for v1.

What is already in the repo:
- approved product scope
- architecture baseline and ADRs
- domain model and rules
- testing strategy
- milestone plan

What is not in the repo yet:
- backend application code
- frontend application code
- Docker Compose or local bootstrap files
- `Makefile` targets
- `.env.example` files
- runnable local URLs

That means there is no real quick start yet. The repository currently documents what must be built, how it should behave, and in which order it should be delivered.


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

The repository currently contains planning and implementation guidance rather than executable app code.

```text
palio/
├─ AGENTS.md
├─ README.md
├─ docs/
│  ├─ architecture/
│  ├─ domain/
│  ├─ product/
│  ├─ qna/
│  ├─ testing/
│  └─ milestones.md
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

Because the implementation skeleton has not landed yet, there is no runnable local environment to start.

Today, useful work in this repository is:
- refining product, domain, and architecture decisions
- validating missing requirements and edge cases in Q&A
- planning thin slices for Milestone 1
- reviewing ADRs and test expectations before implementation

The first implementation milestone is documented in [docs/milestones.md](docs/milestones.md): stand up the monorepo skeleton, schema/migrations, auth plumbing, seeded catalogs, and season-setup flows.


## Quick start

> Replace these commands with the exact ones once the repository bootstrap is in place.

### Prerequisites

* Python 3.12+
* Node.js LTS + npm
* Docker + Docker Compose
* Make
* uv
* PostgreSQL (or Dockerized PostgreSQL for local development)

### Clone the repository

```bash
git clone <your-repo-url>
cd palio-board
```

### Configure environment

Create local environment files as needed:

```bash
cp backend/.env.example backend/.env
cp web/.env.example web/.env
```

Fill in the required values for:

* database connection
* auth configuration
* local URLs / ports

### Start local dependencies

```bash
make up
```

### Run the backend

```bash
make backend-dev
```

### Run the frontend

```bash
make web-dev
```

### Open the app

* Admin UI: `http://localhost:...`
* Public UI: `http://localhost:...`
* Maxi-screen UI: `http://localhost:...`

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
* pre-commit hooks before commit
* automated CI
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

### Test layers

TO BE DONE. As an example:
* pure domain rules → unit tests
* authoritative state transitions / official writes → Postgres-backed integration tests
* standings / projections → unit tests + integration tests
* live collaboration / leases / conflicts → realtime integration tests
* user-visible critical flows → Playwright E2E

### Critical E2E flows for v1

TO BE DONE. As an example:
* complete a ranking game
* verify public update after completion
* progress and complete a 1v1 tournament
* post-completion edit and admin review behavior
* concurrent live updates and field locking

### Run tests

TO BE DONE. As an example:
```bash
make test
```

Or run them per area:

```bash
make test-backend
make test-web
make test-e2e
```

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