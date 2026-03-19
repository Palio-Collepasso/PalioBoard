# Error Catalog Refactor Plan

## Goal

Refactor the current error-catalog toolchain so that:

- the catalog remains the single source of truth for **error identifiers, transport metadata, and the shape of exposed error context fields**
- the tool generates **Python error definitions per owning module**, plus TS and docs
- **no OpenAPI artifacts are generated**
- FastAPI maps **domain/application exceptions → HTTP Problem Details**
- domain error classes remain **handwritten and module-owned**
- runtime exceptions carry the **actual context values**
- the frontend owns the **message templates** and interpolates them from `code + context`
- the CLI becomes **small and obvious**

## Core model

Adopt this conceptual split:

- **catalog/error definition**: defines the stable machine-readable contract
  - `code`
  - `type_slug`
  - `http_status`
  - `title`
  - `translation_key` (optional, recommended)
  - `context_schema` describing the shape of exposed context values
- **runtime error instance**: carries the actual context values for the specific failure
- **frontend**: maps `code` to a localized template and interpolates values from `context`

Example:

- catalog: `JOLLY_ALREADY_USED` declares required fields `team_id`, `game_id`, `previous_game_id`
- backend runtime: raises `JollyAlreadyUsedError(team_id: UUID = ..., game_id: UUID = ..., previous_game_id: UUID = ...)`
- API response: returns `type`, `code`, `title`, `status`, `context`, `request_id`, `instance`
- frontend: renders something like `Team ${team_id} has already used its jolly in game ${previous_game_id}`

## Target end state

Keep:

- catalog validation
- per-module Python generation
- TS generation
- docs generation
- `context_schema` support in the catalog and generated artifacts

Remove:

- OpenAPI component generation
- OpenAPI reference checking
- any dependency from `tools/error_codegen` to `palio.app.factory.create_app`

Introduce:

- shared runtime error primitives in the API app
- one FastAPI exception handler for catalog-backed errors
- module-local handwritten `errors.py` files that reference generated definitions
- explicit support for structured client-safe error `context`

---

## Constraints

- Prefer **incremental changes** over a rewrite.
- Preserve the current catalog concepts unless a rename is needed to support the runtime mapping cleanly.
- Keep generated files dumb: metadata only, no business behavior.
- Keep module ownership intact: generated definitions live in the owning module; exception classes also live in the owning module.
- Keep generated Python and TypeScript artifacts local and uncommitted; verify their shape through tests and snapshots instead of Git-tracked outputs.
- Do not add a new OpenAPI generation path.
- Keep human-readable frontend copy out of the backend catalog except for a stable `translation_key`.
- Only expose **safe-to-expose** structured context in API responses.

---

## Phase 0 — inspect and stabilize the baseline

1. Inspect the current tool package and list the commands and outputs:
   - `tools/error_codegen/cli.py`
   - `tools/error_codegen/__init__.py`
   - `tools/error_codegen/generators/*`
   - `tools/error_codegen/validators.py`
   - current tests under `tools/tests`

2. Confirm the actual repo paths for:
   - app factory
   - shared runtime package
   - modules root
   - docs/api/errors
   - generated TS destination
   - generated docs destination

3. Run the current tests and record failures before refactoring.

### Acceptance

- There is a short note in the PR description or task notes listing the current commands and which ones will be removed.

---

## Phase 1 — simplify the CLI surface

### Change

Refactor `tools/error_codegen/cli.py` so the public commands become:

- `validate`
- `generate`

### Concrete edits

1. Rename `validate-catalog` → `validate`
2. Replace:
   - `generate-python`
   - `generate-ts`
   - `generate-docs`
   - `generate-openapi`

   with one `generate` command that writes:
   - Python definitions
   - TS artifact
   - docs artifact

3. Remove `check-openapi-refs` from the public CLI.
4. Keep the lower-level generator functions internal if they are still useful.

### Acceptance

- `error-codegen validate`
- `error-codegen generate`

are the only commands needed for normal development.

---

## Phase 2 — remove OpenAPI generation and app coupling from the tool

### Change

