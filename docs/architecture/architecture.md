# PalioBoard — Architecture Document

Version: v1 baseline  
Date: 2026-03-11  
Status: Approved implementation baseline

## Architecture at a glance

| Decision area | Baseline |
|---|---|
| System boundary | Python is the only business/data API; Angular never accesses application data directly. |
| Core stack | Angular SPA + FastAPI + PostgreSQL + Supabase Auth + Nginx. |
| Core style | Modular monolith with strict module ownership and public facades. |
| Consistency | Synchronous transactional writes with full recompute of affected standings scope. |
| Official result truth | Canonical normalized `game_entries` + `game_entry_fields`. |
| Realtime | SSE for public/maxi live views, WebSockets for admin live entry, polling where acceptable. |
| Live collaboration | Memory-first live draft state for ranking games only; persisted JSON snapshots for recovery. |
| Audit | Single generic append-only audit table with full before/after snapshots per changed entity. |
| Deployment | Single VPS, Docker Compose, one api instance, same-origin reverse proxy. |

## 1. Purpose and scope

This document is the **implementation architecture baseline** for PalioBoard v1.

It is intentionally **not**:
- a restatement of the PRD
- a UI specification
- a line-by-line database schema dump
- a theoretical DDD treatise

It defines the system boundaries, main modules, domain model, state machines, calculation ownership, authorization, audit, write/read paths, consistency rules, and delivery guidance for implementation.

The product context that matters architecturally is small and stable:
- one season per database
- exactly four teams
- three competition contexts: `palio`, `prepalio`, `giocasport`
- two v1 game formats: `ranking`, fixed 4-teams 1v1 `tournament`
- immediate public visibility
- automatic standings
- auditability for meaningful official changes

## 2. Architectural drivers and non-goals

### 2.1 Primary architectural concerns

1. **Correctness**  
   Standings, Jolly application, state transitions, and result officialization must be correct.

2. **Traceability**  
   Every meaningful official change must be auditable.

3. **Operational simplicity**  
   The app is used for a short annual event window; the architecture should stay boring and maintainable.

4. **Portability**  
   The system must remain portable to plain self-hosted PostgreSQL later.

5. **Low accidental complexity**  
   Avoid unnecessary extra services, caches, generic engines, or distributed consistency.

### 2.2 Non-goals for v1

The architecture explicitly does **not** optimize for:
- multi-year data
- generic tournament engine
- direct client access to database data
- event-driven distributed consistency
- zero-downtime deploys
- advanced infra such as Redis, brokers, or workers
- rich file storage
- runtime-managed roles/capabilities
- automatic ranking derivation from game metrics
- a generic dynamic form builder

## 3. System boundaries: what lives where

**Related ADRs:** ADR-0001

### 3.1 Runtime responsibilities

| Runtime area | What lives there | What does not live there |
|---|---|---|
| Angular SPA | Admin, public, and maxi-screen UI; route composition; shell-specific facades; local view state | Standings logic, authorization truth, official result truth |
| FastAPI app | Business workflows, authorization checks, orchestration, state transitions, audit persistence, projection recomputation, SSE/WebSocket transport | Direct browser rendering, durable client state |
| PostgreSQL | Authoritative business state, projection/read tables, audit log, idempotency records, provisional live-draft snapshots | Business workflow orchestration, permission logic |
| Supabase Auth | Identity provider in v1 | Business authorization, role/capability truth, business data API |
| In-memory live store | Current live draft state, field leases, connected editors, live per-game revision | Official result truth, official history |
| Nginx | Same-origin reverse proxy, TLS, SPA routing, `/api`, `/realtime` | Business logic |

### 3.2 Core boundary rules

1. **Python is the only business/data API.** Angular never talks directly to application data storage.
2. **Supabase is infrastructure, not application logic.** In v1 it provides hosted PostgreSQL and Auth, but core correctness must stay portable to plain Postgres.
3. **Authorization truth lives in the application domain.** JWTs identify the user; Python resolves roles/capabilities from app tables.
4. **Official data is DB-backed.** Realtime and in-memory collaboration state never become official truth by themselves.
5. **Read models are first-class.** Public/maxi-screen reads never query authoritative write tables directly.

