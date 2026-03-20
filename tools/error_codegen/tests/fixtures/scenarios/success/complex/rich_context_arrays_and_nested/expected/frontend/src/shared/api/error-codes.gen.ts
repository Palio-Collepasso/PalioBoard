export type ApiErrorCatalogEntry = {
  code: string;
  typeUri: string;
  title: string;
  httpStatus: number;
  translationKey: string;
};

export type MissingAnyCapabilityContext = {
  required_any: Array<string>;
  granted: Array<string>;
};

export type LiveCycleMismatchContext = {
  game_id: string;
  expected: {
      state: string;
      live_cycle: number;
    };
  actual: {
      state: string;
      live_cycle: number;
    };
};

export const ERROR_CATALOG = {
  MISSING_ANY_CAPABILITY: {
    code: "MISSING_ANY_CAPABILITY",
    typeUri: "https://api.palioboard.local/problems/missing-any-capability",
    title: "Missing any capability",
    httpStatus: 403,
    translationKey: "errors.missingAnyCapability",
  },
  LIVE_CYCLE_MISMATCH: {
    code: "LIVE_CYCLE_MISMATCH",
    typeUri: "https://api.palioboard.local/problems/live-cycle-mismatch",
    title: "Live cycle mismatch",
    httpStatus: 409,
    translationKey: "errors.liveCycleMismatch",
  },
} as const satisfies Record<string, ApiErrorCatalogEntry>;

export type ErrorCode = keyof typeof ERROR_CATALOG;

export interface ErrorContextByCode {
  MISSING_ANY_CAPABILITY: MissingAnyCapabilityContext;
  LIVE_CYCLE_MISMATCH: LiveCycleMismatchContext;
}

export type ErrorContext<TCode extends ErrorCode> = ErrorContextByCode[TCode];
