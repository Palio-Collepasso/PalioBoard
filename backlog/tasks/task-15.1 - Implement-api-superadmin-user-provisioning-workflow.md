---
id: TASK-15.1
title: Implement api superadmin user provisioning workflow
status: To Do
assignee: []
created_date: '2026-03-16 16:40'
updated_date: '2026-03-18 21:09'
labels:
  - api
  - auth
  - user-management
milestone: m-1
dependencies:
  - TASK-13
references:
  - apps/api/src/palio/modules/identity/
  - apps/api/src/palio/modules/users/
  - apps/api/src/palio/modules/identity/facade.py
  - apps/api/src/palio/modules/users/facade.py
documentation:
  - docs/ui/pages/admin/user-management.md
  - docs/qna/architecture/authorization.md
  - docs/architecture/adr/ADR-0006-identity-and-authorization.md
  - docs/architecture/architecture.md
parent_task_id: TASK-15
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Build the api slice of TASK-15 so the system can provision a Supabase identity, create the linked application user, assign one seeded role, and enforce the superadmin-only policy for v1 user management.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Admin APIs expose the minimal user-management commands and reads needed for `/admin/settings/users`, and only callers with the superadmin capability can use provisioning actions.
- [ ] #2 Provisioning creates the Supabase identity and linked application user in one orchestrated workflow with best-effort compensation and structured failure reporting when one step fails.
- [ ] #3 The task adds api unit and integration coverage, updates affected docs, and updates committed API contracts for the user-management surface.
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implementation note: build on the typed `identity` and `users` facade contracts from TASK-13 rather than adding task-local placeholder interfaces or direct internal module imports.

Keep UnitOfWork ownership outside the provisioning workflow classes; use the injected UnitOfWork and do not add a factory abstraction.
<!-- SECTION:NOTES:END -->
