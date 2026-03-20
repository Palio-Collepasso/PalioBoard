"""Prototype-only text helpers for generator assertions.

This module is the intended home for reusable pure helpers such as:
- balanced block extraction for generated source text
- ordered-token assertions
- markdown section splitting for docs injection checks

It should stay pure and test-only, and the docs/TypeScript generator tests
should use it instead of duplicating those helpers locally.
"""


def extract_balanced_block(source: str, start_marker: str) -> str:
    """Return the balanced block that starts at ``start_marker``."""
    start = source.index(start_marker)
    brace_start = source.index("{", start)

    depth = 0
    for index in range(brace_start, len(source)):
        character = source[index]
        if character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
            if depth == 0:
                return source[start : index + 1]

    raise AssertionError(f"Unbalanced block starting at {start_marker!r}.")


def assert_tokens_in_order(source: str, tokens: list[str]) -> None:
    """Assert that all tokens appear in the given order."""
    cursor = -1
    for token in tokens:
        position = source.index(token)
        assert position > cursor, token
        cursor = position


def split_markdown_sections(document: str, heading: str) -> tuple[str, str, str]:
    """Split a markdown document into prefix, owned section, and suffix."""
    heading_start = document.index(heading)
    next_heading_index = document.find("\n# ", heading_start + len(heading))
    if next_heading_index == -1:
        next_heading_index = len(document)
    return (
        document[:heading_start],
        document[heading_start:next_heading_index],
        document[next_heading_index:],
    )
