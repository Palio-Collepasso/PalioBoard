# Repository Guidelines

## Project summary
- PalioBoard is a monorepo to manage the [Palio](docs/domain/palio.md) event.
- Core stack: Angular SPA + FastAPI + PostgreSQL.
- The architecture baseline is a modular monolith with strict module ownership.
- The main correctness risks are official result persistence, standings/projections, tournament progression, live ranking entry, authorization, migrations, and deploy/workflow changes.
- `make` is the stable top-level command surface. Prefer repo `make` targets over ad hoc commands when they exist.

## Rules
### Use Backlog.md
Read the workflow overview (`backlog://workflow/overview`), before creating or updating tasks, or when you're unsure whether to track work.

### Use the nearest `AGENTS.md` for stack-specific commands and conventions
- Backend/API work: `apps/api/AGENTS.md`
- Frontend/web work: `apps/web/AGENTS.md`
- Do not mix backend and frontend conventions in one change unless the task is explicitly full-stack.

## Implementation plan
When asked to write an implementation plan for a task:

1. Read the relevant [docs](`docs/README.md`).
2. Identify documents that need to be updated as part of the task (`docs/engineering/documentation-impact-matrix.md`).
3. Update documents and ask the user to accept the changes before moving to the implementation.

- If unsure whether a document is affected, **ask** to the user.
- If an **uncertainty** is still material after reading the docs, **ask** to the user and **record** the clarifications in the proper docs.

## Task implementation
When a plan is approved and you work on the task:

- Ensure you are on task branch: `tickets/ticket-<ticket-id>-<title>`.
- Ensure any doubt is clarified.
- Update documentation when behavior, schema, API contracts, architecture, or operational truth changes.
- **Flag** contradictions between docs, code, tests, and generated contracts instead of silently choosing one interpretation.

## Review behavior
- Follow `docs/engineering/code-review.md` when reviewing or responding to review comments.

## Done criteria
- relevant lint, typecheck, and tests pass
- docs and contracts are updated
- assumptions, risk, and follow-up work are stated in the PR
- any material conflict is flagged
- any document or folder that became unmanageably large is flagged

## Git Workflow
- **Branching**: Use feature branches when working on tasks (e.g. tasks/task-123-feature-name)
- **Committing**: Use the following format: TASK-123 - Title of the task
- **PR**: 
    - title: {taskId} - {taskTitle} (e.g. TASK-123 - Title of the task)
    - template: `.github/pull_request_template.md`
- **Github CLI**: Use gh whenever possible for PRs and issues