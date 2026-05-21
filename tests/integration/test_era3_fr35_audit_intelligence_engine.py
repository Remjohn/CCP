"""
Integration tests for FR-ERA3-35 Phase-0 Audit Intelligence Engine FastAPI Router.
"""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.ccp.api.phase0_audit import router as phase0_audit_router, reports_db
from src.ccp.models.phase0_intake_models import (
    Phase0ProspectPacket,
    Phase0AuditTargetDescriptor as IntakeTargetDescriptor,
    Phase0CaptionAttachment,
    Phase0AuditTargetContentType
)
from src.ccp.models.phase0_audit_models import (
    AuditTargetContentType,
    AuditIntelligenceReport,
    BridgeTierRecommendation
)


# Define an isolated FastAPI app for router-level contract integration tests
app = FastAPI()
app.include_router(phase0_audit_router, prefix="/api/phase0")


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def target_packet():
    """Returns a realistic Phase-0 Prospect intake packet mock with single image, carousel, and reel targets."""
    prospect_id = "PRSP-INT-300"
    
    # 1. Single Image + Caption
    img_tgt = IntakeTargetDescriptor(
        audit_target_id="AUDT-IMG-99",
        prospect_id=prospect_id,
        content_type=Phase0AuditTargetContentType.SINGLE_IMAGE_CAPTION,
        primary_media_source_ids=[],
        caption_id="CAPT-IMG-99"
    )
    img_cap = Phase0CaptionAttachment(
        caption_id="CAPT-IMG-99",
        prospect_id=prospect_id,
        audit_target_id="AUDT-IMG-99",
        caption_text="Stop lecturing on generic lessons. Show the visceral proof from your client records today.",
        source_kind="manual_entry"
    )

    # 2. Carousel + Caption
    car_tgt = IntakeTargetDescriptor(
        audit_target_id="AUDT-CAR-99",
        prospect_id=prospect_id,
        content_type=Phase0AuditTargetContentType.CAROUSEL_CAPTION,
        primary_media_source_ids=[],
        caption_id="CAPT-CAR-99"
    )
    car_cap = Phase0CaptionAttachment(
        caption_id="CAPT-CAR-99",
        prospect_id=prospect_id,
        audit_target_id="AUDT-CAR-99",
        caption_text="The transformation curve is defined in these five simple frame segments.",
        source_kind="manual_entry"
    )

    # 3. Reel + Caption
    rel_tgt = IntakeTargetDescriptor(
        audit_target_id="AUDT-REL-99",
        prospect_id=prospect_id,
        content_type=Phase0AuditTargetContentType.REEL_CAPTION,
        primary_media_source_ids=[],
        caption_id="CAPT-REL-99"
    )
    rel_cap = Phase0CaptionAttachment(
        caption_id="CAPT-REL-99",
        prospect_id=prospect_id,
        audit_target_id="AUDT-REL-99",
        caption_text="Reaction model format: reacting to standard industry lecture paradigms.",
        source_kind="manual_entry"
    )

    return Phase0ProspectPacket(
        prospect_id=prospect_id,
        display_name="Jean Pierre Beat Cluster",
        coach_id="JP1",
        audit_targets=[img_tgt, car_tgt, rel_tgt],
        captions=[img_cap, car_cap, rel_cap]
    )


def test_generate_audit_direct_single_image(client, target_packet):
    """Verify that posting a direct generate payload returns a correct single-image audit report."""
    payload = {
        "packet": target_packet.model_dump(),
        "audit_target_id": "AUDT-IMG-99",
        "provisional_override": True
    }
    
    response = client.post("/api/phase0/audits/generate-direct", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "report_id" in data
    assert data["prospect_id"] == "PRSP-INT-300"
    assert data["visible_scores"]["humanity"] > 0
    assert data["provisional_upstream_contract"] is True
    
    # Exclusivity validation: SINGLE_IMAGE_CAPTION populated, others null
    assert data["audit_target"]["content_type"] == "single_image_caption"
    assert data["single_image_block"] is not None
    assert data["carousel_block"] is None
    assert data["reel_block"] is None
    
    # Assert receipt ID is logged
    assert len(data["receipt_ids"]) > 0


def test_generate_audit_direct_carousel(client, target_packet):
    """Verify that posting a direct generate payload returns a correct carousel audit report."""
    payload = {
        "packet": target_packet.model_dump(),
        "audit_target_id": "AUDT-CAR-99",
        "provisional_override": True
    }
    
    response = client.post("/api/phase0/audits/generate-direct", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["audit_target"]["content_type"] == "carousel_caption"
    assert data["carousel_block"] is not None
    assert data["single_image_block"] is None
    assert data["reel_block"] is None


def test_generate_audit_direct_reel(client, target_packet):
    """Verify that posting a direct generate payload returns a correct reel audit report with video structure."""
    payload = {
        "packet": target_packet.model_dump(),
        "audit_target_id": "AUDT-REL-99",
        "provisional_override": True
    }
    
    response = client.post("/api/phase0/audits/generate-direct", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["audit_target"]["content_type"] == "reel_caption"
    assert data["reel_block"] is not None
    assert data["reel_block"]["video_structure"]["availability"] == "unavailable"
    assert data["single_image_block"] is None
    assert data["carousel_block"] is None


def test_retrieve_and_extract_payloads(client, target_packet):
    """Verify that a generated report can be retrieved and its PDF/video payloads extracted via REST API."""
    # First generate the report
    payload = {
        "packet": target_packet.model_dump(),
        "audit_target_id": "AUDT-IMG-99",
        "provisional_override": True
    }
    gen_response = client.post("/api/phase0/audits/generate-direct", json=payload)
    assert gen_response.status_code == 200
    report_id = gen_response.json()["report_id"]
    
    # 1. Retrieve the report
    get_response = client.get(f"/api/phase0/audits/{report_id}")
    assert get_response.status_code == 200
    assert get_response.json()["report_id"] == report_id
    
    # 2. Extract PDF Payload
    pdf_response = client.get(f"/api/phase0/audits/{report_id}/pdf-payload")
    assert pdf_response.status_code == 200
    pdf_data = pdf_response.json()
    assert pdf_data["report_id"] == report_id
    assert pdf_data["render_template_key"] == "canonical_pdf_v1"
    assert "breakdown" in pdf_data["sections"][1].lower()

    # 3. Extract Explainer Video Payload
    video_response = client.get(f"/api/phase0/audits/{report_id}/video-payload")
    assert video_response.status_code == 200
    video_data = video_response.json()
    assert video_data["report_id"] == report_id
    assert video_data["render_template_key"] == "explainer_video_v1"
    assert len(video_data["scene_script_blocks"]) == 5
