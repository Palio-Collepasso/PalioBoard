# Test Strategy

## Purpose

Describe how PalioBoard chooses test depth, what must be covered for risky changes, and how teams should think about validation during implementation and review.

## Goals

- Protect standings correctness, official result truth, and lifecycle rules.
- Catch regressions at the cheapest reliable layer.
- Reserve slower end-to-end tests for user-visible critical flows.
- Keep the testing model aligned with the modular-monolith architecture.

## Architecture-informed risk model

The highest-risk changes in PalioBoard are:
- official result persistence and materialization;
- game lifecycle transitions;
- standings/projection logic;
- live ranking collaboration and conflict recovery;
- tournament progression;
- authorization/capability checks on sensitive actions;
- public/maxi visibility after authoritative changes.

These areas require deeper validation than routine UI or presentation-only changes.

## Test layers

| Layer | Purpose | Typical scope | When it is strongest |
|---|---|---|---|
| Unit | Validate pure rules and calculations | placement validation, Jolly rules, projection helpers | deterministic domain logic |
| Integration | Validate real orchestration with Postgres and module boundaries | official writes, transitions, audit, recompute | authoritative workflows |
| Realtime integration | Validate collaboration semantics and conflict handling | lease acquisition, stale writes, reconnect recovery | WebSocket/SSE/live ranking |
| API contract | Validate payload shape, status codes, and error semantics | REST/realtime response envelopes | backend/frontend compatibility |
| E2E | Validate user-visible critical flows across UI + backend | ranking completion, tournament progression, public update | release confidence |
| Manual verification | Validate environment-specific or operational concerns | deploy smoke, browser quirks, operator checks | before release or when automation is not practical |

## Guiding principles

- Prefer the cheapest test that can reliably catch the risk.
- Critical business rules need direct tests, not only incidental coverage.
- Bug fixes should add a regression test when practical.
- Changes to machine-readable errors should update contract coverage.
- New critical journeys should be added to the E2E set only when they truly protect release confidence.

## Minimum test matrix

| Change type | Unit | Integration | Realtime integration | API contract | E2E | Manual |
|---|---|---|---|---|---|---|
| Pure domain rule | required | optional | no | optional | no | optional |
| State transition or official write workflow | maybe | required | no | maybe | maybe | optional |
| Projection / standings logic | required | required | no | optional | maybe | optional |
| Live entry / lease / conflict behavior | maybe | maybe | required | maybe | maybe | optional |
| API error/contract change | optional | required | maybe | required | optional | optional |
| User-visible critical flow already in the critical set | maybe | maybe | maybe | optional | required | optional |
| Pure UI/presentation refactor | optional | no | no | no | optional | optional |
| Deploy / runtime ops change | no | maybe | no | no | no | required |

## Required risky-change rules

These are the default minimums for PalioBoard:
- **Pure domain rule** → unit tests.
- **State transition or official write workflow** → Postgres-backed integration tests.
- **Projection or standings logic** → unit tests for pure calculation plus integration tests for transaction/projection update.
- **Live entry / lease / conflict behavior** → realtime integration tests.
- **User-visible critical flow** → Playwright E2E when the flow is already part of the critical E2E set.

## Unit tests

### Purpose

Prove pure logic without requiring network, browser, or database orchestration.

### Typical PalioBoard targets

- placement validation including explicit ties;
- Jolly eligibility and repeated-use rejection;
- Prepalio aggregate ranking helpers;
- tournament ranking derivation helpers;
- capability/policy helpers that are truly pure;
- projection helper logic.

### What not to test here

- transaction behavior;
- audit persistence;
- row locking or concurrent live entry behavior;
- end-to-end screen flow.

### Starter checklist

- [ ] includes normal case
- [ ] includes at least one edge case
- [ ] includes at least one invalid input case when relevant
- [ ] names the rule being protected

## Integration tests

### Purpose

Prove authoritative workflows against real persistence and module orchestration.

### Required for PalioBoard

- start/complete/under-examination transitions;
- completed-result edit → `pending_admin_review` behavior;
- admin review resolution;
- official entry materialization;
- tournament match save and progression;
- projection recompute after authoritative change;
- audit row creation for authoritative business changes.

