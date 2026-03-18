---
id: TASK-18.2
title: Implement frontend lock-state UX for immutable setup config
status: To Do
assignee: []
created_date: '2026-03-16 16:41'
labels:
  - frontend
  - season-setup
  - immutability
milestone: m-1
dependencies:
  - TASK-17.2
  - TASK-18.1
references:
  - apps/web/src/app/
documentation:
  - docs/ui/pages/admin/season-setup.md
  - docs/ui/pages/admin/game-editor.md
  - docs/qna/data/result model and invariants.md
  - docs/domain/game-catalog.md
parent_task_id: TASK-18
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Build the frontend slice of TASK-18 so season and game setup screens explain immutable state clearly and block destructive actions once official-result-dependent configuration is locked.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Season and game setup screens surface api lock-state reasons inline before submit and disable destructive or invalid actions that would break official history.
- [ ] #2 The client consumes api lock-state information instead of inferring immutability rules locally, and handles forbidden or conflict responses clearly in the UI.
- [ ] #3 The task adds frontend integration coverage and updates any affected UI documentation or local setup notes for immutable setup behavior.
<!-- AC:END -->
