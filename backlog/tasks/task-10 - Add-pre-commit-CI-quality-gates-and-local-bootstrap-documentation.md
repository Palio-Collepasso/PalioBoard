---
id: TASK-10
title: 'Add pre-commit, CI quality gates, and local bootstrap documentation'
status: Done
assignee:
  - '@codex'
created_date: '2026-03-12 01:37'
updated_date: '2026-03-16 11:47'
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
  - docs/ops/local-dev.md
  - docs/testing/test-strategy.md
  - docs/testing/fixtures.md
  - docs/qna/architecture/deployment and operations.md
  - docs/_raw/milestones.md
parent_task_id: M-0
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Close out m-0 by wiring the agreed quality gates into pre-commit and GitHub Actions, then document the exact local bootstrap and verification commands needed to satisfy the milestone exit criteria.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Pre-commit and CI enforce the baseline checks for formatting, linting, typing, tests, build validation, OpenAPI workflow, and architectural boundary rules.
- [x] #2 `README.md` and a dedicated local-development document describe the exact commands to boot, verify, and troubleshoot the `m-0` stack.
- [x] #3 The planning docs no longer disagree about what `m-0` includes once the bootstrap workflow and command surface are in place.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Draft plan pending user approval.

Research summary
- Current repo state: root `.pre-commit-config.yaml` is missing; `.github/workflows/web_build_and_deploy.yaml` is still a stock web-only GitHub Pages workflow; the root `Makefile` only exposes `up/down/api-dev/web-dev/openapi-export/openapi-types/test*`; api tooling in `apps/api/pyproject.toml` does not yet define Ruff or Pyright; the frontend already exposes `build`, `typecheck`, `check-boundaries`, `test`, and `e2e`; `apps/api/tests/support/postgres.py` still carries inline Postgres defaults (`postgres:16-alpine`, URL/password) instead of clearly reusing infra-owned config.

Documentation impact check
Reviewed:
- `README.md`
- `docs/ops/local-dev.md`
- `docs/testing/test-strategy.md`
- `docs/testing/critical-e2e-flows.md`
- `docs/testing/fixtures.md`
- `docs/_raw/milestones.md`
- `docs/qna/architecture/deployment and operations.md`
- `docs/qna/architecture/module boundaries.md`
- `docs/qna/architecture/api and contracts.md`
- `docs/architecture/architecture.md`
- `docs/architecture/adr/ADR-0007-api-and-contract-strategy.md`
- `docs/architecture/adr/ADR-0009-testing-and-quality-gates.md`
- `docs/engineering/documentation-impact-matrix.md`

Must update in this task (complete before code per repo rule):
- `README.md` — align the root quick-start/testing sections with the real `m-0` bootstrap and quality-gate command surface.
- `docs/ops/local-dev.md` — document the exact bootstrap, hook installation, verification, and troubleshooting commands.
- `docs/testing/test-strategy.md` — record the actual baseline quality gates and their stable entrypoints.

Likely update depending on final implementation:
- `docs/testing/fixtures.md` — if the api Postgres harness contract or local E2E prerequisites change.
- `docs/testing/critical-e2e-flows.md` — if the per-PR E2E cadence, entrypoint, or manual fallback changes.

Reviewed and currently expected to stay unchanged unless implementation uncovers a contradiction:
- `docs/qna/architecture/deployment and operations.md`
- `docs/qna/architecture/module boundaries.md`
- `docs/qna/architecture/api and contracts.md`
- `docs/architecture/architecture.md`
- `docs/architecture/adr/ADR-0007-api-and-contract-strategy.md`
- `docs/architecture/adr/ADR-0009-testing-and-quality-gates.md`

Post-implementation documentation reconciliation note:
- Final review uncovered contradictions in `docs/_raw/milestones.md` and `docs/qna/architecture/deployment and operations.md`, so both were updated to align `m-0`, the split workflow layout, and the current same-origin shell-smoke E2E scope.

Implementation plan
1. Documentation contract first
- Update `README.md`, `docs/ops/local-dev.md`, and `docs/testing/test-strategy.md` first so the documented command surface becomes the contract the code will satisfy.
- Remove stale README language that still describes runnable targets as reserved or TODO, and add the `m-0` bootstrap/verification flow plus the pre-commit/CI expectations.

2. Stabilize repo-level quality-gate entrypoints
- Extend the root `Makefile` with explicit top-level targets for formatting/linting, typing, build validation, OpenAPI verification/type generation, and architecture boundary checks so local hooks and CI call one canonical surface.
- Keep the existing app-level commands as the underlying implementation, but prefer `make` at the repo root.

3. Add missing api tooling
- Add Ruff and Pyright to `apps/api/pyproject.toml` with minimal repo-appropriate config.
- Wire api formatting/lint/type commands through `uv run ...` so they work in both local hooks and GitHub Actions.

4. Wire pre-commit with fast/slow stages
- Add a root `.pre-commit-config.yaml`.
- Use fast `pre-commit` hooks for formatting/lint/file hygiene and cheap repo invariants; use heavier `pre-push` hooks for typing/tests/build/contract checks if needed so commit latency stays reasonable while the task still enforces the agreed gates locally.
- Document installation with `pre-commit install --hook-type pre-commit --hook-type pre-push`.

5. Add repo CI without losing the dedicated frontend deploy workflow
- Add a repo-quality workflow that checks out the full monorepo, sets up Node and Python/uv, caches dependencies, and runs the canonical `make` targets.
- Keep or restore the dedicated frontend deploy workflow separately if GitHub Pages is still needed.
- Enforce api and frontend boundary checks, api Ruff/Pyright/pytest, frontend lint/typecheck/test/build, and the OpenAPI export/type-generation workflow.
- Make the OpenAPI gate fail on drift in `docs/api/openapi.yaml`; make type generation an executable check even though the generated TS declarations remain uncommitted.

