import pytest
from fastapi import status
from fastapi.testclient import TestClient

from palio.app import create_app
from palio.settings import APPLICATION_ENV_ENV_VAR, RUNTIME_DATABASE_URL_ENV_VAR
from tests.support.postgres import MigratedPostgresDatabase

pytestmark = pytest.mark.integration


def test_app_reports_ready_against_migrated_postgres(
    monkeypatch: pytest.MonkeyPatch,
    migrated_postgres_database: MigratedPostgresDatabase,
) -> None:
    monkeypatch.setenv(APPLICATION_ENV_ENV_VAR, "test")
    monkeypatch.setenv(
        RUNTIME_DATABASE_URL_ENV_VAR,
        migrated_postgres_database.runtime_url,
    )

    with TestClient(create_app()) as client:
        readiness = client.get("/readyz")
        assert readiness.status_code == status.HTTP_200_OK
        assert readiness.json() == {
            "status": "ok",
            "checks": {"database": "ok"},
        }

        health = client.get("/healthz")
        assert health.status_code == status.HTTP_200_OK
        assert health.json()["status"] == "ok"

        version = client.get("/version")
        assert version.status_code == status.HTTP_200_OK
        assert version.json()["environment"] == "test"
