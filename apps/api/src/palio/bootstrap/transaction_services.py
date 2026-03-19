"""Transaction-scoped module services assembled per request or use case."""

from dataclasses import dataclass

from palio.infrastructure.db.transaction import SqlAlchemyTransaction
from palio.modules.audit.facade import AuditFacade, build_audit_facade
from palio.modules.authorization.facade import (
    AuthorizationFacade,
    build_authorization_facade,
)
from palio.modules.event_operations.facade import (
    EventOperationsFacade,
    build_event_operations_facade,
)
from palio.modules.leaderboard_projection.facade import (
    LeaderboardProjectionFacade,
    build_leaderboard_projection_facade,
)
from palio.modules.live_games.facade import LiveGamesFacade, build_live_games_facade
from palio.modules.public_read.facade import PublicReadFacade, build_public_read_facade
from palio.modules.results.facade import ResultsFacade, build_results_facade
from palio.modules.season_setup.facade import (
    SeasonSetupFacade,
    build_season_setup_facade,
)
from palio.modules.tournaments.facade import (
    TournamentsFacade,
    build_tournaments_facade,
)
from palio.modules.users.facade import UsersFacade, build_users_facade

_TRANSACTION_MODULE_NAMES = (
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
_PUBLIC_SURFACE_MODULE_NAMES = ("public_read", "leaderboard_projection")
_REALTIME_SURFACE_MODULE_NAMES = ("live_games", "event_operations")


@dataclass(frozen=True, slots=True)
class TransactionServices:
    """Request-scoped module facades that participate in one transaction."""

    authorization: AuthorizationFacade
    users: UsersFacade
    season_setup: SeasonSetupFacade
    event_operations: EventOperationsFacade
    results: ResultsFacade
    tournaments: TournamentsFacade
    live_games: LiveGamesFacade
    leaderboard_projection: LeaderboardProjectionFacade
    public_read: PublicReadFacade
    audit: AuditFacade

    def module_names(self) -> tuple[str, ...]:
        """Return module names in transaction wiring order."""
        return (
            self.authorization.module_name,
            self.users.module_name,
            self.season_setup.module_name,
            self.event_operations.module_name,
            self.results.module_name,
            self.tournaments.module_name,
            self.live_games.module_name,
            self.leaderboard_projection.module_name,
            self.public_read.module_name,
            self.audit.module_name,
        )


@dataclass(frozen=True, slots=True)
class TransactionServicesFactory:
    """Build transaction-bound services from a request-owned transaction."""

    def create(self, _transaction: SqlAlchemyTransaction) -> TransactionServices:
        """Build one transaction-scoped service graph.

        The active transaction is accepted here even though the current scaffold
        facades are only descriptors. Real module implementations can use the
        request-owned transaction when repositories and adapters are added.
        """
        # Create
        # - SQLAlchemy repositories
        # - SQL read repositories
        # - module infrastructure adapters that need the active session
        # Only infrastructure wiring should access _transaction.session.

        return TransactionServices(
            authorization=build_authorization_facade(),
            users=build_users_facade(),
            season_setup=build_season_setup_facade(),
            event_operations=build_event_operations_facade(),
            results=build_results_facade(),
            tournaments=build_tournaments_facade(),
            live_games=build_live_games_facade(),
            leaderboard_projection=build_leaderboard_projection_facade(),
            public_read=build_public_read_facade(),
            audit=build_audit_facade(),
        )

    def module_names(self) -> tuple[str, ...]:
        """Return the full transaction-scoped module list."""
        return _TRANSACTION_MODULE_NAMES

    def public_surface_module_names(self) -> tuple[str, ...]:
        """Return modules currently exposed by the public surface."""
        return _PUBLIC_SURFACE_MODULE_NAMES

    def realtime_surface_module_names(self) -> tuple[str, ...]:
        """Return modules currently exposed by the realtime surface."""
        return _REALTIME_SURFACE_MODULE_NAMES


def build_transaction_services_factory() -> TransactionServicesFactory:
    """Build the long-lived factory for request-scoped transaction services."""
    return TransactionServicesFactory()
