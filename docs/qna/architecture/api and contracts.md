# API and Contracts

## 7. API design and contracts
### 60. What API style is used?
**Decision:** REST with explicit command/query endpoints. The API surface is intent-oriented, not generic CRUD.

### 61. Is the API split into multiple surfaces?
**Decision:** Yes. The api is explicitly split into:
- `/api/admin/...` for authenticated command/query operations
- `/api/public/...` for anonymous read models
- `/realtime/...` for SSE and WebSocket endpoints

### 62. What do public endpoints read from?
**Decision:** Public and maxi-screen endpoints read only from projection/read models, never directly from authoritative write tables.

### 63. How are contracts shared with Angular?
**Decision:** Python owns the OpenAPI schema. TypeScript types are generated from OpenAPI, but Angular data-access services remain hand-written.

### 64. What is the error contract?
**Decision:** Errors use a standardized machine-readable envelope with:
- consistent HTTP status usage
- stable error codes
- structured contextual data
- a request/correlation id
Angular translates error codes and data into user-friendly messages.

### 65. Is the API versioned formally in v1?
**Decision:** No. The API is treated as a first-party internal API evolving together with the frontend.


## 13. Runtime consistency, persistence conventions, and contracts
### 118. How should OpenAPI contracts be managed in the repo?
**Decision:** Commit the OpenAPI spec as a versioned artifact and generate TypeScript types from that file. Do not make the frontend depend on a running api just to regenerate types.

### 119. Should generated TypeScript types be committed?
**Decision:** No. Commit only the OpenAPI spec; regenerate TS types locally or in CI through `make`. That keeps review noise down and makes the spec the single committed contract artifact.
