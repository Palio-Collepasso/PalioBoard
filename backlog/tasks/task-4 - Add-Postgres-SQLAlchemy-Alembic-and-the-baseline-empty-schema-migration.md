---
id: TASK-4
title: 'Add Postgres, SQLAlchemy, Alembic, and the baseline empty-schema migration'
status: To Do
assignee:
  - '@codex'
created_date: '2026-03-12 01:37'
updated_date: '2026-03-12 01:47'
labels: []
milestone: m-0
dependencies:
  - TASK-2
documentation:
  - docs/architecture/architecture.md
  - docs/qna/data/schema and migrations.md
parent_task_id: M-0
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Establish the backend database baseline with SQLAlchemy wiring, Alembic configuration, and an initial empty-schema migration that can be applied repeatably in local and CI environments.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The backend can connect to PostgreSQL through the approved persistence baseline and migration configuration.
- [ ] #2 An initial Alembic revision creates the empty application schema successfully and becomes the starting point for later domain tables.
- [ ] #3 The migration workflow keeps schema evolution separate from normal application startup.
<!-- AC:END -->
