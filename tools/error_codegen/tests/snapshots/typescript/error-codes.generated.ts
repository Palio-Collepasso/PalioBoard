/**
 * Generated from docs/api/errors/index.yaml and imported module fragments.
 * Frontend-owned templates should render messages from stable `code + context`.
 * Do not edit by hand.
 */

// Module order follows the committed catalog imports.
export const ERROR_CATALOG_MODULES = [
  "audit",
  "authorization",
  "event_operations",
  "identity",
  "leaderboard_projection",
  "live_games",
  "public_read",
  "results",
  "season_setup",
  "tournaments",
  "users"
] as const;

export type ErrorCatalogModuleName = (typeof ERROR_CATALOG_MODULES)[number];

export const ERROR_CODES = [
  "JOLLY_ALREADY_USED"
] as const;

export type ErrorCode = (typeof ERROR_CODES)[number];

export type RetryPolicy =
  | "never"
  | "immediate"
  | "after_refresh"
  | "after_reauth"
  | "after_delay";

export type LogLevel =
  | "DEBUG"
  | "INFO"
  | "WARNING"
  | "ERROR"
  | "CRITICAL";

export type ErrorSeverity =
  | "low"
  | "medium"
  | "high"
  | "critical";

export interface CatalogProblem<
  Code extends ErrorCode = ErrorCode,
  Context = unknown,
> {
  type: string;
  code: Code;
  status: number;
  title: string;
  context: Context;
}

export interface CatalogErrorMetadata<Code extends ErrorCode = ErrorCode> {
  moduleName: ErrorCatalogModuleName;
  code: Code;
  type: string;
  status: number;
  title: string;
  category: string;
  retryPolicy: RetryPolicy;
  safeToExpose: boolean;
  translationKey: string;
  description?: string;
  logLevel?: LogLevel;
  severity?: ErrorSeverity;
  contextSchema: unknown;
}

export type SharedContextUuidRef = string;

export type JollyAlreadyUsedContext = {
  "game_id": SharedContextUuidRef;
  "previous_game_id"?: SharedContextUuidRef;
  "team_id": SharedContextUuidRef;
};

export interface ErrorContextByCode {
  JOLLY_ALREADY_USED: JollyAlreadyUsedContext;
}

export interface ErrorMetadataByCode {
  JOLLY_ALREADY_USED: CatalogErrorMetadata<"JOLLY_ALREADY_USED">;
}

export const ERROR_METADATA_BY_CODE = {
  "JOLLY_ALREADY_USED": {
  "category": "business_rule",
  "code": "JOLLY_ALREADY_USED",
  "contextSchema": {
    "additionalProperties": false,
    "properties": {
      "game_id": {
        "$ref": "#/shared_context_schemas/UuidRef",
        "description": "Current game being saved"
      },
      "previous_game_id": {
        "$ref": "#/shared_context_schemas/UuidRef",
        "description": "Earlier game where the Jolly was already used"
      },
      "team_id": {
        "$ref": "#/shared_context_schemas/UuidRef",
        "description": "Team using the Jolly"
      }
    },
    "required": [
      "team_id",
      "game_id"
    ],
    "type": "object"
  },
  "description": "The selected team has already consumed its Jolly in a previous game, so the current result cannot be accepted as submitted.\n",
  "moduleName": "event_operations",
  "retryPolicy": "never",
  "safeToExpose": true,
  "status": 409,
  "title": "Jolly already used",
  "translationKey": "errors.jollyAlreadyUsed",
  "type": "https://api.palioboard.local/problems/jolly-already-used"
},
} as const satisfies Record<ErrorCode, CatalogErrorMetadata>;

export const ERROR_CODES_BY_MODULE = {
  "audit": [],
  "authorization": [],
  "event_operations": [
  "JOLLY_ALREADY_USED"
],
  "identity": [],
  "leaderboard_projection": [],
  "live_games": [],
  "public_read": [],
  "results": [],
  "season_setup": [],
  "tournaments": [],
  "users": [],
} as const satisfies Record<ErrorCatalogModuleName, readonly ErrorCode[]>;

const ERROR_CODE_SET = new Set<string>(ERROR_CODES as readonly string[]);

export function isCatalogErrorCode(code: string): code is ErrorCode {
  return ERROR_CODE_SET.has(code);
}

export function getCatalogErrorMetadata(
  code: ErrorCode,
): ErrorMetadataByCode[ErrorCode] {
  return ERROR_METADATA_BY_CODE[code];
}

export function getCatalogTranslationKey(code: ErrorCode): string {
  return getCatalogErrorMetadata(code).translationKey;
}

export function matchesCatalogErrorCode(
  problem: Pick<CatalogProblem, "code"> | null | undefined,
  code: ErrorCode,
): boolean {
  return Boolean(problem && problem.code === code);
}

export function isCatalogProblem(value: unknown): value is CatalogProblem {
  if (!value || typeof value !== "object") {
    return false;
  }

  const record = value as Record<string, unknown>;
  const code = record["code"];
  return (
    typeof record["type"] === "string" &&
    typeof code === "string" &&
    isCatalogErrorCode(code) &&
    typeof record["title"] === "string" &&
    typeof record["status"] === "number" &&
    "context" in record
  );
}

export type CatalogProblemByCode = {
  JOLLY_ALREADY_USED: CatalogProblem<"JOLLY_ALREADY_USED", {
  "game_id": SharedContextUuidRef;
  "previous_game_id"?: SharedContextUuidRef;
  "team_id": SharedContextUuidRef;
}>;
};

export type CatalogErrorContextByCode = ErrorContextByCode;
