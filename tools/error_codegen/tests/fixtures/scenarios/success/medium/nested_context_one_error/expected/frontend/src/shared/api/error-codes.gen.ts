export type ApiErrorCatalogEntry = {
  code: string;
  typeUri: string;
  title: string;
  httpStatus: number;
  translationKey: string;
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

export const ERROR_CATALOG = {
  PLACEMENT_CONFLICT: {
    code: "PLACEMENT_CONFLICT",
    typeUri: "https://api.palioboard.local/problems/placement-conflict",
    title: "Placement conflict",
    httpStatus: 409,
    translationKey: "errors.placementConflict",
  },
} as const satisfies Record<string, ApiErrorCatalogEntry>;

export type ErrorCode = keyof typeof ERROR_CATALOG;

export interface ErrorContextByCode {
  PLACEMENT_CONFLICT: PlacementConflictContext;
}

export type ErrorContext<TCode extends ErrorCode> = ErrorContextByCode[TCode];
