---
id: TASK-16
title: Add season identity and four-rioni management
status: To Do
assignee: []
created_date: '2026-03-16 16:33'
updated_date: '2026-03-16 16:39'
labels:
  - parent-task
  - season-setup
milestone: m-1
dependencies:
  - TASK-13
  - TASK-14
references:
  - apps/api/src/palio/modules/season_setup/
  - apps/web/src/app/
documentation:
  - docs/qna/product/season setup.md
  - docs/ui/pages/admin/season-setup.md
  - docs/domain/palio.md
  - docs/architecture/architecture.md
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Deliver the first season-setup slice for m-1 so admins can manage the active season identity and the four default rioni through api-owned state and the documented `/admin/season` page.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Admin-only api APIs and persistence support one active season plus the four default rioni with prefilled defaults rather than arbitrary team counts.
- [ ] #2 The `/admin/season` page implements the documented season identity and rioni editing flow, keeps the rioni table on the same page, and surfaces validation or lock summaries inline.
- [ ] #3 The task adds api and frontend coverage for happy-path saves and forbidden access, and updates the affected docs and committed API contracts.
<!-- AC:END -->
