# Module Map

## Purpose

This document is the backend codemap for agents.
Use it to answer four implementation questions quickly:
- where should this code go?
- which module owns this behavior or table?
- which cross-module calls are allowed?
- which layer should contain the logic?

Read this after `docs/architecture/architecture.md` when doing backend work.
If this file conflicts with the architecture baseline or an ADR, flag the conflict instead of guessing.

## How to use this file

1. Find the business area or table you need to change.
2. Find the owning module and its public facade.
3. Put the change in the narrowest layer that can own it.
4. If the use case spans multiple modules, coordinate it in an application/use-case orchestrator.
5. Do not import another module's internals.

## Intended backend package shape

The backend is expected to follow this package shape under `apps/api/src/palio/`:

```text
palio/
├── api/                      # FastAPI routers, request/response DTO wiring
├── bootstrap/               # composition root, dependency wiring
├── shared/                  # shared technical helpers only
└── modules/
    ├── identity/
    ├── authorization/
    ├── users/
    ├── season_setup/
    ├── event_operations/
    ├── results/
    ├── tournaments/
    ├── live_games/
    ├── leaderboard_projection/
    ├── public_read/
    └── audit/
```

Each module should keep a consistent internal shape:

```text
<module>/
├── facade.py                # only stable cross-module entrypoint
├── application/             # use cases, orchestrators local to the module
├── domain/                  # entities, value objects, domain services/rules
├── infrastructure/          # repositories, query services, adapters
└── dto/                     # internal DTOs only when useful
```

This is a target codemap. If the code has not reached this exact shape yet, keep new work moving toward it instead of inventing a competing layout.

## Layer responsibilities

| Layer | Owns | Should not own |
|---|---|---|
| `api/` | FastAPI routers, auth entry checks, request/response mapping, HTTP semantics | business workflows, DB queries with domain rules, projection logic |
| `bootstrap/` | dependency wiring, composition root, app startup | domain logic, request handling |
| module `application/` | use cases, orchestration, transaction sequencing, policy rechecks | HTTP transport, ORM model definitions as public contract |
| module `domain/` | business rules, validation, state transition logic, value semantics | framework code, SQL shaping for screens |
| module `infrastructure/` | repositories, explicit SQL queries, adapters, external systems | cross-module business orchestration |
| `shared/` | low-level technical helpers that are truly generic | business rules disguised as utilities |

## Transaction and session ownership

- A multi-step business command is owned by an application/use-case orchestrator.
- The orchestrator owns the unit of work and SQLAlchemy session.
- Repositories are session-bound; they do not create their own sessions.
- Cross-module workflows should stay explicit in code. Do not hide them in signals, triggers, or implicit callbacks.

## Query placement rules

Use these rules by default:
- command-side persistence of authoritative state -> module repository in `infrastructure/`
- read/query for public or admin screens -> explicit query service in the owning read module
- projection recomputation query -> `leaderboard_projection`
- one-off migration or repair query -> migration / ops script, not runtime module logic

Read-side SQL may join across tables when building a screen-shaped result, but that does not change ownership of the underlying data.

## Module ownership map

### `identity`

**Owns**
- bearer token validation
- authenticated principal extraction
- identity-provider adapter boundary

**Likely package surface**
- `palio.modules.identity.facade`
- `palio.modules.identity.infrastructure.supabase_auth_adapter`

**May call**
- nobody for business logic
- possibly `users` only through a public facade if principal hydration needs linked app-user info

**Must not own**
- capability checks
- user provisioning workflow semantics
- application user data as business truth

### `authorization`

**Owns**
- capability vocabulary
- role and effective-permission resolution
- policy checks at application boundaries

**Tables / data it owns**
- `roles`
- `role_capabilities`
- `user_roles`
- `user_capabilities` (future-compatible, not exposed in v1 UI)

**Public facade should answer**
- what capabilities does this user have?
- is this principal allowed to perform this action?

**Must not own**
- user lifecycle
- game-domain rules

### `users`

**Owns**
- application user profile
- link from auth user id to app user id
- minimal provisioning workflow semantics for superadmin-created users

**Tables / data it owns**
- `users`

**May call**
- `identity` adapter boundary for provisioning / deletion compensation
- `authorization` facade for seeded role assignment workflow
- `audit` facade for authoritative admin operations

**Must not own**
- JWT validation rules
- capability vocabulary

### `season_setup`

**Owns**
- season, teams, competitions, games, field selection, points table configuration
- setup-time validation before official results exist
- immutability guard once official result data exists

**Tables / data it owns**
- `seasons`
- `teams`
- `competitions`
- `games`
- `fields` (seeded catalog as referenced data)
- `game_fields`
- `points`

**Public facade should answer**
- read/write setup commands
- can this game still be edited?
- what fields and points config apply to this game?

**Must not own**
- official result persistence
- game lifecycle transitions after execution starts
- leaderboard recomputation

### `event_operations`

**Owns**
- game state transitions
- start / complete / mark under examination / resolve
- pending-admin-review transition rules
- Jolly validation orchestration at the lifecycle boundary when relevant

**Primary table touched**
- `games`

**May call**
- `results` facade to materialize official changes when leaving `in_progress`
- `live_games` facade to load or clear draft state for ranking games
- `leaderboard_projection` facade for synchronous recomputation
- `audit` facade