## 4. Stack and technology choices

**Related ADRs:** ADR-0001, ADR-0007, ADR-0008, ADR-0009

### 4.1 Frontend
- Angular SPA
- one deployable, three lazy shells:
  - `admin`
  - `public`
  - `maxi-screen`
- feature-local state by default
- no global app-wide store in v1
- separate frontend API layers for `admin`, `public`, and `realtime`

### 4.2 Api
- FastAPI
- Pydantic DTOs
- SQLAlchemy 2.x
- Alembic
- sync-first application core
- async only where it helps at the boundary (SSE/WebSockets)

### 4.3 Data and identity
- PostgreSQL as the only application datastore
- direct Postgres connection from Python
- Supabase Auth as identity provider in v1
- no Supabase data APIs for business data

### 4.4 Delivery and operations
- Docker + Docker Compose
- single VPS
- Nginx reverse proxy
- one api instance in v1
- planned downtime deploys allowed
- local development with plain Postgres in Docker, FastAPI/Angular run natively

## 5. Module decomposition and ownership

**Related ADRs:** ADR-0002

The api is a **modular monolith**. Each module exposes a small public facade. Other modules may not import its repositories, ORM models, or internal services.

| Module | Ownership |
|---|---|
| `identity` | JWT verification, current principal resolution, current IdP adapter, future SSO/custom IdP adapter |
| `authorization` | Capability vocabulary, role resolution, policy checks |
| `users` | Application users, IdP-to-app-user linkage, minimal superadmin provisioning workflow |
| `season_setup` | Season, teams, competitions, games, points configuration, static field-catalog selection per game |
| `event_operations` | Game lifecycle and state transitions, Jolly recording rules, under-examination flow, pending-admin-review resolution |
| `results` | Canonical official per-team result persistence via `game_entries` and `game_entry_fields` |
| `tournaments` | 1v1 bracket progression, semifinal pairings, `tournament_matches`, materialization into canonical official entries |
| `live_games` | In-memory draft state, field leases, provisional draft snapshots, live revision, live-cycle handling |
| `leaderboard_projection` | Synchronous standings recomputation and current projection tables |
| `public_read` | Read-only queries for `/public`, `/maxi`, and other screen-shaped read models |
| `audit` | Generic append-only audit persistence from collected workflow facts |

### 5.1 Module interaction rules

- Cross-module workflows are coordinated by an **application/use-case orchestrator**.
- The orchestrator owns the **Unit of Work** and the single DB transaction.
- Public facades are the only stable cross-module contracts.
- CI must fail on forbidden cross-module imports.

## 6. Domain model and invariants

**Related ADRs:** ADR-0004, ADR-0005

This section describes **domain aggregates/entities**, not raw DB tables.

### 6.1 Season aggregate

**Contains:** one active season, exactly four teams, three competition contexts.

**Invariants:**
- one database stores one season only
- exactly four teams exist for the season
- competition contexts are `palio`, `prepalio`, `giocasport`
- each game belongs to exactly one competition context

### 6.2 Game aggregate

A game is the main operational aggregate.

**Contains:**
- game identity and format (`ranking` or `tournament_1v1`)
- lifecycle state
- official per-team result surface
- points configuration
- selected static field catalog entries
- technical `live_cycle`

**Invariants:**
- only one state is active at a time
- official result surface is always per-team, even for tournaments
- once any official result data exists, **every game property and relationship becomes immutable**
- leaderboard impact depends on state and competition type, not on UI behavior
- only completed games count in standings, except that `pending_admin_review` still behaves like completed
- `under_examination` is visible but excluded from standings

### 6.3 Official game result entity

The official per-team result is the canonical truth for a game.

**Contains:**
- team
- official placement
- Jolly flag
- official typed metric fields

**Invariants:**
- a raning game always has results for all 4 teams before completion
- placements are explicit and may include ties such as `1,2,2,4`
- Jolly is valid only for Palio games
- each team may use Jolly at most once across Palio games
- official placement lives directly in the canonical result entity; there is no separate current computed/override table in v1

