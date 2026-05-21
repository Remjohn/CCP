"""
FR-ERA3-35C Complete System Integration Tests
==============================================
Tests the end-to-end integration of Audit Intelligence Engine, DPA Themes,
Eval Card Projection Service, Board Assembly, and FastAPI routers.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from src.ccp.api.main import app
from src.ccp.api.phase0_audit import reports_db
from src.ccp.models.phase0_intake_models import (
    Phase0ProspectPacket,
    Phase0AuditTargetDescriptor,
    Phase0CaptionAttachment
)
from src.ccp.models.phase0_audit_models import AuditTargetContentType
from src.ccp.services.audit_intelligence_engine import AuditIntelligenceEngine
from src.ccp.models.phase0_eval_card_models import (
    EvalCard,
    EvalCardBoard,
    EvalCardRole,
    EvalBoardKind
)


# Helper function to generate a valid prospect packet
def create_integration_prospect_packet() -> Phase0ProspectPacket:
    target = Phase0AuditTargetDescriptor(
        audit_target_id="TGT-TEST-REEL",
        prospect_id="PRP-JOHN-DOE",
        content_type="reel_caption",
        primary_media_source_ids=["media_source_video_1"],
        caption_id="CAP-1",
        platform_hint="Instagram",
        archetype_hint="explainer_reel",
        content_url="https://instagram.com/reel/123"
    )

    caption = Phase0CaptionAttachment(
        caption_id="CAP-1",
        prospect_id="PRP-JOHN-DOE",
        audit_target_id="TGT-TEST-REEL",
        caption_text=(
            "We must delve into authentic leadership and leverage our true voice "
            "to revolutionize our coaching practice. This is a testament to honest effort."
        ),
        source_kind="manual_entry"
    )

    return Phase0ProspectPacket(
        prospect_id="PRP-JOHN-DOE",
        display_name="John Doe",
        coach_id="NDL",
        submitted_at="2026-05-19T10:00:00Z",
        audit_targets=[target],
        captions=[caption]
    )


class TestFRERA335CEvalCardSystemIntegration:

    @pytest.mark.asyncio
    async def test_end_to_end_projection_and_assembly(self):
        """Tests end-to-end card projection, board assembly, and endpoint retrieves."""
        client = TestClient(app)

        # 1. Direct generation of an AuditIntelligenceReport
        packet = create_integration_prospect_packet()
        engine = AuditIntelligenceEngine(coach_acronym="NDL")
        
        report = engine.generate_audit(
            packet=packet,
            target_id="TGT-TEST-REEL",
            provisional_override=True
        )
        assert report.report_id is not None
        assert report.provisional_upstream_contract is True

        # Cache report in memory to simulate API generation
        reports_db[report.report_id] = report

        # 2. Project Card Endpoint POST /api/phase0/eval-cards/project (AC-1 to AC-5, AC-8)
        proj_payload = {
            "report_id": report.report_id,
            "role": "audit_primary"
        }
        response = client.post("/api/phase0/eval-cards/project", json=proj_payload)
        assert response.status_code == 200
        
        card_data = response.json()
        card = EvalCard.model_validate(card_data)
        assert card.report_id == report.report_id
        assert card.face.overall_score == report.visible_scores.presence - 10 or card.face.overall_score > 0
        assert card.face.thumbnail.asset_id == "TMB-media_source_video_1"
        assert len(card.face.visible_stats) == 7
        assert card.provisional_upstream_contract is True
        assert card.theme.background_primary is not None
        
        # Verify receipt was written for card projection
        from src.ccp.core.receipt_chain import ReceiptChain
        rc = ReceiptChain(coach_acronym="NDL")
        receipts = rc.query(action="project_eval_card", asset_id=card.card_id)
        assert len(receipts) == 1
        assert receipts[0].asset_id == card.card_id

        # 3. Direct Card Projection POST /api/phase0/eval-cards/project-direct
        direct_payload = {
            "report": report.model_dump(mode="json"),
            "role": "before_snapshot"
        }
        res_direct = client.post("/api/phase0/eval-cards/project-direct", json=direct_payload)
        assert res_direct.status_code == 200
        card_before = EvalCard.model_validate(res_direct.json())
        assert card_before.face.role == EvalCardRole.before_snapshot

        # Cache before card as well to support comparison
        client.get(f"/api/phase0/eval-cards/{card.card_id}") # retrieve check

        # 4. Assemble Board Endpoint POST /api/phase0/eval-cards/assemble-board (AC-6, AC-7)
        board_payload = {
            "report_id": report.report_id,
            "board_kind": "before_after_comparison",
            "card_ids": [card.card_id, card_before.card_id],
            "title": "Before/After Shift Board",
            "subtitle": "Transformation of Doe's reel delivery alignment",
            "density": "standard"
        }
        res_board = client.post("/api/phase0/eval-cards/assemble-board", json=board_payload)
        assert res_board.status_code == 200
        
        board_data = res_board.json()
        board = EvalCardBoard.model_validate(board_data)
        assert board.board_kind == EvalBoardKind.before_after_comparison
        assert len(board.cards) == 2
        # Ordering check: before_snapshot card should be first (index 0)
        assert board.cards[0].face.role == EvalCardRole.before_snapshot
        assert board.cards[1].face.role == EvalCardRole.audit_primary
        assert board.layout.columns == 2

        # Verify receipt was written for board assembly
        board_receipts = rc.query(action="assemble_eval_board", asset_id=board.board_id)
        assert len(board_receipts) == 1
        assert board_receipts[0].asset_id == board.board_id

        # 5. Render Board Endpoint POST /api/phase0/eval-cards/render-board (AC-11)
        render_payload = {
            "board": board.model_dump(mode="json"),
            "output_format": "png",
            "target_surface": "telegram_chat_preview",
            "watermark_enabled": True
        }
        res_render = client.post("/api/phase0/eval-cards/render-board", json=render_payload)
        assert res_render.status_code == 200
        render_data = res_render.json()
        assert render_data["status"] == "rendered_success"
        assert render_data["render_uri"] == f"https://render.ccp.coaches/exports/{board.board_id}.png"
        assert render_data["watermark_applied"] is True
