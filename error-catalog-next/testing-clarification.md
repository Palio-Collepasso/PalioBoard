The **generator/tool** and the **API runtime** should not have the exact same test basis, even if they share the same error model.

## What the scenarios are best for

Your scenario pack is mainly the right input for testing:

* catalog validation
* code generation
* docs generation
* deterministic output
* CLI behavior

That is because the scenarios are about:

* YAML structure
* `context_schema`
* codes / statuses / type slugs
* generated artifacts

So they are a very good fit for `tools/error_codegen`.

## What the API should be tested against

The API should be tested against **runtime behavior**, not primarily against catalog files.

Meaning: test the API against:

* raised domain/application exceptions
* FastAPI exception handler behavior
* endpoint behavior
* serialized `application/problem+json` responses

So API tests should answer questions like:

* if `JollyAlreadyUsedError` is raised, do I get a 409?
* is the media type correct?
* are `type`, `code`, `title`, `status`, `context` present?
* is `context` passed through correctly?
* do unexpected exceptions become generic 500s?
* do real endpoints raise the right module-owned exceptions?

## Should the API reuse the scenarios at all?

Yes, but only **selectively**.

A good rule is:

* **tool tests** should iterate broadly over scenario catalogs
* **API tests** should use a **small curated subset** of runtime examples

Because the API is not validating YAML or generating files.
It is testing the runtime mapping layer.

So I would not make all API tests depend on the full scenario tree.

## What I would test the API against

I would split API tests into 3 layers.

### 1. Handler-level tests

These do not need full scenarios.

Test directly with synthetic exceptions:

* one 409 business-rule error
* one 403 authorization error
* one 404 not-found error
* one validation-style 400 error if you expose it that way
* one unknown exception → generic 500

These tests should assert:

* status
* media type
* payload keys
* `context` passthrough

### 2. Endpoint integration tests

These should test real application flows.

For example:

* completing a game with an already-used Jolly returns `JOLLY_ALREADY_USED`
* publishing a locked tournament returns `TOURNAMENT_LOCKED`
* missing capability returns `MISSING_CAPABILITY`

These are more valuable than catalog-driven parametrization, because they verify real wiring.

### 3. Optional catalog-to-runtime consistency test

This is the one place where API tests can reuse catalog-derived data.

A useful test is:

* for a curated list of exported runtime exception classes, assert their attached `error_definition` matches the catalog metadata:

  * `code`
  * `type`
  * `title`
  * `http_status`

This is not an endpoint test. It is a consistency test.

## What I would not do

I would **not** make the API suite iterate over every scenario in `tools/error_codegen/tests/fixtures/scenarios/...`.

Why not:

* it couples API tests to generator test fixtures
* many scenario failures are catalog-shape failures, irrelevant to API runtime
* many scenario success cases are only about generation complexity, not HTTP behavior
* it makes API tests noisy and brittle

## Best practical setup

### Tool side

Use the full scenario tree:

* success/simple
* success/medium
* success/complex
* failure/simple
* failure/medium
* failure/complex

### API side

Use either:

* small local fixtures in `apps/api/tests/...`
* or a tiny shared runtime-example set, not the whole tool scenario tree

For example:

```text
apps/api/tests/fixtures/errors/
  jolly_already_used.json
  missing_capability.json
  tournament_locked.json
```

Or no files at all — just explicit test data inside the tests.

## My recommendation

* **No, the API should not broadly test against all the scenarios**
* the API should test against **runtime exceptions and real endpoint flows**
* you may reuse a **small curated subset** of scenario-derived examples for consistency checks
* the full scenario tree should remain primarily a **tool/generator test asset**

## The simplest rule

Use this rule:

* **catalog scenarios** test “can we define and generate the contract correctly?”
* **API tests** test “do runtime exceptions and endpoints produce the correct contract?”

That is the clean separation.