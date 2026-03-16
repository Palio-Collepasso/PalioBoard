---
id: TASK-15
title: Add the superadmin-only user provisioning workflow
status: To Do
assignee: []
created_date: '2026-03-16 16:33'
updated_date: '2026-03-16 16:39'
labels:
  - parent-task
  - auth
  - user-management
milestone: m-1
dependencies:
  - TASK-13
  - TASK-14
references:
  - apps/api/src/palio/modules/identity/
  - apps/api/src/palio/modules/users/
  - apps/web/src/app/
documentation:
  - docs/ui/pages/admin/user-management.md
  - docs/qna/architecture/authorization.md
  - docs/architecture/adr/ADR-0006-identity-and-authorization.md
  - docs/architecture/architecture.md
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Deliver the minimal v1 user-management slice so a superadmin can create a user with an email, password, and seeded role, while the backend keeps Supabase identity and the linked application user in sync.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Superadmins can create a user with email, password, and one seeded role from `/admin/settings/users`, and users without the required capability receive backend forbidden errors even if they reach the surface.
- [ ] #2 The backend provisions the Supabase identity and linked application user in one orchestrated workflow with best-effort compensation and clear operator-facing failure reporting when a cross-system step fails.
- [ ] #3 The task adds backend and UI flow coverage for successful provisioning and forbidden access, and updates the affected docs and committed API contracts.
<!-- AC:END -->
