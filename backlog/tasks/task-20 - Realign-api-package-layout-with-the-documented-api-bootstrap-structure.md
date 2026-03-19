---
id: TASK-20
title: Realign api package layout with the documented api/bootstrap structure
status: Done
assignee:
  - '@codex'
created_date: '2026-03-18 21:08'
updated_date: '2026-03-18 22:15'
labels:
  - api
  - architecture
  - refactor
milestone: m-1
dependencies: []
references:
  - apps/api/src/palio/app/
  - apps/api/src/palio/db/
  - apps/api/README.md
  - Makefile
  - infra/docker/api.Dockerfile
  - apps/api/migrations/env.py
  - apps/api/tests/unit/test_app.py
  - apps/api/tests/unit/test_db_runtime.py
  - apps/api/tests/unit/test_openapi_export.py
  - apps/api/tests/integration/test_app.py
documentation:
  - docs/architecture/architecture.md
  - docs/architecture/module-map.md
  - apps/api/AGENTS.md
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Bring the backend scaffold back in line with the approved architecture so future API feature work lands in the intended package boundaries instead of extending the current `palio.app` and `palio.db` drift.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The backend top-level package layout follows the documented `palio/api`, `palio/bootstrap`, `palio/shared`, and `palio/modules` shape, with the current `palio.app` responsibilities split into the correct `api` and `bootstrap` packages.
- [x] #2 Database runtime and configuration code no longer live under `palio.db`; they are moved under the bootstrap-owned package, and the refactor preserves the current runtime behavior, test coverage, and command surface without introducing a UnitOfWorkFactory abstraction.
- [x] #3 Repository docs, imports, entrypoints, and tests are updated in the same change so the codebase no longer documents or depends on the stale `palio.app` or `palio.db` package layout.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Approved implementation plan for TASK-20:

Decision on DB placement
- Keep the database runtime/configuration/session code together under a bootstrap-owned DB package.
- Do not move the DB layer into `palio.shared` and do not split it between `bootstrap` and `shared`.
- Rationale: the current DB code is runtime assembly (`build_database_runtime`), migration/runtime configuration helpers, readiness probing, and the concrete SQLAlchemy-backed Unit of Work. That is composition-root infrastructure, not a truly generic helper surface. Splitting out only `UnitOfWork` or similar types into `shared` would add churn without improving ownership and would blur the documented rule that `shared` stays limited to low-level generic helpers.

1. Establish the new `palio/api` and `palio/bootstrap` ownership split at the package level.
- Create the documented top-level packages under `apps/api/src/palio/` and move the current `palio.app` responsibilities into them.
- Move HTTP-facing code into `palio/api/`, including routes and request-handling middleware helpers.
- Move composition-root code into `palio/bootstrap/`, including `ApplicationRuntime`, `ModuleFacades`, runtime assembly, the FastAPI app factory/entrypoint wiring, and the OpenAPI export CLI.
- Move the current `palio.db` surface into `palio/bootstrap/db/` so database runtime, readiness, migration config helpers, and the session-bound Unit of Work all live under bootstrap ownership.

2. Rewire imports and startup/CLI entrypoints to the new package layout without changing behavior.
- Update internal imports across relocated modules.
- Update `Makefile`, `infra/docker/api.Dockerfile`, `apps/api/migrations/env.py`, and package exports used by tests.
- Remove direct runtime dependencies on `palio.app` and `palio.db` in the active codebase instead of leaving compatibility shims.
- Preserve current observable behavior exactly.

3. Update the tests to validate the new package layout rather than the old one.
- Rewrite unit and integration imports that currently target `palio.app` or `palio.db` so they exercise the new `palio.api` / `palio.bootstrap` / `palio.bootstrap.db` paths.
- Keep the existing smoke assertions intact.
- Add only the minimum extra coverage needed for any package-export changes.

4. Update only the stale docs and repo guidance relevant to this refactor.
- Update `apps/api/README.md` to describe the new package layout and new module paths for app startup and OpenAPI export.
- Update any repo command/documentation touchpoints that actually become stale because of the move, such as `Makefile` comments/help text if needed and container entrypoint references.
- Ignore `docs/api/*` and error-contract concerns for this task unless the refactor directly breaks them, per user direction.

