# Critical E2E Flows

This file is the task-by-task planning record for active browser end-to-end coverage.
Update it during planning whenever a task adds, removes, narrows, or expands Playwright scope.

The broader target critical-flow philosophy still lives in `docs/testing/test-strategy.md`.
This file records what the repo currently expects the browser suite to prove right now.

## Current active browser coverage

### Same-origin shell smoke

Purpose:
- prove the local same-origin stack boots through Nginx
- prove the browser can reach the routed SPA shells without bypassing the proxy

Assertions:
- `/` resolves to the public shell
- `/admin` renders the admin scaffold
- `/public` renders the public scaffold
- `/maxi` renders the maxi-screen scaffold

Non-goals:
- no result-entry workflows
- no leaderboard or scoring verification
- no realtime conflict behavior
- no broad UI coverage beyond route reachability and shell rendering
