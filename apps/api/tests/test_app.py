import json
from uuid import UUID

from fastapi import status
from fastapi.testclient import TestClient
from loguru import logger

from palio.app import create_app


def test_app_boots_with_placeholder_surfaces() -> None:
    with TestClient(create_app()) as client:
        health = client.get("/healthz")
        assert health.status_code == status.HTTP_200_OK
        assert health.json()["status"] == "ok"
        assert health.headers["X-Request-ID"]
        assert UUID(health.headers["X-Request-ID"]).version == 7

        readiness = client.get("/readyz")
        assert readiness.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert readiness.json() == {
            "status": "not_ready",
            "checks": {"database": "database_not_configured"},
        }

        version = client.get("/version")
        assert version.status_code == status.HTTP_200_OK
        assert version.json() == {
            "app": "palio-api",
            "environment": "development",
            "version": "0.1.0",
        }

        admin = client.get("/api/admin/health")
        assert admin.status_code == status.HTTP_200_OK
        assert admin.json()["surface"] == "admin"
        assert "identity" in admin.json()["modules"]

        public = client.get("/api/public/health")
        assert public.status_code == status.HTTP_200_OK
        assert public.json() == {
            "surface": "public",
            "status": "ok",
            "modules": ["public_read", "leaderboard_projection"],
        }

        realtime = client.get("/realtime/health")
        assert realtime.status_code == status.HTTP_200_OK
        assert realtime.json() == {
            "surface": "realtime",
            "status": "ok",
            "modules": ["live_games", "event_operations"],
        }

        with client.websocket_connect("/realtime/ws") as websocket:
            assert websocket.receive_json() == {
                "surface": "realtime",
                "status": "ready",
            }


def test_request_id_header_is_propagated_and_logged() -> None:
    emitted_messages: list[str] = []

    with TestClient(create_app()) as client:
        sink_id = logger.add(
            lambda message: emitted_messages.append(str(message)),
            serialize=True,
        )
        response = client.get(
            "/healthz",
            headers={"X-Request-ID": "req-123"},
        )
        logger.remove(sink_id)

    assert response.headers["X-Request-ID"] == "req-123"
    request_log = next(
        json.loads(message)
        for message in emitted_messages
        if json.loads(message)["record"]["message"] == "request.completed"
    )
    record = request_log["record"]
    assert record["extra"]["request_id"] == "req-123"
    assert record["extra"]["method"] == "GET"
    assert record["extra"]["path"] == "/healthz"
    assert record["extra"]["status_code"] == status.HTTP_200_OK
    assert record["extra"]["duration_ms"] >= 0


def test_request_logging_uses_loguru_json_payload_shape() -> None:
    emitted_messages: list[str] = []

    with TestClient(create_app()) as client:
        sink_id = logger.add(
            lambda message: emitted_messages.append(str(message)),
            serialize=True,
        )
        client.get("/healthz", headers={"X-Request-ID": "req-123"})
        logger.remove(sink_id)

    payload = next(
        json.loads(message)
        for message in emitted_messages
        if json.loads(message)["record"]["message"] == "request.completed"
    )

    assert payload["record"]["message"] == "request.completed"
    assert payload["record"]["extra"]["request_id"] == "req-123"
    assert payload["record"]["extra"]["method"] == "GET"
    assert payload["record"]["extra"]["path"] == "/healthz"
    assert payload["record"]["extra"]["status_code"] == status.HTTP_200_OK
