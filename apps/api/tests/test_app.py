from fastapi.testclient import TestClient

from palio.app import create_app


def test_app_boots_with_placeholder_surfaces() -> None:
    with TestClient(create_app()) as client:
        health = client.get("/healthz")
        assert health.status_code == 200
        assert health.json()["status"] == "ok"

        admin = client.get("/api/admin/health")
        assert admin.status_code == 200
        assert admin.json()["surface"] == "admin"
        assert "identity" in admin.json()["modules"]

        public = client.get("/api/public/health")
        assert public.status_code == 200
        assert public.json() == {
            "surface": "public",
            "status": "ok",
            "modules": ["public_read", "leaderboard_projection"],
        }

        realtime = client.get("/realtime/health")
        assert realtime.status_code == 200
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
