---
id: TASK-6
title: Wire Docker Compose and Nginx into a same-origin local stack
status: To Do
assignee:
  - '@codex'
created_date: '2026-03-12 01:37'
labels: []
milestone: m-0
dependencies:
  - TASK-3
  - TASK-4
  - TASK-5
documentation:
  - 'docs/architecture/architecture.md'
  - 'docs/qna/architecture/deployment and operations.md'
parent_task_id: M-0
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add the local infrastructure needed to boot the stack behind one origin, including Compose services and Nginx routing for SPA paths, `/api`, and later `/realtime`.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Docker Compose can boot the baseline local stack with PostgreSQL and the application-facing containers needed for M1 verification.
- [ ] #2 Nginx serves the SPA and proxies backend requests through one origin using the documented route split.
- [ ] #3 The backend and frontend skeletons are both reachable through the same-origin proxy in a local smoke run.
<!-- AC:END -->
