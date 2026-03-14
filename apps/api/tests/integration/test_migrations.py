import pytest
import psycopg

from tests.support.postgres import (
    APPLICATION_SCHEMA,
    BASELINE_REVISION,
    MigratedPostgresDatabase,
    to_psycopg_conninfo,
)

pytestmark = pytest.mark.integration


def test_real_migrations_create_the_application_schema(
    migrated_postgres_database: MigratedPostgresDatabase,
) -> None:
    with psycopg.connect(
        to_psycopg_conninfo(migrated_postgres_database.runtime_url)
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT schema_name
                FROM information_schema.schemata
                WHERE schema_name = %s
                """,
                (APPLICATION_SCHEMA,),
            )
            assert cursor.fetchone() == (APPLICATION_SCHEMA,)

            cursor.execute("SELECT version_num FROM alembic_version")
            assert cursor.fetchone() == (BASELINE_REVISION,)
