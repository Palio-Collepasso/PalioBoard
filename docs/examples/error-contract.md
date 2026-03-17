# API Error Contract

## Purpose

Define the stable, machine-readable error contract exposed by the PalioBoard API.

This document exists so that:
- api and frontend use the same error vocabulary;
- concurrent-edit and stale-write situations are handled predictably;
- domain-rule violations are distinguishable from transport or authentication failures;
- user-facing messages can be translated from stable api error codes.

## Scope

This applies to all API surfaces that expose PalioBoard business behavior, including:
- admin HTTP APIs;
- public/maxi read APIs where errors are exposed to clients;
- realtime mutation responses for live ranking entry.

## Non-goals

This document does not define:
- frontend wording shown to end users;
- internal exception class names;
- infrastructure-only errors that never cross the API boundary.

## Principles

- Error `code` values are stable and machine-readable.
- Human-readable `message` values may evolve without breaking clients.
- The same business failure must map to the same error code everywhere.
- Validation, authorization, domain, and concurrency failures must be distinguishable.
- Internal stack traces, SQL details, and secrets must never leak to clients.

## Standard envelope

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": {},
    "request_id": "string"
  }
}
```

### Notes

- `code` is the stable identifier used by frontend logic.
- `message` is for operators and users, but is not part of the compatibility contract.
- `details` contains typed structured fields for client recovery.
- `request_id` allows correlation with logs and audit investigation.

## Validation error envelope

```json
{
  "error": {
    "code": "validation_error",
    "message": "Validation failed",
    "details": {
      "fields": [
        {
          "field": "placements[2]",
          "code": "invalid_placement_structure",
          "reason": "Placements must be structurally valid, including explicit ties"
        }
      ]
    },
    "request_id": "req_123"
  }
}
```

## Concurrency and collaboration envelopes

### Version conflict

```json
{
  "error": {
    "code": "version_conflict",
    "message": "The resource was modified by another user",
    "details": {
      "resource_type": "live_game_draft",
      "resource_id": "game_123",
      "provided_version": 7,
      "current_version": 8
    },
    "request_id": "req_123"
  }
}
```

### Field locked

```json
{
  "error": {
    "code": "field_locked",
    "message": "This field is currently being edited by another user",
    "details": {
      "game_id": "game_123",
      "team_id": "team_borgo",
      "field_key": "placement",
      "locked_by_user_id": "user_456",
      "lease_expires_at": "2026-08-15T18:43:12Z"
    },
    "request_id": "req_123"
  }
}
```

## Error code index

| Error code | HTTP status | Category | Retryable | Typical use |
|---|---:|---|---|---|
| `validation_error` | 400 | validation | no | Malformed payload or missing required fields |
| `unauthenticated` | 401 | auth | maybe | No valid login/session/token |
| `forbidden` | 403 | authz | no | User lacks required capability |
| `not_found` | 404 | lookup | no | Target game/user/resource does not exist or is not visible |
| `unprocessable_state_transition` | 422 | domain | no | Requested game transition is not allowed |
| `invalid_placement_structure` | 422 | domain | no | Placements are incomplete or structurally invalid |
| `required_field_missing` | 422 | validation | no | A required configured result field is missing |
| `jolly_not_allowed` | 422 | domain | no | Jolly attempted outside Palio |
| `jolly_already_used` | 409 | domain | no | Team already consumed Jolly in another Palio game |
| `tournament_pairings_incomplete` | 422 | domain | no | 1v1 tournament cannot start without semifinal pairings |
| `version_conflict` | 409 | concurrency | yes | Client wrote stale version |
| `field_locked` | 409 | concurrency | yes | Another editor currently owns the field lease |
| `game_not_in_progress` | 409 | domain | no | Ranking live-draft action attempted outside `in_progress` |
| `pending_admin_review_required` | 409 | domain | no | Workflow blocked until admin resolves review state |
| `under_examination` | 409 | domain | no | Action blocked because the game is suspended |
| `internal_error` | 500 | internal | maybe | Unexpected server failure |

## Category rules

### Validation

Use when the payload itself is incomplete, malformed, or fails simple shape checks.

Typical examples:
- missing required field value;
- wrong type;
- illegal enum value;
- malformed placement list.

### Domain

Use when the payload is well formed, but violates Palio business rules.

Typical examples:
- Jolly used in Prepalio;
- illegal state transition;
- tournament started without pairings.

### Concurrency

Use when the client is valid but stale, or when another editor currently owns a field lease.

Typical examples:
- live ranking save with obsolete revision;
- attempted edit of a locked team/field.

### Authorization

Use `unauthenticated` when identity is missing or invalid. Use `forbidden` when identity is known but capability is missing.

## Error definitions

### `unprocessable_state_transition`

- **Status:** `422`
- **Category:** `domain`
- **Retryable:** `no`
- **Meaning:** The requested game state change is not allowed from the current state.
- **Client action:** Refresh game state and present allowed actions only.
- **When returned:**
  - starting a game already `in_progress`;
  - completing a game still in `draft`;
  - resolving `pending_admin_review` without admin capability.
- **Must not be used for:**
  - malformed payloads;
  - stale live-draft revisions.
- **Payload details:**
  - `game_id`: target game;
  - `from_state`: current state;
  - `requested_to_state`: attempted destination;
  - `allowed_to_states`: valid next states.

### `invalid_placement_structure`

- **Status:** `422`
- **Category:** `domain`
- **Retryable:** `no`
- **Meaning:** The submitted placements do not form a valid official ranking.
- **Client action:** Correct the placements before attempting completion.
- **When returned:**
  - placements do not cover all four teams;
  - explicit tie structure is invalid;
  - duplicate or impossible positions are supplied.
- **Must not be used for:**
  - a missing typed metric field;
  - Jolly violations.

### `jolly_already_used`

- **Status:** `409`
- **Category:** `domain`
- **Retryable:** `no`
- **Meaning:** The selected team already used Jolly in another Palio game.
- **Client action:** Remove Jolly for this team and choose another valid configuration.
- **When returned:**
  - saving or completing a Palio result with a repeated Jolly usage.
- **Payload details:**
  - `team_id`;
  - `current_game_id`;
  - `existing_jolly_game_id`.

### `version_conflict`

- **Status:** `409`
- **Category:** `concurrency`
- **Retryable:** `yes`
- **Meaning:** The client sent a stale live ranking revision.
- **Client action:** Reload the latest server state, show the user that another editor changed the draft, then retry on top of the new version.
- **When returned:**
  - saving live ranking data with an outdated revision number.
- **Payload details:**
  - `provided_version`;
  - `current_version`;
  - `resource_type`.

### `field_locked`

- **Status:** `409`
- **Category:** `concurrency`
- **Retryable:** `yes`
- **Meaning:** Another editor currently owns the field/team lease in a ranking game.
- **Client action:** Inform the user, show who holds the lease if allowed, and offer retry after lease expiry.
- **When returned:**
  - attempting live edit on a team/field already leased by another user.
- **Must not be used for:**
  - generic stale-version conflicts where no active lease exists.

## Endpoint-specific notes

Replace these example route references with the actual OpenAPI paths once finalized.

- Starting a game should be able to return `unprocessable_state_transition` and `tournament_pairings_incomplete`.
- Completing a ranking game should be able to return `invalid_placement_structure`, `required_field_missing`, `jolly_already_used`, and `version_conflict`.
- Saving a live ranking draft should be able to return `field_locked`, `version_conflict`, and `game_not_in_progress`.
- Editing a completed game should be able to return `forbidden`, `pending_admin_review_required`, or `under_examination` when business policy blocks the action.

## Frontend mapping guidance

The frontend should map stable `error.code` values to user-facing language.

Recommended frontend buckets:
- **fix your input**: `validation_error`, `invalid_placement_structure`, `required_field_missing`;
- **you are not allowed**: `unauthenticated`, `forbidden`;
- **the domain rule forbids this**: `jolly_already_used`, `jolly_not_allowed`, `unprocessable_state_transition`;
- **someone else changed this first**: `version_conflict`, `field_locked`.

## Open questions

- Should public/maxi read endpoints expose a distinct `service_degraded` code for temporary realtime outages, or is generic HTTP failure enough for v1?
- Should `pending_admin_review_required` remain a distinct code, or should it collapse into a more generic workflow-blocked domain code?
