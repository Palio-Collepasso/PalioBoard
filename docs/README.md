# Documentation map

Read this file first when you need repo context.

## Product
- `docs/product/prd.md` — product scope, goals, non-goals
- `docs/product/functional-requirements.md` — required behavior and critical flows
- `docs/product/acceptance-scenarios.md` — acceptance criteria and Given/When/Then examples

## Architecture and decisions
- `docs/architecture/architecture.md` — baseline system shape, boundaries, ownership, delivery conventions
- `docs/architecture/adr/` — architectural decision records

## Domain and data
- `docs/domain/er-schema.md` — entities and relationships
- `docs/domain/business-rules.md` — invariants and business semantics.
- `docs/domain/game-catalog.md` — seeded game fields / configuration catalog
- `docs/domain/palio-rules.md` — official source rules from the real-world event
- `docs/domain/palio-context.md` — a brief description of the event 

## API
- `docs/api/openapi.yaml` — committed API contract
- `docs/api/error-contract.md` — machine-readable business error codes and semantics, with HTTP status mapping for each.

## Testing
- `docs/testing/test-strategy.md` — test layers and depth expectations
- `docs/testing/critical-e2e-flows.md` — the small must-pass E2E suite
- `docs/testing/fixtures.md` — fixtures and seeded data

## Operations
- `docs/ops/local-dev.md` — setup and daily commands
- `docs/ops/deploy.md` — deploy process
- `docs/ops/runbook.md` — operational troubleshooting / recovery

## Repo process and governance
- `docs/qna/README.md` — clarification index and implementation notes

## Reading strategy
- Read the smallest relevant subset for the task.
- Prefer baseline docs and ADRs over scattered comments.
- If docs conflict, flag the conflict instead of guessing.
