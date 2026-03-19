---
id: TASK-17.1
title: Implement api competition and game configuration
status: To Do
assignee: []
created_date: '2026-03-16 16:40'
updated_date: '2026-03-18 21:09'
labels:
  - api
  - season-setup
  - game-config
milestone: m-1
dependencies:
  - TASK-16.1
references:
  - apps/api/src/palio/modules/season_setup/
  - apps/api/src/palio/modules/season_setup/facade.py
documentation:
  - docs/domain/game-catalog.md
  - docs/qna/product/season setup.md
  - 'docs/qna/product/scoring, jolly, and ties.md'
  - docs/ui/pages/admin/game-editor.md
  - docs/architecture/architecture.md
parent_task_id: TASK-17
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Build the api slice of TASK-17 so admins can create and manage competitions and games for the active season, choose supported formats, select seeded fields, and configure per-game points tables.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Season-setup APIs allow creating, editing, listing, and deleting competitions and games using only the allowed competition contexts and normalized formats defined in the product and domain docs.
- [ ] #2 Game configuration persistence and validation support seeded field-catalog selection and per-game points-table configuration with the documented defaults and structured validation errors.
- [ ] #3 The task adds api unit and integration coverage, updates affected docs, and updates committed API contracts for competition and game configuration.
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implementation note: extend the typed `season_setup` public facade created by TASK-16.1 instead of growing the current metadata-only alias or bypassing the module boundary.

Keep transaction ownership outside repositories and helpers; this slice should consume the injected UnitOfWork rather than introducing a `UnitOfWorkFactory`.
<!-- SECTION:NOTES:END -->
