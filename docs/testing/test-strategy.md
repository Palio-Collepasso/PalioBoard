# Test strategy

## Introduction

This document defines a practical, opinionated testing strategy for v1 of PalioBoard. Its goal is to protect the failure modes that matter most for this product: authoritative result correctness, state-transition correctness, leaderboard/projection correctness, live-collaboration safety, and immediate public visibility after official changes.

This is not a “test everything everywhere” strategy. The target is a small, high-signal suite that maps each risk area to the cheapest layer that can prove correctness with enough confidence. For this system, that means:
- pure domain rules belong in unit tests
- authoritative workflows belong in real Postgres integration tests
- live collaboration behavior belongs in targeted realtime integration tests
- only a handful of user-visible critical flows belong in Playwright E2E

The architecture and ADRs are explicit that the highest-risk failures are transactional, concurrent, and integration-heavy, and that the minimum required test depth depends on the kind of change being made.

## Testing principles for this repo

### 1. Test at the layer where the risk actually lives

Do not push DB-centric or orchestration-heavy behavior down into unit tests. The system’s correctness lives in backend workflows that open one transaction, write authoritative state, write audit rows, recompute affected projections, and only then commit. That shape must be tested with real Postgres, not mocks. 

### 2. Prefer the minimum layer that can prove the behavior

Use the lowest-cost layer that still exercises the real risk:
- pure calculation or validation rule -> unit test
- workflow touching DB state, audit, projections, locks, or immutability -> Postgres-backed integration test
- lease, stale-write, reconnect, restart, or realtime delivery behavior -> realtime integration test
- full user-visible critical flow -> Playwright E2E

This follows the required test-layer mapping defined in the architecture.

### 3. Keep E2E small and critical-path only

Playwright should cover only must-not-break operational flows. The ADR set explicitly calls for a small Playwright suite, not broad UI coverage.

### 4. Treat projections as outputs of workflows, not as independently edited state

Leaderboard and public-read correctness must be tested as the result of authoritative writes and synchronous recomputation, not by directly mutating projection tables or stubbing projection internals. Projection recomputation is part of the transaction for critical workflows.

### 5. Separate official truth from provisional live state

Live drafts and leases are technical collaboration state, not official business truth. Tests must reflect that:
- live draft behavior is tested in realtime integration
- official result materialization is tested in Postgres integration
- frontend tests must not assume in-progress live state counts toward standings
- E2E must verify user-facing conflict/recovery behavior, not internal live-store implementation details

This matches the live-collaboration ADR and the architecture’s live-draft invariants.

### 6. Protect trust-critical invariants first

The most important invariants for v1 are:
- no invalid official completion
- no silent live overwrite
- no incorrect leaderboard inclusion/exclusion
- no invalid Jolly reuse
- no broken Prepalio roll-up into Palio
- no mutation of game setup after official result data exists
- no authoritative write without audit
- no successful write when projection recomputation fails

These are driven by the PRD, requirements, and failure matrix.

### 7. Use thin slices as the default development rhythm

A valid thin slice includes one real workflow, real persistence, audit when authoritative, projection update when affected, and at least one matching test at the correct layer. Testing should follow that same vertical rhythm.

### 8. Avoid snapshot-heavy frontend tests

Do not use large snapshot suites as a substitute for behavior tests. The frontend is intentionally thin in business logic ownership; heavy snapshot testing adds maintenance cost without protecting the main risks. Ranking logic, state transitions, Jolly, Prepalio, and officialization belong in backend tests, not UI snapshots.

### 9. Static quality gates complement, but do not replace, behavioral tests

CI should also enforce architectural boundaries and contract hygiene using the repo’s agreed tooling. Ruff, Pyright, pytest, frontend lint/test/build, OpenAPI export/type generation checks, and import-boundary checks are part of the quality baseline.

Current backend baseline note: the scaffold introduced in TASK-2 ships a local import-boundary command at `cd apps/api && uv run python -m palio.shared.module_boundaries`. Later CI wiring should execute the same rule automatically.
TASK-7 adds `make openapi-export`, backed by `cd apps/api && uv run python -m palio.app.export_openapi ../../docs/api/openapi.yaml`, as the local contract-export command.

