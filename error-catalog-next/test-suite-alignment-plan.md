# Error Catalog Test Suite Alignment Plan

## Confirmed decisions

- `error-catalog-next/*.md` is the intended target. In conflicts, it wins over copied local test-pack README files.
- Validation behavior must be enforced by unit tests, not only scenario-driven integration tests.
- Anything not fully enforced today must gain enforcement through stronger unit tests and, where appropriate, integration tests and scenarios.
- API tests must be rewritten toward runtime behavior. The broad dependency on the tool scenario tree is not the target shape.
- Python generator tests must be rewritten to enforce the intended architecture and invariants, not current implementation details.
- `test_generate_python_invariants.py` should follow the comment at the top of the file and assert invariants, not exact template formatting.
- Docs generation tests must enforce preservation of content before and after `# Error Catalog`, idempotence, and failure on missing heading.
- TypeScript generation tests must be strengthened.
- API runtime tests must be rewritten from scratch.
- Delete stale or misleading test code rather than carrying compatibility scaffolding.

## Important contradiction resolved

These local files are stale and should be treated as outdated:

- `tools/error_codegen/tests/README.md`
- `tools/error_codegen/tests/fixtures/scenarios/README.md`

Reason:

- they still describe metadata-only generated Python
- the intended target in `error-catalog-next/PLACEMENT_GUIDE.md` and `error-catalog-next/TEST_EXPECTATIONS.md` expects generated domain errors plus generated API problem specs and mappings

## Current gaps to fix

### Tool tests

- `tools/error_codegen/tests/unit/test_validators.py`
  Rewrite completely around catalog correctness, consistency, split-catalog semantics, and public-contract safety.

- `tools/error_codegen/tests/unit/test_models.py`
  Keep only field-level and parsing-level guarantees that belong to model validation.
  Remove assertions that overfit internal derived fields when they are not part of the intended contract.

- `tools/error_codegen/tests/unit/test_python_generator_helpers.py`
  Rewrite to enforce the intended Python generator architecture.
  Do not assert registry-style names like `ERROR_BY_CODE` if those are not target behavior.

- `tools/error_codegen/tests/integration/test_generate_python_invariants.py`
  Rewrite around invariants only:
  - one generated file per owning module
  - expected relative file path
  - no unexpected extra module files
  - syntactically valid Python
  - expected per-entry metadata/invariants as described in the comment
  - no exact formatting assertions

- `tools/error_codegen/tests/unit/test_docs_generator_helpers.py`
  Extend to cover:
  - replacing only the `# Error Catalog` section
  - preserving content before and after byte-for-byte
  - idempotence
  - failure when heading is missing

- `tools/error_codegen/tests/integration/test_generate_docs_invariants.py`
  Keep scenario-driven artifact coverage, but align it with section-injection rules instead of only string presence.

- `tools/error_codegen/tests/unit/test_typescript_generator_helpers.py`
  Extend to cover:
  - exported metadata contract
  - context key exposure for interpolation
  - nested object rendering behavior
  - no accidental flattening

- `tools/error_codegen/tests/integration/test_generate_typescript_invariants.py`
  Keep deterministic rendering and strengthen invariants around exported metadata shape and context typing.

- `tools/error_codegen/tests/integration/test_cli_smoke.py`
  Align to the current intended CLI prototype only.
  Remove stale compatibility-option expectations.

### API tests

- Delete `apps/api/tests/support/error_codegen_adapters.py`.
  It is stale, couples API tests to tool internals, and points at the wrong runtime module paths.

- Delete the current API mapping test and rewrite from scratch:
  - `apps/api/tests/integration/shared/errors/test_error_mapping.py`

- Replace the empty placeholder:
  - `apps/api/tests/integration/shared/errors/test_error_handler.py`

- Remove any API-side dependency on the full tool scenario tree.
  API tests should use:
  - local curated runtime examples
  - or explicit in-test data
  - or a small API-owned fixture pack

- Add API runtime unit-style coverage for:
  - handler maps known domain/application errors to `application/problem+json`
  - payload includes `type`, `code`, `title`, `status`, `context`
  - context passthrough is preserved
  - unknown/unmapped exceptions remain generic 500 behavior

- Add API integration coverage for real endpoint flows once the updated API scenarios are in place.

## Code/tests to delete as stale or misleading

- `tools/error_codegen/tests/old_unit/*`
- `tools/error_codegen/tests/old_integration/*`
- `apps/api/tests/support/error_codegen_adapters.py`
- current API mapping tests built on broad scenario reuse
- any runtime expectation helpers that live under tool test support and only exist to feed API runtime tests

Deletion rule:

- if a file exists only to preserve the previous metadata-registry test shape or old adapter compatibility, delete it
- if a helper still supports both old and new import paths, remove the old compatibility branches

## Refactoring direction

- Keep tool-side support under `tools/error_codegen/tests/support/` only for:
  - scenario discovery
  - catalog loading
  - generator invocation
  - CLI invocation
  - tool-side expectation derivation

- Move API runtime support to API tests only.
  Do not let API tests import runtime helpers from tool support.

- Extract repeated unit-test import helpers into one reusable support helper if they remain necessary after cleanup.

