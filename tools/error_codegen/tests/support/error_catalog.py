import sys
from importlib import util
from pathlib import Path
from types import ModuleType

REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
ERRORS_DIR = REPOSITORY_ROOT / "docs" / "api" / "errors"
API_SRC_DIR = REPOSITORY_ROOT / "apps" / "api" / "src"
MODULE_NAMES = (
    "audit",
    "authorization",
    "event_operations",
    "identity",
    "leaderboard_projection",
    "live_games",
    "public_read",
    "results",
    "season_setup",
    "tournaments",
    "users",
)
MODULE_IMPORTS = tuple(f"{module_name}.yaml" for module_name in MODULE_NAMES)


def write_catalog(
    tmp_path: Path | None = None,
    *,
    imports: list[str] | tuple[str, ...] = MODULE_IMPORTS,
    fragments: dict[str, str] | None = None,
    base_type_uri: str = "https://example.test/problems/",
    include_all_modules: bool = True,
    output_dir: Path | None = None,
) -> Path:
    base_dir = output_dir or tmp_path
    assert base_dir is not None
    errors_dir = base_dir / "docs" / "api" / "errors"
    errors_dir.mkdir(parents=True, exist_ok=True)

    (errors_dir / "schema.json").write_text(
        (ERRORS_DIR / "schema.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    fragment_sources = fragments or {}
    imported_fragments = tuple(imports)
    index_imports = MODULE_IMPORTS if include_all_modules else imported_fragments

    (errors_dir / "index.yaml").write_text(
        "\n".join(
            [
                "catalog_version: 1",
                "namespace: palioboard",
                f"base_type_uri: {base_type_uri}",
                "schema_dialect: https://json-schema.org/draft/2020-12/schema",
                "default_media_type: application/problem+json",
                "imports:",
                *[f"  - {fragment_name}" for fragment_name in index_imports],
                "shared_context_schemas:",
                "  UuidRef:",
                "    type: string",
                "    format: uuid",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    fragment_names = MODULE_IMPORTS if include_all_modules else imported_fragments
    for fragment_name in fragment_names:
        (errors_dir / fragment_name).write_text(
            fragment_sources.get(fragment_name, "errors: {}\n"),
            encoding="utf-8",
        )

    return errors_dir / "index.yaml"


def fragment_with_error(
    *,
    code: str,
    type_slug: str,
    title: str | None = None,
    description: str | None = None,
    category: str = "conflict",
    recommended_http_status: int = 409,
    retry_policy: str = "never",
    safe_to_expose: bool = True,
    type_uri_override: str | None = None,
) -> str:
    override = ""
    if type_uri_override is not None:
        override = f"    type_uri_override: {type_uri_override}\n"
    description_line = ""
    if description is not None:
        description_line = f"    description: {description}\n"
    return (
        "errors:\n"
        f"  {code}:\n"
        f"    type_slug: {type_slug}\n"
        f"{override}"
        f"    recommended_http_status: {recommended_http_status}\n"
        f"    title: {title or code.replace('_', ' ').title()}\n"
        f"{description_line}"
        f"    category: {category}\n"
        f"    retry_policy: {retry_policy}\n"
        f"    safe_to_expose: {str(safe_to_expose).lower()}\n"
        "    context_schema:\n"
        "      type: object\n"
        "      additionalProperties: false\n"
        "      properties: {}\n"
    )


def load_module_from_path(path: Path, *, module_name: str) -> ModuleType:
    api_src = str(API_SRC_DIR)
    if api_src not in sys.path:
        sys.path.insert(0, api_src)

    spec = util.spec_from_file_location(module_name, path)
    assert spec is not None
    assert spec.loader is not None
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