**Must not own**
- canonical official result storage details
- tournament bracket storage

### `results`

**Owns**
- canonical official per-team result persistence
- typed official field persistence
- structural validation for placements and required fields
- Jolly persistence on official entries

**Tables / data it owns**
- `game_entries`
- `game_entry_fields`

**Public facade should answer**
- load current official result
- validate official result payload
- upsert changed official entries
- compare draft vs official state

**Must not own**
- game state machine
- bracket progression
- read-model shaping for public screens

### `tournaments`

**Owns**
- semifinal pairings
- match outcome persistence
- derivation of final 1st/2nd and 3rd/4th placements
- materialization of tournament official per-team entries

**Tables / data it owns**
- `tournament_matches`
- writes through `results` facade into `game_entries` when official surface must reflect match outcomes

**May call**
- `results` facade
- `leaderboard_projection` facade when whole tournament becomes complete
- `audit` facade

**Must not own**
- generic ranking-game live draft behavior
- public read shaping

### `live_games`

**Owns**
- in-memory ranking-game draft state
- live per-game revision
- field lease rules
- persisted recovery snapshots
- hydration from official state when a game enters `in_progress`

**Tables / data it owns**
- `game_live_drafts` (recovery snapshots only)

**Public facade should answer**
- get live draft snapshot
- apply live draft mutation with revision check
- persist recovery snapshot
- clear or obsolete draft on lifecycle exit

**Must not own**
- official truth
- leaderboard updates from draft state

### `leaderboard_projection`

**Owns**
- standings recomputation
- position-count recomputation
- Prepalio aggregate ranking projection
- application of manual leaderboard adjustments to the derived current view

**Tables / data it owns**
- `leaderboard_current`
- `leaderboard_position_counts`
- reads `leaderboard_adjustments` as authoritative adjustment input

**May call**
- reads official result truth from `results`-owned tables
- reads setup config from `season_setup`

**Must not own**
- result entry workflows
- public transport concerns

### `public_read`

**Owns**
- read-only, screen-shaped queries for public pages, maxi-screen, and other presentation-specific reads
- joining projection tables with stable descriptive data to build response DTOs

**Should read from**
- `leaderboard_current`
- `leaderboard_position_counts`
- stable setup tables
- allowed official-state reads when the screen explicitly needs current official result detail

**Must not own**
- authoritative writes
- domain validation
- lifecycle transitions

### `audit`

**Owns**
- append-only audit persistence for authoritative changes
- correlation grouping for one business workflow

**Tables / data it owns**
- `audit_logs`

**Public facade should answer**
- append audit rows from structured workflow facts
- query audit history for admin screens

**Must not own**
- business decision making
- projection-only churn

## Ownership by table

| Table | Owning module | Notes |
|---|---|---|
| `seasons`, `teams`, `competitions`, `games`, `game_fields`, `points` | `season_setup` | `games.state` is written through lifecycle workflows led by `event_operations` |
| `fields` | `season_setup` / seeded reference data | treated as seeded catalog, not end-user editable in v1 |
| `game_entries`, `game_entry_fields` | `results` | canonical official result truth |
| `tournament_matches` | `tournaments` | operational bracket record |
| `game_live_drafts` | `live_games` | provisional recovery snapshots only |
| `leaderboard_current`, `leaderboard_position_counts` | `leaderboard_projection` | derived read models |
| `leaderboard_adjustments` | `leaderboard_projection` | authoritative adjustment input |
| `users` | `users` | linked app-user truth |
| `roles`, `user_roles`, `role_capabilities`, `user_capabilities` | `authorization` | seeded roles, future-compatible direct grants |
| `audit_logs` | `audit` | append-only history |

## Allowed cross-module interaction patterns

Allowed:
- router -> module/application entrypoint
- module orchestrator -> other module `facade.py`
- read query service -> cross-table SQL when building a read model
- infrastructure adapter -> external system through explicit interface

Not allowed:
- importing another module's repository
- importing another module's ORM models directly as a convenience shortcut
- calling another module's domain internals
- putting cross-module orchestration in routers or background glue

## Where common changes should go

| Change | Default home |
|---|---|
| new capability or policy check | `authorization` |
| new superadmin provisioning behavior | `users` + `identity` adapter |
| new setup validation before results exist | `season_setup` |
| start / suspend / resolve / review state transition | `event_operations` |
| official placement / field validation or persistence | `results` |
| tournament pairing or bracket derivation | `tournaments` |
| live field lease, live revision, draft snapshot behavior | `live_games` |
| standings math or recomputation scope | `leaderboard_projection` |
| public leaderboard or maxi-screen response shaping | `public_read` |
| append-only audit behavior | `audit` |

## Red flags for reviewers and agents

Flag the change if you see any of these:
- a router directly updating multiple modules' tables
- `public_read` gaining write behavior
- `live_games` treated as official truth
- `season_setup` changing official results
- `results` owning game-state transitions
- cross-module imports that bypass `facade.py`
- read-model requirements implemented by moving business logic into SQL triggers

## Companion docs

- `docs/architecture/architecture.md` — boundary, invariants, lifecycle, source of truth
- `docs/architecture/runtime-flows.md` — exact sequencing for high-risk workflows
- `docs/domain/business-rules.md` — rule catalog
- `docs/domain/er-schema.md` — table and relationship detail
