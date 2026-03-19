# Repository Guidelines

## Purpose
PalioBoard is a monorepo for managing the Palio event.
This file defines **repo-wide working rules** for coding agents.

For documentation source precedence, reading sets, archive policy, and UI proposal status, read `docs/README.md`.

## Start sequence
1. Read `docs/README.md`.
2. Read the nearest scope-specific `AGENTS.md`.
3. Read only the smallest relevant authoritative doc set.
4. If code, migrations, or committed API contracts disagree with docs, treat code and committed contracts as current behavior and update docs in the same change.
5. Flag contradictions instead of guessing.

## Scope-specific AGENTS files
- Backend/API work: `apps/api/AGENTS.md`
- Frontend/web work: `apps/web/AGENTS.md`

## Stable command surface
Use repo `make` targets when they exist.

- Repo quality gates: `make format`, `make format-check`, `make lint`, `make typecheck`, `make check-boundaries`, `make check-openapi`, `make test`, `make build`, `make verify`
- API contract workflow: `make openapi-export`, `make openapi-types`, `make check-openapi`
- Backend local tests: `make test-api-unit`, `make test-api-integration`
- Web local tests: `make test-web`, `make test-e2e`
- Local environment details: `docs/ops/local-dev.md`

## Repo-wide working rules
- Keep business logic in backend application or domain layers, not in the frontend, database views, triggers, or migrations.
- Preserve module boundaries; use public facades and explicit orchestrators for cross-module workflows.
- Treat the write model as authoritative and read models or projections as derived data.
- Keep changes narrowly scoped; do not mix unrelated refactors into correctness-sensitive work.
- Flag documentation that became contradictory, redundant, or too large to navigate quickly.

## Documentation update rule
Update the authoritative docs in the same change when behavior, schema, API contracts, architecture, operations, or an implemented UI workflow changes.

## Stop and flag
Stop and flag the issue when:
- two authoritative docs disagree
- a required rule is missing
- a Q&A answer appears to override an authoritative doc
- the task depends on behavior that is still open or ambiguous
- the relevant doc is too large or too scattered to navigate safely

## Git Workflow
- **Branching**: Use feature branches when working on tasks (e.g. tasks/task-123-feature-name)
- **Committing**: Use the following format: TASK-123 - Title of the task
- **PR**: 
    - title: {taskId} - {taskTitle} (e.g. TASK-123 - Title of the task)
    - template: `.github/pull_request_template.md`
- **Github CLI**: Use gh whenever possible for PRs and issues