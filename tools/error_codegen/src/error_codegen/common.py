"""Shared helpers for the error-code generation toolchain."""

import re
from collections.abc import Sequence
from pathlib import Path
from typing import Protocol


class IssueLike(Protocol):
    """Minimal issue surface used by formatter helpers."""

    @property
    def location(self) -> str:
        """Return the issue location."""
        ...

    @property
    def message(self) -> str:
        """Return the issue message."""
        ...


REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_CATALOG_INDEX_PATH = REPOSITORY_ROOT / "docs" / "api" / "errors" / "index.yaml"
DEFAULT_SCHEMA_PATH = REPOSITORY_ROOT / "docs" / "api" / "errors" / "schema.json"
DEFAULT_MODULES_ROOT = REPOSITORY_ROOT / "apps" / "api" / "src" / "palio" / "modules"


def display_path(path: Path) -> str:
    """Render a repository-relative path when possible."""
    try:
        return path.relative_to(REPOSITORY_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def location(path: Path, suffix: str) -> str:
    """Build a stable issue location string."""
    if suffix.startswith("."):
        suffix = suffix[1:]
    if suffix == "<root>":
        return display_path(path)
    if suffix:
        return f"{display_path(path)}:{suffix}"
    return display_path(path)


def sort_issues[T: IssueLike](issues: Sequence[T]) -> list[T]:
    """Return issues sorted by location and message."""
    return sorted(
        issues,
        key=lambda issue: (
            issue.location,
            issue.message,
        ),
    )


def format_issue_message(issues: Sequence[IssueLike]) -> str:
    """Render a multi-line exception message from collected issues."""
    return "\n".join(f"{issue.location}: {issue.message}" for issue in issues)


def display_module_name(module_name: str) -> str:
    """Render a human-readable module label."""
    normalized = re.sub(r"[_-]+", " ", module_name).strip()
    if not normalized:
        return module_name
    return " ".join(part.capitalize() for part in normalized.split())


def pascal_case(value: str) -> str:
    """Convert snake/kebab/space-delimited names to PascalCase."""
    if not re.search(r"[_\-\s]", value):
        return value[:1].upper() + value[1:]

    parts = [part for part in re.split(r"[_\-\s]+", value) if part]
    return "".join(part[:1].upper() + part[1:].lower() for part in parts)


def write_text_artifact(output_path: Path, content: str) -> Path:
    """Write a rendered text artifact and return its resolved path."""
    resolved_output_path = output_path.resolve()
    resolved_output_path.parent.mkdir(parents=True, exist_ok=True)
    resolved_output_path.write_text(content, encoding="utf-8")
    return resolved_output_path