Current frontend baseline:
- TASK-3 introduces `cd apps/web && npm run check-boundaries`, backed by dependency-cruiser, as the initial CI-friendly import-boundary rule for shell isolation and generic `shared/` code.
- TASK-7 introduces `make openapi-types` and `cd apps/web && npm run generate:api-types` so the frontend can regenerate ignored TS declarations from the committed OpenAPI artifact without a running backend.
- TASK-9 will add the broader frontend and Playwright behavioral harnesses that complement this static guardrail.

## Test pyramid / test-layer overview

The recommended v1 testing pyramid is intentionally backend-heavy.

| Layer | Main purpose | Typical scope | Volume |
|---|---|---|---|
| Unit tests | Prove pure domain logic deterministically | placement validation, points calculation, ex aequo handling, Jolly math, Prepalio aggregation rules, tournament ranking derivation helpers | highest |
| Postgres-backed integration tests | Prove authoritative workflows and transactional consistency | state transitions, official result materialization, audit, projection recomputation, immutability, under-examination behavior, post-completion edits | high |
| Realtime integration tests | Prove collaboration safety and recovery behavior | field leases, stale/concurrent writes, monotonic revisions, reconnect/restart recovery, post-commit notifications | medium |
| Frontend tests | Prove UI behavior at component/feature boundary | form validation wiring, API error rendering, shell-specific rendering, realtime state replacement behavior | low-medium |
| Playwright E2E | Prove must-pass operational journeys | judge/admin/public critical paths only | very low |

Opinionated ratio:
- many unit tests for pure calculation and validation
- many fewer, but highly targeted, Postgres integration tests
- a small set of realtime integration tests
- a small set of frontend behavior tests
- a very small Playwright suite

## Mapping from change type to minimum required test type

| Change type | Minimum required test type | Why |
|---|---|---|
| Pure domain rule | Unit test | No DB/realtime needed; fastest signal |
| Placement validation or ex aequo scoring rule | Unit test | Pure deterministic rule |
| Jolly eligibility or Jolly points math | Unit test | Pure rule and calculation |
| Prepalio aggregation/tie strategy calculation | Unit test | Pure calculation logic |
| 1v1 ranking derivation helper | Unit test | Pure derivation logic |
| State transition | Postgres-backed integration test | Needs authoritative state + audit + projection side effects |
| Official write workflow | Postgres-backed integration test | Must prove transaction semantics |
| Result materialization from ranking live draft | Postgres-backed integration test | Writes canonical entries and audit rows |
| Edit completed result / pending admin review | Postgres-backed integration test | Official rewrite + audit + projection semantics |
| Under-examination mark/resolve | Postgres-backed integration test | Visibility vs counting semantics |
| Immutability after official result data | Postgres-backed integration test | DB-backed workflow/invariant |
| Manual standings adjustment | Postgres-backed integration test | Authoritative write with immediate projection effect |
| Projection / standings logic change | Unit tests plus Postgres-backed integration test | Pure calculation must be isolated; transaction/projection update must also be proven |
| Live field lease behavior | Realtime integration test | Requires connection-oriented behavior |
| Stale concurrent live write rejection | Realtime integration test | Requires revision/conflict semantics |
| Reconnect conflict recovery | Realtime integration test | Requires server/client state recovery path |
| Restart hydration from persisted draft snapshot | Realtime integration test | Requires live-store + persisted recovery behavior |
| Public propagation after commit | Realtime integration test and/or Playwright E2E if in critical flow | Realtime is post-commit and user-visible |
| Critical user-visible operational workflow | Playwright E2E | Protect real browser flow already designated as critical |
| Frontend-only rendering or error-message mapping | Frontend test | No full browser suite needed |
| API contract surface change | Frontend/API integration test plus CI contract checks | Protect typed contract drift |

This aligns with the architecture’s explicit mapping for risky changes.

## Unit tests

### What belongs here

Unit tests should cover logic that is:
- pure
- deterministic
- cheap to run
- independent of database state, realtime transport, and framework wiring

