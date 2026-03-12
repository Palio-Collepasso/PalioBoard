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

**For product scope, goals, and non-goals**: See [docs/product/prd.md](docs/product/prd.md)
**For user-visible behavior and required flows**: See [docs/product/functional-requirements.md](docs/product/functional-requirements.md)
**For acceptance criteria and Given/When/Then scenarios**: See [docs/product/acceptance-scenarios.md](docs/product/acceptance-scenarios.md)

**For architecture, boundaries, ownership, and implementation rules**: See [docs/architecture/architecture.md](docs/architecture/architecture.md)
**For the rationale behind architectural decisions**: See [docs/architecture/adr/](docs/architecture/adr/)

**For the data model, entities, and relationships**: See [docs/domain/er-schema.md](docs/domain/er-schema.md)
**For domain rules, invariants, and business semantics**: See [docs/domain/business-rules.md](docs/domain/business-rules.md)
**For per-game configuration, formats, fields, and scoring setup**: See [docs/domain/game-catalog.md](docs/domain/game-catalog.md)
**For official source rules from the real-world event**: See [docs/domain/palio-rules.md](docs/domain/palio-rules.md)

**For clarifications, decisions and implementation notes**: See [docs/qna/README.md](docs/qna/README.md)

**For API endpoints and payloads**: See [docs/api/openapi.yaml](docs/api/openapi.yaml)
**For error codes and error semantics**: See [docs/api/error-contract.md](docs/api/error-contract.md)

**For test strategy and required test depth**: See [docs/testing/test-strategy.md](docs/testing/test-strategy.md)
**For critical end-to-end flows**: See [docs/testing/critical-e2e-flows.md](docs/testing/critical-e2e-flows.md)
**For fixtures, seed data, and test datasets**: See [docs/testing/fixtures.md](docs/testing/fixtures.md)

**For local setup and daily development commands**: See [docs/ops/local-dev.md](docs/ops/local-dev.md)
**For deployment and operational procedures**: See [docs/ops/deploy.md](docs/ops/deploy.md) and [docs/ops/runbook.md](docs/ops/runbook.md)

**For tracked changes**: See [REDLINING.md](REDLINING.md)

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

Whenever a task changes behavior, rules, structure, setup, operations, or shared understanding, update every affected document in the same change. Do not update code without updating the corresponding docs when the previous text would become stale or misleading.

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

A task is not fully complete if:
- the plan was made without gathering the needed information first
- a material doubt was left unresolved without asking the user
- a relevant Q&A clarification was discovered but not recorded
- an affected document was left stale
- a material conflict was found but not flagged
- a document or folder became unmanageably large and this was not flagged
