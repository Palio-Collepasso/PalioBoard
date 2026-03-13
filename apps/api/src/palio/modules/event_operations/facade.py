"""Public facade for the event operations module."""

from palio.shared.module_facade import ModuleFacade

EventOperationsFacade = ModuleFacade


def build_event_operations_facade() -> EventOperationsFacade:
    return ModuleFacade(
        module_name="event_operations",
        purpose="Game lifecycle, state transitions, and review flows.",
    )