Primary v1 candidates:
- placement structure validation, including valid ties like `1,2,2,4` and rejection of invalid structures
- points-table application
- ex aequo point splitting logic
- Jolly points doubling math
- Jolly eligibility helper logic when expressed as pure domain rule inputs
- Prepalio aggregate point summation
- Prepalio final ranking derivation from subgame totals
- configurable tie-strategy helpers for Prepalio aggregation
- 1v1 final ranking derivation from semifinal/final winners
- small policy/helper objects that encode state-machine legality without side effects
- DTO/domain mappers that are genuinely pure

Requirements explicitly call out placement validation, Jolly rules, Prepalio aggregation, and 1v1 final ranking derivation as core domain behavior.

### Unit-test style guidance

- Favor table-driven cases for scoring and placement validation.
- Test edge cases aggressively; these are the highest value at this layer.
- Keep fixtures minimal and explicit: four teams, one game, one points table.
- Do not mock repositories for logic that should instead be tested as a real workflow in integration.
- Keep unit tests free of ORM, SQL, WebSocket, or HTTP concerns.

### Must-cover unit domains

#### Placement and scoring
- valid explicit ties
- invalid placement gaps/duplicates
- default `4,3,2,1`
- custom points table handling
- ex aequo point assignment

#### Jolly
- doubling points only for Palio
- no Jolly in Prepalio or Giocasport
- summary derivation helpers if implemented as pure read logic

#### Prepalio
- subgame point accumulation
- aggregate ranking computation
- mapping aggregate final ranking back into Palio points
- unresolved tie cases that require admin override signaling

#### Tournament derivation
- ranking derivation from four match winners
- override-allowed cases represented cleanly

### What does not belong here

Do not try to prove the following with unit tests:
- one-transaction authoritative workflows
- audit persistence
- projection-table updates
- row locking or optimistic version semantics
- live leases
- restart recovery
- public update propagation
- immutability enforcement through real write paths

Those belong at heavier layers.

## Postgres-backed integration tests

### Why this layer is first-class

This project is DB-centric by design:
- official state is DB-backed
- audit is required for authoritative changes
- projections are recomputed in the same transaction
- a command succeeds only if authoritative state, audit, and required projection updates all succeed
- games and related configuration become immutable after official result data exists

Those are integration concerns, not unit concerns.

### Environment expectations

These tests should run against a real local PostgreSQL instance, matching the accepted testing strategy. Avoid SQLite substitutions; they will not faithfully protect transaction behavior, constraints, JSONB usage, or locking semantics.

Recommended setup:
- apply real migrations
- use per-test or per-module database isolation
- seed minimal static data needed for the slice
- exercise real repositories, Unit of Work, and orchestrator/application service boundaries
- assert persisted authoritative tables, audit rows, and projection tables together

### Core behaviors to cover here

#### State transitions
- `draft -> in_progress` increments `live_cycle`
- ranking game start prefills live draft from current official entries
- `in_progress -> completed` validates structure, materializes changes, audits, and recomputes projections
- `in_progress -> under_examination` materializes changes, audits, and excludes the game from leaderboard projections
- completed-result edit moves game to `pending_admin_review`
- admin review resolution can move back to `completed`
- mark/resolve `under_examination` preserves visibility semantics correctly

The allowed transitions and side effects are explicitly defined.

#### Official result materialization
- only changed ranking draft values are materialized into `game_entries` / `game_entry_fields`
- 1v1 match saves materialize canonical official per-team entries immediately
- leaderboard changes for 1v1 happen only when the tournament/game is completed
- current official placement in `game_entries` is the canonical source for projections

This is a central architectural decision.

#### Projection recomputation
- completing a ranking game updates affected standings
- under-examination excludes the game from standings while keeping official result visible
- pending admin review still counts
- Prepalio subgames update Prepalio aggregate ranking, which then updates Palio standings
- Giocasport remains isolated from Palio standings
- manual leaderboard adjustments apply immediately
- projection recomputation failure rolls back the whole command

Projection logic is synchronous and current-state only.

#### Audit
- authoritative writes produce audit rows
- one row per changed authoritative entity where relevant
- correlation id is shared across one workflow
- projection churn is not audited
- live keystrokes are not audited
- post-completion edits produce auditable before/after history

Audit is mandatory for authoritative changes.

