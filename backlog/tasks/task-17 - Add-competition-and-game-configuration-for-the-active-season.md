---
id: TASK-17
title: Add competition and game configuration for the active season
status: To Do
assignee: []
created_date: '2026-03-16 16:33'
updated_date: '2026-03-16 16:39'
labels:
  - parent-task
  - season-setup
  - game-config
milestone: m-1
dependencies:
  - TASK-16
references:
  - apps/api/src/palio/modules/season_setup/
  - apps/web/src/app/
documentation:
  - docs/domain/game-catalog.md
  - docs/qna/product/season setup.md
  - 'docs/qna/product/scoring, jolly, and ties.md'
  - docs/ui/pages/admin/game-editor.md
  - docs/architecture/architecture.md
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Extend season setup so admins can define the season competitions and games, choose the supported formats, select seeded result fields, and configure per-game points tables from the documented admin flow.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Admin-only APIs allow creating, editing, listing, and removing season competitions and games using only the allowed competition contexts and normalized formats from the product and domain docs.
- [ ] #2 Game configuration supports seeded field-catalog selection and per-game points-table configuration with documented defaults and validation surfaced in the editor UI.
- [ ] #3 The task adds api and frontend coverage for create/edit validation and the documented admin flow, and updates the affected docs and committed API contracts.
<!-- AC:END -->
