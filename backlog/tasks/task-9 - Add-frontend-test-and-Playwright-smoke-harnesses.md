---
id: TASK-9
title: Add frontend test and Playwright smoke harnesses
status: Done
assignee:
  - '@codex'
created_date: '2026-03-12 01:37'
updated_date: '2026-03-15 12:29'
labels: []
milestone: m-0
dependencies:
  - TASK-3
  - TASK-6
  - TASK-7
documentation:
  - docs/testing/test-strategy.md
  - docs/qna/architecture/deployment and operations.md
parent_task_id: M-0
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Set up the frontend behavior-test baseline and a minimal Playwright smoke path so M1 proves the stack can boot through the browser without expanding into broad UI coverage too early.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The Angular app has a repeatable frontend test entrypoint for component or feature-level behavior checks.
- [x] #2 Playwright is configured with a minimal smoke scenario that proves the browser can reach the routed shells through the local stack.
- [x] #3 The smoke coverage stays intentionally small and aligned with the documented critical-flow philosophy.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Draft plan pending user approval before coding.

1. Update `docs/testing/critical-e2e-flows.md` during planning so TASK-9 records the intended browser smoke coverage before implementation starts.
- If the file is still absent in this branch, create it in the planning phase rather than deferring it.
- Record the TASK-9 smoke scope there explicitly: same-origin browser reachability through Nginx plus the routed shell checks for `/`, `/admin`, `/public`, and `/maxi`.
- Keep the entry intentionally narrow so the documented E2E baseline stays aligned with the small-suite philosophy in `docs/testing/test-strategy.md`.

2. Replace the reserved frontend test target with a real Angular behavior-test harness that fits the current scaffold instead of introducing a parallel frontend toolchain.
- Add a `test` target to `apps/web/angular.json` using the installed `@angular/build:unit-test` builder with its default Vitest runner.
- Add the minimal supporting files and dev dependencies that builder expects (`vitest` plus a DOM environment such as `jsdom`), then point `apps/web/package.json` at the real Angular test entrypoint.
- Keep the harness intentionally small and behavior-focused; do not add snapshot-heavy coverage or duplicate api-owned business rules in Angular.

3. Seed the new frontend harness with a very small set of high-signal specs around the scaffolded shell behavior that already exists today.
- Add focused specs for the current standalone shell pages/components so the suite proves route-level shell content and placeholder-card wiring actually render.
- Prefer the existing admin/public/maxi scaffold surfaces and the root redirect path because they are the real user-visible behaviors currently implemented.
- Keep scope below broad integration coverage: no standings math, lifecycle rules, or realtime business semantics in frontend tests.

4. Add a minimal Playwright smoke harness that exercises the browser through the same-origin local stack from TASK-6.
- Add Playwright config and a single smoke spec that targets `http://127.0.0.1:8080` by default.
- Keep coverage intentionally tiny and aligned with the testing strategy: verify the browser can reach the Nginx-served SPA, that `/` lands on the public shell, and that `/admin`, `/public`, and `/maxi` each render their expected scaffold headings/cards through the same-origin stack.
- Do not expand into the later critical operational journeys yet; those broader flows belong to future product slices once real UI behavior exists.

5. Make the E2E entrypoint repeatable without changing the repo’s same-origin architecture.
- Replace the current `npm run e2e` placeholder with a real Playwright command.
- Add the smallest support code needed so local runs can target the Compose/Nginx stack repeatably, ideally by reusing an existing `PLAYWRIGHT_BASE_URL` when provided and otherwise managing the stack lifecycle around the smoke run.
- Reuse `infra/compose/docker-compose.yml` and the current proxy routes instead of introducing a dev-server-only E2E path.

6. Update the affected docs so the repository truth matches the new harnesses.
- Refresh `README.md`, `apps/web/README.md`, and `docs/ops/local-dev.md` so `make test-web` and `make test-e2e` are documented as real commands rather than TASK-9 placeholders, including any Playwright browser-install prerequisite.
- Update `docs/testing/test-strategy.md` so the frontend baseline reflects the actual harness added here and continues to state that Playwright remains intentionally small.
- Keep `docs/testing/critical-e2e-flows.md` in sync with the final approved smoke scope if implementation details shift after planning.

