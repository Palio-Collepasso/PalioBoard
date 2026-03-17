"""Typed runtime settings for the Palio api."""

import os
from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum

from palio import __version__

APPLICATION_SCHEMA = "palio_board"
RUNTIME_DATABASE_URL_ENV_VAR = "PALIO_DB_RUNTIME_URL"
MIGRATION_DATABASE_URL_ENV_VAR = "PALIO_DB_MIGRATION_URL"
APPLICATION_ENV_ENV_VAR = "PALIO_ENV"
LOG_LEVEL_ENV_VAR = "PALIO_LOG_LEVEL"
REQUEST_ID_HEADER_ENV_VAR = "PALIO_REQUEST_ID_HEADER"
BUILD_VERSION_ENV_VAR = "PALIO_BUILD_VERSION"
BUILD_COMMIT_SHA_ENV_VAR = "PALIO_BUILD_COMMIT_SHA"
DEFAULT_REQUEST_ID_HEADER = "X-Request-ID"
DEFAULT_APPLICATION_NAME = "palio-api"
DEFAULT_API_TITLE = "PalioBoard API"


class ApplicationEnvironment(StrEnum):
    """Supported application environments."""

    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


class LogLevel(StrEnum):
    """Supported log levels for application logging."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True, slots=True)
class DatabaseSettings:
    """Database-specific settings loaded from the environment."""

    runtime_url: str | None
    migration_url: str | None
    schema: str = APPLICATION_SCHEMA


@dataclass(frozen=True, slots=True)
class LoggingSettings:
    """Logging-related runtime settings."""

    level: LogLevel


@dataclass(frozen=True, slots=True)
class RequestContextSettings:
    """HTTP request-context runtime settings."""

    header_name: str = DEFAULT_REQUEST_ID_HEADER


@dataclass(frozen=True, slots=True)
class BuildSettings:
    """Build metadata exposed at runtime."""

    version: str = __version__
    commit_sha: str | None = None


@dataclass(frozen=True, slots=True)
class ApplicationSettings:
    """Full application settings model."""

    environment: ApplicationEnvironment
    app_name: str
    api_title: str
    database: DatabaseSettings
    logging: LoggingSettings
    request_context: RequestContextSettings
    build: BuildSettings


def _parse_environment(value: str | None) -> ApplicationEnvironment:
    """Parse the configured application environment.

    Args:
        value: Raw environment value.

    Returns:
        The parsed application environment.

    Raises:
        ValueError: When the configured value is invalid.
    """

    if value is None:
        return ApplicationEnvironment.DEVELOPMENT

    normalized = value.strip().lower()
    aliases = {
        "dev": ApplicationEnvironment.DEVELOPMENT,
        "development": ApplicationEnvironment.DEVELOPMENT,
        "local": ApplicationEnvironment.DEVELOPMENT,
        "prod": ApplicationEnvironment.PRODUCTION,
        "production": ApplicationEnvironment.PRODUCTION,
        "test": ApplicationEnvironment.TEST,
    }
    if normalized not in aliases:
        raise ValueError(
            f"Unsupported {APPLICATION_ENV_ENV_VAR} value {value!r}. "
            "Use development, test, or production."
        )
    return aliases[normalized]


def _parse_log_level(value: str | None) -> LogLevel:
    """Parse the configured application log level.

    Args:
        value: Raw environment value.

    Returns:
        The parsed log level.

    Raises:
        ValueError: When the configured value is invalid.
    """

    if value is None:
        return LogLevel.INFO

    normalized = value.strip().upper()
    try:
        return LogLevel(normalized)
    except ValueError as exc:
        raise ValueError(
            f"Unsupported {LOG_LEVEL_ENV_VAR} value {value!r}. "
            "Use DEBUG, INFO, WARNING, ERROR, or CRITICAL."
        ) from exc


def load_settings(
    environment: Mapping[str, str] | None = None,
) -> ApplicationSettings:
    """Load application settings from environment variables.

    Args:
        environment: Optional environment mapping override for tests.

    Returns:
        The typed application settings object.
    """

    source = environment or os.environ
    request_id_header = (
        source.get(REQUEST_ID_HEADER_ENV_VAR, DEFAULT_REQUEST_ID_HEADER).strip()
        or DEFAULT_REQUEST_ID_HEADER
    )
    return ApplicationSettings(
        environment=_parse_environment(source.get(APPLICATION_ENV_ENV_VAR)),
        app_name=DEFAULT_APPLICATION_NAME,
        api_title=DEFAULT_API_TITLE,
        database=DatabaseSettings(
            runtime_url=source.get(RUNTIME_DATABASE_URL_ENV_VAR),
            migration_url=source.get(MIGRATION_DATABASE_URL_ENV_VAR),
        ),
        logging=LoggingSettings(
            level=_parse_log_level(source.get(LOG_LEVEL_ENV_VAR)),
        ),
        request_context=RequestContextSettings(header_name=request_id_header),
        build=BuildSettings(
            version=source.get(BUILD_VERSION_ENV_VAR, __version__),
            commit_sha=source.get(BUILD_COMMIT_SHA_ENV_VAR),
        ),
    )