#### Immutability
- game deletion is blocked once official result data exists
- game property edits are blocked once official result data exists
- game-field configuration edits are blocked once official result data exists
- points-table edits are blocked once official result data exists

The ER and requirements make this rule explicit.

#### Transactional guarantees and failure handling
- if audit insert fails, authoritative write is rolled back
- if projection recomputation fails, authoritative write is rolled back
- draft cleanup failure after leaving `in_progress` does not fail the business transaction
- idempotent retry returns the same logical outcome

The failure matrix is architecture-level behavior and deserves direct tests.

### Recommended structure of these tests

Organize around use cases, not tables:
- `test_start_ranking_game.py`
- `test_complete_ranking_game.py`
- `test_mark_under_examination.py`
- `test_edit_completed_result.py`
- `test_resolve_pending_admin_review.py`
- `test_manual_leaderboard_adjustment.py`
- `test_complete_prepalio_subgame.py`
- `test_complete_tournament_game.py`
- `test_game_immutability.py`

Each test should usually assert three things together:
1. authoritative write state
2. audit side effects
3. projection/read-model effects

That is the minimum bundle of correctness for this architecture.

### What not to test here

Do not overuse this layer for:
- pure scoring tables with many input combinations better covered by unit tests
- CSS/layout behavior
- browser navigation polish
- low-level WebSocket client rendering details

## Realtime integration tests

### Why this layer exists

Live collaboration risk is explicitly different from authoritative-write risk. The system must support:
- field-level exclusive editing
- stale-write rejection
- reconnect/conflict recovery
- restart recovery using persisted draft snapshots
- multiple games in progress
- post-commit realtime notifications for public/admin views

Those behaviors depend on memory-first live state and transport semantics, so they deserve targeted realtime integration tests.

### Scope of this layer

These are backend integration tests that exercise real realtime endpoints or the live subsystem boundary with realistic connection/session behavior. They should not require a browser unless the browser itself is the thing being tested.

### Critical scenarios to cover

#### Field lease and conflict behavior
- user A acquires a field lease, user B is blocked or receives a structured conflict response
- stale revision update is rejected with machine-readable error payload
- non-conflicting field edits can proceed when allowed by design
- a lease expires or is released correctly if that behavior exists

#### Reconnect recovery
- client reconnects and receives the latest server snapshot
- client conflict path replaces local state from newer server revision
- reconnect messaging surfaces conflict in a structured way suitable for UI handling

Requirements explicitly require server-state restoration and user-visible conflict handling.

#### Restart recovery
- persisted `game_live_drafts` snapshot reloads after backend restart / store reset
- stale snapshot from previous `live_cycle` is ignored
- active leases are not restored and must be reacquired after restart

This behavior is explicitly documented in both architecture and ER semantics.

#### Revision monotonicity
- every accepted live update advances per-game revision
- clients replace local state only when revision is newer
- duplicate/out-of-order messages do not regress client state

#### Public/admin propagation
- official completion emits post-commit notification
- public/maxi consumers recover correctly by refetching/read models when realtime delivery is missed
- no standings update is emitted from provisional in-progress ranking data

The architecture is explicit that realtime is best-effort and post-commit only.

### What not to test here

Do not turn this layer into full browser E2E for every conflict scenario. Also do not duplicate pure placement/Jolly/Prepalio calculation tests here. Keep the focus on connection, lease, revision, and recovery semantics.

## Frontend tests

### What frontend tests are for in this repo

Frontend tests should prove that the Angular app:
- renders the right state from API/read-model data
- sends the intended commands
- handles structured backend errors correctly
- reacts properly to realtime snapshots and conflict messages
- keeps public/admin/maxi concerns separated at the shell/feature level

The frontend does not own standings logic, authorization truth, or official result truth, so tests should not pretend otherwise.

### Good frontend-test targets

#### Admin/judge operational screens
- complete button disabled until required placement/field data is present
- machine-readable backend errors render appropriate user-facing messages
- pending-admin-review and under-examination badges/labels render correctly
- tournament progression UI reflects bracket state received from backend
- Jolly flag controls appear only where allowed

