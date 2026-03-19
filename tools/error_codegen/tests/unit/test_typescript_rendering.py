from error_codegen.generators.typescript import generate_typescript_error_artifact
from support.sample_catalog import build_sample_catalog


def test_generate_typescript_error_artifact_is_stable_for_same_catalog() -> None:
    catalog = build_sample_catalog()

    assert generate_typescript_error_artifact(
        catalog
    ) == generate_typescript_error_artifact(catalog)


def test_generate_typescript_error_artifact_renders_frontend_helpers() -> None:
    rendered = generate_typescript_error_artifact(build_sample_catalog())

    assert 'export const ERROR_CATALOG_MODULES = [\n  "audit",' in rendered
    assert '  "event_operations",' in rendered
    assert (
        'export const ERROR_CODES = [\n  "JOLLY_ALREADY_USED"\n] as const;' in rendered
    )
    assert "export type JollyAlreadyUsedContext = {" in rendered
    assert '  "team_id": SharedContextUuidRef;' in rendered
    assert (
        "export function getCatalogTranslationKey(code: ErrorCode): string {"
        in rendered
    )
    assert "export function matchesCatalogErrorCode(" in rendered
