# Failure / Medium / duplicate_type_slug_across_modules

This scenario is aligned with the revised placement guide:
- the catalog defines stable error identifiers, transport metadata, and `context_schema`
- generated domain errors and API problem mappings are derived from valid catalog entries
- validation must fail before any generated backend or frontend artifacts are accepted

Expected result: catalog is invalid and validation fails.

## Inputs
- `contracts/errors/event_operations.yaml`
- `contracts/errors/index.yaml`
- `contracts/errors/teams.yaml`

## Expected artifacts
- `validation-report.txt`
