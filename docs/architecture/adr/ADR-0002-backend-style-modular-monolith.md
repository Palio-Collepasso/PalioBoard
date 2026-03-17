# ADR-0002 — Api Style: Modular Monolith with Strict Module Boundaries

- Status: Accepted
- Date: 2026-03-11

## Context

The domain has multiple distinct concerns:

- season setup
- game lifecycle
- official result persistence
- tournaments
- live collaboration
- projections
- audit
- identity and authorization

The system is small enough for one deployable, but large enough that feature-folder sprawl would decay quickly.

## Decision

Adopt a Python modular monolith with explicit bounded modules.

Each module exposes a small public facade and keeps internals private.

Recommended module set:

- identity
- authorization
- users
- season_setup
- event_operations
- results
- tournaments
- live_games
- leaderboard_projection
- public_read
- audit

Rules:

- modules own their tables and repositories
- other modules may call only public facades/contracts
- cross-module orchestration lives in the application/use-case layer
- manual explicit wiring in a composition root
- no DI framework in v1

## Consequences

### Positive

- Strong internal boundaries without microservice complexity.
- Better fit for audit-heavy transactional workflows.
- Easier future extraction if one module grows significantly.

### Negative

- Requires discipline and CI checks to prevent boundary erosion.
- Some workflows will involve multiple module calls inside one transaction.

## Follow-ups

- Add automated architecture import checks in CI for api modules.
- Revisit DI only if dependency graphs become painful.
