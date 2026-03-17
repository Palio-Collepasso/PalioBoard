"""Manual application wiring for the api composition root."""

from dataclasses import dataclass

from palio.db import DatabaseRuntime, build_database_runtime
from palio.modules.audit.facade import AuditFacade, build_audit_facade
from palio.modules.authorization.facade import (
    AuthorizationFacade,
    build_authorization_facade,
)
from palio.modules.event_operations.facade import (
    EventOperationsFacade,
    build_event_operations_facade,
)
from palio.modules.identity.facade import IdentityFacade, build_identity_facade
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
from palio.settings import ApplicationSettings, load_settings


@dataclass(frozen=True, slots=True)
class ModuleFacades:
    """Explicit list of module contracts assembled by the composition root."""

    identity: IdentityFacade
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

    def names(self) -> tuple[str, ...]:
        return (
            self.identity.module_name,
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
class ApplicationRuntime:
    """Top-level runtime assembled without a DI framework."""

    settings: ApplicationSettings
    database: DatabaseRuntime
    modules: ModuleFacades


def build_module_facades() -> ModuleFacades:
    """Assemble module facades explicitly so wiring stays visible."""

    return ModuleFacades(
        identity=build_identity_facade(),
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


def build_runtime() -> ApplicationRuntime:
    """Build the minimal api runtime used by the scaffold."""

    settings = load_settings()
    return ApplicationRuntime(
        settings=settings,
        database=build_database_runtime(dsn=settings.database.runtime_url),
        modules=build_module_facades(),
    )
