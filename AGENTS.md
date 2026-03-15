# Repository Guidelines

## Project summary
- PalioBoard is a monorepo for an annual event-operations app.
- Core stack: Angular SPA + FastAPI + PostgreSQL.
- The architecture baseline is a modular monolith with strict module ownership.
- The main correctness risks are official result persistence, standings/projections, tournament progression, live ranking entry, authorization, migrations, and deploy/workflow changes.
- `make` is the stable top-level command surface. Prefer repo `make` targets over ad hoc commands when they exist.

## Instruction routing
- Root rules apply everywhere.
- Use the nearest nested `AGENTS.md` for stack-specific commands and conventions.
- Backend/API work: `apps/api/AGENTS.md`
- Frontend/web work: `apps/web/AGENTS.md`
- Do not mix backend and frontend conventions in one change unless the task is explicitly full-stack.

## Task tracking
- This repo uses Backlog.md / MCP task tracking. Read the workflow overview (`backlog://workflow/overview`) before creating or updating tasks.
- **First time working here?** Read the overview resource IMMEDIATELY to learn the workflow
- **Already familiar?** You should have the overview cached ("## Backlog.md Overview (MCP)")
- **When to read it**: BEFORE creating tasks, or when you're unsure whether to track work

You MUST read the overview resource to understand the complete workflow. The information is NOT summarized here.

## Task startup
- For non-trivial work, read the relevant docs starting from `docs/README.md`.
- Search the relevant Q&A, ADRs, and architecture/product docs before asking the user.
- If an **uncertainty** is still material after reading the docs, **ask** the smallest set of questions to the user.
- Record resolved clarifications in the appropriate Q&A document when the repo workflow expects that.

## Working rules
- Work only on a fresh task branch: `tickets/ticket-<ticket-id>-<title>`.
- Prefer the simplest solution that fits the current architecture.
- Keep changes narrow. Avoid opportunistic refactors.
- Preserve module boundaries. Use public facades rather than importing another module's internals.
- Update documentation when behavior, schema, API contracts, architecture, or operational truth changes.
- **Flag** contradictions between docs, code, tests, and generated contracts instead of silently choosing one interpretation.

## Review behavior
- Follow `docs/code-review.md` when reviewing or responding to review comments.

## Done when
- relevant lint, typecheck, and tests pass
- docs and contracts are updated when needed
- assumptions, risk, and follow-up work are stated in the PR
