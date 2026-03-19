---
id: TASK-16.1
title: Implement api season identity and four-rioni management
status: To Do
assignee: []
created_date: '2026-03-16 16:40'
updated_date: '2026-03-18 21:09'
labels:
  - api
  - season-setup
milestone: m-1
dependencies:
  - TASK-13
references:
  - apps/api/src/palio/modules/season_setup/
  - apps/api/src/palio/modules/season_setup/facade.py
  - apps/api/src/palio/shared/module_facade.py
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

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Architecture constraint: replace the current metadata-only `season_setup` facade placeholder with a real typed public contract as part of this task.

Wiring constraint: keep UnitOfWork creation outside the season-setup services/orchestrators and inject the UnitOfWork they use instead of adding a `UnitOfWorkFactory`.
<!-- SECTION:NOTES:END -->
