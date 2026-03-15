# API Error Contract

## Purpose

Define the stable error contract exposed by the API:

- HTTP status usage
- machine-readable error codes
- response payload shape
- field-level validation format
- concurrency/conflict semantics
- authorization/authentication semantics
- retry guidance for clients

## Scope

This document applies to all externally consumed API endpoints.

## Principles

- Error codes are stable and machine-readable once committed here.
- Human-readable messages may evolve without breaking clients.
- Domain conflicts and concurrency conflicts must be distinguishable when the backend starts exposing them.
- Internal implementation details must not leak in API responses.

## Standard Error Envelope

The backend scaffolding completed in `TASK-1` through `TASK-9` has not yet ratified a custom machine-readable application error envelope. Use the structure below as the template for future task-backed error-contract updates.

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

## Field Validation Error Envelope

Use this template when a future task commits stable field-level validation semantics:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Validation failed",
    "details": {
      "fields": [
        {
          "field": "string",
          "reason": "string",
          "code": "string"
        }
      ]
    },
    "request_id": "string"
  }
}
```

## Concurrency / Conflict Error Envelope

Use this template when a future task commits stable optimistic-concurrency or stale-write handling:

```json
{
  "error": {
    "code": "version_conflict",
    "message": "The resource was modified by another user",
    "details": {
      "resource_type": "string",
      "resource_id": "string",
      "current_version": 0,
      "provided_version": 0
    },
    "request_id": "string"
  }
}
```

## Error Code Index

> The records in this section are illustrative examples only. Remove them as soon as the first real task-backed error definition is documented here.

| Error code | HTTP status | Category | Retryable | Notes |
|---|---:|---|---|---|
| `validation_error` | 400 | validation | no | Input is malformed or missing required fields. |
| `unauthenticated` | 401 | auth | maybe | Authentication is missing or invalid. |

---

## Error Definitions

Template for each error definition: `docs/templates/api/error-definition.template.md`

> The record in this section is illustrative only. Remove it as soon as the first real task-backed error definition is documented here.

### `validation_error`

- **Status:** `400`
- **Category:** `validation`
- **Retryable:** `no`
- **Client action:** Correct the request payload and retry.
- **Meaning:** The request payload is malformed, incomplete, or structurally invalid.
- **When returned:**
  - A required field is missing.
  - A field value fails request validation.
- **Must not be used for:**
  - authentication or authorization failures
- **Payload details:**
  - `fields`: optional list of failing fields
  - `request_id`: correlation id for debugging
- **Security/privacy notes:** Validation responses must not leak internal implementation details.
- **Example response:**

```json
{
  "error": {
    "code": "validation_error",
    "message": "Validation failed",
    "details": {
      "fields": []
    },
    "request_id": "req_123"
  }
}
```

- **Related endpoints:**
  - `POST /example`
- **Related domain rules:**
  - none yet

---

## Endpoint-Specific Deviations

Template for each endpoint-specific deviation: `docs/templates/api/endpoint-deviation.template.md`

> Use this section only when an endpoint intentionally deviates from the common contract.

### Current baseline

- **Deviation:** No endpoint-specific deviations are documented yet.
- **Why:** The completed work to date exposes operational and scaffold endpoints, but has not standardized custom business-error handling.
- **Approved by:** Pending a future task that commits the first client-facing error semantics.

---

## Open Questions

- Which first business workflows will define the initial stable machine-readable error codes?
- Will FastAPI default validation responses be wrapped or left as-is when the first custom error contract lands?