Delete the OpenAPI-specific workflow from the toolchain.

### Concrete edits

1. In `tools/error_codegen/__init__.py`:
   - remove `from palio.app.factory import create_app`
   - remove all OpenAPI-related exports

2. Remove or archive:
   - `tools/error_codegen/generators/openapi.py`
   - OpenAPI-related CLI plumbing
   - OpenAPI-related validator entrypoints if they are no longer used

3. Remove these public APIs:
   - `generate_openapi_error_artifacts`
   - `check_openapi_error_references_report`
   - `render_openapi_error_reference_report`

4. Remove OpenAPI defaults from:
   - `common.py`
   - CLI
   - tests
   - docs/comments

5. Keep the tool package importable without importing any app code.

### Acceptance

- importing `tools.error_codegen` no longer imports the app factory
- the tool can run validation/generation without app runtime dependencies

---

## Phase 3 — tighten the catalog model for runtime mapping

### Change

Shift the catalog semantics from “recommended HTTP status” to “actual HTTP mapping metadata”.

### Concrete edits

1. In schema, models, fixtures, generators, and docs:
   - rename `recommended_http_status` → `http_status`

2. In `models.py`:
   - add stronger typed validation on the Pydantic side
   - enforce:
     - `code` is UPPER_SNAKE_CASE
     - `type_slug` is kebab-case
     - `http_status` is 400–599
     - `translation_key` rules are coherent with `safe_to_expose`
     - `context_schema`, when present, is an object schema intended for client-safe structured context

3. Keep JSON Schema validation, but move more semantic validation into Pydantic validators.

4. Remove dead fields from the root model if unused, especially anything only needed for the OpenAPI flow.

### Context rules

- Keep `context_schema` in the catalog.
- `context_schema` describes the shape of the values returned under `context` in the HTTP error payload.
- Use `additionalProperties: false` by default for predictable frontend interpolation.
- Prefer explicit `required` fields over loose optional bags.
- Keep only **safe-to-expose** fields in `context_schema`.

### Acceptance

- catalog entries represent the exact runtime transport metadata used by FastAPI
- invalid symbolic codes / slugs / status values fail with clear validation errors
- invalid or ambiguous context schemas fail early

---

## Phase 4 — refactor Python generation to emit definitions, not a mini runtime

### Change

Replace the current generated Python artifact shape with **module-local error definitions**.

### Current file

- `tools/error_codegen/generators/python.py`
- `tools/error_codegen/templates/python_errors.py.j2`

### Concrete edits

1. Change the generated filename from:
   - `error_codes_generated.py`

   to something like:
   - `error_defs_gen.py`

2. Generate only metadata objects, for example:
   - `ErrorDefinition`
   - one constant per error
   - optional per-module registries such as `ERROR_DEFINITIONS_BY_CODE`

3. Do **not** generate exception classes.

4. Include the normalized `context_schema` in the generated definition so runtime/tests can inspect the expected shape if needed.

5. Keep generation one-file-per-module.

### Target shape

Each module gets a generated file similar to:

- `apps/api/src/palio/modules/<module>/error_defs_gen.py`

containing:

- `ErrorDefinition` imports from shared runtime
- constants like `JOLLY_ALREADY_USED`
- maybe `ALL_ERROR_DEFINITIONS` / `ERROR_DEFINITIONS_BY_CODE`

### Acceptance

- generated Python files are dumb metadata artifacts
- no business logic or HTTP handling lives in generated files
- generated definitions preserve context shape metadata
- generated Python definitions are treated as local build artifacts rather than committed repo contracts

---

## Phase 5 — add shared runtime error primitives in the API app

### Change

Introduce a tiny shared runtime package in the API app for error transport.

### Create

Use the real project path for shared runtime, but add equivalents of:

- `.../shared/errors/base.py`
- `.../shared/errors/handlers.py`

### Concrete contents

1. Add a shared immutable `ErrorDefinition` dataclass with fields like:
   - `code`
   - `type_uri`
   - `title`
   - `http_status`
   - `translation_key`
   - `context_schema`

