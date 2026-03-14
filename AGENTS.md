# Repository Guidelines

<!-- BACKLOG.MD MCP GUIDELINES START -->

<CRITICAL_INSTRUCTION>

## BACKLOG WORKFLOW INSTRUCTIONS

This project uses Backlog.md MCP for all task and project management activities.

**CRITICAL GUIDANCE**

- If your client supports MCP resources, read `backlog://workflow/overview` to understand when and how to use Backlog for this project.
- If your client only supports tools or the above request fails, call `backlog.get_workflow_overview()` tool to load the tool-oriented overview (it lists the matching guide tools).

- **First time working here?** Read the overview resource IMMEDIATELY to learn the workflow
- **Already familiar?** You should have the overview cached ("## Backlog.md Overview (MCP)")
- **When to read it**: BEFORE creating tasks, or when you're unsure whether to track work

These guides cover:
- Decision framework for when to create tasks
- Search-first workflow to avoid duplicates
- Links to detailed guides for task creation, execution, and finalization
- MCP tools reference

You MUST read the overview resource to understand the complete workflow. The information is NOT summarized here.

</CRITICAL_INSTRUCTION>

<!-- BACKLOG.MD MCP GUIDELINES END -->

- For changes under `apps/api/`, follow `apps/api/AGENTS.md`.
- For changes under `apps/web/`, follow `apps/web/AGENTS.md`.
- **NEVER** mix conventions under `apps/api/` with conventions under `apps/web/`.

## Workflow
When working on a task:
1. Assign it to yourself: : -a @{your-name}
2. Create a git worktree under `../palio-trees/tasks/task-taskId-taskTitle`
3. At the end of every task implementation, try to take a moment to see if you can simplify it. When you are done implementing, you know much more about a task than when you started. At this point you can better judge retrospectively what can be the simplest architecture to solve the problem. If you can simplify the code, do it.

## Simplicity-first implementation rules
- Prefer a single implementation for similar concerns. Reuse or refactor to a shared helper instead of duplicating.

## Planning and information gathering

Before planning or implementing any non-trivial task, gather enough information to execute safely.

Required behavior:
- Explore the relevant docs before proposing or executing a plan.
- Read the most relevant product, architecture, domain, API, testing, ops, and Q&A documents for the task.
- Use Q&A files to resolve local clarifications before asking the user.
- Do not assume missing details when the docs are likely to contain them.
- If the docs do not provide enough information to proceed safely, follow [Doubts and unanswered questions](#doubts-and-unanswered-questions)

A plan is valid only if it is based on enough documented information or on explicit user answers for the remaining gaps.

## Documentation (Where to find information)

**Product scope, goals, and non-goals**: See [docs/product/prd.md](docs/product/prd.md)
**User-visible behavior and required flows**: See [docs/product/functional-requirements.md](docs/product/functional-requirements.md)
**Acceptance criteria and Given/When/Then scenarios**: See [docs/product/acceptance-scenarios.md](docs/product/acceptance-scenarios.md)

**Architecture, boundaries, ownership, and implementation rules**: See [docs/architecture/architecture.md](docs/architecture/architecture.md)
**Rationale behind architectural decisions**: See [docs/architecture/adr/](docs/architecture/adr/)

**Data model, entities, and relationships**: See [docs/domain/er-schema.md](docs/domain/er-schema.md)
**Domain rules, invariants, and business semantics**: See [docs/domain/business-rules.md](docs/domain/business-rules.md)
**Per-game configuration, formats, fields, and scoring setup**: See [docs/domain/game-catalog.md](docs/domain/game-catalog.md)
**Official source rules from the real-world event**: See [docs/domain/palio-rules.md](docs/domain/palio-rules.md)

**Clarifications, decisions and implementation notes**: See [docs/qna/README.md](docs/qna/README.md)

**API endpoints and payloads**: See [docs/api/openapi.yaml](docs/api/openapi.yaml)
**Error codes and error semantics**: See [docs/api/error-contract.md](docs/api/error-contract.md)

**Test strategy and required test depth**: See [docs/testing/test-strategy.md](docs/testing/test-strategy.md)
**Critical end-to-end flows**: See [docs/testing/critical-e2e-flows.md](docs/testing/critical-e2e-flows.md)
**Fixtures, seed data, and test datasets**: See [docs/testing/fixtures.md](docs/testing/fixtures.md)

**Local setup and daily development commands**: See [docs/ops/local-dev.md](docs/ops/local-dev.md)
**Deployment and operational procedures**: See [docs/ops/deploy.md](docs/ops/deploy.md) and [docs/ops/runbook.md](docs/ops/runbook.md)

**Tracked changes**: See [REDLINING.md](REDLINING.md)

## Conflict and contradiction handling

When you find a conflict, contradiction, mismatch, or ambiguity in or across documents, flag it to the user explicitly.

Required behavior:
- Do **not** silently choose one interpretation when the conflict is material.
- Report where the conflict appears and why it matters.
- Ask the user for a decision before proceeding.
- Solve the conflict by updating the affected documents.
- When relevant, record the clarification in the appropriate Q&A file.

## Doubts and unanswered questions

If a doubt cannot be resolved from the main docs or the Q&A docs, ask the user a focused question before making a risky assumption.

Required behavior:
- Ask the user the smallest set of concrete questions needed to continue safely.
- After the user answers, add the clarification to the proper Q&A file.
- If the user has not answered yet and the question is still open, repeat.

## Documentation maintenance

The agent must update the relevant docs whenever a task changes their truth. Do not update code without updating the corresponding docs when the previous text would become stale or misleading.

This applies to all affected documentation, including but not limited to:
- product docs
- architecture docs
- ADRs
- domain docs
- Q&A docs
- API docs
- testing docs
- ops docs
- tracked-change notes

Required behavior:
- Perform a documentation impact check for every non-trivial task.
- Update all affected docs, not just the most obvious one.
- Prefer updating existing sections over duplicating information.
- Keep docs consistent with code, tests, and other docs in the same change.
- If a task changes current behavior, examples, commands, guarantees, constraints, or workflows, update the relevant docs immediately.


## File size and document health

When a file becomes too large, too mixed in purpose, or too hard to navigate, flag it to the user.

Required behavior:
- Flag files that are hard to explore, hard to search mentally, or carry too many unrelated responsibilities.
- Suggest a split when one file mixes unrelated topics that should live in separate documents.
- Suggest an index or README when a folder grows enough that discoverability becomes poor.
- Prefer structural fixes over adding more text to an already overloaded file.

Heuristics to watch for:
- dense prose files roughly above 300-400 lines
- multiple unrelated concerns in one document
- repeated back-and-forth scanning to find one answer
- sections that should clearly live in different subpaths
- a Q&A folder whose contents are no longer discoverable from its README

## Done criteria

A task is fully complete if:
- the plan is made after gathering the needed information first
- all material doubts are resolved by asking the user
- any relevant Q&A clarification is recorded
- all affected documents are kept up to date
- `README.md` is up to date
- any material conflict is flagged
- any document or folder that became unmanageably large is flagged

## Git Workflow
- **Branching**: Use feature branches when working on tasks (e.g. tasks/task-123-feature-name)
- **Committing**: Use the following format: TASK-123 - Title of the task
- **PR**: 
    - title: {taskId} - {taskTitle} (e.g. TASK-123 - Title of the task)
    - template: `.github/pull_request_template.md`
- **Github CLI**: Use gh whenever possible for PRs and issues
