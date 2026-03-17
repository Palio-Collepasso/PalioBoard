"""Alembic environment for the Palio api."""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from palio.db.config import require_migration_database_url
from palio.settings import load_settings

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = None
settings = load_settings()


def _get_x_argument(name: str) -> str | None:
    """Read one Alembic `-x` argument by name.

    Args:
        name: The argument key to read.

    Returns:
        The configured argument value when present.
    """

    return context.get_x_argument(as_dictionary=True).get(name)


def run_migrations_offline() -> None:
    """Run migrations without creating a DB connection."""

    context.configure(
        url=require_migration_database_url(
            settings.database.migration_url,
            explicit_url=_get_x_argument("db_url"),
        ),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        version_table="alembic_version",
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations with a live DB connection."""

    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = require_migration_database_url(
        settings.database.migration_url,
        explicit_url=_get_x_argument("db_url"),
    )
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            version_table="alembic_version",
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
