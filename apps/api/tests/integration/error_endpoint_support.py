"""API-local helpers for the fake endpoint-flow error integration test.

This module keeps the generated error fixture self-contained. It does not rely
on repo-generated error modules, mappings, or specs.
"""

import importlib
import sys
from dataclasses import dataclass
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from palio.shared.errors import ApplicationError
from palio.shared.errors.handlers import register_error_handlers

ENDPOINT_FLOW_ROUTE = "/_tests/errors/endpoint-flow"
PROBLEM_JSON_MEDIA_TYPE = "application/problem+json"


@dataclass(frozen=True, slots=True)
class FakeGeneratedContract:
    """One fake generated error contract used by the endpoint-flow test."""

    domain_error_type: type[ApplicationError]
    problem_spec: object
    mapping: dict[type[ApplicationError], object]
    expected_body: dict[str, object]


@dataclass(frozen=True, slots=True)
class EndpointFlowResponse:
    """Captured HTTP response details for the fake endpoint flow."""

    status_code: int
    content_type: str
    body: dict[str, object]
    text: str
    contract: FakeGeneratedContract


def build_fake_generated_contract(tmp_path: Path) -> FakeGeneratedContract:
    """Create and import one self-contained fake generated error contract."""
    # TODO(TASK-19): Delete this hardcoded fake generated contract once the
    # error-codegen tool can generate the runtime contract needed by this test.
    # This flow should then invoke the tool from the test setup, import the real
    # generated classes/specs/mapping, and exercise the same HTTP assertions.
    modules_root = tmp_path / "generated_error_contract"
    modules_root.mkdir(parents=True, exist_ok=True)

    module_suffix = "".join(
        character if character.isalnum() else "_" for character in tmp_path.name
    )
    errors_module_name = f"test_generated_errors_{module_suffix}"
    specs_module_name = f"test_generated_specs_{module_suffix}"
    mapping_module_name = f"test_generated_mapping_{module_suffix}"

    errors_path = modules_root / f"{errors_module_name}.py"
    specs_path = modules_root / f"{specs_module_name}.py"
    mapping_path = modules_root / f"{mapping_module_name}.py"

    errors_path.write_text(
        """from palio.shared.errors import ApplicationError, ErrorDefinition

JOLLY_ALREADY_USED = ErrorDefinition(
    code="JOLLY_ALREADY_USED",
    module_name="event_operations",
    type_slug="jolly-already-used",
    type_uri="https://api.palioboard.local/problems/jolly-already-used",
    http_status=409,
    title="Jolly already used",
    description=None,
    category="business_rule",
    retry_policy="never",
    safe_to_expose=True,
    translation_key="errors.jollyAlreadyUsed",
    log_level=None,
    severity=None,
    context_schema={
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "team_id": {"type": "string"},
            "game_id": {"type": "string"},
            "previous_game_id": {"type": "string"},
        },
        "required": ["team_id", "game_id"],
    },
    notes_for_operators=None,
)


class JollyAlreadyUsedError(ApplicationError):
    error_definition = JOLLY_ALREADY_USED

    def __init__(self, *, team_id: str, game_id: str, previous_game_id: str) -> None:
        super().__init__(
            context={
                "team_id": team_id,
                "game_id": game_id,
                "previous_game_id": previous_game_id,
            }
        )
""",
        encoding="utf-8",
    )

    specs_path.write_text(
        """from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ApiProblemSpec:
    code: str
    type_uri: str
    title: str
    http_status: int
    translation_key: str


JOLLY_ALREADY_USED_API_PROBLEM = ApiProblemSpec(
    code="JOLLY_ALREADY_USED",
    type_uri="https://api.palioboard.local/problems/jolly-already-used",
    title="Jolly already used",
    http_status=409,
    translation_key="errors.jollyAlreadyUsed",
)
""",
        encoding="utf-8",
    )

    mapping_path.write_text(
        f"""from {errors_module_name} import JollyAlreadyUsedError
from {specs_module_name} import JOLLY_ALREADY_USED_API_PROBLEM

ERROR_TO_PROBLEM = {{
    JollyAlreadyUsedError: JOLLY_ALREADY_USED_API_PROBLEM,
}}
""",
        encoding="utf-8",
    )

    sys.path.insert(0, str(modules_root))
    try:
        errors_module = importlib.import_module(errors_module_name)
        specs_module = importlib.import_module(specs_module_name)
        mapping_module = importlib.import_module(mapping_module_name)
    finally:
        sys.path.remove(str(modules_root))

    domain_error_type = errors_module.JollyAlreadyUsedError
    problem_spec = specs_module.JOLLY_ALREADY_USED_API_PROBLEM
    mapping = mapping_module.ERROR_TO_PROBLEM

    if mapping.get(domain_error_type) is not problem_spec:
        raise AssertionError(
            "The fake generated domain error must resolve to the fake generated "
            "API problem spec."
        )

    return FakeGeneratedContract(
        domain_error_type=domain_error_type,
        problem_spec=problem_spec,
        mapping=mapping,
        expected_body={
            "type": "https://api.palioboard.local/problems/jolly-already-used",
            "code": "JOLLY_ALREADY_USED",
            "title": "Jolly already used",
            "status": 409,
            "context": {
                "team_id": "team-001",
                "game_id": "game-002",
                "previous_game_id": "game-003",
            },
        },
    )


def build_fake_endpoint_app(tmp_path: Path) -> tuple[FastAPI, FakeGeneratedContract]:
    """Build one test-only FastAPI app that raises a fake mapped domain error."""
    contract = build_fake_generated_contract(tmp_path)
    app = FastAPI()
    register_error_handlers(app)

    @app.get(ENDPOINT_FLOW_ROUTE)
    def raise_endpoint_error() -> dict[str, str]:
        raise contract.domain_error_type(
            team_id="team-001",
            game_id="game-002",
            previous_game_id="game-003",
        )

    return app, contract


def invoke_fake_problem_endpoint(tmp_path: Path) -> EndpointFlowResponse:
    """Exercise the fake endpoint through HTTP and capture the response."""
    app, contract = build_fake_endpoint_app(tmp_path)
    response = TestClient(app, raise_server_exceptions=False).get(ENDPOINT_FLOW_ROUTE)
    return EndpointFlowResponse(
        status_code=response.status_code,
        content_type=response.headers.get("content-type", ""),
        body=response.json(),
        text=response.text,
        contract=contract,
    )
