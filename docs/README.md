# Documentation

Read this file first when you need repo context. 

## Reading strategy
- Read the smallest relevant subset for the change.
- Prefer baseline docs and ADRs over scattered comments.
- If docs conflict, **flag** the conflict instead of guessing.
- Prefer already-resolved clarifications in `docs/qna/`.

## Index
### Product
- `docs/product/prd.md` — product scope, goals, non-goals
- `docs/product/functional-requirements.md` — required behavior and critical flows
- `docs/product/acceptance-scenarios.md` — acceptance criteria and Given/When/Then examples
- `docs/product/roadmap.md` — maintained milestone summary for the active documentation set

### Architecture and decisions
- `docs/architecture/architecture.md` — baseline system shape, boundaries, ownership, delivery conventions
- `docs/architecture/adr/` — architectural decision records

### Domain and data
- `docs/domain/er-schema.md` — entities and relationships
- `docs/domain/business-rules.md` — invariants and business semantics.
- `docs/domain/game-catalog.md` — seeded game fields / configuration catalog
- `docs/domain/palio.md` — a brief description of the event
- `docs/domain/palio-rules.md` — official source rules from the real-world event

### API
- `docs/api/openapi.yaml` — committed API contract
- `docs/api/error-contract.md` — machine-readable business error codes and semantics, with HTTP status mapping for each.

### Testing
- `docs/testing/test-strategy.md` — test layers and depth expectations
- `docs/testing/critical-e2e-flows.md` — the small must-pass E2E suite
- `docs/testing/fixtures.md` — fixtures and seeded data

### Operations
- `docs/ops/local-dev.md` — setup and daily commands
- `docs/ops/deploy.md` — deploy process
- `docs/ops/runbook.md` — operational troubleshooting / recovery

### Repo process and governance
- `docs/engineering/documentation-impact-matrix.md` — required doc-impact check for non-trivial changes

### Doubts and already addressed questions
- `docs/qna/README.md` — clarification index and implementation notes

### App roots
- `apps/README.md` — runnable app-root overview
- `apps/api/README.md` — api scaffold details and commands
- `apps/web/README.md` — frontend scaffold details and commands

### Examples and source material
- `docs/examples/README.md` — examples showing the intended structure and usage of maintained doc types
- `docs/_raw/README.md` — original long-form source material kept outside the maintained active doc surface

### Maintenance
- **Flag** when there is duplication or redundancy in or across documents
- **Flag** when something is not clear or may be summarized
- **Flag** when there are contradictions in or across documents
- **Flag** when a document is too long or hard to read