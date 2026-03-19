"""Startup-scoped application wiring shared across requests."""

from dataclasses import dataclass

from palio.bootstrap.transaction_services import (
    TransactionServicesFactory,
    build_transaction_services_factory,
)
from palio.modules.identity.facade import IdentityFacade, build_identity_facade
from palio.shared.db.unit_of_work import UnitOfWorkFactory


@dataclass(frozen=True, slots=True)
class AppServices:
    """Long-lived application services assembled once at startup."""

    identity: IdentityFacade
    uow_factory: UnitOfWorkFactory
    transaction_services_factory: TransactionServicesFactory

    def module_names(self) -> tuple[str, ...]:
        """Return the complete app module list exposed by the runtime."""
        return (
            self.identity.module_name,
            *self.transaction_services_factory.module_names(),
        )


def build_app_services(*, uow_factory: UnitOfWorkFactory) -> AppServices:
    """Build startup-scoped services and factories for the application runtime."""
    return AppServices(
        identity=build_identity_facade(),
        uow_factory=uow_factory,
        transaction_services_factory=build_transaction_services_factory(),
    )
