# PalioBoard — Architecture Baseline

Status: approved v1 baseline

This document defines the system boundary, module ownership, source of truth, non-negotiable invariants, critical lifecycle rules, and where new logic belongs.

It is intentionally not:
- a restatement of product scope
- a schema dump
- a UI specification
- a testing handbook
- a deployment runbook

## Purpose and system shape

PalioBoard is a monorepo application for managing one Palio season with:
- one database per season
- exactly four teams
- three competition contexts: `palio`, `prepalio`, `giocasport`
- two v1 game formats: `ranking` and fixed four-team `tournament_1v1`

Core stack:
- Angular SPA
- Python FastAPI backend
- PostgreSQL
- Supabase Auth as identity provider in v1
- Nginx reverse proxy

Architectural style:
- modular monolith on the backend API
- synchronous transactional writes
- explicit projection/read models
- memory-first live draft state for ranking games only

## Top-level boundary rules

1. Python is the only business and data API.
   Angular never talks directly to application tables.
2. Official truth is DB-backed.
   Realtime state and live drafts are never official truth by themselves.
3. Authorization truth lives in the application.
   JWTs identify users; roles and capabilities are resolved from application tables and policy code.
4. Read models are derived data.
   Public and maxi-screen reads use projection/read tables or live read models, not write tables as source of truth.
5. Business logic belongs in backend modules.
   Do not put scoring, lifecycle, authorization policy, or standings logic in the frontend, migrations, or SQL triggers.

## Runtime responsibilities

| Runtime area | Owns | Does not own |
|---|---|---|
| Angular SPA | admin/public/maxi UI, route composition, shell-specific client facades, local view state | standings logic, official result truth, authorization truth |
| FastAPI | business workflows, orchestration, authorization checks, state transitions, audit writes, projection recomputation, realtime transport | direct browser rendering, durable client-side state |
| PostgreSQL | authoritative business state, projections, audit log, idempotency records, persisted draft snapshots for recovery | business workflow orchestration, permission policy |
| Supabase Auth | identity provider in v1 | business authorization and business data |
| In-memory live store | current ranking live draft state, leases, editors, per-game revision, live-cycle data | official truth, official history |
| Nginx | same-origin reverse proxy, TLS, SPA routing | business logic |

## Backend module ownership

The backend is a modular monolith. Each module exposes a small public facade. Modules may not import another module's repositories, ORM models, or internal services.

| Module | Owns |
|---|---|
| `identity` | JWT verification, principal resolution, current IdP adapter |
| `authorization` | capability vocabulary, role resolution, policy checks |
| `users` | application users, IdP-to-app-user linkage, superadmin provisioning |
| `season_setup` | season, teams, competitions, games, points config, static field-catalog selection |
| `event_operations` | game lifecycle transitions, Jolly rules, under-examination flow, pending-admin-review flow |
| `results` | canonical official per-team result persistence via `game_entries` and `game_entry_fields` |
| `tournaments` | semifinal pairings, match progression, derived final ranking, materialization into canonical official entries |
| `live_games` | in-memory ranking live draft state, field leases, revision handling, persisted draft snapshots |
| `leaderboard_projection` | synchronous standings recomputation and projection tables |
| `public_read` | read-only queries for public, maxi-screen, and other screen-shaped read models |
| `audit` | append-only audit persistence from authoritative workflow facts |

### Cross-module rule
- Cross-module workflows are coordinated by an application/use-case orchestrator.
- The orchestrator owns the unit of work and the DB transaction.
- Public facades are the only stable cross-module contracts.

## Source of truth

### Official game result truth
The canonical official per-team result surface is:
- `game_entries`
- `game_entry_fields`

Official truth includes:
- team
- official placement
- Jolly flag
- official typed field values

There is no separate official ranking override table in v1. The current official placement on the canonical result is the source of truth for standings and projections.

### Live truth vs official truth
Ranking live entry uses a memory-first draft model for in-progress work.
That draft state is provisional, collaborative, and recoverable, but never official by itself.
Official truth changes only through authoritative backend workflows.

### Standings truth
Standings are a derived current read model computed from:
- official results
- points configuration
- Jolly flags
- manual standings adjustments
- Prepalio aggregate ranking

Projection tables are not authoritative business state.

## Non-negotiable invariants

