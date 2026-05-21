"""
Integration tests for FR-ERA3-33 Phase-0 Prospect Intake API Router.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from fastapi import FastAPI
from src.ccp.api.phase0_intake import router as phase0_intake_router

app = FastAPI()
app.include_router(phase0_intake_router, prefix="/api/phase0")


@pytest.fixture
def client():
    return TestClient(app)



def test_api_full_intake_cycle(client):
    prospect_id = "prospect-api-test"

    # 1. Create a draft prospect
    create_payload = {
        "prospect_id": prospect_id,
        "display_name": "Audrey CMF Sonic",
        "coach_id": "NDL",
        "campaign_metadata": {"outreach_channel": "telegram"}
    }
    response = client.post("/api/phase0/prospects", json=create_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prospect_id"] == prospect_id
    assert data["display_name"] == "Audrey CMF Sonic"
    assert data["status"] == "draft"

    # 2. Get the created prospect
    response = client.get(f"/api/phase0/prospects/{prospect_id}")
    assert response.status_code == 200
    assert response.json()["prospect_id"] == prospect_id

    # 3. Attach media source
    media_payload = {
        "media_kind": "interview_audio",
        "storage_uri": "r2://phase0/prospect-api-test/interview.mp3",
        "original_filename": "interview.mp3",
        "file_size_bytes": 1024 * 1024 * 12,
        "duration_seconds": 240.5
    }
    response = client.post(f"/api/phase0/prospects/{prospect_id}/media/upload", json=media_payload)
    assert response.status_code == 200
    media_data = response.json()
    assert media_data["media_kind"] == "interview_audio"
    assert media_data["storage_uri"] == "r2://phase0/prospect-api-test/interview.mp3"

    # 4. Attach transcript
    transcript_payload = {
        "source_kind": "inline_text",
        "raw_text": "This is a detailed audio transcript of the client discussing their main pain points.",
        "language_hint": "en"
    }
    response = client.post(f"/api/phase0/prospects/{prospect_id}/transcripts", json=transcript_payload)
    assert response.status_code == 200
    assert response.json()["word_count"] > 0

    # 5. Attach voice DNA source
    voice_dna_payload = {
        "linked_media_source_ids": [media_data["source_id"]],
        "notes": "Clear resonant coaching voice",
        "quality_confidence": 0.98
    }
    response = client.post(f"/api/phase0/prospects/{prospect_id}/voice-dna-sources", json=voice_dna_payload)
    assert response.status_code == 200
    assert response.json()["quality_confidence"] == 0.98

    # 6. Attach voice clone source
    voice_clone_payload = {
        "linked_media_source_ids": [media_data["source_id"]],
        "duration_seconds_total": 240.5,
        "quality_confidence": 0.95,
        "consent_status": "granted"
    }
    response = client.post(f"/api/phase0/prospects/{prospect_id}/voice-clone-sources", json=voice_clone_payload)
    assert response.status_code == 200
    assert response.json()["duration_seconds_total"] == 240.5

    # 7. Attach avatar ref
    avatar_payload = {
        "image_source_ids": [],
        "style_notes": "Sleek professional portrait style"
    }
    response = client.post(f"/api/phase0/prospects/{prospect_id}/avatar-refs", json=avatar_payload)
    assert response.status_code == 200
    assert response.json()["style_notes"] == "Sleek professional portrait style"

    # 8. Set audience profile
    audience_payload = {
        "primary_audience_label": "Agile Leaders",
        "pain_points": ["slow execution", "organizational alignment"],
        "desires": ["high velocity", "clear structure"]
    }
    response = client.post(f"/api/phase0/prospects/{prospect_id}/audience-profile", json=audience_payload)
    assert response.status_code == 200
    assert response.json()["primary_audience_label"] == "Agile Leaders"

    # 9. Attach Guardian BI
    guardian_payload = {
        "market_summary": "High-growth tech founders needing leadership coaching",
        "offer_summary": "Intensive scaling advisory board container"
    }
    response = client.post(f"/api/phase0/prospects/{prospect_id}/guardian-bi", json=guardian_payload)
    assert response.status_code == 200
    assert response.json()["market_summary"] == "High-growth tech founders needing leadership coaching"

    # 10. Create audit target descriptor
    audit_target_payload = {
        "content_type": "carousel_caption",
        "platform_hint": "linkedin",
        "notes": "Diagnose baseline engagement metrics"
    }
    response = client.post(f"/api/phase0/prospects/{prospect_id}/audit-targets", json=audit_target_payload)
    assert response.status_code == 200
    target_data = response.json()
    assert target_data["content_type"] == "carousel_caption"
    assert target_data["platform_hint"] == "linkedin"

    # 11. Attach caption to the audit target
    caption_payload = {
        "caption_text": "Here are 5 lessons on organic outreach...",
        "source_kind": "manual_entry"
    }
    response = client.post(
        f"/api/phase0/prospects/{prospect_id}/audit-targets/{target_data['audit_target_id']}/caption",
        json=caption_payload
    )
    assert response.status_code == 200
    assert response.json()["caption_text"] == "Here are 5 lessons on organic outreach..."

    # 12. Validate readiness
    response = client.post(f"/api/phase0/prospects/{prospect_id}/validate")
    assert response.status_code == 200
    readiness = response.json()
    assert readiness["packet_status"] == "ready_for_phase0"
    assert readiness["delivery_readiness"] == "ready"
    assert len(readiness["blocking_missing_inputs"]) == 0
    assert len(readiness["warning_missing_inputs"]) == 0

    # 13. Emit handoff packet
    response = client.post(f"/api/phase0/prospects/{prospect_id}/handoff")
    assert response.status_code == 200
    final_packet = response.json()
    assert final_packet["status"] == "handed_off"
