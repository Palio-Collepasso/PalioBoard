# Error catalog fixtures, snapshots, and test pack (v2)

This pack reflects the revised architecture:

- **generated domain errors**
- **generated API problem specs**
- **generated mapping** from domain error type to API problem spec
- **handwritten boundary/runtime pieces only**
  - shared `DomainError`
  - Specs DTO/helper
  - FastAPI exception handlers
- **generated docs injected into** `docs/api/error-contract.md`
- **frontend owns final user-facing templates**, consuming `code + context`

## Main differences from current version

- generated Python is no longer `ErrorDefinition` next to the domain module
- domain errors are now generated under each owning module
- API problem specs are generated in the API layer
- mappings are generated in the API layer
- handlers and shared base classes stay handwritten
- the docs generator must replace only the `# Error Catalog` section body, preserving the rest

## Pack contents

- `PLACEMENT_GUIDE.md` — where each piece belongs
- `TEST_EXPECTATIONS.md` — what the tests should verify
- `fixtures/` — inputs for generation and validation tests
- `snapshots/` — expected generated outputs and reports
- `tests/` — pytest-style test templates aligned to the architecture
- `examples/` — illustrative generated/handwritten code samples

## Architecture summary

For each catalog entry, generate:

1. a **domain error class** in `palio/modules/<module>/errors_gen.py`
2. an **API problem spec** in `palio/api/modules/<module>/errors/specs_gen.py`
3. a **mapping entry** in `palio/api/modules/<module>/errors/mapping_gen.py`

At runtime:

- application/domain code raises the **generated domain error**
- FastAPI handler catches `DomainError`
- mapping resolves the API problem spec
- dataclass fields are serialized into `context`
- frontend renders localized templates from `code + context`
