---
id: TASK-1
title: Bootstrap the monorepo layout and top-level make workflow
status: To Do
assignee:
  - '@codex'
created_date: '2026-03-12 01:37'
updated_date: '2026-03-12 01:46'
labels: []
milestone: m-0
dependencies: []
documentation:
  - docs/architecture/architecture.md
  - docs/qna/architecture/module boundaries.md
  - docs/qna/architecture/deployment and operations.md
parent_task_id: M-0
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create the initial repository skeleton for the documented monorepo and establish `make` as the stable top-level command surface for local development and CI.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Root layout matches the approved monorepo structure for `backend/`, `web/`, `infra/`, `docs/`, `tools/`, and `.github/workflows/`.
- [ ] #2 A top-level `Makefile` exposes the baseline developer entrypoints needed by later M1 tasks without hiding implementation details inside ad hoc scripts.
<!-- AC:END -->