### 6.4 Tournament entity (within a game)

For `tournament_1v1`, the bracket is an operational entity inside the game.

**Contains:**
- semifinal 1
- semifinal 2
- final 3rd/4th
- final 1st/2nd
- winners per match

**Invariants:**
- pairings are manually set before tournament start
- each saved match outcome is official immediately
- official per-team consequences are materialized into the canonical official result entity
- leaderboard still waits for whole-game completion

### 6.5 Live draft entity (technical, not official business truth)

Only ranking games use live draft in v1.

**Contains:**
- current in-memory draft values
- field-level last editor metadata
- field-level leases
- per-game live revision
- `live_cycle` scoping
- persisted provisional JSON snapshot for recovery

**Invariants:**
- live draft is never official by itself
- active field leases are memory-first and must be reacquired after restart
- persisted draft snapshot is recovery state only, not audited business history
- when a game leaves `in_progress`, changed draft values are materialized into official state and the draft becomes obsolete
- stale drafts from an older `live_cycle` are ignored

### 6.6 Standings scope

Standings are a **derived current read model**, not a mutable business aggregate.

**Inputs:**
- official game results
- configured points tables
- Jolly flags
- manual standings adjustments
- Prepalio aggregate ranking

**Invariants:**
- Giocasport standings are separate from Palio standings
- Prepalio subgames feed a Prepalio aggregate ranking, which then feeds the main Palio standings
- manual adjustments are explicit authoritative inputs, not hidden exceptions

## 7. State machines and side effects

**Related ADRs:** ADR-0003, ADR-0004, ADR-0005

### 7.1 Game state machine

States:
- `draft`
- `in_progress`
- `completed`
- `pending_admin_review`
- `under_examination`

### 7.2 Allowed transitions

| From | To | Trigger | Side effects |
|---|---|---|---|
| `draft` | `in_progress` | Start game | increment `live_cycle`; prefill live draft from current official entries for ranking games |
| `in_progress` | `completed` | Complete game | validate structure; materialize changed draft values into official entries for ranking games; audit changed authoritative entities; clear current draft best-effort; recompute affected projections |
| `in_progress` | `under_examination` | Mark under examination | materialize changed draft values into official entries for ranking games; audit changed authoritative entities; clear current draft best-effort; exclude game from leaderboard projections |
| `completed` | `pending_admin_review` | Judge edits completed official result | write new official result; audit; latest result remains official/counting; admin review required |
| `pending_admin_review` | `completed` | Admin review resolves | possibly revert or confirm latest official result; audit new authoritative changes |
| `completed` or `pending_admin_review` | `under_examination` | Judge/admin marks under examination | keep latest official result visible; exclude from leaderboard projections |
| `under_examination` | `completed` | Judge/admin resolves examination | keep current official result or a newly corrected one; recompute projections |

### 7.3 Transition rules that must never be violated

- A game enters `in_progress` only via explicit **Start game**.
- A raning game can leave `in_progress` only after materialization of changed draft values.
- A 1v1 game bypasses live draft in v1.
- `pending_admin_review` is not the same as `under_examination`:
  - `pending_admin_review` still counts
  - `under_examination` does not count
- Once official result data exists, setup/config mutation is forbidden.

## 8. Calculation ownership

**Related ADRs:** ADR-0003, ADR-0004

### 8.1 Official ranking and leaderboard logic

**Owner:** `leaderboard_projection` module in Python.

**Inputs:**
- official canonical result surface
- points configuration
- Jolly flags
- manual standings adjustments
- competition context
- Prepalio aggregate ranking

**Outputs:**
- current leaderboard projection tables
- current position-count projection tables

### 8.2 Related calculation responsibilities

- **1v1 bracket progression** lives in `tournaments`.
- **Automatic 1v1 final ranking derivation** lives in `tournaments`, then materializes into canonical official entries.
- **Prepalio aggregate ranking derivation** belongs in api calculation code, not in UI, triggers, or ad hoc SQL.
- **Live provisional game view** belongs to `live_games` + `public_read` and is explicitly **not official standings logic**.

