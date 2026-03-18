# Documentation Guide

Read this file first when you need repository or product context.
Its job is to route you to the smallest authoritative doc set needed for the task.
Do not scan the whole `docs/` tree by default.

## Quick start
1. Start here.
2. Read the nearest `AGENTS.md` for repo or app-specific working rules.
3. Read only the smallest relevant subset of authoritative docs.
4. If documents conflict, flag the conflict instead of guessing.
5. Promote stable clarifications into authoritative docs instead of growing side notes.

## Source precedence
When multiple documents touch the same topic, use this order:

1. Code, migrations, and committed API contracts
2. `docs/architecture/architecture.md`
3. ADRs in `docs/architecture/adr/`
4. Authoritative product, domain, API, testing, and ops docs
5. `docs/qna/recently-resolved.md`
6. `docs/qna/open-questions.md`
7. `docs/ui/*` proposal UI docs
8. `docs/archive/*`

If two sources disagree, do not silently choose one. Flag the conflict.

## Read by task type
### Backend feature or bug fix
Read:
1. `docs/architecture/architecture.md`
2. `docs/architecture/module-map.md`
3. the smallest relevant subset of:
   - `docs/product/functional-requirements.md`
   - `docs/domain/business-rules.md`
   - `docs/domain/er-schema.md`
   - `docs/api/error-contract.md`
   - `docs/testing/test-strategy.md`

### API contract change
Read:
1. `docs/api/README.md`
2. `docs/api/error-contract.md` for semantic error behavior
3. affected paths in `docs/api/openapi.yaml` or regenerate it and review diff
4. relevant product and domain docs
5. `docs/testing/test-strategy.md`

### UI page or component implementation
Read:
1. `docs/architecture/architecture.md` for system boundaries
2. the smallest relevant subset of:
   - `docs/product/functional-requirements.md`
   - `docs/domain/business-rules.md`
   - `docs/domain/er-schema.md`
   - `docs/product/acceptance-scenarios.md`
   - `docs/api/README.md` / `docs/api/openapi.yaml` if the page depends on API data
3. only the relevant `docs/ui/*` proposal docs for the task

### Domain rule or standings logic change
Read:
1. `docs/architecture/architecture.md`
2. `docs/domain/business-rules.md`
3. `docs/domain/er-schema.md`
4. relevant product docs
5. `docs/testing/test-strategy.md`
6. `docs/testing/critical-e2e-flows.md` only if the change touches an automated critical browser flow

### Schema or migration change
Read:
1. `docs/architecture/architecture.md`
2. `docs/domain/er-schema.md`
3. `docs/domain/business-rules.md`
4. relevant ADRs
5. `docs/ops/deploy.md` if the migration affects rollout or rollback
6. `docs/testing/test-strategy.md`

### Operational or deployment change
Read:
1. relevant `docs/ops/*`
2. relevant ADRs
3. `docs/testing/test-strategy.md` if rollout, rollback, readiness, or recovery behavior changes
4. `docs/architecture/architecture.md` if the change affects a system boundary

### Product or acceptance clarification
Read:
1. `docs/product/prd.md`
2. `docs/product/functional-requirements.md`
3. `docs/product/acceptance-scenarios.md`
4. relevant domain docs if the clarification changes business semantics

## Authoritative document map
### Architecture
- `docs/architecture/architecture.md` — system boundary, module ownership, source of truth, invariants, lifecycle, write/read model, and logic placement rules
- `docs/architecture/module-map.md` — backend codemap by package/path, public facades, allowed dependencies, and code placement guidance
- `docs/architecture/runtime-flows.md` — critical high-risk flows and side effects
- `docs/architecture/adr/` — durable architecture decisions and consequences

### Product
- `docs/product/prd.md` — scope, goals, non-goals, and product framing
- `docs/product/functional-requirements.md` — supported behavior by feature surface
- `docs/product/acceptance-scenarios.md` — business-facing observable scenarios
- `docs/product/roadmap.md` — active milestone summary

### Domain and data
- `docs/domain/business-rules.md` — compact normative rule catalog and invariants
- `docs/domain/er-schema.md` — entities, relationships, and structural constraints
- `docs/domain/game-catalog.md` — seeded game setup catalog for v1
- `docs/domain/capabilities.yaml` — machine-readable capability vocabulary
- `docs/domain/palio-context.md` — compact event context and external-rule summary

### API
- `docs/api/README.md` — human guide to API ownership, generation, and stable surfaces
- `docs/api/openapi.yaml` — committed HTTP contract
- `docs/api/error-contract.md` — stable machine error codes and semantics currently emitted by the backend

### Testing
- `docs/testing/test-strategy.md` — required test depth by change type
- `docs/testing/critical-e2e-flows.md` — small automated browser flow shortlist
- `docs/testing/fixtures.md` — fixture and seeded-data reference

### Operations
- `docs/ops/local-dev.md` — setup and daily commands
- `docs/ops/deploy.md` — rollout and rollback procedure
- `docs/ops/runbook.md` — troubleshooting and recovery

### Engineering process
- `docs/engineering/code-review.md` — review expectations
- `docs/engineering/documentation-impact-matrix.md` — which docs must change when behavior changes

### UI
Treat `docs/ui/*` as proposal docs only. They are starting points for implementation, not product or business truth.

- `docs/ui/README.md` — how to navigate UI proposals and how to verify them
- `docs/ui/layouts/*` — shell-level proposal docs
- `docs/ui/pages/*` — route-level proposal docs
- `docs/ui/components/*` — shared UI building blocks
- `docs/ui/component_checklist.md` — compact v1 component inventory
- `docs/ui/design_tokens.json` — visual proposal tokens and semantic status mappings

### Temporary clarification layer
- `docs/qna/recently-resolved.md` — recent answers not yet promoted into authoritative docs
- `docs/qna/open-questions.md` — unresolved questions only

## Not part of the default reading path
Do not read these unless the task explicitly needs them:
- `docs/archive/*`
- archived Q&A
- examples used only as structure references
- templates used only for editing maintained docs
- old source material already summarized elsewhere
- `docs/ui/*` pages, shells, or components that are outside the current task scope

## Documentation maintenance rules
When a change affects behavior, architecture, schema, contracts, operations, or an implemented UI workflow:
1. update the authoritative document first
2. update `docs/ui/*` only as proposals or implementation starting points
3. update Q&A only if the answer is still temporary
4. archive outdated examples or migrated notes instead of keeping two active sources
5. flag any document that became contradictory, redundant, or too large to navigate quickly

## When to stop and ask or flag
Stop and flag the issue when:
- two authoritative docs disagree
- a required rule is missing
- a Q&A answer appears to override an authoritative doc
- a UI proposal implies behavior not supported by authoritative docs
- the task depends on behavior that is still open or ambiguous
- the relevant doc is too large or too scattered to navigate safely

## Track changes
Tracked changes in `docs/REDLINING.md`
