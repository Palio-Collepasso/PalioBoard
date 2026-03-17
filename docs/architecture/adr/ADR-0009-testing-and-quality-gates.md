# ADR-0009 — Testing and Quality Gates

- Status: Accepted
- Date: 2026-03-11

## Context

The highest-risk failures are transactional, concurrent, and integration-heavy:

- standings correctness
- result officialization
- post-completion edits
- 1v1 progression
- live-entry conflicts
- frontend/api contract drift

## Decision

Api testing strategy:

- pure unit tests for domain logic
- integration tests against real local PostgreSQL
- targeted realtime tests for WebSocket behavior

Frontend testing strategy:

- local unit/integration where valuable
- small Playwright suite for must-pass user flows

Must-pass E2E:

- complete ranking-template game
- public update after completion
- 1v1 progression/completion
- post-completion edit behavior
- concurrent live-result locking/conflict behavior

Quality/tooling:

- Python: Ruff + Pyright + pytest + pre-commit
- frontend: npm-based lint/test/build
- monorepo: make as stable command surface
- architectural import checks in CI for api and frontend boundaries

## Consequences

### Positive

- Quality gates align with the actual failure modes of the product.
- Architectural boundaries are enforced automatically, not only socially.
- Contract drift is reduced.

### Negative

- Integration tests are heavier than SQLite/mock-based approaches.
- E2E flows still require careful maintenance.

## Follow-ups

- Keep the Playwright suite small and critical-path only.
- Keep api integration tests first-class, because correctness is DB-centric.
