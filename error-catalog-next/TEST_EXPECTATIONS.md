# Test expectations

These expectations match the corrected architecture:

- generated domain errors
- generated API problem specs
- generated mappings
- handwritten runtime/boundary code
- section injection into `docs/api/error-contract.md`

## Tool tests

### Validation tests
Should verify:
- valid split catalogs pass
- invalid `code` fails
- invalid `type_slug` fails
- invalid `http_status` fails
- example context must satisfy `context_schema`
- cross-file duplicate `code` fails
- cross-file duplicate `type_slug` fails

### Domain error generation tests
Should verify:
- one dataclass-like domain error per catalog entry
- generated file lives under `palio/modules/<module>/errors_gen.py`
- field names come from `context_schema.properties`
- required and optional fields are represented consistently
- no HTTP/API metadata leaks into generated domain classes

### API problem spec generation tests
Should verify:
- one API problem constant per catalog entry
- generated file lives under `palio/api/modules/<module>/errors/specs_gen.py`
- `code`, `type_uri`, `title`, `http_status`, `translation_key` are correct
- no domain fields are duplicated as top-level spec metadata

### Mapping generation tests
Should verify:
- one mapping entry per catalog entry
- mapping connects generated domain type to generated API problem spec
- mapping file lives under `palio/api/modules/<module>/errors/mapping_gen.py`

### TypeScript generation tests
Should verify:
- exported catalog contains `code`, `typeUri`, `title`, `httpStatus`, `translationKey`
- context keys are listed for frontend interpolation
- nested fields are not flattened incorrectly unless intentionally designed

### Doc injection tests
Should verify:
- only the `# Error Catalog` section is replaced
- content before and after the section is preserved byte-for-byte
- rerunning generation is idempotent
- failure occurs when the heading is missing
- failure occurs when generated markers are malformed, if your generator requires them

## Runtime integration tests

### Domain error to Problem Details mapping
Should verify:
- raising a generated domain error is caught by the handler
- registry resolves the correct generated API problem spec
- response media type is `application/problem+json`
- response includes:
  - `type`
  - `code`
  - `title`
  - `status`
  - `context`
- `context` is built from the generated domain error fields

### Unknown error behavior
Should verify:
- unknown/unmapped exceptions do not silently claim a catalog problem
- generic 500 behavior remains separate

## Recommended test split

```text
tests/
  unit/
    test_validate_catalog.py
    test_generate_domain_errors.py
    test_generate_api_problems.py
    test_generate_mappings.py
    test_generate_typescript.py
    test_doc_injection.py
  integration/
    test_runtime_problem_mapping.py
    test_catalog_to_http_problem_flow.py
```
