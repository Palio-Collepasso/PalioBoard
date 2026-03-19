---
id: TASK-19
title: Add API error catalog validation and generation workflow
status: Done
assignee:
  - '@codex'
created_date: '2026-03-18 21:00'
updated_date: '2026-03-18 22:30'
labels:
  - parent-task
  - api
  - error-catalog
  - codegen
dependencies: []
references:
  - docs/api/errors/index.yaml
  - docs/api/errors/schema.json
  - docs/api/errors/auth.yaml
  - docs/api/errors/users.yaml
  - docs/api/errors/games.yaml
  - docs/api/errors/standings.yaml
  - docs/api/errors/validation.yaml
  - apps/api/src/palio/app/export_openapi.py
  - Makefile
  - apps/web/src/app/shared/api/generated/
documentation:
  - docs/architecture/adr/ADR-0010-error-catalog-and-problem-details.md
  - docs/api/README.md
  - docs/api/errors/README.md
  - docs/api/error-contract.md
  - docs/api/errors/examples/example.yaml
  - docs/api/errors/examples/example.md
  - docs/engineering/documentation-impact-matrix.md
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Establish the repo-owned workflow around the endpoint-independent YAML error catalog in `docs/api/errors/`. The catalog remains the source of truth for problem identity and metadata, while `docs/api/openapi.yaml` continues to define which endpoints can return which errors. Deliver validator/generator/checker tooling that follows the existing `python -m palio.app.*` CLI pattern, commits generated Python, TypeScript, OpenAPI, and documentation artifacts, removes `replaced_by` from the active catalog contract, and adds stable top-level make groups for errors-only, api-only, and combined contract workflows.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The repository has a complete error-catalog toolchain made of catalog validation, per-module Python error-code generation, merged frontend TypeScript error-code generation, one generated OpenAPI/problem-details artifact, human-readable error-doc generation, and OpenAPI error-reference checking, all treating `docs/api/errors/index.yaml` plus imported fragment files as the single source of truth for error identity and metadata.
- [x] #2 Generated artifacts are committed, deterministic, and documented; backend Python generation respects module boundaries by emitting per-module code artifacts, the frontend receives one merged `error-codes.generated.ts`, the OpenAPI layer receives one generated problem-details artifact, and `docs/api/error-contract.md` groups errors by module provenance.
- [x] #3 Stable top-level make groups exist for error validation/generation, api validation/generation, and the combined contract workflow, and the active docs/schema/templates are aligned with the implemented workflow, including removal of `replaced_by` from the current catalog contract.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Foundation first: complete TASK-19.1 to normalize the catalog into module-owned fragments aligned with `apps/api/src/palio/modules/*`, establish `palio.shared.error_catalog` as the shared loader/validator/merged-model surface, preserve owning-module provenance, remove `replaced_by` from the active contract, and wire the initial grouped workflow plumbing without letting later tasks reparse catalog fragments independently.
2. Once TASK-19.1 lands, fan out the artifact generators against that shared model: TASK-19.2 generates per-module `error_codes_generated.py` files beside handwritten module `errors.py`, TASK-19.3 emits one merged frontend `error-codes.generated.ts`, and TASK-19.5 generates the human-readable error contract while owning the `# Error Catalog` section grouped by module provenance.
3. Handle the OpenAPI integration as a coordinated branch after the shared model is stable: TASK-19.4 generates one OpenAPI/problem-details artifact and composes it into a self-contained committed `docs/api/openapi.yaml` with local `#/components/...` refs, while TASK-19.6 validates that the committed spec references only catalog-defined errors and reports unreferenced catalog codes without moving endpoint ownership into the catalog.
4. Keep cross-cutting constraints fixed across all subtasks: the catalog stays endpoint-independent, `docs/api/openapi.yaml` remains the owner of endpoint-to-error mapping, `palio.app.*` modules are CLI entrypoints while reusable logic stays in shared packages, generated artifacts are committed, module exception classes and domain-specific constructors stay handwritten, HTTP exception mapping stays handwritten, generated human-readable docs stay owned by TASK-19.5, and `replaced_by` is not reintroduced.
5. Preserve the user-requested repo command surface as three primary grouped workflows: one errors workflow, one api workflow, and one combined contract workflow. Helper targets or scripts may exist underneath, but the top-level grouped entrypoints must remain obvious and consistent across implementation, docs, and tests.
6. Validation sequencing after implementation should stay narrow-first then grouped: each subtask adds deterministic unit coverage and its local drift checks, then the grouped workflows, then existing contract checks such as `make openapi-export`, `make openapi-types`, `make check-openapi`, and broader repo gates only when the touched surface justifies them.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Planning review completed: parent sequencing approved pending user final review and execution approval.

User final-review direction applied: backend generation is per-module `error_codes_generated.py`, frontend generation is one merged `error-codes.generated.ts`, OpenAPI generation is one problem-details artifact, and handwritten ownership remains with module `errors.py`, handwritten HTTP exception mapping, and handwritten domain-specific helper constructors.

Execution complete: all six subtasks landed with reviewed implementations and final integration across the grouped repo workflow surface.

Validation summary: focused backend unit coverage for the full toolchain passed with `31 passed`; `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache uv run --group dev pyright` passed with only the pre-existing `testcontainers.postgres` missing-stub warning; `npm run typecheck` in `apps/web` passed.

Workflow summary: `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache make typecheck` passed; `make errors` and `make api-contract` ran their full generation/validation paths and then correctly failed only on the final clean-tree drift check because the new committed generated artifacts are not yet committed in the current worktree.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Completed the API error-catalog workflow: module-aligned catalog validation, per-module backend code generation, merged frontend error-code generation, reusable OpenAPI/problem-details generation, human-readable docs generation, and OpenAPI reference checking. The repo now has the grouped `make errors`, `make api-contract`, and `make contracts` workflows, aligned docs, committed generated artifact paths, and reviewed cross-task integration.
<!-- SECTION:FINAL_SUMMARY:END -->
