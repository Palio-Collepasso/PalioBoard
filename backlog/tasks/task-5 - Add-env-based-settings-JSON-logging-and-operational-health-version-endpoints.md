---
id: TASK-5
title: Add env-based settings, JSON logging, and operational health/version endpoints
status: To Do
assignee:
  - '@codex'
created_date: '2026-03-12 01:37'
labels: []
milestone: m-0
dependencies:
  - TASK-2
documentation:
  - 'docs/architecture/architecture.md'
  - 'docs/qna/architecture/deployment and operations.md'
parent_task_id: M-0
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add the runtime settings and operational baseline expected by the architecture, including typed env-based configuration, structured logging, correlation-id propagation, and the minimal health/version endpoints.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Backend runtime configuration is driven by typed environment settings rather than hard-coded values.
- [ ] #2 HTTP requests emit structured JSON logs that include a request or correlation identifier suitable for local debugging and production operations.
- [ ] #3 The backend exposes liveness, readiness, and build/version endpoints that can be consumed by Compose, Nginx, and CI smoke checks.
<!-- AC:END -->
