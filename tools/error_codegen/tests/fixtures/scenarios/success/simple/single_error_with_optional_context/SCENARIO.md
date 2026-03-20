# Success / Simple / single_error_with_optional_context

This scenario is aligned with the revised placement guide:
- the catalog defines stable error identifiers, transport metadata, and `context_schema`
- generated domain errors live under `apps/api/src/palio/modules/<module>/errors_gen.py`
- generated API problem specs and mappings live under `apps/api/src/palio/api/modules/<module>/errors/`
- FastAPI serializes `DomainError` instances to `application/problem+json` using the generated mapping
- the frontend renders localized templates from `code + context`

Expected result: catalog is valid and generation succeeds.

## Inputs
- `contracts/errors/teams.yaml`

## Expected artifacts
- `docs/api/error-contract.md`
- `apps/api/src/palio/modules/teams/errors_gen.py`
- `apps/api/src/palio/api/modules/teams/errors/specs_gen.py`
- `apps/api/src/palio/api/modules/teams/errors/mapping_gen.py`
- `frontend/src/shared/api/error-codes.gen.ts`
- `runtime/problem_response.json`