5. Validate the refactor with focused backend checks.
- Run `make test-api-unit`, `make test-api-integration`, `make check-openapi`, and `make check-boundaries`.
- Run `make lint` and `make typecheck` if the moved modules introduce broader fallout.
- Confirm the updated OpenAPI export path and app boot entrypoint resolve after the move.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Research completed before planning: reviewed `docs/README.md`, `apps/api/AGENTS.md`, `docs/architecture/architecture.md`, `docs/architecture/module-map.md`, `docs/architecture/runtime-flows.md`, `apps/api/README.md`, the current `apps/api/src/palio/app/` and `apps/api/src/palio/db/` packages, `apps/api/migrations/env.py`, the top-level `Makefile`, `infra/docker/api.Dockerfile`, and the current unit/integration tests that import the old package layout.

Current codebase findings: the authoritative architecture docs and backend AGENTS file already expect `apps/api/src/palio/api/` and `apps/api/src/palio/bootstrap/`, but the actual code tree still exposes only `palio.app` and `palio.db`. `palio.app.bootstrap` owns runtime/module wiring and imports `palio.db`; `palio.app.factory` currently mixes app creation, middleware registration, and router inclusion; `palio.db` owns migration config helpers, SQLAlchemy runtime assembly, readiness probing, and the session-bound Unit of Work.

Dependency surface found during research: the stale package paths are referenced by `Makefile`, `infra/docker/api.Dockerfile`, `apps/api/migrations/env.py`, `apps/api/README.md`, `apps/api/tests/unit/test_app.py`, `apps/api/tests/unit/test_db_runtime.py`, `apps/api/tests/unit/test_openapi_export.py`, and `apps/api/tests/integration/test_app.py`. The architecture docs already describe the target state correctly, so the expected documentation work is mostly removing stale implementation-path references rather than rewriting the architecture baseline.

Additional documentation gap noted during research: `docs/README.md` tells API-contract work to read `docs/api/README.md`, but `docs/api/README.md` does not currently exist in the repo. That is not a blocker for TASK-20, but it is a concrete doc-navigation inconsistency surfaced during the planning pass.

No code changes started. Waiting for explicit user approval before implementation.

User approved implementation on 2026-03-18 and explicitly directed this task to ignore `docs/api` and error-contract concerns unless they directly block the package-layout refactor.

Placement decision recorded before coding: the DB layer should stay together under bootstrap ownership as `palio.bootstrap.db`, not move to `palio.shared` and not be split across bootstrap/shared. The current DB code is composition-root/runtime infrastructure rather than a generic shared helper surface.

Implemented the package realignment by creating `apps/api/src/palio/api/` and `apps/api/src/palio/bootstrap/`, moving the former `palio.app` HTTP code into `palio.api`, moving runtime/app-factory wiring into `palio.bootstrap`, and moving the former `palio.db` package intact into `palio.bootstrap.db`. The old `apps/api/src/palio/app/` and `apps/api/src/palio/db/` trees were removed so the top-level package layout now matches the documented target shape.

Updated the active dependency surface to the new package paths: `Makefile` now points `api-dev` at `src/palio/bootstrap/main.py` and `openapi-export` at `palio.bootstrap.export_openapi`; `infra/docker/api.Dockerfile` now runs the bootstrap entrypoint; `apps/api/migrations/env.py` now imports `palio.bootstrap.db.config`; and the API smoke/runtime tests now import from `palio.bootstrap` / `palio.bootstrap.db`. `apps/api/README.md` was updated to describe the new package layout and command paths.

