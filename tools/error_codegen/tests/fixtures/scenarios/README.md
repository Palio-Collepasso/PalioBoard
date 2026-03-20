# Scenario pack for revised error-code generation

This pack is organized around self-contained scenarios and aligned with the revised placement guide.

## Structure

- `success/<simple|medium|complex>/<scenario>/`
- `failure/<simple|medium|complex>/<scenario>/`
- `SCENARIO.md`
- `inputs/` → catalog or document fixtures used as test inputs
- `expected/` → generated artifacts or validation reports expected from the revised architecture

## Revised architecture reflected here

The scenarios now assume:

- `contracts/errors/*.yaml` is the single source of truth for stable error identifiers, transport metadata, and `context_schema`
- generated domain errors live under `apps/api/src/palio/modules/<module>/errors_gen.py`
- generated API problem specs and domain-to-problem mappings live under `apps/api/src/palio/api/modules/<module>/errors/`
- frontend generation produces `frontend/src/shared/api/error-codes.gen.ts`
- docs generation produces `docs/api/error-contract.md`
- runtime responses are serialized as `application/problem+json` with a `context` object built from domain error fields