### 8.3 Forbidden ownership

The following must never own ranking logic:
- Angular
- SQL triggers
- ad hoc scripts
- projection tables themselves
- in-memory live draft state

## 9. Authorization model

**Related ADRs:** ADR-0006

### 9.1 Identity

- Supabase Auth provides identity in v1.
- Angular sends bearer tokens to FastAPI.
- FastAPI validates the token and resolves an app user.
- App authorization/capabilities remain fully in the application DB and code.

### 9.2 Authorization

- Authorization is **capability-based**.
- Capabilities are defined in code.
- Roles are seeded bundles stored in DB.
- User-role assignments are DB-backed.
- Direct user capability grants are schema-supported but not used in v1 UI.

### 9.3 Default role bundles

- **Superadmin**: admin capabilities + user creation + future app-management capabilities
- **Admin**: all operational/admin capabilities except superadmin-only provisioning
- **Judge**: result entry/editing, tournament pairing, Jolly marking, state operations allowed by policy
- **Public**: no login, read-only

### 9.4 Policy rules

- Capability checks happen at API entry points.
- Critical domain invariants are rechecked inside application services.
- WebSocket capabilities are checked at connection time; domain rules are checked on every mutating action.

## 10. Audit model

**Related ADRs:** ADR-0004, ADR-0005

### 10.1 What audit is for

Audit is the **historical explanation layer** for authoritative business changes.

It must answer:
- who changed official state
- when they changed it
- what changed
- why it changed when a reason exists
- which authoritative entities changed inside one workflow

### 10.2 Audit shape

- one **generic append-only table**
- one audit row per changed authoritative entity
- full `before` and `after` snapshots
- `actor_user_id` only
- shared `correlation_id` across rows from the same workflow

### 10.3 What is audited

- game state changes
- official result changes
- Jolly changes
- tournament pairing changes
- manual standings adjustments
- user creation and other authoritative admin operations

### 10.4 What is not audited

- projections/read-model churn
- in-progress keystroke-level draft updates
- transient leases/presence data
- transport-level realtime notifications

## 11. Write model and read model

### 11.1 Write model

Official writes use a **single transaction** coordinated by an application/use-case orchestrator.

**Write path:**
1. API entry authenticates and authorizes.
2. Orchestrator opens Unit of Work.
3. Critical workflow locks the game aggregate when needed.
4. Relevant module facades run in explicit order.
5. Domain/application facts are collected.
6. Audit rows are produced from those facts.
7. Affected projections are recomputed in Python.
8. Transaction commits.
9. Post-commit realtime notification is emitted best effort.

### 11.2 Read model

Read concerns are separate.

**Public/maxi-screen read path:**
- read only from projection/read tables or live per-game read models
- never query authoritative write tables directly

**Admin read path:**
- normal screen-shaped queries use dedicated query services
- live ranking-format entry uses initial HTTP fetch + per-game realtime stream

### 11.3 Live read path

For ranking games in progress:
- current live view is memory-first
- full snapshots are emitted per `game_id`
- snapshots include monotonic per-game revision
- clients replace local state on newer revision
- persisted draft snapshots are only a recovery boundary

## 12. Failure and consistency rules

**Related ADRs:** ADR-0003, ADR-0005, ADR-0008

### 12.1 Hard rule

A business command is considered successful only if **authoritative state, required audit rows, and required projection updates** all succeed inside the transaction.

### 12.2 Failure matrix