7. Validate with the narrowest honest checks for this slice.
- Run the new frontend harness directly in `apps/web` via `npm test -- --watch=false` and `npm run e2e`.
- Run the existing frontend static checks (`npm run typecheck` and `npm run check-boundaries`) so TASK-9 lands without weakening the scaffold guardrails.
- Confirm the browser smoke path can reach the same-origin stack cleanly and that any stack startup/teardown in the harness behaves predictably.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Research completed before planning: reviewed the Backlog workflow overview and task-execution guidance; `apps/web/AGENTS.md`; `docs/README.md`; `docs/testing/test-strategy.md`; `docs/ops/local-dev.md`; `docs/product/functional-requirements.md`; `docs/architecture/architecture.md`; `docs/architecture/adr/ADR-0009-testing-and-quality-gates.md`; `docs/qna/architecture/deployment and operations.md`; `docs/qna/ui/frontend architecture.md`; the current `Makefile`; `apps/web/package.json`; `apps/web/angular.json`; the shell route/components/services under `apps/web/src/app/`; the same-origin proxy config under `infra/`; and the TASK-3/TASK-6/TASK-7 dependency task records.

Current repo findings: `apps/web/package.json` still routes `test` and `e2e` to `tools/reserved-target.mjs`; `apps/web/angular.json` has build/serve targets only; the installed Angular build package already ships the experimental `unit-test` builder and defaults it to Vitest; the scaffolded browser paths are `/`, `/admin`, `/public`, and `/maxi`; and the same-origin stack from TASK-6 already serves those routes through Nginx at `http://127.0.0.1:8080`.

Documentation mismatch found during research: multiple instructions point to `docs/testing/critical-e2e-flows.md`, but that file is currently absent from the repo. The plan assumes TASK-9 should clean up that stale reference while keeping the Playwright scope aligned with the critical-flow guidance already present in `docs/testing/test-strategy.md` and the deployment/testing Q&A notes.

User clarification on 2026-03-15: `docs/testing/critical-e2e-flows.md` is expected to be updated task-by-task during the planning phase, so TASK-9 planning now treats that document as a required planning artifact instead of an optional cleanup item.

Implemented TASK-9 by adding the planning-phase browser scope record in `docs/testing/critical-e2e-flows.md`, wiring `apps/web/angular.json` to the Angular `@angular/build:unit-test` builder with a dedicated `tsconfig.spec.json`, and replacing the reserved `npm test` target with a real Vitest-backed Angular test entrypoint plus focused shell-page specs.

Added Playwright under `apps/web/` with `playwright.config.ts`, `e2e/shell-smoke.spec.ts`, and `tools/run-playwright.mjs`. The browser smoke scope stays intentionally small: root redirect plus `/admin`, `/public`, and `/maxi` shell reachability through the same-origin Nginx stack. The helper script now reuses `PLAYWRIGHT_BASE_URL` when provided and otherwise starts/stops the local Compose stack automatically.

Validation completed with `cd apps/web && npm run typecheck`, `cd apps/web && npm run check-boundaries`, `cd apps/web && npm test -- --watch=false`, `cd apps/web && npm run e2e:install`, and `cd apps/web && npm run e2e`. During validation I tightened the Playwright root-page selector to avoid a strict-mode false positive and fixed `tools/run-playwright.mjs` so stack teardown still runs after the Playwright process exits.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added the missing frontend behavior-test and browser smoke harnesses for the Angular scaffold. The web app now has a real `npm test` entrypoint backed by Angular’s `@angular/build:unit-test` builder with Vitest, plus focused component/feature specs for the current admin, public, and maxi shell pages. The app TypeScript config now excludes spec files from the main app typecheck, while the new spec config isolates test globals cleanly.

Added a small Playwright smoke suite under `apps/web/e2e/` together with `playwright.config.ts` and a local runner script that targets the TASK-6 same-origin stack. The smoke scope is intentionally narrow: it verifies `/` redirects into the public shell and that `/admin`, `/public`, and `/maxi` all render through Nginx. The helper script supports `PLAYWRIGHT_BASE_URL` overrides and, by default, starts and tears down the local Compose stack automatically.

Updated the repo docs to match the new truth: `docs/testing/critical-e2e-flows.md` now records the current active browser scope during planning, and `README.md`, `apps/web/README.md`, `docs/ops/local-dev.md`, and `docs/testing/test-strategy.md` now describe the real frontend and Playwright commands instead of TASK-9 placeholders. Validation run: `cd apps/web && npm run typecheck`, `cd apps/web && npm run check-boundaries`, `cd apps/web && npm test -- --watch=false`, `cd apps/web && npm run e2e:install`, and `cd apps/web && npm run e2e`.
<!-- SECTION:FINAL_SUMMARY:END -->
