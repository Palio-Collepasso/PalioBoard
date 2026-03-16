---
id: TASK-17.1
title: Implement backend competition and game configuration
status: To Do
assignee: []
created_date: '2026-03-16 16:40'
labels:
  - api
  - season-setup
  - game-config
milestone: m-1
dependencies:
  - TASK-16.1
references:
  - apps/api/src/palio/modules/season_setup/
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
Build the backend slice of TASK-17 so admins can create and manage competitions and games for the active season, choose supported formats, select seeded fields, and configure per-game points tables.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Season-setup APIs allow creating, editing, listing, and deleting competitions and games using only the allowed competition contexts and normalized formats defined in the product and domain docs.
- [ ] #2 Game configuration persistence and validation support seeded field-catalog selection and per-game points-table configuration with the documented defaults and structured validation errors.
- [ ] #3 The task adds backend unit and integration coverage, updates affected docs, and updates committed API contracts for competition and game configuration.
<!-- AC:END -->