Validation completed with backend-focused checks:
- `./.venv/bin/python -u -m pytest tests/unit/test_db_runtime.py tests/unit/test_openapi_export.py tests/unit/test_module_boundaries.py tests/unit/test_settings.py -q`
- `./.venv/bin/python -u -m palio.shared.module_boundaries`
- `./.venv/bin/ruff check src tests`
- `./.venv/bin/ruff format --check src tests`
- `./.venv/bin/pyright`
- `./.venv/bin/python -u -m palio.bootstrap.export_openapi ../../docs/api/openapi.yaml`
- `git diff --exit-code -- docs/api/openapi.yaml`
- outside the sandbox to bypass local execution limits: `env -u VIRTUAL_ENV uv run pytest tests/unit -q`, `env -u VIRTUAL_ENV uv run pytest tests/integration/test_migrations.py -q`, and `env -u VIRTUAL_ENV uv run pytest tests/integration/test_app.py -q`
The backend boundary checker and API test suites passed. Full top-level `make check-boundaries` remains blocked in this local environment by the frontend half (`apps/web` reports `depcruise: not found`), which is unrelated to TASK-20.

Follow-up refinement after initial completion: moved the `UnitOfWork` protocol out of `palio.bootstrap.db` into `apps/api/src/palio/shared/unit_of_work.py`, removed the SQLAlchemy `Session` type from the public Unit of Work interface, and kept `SqlAlchemyUnitOfWork` as the bootstrap-owned implementation detail. `DatabaseRuntime.create_unit_of_work()` now returns the application-facing `UnitOfWork` contract while the DB package only exposes the concrete SQLAlchemy implementation.

Follow-up refinement after the first UnitOfWork cleanup: moved the application-facing `UnitOfWork` contract again from `palio.shared` into a dedicated `apps/api/src/palio/application/` package so the interface now lives in the application layer rather than in the DB or shared technical layer. `palio.bootstrap.db` continues to own only the SQLAlchemy implementation.

Follow-up refinement after the application-layer UnitOfWork move: moved the concrete `SqlAlchemyUnitOfWork` implementation out of `palio.bootstrap.db` into `apps/api/src/palio/shared/db/`, leaving `palio.bootstrap.db` responsible only for runtime DB assembly and wiring. Updated the module map so it now documents `bootstrap/db` as runtime wiring and `shared/db` as reusable low-level DB implementation helpers.

Final follow-up refinement: moved `SqlAlchemyUnitOfWork` from `palio.shared.db` into `apps/api/src/palio/infrastructure/db/`, so the final ownership split is now `palio.application` for the interface contract, `palio.infrastructure.db` for the reusable concrete SQLAlchemy implementation, and `palio.bootstrap.db` for runtime DB assembly and factory wiring. Updated `apps/api/README.md` and `docs/architecture/module-map.md` to reflect that final structure.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Realigned the API scaffold to the documented package shape by replacing the stale `palio.app` and `palio.db` top-level packages with `palio.api`, `palio.bootstrap`, and `palio.bootstrap.db`. HTTP routes and request middleware now live under the API package, while app/runtime wiring, logging setup, OpenAPI export, and SQLAlchemy runtime/configuration stay under bootstrap ownership.

Updated the active command/import surface in `Makefile`, `infra/docker/api.Dockerfile`, `apps/api/migrations/env.py`, `apps/api/README.md`, and the API smoke/runtime tests so the codebase no longer depends on the old package paths. Validation covered linting, formatting, type checking, backend boundary enforcement, OpenAPI export stability, the full API unit suite, and the integration migration/readiness smoke tests.

After completion, tightened the ownership boundary further by moving the `UnitOfWork` protocol out of the DB package and stripping SQLAlchemy `Session` from the interface surface. The protocol now lives in `palio.shared`, while `palio.bootstrap.db` keeps only the SQLAlchemy-backed implementation and runtime wiring.

A later cleanup also introduced `palio.application` so the `UnitOfWork` contract now lives in the application layer instead of in `shared`, keeping SQLAlchemy concerns confined to `palio.bootstrap.db`.

Another cleanup then moved `SqlAlchemyUnitOfWork` under `palio.shared.db`, leaving `palio.bootstrap.db` focused on runtime assembly while `palio.application` owns the interface contract.

The final ownership split places `UnitOfWork` in `palio.application`, `SqlAlchemyUnitOfWork` in `palio.infrastructure.db`, and runtime DB assembly in `palio.bootstrap.db`.
<!-- SECTION:FINAL_SUMMARY:END -->
