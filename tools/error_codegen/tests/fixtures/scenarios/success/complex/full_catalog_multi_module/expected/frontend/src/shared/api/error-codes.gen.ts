export type ApiErrorCatalogEntry = {
  code: string;
  typeUri: string;
  title: string;
  httpStatus: number;
  translationKey: string;
};

export type MissingCapabilityContext = {
  capability: string;
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

export type PlacementConflictContext = {
  game_id: string;
  existing_result: {
      team_id: string;
      placement: number;
    };
  incoming_result: {
      team_id: string;
      placement: number;
    };
};

export type TeamNotFoundContext = {
  team_id: string;
  source?: "route" | "body" | "query";
};

export const ERROR_CATALOG = {
  MISSING_CAPABILITY: {
    code: "MISSING_CAPABILITY",
    typeUri: "https://api.palioboard.local/problems/missing-capability",
    title: "Missing capability",
    httpStatus: 403,
    translationKey: "errors.missingCapability",
  },
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
  PLACEMENT_CONFLICT: {
    code: "PLACEMENT_CONFLICT",
    typeUri: "https://api.palioboard.local/problems/placement-conflict",
    title: "Placement conflict",
    httpStatus: 409,
    translationKey: "errors.placementConflict",
  },
  TEAM_NOT_FOUND: {
    code: "TEAM_NOT_FOUND",
    typeUri: "https://api.palioboard.local/problems/team-not-found",
    title: "Team not found",
    httpStatus: 404,
    translationKey: "errors.teamNotFound",
  },
} as const satisfies Record<string, ApiErrorCatalogEntry>;

export type ErrorCode = keyof typeof ERROR_CATALOG;

export interface ErrorContextByCode {
  MISSING_CAPABILITY: MissingCapabilityContext;
  JOLLY_ALREADY_USED: JollyAlreadyUsedContext;
  GAME_NOT_IN_PROGRESS: GameNotInProgressContext;
  PLACEMENT_CONFLICT: PlacementConflictContext;
  TEAM_NOT_FOUND: TeamNotFoundContext;
}

export type ErrorContext<TCode extends ErrorCode> = ErrorContextByCode[TCode];
