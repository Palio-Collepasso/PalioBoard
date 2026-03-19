from palio.bootstrap.app_services import build_app_services
from palio.infrastructure.db.runtime import build_database_runtime
from palio.infrastructure.db.transaction import SqlAlchemyTransaction
from palio.infrastructure.db.unit_of_work import build_sqlalchemy_unit_of_work_factory


def test_app_services_expose_identity_and_transaction_module_names() -> None:
    database = build_database_runtime(
        dsn="postgresql+psycopg://palio_runtime:secret@localhost:5432/palio_dev"
    )

    uow_factory = build_sqlalchemy_unit_of_work_factory(database=database)
    app_services = build_app_services(uow_factory=uow_factory)

    assert app_services.identity.module_name == "identity"
    assert callable(app_services.uow_factory)
    assert app_services.module_names() == (
        "identity",
        "authorization",
        "users",
        "season_setup",
        "event_operations",
        "results",
        "tournaments",
        "live_games",
        "leaderboard_projection",
        "public_read",
        "audit",
    )


def test_app_services_build_transaction_services_from_one_uow() -> None:
    database = build_database_runtime(
        dsn="postgresql+psycopg://palio_runtime:secret@localhost:5432/palio_dev"
    )
    app_services = build_app_services(
        uow_factory=build_sqlalchemy_unit_of_work_factory(database=database)
    )
    transaction = app_services.uow_factory().begin()

    assert isinstance(transaction, SqlAlchemyTransaction)

    with transaction:
        transaction_services = app_services.transaction_services_factory.create(
            transaction
        )

    assert transaction_services.module_names() == (
        "authorization",
        "users",
        "season_setup",
        "event_operations",
        "results",
        "tournaments",
        "live_games",
        "leaderboard_projection",
        "public_read",
        "audit",
    )
