# Documentation impact matrix

Use this during planning for every non-trivial change.

## `docs/api/error-contract.md`
Update when a change affects:
- machine-readable error codes
- error envelope shape
- validation error semantics
- concurrency/conflict error behavior
- authorization/authentication error behavior exposed to clients

## `docs/domain/business-rules.md`
Update when a change affects:
- domain invariants
- scoring rules
- standings rules
- Jolly rules
- lifecycle/state-transition rules
- official result semantics
- authorization/business-policy semantics

## `docs/testing/test-strategy.md`
Update when a change affects:
- required test layers
- quality gates
- test tooling/policies
- what kinds of changes require unit, integration, realtime, or E2E tests

## `docs/testing/critical-e2e-flows.md`
Update when a change affects:
- must-pass end-to-end flows
- critical user journeys
- high-risk regression scenarios
- release-blocking acceptance flows

## `docs/testing/fixtures.md`
Update when a change affects:
- seed data
- fixture structure
- canonical test datasets
- assumptions required by tests
- reusable scenario setup

## `docs/ops/local-dev.md`
Update when a change affects:
- local setup steps
- required services/tools
- developer commands
- local environment variables
- bootstrap or migration steps needed for development

## `docs/ops/deploy.md`
Update when a change affects:
- deployment steps
- build/release procedure
- migration/deploy order
- infrastructure assumptions
- rollback or release sequencing

## `docs/ops/runbook.md`
Update when a change affects:
- operational diagnostics
- incident handling
- manual recovery procedures
- admin/operator troubleshooting steps
- production verification steps
