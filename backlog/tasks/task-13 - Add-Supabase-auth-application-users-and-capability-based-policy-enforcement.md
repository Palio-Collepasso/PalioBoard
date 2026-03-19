---
id: TASK-13
title: 'Add Supabase auth, application users, and capability-based policy enforcement'
status: To Do
assignee: []
created_date: '2026-03-16 16:33'
updated_date: '2026-03-18 21:09'
labels:
  - api
  - auth
milestone: m-1
dependencies:
  - TASK-20
references:
  - apps/api/src/palio/modules/identity/
  - apps/api/src/palio/modules/authorization/
  - apps/api/src/palio/modules/users/
  - apps/api/src/palio/modules/identity/facade.py
  - apps/api/src/palio/modules/authorization/facade.py
  - apps/api/src/palio/modules/users/facade.py
  - apps/api/src/palio/shared/module_facade.py
documentation:
  - docs/architecture/adr/ADR-0006-identity-and-authorization.md
  - docs/qna/architecture/authorization.md
  - docs/qna/architecture/system boundaries.md
  - docs/architecture/architecture.md
  - docs/qna/data/schema and migrations.md
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Introduce the api identity and authorization foundation for m-1 so protected APIs resolve real application users, seeded roles/capabilities, and api-enforced policy checks before any setup workflows depend on them.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Protected api entry points validate Supabase bearer tokens through an explicit identity-provider adapter and resolve a linked application user for request and audit context.
- [ ] #2 The application schema and seed workflow provide a code-defined capability vocabulary, roles, role-capability mappings, user-role assignments, and the default Superadmin/Admin/Judge bundles plus a documented bootstrap path for the first superadmin.
- [ ] #3 Capability-based policy helpers return structured unauthorized and forbidden errors, and the task updates the affected tests, docs, and committed API contracts.
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Architecture constraint: replace the current metadata-only facade placeholders with real typed public contracts for `identity`, `authorization`, and `users` as part of this task.

Wiring constraint: application services and orchestrators should receive the UnitOfWork from outer composition/injection and must not introduce a `UnitOfWorkFactory` layer or create their own sessions.
<!-- SECTION:NOTES:END -->
