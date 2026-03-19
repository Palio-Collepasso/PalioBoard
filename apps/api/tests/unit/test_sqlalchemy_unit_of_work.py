from typing import cast

from sqlalchemy.orm import Session, sessionmaker

from palio.infrastructure.db.transaction import SqlAlchemyTransaction
from palio.infrastructure.db.unit_of_work import SqlAlchemyUnitOfWork


def test_sqlalchemy_transaction_delegates_commit_and_rollback() -> None:
    events: list[str] = []

    class FakeSession:
        def commit(self) -> None:
            events.append("commit")

        def rollback(self) -> None:
            events.append("rollback")

        def close(self) -> None:
            events.append("close")

    session = cast(Session, FakeSession())
    transaction = SqlAlchemyTransaction(session)

    with transaction:
        transaction.commit()
        transaction.rollback()

    assert events == ["commit", "rollback", "close"]


def test_sqlalchemy_unit_of_work_begin_creates_transaction() -> None:
    events: list[str] = []

    class FakeSession:
        def close(self) -> None:
            events.append("close")

    session = cast(Session, FakeSession())
    unit_of_work = SqlAlchemyUnitOfWork(cast(sessionmaker[Session], lambda: session))

    transaction = unit_of_work.begin()

    assert isinstance(transaction, SqlAlchemyTransaction)

    with transaction:
        assert transaction.session is session

    assert events == ["close"]