2. Add a base `DomainError` or `ApplicationError` class with:
   - `error_definition`
   - structured `context`

3. Validate runtime `context` against the expected schema at construction time or via a lightweight helper, at least in tests/dev paths.

4. Add a FastAPI exception handler that:
   - catches the base app/domain error type
   - returns `application/problem+json`
   - serializes:
     - `type`
     - `code`
     - `title`
     - `status`
     - `context`
   - optionally `detail` only if you explicitly want it

5. Register the handler in the app factory.

### Acceptance

- app code can raise a handwritten domain error and get a proper problem-details-style response automatically
- runtime responses include the structured `context` values expected by the frontend

---

## Phase 6 — create handwritten module-owned exceptions

### Change

For each module with catalog entries, create or update a handwritten `errors.py`.

### Concrete edits

For each module represented in `docs/api/errors/*.yaml`:

1. Create/update:
   - `apps/api/src/palio/modules/<module>/errors.py`

2. Add:
   - a module base error class
   - one handwritten exception class per exported business/app error, each referencing a generated `ErrorDefinition`

3. Exception constructors should accept the actual context values and pass them into the shared base class.

Example pattern:
- module-owned class in `errors.py`
- imports `JOLLY_ALREADY_USED` from `error_defs_gen.py`
- sets `error_definition = JOLLY_ALREADY_USED`
- constructor accepts `team_id`, `game_id`, `previous_game_id`

4. Do not centralize all exceptions in one shared package.

### Acceptance

- error classes live in the proper module
- generated definitions stay separate from handwritten semantics
- runtime exception instances carry actual context values

---

## Phase 7 — wire endpoints/use cases to raise module errors

### Change

Replace any ad hoc API error construction with raised module-owned exceptions.

### Concrete edits

1. Find where endpoints or application services currently:
   - manually build error payloads
   - rely on status/code constants directly
   - raise generic HTTP exceptions for business errors

2. Replace those with module-owned exception classes.

3. Pass the actual runtime context values into the exception constructor.

4. Keep infrastructure failures out of this path; only known business/app errors should use the catalog-backed handler.

### Acceptance

- business or policy failures are raised as module exceptions, not built ad hoc in endpoints
- the frontend receives structured `context` for templated rendering

---

## Phase 8 — keep docs and TS generation, drop OpenAPI generation

### Change

The generator still produces:

- TS error artifact
- docs error contract

but no OpenAPI artifact.

### Concrete edits

1. Keep:
   - `generators/typescript.py`
   - `generators/docs.py`

2. Remove all mentions of generated OpenAPI outputs from:
   - CLI help text
   - comments
   - docs
   - tests

3. Update TS/docs generators to use `http_status` instead of `recommended_http_status`.

4. Generate TS artifacts that preserve the error code catalog and the expected context shape for frontend typing.

5. In docs, describe frontend usage as:
   - map by `code`
   - interpolate `context`
   - own templates in the frontend/i18n layer

### Acceptance

- `generate` emits Python + TS + docs only
- TS output is sufficient for frontend templating from `code + context`

---

## Phase 9 — restructure tests around the new flow

### Change

Split tests into pure tool tests and runtime integration tests.

### Tool tests

Move the tool tests under something like:

- `tools/error_codegen/tests/unit`
- `tools/error_codegen/tests/integration`
- `tools/error_codegen/tests/snapshots`
- `tools/error_codegen/tests/fixtures`

### Add tool coverage for

1. catalog validation
2. semantic validation
3. Python definition generation
4. TS generation
5. docs generation
6. CLI `validate`
7. CLI `generate`
8. `context_schema` normalization and validation
9. snapshot coverage for representative generated `.py`, `.ts`, and `.md` outputs

### Remove/replace

- OpenAPI generator tests
- OpenAPI reference checker tests

### Add app/runtime tests

In the API app test suite, add tests for:

1. raised module-owned exception → correct problem response
2. response media type is `application/problem+json`
3. status matches `http_status`
4. body includes `type`, `code`, `title`, `status`, `context`
5. runtime context values are serialized exactly as expected
6. invalid context values are caught where validation is enabled
7. unknown exceptions still become generic 500 behavior