6. Reconcile shared bootstrap/test config
- Inspect `apps/api/tests/support/postgres.py` against `infra/compose/docker-compose.yml` and reduce duplicated inline Postgres defaults where practical so the integration harness follows infra-owned image/config rather than drifting.
- Update any affected fixture docs if this changes local assumptions.

7. Verify and document the final workflow
- After implementation, run the full local gate set and record the exact verification commands/results in task notes. If the documented bootstrap path cannot be rerun honestly in the current environment, note that explicitly instead of implying it was exercised.
- Do not start coding until the user approves this plan.

Plan execution note: approved on 2026-03-15 and completed with the planned structure. One small compatibility fix was added during execution: the placeholder HTTP routes were converted to `async def` and the `UnitOfWork` protocol stubs were tightened so the expanded type/test gate path stayed green.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Future verification check: the api Postgres integration harness should no longer rely on hardcoded container image/default bootstrap values in `apps/api/tests/support/postgres.py`. As part of the `m-0` quality-gate/bootstrap pass, verify the tests reuse the infra-owned Docker image/service configuration introduced by the infra tasks instead of carrying separate inline defaults.

Research pass on 2026-03-15: root pre-commit config is missing, the only GitHub Actions workflow is a stock web-only GitHub Pages pipeline, the root Makefile does not yet expose lint/type/build/boundary/contract gates, and `apps/api/tests/support/postgres.py` still duplicates disposable Postgres defaults instead of clearly reusing infra-owned config.

Implemented the repo-level quality-gate surface in `Makefile`, added root `pre-commit` / `pre-push` hooks, and added a dedicated monorepo quality-gates workflow that runs the same checks through `pre-commit` while keeping the web deploy workflow separate.

Added api dev tooling (`ruff`, `pyright`, `pre-commit`) via the API dependency group, aligned the disposable Postgres integration harness with `infra/compose/docker-compose.yml`, and added unit coverage for the shared Compose-derived defaults.

Verification note: in-sandbox api HTTP tests and `pre-commit` metadata writes hit environment restrictions (loopback port binding and home-cache write access), so final validation used `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache make verify` outside the sandbox plus `PRE_COMMIT_HOME=/tmp/pre-commit ... pre-commit run --hook-stage pre-commit` and `--hook-stage pre-push`.

Post-review fix on 2026-03-16: cleaned the malformed GitHub Actions workflow tail, then split the workflows cleanly into `.github/workflows/quality_gates.yaml` for repo-wide gates and `.github/workflows/web_build_and_deploy.yaml` for the frontend Pages deploy path. The README, roadmap doc, and deployment Q&A were then reconciled to the current `m-0` truth.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented the `m-0` quality-gate and bootstrap pass for the monorepo.

What changed:
- Added stable repo-level quality-gate targets in `Makefile` for formatting, linting, typing, boundary checks, OpenAPI verification, build validation, and full-suite verification.
- Added api dev tooling through `apps/api/pyproject.toml` and `uv.lock` with Ruff, Pyright, and pre-commit support.
- Added a root `.pre-commit-config.yaml` that uses fast `pre-commit` hooks for format/lint/boundaries and heavier `pre-push` hooks for OpenAPI, type, test, and build validation.
- Added a repo-wide quality-gates workflow that installs api and frontend tooling, installs Playwright Chromium, and runs the same hook stages in CI, while keeping the frontend-only deploy workflow separate.
- Aligned `apps/api/tests/support/postgres.py` with the local Compose DB service so disposable integration-test defaults reuse infra-owned image/bootstrap settings instead of inline hardcoded values, and added `apps/api/tests/unit/test_postgres_support.py` coverage for that contract.
- Updated `README.md`, `docs/ops/local-dev.md`, `docs/testing/test-strategy.md`, `docs/testing/fixtures.md`, `docs/qna/architecture/deployment and operations.md`, `docs/_raw/milestones.md`, and `apps/api/README.md` so the documented bootstrap, troubleshooting, roadmap, and verification commands match the implemented `m-0` command surface.
- Converted the placeholder HTTP health/version routes to `async def` and corrected the `UnitOfWork` protocol method stubs so the expanded type/test gate path stays green.

Why:
- TASK-10 closes the remaining `m-0` delivery gap by making the agreed checks executable locally and in CI, and by documenting the exact bootstrap and verification flow required for contributors and reviewers.

Validation run:
- `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache make verify`
- `env -u VIRTUAL_ENV PRE_COMMIT_HOME=/tmp/pre-commit UV_CACHE_DIR=/tmp/uv-cache uv run --group dev pre-commit run --all-files --hook-stage pre-commit`
- `env -u VIRTUAL_ENV PRE_COMMIT_HOME=/tmp/pre-commit UV_CACHE_DIR=/tmp/uv-cache uv run --group dev pre-commit run --all-files --hook-stage pre-push`

Risks / follow-up:
- None required for TASK-10. The only environment-specific caveat was that local sandbox restrictions prevented honest execution of the api HTTP and Docker-backed paths, so final verification was completed outside the sandbox.

Follow-up: after self-review, cleaned the malformed workflow tail, restored `.github/workflows/web_build_and_deploy.yaml` as the frontend Pages workflow, and moved the repo-wide checks into `.github/workflows/quality_gates.yaml`.
<!-- SECTION:FINAL_SUMMARY:END -->
