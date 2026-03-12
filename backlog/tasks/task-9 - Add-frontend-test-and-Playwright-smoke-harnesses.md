---
id: TASK-9
title: Add frontend test and Playwright smoke harnesses
status: To Do
assignee:
  - '@codex'
created_date: '2026-03-12 01:37'
labels: []
milestone: m-0
dependencies:
  - TASK-3
  - TASK-6
  - TASK-7
documentation:
  - 'docs/testing/test-strategy.md'
  - 'docs/qna/architecture/deployment and operations.md'
parent_task_id: M-0
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Set up the frontend behavior-test baseline and a minimal Playwright smoke path so M1 proves the stack can boot through the browser without expanding into broad UI coverage too early.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The Angular app has a repeatable frontend test entrypoint for component or feature-level behavior checks.
- [ ] #2 Playwright is configured with a minimal smoke scenario that proves the browser can reach the routed shells through the local stack.
- [ ] #3 The smoke coverage stays intentionally small and aligned with the documented critical-flow philosophy.
<!-- AC:END -->
