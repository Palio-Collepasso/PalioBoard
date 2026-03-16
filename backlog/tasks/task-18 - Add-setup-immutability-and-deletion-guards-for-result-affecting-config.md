---
id: TASK-18
title: Add setup immutability and deletion guards for result-affecting config
status: To Do
assignee: []
created_date: '2026-03-16 16:34'
updated_date: '2026-03-16 16:39'
labels:
  - parent-task
  - season-setup
  - immutability
milestone: m-1
dependencies:
  - TASK-17
references:
  - apps/api/src/palio/modules/season_setup/
  - apps/api/src/palio/modules/results/
  - apps/web/src/app/
documentation:
  - docs/qna/data/result model and invariants.md
  - docs/domain/game-catalog.md
  - docs/qna/product/season setup.md
  - docs/ui/pages/admin/season-setup.md
  - docs/ui/pages/admin/game-editor.md
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Harden the season-setup workflows so result-affecting configuration cannot be changed or deleted once official result data exists, and expose those lock reasons clearly in both the API and the admin UI.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Setup services reject edits and deletes to games and other result-affecting configuration once official result data exists, following the documented rule that game properties and relationships become immutable after official data appears.
- [ ] #2 The admin season and game setup UI surfaces lock reasons inline before submit and blocks destructive actions that would break official history.
- [ ] #3 The task adds unit and integration coverage for unlocked and locked paths, and delivers any minimal schema, contract, and documentation updates needed to detect official-result presence in the same change.
<!-- AC:END -->
