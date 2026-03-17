---
id: TASK-16.2
title: Implement frontend season setup UI for season identity and rioni
status: To Do
assignee: []
created_date: '2026-03-16 16:41'
labels:
  - frontend
  - season-setup
milestone: m-1
dependencies:
  - TASK-14
  - TASK-16.1
references:
  - apps/web/src/app/
documentation:
  - docs/ui/pages/admin/season-setup.md
  - docs/qna/product/season setup.md
  - docs/domain/palio.md
parent_task_id: TASK-16
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Build the frontend slice of TASK-16 so admins can manage the active season identity and the four rioni from the documented `/admin/season` experience.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The `/admin/season` route implements the documented season identity and rioni editing layout, including inline validation, row editing, and lock or rules summaries.
- [ ] #2 The page reads and writes api-owned season data through the authenticated admin session and surfaces forbidden or validation errors without duplicating business rules in the client.
- [ ] #3 The task adds frontend integration coverage and updates any affected UI documentation or local setup notes for the season-setup page.
<!-- AC:END -->
