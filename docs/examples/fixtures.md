# Test Fixtures

## Purpose

Document the named fixtures, seeds, and canonical data scenarios used by PalioBoard tests.

Good fixture documentation helps agents and humans answer:
- which scenario already exists;
- when a shared fixture is safe to modify;
- which tests depend on a given dataset;
- whether a failure is caused by product logic or by broken fixture assumptions.

## Principles

- Fixtures should be deterministic.
- Fixtures should be minimal but realistic.
- Shared fixtures should model recognizable business scenarios.
- If multiple suites depend on a fixture, document it here.

## Fixture index

| Fixture ID | Name | Scope | Used by | Source |
|---|---|---|---|---|
| `FX-001` | Base season with four teams | integration / e2e | many suites | `<replace with path>` |
| `FX-002` | Draft ranking game ready for completion | integration / e2e | ranking flows | `<replace with path>` |
| `FX-003` | In-progress ranking game with live revision state | realtime / e2e | collaboration flows | `<replace with path>` |
| `FX-004` | Completed Palio game with review/edit scenario | integration / e2e | post-completion review flows | `<replace with path>` |
| `FX-005` | Tournament game with semifinal pairings | integration / e2e | tournament flows | `<replace with path>` |

---

## Active fixtures

### `FX-001` — Base season with four teams

- **Status:** `active`
- **Scope:** `integration / e2e`
- **Purpose:** Provide the canonical v1 season baseline: one season, four teams, and the three competition contexts.
- **Defined in:** `<replace with fixture file/path>`
- **Used by:**
  - ranking completion flows
  - tournament flows
  - public standings flows

#### Scenario represented

A newly initialized PalioBoard season with the standard four teams, supported competitions, and baseline users/capabilities needed for tests.

#### Contents

- one active season;
- four teams/rioni;
- competition contexts `palio`, `prepalio`, `giocasport`;
- at least one admin user and one judge user;
- default or typical points configuration.

#### Important values / assumptions

- exactly four teams exist;
- user identities remain stable across dependent tests;
- the fixture is the parent dependency for most other shared fixtures.

#### Setup instructions

1. Seed the canonical season baseline before specialized game fixtures.
2. Reuse team identifiers rather than creating suite-specific copies unless isolation requires it.

#### Reset / cleanup instructions

1. Reset database state to the suite baseline.
2. Re-seed the season before dependent fixture setup.

#### Safe to modify?

- **Yes/No:** `no, not casually`
- **Constraints:** team identities, competition contexts, and user roles/capabilities should remain stable because many tests depend on them.

#### Related business rules

- `BR-001`

#### Related E2E flows

- `E2E-001`
- `E2E-002`
- `E2E-003`
- `E2E-004`
- `E2E-005`

### `FX-002` — Draft ranking game ready for completion

- **Status:** `active`
- **Scope:** `integration / e2e`
- **Purpose:** Support the normal ranking-game happy path and completion validation.
- **Defined in:** `<replace with fixture file/path>`
- **Used by:**
  - ranking completion tests
  - public update after completion

#### Scenario represented

A ranking-format game exists in `draft`, belongs to a known competition, has configured fields and points table, and can be started/completed in a short path.

#### Contents

- one ranking game in `draft`;
- configured result fields, including at least one required field;
- no official result data yet.

#### Important values / assumptions

- the game should be simple enough for smoke and E2E tests;
- if it is a Palio game, Jolly validity rules can be exercised;
- no previous Jolly usage should make the happy path invalid by accident.

#### Setup instructions

1. Seed `FX-001`.
2. Insert one ranking game with configured fields and default points table.

#### Reset / cleanup instructions

1. Reset or recreate the game between tests that mutate authoritative state.

#### Safe to modify?

- **Yes/No:** `yes, carefully`
- **Constraints:** keep one straightforward happy-path ranking scenario available.

#### Related business rules

- `BR-002`
- `BR-003`
- `BR-005`

#### Related E2E flows

- `E2E-001`
- `E2E-002`

### `FX-003` — In-progress ranking game with live revision state

- **Status:** `active`
- **Scope:** `realtime / e2e`
- **Purpose:** Exercise field leases, stale-write rejection, reconnect recovery, and live-cycle behavior.
- **Defined in:** `<replace with fixture file/path>`
- **Used by:**
  - realtime collaboration tests
  - concurrency E2E flows

