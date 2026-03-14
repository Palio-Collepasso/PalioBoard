# Backend rules
These rules apply only to backend.

## Python rules
- Do NOT add `from __future__ import annotations` unless strictly necessary.
- Use **modern typing** syntax (PEP 695): define type parameters directly in functions or classes (`def func[T](...) -> T:`). Avoid legacy typing (`TypeVar`, `Generic`, `Optional`, `Dict`, etc.).
- Prefer `Annotated`.
- Prefer `typer` to `argparse`.
- Whne you change the code, update the related docstring using Google style with typing.
- Use `is` for comparing enum members (including `StrEnum`) when identity is expected; use `==` only when intentional value-level equivalence (e.g., accepting raw strings) is required.
- Prefer `Sequence[T]` to `tuple[T, ...]`