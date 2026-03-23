"""
Canvas API Router — Integration Tests
======================================
Tests for the FastAPI canvas_api router endpoints.
Uses TestClient against the main app.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from src.ccp.api.main import app
from src.ccp.api.canvas_api import _SERVICE_CACHE
from src.ccp.services.canvas_composition_service import register_template, get_template

client = TestClient(app)

_TPL_ID = "TPL-CAROUSEL-DOPAMINE-CLIFF-003"
_COACH = "TST"
_DIMS = {"width_px": 1080, "height_px": 1350, "aspect_ratio": "4:5"}
_HB = {
    "visible": True,
    "coach_name": "Jean Pierre",
    "coach_handle": "@jeanpierre.coaching",
    "profile_picture_url": "https://r2.ccf-assets.com/coach/jp-profile.jpg",
    "logo_url": "https://r2.ccf-assets.com/coach/jp-logo.png",
}


# ═══════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════


def _ensure_template() -> None:
    if get_template(_TPL_ID) is None:
        register_template(_TPL_ID, {
            "zones": ["identity", "hook", "body", "action", "image"],
            "dimensions": _DIMS,
        })


def _create_composition(
    slide_count: int = 4,
    coach: str = _COACH,
    template_id: str = _TPL_ID,
) -> dict:
    _ensure_template()
    resp = client.post("/api/canvas/compositions", json={
        "coach_acronym": coach,
        "vcb_id": "VCB-TST-20260320-001",
        "template_id": template_id,
        "slide_count": slide_count,
        "dimensions": _DIMS,
        "handle_bar": _HB,
    })
    assert resp.status_code == 201, resp.text
    return resp.json()


def _populate_all_slots(composition_id: str, slide_count: int = 4) -> dict:
    last = None
    for i in range(slide_count):
        resp = client.post(f"/api/canvas/compositions/{composition_id}/assets", json={
            "coach_acronym": _COACH,
            "slide_index": i,
            "image_url": f"https://r2.example.com/slide_{i}.png",
            "image_source": "runninghub_tier_3",
        })
        assert resp.status_code == 200, resp.text
        last = resp.json()
    return last


@pytest.fixture(autouse=True)
def _clear_service_cache():
    """Ensure clean state per test."""
    _SERVICE_CACHE.clear()
    yield
    _SERVICE_CACHE.clear()


# ═══════════════════════════════════════════════════════════════════════
# Tests — Create Composition
# ═══════════════════════════════════════════════════════════════════════


class TestCreateComposition:

    def test_create_returns_201(self):
        data = _create_composition()
        assert data["status"] == "ASSEMBLING"
        assert data["slide_count"] == 4
        assert data["coach_acronym"] == _COACH

    def test_create_composition_id_format(self):
        data = _create_composition()
        assert data["composition_id"].startswith("COMP-TST-")

    def test_create_with_text_content(self):
        _ensure_template()
        resp = client.post("/api/canvas/compositions", json={
            "coach_acronym": _COACH,
            "vcb_id": "VCB-TST-20260320-002",
            "template_id": _TPL_ID,
            "slide_count": 2,
            "dimensions": _DIMS,
            "handle_bar": _HB,
            "text_content": {"0": {"hook": "Hello world"}},
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["slots"][0]["text_populated"] is True

    def test_create_invalid_template_404(self):
        resp = client.post("/api/canvas/compositions", json={
            "coach_acronym": _COACH,
            "vcb_id": "VCB-TST-20260320-003",
            "template_id": "NONEXISTENT",
            "slide_count": 2,
            "dimensions": _DIMS,
            "handle_bar": _HB,
        })
        assert resp.status_code == 404
        assert "TEMPLATE_NOT_FOUND" in resp.json()["detail"]

    def test_create_invalid_coach_acronym(self):
        resp = client.post("/api/canvas/compositions", json={
            "coach_acronym": "X",
            "vcb_id": "VCB-X-20260320-001",
            "template_id": _TPL_ID,
            "slide_count": 2,
            "dimensions": _DIMS,
            "handle_bar": _HB,
        })
        # Pydantic validation error for min_length
        assert resp.status_code == 422

    def test_create_xss_sanitised(self):
        _ensure_template()
        resp = client.post("/api/canvas/compositions", json={
            "coach_acronym": _COACH,
            "vcb_id": "VCB-TST-20260320-004",
            "template_id": _TPL_ID,
            "slide_count": 2,
            "dimensions": _DIMS,
            "handle_bar": {
                "visible": True,
                "coach_name": "<script>alert('xss')</script>Clean Name",
                "coach_handle": "@handle",
            },
        })
        assert resp.status_code == 201
        data = resp.json()
        assert "<script>" not in data["handle_bar"]["coach_name"]
        assert "Clean Name" in data["handle_bar"]["coach_name"]


# ═══════════════════════════════════════════════════════════════════════
# Tests — Get Composition
# ═══════════════════════════════════════════════════════════════════════


class TestGetComposition:

    def test_get_existing(self):
        created = _create_composition()
        cid = created["composition_id"]
        resp = client.get(f"/api/canvas/compositions/{cid}", params={"coach_acronym": _COACH})
        assert resp.status_code == 200
        assert resp.json()["composition_id"] == cid

    def test_get_not_found_404(self):
        # Need a service to exist first
        _create_composition()
        resp = client.get(
            "/api/canvas/compositions/COMP-NONEXISTENT",
            params={"coach_acronym": _COACH},
        )
        assert resp.status_code == 404


# ═══════════════════════════════════════════════════════════════════════
# Tests — Receive Asset
# ═══════════════════════════════════════════════════════════════════════


class TestReceiveAsset:

    def test_receive_single_asset(self):
        comp = _create_composition(slide_count=3)
        cid = comp["composition_id"]
        resp = client.post(f"/api/canvas/compositions/{cid}/assets", json={
            "coach_acronym": _COACH,
            "slide_index": 0,
            "image_url": "https://r2.example.com/slide_0.png",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["slots"][0]["image_populated"] is True
        assert data["status"] == "ASSEMBLING"

    def test_all_assets_transitions_to_ready(self):
        comp = _create_composition(slide_count=2)
        cid = comp["composition_id"]
        data = _populate_all_slots(cid, slide_count=2)
        assert data["status"] == "READY_FOR_REVIEW"

    def test_asset_for_unknown_composition_404(self):
        _create_composition()
        resp = client.post("/api/canvas/compositions/COMP-NOPE/assets", json={
            "coach_acronym": _COACH,
            "slide_index": 0,
            "image_url": "https://r2.example.com/slide_0.png",
        })
        assert resp.status_code == 404


# ═══════════════════════════════════════════════════════════════════════
# Tests — Export
# ═══════════════════════════════════════════════════════════════════════


class TestExportComposition:

    def test_export_records_urls(self):
        comp = _create_composition(slide_count=2)
        cid = comp["composition_id"]
        _populate_all_slots(cid, slide_count=2)
        resp = client.post(f"/api/canvas/compositions/{cid}/export", json={
            "coach_acronym": _COACH,
            "slide_urls": ["https://cdn/s0.png", "https://cdn/s1.png"],
            "stitch_url": "https://cdn/stitch.png",
            "zip_url": "https://cdn/archive.zip",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["export_assets"]["individual_slides"]) == 2
        assert data["export_assets"]["horizontal_stitch"] == "https://cdn/stitch.png"
        assert data["export_assets"]["zip_archive"] == "https://cdn/archive.zip"


# ═══════════════════════════════════════════════════════════════════════
# Tests — Approve
# ═══════════════════════════════════════════════════════════════════════


class TestApprove:

    def test_approve_sets_status(self):
        comp = _create_composition(slide_count=2)
        cid = comp["composition_id"]
        _populate_all_slots(cid, slide_count=2)
        resp = client.post(f"/api/canvas/compositions/{cid}/approve", json={
            "coach_acronym": _COACH,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "APPROVED"
        assert data["approval_action"] == "APPROVE_AND_PUBLISH"

    def test_edit_and_approve_sets_status(self):
        comp = _create_composition(slide_count=2)
        cid = comp["composition_id"]
        _populate_all_slots(cid, slide_count=2)
        resp = client.post(f"/api/canvas/compositions/{cid}/edit-approve", json={
            "coach_acronym": _COACH,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "MANUALLY_EDITED_APPROVED"
        assert data["approval_action"] == "EDIT_AND_APPROVE"


# ═══════════════════════════════════════════════════════════════════════
# Tests — Regeneration
# ═══════════════════════════════════════════════════════════════════════


class TestRegenerate:

    def test_regenerate_returns_request_and_composition(self):
        comp = _create_composition(slide_count=3)
        cid = comp["composition_id"]
        _populate_all_slots(cid, slide_count=3)
        resp = client.post(f"/api/canvas/compositions/{cid}/regenerate", json={
            "coach_acronym": _COACH,
            "slide_index": 1,
            "revision_note": "Background too dark, lighten please",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["composition"]["status"] == "REGENERATION_REQUESTED"
        assert data["regeneration_request"]["slide_index"] == 1
        assert data["regeneration_request"]["revision_note"] == "Background too dark, lighten please"

    def test_regenerate_clears_slot(self):
        comp = _create_composition(slide_count=2)
        cid = comp["composition_id"]
        _populate_all_slots(cid, slide_count=2)
        resp = client.post(f"/api/canvas/compositions/{cid}/regenerate", json={
            "coach_acronym": _COACH,
            "slide_index": 0,
            "revision_note": "Redo this slide",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["composition"]["slots"][0]["image_populated"] is False


# ═══════════════════════════════════════════════════════════════════════
# Tests — Templates
# ═══════════════════════════════════════════════════════════════════════


class TestTemplates:

    def test_list_templates(self):
        _ensure_template()
        resp = client.get("/api/canvas/templates")
        assert resp.status_code == 200
        data = resp.json()
        assert "templates" in data
        ids = [t["template_id"] for t in data["templates"]]
        assert _TPL_ID in ids


# ═══════════════════════════════════════════════════════════════════════
# Tests — CORS
# ═══════════════════════════════════════════════════════════════════════


class TestCORS:

    def test_cors_allows_localhost_3000(self):
        resp = client.options(
            "/api/canvas/templates",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert resp.status_code == 200
        assert "access-control-allow-origin" in resp.headers