| Situation | Rule |
|---|---|
| Save of official state succeeds but recomputation fails | The transaction must roll back. The save is not considered successful. |
| Audit write fails for an authoritative business change | The transaction must roll back. Audit is required for official state change. |
| Realtime notification fails after commit | No rollback. DB state remains source of truth; clients recover by reconnecting/refetching. |
| Two users edit the same raning game live | Field lease + optimistic versioning protect the field; stale writes are rejected; reconnect flow surfaces conflict. |
| Two critical commands target the same game concurrently | Game row lock serializes critical workflow execution; optimistic version helps stale-data UX. |
| A completed result is edited by a judge | Official result is updated and audited immediately; game moves to `pending_admin_review`; latest result still counts. |
| An admin reverts a post-completion change | This is a new authoritative write, not deletion of history; official result is rewritten, audited, and state can move back to `completed`. |
| A game is marked `under_examination` | Latest official result remains visible, but the game is excluded from leaderboard calculation. |
| Draft cleanup fails after leaving `in_progress` | Business transaction still succeeds. Stale draft is harmless because `live_cycle` invalidates old draft state. |
| Idempotent command is retried | Shared idempotency service returns the same logical outcome instead of applying the command twice. |
| User provisioning creates IdP account but app-user creation fails | Api attempts compensating delete in the IdP; if that fails, surface clear manual-recovery case. |
| Api restarts while a ranking game is in progress | Persisted draft snapshot is reloaded into memory on first access; active leases are not restored and must be reacquired. |

### 12.3 Special consistency notes

- `pending_admin_review` is a **monitoring state**, not a suspended scoring state.
- `under_examination` is a **suspended scoring state**.
- 1v1 official match outcomes can exist before leaderboard impact; standings still wait for whole-game completion.

## 13. Delivery guidance for Codex

This section is normative for implementation.

### 13.1 Where business logic belongs

**Must live in api application/domain modules:**
- state transitions
- standings calculation
- Jolly validation
- Prepalio aggregation
- 1v1 ranking derivation
- official result materialization
- immutability rules
- authorization policy decisions

**May live in adapters/infrastructure:**
- JWT verification
- live in-memory state store
- clock
- idempotency storage adapter
- DB repositories/query services
- Nginx, Docker, deployment scripts

### 13.2 Forbidden shortcuts

Codex must **not**:
- put standings logic in Angular
- bypass the orchestrator/Unit of Work for authoritative writes
- mutate projection tables directly as if they were source of truth
- treat provisional draft snapshots as official result state
- add business logic to SQL triggers
- let modules import another module’s internals
- use generic JSON blobs as official result persistence
- reintroduce mutable game config after official results exist
- use the audit log as current-state truth

### 13.3 Required test layers for risky changes

Risky changes must include the right test depth.

| Change type | Minimum required tests |
|---|---|
| Pure domain rule | unit tests |
| State transition or official write workflow | Postgres-backed integration tests |
| Projection or standings logic | unit tests for pure calculation + integration tests for transaction/projection update |
| Live entry / lease / conflict behavior | realtime integration tests |
| User-visible critical flow | Playwright E2E when the flow is already part of the critical E2E set |

Critical E2E flows for v1:
- complete a raning game
- verify public update after completion
- progress and complete a 1v1 tournament
- post-completion edit and admin review behavior
- concurrent live updates and field locking

### 13.4 What counts as a valid thin slice

A valid thin slice is a **vertical end-to-end implementation** that exercises the real architecture.

A thin slice is valid when it includes:
- one API command or query
- one orchestrated api flow using real module boundaries
- real persistence in Postgres
- audit if the change is authoritative
- projection update if standings/public reads are affected
- at least one matching test at the right layer
- minimal UI only if needed to exercise the workflow

Examples of valid thin slices:
- Start a ranking game and persist `in_progress`
- Complete a ranking game and recompute leaderboard
- Save a 1v1 semifinal winner and update official entries
- Create a manual standings adjustment and refresh the read model

### 13.5 What requires an ADR

An ADR is required for changes that alter architectural boundaries, consistency rules, or long-lived technical direction.

Examples:
- introducing Redis, a broker, or a worker service
- changing projection strategy from synchronous to eventual
- changing module boundaries or ownership
- changing auth/identity architecture
- changing authoritative result persistence shape
- introducing direct client access to DB-backed data
- changing immutability rules for games
- introducing generic dynamic form-builder behavior
- changing the live draft persistence model in a way that affects correctness semantics

## 14. Proposed project structure
### 14.1 Top-level monorepo