- Keep test ownership clean:
  - catalog and generation behavior in `tools/error_codegen/tests/...`
  - FastAPI/runtime behavior in `apps/api/tests/...`

## Phased plan

### Phase 1: Cleanup and ownership reset

- Delete stale test trees and stale compatibility helpers.
- Delete API-side `error_codegen_adapters.py`.
- Remove API test dependency on the full tool scenario tree.
- Normalize support ownership boundaries.

### Phase 2: Validation unit test rewrite

- Rewrite `test_validators.py` from scratch around:
  - field-shape rules
  - semantic rules
  - `context_schema` rules
  - split-catalog rules
  - exposure/transport rules

- Tighten `test_models.py` to field-level parsing and validation concerns only.

### Phase 3: Python generator test rewrite

- Rewrite helper/unit tests for the intended architecture.
- Rewrite integration invariants for file count, module ownership, path shape, syntax validity, and invariant metadata checks.
- Avoid exact template or formatting assertions.

### Phase 4: Docs and TypeScript strengthening

- Add doc injection unit tests for preservation, idempotence, and missing heading failure.
- Strengthen docs integration invariants around section ownership.
- Strengthen TypeScript unit tests around exported metadata shape and context typing.
- Strengthen TypeScript integration invariants.

### Phase 5: CLI alignment

- Keep only the intended CLI surface in smoke and prototype tests.
- Ensure smoke tests validate the supported options and artifact outputs.

### Phase 6: API runtime suite rewrite

- Write handler-level tests from scratch using local API-side support only.
- Add explicit unknown-exception behavior tests.
- Add curated consistency/runtime tests for known domain/application errors.
- Add API integration tests for real endpoint flows once updated API scenarios are ready.

## Task order and parallelization

Recommended execution order:

1. Task A first.
   It removes stale test code, stale adapters, and misleading ownership boundaries.
2. After Task A, run Tasks B, C, D, E, F, and G in parallel.
   Their write scopes are mostly independent and align to separate test surfaces.
3. Task H last.
   It depends on the rewritten API runtime direction from Task G and on updated API-side runtime scenarios or fixtures.

Parallelization summary:

- Must run first:
  - Task A
- Can run in parallel after Task A:
  - Task B
  - Task C
  - Task D
  - Task E
  - Task F
  - Task G
- Must run after Task G and updated runtime fixtures:
  - Task H

## Subagent-ready task split

### Task A: Tool test cleanup and ownership reset

Write scope:

- `tools/error_codegen/tests/old_unit/*`
- `tools/error_codegen/tests/old_integration/*`
- `tools/error_codegen/tests/support/*`
- `apps/api/tests/support/error_codegen_adapters.py`
- API test files that currently import it

Deliverables:

- stale files deleted
- support boundaries cleaned up
- no broad API dependency on tool test internals

### Task B: Validation/model unit tests

Write scope:

- `tools/error_codegen/tests/unit/test_models.py`
- `tools/error_codegen/tests/unit/test_validators.py`
- small shared unit-test helper if really needed

Deliverables:

- field-level model tests
- semantic validator tests
- split-catalog and context-schema rule coverage

### Task C: Python generator tests

Write scope:

- `tools/error_codegen/tests/unit/test_python_generator_helpers.py`
- `tools/error_codegen/tests/integration/test_generate_python_invariants.py`
- tool-side support helpers only if needed for these tests

Deliverables:

- strong invariant-based Python generator tests aligned with the intended target

### Task D: Docs generator tests

Write scope:

- `tools/error_codegen/tests/unit/test_docs_generator_helpers.py`
- `tools/error_codegen/tests/integration/test_generate_docs_invariants.py`

Deliverables:

- section-injection preservation tests
- idempotence tests
- missing-heading failure tests

### Task E: TypeScript tests

Write scope:

- `tools/error_codegen/tests/unit/test_typescript_generator_helpers.py`
- `tools/error_codegen/tests/integration/test_generate_typescript_invariants.py`

Deliverables:

- stronger metadata-shape and context-rendering assertions
- deterministic integration coverage

### Task F: CLI smoke and prototype tests

Write scope:

- `tools/error_codegen/tests/unit/test_cli_prototype.py`
- `tools/error_codegen/tests/integration/test_cli_smoke.py`

Deliverables:

- no stale compatibility-option expectations
- smoke coverage aligned with the intended CLI surface only

### Task G: API runtime handler-level suite rewrite

Write scope:

- `apps/api/tests/integration/shared/errors/*`
- API-local runtime support helpers under the same package or API test support

Deliverables:

- rewritten mapping/handler tests from scratch
- known-error handler tests
- unknown-exception 500 tests
- no dependency on tool support adapters

### Task H: API endpoint/runtime integration follow-up

Write scope:

- API integration tests outside the shared handler package, once updated runtime scenarios/fixtures are available

Deliverables:

- real endpoint-flow tests for representative module-owned errors
- optional curated consistency checks between runtime exception classes and catalog metadata

## Execution constraints for later

- Do not read or rewrite scenario YAML content unless explicitly required.
- Prefer deleting misleading compatibility code over adding more fallback logic.
- Keep test ownership boundaries clean even if that means replacing helpers instead of reusing them.

## Progress

Write here the progress. Append only