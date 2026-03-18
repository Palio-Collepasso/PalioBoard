# Code Review Guide

## Purpose
Use this file as the review checklist for changes that can break correctness, contracts, operations, or documentation trust.

## Document boundary
This file owns **review focus**.
It does not own full test policy, architecture rules, or deployment procedure.
- Test depth lives in `docs/testing/test-strategy.md`.
- Architecture ownership lives in `docs/architecture/*`.
- Deployment steps live in `docs/ops/deploy.md`.

## General review checks
[ ] scope matches the intended change
[ ] module/layer ownership is preserved
[ ] docs and committed contracts changed with behavior
[ ] backend Python conventions and related docstrings were followed/updated
[ ] tests match the risk
[ ] no unrelated refactor is mixed into a correctness-sensitive change

## Common reviewer commands
- repo gates: `make verify`
- backend unit tests: `make test-api-unit`
- backend integration tests: `make test-api-integration`
- web tests: `make test-web`
- browser E2E: `make test-e2e`

See `docs/ops/local-dev.md` for fuller command guidance

## Critical-path review checklist
### Official results and canonical materialization
Verify:
- canonical per-team result truth still lives in `game_entries` and `game_entry_fields`
- placement, Jolly, and configured fields are written consistently
- `completed`, `pending_admin_review`, and `under_examination` still have the documented semantics
- authoritative result changes still produce audit rows and projection updates together

### Standings, scoring, Prepalio, and projections
Verify:
- standings are recomputed only from authoritative truth plus adjustments
- Jolly, Prepalio, and Giocasport behavior still follow business rules
- projection tables are treated as derived state, not source of truth
- read paths do not accidentally move business logic into SQL-only shortcuts

### Tournament progression
Verify:
- semifinal/final progression remains deterministic
- canonical official team results stay synchronized with match outcomes
- leaderboard impact still waits for the documented completion point

### Live ranking entry and collaboration
Verify:
- draft state never becomes official truth by accident
- stale writes and conflicts are rejected clearly
- reconnect and recovery behavior is still safe
- draft materialization and cleanup still happen at the correct lifecycle boundaries

### Authorization and identity
Verify:
- Python remains the authorization source of truth
- capability checks still protect the right actions
- `401` vs `403` semantics still match the API contract
- user provisioning or linkage changes still preserve auditability and explicit failure handling

### Migrations and schema changes
Verify:
- the schema change matches `docs/domain/er-schema.md`
- migrations are operationally safe and documented in `docs/ops/deploy.md` when needed
- DB-backed behavior has integration coverage
- data fixes or backfills are not hidden inside request-time logic

### Infra, CI, and workflows
Verify:
- release steps did not change accidentally
- protected-branch or contract-generation checks were not weakened
- secrets handling and environment assumptions stay explicit
- runbook or deploy docs were updated when operator behavior changed
