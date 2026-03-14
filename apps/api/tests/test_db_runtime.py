from pathlib import Path

import pytest
from sqlalchemy.orm import Session

from palio.db.config import (
    APPLICATION_SCHEMA,
    DatabaseConfigurationError,
    MIGRATION_DATABASE_URL_ENV_VAR,
    RUNTIME_DATABASE_URL_ENV_VAR,
    get_migration_database_url,
)
from palio.db.runtime import DatabaseNotConfiguredError, build_database_runtime


def test_build_database_runtime_is_inert_without_runtime_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(RUNTIME_DATABASE_URL_ENV_VAR, raising=False)

    runtime = build_database_runtime()

    assert runtime.is_configured is False
    assert runtime.schema == APPLICATION_SCHEMA
    with pytest.raises(DatabaseNotConfiguredError):
        runtime.create_session()


def test_build_database_runtime_uses_postgres_runtime_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime_url = "postgresql+psycopg://palio_runtime:secret@localhost:5432/palio_dev"
    monkeypatch.setenv(RUNTIME_DATABASE_URL_ENV_VAR, runtime_url)

    runtime = build_database_runtime()

    assert runtime.is_configured is True
    assert runtime.dsn == runtime_url
    assert runtime.engine is not None
    assert runtime.engine.dialect.name == "postgresql"
    assert runtime.engine.url.render_as_string(hide_password=False) == runtime_url

    session = runtime.create_session()
    assert isinstance(session, Session)
    assert session.bind is runtime.engine
    session.close()


def test_unit_of_work_opens_a_session_without_connecting(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        RUNTIME_DATABASE_URL_ENV_VAR,
        "postgresql+psycopg://palio_runtime:secret@localhost:5432/palio_dev",
    )
    runtime = build_database_runtime()

    with runtime.create_unit_of_work() as unit_of_work:
        assert unit_of_work.session is not None
        assert unit_of_work.session.bind is runtime.engine


def test_migration_database_url_requires_explicit_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(MIGRATION_DATABASE_URL_ENV_VAR, raising=False)

    with pytest.raises(DatabaseConfigurationError):
        get_migration_database_url()


def test_baseline_revision_creates_palio_board_schema() -> None:
    migration_path = (
        Path(__file__).resolve().parents[1]
        / "migrations"
        / "versions"
        / "20260314_0001_create_palio_board_schema.py"
    )
    migration_text = migration_path.read_text()

    assert 'APPLICATION_SCHEMA = "palio_board"' in migration_text
    assert "CREATE SCHEMA IF NOT EXISTS" in migration_text
