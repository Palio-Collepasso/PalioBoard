from collections.abc import Generator

from palio.bootstrap.app_services import build_app_services
from palio.bootstrap.runtime import ApplicationRuntime
from palio.bootstrap.transaction_services import TransactionServices
from palio.infrastructure.db import (
    build_database_runtime,
    build_sqlalchemy_unit_of_work_factory,
)
from palio.infrastructure.db.transaction import SqlAlchemyTransaction
from palio.settings import load_settings


def build_runtime() -> ApplicationRuntime:
    """Build the process-wide runtime for the API application."""
    settings = load_settings()
    database = build_database_runtime(dsn=settings.database.require_runtime_url())
    uow_factory = build_sqlalchemy_unit_of_work_factory(database=database)
    return ApplicationRuntime(
        settings=settings,
        database=database,
        app=build_app_services(uow_factory=uow_factory),
    )


def open_transaction_services(
    runtime: ApplicationRuntime,
) -> Generator[TransactionServices, None, None]:
    """Open a new transaction for request-scoped services."""
    unit_of_work = runtime.app.uow_factory()
    transaction = unit_of_work.begin()

    if not isinstance(transaction, SqlAlchemyTransaction):
        raise TypeError("TransactionServicesFactory requires a SqlAlchemyTransaction.")

    with transaction:
        yield runtime.app.transaction_services_factory.create(transaction)
