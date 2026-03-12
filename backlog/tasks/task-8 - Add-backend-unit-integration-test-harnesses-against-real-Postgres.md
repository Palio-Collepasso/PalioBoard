---
id: TASK-8
title: Add backend unit and integration test harnesses against real Postgres
status: To Do
assignee:
  - '@codex'
created_date: '2026-03-12 01:37'
labels: []
milestone: m-0
dependencies:
  - TASK-2
  - TASK-4
  - TASK-5
documentation:
  - 'docs/testing/test-strategy.md'
  - 'docs/qna/architecture/deployment and operations.md'
parent_task_id: M-0
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create the backend testing baseline with fast unit-test entrypoints and Postgres-backed integration-test wiring that applies real migrations and exercises the application skeleton honestly.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Backend tests are split into unit and Postgres-backed integration layers in line with the documented strategy.
- [ ] #2 Integration tests run against a real local PostgreSQL database and apply real migrations rather than using SQLite substitutes.
- [ ] #3 The test harness includes at least one smoke path for app startup or health endpoints and one smoke path for migration/application bootstrapping.
<!-- AC:END -->
