from palio.modules.event_operations.errors_gen import (
    GameNotInProgressError,
    JollyAlreadyUsedError,
)

from .event_operations_api_problems_gen import (
    GAME_NOT_IN_PROGRESS_API_PROBLEM,
    JOLLY_ALREADY_USED_API_PROBLEM,
)

ERROR_TO_PROBLEM = {
    JollyAlreadyUsedError: JOLLY_ALREADY_USED_API_PROBLEM,
    GameNotInProgressError: GAME_NOT_IN_PROGRESS_API_PROBLEM,
}
