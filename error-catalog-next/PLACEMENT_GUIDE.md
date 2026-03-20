# Placement guide

Use this layout for the revised architecture.

```text
contracts/
  errors/
    index.yaml
    event_operations.yaml
    authorization.yaml
    teams.yaml
    results.yaml
  openapi.yaml

docs/
  api/
    error-contract.md

tools/
  error_codegen/
    ...

apps/
  api/
    src/
      palio/
        shared/
          errors.py                  # base DomainError only, no HTTP/API knowledge
        modules/
          event_operations/
            errors.py                # handwritten domain errors, re-exports from errors_gen.py.
            errors_gen.py            # generated domain errors
          authorization/
            errors.py
          ...
        api/
          errors/
            spec.py                  # API transport DTO/helper
            handlers.py              # FastAPI exception handlers
          modules/
            event_operations/
              errors/
                specs_gen.py
                mapping_gen.py
              ...
```

## What goes where

### `contracts/errors/*.yaml`
Single source of truth for:
- stable error code
- `type_slug`
- `http_status`
- `title`
- `translation_key`
- `context_schema`
...

### `apps/api/src/palio/shared/errors.py`
Only domain-wide base exception types.
No HTTP status, no media type, no Problem Details knowledge.

### `apps/api/src/palio/modules/<module>/errors_gen.py`
Generated domain errors with explicit fields.

Example:
```python
@dataclass(slots=True)
class JollyAlreadyUsedError(DomainError):
    team_id: str
    game_id: str
    previous_game_id: str
```

These classes may subclass `DomainError`, but must not know:
- HTTP status
- `type_uri`
- response envelopes
- FastAPI

### `apps/api/src/palio/api/modules/<module>/errors/specs_gen.py`
Generated API error specs from the catalog.

These contain transport metadata only, for example:

```python
JOLLY_ALREADY_USED_API_PROBLEM = ApiProblemSpec(
    code="JOLLY_ALREADY_USED",
    type_uri="https://api.palioboard.local/problems/jolly-already-used",
    title="Jolly already used",
    http_status=409,
)
```

### `apps/api/src/palio/api/modules/<module>/errors/mapping_gen.py`
Generated mapping tables from domain error type to API problem spec.

Default recommendation:
- generate mappings when the catalog-to-domain mapping is 1:1
- allow handwritten overrides only for special cases

Example:
```python
from app.modules.event_operations.errors_gen import JollyAlreadyUsedError

ERROR_TO_PROBLEM = {
    JollyAlreadyUsedError: JOLLY_ALREADY_USED_API_PROBLEM,
}
```

### `apps/api/src/palio/api/errors/spec.py`
- `ApiProblemSpec`
- serializer/helper to build reponse payloads

Example:
```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ApiProblemSpec:
    code: str
    type_uri: str
    title: str
    http_status: int
```

### `apps/api/src/palio/api/errors/handlers.py`
FastAPI exception handlers:
- catch `DomainError`
- look up the generated API problem spec through the mapping
- serialize a Problem Details response with `context` built from domain error fields

Example:
```python
from dataclasses import asdict
from fastapi.responses import JSONResponse

@app.exception_handler(DomainError)
async def handle_domain_error(request, exc: DomainError) -> JSONResponse:
    spec = ERROR_TO_PROBLEM[type(exc)]
    return JSONResponse(
        status_code=spec.http_status,
        media_type="application/problem+json",
        content={
            "type": spec.type_uri,
            "code": spec.code,
            "title": spec.title,
            "status": spec.http_status,
            "context": asdict(exc),
        },
    )
```

### `docs/api/error-contract.md`
Human-edited document with one injected section.

The generator must:
- find the `# Error Catalog` heading
- replace only that section body
- preserve everything before and after it

Generated content must stay inside the `# Error Catalog` section only.
