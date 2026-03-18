# UI proposals guide

## Proposal status
All files under `docs/ui/` are **non-authoritative proposals**.
They are starting points for shell/page/component implementation.
They do not override product, domain, architecture, API, testing, or business-rule docs.

## How to use `docs/ui`
1. Read the smallest relevant authoritative doc set first.
2. Read only the relevant UI proposal docs for the task:
   - one shell doc
   - one or two page docs
   - shared primitives if needed
   - tokens/checklist only if needed
3. Verify behavior against authoritative docs before implementation.
4. Change these proposals freely when implementation, business rules, or committed contracts require it.

## Source precedence inside UI work
Use this order:
1. product/domain/architecture/API/testing docs
2. relevant code and committed contracts
3. `docs/ui/*` proposals

If a UI proposal conflicts with a more authoritative doc, the proposal loses.

## What each UI file type is for
- `layouts/*` — shell-level layout and persistent-region proposals
- `pages/*` — route-level proposals
- `components/*` — reusable shared building blocks
- `component_checklist.md` — compact v1 component inventory
- `design_tokens.json` — visual proposal tokens and semantic status mappings

## What `docs/ui` should not do
- define business truth
- define lifecycle semantics
- define capability semantics without verification
- invent API contracts
- force Codex to read unrelated pages/components

## Verify against
For almost every UI task, verify against some subset of:
- `docs/product/functional-requirements.md`
- `docs/product/acceptance-scenarios.md`
- `docs/domain/business-rules.md`
- `docs/domain/er-schema.md`
- `docs/architecture/architecture.md`
- `docs/api/README.md` / `docs/api/openapi.yaml`