#### Public/maxi screens
- public pages render standings/results/history from read models
- under-examination result remains visible but clearly marked
- public pages do not show stale local assumptions after a newer fetch/realtime update
- live pages replace state on newer snapshot revision

#### API facade / adapter tests
- typed mapping from backend envelopes to UI models
- no accidental mixing of admin/public/realtime surfaces
- OpenAPI/type-generation changes are consumed correctly

### What to avoid

Do not:
- rebuild backend business rules in frontend tests
- use broad component snapshots as a safety blanket
- test every template permutation
- assert CSS details unless they carry operational meaning
- duplicate Playwright coverage for the same full user journey

### Recommended frontend-test style

- prefer focused component/feature tests over giant shell-level tests
- mock network boundaries, not deep component internals
- assert behavior and rendered decisions, not markup trivia

## Playwright E2E

### Purpose

Playwright exists to prove that the most important real user journeys still work end to end across browser, frontend, backend, database, projections, and realtime surfaces.

It should remain small. The requirements and ADRs define the must-pass E2E set explicitly.

### Scope rules

A flow deserves Playwright coverage only when all of the following are true:
- it is user-visible
- it crosses multiple architectural layers
- failure would materially damage event operations or public trust
- the flow is already part of the critical set, or it is close enough to justify replacing a lower-signal test

### Recommended Playwright style

- use seeded test data with deterministic four-team scenarios
- keep each spec focused on one operational story
- prefer robust user-visible assertions over internal polling hacks
- avoid covering every validation branch in the browser; most branches belong in unit/integration tests
- keep flaky realtime timing under control with deterministic server fixtures when possible

## Critical must-pass E2E flows

The following should be treated as the must-pass Playwright set for v1.

### 1. Complete a ranking game successfully
Assert:
- judge/admin starts a ranking game
- enters team-by-team data
- enters valid final placements
- completes the game
- sees completion success and updated official state
- relevant leaderboard/public read model reflects the result

This is explicitly part of the critical E2E set.

### 2. Public view updates after official completion
Assert:
- a ranking or tournament completion changes official result
- public page shows updated result/standings without manual back-office intervention
- update happens through the real read model, not direct write-table reads

Immediate public visibility is a product success criterion.

### 3. Progress and complete a 1v1 tournament
Assert:
- pairings are set
- semifinal winners are recorded
- bracket progression becomes visible while in progress
- final ranking is derived
- leaderboard changes only after tournament completion

This behavior is explicitly required.

### 4. Post-completion edit and admin review behavior
Assert:
- a completed result is edited by a judge
- latest official result remains visible/counting
- game moves to `pending_admin_review`
- admin can review and resolve back to `completed`
- audit/history-facing cues are present where expected

This is both a critical flow and a major trust-risk area.

### 5. Concurrent live-result updates with field locking/conflict behavior
Assert:
- two judge sessions interact with the same in-progress ranking game
- field lock / lease behavior prevents silent overwrite
- stale update is rejected
- user sees recoverable conflict behavior

This is explicitly a must-pass E2E behavior.

### Flows that are important but should usually stay below E2E

Keep these mainly in integration/realtime tests unless they become proven browser regressions:
- full matrix of placement-validation edge cases
- Jolly reuse rejection
- Prepalio aggregation math
- immutability after official result data
- restart hydration from persisted draft snapshot
- projection rollback on audit/projection failure
- manual standings adjustment arithmetic

## Recommended slice-by-slice workflow

The preferred development loop for v1 is:

### 1. Start from one acceptance scenario
Write or refine the scenario in Given / When / Then form first. The scenario should describe one vertical slice, such as:
- start ranking game
- complete ranking game
- save tournament semifinal winner
- mark game under examination
- apply manual standings adjustment

This matches the architecture’s definition of a valid thin slice.

### 2. Identify the real risk in that slice
Ask which of these is actually being changed:
- pure domain rule
- authoritative workflow
- projection behavior
- live collaboration behavior
- UI wiring only
- full user-visible critical path

### 3. Add the minimum matching tests
Default rule:
- pure rule -> unit tests
- authoritative workflow -> Postgres integration test
- live collaboration -> realtime integration test
- critical user-visible flow -> Playwright only if already in the critical set
- optional focused frontend test if UI behavior itself is non-trivial

