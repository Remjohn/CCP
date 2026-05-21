"""FR-ERA3-06 - primitive registry API integration tests."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from fastapi.testclient import TestClient

from src.ccp.api.main import app


def _run(func, *args, **kwargs):
    return func(*args, **kwargs)


class TestAC223RouteRegistrationAndLookup:
    def test_known_experience_and_meaning_routes_are_registered(self):
        with TestClient(app) as client:
            experience_response = client.get("/api/primitives/experience/EXP-FBK-001")
            meaning_response = client.get("/api/primitives/meaning/PRM-BUS-001")

        assert experience_response.status_code == 200
        assert experience_response.json()["experience_primitive_id"] == "EXP-FBK-001"
        assert meaning_response.status_code == 200
        assert meaning_response.json()["primitive_id"] == "PRM-BUS-001"

    def test_unknown_primitive_returns_404(self):
        with TestClient(app) as client:
            response = client.get("/api/primitives/experience/EXP-XXX-999")
        assert response.status_code == 404


class TestAC212InvalidateAuth:
    def test_invalidation_rejects_invalid_internal_api_key(self, monkeypatch):
        monkeypatch.setenv("INTERNAL_API_KEY", "secret-123")
        with TestClient(app) as client:
            response = client.post(
                "/api/primitives/invalidate",
                json={"primitive_id": "EXP-FBK-001"},
            )

        assert response.status_code == 403

    def test_invalidation_accepts_valid_internal_api_key(self, monkeypatch):
        monkeypatch.setenv("INTERNAL_API_KEY", "secret-123")
        with TestClient(app) as client:
            response = client.post(
                "/api/primitives/invalidate",
                json={"primitive_id": "EXP-FBK-001"},
                headers={"x-internal-api-key": "secret-123"},
            )

        assert response.status_code == 200
        assert response.json()["deleted_keys"] == 1


class TestAC211HealthPayloadShape:
    def test_health_reports_redis_connectivity_and_counts(self):
        with TestClient(app) as client:
            response = client.get("/api/primitives/health")

        payload = response.json()
        assert response.status_code == 200
        assert payload["total_cached"] >= 243
        assert payload["experience_count"] > 0
        assert payload["meaning_count"] > 0
        assert "redis_connected" in payload

    def test_root_health_exposes_primitive_registry_section(self):
        with TestClient(app) as client:
            response = client.get("/health")

        payload = response.json()
        assert response.status_code == 200
        assert payload["primitive_registry"]["total_cached"] >= 243