### Acceptance

- the tool can be tested without importing the app
- the API runtime mapping is tested in the app suite
- context-driven frontend use cases are covered by contract tests or snapshots
- snapshot tests, not committed generated code, are the stability mechanism for backend/frontend artifact shape

---

## Phase 10 — clean packaging and imports

### Change

Make the tool package import boundaries clear.

### Concrete edits

1. Normalize imports so the package works from the actual repo layout.
2. Decide one import style and make it consistent:
   - repo-internal `tools.error_codegen...`
   - or package-local relative imports

3. If the repo already treats `tools` as a package, keep that.
4. If not, fix the layout or add minimal package metadata.

### Acceptance

- tests collect without path hacks
- imports are consistent with the real repo structure

---

## Phase 11 — update docs and developer flow

### Change

Document the new workflow.

### Update docs to say

- catalog is the single source of truth for identifiers, transport metadata, and the shape of exposed error context
- generated Python definitions are consumed by handwritten module exceptions
- generated Python and TypeScript artifacts are local build outputs and should not be committed
- FastAPI serializes catalog-backed exceptions at the boundary
- frontend owns message templates and interpolates data from `code + context`
- no generated OpenAPI error components exist
- developer workflow is:

```bash
error-codegen validate
error-codegen generate
```

### Acceptance

- no doc still tells developers to run `generate-openapi` or `check-openapi-refs`
- docs explain how frontend templates consume `context`

---

## Exact files to touch first

Start with these, in this order:

1. `tools/error_codegen/cli.py`
2. `tools/error_codegen/__init__.py`
3. `tools/error_codegen/models.py`
4. `tools/error_codegen/loader.py`
5. `tools/error_codegen/validators.py`
6. `tools/error_codegen/generators/python.py`
7. `tools/error_codegen/templates/python_errors.py.j2`
8. `tools/error_codegen/generators/typescript.py`
9. `tools/error_codegen/generators/docs.py`
10. tool tests
11. app shared runtime error files
12. module-local `errors.py`
13. app factory / FastAPI handler registration

---

## What Codex should remove

Delete or stop using:

- `generate-openapi` command
- `check-openapi-refs` command
- `tools/error_codegen/generators/openapi.py`
- OpenAPI-specific tests
- any import of `create_app()` from the tool package

---

## What Codex should keep

Keep and adapt:

- YAML catalog
- JSON Schema validation
- context schema normalization
- example validation
- per-module generation
- TS generator
- docs generator

---

## Definition of done

The work is done when all of these are true:

1. `tools.error_codegen` is importable without importing app runtime
2. CLI has only:
   - `validate`
   - `generate`
3. No OpenAPI artifacts are generated by the tool
4. Catalog entries drive generated module-local Python definitions
5. Handwritten module errors reference generated definitions
6. FastAPI exception handling maps those errors to problem responses
7. Responses include structured client-safe `context`
8. Tool tests pass
9. App runtime error-mapping tests pass
10. Docs describe the new flow
11. No stale code or stale tests remain for the removed OpenAPI workflow

---

## Suggested implementation order for Codex

Tell Codex to do the work in these batches:

### Batch 1

- simplify CLI
- remove OpenAPI generation path
- decouple `__init__.py` from app factory

### Batch 2

- rename `recommended_http_status` → `http_status`
- strengthen validation
- preserve and formalize `context_schema`
- refactor Python generator to `error_defs_gen.py`

### Batch 3

- add shared runtime error primitives
- add FastAPI exception handler
- create/update module-local `errors.py`
- make exceptions carry actual context values

### Batch 4

- update TS/docs generators
- remove obsolete tests
- add new tool/runtime tests
- update developer docs

---

## One important implementation note

Codex should **not** try to derive domain errors from HTTP status.
The mapping direction must be:

```text
module-owned exception class
-> generated ErrorDefinition
-> FastAPI exception handler
-> HTTP Problem Details response
```

The frontend contract is:

```text
error code + structured client-safe context
-> frontend/i18n template
-> rendered message
```

That is the central design constraint.