### 4. Implement the slice vertically
Use the real orchestrator/module boundaries, real persistence, and real projection path for the slice. Do not fake architecture with shortcuts just to satisfy a test. Forbidden shortcuts are called out explicitly in the architecture.

### 5. Run the narrowest meaningful suite first
Typical order during development:
1. affected unit tests
2. affected integration/realtime tests
3. affected frontend tests
4. Playwright only when the slice touches a critical E2E flow or before merging a substantial cross-layer change

### 6. Add or widen E2E only when the slice changes critical operational behavior
Do not add a browser test for every new rule. E2E is there to prove operations still work, not to become the main correctness harness.

### 7. Refactor with tests preserving boundaries
If implementation pressure suggests moving logic into Angular, SQL triggers, ad hoc scripts, or projection tables, stop and fix the design instead. That would violate the architectural ownership model.

## What not to test at each layer

### Unit tests should not test
- SQL queries
- ORM configuration
- transaction rollbacks
- audit persistence
- row locking
- live transport
- browser behavior
- projection table persistence

### Postgres-backed integration tests should not test
- every pure arithmetic permutation already covered by unit tests
- browser routing
- visual layout
- WebSocket rendering details in the browser

### Realtime integration tests should not test
- all placement/scoring math
- general projection arithmetic
- cosmetic UI details
- every full end-to-end journey

### Frontend tests should not test
- backend business rules as if owned by Angular
- leaderboard calculation internals
- Jolly/Prepalio/tournament logic duplicated from backend
- large snapshots of entire pages

### Playwright E2E should not test
- every validation branch
- every error code variant
- every scoring edge case
- internal DB details
- low-level transport mechanics better proven by realtime integration tests

## Appendix: example test cases by feature area

### Ranking game lifecycle
- unit: placement validator accepts `1,2,2,4` and rejects invalid structures
- Postgres integration: completing ranking game materializes changed entries only, writes audit, recomputes leaderboard
- realtime integration: stale live update is rejected after newer revision is accepted
- frontend: complete button stays disabled until required data is present
- Playwright: judge completes ranking game and public standings update

### Jolly
- unit: Jolly doubles awarded Palio points
- unit: Jolly not allowed for Prepalio/Giocasport competition contexts
- Postgres integration: reusing Jolly in a second Palio game is rejected and no authoritative write occurs
- frontend: Jolly indicator renders in summary/public result views where applicable

### Prepalio
- unit: aggregate ranking is computed from Prepalio subgame points
- unit: unresolved aggregate tie yields “manual override required” outcome
- Postgres integration: completing a Prepalio subgame updates Prepalio aggregate and then main Palio standings
- frontend: public view shows Prepalio separately from Palio and Giocasport

### 1v1 tournament
- unit: final ranking derivation from four match winners
- Postgres integration: saving match winners updates `tournament_matches` and canonical `game_entries`
- Postgres integration: leaderboard does not change until tournament completion
- Playwright: judge/admin progresses and completes tournament through the UI

### Post-completion edits and review
- Postgres integration: editing a completed result writes new official state, writes audit, and moves to `pending_admin_review`
- Postgres integration: admin resolution returns state to `completed` and preserves append-only history
- Playwright: operational review flow behaves correctly end to end

### Under examination
- Postgres integration: marking a game under examination keeps official result visible but removes it from standings
- Postgres integration: resolving under examination restores counting behavior
- frontend: public page displays provisional / under-examination label correctly

### Immutability
- Postgres integration: game field selection cannot change after official result data exists
- Postgres integration: points table cannot change after official result data exists
- Postgres integration: delete game is rejected after official result data exists

### Reconnect and restart recovery
- realtime integration: reconnect returns latest snapshot and conflict metadata
- realtime integration: restart reloads persisted draft snapshot from `game_live_drafts`
- realtime integration: stale snapshot from old `live_cycle` is ignored
- frontend: client replaces local live state only when incoming revision is newer

### Public update propagation
- realtime integration: post-commit notification is emitted only after authoritative success
- Postgres integration: if projection recomputation fails, no public-visible official update exists
- Playwright: public page reflects official change after completion without relying on admin-only pages