#### Scenario represented

A ranking game is already `in_progress`, has initialized live draft state, and supports two concurrent editors.

#### Contents

- one ranking game in `in_progress`;
- initial live revision number;
- at least one leased-editable field/team combination;
- optionally a saved provisional draft snapshot for restart recovery.

#### Important values / assumptions

- the game still has official result baseline data from which the live draft was derived;
- revision increments are deterministic;
- editors can be represented by two distinct authenticated users.

#### Setup instructions

1. Seed `FX-001`.
2. Start a ranking game programmatically or through the application workflow.
3. Initialize live draft state and, if needed, acquire a test lease.

#### Reset / cleanup instructions

1. Clear live in-memory state and persisted recovery snapshots.
2. Recreate the game or reset `live_cycle` assumptions before reuse.

#### Safe to modify?

- **Yes/No:** `no, not casually`
- **Constraints:** revision, lease, and recovery semantics must remain stable for collaboration suites.

#### Related business rules

- `BR-006`

#### Related E2E flows

- `E2E-005`

### `FX-004` — Completed Palio game with review/edit scenario

- **Status:** `active`
- **Scope:** `integration / e2e`
- **Purpose:** Validate post-completion editing, `pending_admin_review`, and counting-state semantics.
- **Defined in:** `<replace with fixture file/path>`
- **Used by:**
  - review workflow tests
  - public/state-counting tests

#### Scenario represented

A completed Palio game already affects standings and contains a valid authoritative result that can be edited by a judge and resolved by an admin.

#### Contents

- one completed Palio game;
- official per-team entries already materialized;
- standings already reflect the current result;
- a judge and an admin user.

#### Important values / assumptions

- the baseline result should be easy to change visibly;
- if Jolly is present, its meaning should be explicit and testable;
- audit assertions depend on this fixture producing new authoritative writes on edit.

#### Setup instructions

1. Seed `FX-001`.
2. Create or complete a Palio game with known placements.
3. Ensure the standings projection includes the game before the test begins.

#### Reset / cleanup instructions

1. Reset authoritative state between tests that perform post-completion edits.
2. Clear related audit expectations if using snapshot-based assertions.

#### Safe to modify?

- **Yes/No:** `carefully`
- **Constraints:** keep at least one stable review/edit scenario with predictable standings impact.

#### Related business rules

- `BR-004`
- `BR-005`
- `BR-009`

#### Related E2E flows

- `E2E-004`

### `FX-005` — Tournament game with semifinal pairings

- **Status:** `active`
- **Scope:** `integration / e2e`
- **Purpose:** Support tournament progression, official match save behavior, and deferred leaderboard impact until completion.
- **Defined in:** `<replace with fixture file/path>`
- **Used by:**
  - tournament progression tests
  - tournament E2E flow

#### Scenario represented

A four-team 1v1 tournament exists with semifinal pairings configured and ready to progress through all matches.

#### Contents

- one `tournament_1v1` game;
- semifinal pairings;
- empty or initial match outcomes;
- known expected final ranking for the test path.

#### Important values / assumptions

- pairings must be explicit before start;
- match winners should deterministically imply a final ranking;
- leaderboard should remain unchanged until completion.

#### Setup instructions

1. Seed `FX-001`.
2. Create a tournament game and attach semifinal pairings.

#### Reset / cleanup instructions

1. Reset match outcomes and authoritative entries between tests.

#### Safe to modify?

- **Yes/No:** `yes, with care`
- **Constraints:** keep one canonical straightforward tournament path for fast E2E coverage.

#### Related business rules

- `BR-007`

#### Related E2E flows

- `E2E-003`

## Canonical scenario sets

### `CS-001` — Core happy-path release set

- **Purpose:** Minimal scenario bundle required to validate release-critical user flows.
- **Fixtures included:**
  - `FX-001`
  - `FX-002`
  - `FX-004`
  - `FX-005`
- **Used for:**
  - release smoke
  - critical E2E runs

### `CS-002` — Live collaboration set

- **Purpose:** Validate ranking live-entry concurrency and recovery.
- **Fixtures included:**
  - `FX-001`
  - `FX-003`
- **Used for:**
  - realtime integration suites
  - concurrency-focused E2E/manual checks
