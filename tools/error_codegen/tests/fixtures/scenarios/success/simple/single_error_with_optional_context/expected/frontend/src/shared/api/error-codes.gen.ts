export type ApiErrorCatalogEntry = {
  code: string;
  typeUri: string;
  title: string;
  httpStatus: number;
  translationKey: string;
};

export type TeamNotFoundContext = {
  team_id: string;
  source?: "route" | "body" | "query";
};

export const ERROR_CATALOG = {
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
  TEAM_NOT_FOUND: TeamNotFoundContext;
}

export type ErrorContext<TCode extends ErrorCode> = ErrorContextByCode[TCode];
