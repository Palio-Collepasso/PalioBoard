export type ApiErrorCatalogEntry = {
  code: string;
  typeUri: string;
  title: string;
  httpStatus: number;
  translationKey: string;
};

export type JollyAlreadyUsedContext = {
  team_id: string;
  game_id: string;
  previous_game_id: string;
};

export type GameNotInProgressContext = {
  game_id: string;
  current_state: string;
};

export type InvalidPlacementContext = {
  game_id: string;
  team_id: string;
  placement: number;
};

export const ERROR_CATALOG = {
  JOLLY_ALREADY_USED: {
    code: "JOLLY_ALREADY_USED",
    typeUri: "https://api.palioboard.local/problems/jolly-already-used",
    title: "Jolly already used",
    httpStatus: 409,
    translationKey: "errors.jollyAlreadyUsed",
  },
  GAME_NOT_IN_PROGRESS: {
    code: "GAME_NOT_IN_PROGRESS",
    typeUri: "https://api.palioboard.local/problems/game-not-in-progress",
    title: "Game not in progress",
    httpStatus: 409,
    translationKey: "errors.gameNotInProgress",
  },
  INVALID_PLACEMENT: {
    code: "INVALID_PLACEMENT",
    typeUri: "https://api.palioboard.local/problems/invalid-placement",
    title: "Invalid placement",
    httpStatus: 400,
    translationKey: "errors.invalidPlacement",
  },
} as const satisfies Record<string, ApiErrorCatalogEntry>;

export type ErrorCode = keyof typeof ERROR_CATALOG;

export interface ErrorContextByCode {
  JOLLY_ALREADY_USED: JollyAlreadyUsedContext;
  GAME_NOT_IN_PROGRESS: GameNotInProgressContext;
  INVALID_PLACEMENT: InvalidPlacementContext;
}

export type ErrorContext<TCode extends ErrorCode> = ErrorContextByCode[TCode];
