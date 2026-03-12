---
id: TASK-7
title: Add the OpenAPI export and frontend type-generation workflow
status: To Do
assignee:
  - '@codex'
created_date: '2026-03-12 01:37'
labels: []
milestone: m-0
dependencies:
  - TASK-2
  - TASK-3
documentation:
  - 'docs/qna/architecture/api and contracts.md'
  - 'docs/architecture/adr/ADR-0007-api-and-contract-strategy.md'
parent_task_id: M-0
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Set up the contract workflow where FastAPI owns the OpenAPI artifact, the spec is committed in the repo, and frontend TypeScript types are generated from that committed file instead of from a running backend.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A repeatable command exports the backend OpenAPI spec as a committed repo artifact.
- [ ] #2 Frontend TypeScript types can be regenerated from the committed OpenAPI file without requiring a running backend.
- [ ] #3 The workflow makes it clear that the spec is committed while generated TS types are not.
<!-- AC:END -->
