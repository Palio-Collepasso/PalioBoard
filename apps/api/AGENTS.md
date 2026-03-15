# API / backend instructions

## Scope
This file applies to backend work under `apps/api/`.

## Core rules
- Keep business logic in Python, not in the frontend, database views, or migrations.
- Preserve the modular-monolith boundaries. Cross-module work should go through public facades and use-case orchestration.
- For schema or behavior changes, update the relevant docs and committed contracts in the same change.

## Python rules
- Do NOT add `from __future__ import annotations` unless strictly necessary.
- Use **modern typing** syntax (PEP 695): define type parameters directly in functions or classes (`def func[T](...) -> T:`). Avoid legacy typing (`TypeVar`, `Generic`, `Optional`, `Dict`, etc.).
- Prefer `Annotated`.
- Prefer `typer` to `argparse`.
- When you change the code, update the related docstring using Google style with typing.
- Use `is` for comparing enum members (including `StrEnum`) when identity is expected; use `==` only when intentional value-level equivalence (e.g., accepting raw strings) is required.
- Prefer `Sequence[T]` to `tuple[T, ...]`

## What to read first
Start from `docs/README.md`, then read the smallest relevant subset of:
- product and functional requirements
- architecture baseline and ADRs
- domain rules and schema docs
- API contract docs
- test strategy and critical E2E flows

## Commands
Prefer repo `make` targets from the repository root when available.

## Required validation by change type
- Pure domain logic: add/update unit tests.
- DB-backed behavior, projections, or transactions: add/update integration tests against real PostgreSQL.
- Live entry or realtime behavior: add/update targeted realtime tests.
- API contract change: update committed OpenAPI and any affected client contract generation workflow.

## Do NOT
- do NOT bypass module boundaries for convenience
- do NOT silently change error codes or API shapes
- do NOT mix unrelated refactors into critical correctness changes
