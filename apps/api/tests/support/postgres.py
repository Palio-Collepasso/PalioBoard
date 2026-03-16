"""Helpers for Postgres-backed backend integration tests."""

import os
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, cast

import psycopg
import yaml
from psycopg import sql
from sqlalchemy.engine import make_url
from testcontainers.postgres import PostgresContainer

APPLICATION_SCHEMA = "palio_board"
BASELINE_REVISION = "20260314_0001"
POSTGRES_STARTUP_TIMEOUT_SECONDS = 30.0
TEST_POSTGRES_IMAGE_ENV_VAR = "PALIO_TEST_POSTGRES_IMAGE"
TEST_POSTGRES_URL_ENV_VAR = "PALIO_TEST_POSTGRES_URL"

API_ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_ROOT = API_ROOT.parents[1]
LOCAL_STACK_COMPOSE_FILE = REPOSITORY_ROOT / "infra" / "compose" / "docker-compose.yml"


@dataclass(frozen=True, slots=True)
class LocalStackPostgresDefaults:
    """Represent the disposable Postgres defaults shared with the local stack."""

    image: str
    user: str
    password: str
    database: str

    @property
    def admin_url(self) -> str:
        """Build the local admin URL for the shared defaults."""

        return f"postgresql+psycopg://{self.user}:{self.password}@127.0.0.1:5432/{self.database}"


@dataclass(frozen=True, slots=True)
class PostgresServer:
    """Represent the Postgres server used by the integration suite."""

    admin_url: str
    container: Any | None = None


@dataclass(frozen=True, slots=True)
class MigratedPostgresDatabase:
    """Represent one isolated migrated test database."""

    admin_url: str
    runtime_url: str
    database_name: str


def build_database_url(admin_url: str, database_name: str) -> str:
    """Build a DB URL for one database on the admin server."""

    return (
        make_url(admin_url)
        .set(database=database_name)
        .render_as_string(hide_password=False)
    )


def to_psycopg_conninfo(database_url: str) -> str:
    """Convert a SQLAlchemy Postgres URL into a psycopg-compatible URL."""

    return (
        make_url(database_url)
        .set(drivername="postgresql")
        .render_as_string(hide_password=False)
    )


@lru_cache(maxsize=1)
def load_local_stack_postgres_defaults() -> LocalStackPostgresDefaults:
    """Load the disposable test-server defaults from the local Compose stack."""

    specification = _require_mapping(
        yaml.safe_load(LOCAL_STACK_COMPOSE_FILE.read_text(encoding="utf-8")),
        error_message=(
            "The local stack compose file does not define a top-level mapping."
        ),
    )
    services = _require_mapping(
        specification.get("services"),
        error_message=(
            "The local stack compose file does not define a services mapping for tests."
        ),
    )
    db_service = _require_mapping(
        services.get("db"),
        error_message=(
            "The local stack compose file does not define a db service for tests."
        ),
    )
    environment = _require_mapping(
        db_service.get("environment"),
        error_message=(
            "The local stack db service does not define dict-based environment values."
        ),
    )

    image = db_service.get("image")
    if not isinstance(image, str):
        raise RuntimeError("The local stack db service is missing its image setting.")

    required_keys = (
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
    )
    missing_keys = [key for key in required_keys if key not in environment]
    if missing_keys:
        raise RuntimeError(
            "The local stack db service is missing required Postgres "
            "environment values: " + ", ".join(missing_keys)
        )

    return LocalStackPostgresDefaults(
        image=image,
        user=str(environment["POSTGRES_USER"]),
        password=str(environment["POSTGRES_PASSWORD"]),
        database=str(environment["POSTGRES_DB"]),
    )


def start_postgres_server() -> PostgresServer:
    """Start or reuse the Postgres server for integration tests."""

    configured_url = os.environ.get(TEST_POSTGRES_URL_ENV_VAR)
    if configured_url is not None:
        wait_for_postgres(configured_url)
        return PostgresServer(admin_url=configured_url)

    defaults = load_local_stack_postgres_defaults()
    image = os.environ.get(TEST_POSTGRES_IMAGE_ENV_VAR, defaults.image)
    container = PostgresContainer(
        image=image,
        username=defaults.user,
        password=defaults.password,
        dbname=defaults.database,
    )
    try:
        container.start()
    except Exception as exc:
        raise RuntimeError("Unable to start the Postgres test container.") from exc

    admin_url = (
        make_url(container.get_connection_url())
        .set(drivername="postgresql+psycopg")
        .render_as_string(hide_password=False)
    )
    wait_for_postgres(admin_url)
    return PostgresServer(
        admin_url=admin_url,
        container=container,
    )


def stop_postgres_server(server: PostgresServer) -> None:
    """Stop the disposable Postgres container when the suite ends."""

    if server.container is None:
        return

    server.container.stop()


def wait_for_postgres(admin_url: str) -> None:
    """Wait until a Postgres server accepts SQL traffic."""

    deadline = time.monotonic() + POSTGRES_STARTUP_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        try:
            with (
                psycopg.connect(
                    to_psycopg_conninfo(admin_url),
                    autocommit=True,
                ) as connection,
                connection.cursor() as cursor,
            ):
                cursor.execute("SELECT 1")
            return
        except psycopg.OperationalError:
            time.sleep(0.25)

    raise RuntimeError(
        "Timed out while waiting for PostgreSQL to accept connections. "
        f"Last URL attempted: {admin_url!r}"
    )


def create_database(admin_url: str) -> MigratedPostgresDatabase:
    """Create one isolated database for an integration test."""

    database_name = f"palio_test_{uuid.uuid4().hex}"
    with (
        psycopg.connect(to_psycopg_conninfo(admin_url), autocommit=True) as connection,
        connection.cursor() as cursor,
    ):
        cursor.execute(
            sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name))
        )

    return MigratedPostgresDatabase(
        admin_url=admin_url,
        runtime_url=build_database_url(admin_url, database_name),
        database_name=database_name,
    )


def drop_database(database: MigratedPostgresDatabase) -> None:
    """Drop one isolated database after the test finishes."""

    with (
        psycopg.connect(
            to_psycopg_conninfo(database.admin_url),
            autocommit=True,
        ) as connection,
        connection.cursor() as cursor,
    ):
        cursor.execute(
            """
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = %s
                  AND pid <> pg_backend_pid()
                """,
            (database.database_name,),
        )
        cursor.execute(
            sql.SQL("DROP DATABASE IF EXISTS {}").format(
                sql.Identifier(database.database_name)
            )
        )


def apply_migrations(database_url: str) -> None:
    """Apply the real Alembic migrations to one integration database."""

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "alembic",
            "-x",
            f"db_url={database_url}",
            "upgrade",
            "head",
        ],
        cwd=API_ROOT,
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "PALIO_ENV": "test"},
    )
    if completed.returncode == 0:
        return

    message = completed.stderr.strip() or completed.stdout.strip() or "unknown error"
    raise RuntimeError(f"Unable to apply Alembic migrations: {message}")


def _require_mapping(
    value: object,
    *,
    error_message: str,
) -> dict[str, object]:
    """Return a dict-like value or raise a repo-specific runtime error."""

    if not isinstance(value, dict):
        raise RuntimeError(error_message)

    return cast(dict[str, object], value)
