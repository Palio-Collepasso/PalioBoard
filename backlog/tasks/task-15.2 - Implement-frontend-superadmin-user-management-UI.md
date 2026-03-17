---
id: TASK-15.2
title: Implement frontend superadmin user management UI
status: To Do
assignee: []
created_date: '2026-03-16 16:41'
labels:
  - frontend
  - auth
  - user-management
milestone: m-1
dependencies:
  - TASK-14
  - TASK-15.1
references:
  - apps/web/src/app/
documentation:
  - docs/ui/pages/admin/user-management.md
  - docs/qna/architecture/authorization.md
  - docs/architecture/architecture.md
parent_task_id: TASK-15
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Build the frontend slice of TASK-15 so a superadmin can view the user-management screen and create a user with email, password, and one seeded role from the documented admin flow.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The `/admin/settings/users` route implements the documented table, empty state, and create-user modal or drawer using the protected admin session flow.
- [ ] #2 The create-user flow submits email, password, and seeded role to the api, and handles success, validation, forbidden, and api failure states clearly in the UI.
- [ ] #3 The task adds frontend integration coverage and updates any affected UI documentation or local setup notes for the user-management flow.
<!-- AC:END -->
