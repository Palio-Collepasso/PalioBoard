"""Helpers for Postgres-backed backend integration tests."""

from dataclasses import dataclass
from pathlib import Path
import os
import socket
import subprocess
import sys
import time
import uuid

import psycopg
from psycopg import sql
from sqlalchemy.engine import make_url

APPLICATION_SCHEMA = "palio_board"
BASELINE_REVISION = "20260314_0001"
DEFAULT_POSTGRES_IMAGE = "postgres:16-alpine"
DEFAULT_POSTGRES_PASSWORD = "postgres"
DEFAULT_POSTGRES_URL = "postgresql+psycopg://postgres:postgres@127.0.0.1:5432/postgres"
POSTGRES_STARTUP_TIMEOUT_SECONDS = 30.0
TEST_POSTGRES_IMAGE_ENV_VAR = "PALIO_TEST_POSTGRES_IMAGE"
TEST_POSTGRES_URL_ENV_VAR = "PALIO_TEST_POSTGRES_URL"

API_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True, slots=True)
class PostgresServer:
    """Represent the Postgres server used by the integration suite."""

    admin_url: str
    container_id: str | None = None


@dataclass(frozen=True, slots=True)
class MigratedPostgresDatabase:
    """Represent one isolated migrated test database."""

    admin_url: str
    runtime_url: str
    database_name: str


def build_database_url(admin_url: str, database_name: str) -> str:
    """Build a DB URL for one database on the admin server."""

    return make_url(admin_url).set(database=database_name).render_as_string(
        hide_password=False
    )


def to_psycopg_conninfo(database_url: str) -> str:
    """Convert a SQLAlchemy Postgres URL into a psycopg-compatible URL."""

    return make_url(database_url).set(drivername="postgresql").render_as_string(
        hide_password=False
    )


def start_postgres_server() -> PostgresServer:
    """Start or reuse the Postgres server for integration tests."""

    configured_url = os.environ.get(TEST_POSTGRES_URL_ENV_VAR)
    if configured_url is not None:
        wait_for_postgres(configured_url)
        return PostgresServer(admin_url=configured_url)

    host_port = _pick_free_port()
    container_name = f"palio-task-8-postgres-{uuid.uuid4().hex[:8]}"
    image = os.environ.get(TEST_POSTGRES_IMAGE_ENV_VAR, DEFAULT_POSTGRES_IMAGE)
    command = [
        "docker",
        "run",
        "--detach",
        "--rm",
        "--name",
        container_name,
        "--publish",
        f"127.0.0.1:{host_port}:5432",
        "--env",
        f"POSTGRES_PASSWORD={DEFAULT_POSTGRES_PASSWORD}",
        image,
    ]
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip() or "unknown error"
        raise RuntimeError(f"Unable to start the Postgres test container: {message}")

    admin_url = build_database_url(
        DEFAULT_POSTGRES_URL.replace("127.0.0.1:5432", f"127.0.0.1:{host_port}"),
        "postgres",
    )
    wait_for_postgres(admin_url)
    return PostgresServer(
        admin_url=admin_url,
        container_id=completed.stdout.strip(),
    )


def stop_postgres_server(server: PostgresServer) -> None:
    """Stop the disposable Postgres container when the suite ends."""

    if server.container_id is None:
        return

    subprocess.run(
        ["docker", "stop", server.container_id],
        check=False,
        capture_output=True,
        text=True,
    )


def wait_for_postgres(admin_url: str) -> None:
    """Wait until a Postgres server accepts SQL traffic."""

    deadline = time.monotonic() + POSTGRES_STARTUP_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        try:
            with psycopg.connect(
                to_psycopg_conninfo(admin_url),
                autocommit=True,
            ) as connection:
                with connection.cursor() as cursor:
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
    with psycopg.connect(to_psycopg_conninfo(admin_url), autocommit=True) as connection:
        with connection.cursor() as cursor:
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

    with psycopg.connect(
        to_psycopg_conninfo(database.admin_url),
        autocommit=True,
    ) as connection:
        with connection.cursor() as cursor:
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


def _pick_free_port() -> int:
    """Reserve one local TCP port for the disposable Postgres container."""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])
