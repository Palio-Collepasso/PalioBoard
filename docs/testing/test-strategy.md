# Test Strategy

## Purpose
Define the required test depth, ownership, and command surface for changes in this repo.

## Document boundary
This file owns **test policy**.
It does not restate domain rules or act as a second acceptance catalog.
- Domain invariants live in `docs/domain/business-rules.md`.
- Observable product scenarios live in `docs/product/acceptance-scenarios.md`.
- Browser-critical shortlist lives in `docs/testing/critical-e2e-flows.md`.

## Risk model
The highest-risk failures are:
- authoritative result persistence
- standings/projection correctness
- tournament progression and completion timing
- live-edit conflict behavior
- auth/session semantics on protected routes
- migration/deploy mismatches
- contract drift between backend and consumers

## Stable command surface
- repo gates: `make format`, `make format-check`, `make lint`, `make typecheck`, `make check-boundaries`, `make check-openapi`, `make test`, `make build`, `make verify`
- backend unit: `make test-api-unit`
- backend integration: `make test-api-integration`
- web unit/component: `make test-web`
- browser E2E: `make test-e2e`

## Test layers
| Layer | Use for | Owner | Minimum examples |
|---|---|---|---|
| Unit | pure calculations, validation helpers, mappers, small component behavior | feature author | scoring helpers, placement validation helpers |
| Integration | DB-backed workflows, migrations, audit/projection side effects, auth/session semantics | backend author | lifecycle commands, readiness, migration-sensitive flows |
| API contract | committed request/response/status drift | backend author with consumer awareness | OpenAPI export and generated-type compatibility |
| E2E | release-critical browser-visible flows only | web/app owner or full-stack owner | flows listed in `docs/testing/critical-e2e-flows.md` |
| Manual verification | deploy/rollback or operator checks not yet worth permanent automation | change owner | release smoke, rollback confirmation |

## Change-type matrix
| Change type | Unit | Integration | API contract | E2E | Manual |
|---|---|---|---|---|---|
| Pure UI rendering change | required | no | no | optional | no |
| Domain rule change | required | required | maybe | maybe | no |
| Persistence/query/workflow change | maybe | required | maybe | maybe | no |
| Auth/session behavior change | required | required | maybe | maybe | no |
| API shape/status change | maybe | required | required | optional | no |
| Release-critical browser flow change | maybe | required when backend behavior changes | maybe | required | maybe |
| Deploy/infra change | no | maybe | no | no | required |

## Traceability to critical flows
| Critical flow | Minimum protection |
|---|---|
| `E2E-001` same-origin shell smoke | Playwright spec + fixture `FX-002` |

## Required rules
- Use the cheapest honest test that can catch the real risk.
- DB-backed correctness must be proven with real Postgres integration tests, not SQLite substitutes.
- Official state, audit writes, and projection side effects should be tested together when they share one transaction.
- Browser E2E must stay small and only cover release-critical flows.
- Static checks complement behavioral tests; they do not replace them.

## Review checklist
- [ ] The chosen test depth matches the change-type matrix.
- [ ] New or changed critical rules have direct tests.
- [ ] Contract changes updated `docs/api/openapi.yaml` and related consumer flow.
- [ ] Shared fixtures were updated when their assumptions changed.
- [ ] Critical browser flows were updated only when truly release-critical.
