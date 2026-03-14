import pytest

from palio.settings import (
    APPLICATION_ENV_ENV_VAR,
    BUILD_COMMIT_SHA_ENV_VAR,
    BUILD_VERSION_ENV_VAR,
    LOG_LEVEL_ENV_VAR,
    MIGRATION_DATABASE_URL_ENV_VAR,
    REQUEST_ID_HEADER_ENV_VAR,
    RUNTIME_DATABASE_URL_ENV_VAR,
    ApplicationEnvironment,
    LogLevel,
    load_settings,
)


def test_load_settings_reads_typed_runtime_configuration() -> None:
    settings = load_settings(
        {
            APPLICATION_ENV_ENV_VAR: "production",
            LOG_LEVEL_ENV_VAR: "debug",
            REQUEST_ID_HEADER_ENV_VAR: "X-Correlation-ID",
            BUILD_VERSION_ENV_VAR: "1.2.3",
            BUILD_COMMIT_SHA_ENV_VAR: "abc123",
            RUNTIME_DATABASE_URL_ENV_VAR: "postgresql+psycopg://runtime",
            MIGRATION_DATABASE_URL_ENV_VAR: "postgresql+psycopg://migration",
        }
    )

    assert settings.environment is ApplicationEnvironment.PRODUCTION
    assert settings.logging.level is LogLevel.DEBUG
    assert settings.request_context.header_name == "X-Correlation-ID"
    assert settings.build.version == "1.2.3"
    assert settings.build.commit_sha == "abc123"
    assert settings.database.runtime_url == "postgresql+psycopg://runtime"
    assert settings.database.migration_url == "postgresql+psycopg://migration"


def test_load_settings_rejects_invalid_environment_values() -> None:
    with pytest.raises(ValueError):
        load_settings({APPLICATION_ENV_ENV_VAR: "staging"})


def test_load_settings_rejects_invalid_log_levels() -> None:
    with pytest.raises(ValueError):
        load_settings({LOG_LEVEL_ENV_VAR: "verbose"})
