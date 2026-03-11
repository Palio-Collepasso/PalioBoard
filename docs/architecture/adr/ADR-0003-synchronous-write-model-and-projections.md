# ADR-0003 — Synchronous Write Model and Current-State Projections

- Status: Accepted
- Date: 2026-03-11

## Context

Official state changes must be visible quickly and reliably. The leaderboard is central to the product and must not drift from accepted official writes.

The domain includes:

- Jolly
- Prepalio roll-up
- manual standings adjustments
- post-completion edits
- under-examination exclusions

## Decision

Use synchronous transactional writes for business correctness.

Each critical workflow:

1. validates capability and domain rules
2. opens one Unit of Work / DB transaction
3. updates authoritative state
4. writes audit rows
5. fully recomputes the affected current projection scope
6. commits once

Projection rules:

- `leaderboard_current` and related read models are current-state only
- recomputation is full recompute of affected scope, not incremental delta math
- projection logic lives in Python application services
- projection tables are not audited

Realtime rules:

- notifications are post-commit only
- delivery is best-effort and ephemeral
- clients recover by refetching from DB-backed read models

## Consequences

### Positive

- Easier correctness reasoning.
- Easier replay/rebuild later.
- No hidden eventual-consistency gap for official state.

### Negative

- Writes are heavier than async/event-driven designs.
- Projection updates stay on the critical path.

## Follow-ups

- Keep affected-scope recomputation deterministic and well tested.
- Do not introduce DB triggers for business orchestration.
