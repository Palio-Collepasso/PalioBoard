"""Event operations module public surface."""

from palio.modules.event_operations.facade import (
    EventOperationsFacade,
    build_event_operations_facade,
)

__all__ = ["EventOperationsFacade", "build_event_operations_facade"]
