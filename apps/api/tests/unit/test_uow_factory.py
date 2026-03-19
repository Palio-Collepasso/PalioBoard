from palio.infrastructure.db.runtime import build_database_runtime
from palio.infrastructure.db.unit_of_work import (
    SqlAlchemyUnitOfWork,
    SqlAlchemyUnitOfWorkFactory,
    build_sqlalchemy_unit_of_work_factory,
)


def test_sqlalchemy_uow_factory_uses_database_session_factory() -> None:
    database = build_database_runtime(
        dsn="postgresql+psycopg://palio_runtime:secret@localhost:5432/palio_dev"
    )

    uow_factory = build_sqlalchemy_unit_of_work_factory(database=database)

    assert isinstance(uow_factory, SqlAlchemyUnitOfWorkFactory)
    assert uow_factory.session_factory is database.session_factory

    unit_of_work = uow_factory()

    assert isinstance(unit_of_work, SqlAlchemyUnitOfWork)

    with unit_of_work.begin() as transaction:
        assert transaction is not None
