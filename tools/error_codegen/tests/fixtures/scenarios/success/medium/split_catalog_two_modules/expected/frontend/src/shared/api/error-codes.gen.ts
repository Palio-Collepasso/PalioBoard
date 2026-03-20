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

export type GameNotInProgressContext = {
  game_id: string;
  current_state: string;
};

export const ERROR_CATALOG = {
  MISSING_CAPABILITY: {
    code: "MISSING_CAPABILITY",
    typeUri: "https://api.palioboard.local/problems/missing-capability",
    title: "Missing capability",
    httpStatus: 403,
    translationKey: "errors.missingCapability",
  },
  GAME_NOT_IN_PROGRESS: {
    code: "GAME_NOT_IN_PROGRESS",
    typeUri: "https://api.palioboard.local/problems/game-not-in-progress",
    title: "Game not in progress",
    httpStatus: 409,
    translationKey: "errors.gameNotInProgress",
  },
} as const satisfies Record<string, ApiErrorCatalogEntry>;

export type ErrorCode = keyof typeof ERROR_CATALOG;

export interface ErrorContextByCode {
  MISSING_CAPABILITY: MissingCapabilityContext;
  GAME_NOT_IN_PROGRESS: GameNotInProgressContext;
}

export type ErrorContext<TCode extends ErrorCode> = ErrorContextByCode[TCode];
