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

export const ERROR_CATALOG = {
  JOLLY_ALREADY_USED: {
    code: "JOLLY_ALREADY_USED",
    typeUri: "https://api.palioboard.local/problems/jolly-already-used",
    title: "Jolly already used",
    httpStatus: 409,
    translationKey: "errors.jollyAlreadyUsed",
  },
} as const satisfies Record<string, ApiErrorCatalogEntry>;

export type ErrorCode = keyof typeof ERROR_CATALOG;

export interface ErrorContextByCode {
  JOLLY_ALREADY_USED: JollyAlreadyUsedContext;
}

export type ErrorContext<TCode extends ErrorCode> = ErrorContextByCode[TCode];
