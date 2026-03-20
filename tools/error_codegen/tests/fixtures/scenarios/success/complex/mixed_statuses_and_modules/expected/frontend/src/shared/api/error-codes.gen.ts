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

export type GameAlreadyClosedContext = Record<string, never>;

export type TeamNotFoundContext = {
  team_id: string;
};

export type InvalidEntryPayloadContext = {
  field: string;
  reason: string;
};

export const ERROR_CATALOG = {
  MISSING_CAPABILITY: {
    code: "MISSING_CAPABILITY",
    typeUri: "https://api.palioboard.local/problems/missing-capability",
    title: "Missing capability",
    httpStatus: 403,
    translationKey: "errors.missingCapability",
  },
  GAME_ALREADY_CLOSED: {
    code: "GAME_ALREADY_CLOSED",
    typeUri: "https://api.palioboard.local/problems/game-already-closed",
    title: "Game already closed",
    httpStatus: 409,
    translationKey: "errors.gameAlreadyClosed",
  },
  TEAM_NOT_FOUND: {
    code: "TEAM_NOT_FOUND",
    typeUri: "https://api.palioboard.local/problems/team-not-found",
    title: "Team not found",
    httpStatus: 404,
    translationKey: "errors.teamNotFound",
  },
  INVALID_ENTRY_PAYLOAD: {
    code: "INVALID_ENTRY_PAYLOAD",
    typeUri: "https://api.palioboard.local/problems/invalid-entry-payload",
    title: "Invalid entry payload",
    httpStatus: 400,
    translationKey: "errors.invalidEntryPayload",
  },
} as const satisfies Record<string, ApiErrorCatalogEntry>;

export type ErrorCode = keyof typeof ERROR_CATALOG;

export interface ErrorContextByCode {
  MISSING_CAPABILITY: MissingCapabilityContext;
  GAME_ALREADY_CLOSED: GameAlreadyClosedContext;
  TEAM_NOT_FOUND: TeamNotFoundContext;
  INVALID_ENTRY_PAYLOAD: InvalidEntryPayloadContext;
}

export type ErrorContext<TCode extends ErrorCode> = ErrorContextByCode[TCode];
