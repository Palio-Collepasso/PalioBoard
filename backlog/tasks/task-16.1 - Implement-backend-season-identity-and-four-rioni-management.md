---
id: TASK-16.1
title: Implement api season identity and four-rioni management
status: To Do
assignee: []
created_date: '2026-03-16 16:40'
labels:
  - api
  - season-setup
milestone: m-1
dependencies:
  - TASK-13
references:
  - apps/api/src/palio/modules/season_setup/
documentation:
  - docs/qna/product/season setup.md
  - docs/ui/pages/admin/season-setup.md
  - docs/domain/palio.md
  - docs/architecture/architecture.md
parent_task_id: TASK-16
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Build the api slice of TASK-16 so admins can manage one active season and the four default rioni through api-owned season-setup APIs and persistence.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Season-setup services and persistence support one active season plus exactly four rioni with prefilled defaults, validation, and admin-only authorization.
- [ ] #2 The api exposes the commands and reads needed by `/admin/season`, including structured forbidden and validation errors for invalid or unauthorized changes.
- [ ] #3 The task adds api unit and integration coverage, updates affected docs, and updates committed API contracts for the season identity and rioni surface.
<!-- AC:END -->
