"""FastAPI dependencies for request-scoped application services."""

from collections.abc import Generator
from typing import cast

from fastapi import Depends, Request

from palio.bootstrap.runtime import ApplicationRuntime
from palio.bootstrap.transaction_services import (
    TransactionServices,
)
from palio.bootstrap.wiring import open_transaction_services


def get_runtime(request: Request) -> ApplicationRuntime:
    """Return the startup-scoped application runtime stored on the app."""
    return cast(ApplicationRuntime, request.app.state.runtime)


def get_transaction_services(
    runtime: ApplicationRuntime = Depends(get_runtime),  # noqa: B008
) -> Generator[TransactionServices, None, None]:
    """Build one transaction-scoped service graph for the current request."""
    yield from open_transaction_services(runtime)
