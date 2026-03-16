---
id: TASK-14
title: Add login route and protected admin session handling
status: To Do
assignee: []
created_date: '2026-03-16 16:33'
updated_date: '2026-03-16 16:38'
labels:
  - frontend
  - auth
milestone: m-1
dependencies:
  - TASK-13
references:
  - apps/web/src/app/
documentation:
  - docs/ui/pages/admin/login.md
  - docs/qna/ui/frontend architecture.md
  - docs/qna/architecture/system boundaries.md
  - docs/architecture/architecture.md
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Give admin, judge, and superadmin users a real authenticated entry point so the private admin shell and API clients run behind the documented Supabase-backed session flow instead of placeholder access.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The `/login` route implements the documented email/password sign-in flow, handles loading and error states, and redirects authenticated users into the admin shell while redirecting already-authenticated users away from the login page.
- [ ] #2 Private admin routes and admin API clients use the authenticated bearer token and session state without leaking auth assumptions into the public or maxi-screen shells.
- [ ] #3 The task adds frontend integration coverage for sign-in and protected-route behavior, and updates any affected local-auth or bootstrap documentation.
<!-- AC:END -->
