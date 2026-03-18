# Recently Resolved

## Purpose

This file is a temporary holding area for answers that were recently clarified and have already been promoted into authoritative docs.
Keep entries short.
Delete an entry once the promotion is old enough that agents no longer need the cross-reference.

## Promotion map

### RR-001 — Authentication approach for v1

**Resolution**
Use Supabase Auth for identity in v1. Python validates the bearer token and resolves the linked application user.
Provisioning is minimal email/password created by superadmin; there is no self-registration or in-app password reset flow in v1.

**Promoted to**
- `docs/architecture/architecture.md`
- `docs/product/functional-requirements.md`
- `docs/architecture/adr/ADR-0006-identity-and-authorization.md`

### RR-002 — Authorization model

**Resolution**
Authorization is capability-based. Roles are seeded bundles of capabilities, and critical checks happen in backend application workflows.

**Promoted to**
- `docs/architecture/architecture.md`
- `docs/product/functional-requirements.md`
- `docs/domain/business-rules.md`
- `docs/architecture/adr/ADR-0006-identity-and-authorization.md`

### RR-003 — Backend architecture style

**Resolution**
Use a modular monolith with strict module ownership, public facades for cross-module calls, synchronous transactional writes, and derived read models.

**Promoted to**
- `docs/architecture/architecture.md`
- `docs/architecture/module-map.md`
- `docs/architecture/adr/ADR-0002-backend-style-modular-monolith.md`
- `docs/architecture/adr/ADR-0003-synchronous-write-model-and-projections.md`

### RR-004 — Official result model

**Resolution**
Canonical official per-team result truth lives in `game_entries` and `game_entry_fields` for every game format, including tournaments.
There is no separate official ranking override table in v1.

**Promoted to**
- `docs/architecture/architecture.md`
- `docs/domain/er-schema.md`
- `docs/product/functional-requirements.md`
- `docs/architecture/adr/ADR-0004-official-result-model.md`

### RR-005 — Live ranking entry model

**Resolution**
Ranking live entry is memory-first, provisional, revisioned, and recoverable through persisted snapshots.
It never becomes official truth until materialized into canonical result tables.
Tournament games bypass this subsystem in v1.

**Promoted to**
- `docs/architecture/architecture.md`
- `docs/architecture/runtime-flows.md`
- `docs/product/functional-requirements.md`
- `docs/architecture/adr/ADR-0005-live-collaboration-model.md`

### RR-006 — Leaderboard effects of special states

**Resolution**
`pending_admin_review` still counts using the latest official result.
`under_examination` remains visible but is excluded from leaderboard calculations.

**Promoted to**
- `docs/architecture/architecture.md`
- `docs/domain/business-rules.md`
- `docs/product/functional-requirements.md`
- `docs/architecture/runtime-flows.md`

### RR-007 — Deployment and system boundary direction

**Resolution**
Angular is the UI, FastAPI owns business APIs and orchestration, PostgreSQL stores official truth and projections, Supabase Auth provides identity, and Nginx fronts same-origin delivery.
The design must remain portable to plain Postgres later.

**Promoted to**
- `docs/architecture/architecture.md`
- `docs/architecture/adr/ADR-0001-system-boundary-and-core-stack.md`
- `docs/architecture/adr/ADR-0008-deployment-and-operational-model.md`

## Cleanup rule

When an item here no longer helps navigation, remove it.
This file should stay small and recent.
