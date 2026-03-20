export type ApiErrorCatalogEntry = {
  code: string;
  typeUri: string;
  title: string;
  httpStatus: number;
  translationKey: string;
};

export type GameAlreadyClosedContext = Record<string, never>;

export const ERROR_CATALOG = {
  GAME_ALREADY_CLOSED: {
    code: "GAME_ALREADY_CLOSED",
    typeUri: "https://api.palioboard.local/problems/game-already-closed",
    title: "Game already closed",
    httpStatus: 409,
    translationKey: "errors.gameAlreadyClosed",
  },
} as const satisfies Record<string, ApiErrorCatalogEntry>;

export type ErrorCode = keyof typeof ERROR_CATALOG;

export interface ErrorContextByCode {
  GAME_ALREADY_CLOSED: GameAlreadyClosedContext;
}

export type ErrorContext<TCode extends ErrorCode> = ErrorContextByCode[TCode];
