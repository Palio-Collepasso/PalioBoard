from collections.abc import Iterator

import pytest

from tests.support.postgres import (
    MigratedPostgresDatabase,
    PostgresServer,
    apply_migrations,
    create_database,
    drop_database,
    start_postgres_server,
    stop_postgres_server,
)


@pytest.fixture(scope="session")
def postgres_server() -> Iterator[PostgresServer]:
    server = start_postgres_server()
    try:
        yield server
    finally:
        stop_postgres_server(server)


@pytest.fixture()
def migrated_postgres_database(
    postgres_server: PostgresServer,
) -> Iterator[MigratedPostgresDatabase]:
    database = create_database(postgres_server.admin_url)
    try:
        apply_migrations(database.runtime_url)
        yield database
    finally:
        drop_database(database)
