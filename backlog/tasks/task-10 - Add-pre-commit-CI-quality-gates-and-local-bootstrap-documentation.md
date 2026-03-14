---
id: TASK-10
title: 'Add pre-commit, CI quality gates, and local bootstrap documentation'
status: To Do
assignee:
  - '@codex'
created_date: '2026-03-12 01:37'
updated_date: '2026-03-14 19:05'
labels: []
milestone: m-0
dependencies:
  - TASK-1
  - TASK-6
  - TASK-7
  - TASK-8
  - TASK-9
documentation:
  - README.md
  - docs/testing/test-strategy.md
  - docs/qna/architecture/deployment and operations.md
parent_task_id: M-0
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Close out M1 by wiring the agreed quality gates into pre-commit and GitHub Actions, then document the exact local bootstrap and verification commands needed to satisfy the milestone exit criteria.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Pre-commit and CI enforce the baseline checks for formatting, linting, typing, tests, build validation, OpenAPI workflow, and architectural boundary rules.
- [ ] #2 `README.md` and a dedicated local-development document describe the exact commands to boot, verify, and troubleshoot the M1 stack.
- [ ] #3 The planning docs no longer disagree about what M1 includes once the bootstrap workflow and command surface are in place.
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Future verification check: the backend Postgres integration harness should no longer rely on hardcoded container image/default bootstrap values in `apps/api/tests/support/postgres.py`. As part of the M1 quality-gate/bootstrap pass, verify the tests reuse the infra-owned Docker image/service configuration introduced by the infra tasks instead of carrying separate inline defaults.
<!-- SECTION:NOTES:END -->
