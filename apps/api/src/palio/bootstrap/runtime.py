"""Manual startup wiring for the API composition root."""

from dataclasses import dataclass
from typing import Protocol

from palio.bootstrap.app_services import AppServices
from palio.infrastructure.db import (
    ReadinessCheck,
)
from palio.settings import ApplicationSettings


class RuntimeDatabase(Protocol):
    """Database runtime contract exposed through the application runtime."""

    def check_readiness(self) -> ReadinessCheck:
        """Report whether the runtime database is ready for traffic."""
        ...


@dataclass(frozen=True, slots=True)
class ApplicationRuntime:
    """Top-level runtime assembled once for the process lifetime."""

    settings: ApplicationSettings
    database: RuntimeDatabase
    app: AppServices
