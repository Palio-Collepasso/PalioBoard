"""Shared generator helpers for the error-code generation toolchain."""

import json
from functools import lru_cache
from pathlib import Path
from pprint import pformat
from typing import cast

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from error_codegen.common import display_module_name, pascal_case

TEMPLATE_ROOT = Path(__file__).resolve().parents[1] / "templates"


def python_literal(value: object) -> str:
    """Render a stable Python literal."""
    return pformat(value, sort_dicts=False, width=88)


def json_literal(value: object, *, indent: int = 2) -> str:
    """Render a stable JSON literal."""
    return json.dumps(value, indent=indent)


def render_python_field(name: str, value: object, *, indent: int = 4) -> str:
    """Render one Python keyword argument assignment."""
    literal_lines = python_literal(value).splitlines()
    prefix = " " * indent
    if len(literal_lines) == 1:
        return f"{prefix}{name}={literal_lines[0]},"

    lines = [f"{prefix}{name}={literal_lines[0]}"]
    lines.extend(f"{prefix}{line}" for line in literal_lines[1:-1])
    lines.append(f"{prefix}{literal_lines[-1]},")
    return "\n".join(lines)


def render_name_tuple(names: tuple[str, ...] | list[str]) -> str:
    """Render a Python tuple literal from symbolic names."""
    if not names:
        return ""
    if len(names) == 1:
        return f"{names[0]},"
    return ", ".join(names)


@lru_cache
def template_environment() -> Environment:
    """Return the shared Jinja environment for artifact generators."""
    environment = Environment(
        loader=FileSystemLoader(TEMPLATE_ROOT),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        undefined=StrictUndefined,
    )
    environment.filters["display_module_name"] = display_module_name
    environment.filters["json_literal"] = json_literal
    environment.filters["pascal_case"] = pascal_case
    environment.filters["python_literal"] = python_literal
    globals_map = cast(dict[str, object], environment.globals)
    globals_map["render_name_tuple"] = render_name_tuple
    globals_map["render_python_field"] = render_python_field
    return environment


def render_template(template_name: str, **context: object) -> str:
    """Render one named Jinja template."""
    return template_environment().get_template(template_name).render(**context)
