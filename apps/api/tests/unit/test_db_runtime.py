from pathlib import Path
from typing import cast

import pytest
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from palio.bootstrap.db.config import (
    DatabaseConfigurationError,
    require_migration_database_url,
)
from palio.bootstrap.db.runtime import (
    DatabaseNotConfiguredError,
    ReadinessCheck,
    SessionFactory,
    build_database_runtime,
)
from palio.settings import APPLICATION_SCHEMA


def test_build_database_runtime_is_inert_without_runtime_url() -> None:
    runtime = build_database_runtime()

    assert runtime.is_configured is False
    assert runtime.schema == APPLICATION_SCHEMA
    with pytest.raises(DatabaseNotConfiguredError):
        runtime.create_session()


def test_build_database_runtime_uses_postgres_runtime_url() -> None:
    runtime_url = "postgresql+psycopg://palio_runtime:secret@localhost:5432/palio_dev"

    runtime = build_database_runtime(dsn=runtime_url)

    assert runtime.is_configured is True
    assert runtime.dsn == runtime_url
    assert runtime.engine is not None
    assert runtime.engine.dialect.name == "postgresql"
    assert runtime.engine.url.render_as_string(hide_password=False) == runtime_url

    session = runtime.create_session()
    assert isinstance(session, Session)
    assert session.bind is runtime.engine
    session.close()


def test_unit_of_work_opens_a_session_without_connecting() -> None:
    runtime = build_database_runtime(
        dsn="postgresql+psycopg://palio_runtime:secret@localhost:5432/palio_dev"
    )

    with runtime.create_unit_of_work() as unit_of_work:
        assert unit_of_work is not None


def test_database_runtime_reports_not_ready_without_runtime_url() -> None:
    runtime = build_database_runtime()

    assert runtime.check_readiness() == ReadinessCheck(
        is_ready=False,
        reason="database_not_configured",
    )


def test_database_runtime_reports_ready_when_ping_succeeds() -> None:
    class FakeConnection:
        def __enter__(self) -> "FakeConnection":
            return self

        def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
            return None

        def execute(self, statement: object) -> None:
            assert statement is not None

    class FakeEngine:
        def connect(self) -> FakeConnection:
            return FakeConnection()

    runtime = build_database_runtime(
        dsn="postgresql+psycopg://palio_runtime:secret@localhost:5432/palio_dev",
    )
    runtime = runtime.__class__(
        dsn=runtime.dsn,
        schema=runtime.schema,
        engine=cast(Engine, FakeEngine()),
        session_factory=cast(SessionFactory, object()),
    )

    assert runtime.check_readiness() == ReadinessCheck(
        is_ready=True,
        reason="ok",
    )


def test_database_runtime_reports_not_ready_when_ping_fails() -> None:
    class FakeEngine:
        def connect(self) -> object:
            raise RuntimeError("boom")

    runtime = build_database_runtime(
        dsn="postgresql+psycopg://palio_runtime:secret@localhost:5432/palio_dev",
    )
    runtime = runtime.__class__(
        dsn=runtime.dsn,
        schema=runtime.schema,
        engine=cast(Engine, FakeEngine()),
        session_factory=cast(SessionFactory, object()),
    )

    assert runtime.check_readiness() == ReadinessCheck(
        is_ready=False,
        reason="database_unavailable:RuntimeError",
    )


def test_migration_database_url_requires_explicit_configuration() -> None:
    with pytest.raises(DatabaseConfigurationError):
        require_migration_database_url(None)


def test_baseline_revision_creates_palio_board_schema() -> None:
    migration_path = (
        Path(__file__).resolve().parents[2]
        / "migrations"
        / "versions"
        / "20260314_0001_create_palio_board_schema.py"
    )
    migration_text = migration_path.read_text()

    assert 'APPLICATION_SCHEMA = "palio_board"' in migration_text
    assert "CREATE SCHEMA IF NOT EXISTS" in migration_text