### Expectations

- run against Postgres, not an in-memory imitation;
- validate both state change and required side effects;
- assert that transaction rollback occurs when required side effects fail.

### Starter checklist

- [ ] validates final authoritative state
- [ ] validates audit expectations when applicable
- [ ] validates projection/read-model effects when applicable
- [ ] validates blocked state transitions when relevant

## Realtime integration tests

### Purpose

Prove live collaboration safety in ranking games.

### Required scenarios

- field lease acquisition and rejection when already leased;
- stale revision rejection with server-provided current version;
- reconnect recovery to latest server state;
- live draft initialization from official result on start;
- `live_cycle` invalidation of stale drafts after leaving `in_progress`.

### Expectations

- test at the transport/application boundary actually used by the live subsystem;
- prefer deterministic orchestration over timing-sensitive ad hoc sleeps.

## API contract tests

### Purpose

Prove that backend and frontend agree on status codes, error codes, and payload shapes.

### Required when

- introducing or changing machine-readable error codes;
- changing success payload shape for consumed endpoints;
- changing validation semantics or details structure.

### Starter assertions

- `error.code` is stable and machine-readable;
- the expected HTTP status is returned;
- concurrency errors contain structured recovery details;
- validation errors identify field-level issues where possible.

## End-to-end tests

### Purpose

Protect release-critical user journeys that cross UI, backend, and persistence boundaries.

### Current critical E2E set for v1

- complete a ranking game;
- verify public update after completion;
- progress and complete a 1v1 tournament;
- edit a completed result and verify review/audit behavior;
- concurrent live updates and field locking.

See `docs/testing/critical-e2e-flows.md` for the detailed flows.

### Add a new critical E2E flow only when

- the flow is directly tied to core business value or trust;
- unit/integration coverage alone would not meaningfully protect it;
- the flow is stable enough to avoid chronic flakiness.

## Manual verification

Manual checks are still valuable for:
- deploy smoke verification;
- public/maxi screen presentation sanity;
- browser/device-specific issues;
- operator workflows not yet automated.

Document manual checks in the PR when they matter.

## Fixture policy

Canonical shared fixtures live in `docs/testing/fixtures.md` and in the corresponding test data source files.

Rules:
- prefer named business scenarios over anonymous seed blobs;
- keep shared fixtures deterministic;
- document any fixture that multiple suites depend on;
- update fixture docs when assumptions change.

## Flaky test policy

- A flaky test is one that fails without a product regression.
- Flaky tests should be fixed, quarantined, or removed quickly.
- A known flaky test should not silently remain in the required merge gate forever.
- If a critical E2E flow is flaky, reduce fragility or move part of its protection to integration coverage.

## Commands

Replace these placeholders with the real repo commands.

- **Run all backend tests:** `<repo command>`
- **Run backend unit tests:** `<repo command>`
- **Run backend integration tests:** `<repo command>`
- **Run web tests:** `<repo command>`
- **Run E2E tests:** `<repo command>`
- **Run lint/type checks:** `<repo command>`

## Review checklist

- [ ] The chosen test depth matches the risk of the change.
- [ ] Business-rule changes have direct coverage.
- [ ] Official-write workflows use integration tests.
- [ ] Projection changes include both calculation and workflow coverage when needed.
- [ ] Live ranking collaboration changes include realtime integration coverage.
- [ ] Critical user-flow changes updated the E2E set when needed.
- [ ] Fixture assumptions were updated if the change affects shared scenarios.

## Starter examples

### Example: Jolly validation change

Minimum expected coverage:
- unit tests for the pure Jolly rule;
- integration test proving the authoritative workflow rejects a repeated Jolly use;
- API contract assertion if the error payload or code changed.

### Example: ranking live-field lease change

Minimum expected coverage:
- realtime integration tests for lease acquisition, rejection, and recovery;
- integration or API-contract coverage if the payload changed;
- E2E only if the user-visible critical collaboration journey changed materially.

### Example: public leaderboard rendering-only tweak

Minimum expected coverage:
- frontend component/unit test or visual test if available;
- no new backend integration coverage unless backend behavior changed.
