---
id: TASK-3
title: 'Scaffold the Angular SPA with admin, public, and maxi shells'
status: To Do
assignee:
  - '@codex'
created_date: '2026-03-12 01:37'
updated_date: '2026-03-12 01:47'
labels: []
milestone: m-0
dependencies:
  - TASK-1
documentation:
  - docs/architecture/architecture.md
  - docs/qna/ui/frontend architecture.md
  - docs/qna/architecture/module boundaries.md
parent_task_id: M-0
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create the single Angular application with three lazy route shells and the agreed internal folder boundaries for `core`, `features`, and `shared` code.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The web app exposes separate lazy-loaded admin, public, and maxi-screen route areas in one SPA.
- [ ] #2 The frontend source layout reflects the documented `core`, `shell-*`, `features`, and `shared/*` boundaries.
- [ ] #3 A frontend boundary-check approach is defined so shells and shared code can be enforced by linting or import rules in CI.
<!-- AC:END -->
