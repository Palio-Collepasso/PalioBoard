---
id: TASK-17.2
title: Implement frontend competition and game configuration UI
status: To Do
assignee: []
created_date: '2026-03-16 16:41'
labels:
  - frontend
  - season-setup
  - game-config
milestone: m-1
dependencies:
  - TASK-16.2
  - TASK-17.1
references:
  - apps/web/src/app/
documentation:
  - docs/ui/pages/admin/game-editor.md
  - docs/domain/game-catalog.md
  - docs/qna/product/season setup.md
  - 'docs/qna/product/scoring, jolly, and ties.md'
parent_task_id: TASK-17
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Build the frontend slice of TASK-17 so admins can create and edit competitions and games, choose supported formats, select seeded result fields, and manage per-game points tables from the documented admin flow.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The admin UI implements the documented game create and edit experience with the allowed competition and format choices, seeded field selection, and points-table editing surfaces.
- [ ] #2 The client reads and writes backend-owned competition and game configuration through the authenticated admin session and surfaces validation or forbidden errors without re-owning business rules.
- [ ] #3 The task adds frontend integration coverage and updates any affected UI documentation or local setup notes for game configuration.
<!-- AC:END -->
