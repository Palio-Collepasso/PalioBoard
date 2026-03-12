---
id: m-6
title: "Trust and exception workflows"
---
## Description

Milestone: Trust and exception workflows

Depends on: m-2 Trusted ranking result backbone, m-3 Live ranking operations and collaboration safety, m-4 Advanced standings rules: Jolly, Prepalio, Giocasport, adjustments, and m-5 1v1 tournament workflow.

Objective: complete the workflows that protect operational trust during the appeal window and after corrections, including under examination, post-completion edits, admin review, and audit visibility.

Scope:
- `completed -> pending_admin_review` flow on judge edits.
- Admin review and resolution back to `completed`.
- Marking and resolving `under_examination`.
- Projection rules where `pending_admin_review` still counts and `under_examination` does not.
- Audit browsing and read models for operational review.
- Structured reason capture where required.
- Critical E2E flow for post-completion edit and review behavior.

Exit criteria:
- Editing a completed result creates a new authoritative write, records audit, and moves the game to `pending_admin_review`.
- `under_examination` keeps the result visible publicly while excluding it from standings.
- Admins can resolve review and examination flows correctly.
- Audit history is sufficient to understand what changed, by whom, and why.
- The exception workflows pass their dedicated integration and E2E tests.
