"""Check that backend modules import each other through `facade.py` only."""


import argparse
import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

PACKAGE_PREFIX = ("palio", "modules")
DEFAULT_MODULES_ROOT = Path(__file__).resolve().parents[1] / "modules"


@dataclass(frozen=True, slots=True)
class BoundaryViolation:
    """A forbidden cross-module import discovered by the checker."""

    file: Path
    lineno: int
    import_target: str
    message: str


def check_module_boundaries(modules_root: Path = DEFAULT_MODULES_ROOT) -> list[BoundaryViolation]:
    """Return every forbidden cross-module import under `palio.modules`."""

    violations: list[BoundaryViolation] = []

    for file_path in _iter_python_files(modules_root):
        current_module = file_path.relative_to(modules_root).parts[0]
        package_parts = _package_parts_for_file(file_path, modules_root)
        tree = ast.parse(file_path.read_text(), filename=str(file_path))

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    violations.extend(
                        _check_target(
                            current_module=current_module,
                            file_path=file_path,
                            lineno=node.lineno,
                            target=alias.name,
                        )
                    )
            elif isinstance(node, ast.ImportFrom):
                target = _resolve_import_from(
                    package_parts=package_parts,
                    module=node.module,
                    level=node.level,
                )
                if not target:
                    continue

                violations.extend(
                    _check_target(
                        current_module=current_module,
                        file_path=file_path,
                        lineno=node.lineno,
                        target=target,
                    )
                )

    return violations


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entrypoint for local and CI boundary checks."""

    parser = argparse.ArgumentParser(
        description="Validate that backend modules import each other via facade.py only.",
    )
    parser.add_argument(
        "modules_root",
        nargs="?",
        default=str(DEFAULT_MODULES_ROOT),
        help="Path to the palio/modules directory.",
    )
    args = parser.parse_args(argv)

    modules_root = Path(args.modules_root).resolve()
    violations = check_module_boundaries(modules_root)
    if not violations:
        print("Backend module boundary check passed.")
        return 0

    for violation in violations:
        print(_format_violation(violation))

    return 1


def _iter_python_files(modules_root: Path) -> Iterable[Path]:
    for file_path in sorted(modules_root.rglob("*.py")):
        if "__pycache__" not in file_path.parts:
            yield file_path


def _package_parts_for_file(file_path: Path, modules_root: Path) -> tuple[str, ...]:
    relative_parts = file_path.relative_to(modules_root).with_suffix("").parts
    return PACKAGE_PREFIX + tuple(relative_parts[:-1])


def _resolve_import_from(
    package_parts: tuple[str, ...],
    module: str | None,
    level: int,
) -> str:
    if level == 0:
        return module or ""

    drop_count = max(level - 1, 0)
    anchor_parts = package_parts if drop_count == 0 else package_parts[:-drop_count]
    if module:
        return ".".join(anchor_parts + tuple(module.split(".")))
    return ".".join(anchor_parts)


def _check_target(
    *,
    current_module: str,
    file_path: Path,
    lineno: int,
    target: str,
) -> list[BoundaryViolation]:
    parts = tuple(target.split("."))
    if parts[:2] != PACKAGE_PREFIX or len(parts) < 3:
        return []

    target_module = parts[2]
    if target_module == current_module:
        return []

    if len(parts) == 4 and parts[3] == "facade":
        return []

    return [
        BoundaryViolation(
            file=file_path,
            lineno=lineno,
            import_target=target,
            message="Cross-module imports must target another module's facade.py only.",
        )
    ]


def _format_violation(violation: BoundaryViolation) -> str:
    return (
        f"{violation.file}:{violation.lineno}: "
        f"{violation.message} Found `{violation.import_target}`."
    )


if __name__ == "__main__":
    raise SystemExit(main())