1. One database stores one season only in v1.
2. The season has exactly four teams and exactly three competition contexts.
3. Every game belongs to exactly one competition context.
4. The official result surface is always per-team, even for tournaments.
5. Once any official result data exists for a game, every result-affecting game property and relationship becomes immutable.
6. A ranking game can complete only with structurally valid official data for all four teams.
7. Jolly is valid only for Palio games and at most once per team across Palio games.
8. `pending_admin_review` still counts in leaderboard calculations using the latest saved official result.
9. `under_examination` remains visible but is excluded from leaderboard calculations.
10. Ranking live draft state is provisional and never becomes official without materialization into canonical official entries.
11. Tournament match outcomes are official immediately, but leaderboard impact waits for whole-game completion.
12. Audit is required for authoritative business changes.

## Game lifecycle rules

### States
- `draft`
- `in_progress`
- `completed`
- `pending_admin_review`
- `under_examination`

### Allowed transitions
| From | To | Meaning |
|---|---|---|
| `draft` | `in_progress` | explicit start game |
| `in_progress` | `completed` | explicit end game |
| `in_progress` | `under_examination` | suspend scoring while keeping visibility |
| `completed` | `pending_admin_review` | judge edits an already completed official result |
| `pending_admin_review` | `completed` | admin resolves review |
| `completed` or `pending_admin_review` | `under_examination` | judge/admin suspends scoring |
| `under_examination` | `completed` | judge/admin resolves examination |

### Lifecycle rules that must not be broken
- A game enters `in_progress` only through explicit start.
- Ranking games use live draft while in progress.
- Tournament games bypass live draft in v1.
- Leaving `in_progress` for a ranking game requires materialization of changed draft values into canonical official entries.
- `pending_admin_review` is not a suspended-scoring state.
- `under_examination` is a suspended-scoring state.

## Write model and consistency model

Official writes run inside one DB transaction coordinated by an application/use-case orchestrator.

### Authoritative write path
1. API entry authenticates and authorizes.
2. The orchestrator opens the unit of work.
3. The critical workflow locks the game aggregate when needed.
4. Relevant module facades execute in explicit order.
5. Authoritative facts are collected.
6. Audit rows are produced from those facts.
7. Affected projections are recomputed in Python.
8. The transaction commits.
9. Realtime notification is emitted best effort after commit.

### Hard consistency rule
A business command succeeds only if all required authoritative state writes, audit rows, and projection updates succeed in the same transaction.

### Important failure rules
- If authoritative state save succeeds but projection recomputation fails, roll back.
- If an audit write for an authoritative change fails, roll back.
- If realtime notification fails after commit, do not roll back.
- If draft cleanup fails after leaving `in_progress`, the business transaction still succeeds; `live_cycle` prevents stale draft reuse.

## Authorization model

- Identity comes from Supabase Auth in v1.
- Authorization is capability-based.
- Capabilities are defined in code.
- Roles are stored as seeded bundles in the application DB.
- User-role assignments are DB-backed.
- Capability checks happen at API entry points.
- Critical invariants are rechecked inside backend workflows.
- WebSocket capability checks happen at connection time; domain rules are rechecked on each mutating action.

## Audit model

Audit is the historical explanation layer for authoritative business changes.

### Required audit properties
- append-only
- one row per changed authoritative entity
- full `before` and `after` snapshots
- `actor_user_id`
- shared `correlation_id` for one workflow

### Audit authoritative changes
- game state changes
- official result changes
- Jolly changes
- tournament pairing changes
- manual standings adjustments
- user creation and other authoritative admin operations

### Do not audit as authoritative history
- projection churn
- in-progress keystroke-level draft changes
- transient leases or presence
- transport-level realtime notifications

## Where new logic belongs

### Must live in backend business/application modules
- lifecycle/state transitions
- standings calculation
- Jolly validation
- Prepalio aggregation
- tournament ranking derivation
- official result materialization
- immutability rules
- authorization policy decisions

### May live in adapters or infrastructure
- JWT verification adapter
- repositories and query services
- live in-memory state store
- idempotency storage adapter
- transport and deployment wiring

### Must not be used as business-logic owners
- Angular
- SQL triggers
- projection tables
- in-memory live draft state
- ad hoc scripts
- audit log

## Companion documents

Read these only when the task needs them:
- `docs/architecture/module-map.md` — package/path codemap and allowed dependencies
- `docs/architecture/runtime-flows.md` — critical write flows and side effects
- `docs/architecture/adr/` — durable architectural decisions and consequences
- `docs/domain/business-rules.md` — business rule catalog
- `docs/domain/er-schema.md` — entity and relationship detail
- `docs/api/error-contract.md` — stable business error semantics
- `docs/testing/test-strategy.md` — required test depth by change type
