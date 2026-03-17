---
id: TASK-18.1
title: Implement api immutability and deletion guards for setup config
status: To Do
assignee: []
created_date: '2026-03-16 16:40'
labels:
  - api
  - season-setup
  - immutability
milestone: m-1
dependencies:
  - TASK-17.1
references:
  - apps/api/src/palio/modules/season_setup/
  - apps/api/src/palio/modules/results/
documentation:
  - docs/qna/data/result model and invariants.md
  - docs/domain/game-catalog.md
  - docs/qna/product/season setup.md
  - docs/ui/pages/admin/season-setup.md
  - docs/ui/pages/admin/game-editor.md
parent_task_id: TASK-18
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Build the api slice of TASK-18 so result-affecting setup cannot be edited or deleted once official result data exists, with explicit lock-state checks and structured error reporting.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Season-setup services reject edits and deletes to games and other result-affecting configuration once official result data exists, following the documented immutability rules.
- [ ] #2 The api exposes enough lock-state information for the admin UI to explain why a field or action is disabled before submit.
- [ ] #3 The task adds api unit and integration coverage, plus any minimal schema, contract, and documentation updates needed to detect official-result presence in the same change.
<!-- AC:END -->
