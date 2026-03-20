from pathlib import Path

from support.expectations import (
    RawContextExpectation,
    collect_raw_error_entries,
    expected_codes_by_module,
    expected_context_fields_by_code,
    expected_failure_markers,
    expected_runtime_payloads,
)


def _write_catalog(path: Path) -> Path:
    """Create a tiny split catalog rooted at ``index.yaml`` for helper tests."""
    errors_root = path / "contracts" / "errors"
    errors_root.mkdir(parents=True)
    (errors_root / "index.yaml").write_text(
        "catalog_version: 1\n"
        "namespace: palioboard\n"
        "base_type_uri: https://api.palioboard.local/problems/\n"
        "includes:\n"
        "  - event_operations.yaml\n",
        encoding="utf-8",
    )
    (errors_root / "event_operations.yaml").write_text(
        "module: event_operations\n"
        "errors:\n"
        "  JOLLY_ALREADY_USED:\n"
        "    code: JOLLY_ALREADY_USED\n"
        "    type_slug: jolly-already-used\n"
        "    http_status: 409\n"
        "    title: Jolly already used\n"
        "    translation_key: errors.jollyAlreadyUsed\n"
        "    context_schema:\n"
        "      type: object\n"
        "      additionalProperties: false\n"
        "      properties:\n"
        "        team_id:\n"
        "          type: string\n"
        "        previous_game_id:\n"
        "          type: string\n"
        "      required:\n"
        "        - team_id\n"
        "    example_context:\n"
        "      team_id: team-001\n"
        "      previous_game_id: game-002\n",
        encoding="utf-8",
    )
    return errors_root / "index.yaml"


def test_collect_raw_error_entries_reads_split_catalog(tmp_path: Path) -> None:
    """Raw-entry collection should preserve module ownership and transport metadata."""
    index_path = _write_catalog(tmp_path)

    entries = collect_raw_error_entries(index_path)

    assert len(entries) == 1
    entry = entries[0]
    assert entry.module == "event_operations"
    assert entry.code == "JOLLY_ALREADY_USED"
    assert entry.type_slug == "jolly-already-used"
    assert entry.http_status == 409


def test_expected_runtime_payloads_build_problem_details_payloads(
    tmp_path: Path,
) -> None:
    """Runtime expectations should derive ``type`` from ``base_type_uri`` plus ``type_slug``."""
    index_path = _write_catalog(tmp_path)

    payloads = expected_runtime_payloads(index_path)

    assert payloads == [
        {
            "type": "https://api.palioboard.local/problems/jolly-already-used",
            "code": "JOLLY_ALREADY_USED",
            "title": "Jolly already used",
            "status": 409,
            "context": {"team_id": "team-001", "previous_game_id": "game-002"},
        }
    ]


def test_expected_failure_markers_returns_specific_and_fallback_markers() -> None:
    """Known scenarios should get specific markers; unknown ones should fall back to a generic one."""
    specific = expected_failure_markers("invalid_code_format")
    fallback = expected_failure_markers("brand_new_failure_case")

    assert "UPPER_SNAKE_CASE" in specific
    assert fallback == ["catalog"]


def test_expected_codes_by_module_groups_entries_per_owner(tmp_path: Path) -> None:
    """Code expectations should be grouped and sorted by owning module."""
    index_path = _write_catalog(tmp_path)

    grouped = expected_codes_by_module(index_path)

    assert grouped == {"event_operations": ("JOLLY_ALREADY_USED",)}


def test_expected_context_fields_by_code_extracts_required_and_optional_fields(
    tmp_path: Path,
) -> None:
    """Context expectations should split required and optional fields."""
    index_path = _write_catalog(tmp_path)

    fields = expected_context_fields_by_code(index_path)

    assert fields == {
        "JOLLY_ALREADY_USED": RawContextExpectation(
            required=("team_id",),
            optional=("previous_game_id",),
        )
    }
