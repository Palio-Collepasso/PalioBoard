# Documentation Impact Matrix

Use this matrix during planning and before merge for every non-trivial change.

| Document | Update when the change affects | Notes |
|---|---|---|
| `docs/architecture/architecture.md` | system boundary, source of truth, invariants, lifecycle semantics, write/read model | baseline architecture map only |
| `docs/architecture/module-map.md` | module ownership, package placement, allowed dependencies, table ownership | code-placement guide |
| `docs/architecture/runtime-flows.md` | transaction order, authoritative side effects, post-commit behavior, flow sequencing | high-risk workflow guide |
| `docs/architecture/adr/*` | long-lived architecture direction changed materially | add/update ADR first, then fold into baseline |
| `docs/product/prd.md` | scope, goals, non-goals, users, milestone meaning | product framing only |
| `docs/product/functional-requirements.md` | supported behavior, capabilities, lifecycle support, public/admin feature scope | feature intent |
| `docs/product/acceptance-scenarios.md` | observable workflow outcomes changed | business-facing scenarios |
| `docs/product/roadmap.md` | milestone order or milestone meaning changed | keep concise |
| `docs/domain/business-rules.md` | invariants, scoring rules, trust rules, state semantics, authorization business rules changed | compact normative rule catalog |
| `docs/domain/er-schema.md` | entities, relationships, constraints, authoritative table semantics changed | structural model |
| `docs/domain/game-catalog.md` | seeded per-game setup reference changed | catalog/reference only |
| `docs/domain/capabilities.yaml` | capability vocabulary or ownership changed | machine-readable catalog |
| `docs/domain/palio-context.md` | external-rule summary or event vocabulary changed materially | compact context only |
| `docs/api/README.md` | API entrypoint guidance, stable surfaces, generation workflow changed | human contract guide |
| `docs/api/openapi.yaml` | committed request/response/status contract changed | generated/committed artifact |
| `docs/api/errors/*.yaml` | stable machine-readable API error identity or metadata changed | endpoint-independent error catalog |
| `docs/api/error-contract.md` | commited machine-readable error semantics changed | generated/committed errors only |
| `docs/testing/test-strategy.md` | required test layers, quality gates, change-type matrix, ownership changed | test-depth policy |
| `docs/testing/critical-e2e-flows.md` | browser-critical flows, owners, spec mappings, promotion criteria changed | small automated shortlist |
| `docs/testing/fixtures.md` | shared fixtures, reusable scenario seeds, fixture owners or lifecycle changed | fixture inventory only |
| `docs/ops/local-dev.md` | local setup, canonical commands, env vars, troubleshooting, bootstrap steps changed | developer workflow |
| `docs/ops/deploy.md` | deploy steps, migration order, artifact locations, verification, rollback changed | release procedure |
| `docs/ops/runbook.md` | actionable incident checks, commands, recovery steps changed | executable operator playbooks |
| `docs/qna/open-questions.md` | unresolved question set changed | unresolved only |
| `docs/qna/recently-resolved.md` | a recent clarification was promoted into an authoritative doc | temporary redirect layer |
| `docs/README.md` | doc precedence, routing, or authoritative map changed | entrypoint only |
| `AGENTS.md` / nearest `AGENTS.md` | read order, command surface, doc-precedence, or scope-specific rules changed | agent workflow instructions |

## Rule
If a behavior change touches more than one row, update all affected docs in the same change or explicitly flag why a row was intentionally left unchanged.
Generated documents should not be hand-edited. Regenerate the committed artifact instead.