```text
palio-board/
├─ Makefile
├─ docs/
├─ apps/
│  ├─ api/
│  └─ web/
├─ infra/
├─ tools/
└─ .github/workflows/
```

### 14.2 Api

```text
apps/api/
├─ pyproject.toml
├─ alembic.ini
├─ migrations/
├─ src/palio/
│  ├─ app/
│  ├─ db/
│  ├─ shared/
│  └─ modules/
│     ├─ identity/
│     ├─ authorization/
│     ├─ users/
│     ├─ season_setup/
│     ├─ event_operations/
│     ├─ results/
│     ├─ tournaments/
│     ├─ live_games/
│     ├─ leaderboard_projection/
│     ├─ public_read/
│     └─ audit/
└─ tests/
```

Each module follows:

```text
<module>/
├─ facade.py
├─ application/
├─ domain/
└─ infrastructure/
```

### 14.3 Frontend

```text
apps/web/
├─ package.json
├─ src/app/
│  ├─ core/
│  ├─ shell-admin/
│  ├─ shell-public/
│  ├─ shell-maxi/
│  ├─ features/
│  └─ shared/
│     ├─ api/
│     ├─ ui/
│     ├─ utils/
│     └─ types/
└─ tests/
```

### 14.4 Infrastructure

```text
infra/
├─ docker/
├─ nginx/
└─ compose/
```

## 15. Operational baseline

- one Angular SPA with three lazy shells
- one FastAPI application serving REST, SSE, and WebSockets
- one Postgres database
- one api instance in v1
- Nginx same-origin reverse proxy
- Docker Compose deploy
- structured JSON logs with correlation id
- liveness, readiness, and build/version endpoints
- logs-only monitoring in v1
- managed DB backups only in v1

## 16. Repository and delivery conventions

- monorepo, tooling-light
- `make` as the top-level command surface
- `uv` for Python, `npm` for frontend
- pre-commit hooks before commit
- automated CI + manual production deploy
- OpenAPI spec committed; generated TS types not committed
- api module boundaries and frontend import boundaries enforced in CI

## 17. ADR governance

### 17.1 When to write a new ADR

Create a new ADR when a change affects at least one of:
- system boundaries
- module ownership
- transaction/consistency model
- official result model
- projection strategy
- live collaboration model
- authorization model
- deployment/operational model
- test strategy or quality gates
- portability assumptions

Examples:
- adopting Redis for live state
- adding a worker/outbox
- changing official result persistence shape
- moving from bearer-token SPA auth to api session auth
- introducing multi-year support

### 17.2 What should not become an ADR

Do **not** write an ADR for:
- local refactors with no architectural consequence
- naming cleanups
- implementation details hidden behind existing adapters
- small UI-only changes
- routine package upgrades with no architectural impact

### 17.3 Update process

Use this change process:

1. create or update the relevant implementation change
2. write a new ADR if the architectural decision is new or materially changed
3. keep the ADR set as the source of recent architectural decisions
4. periodically refresh this baseline document so it reflects accepted ADRs cleanly

### 17.4 Precedence rule

If there is a mismatch between this baseline and a newer **accepted** ADR:
- the accepted ADR is authoritative
- this baseline should be updated as soon as practical

### 17.5 Current ADR map

| ADR | Topic | Main sections affected in this document |
|---|---|---|
| ADR-0001 | System boundary and core stack | 3, 4 |
| ADR-0002 | Modular monolith and strict module boundaries | 5, 13 |
| ADR-0003 | Synchronous writes and current-state projections | 7, 8, 11, 12 |
| ADR-0004 | Canonical official result model | 6, 7, 8, 10 |
| ADR-0005 | Live collaboration model for ranking games | 6, 7, 10, 11, 12 |
| ADR-0006 | Identity, application users, capability-based authorization | 9 |
| ADR-0007 | API surfaces and OpenAPI contract strategy | 4, 11, 13 |
| ADR-0008 | Deployment and operational model | 4, 12 |
| ADR-0009 | Testing and quality gates | 4, 13 |
