"""
FR-ERA3-35C Board Assembly Service Unit Tests
==============================================
Tests card board assembly, layout mappings, columns, density, and ordering.
"""

from __future__ import annotations

import pytest

from src.ccp.models.phase0_eval_card_models import (
    EvalCard,
    EvalCardFace,
    EvalCardStatLine,
    CardThumbnailAsset,
    CardVerdictBlock,
    CardThemeProjection,
    VisibleCardStatKey,
    EvalCardRole,
    EvalBoardKind,
    CardScoreBand,
    BoardDensity
)
from src.ccp.services.eval_board_assembly_service import EvalBoardAssemblyService


# Helper functions to build mockup EvalCard objects
def create_mock_card(card_id: str, role: EvalCardRole, overall_score: int) -> EvalCard:
    thumbnail = CardThumbnailAsset(
        asset_id="tmb_123",
        storage_uri="https://ccp.storage/123.jpg",
        width=800,
        height=600,
        alt_text="Mock Scouter Thumbnail",
        source_kind="reel_caption"
    )

    verdict = CardVerdictBlock(
        verdict_line="Strong authentic presence shown.",
        fix_line="Quell AI slop by introducing case markers."
    )

    stats = [
        EvalCardStatLine(key=VisibleCardStatKey.humanity, label="Humanity", score=overall_score, band=CardScoreBand.strong),
        EvalCardStatLine(key=VisibleCardStatKey.presence, label="Presence", score=overall_score, band=CardScoreBand.strong),
        EvalCardStatLine(key=VisibleCardStatKey.trust, label="Trust", score=overall_score, band=CardScoreBand.strong),
        EvalCardStatLine(key=VisibleCardStatKey.memorability, label="Memorability", score=overall_score, band=CardScoreBand.strong),
        EvalCardStatLine(key=VisibleCardStatKey.resonance, label="Resonance", score=overall_score, band=CardScoreBand.strong),
        EvalCardStatLine(key=VisibleCardStatKey.signal, label="Signal", score=overall_score, band=CardScoreBand.strong),
        EvalCardStatLine(key=VisibleCardStatKey.ai_slop_risk, label="AI Slop Risk", score=10, band=CardScoreBand.weak),
    ]

    face = EvalCardFace(
        title=f"Mock Card — {card_id}",
        thumbnail=thumbnail,
        overall_score=overall_score,
        role=role,
        card_type_label="Audit Card",
        visible_stats=stats,
        verdict=verdict
    )

    theme = CardThemeProjection(
        background_primary="#1e293b",
        background_secondary="#0f172a",
        accent="#3b82f6",
        text_primary="#f8fafc"
    )

    return EvalCard(
        card_id=card_id,
        report_id="RPT-ABC-123",
        face=face,
        theme=theme,
        source_content_type="reel_caption",
        generated_at="2026-05-19T12:00:00Z"
    )


class TestEvalBoardAssemblyService:

    def test_single_card_detail_assembly(self):
        """Verify assembling a single card detail board is successful."""
        service = EvalBoardAssemblyService()
        card = create_mock_card("CRD-1", EvalCardRole.audit_primary, 85)

        board = service.assemble_board(
            report_id="RPT-ABC-123",
            board_kind=EvalBoardKind.single_card_detail,
            cards=[card],
            title="Single Channel Deep Dive"
        )

        assert board.board_kind == EvalBoardKind.single_card_detail
        assert len(board.cards) == 1
        assert board.layout.columns == 1
        assert board.layout.density == BoardDensity.standard

    def test_audit_spread_layout_assembly(self):
        """Verify assembling multiple cards into an audit spread board works and default columns = 3."""
        service = EvalBoardAssemblyService()
        cards = [
            create_mock_card("CRD-1", EvalCardRole.audit_primary, 85),
            create_mock_card("CRD-2", EvalCardRole.audit_secondary, 72)
        ]

        board = service.assemble_board(
            report_id="RPT-ABC-123",
            board_kind=EvalBoardKind.audit_spread,
            cards=cards,
            title="Full Brand Coverage Audit"
        )

        assert board.board_kind == EvalBoardKind.audit_spread
        assert len(board.cards) == 2
        assert board.layout.columns == 3

    def test_before_after_ordering_law(self):
        """Verify that cards are reordered such that before_snapshot is placed first (AC-6, task 21)."""
        service = EvalBoardAssemblyService()
        # Create an out-of-order list where after snapshot is first
        after_card = create_mock_card("CRD-AFTER", EvalCardRole.after_snapshot, 92)
        before_card = create_mock_card("CRD-BEFORE", EvalCardRole.before_snapshot, 55)

        board = service.assemble_board(
            report_id="RPT-ABC-123",
            board_kind=EvalBoardKind.before_after_comparison,
            cards=[after_card, before_card],
            title="Signal Transformation Comparison"
        )

        assert board.board_kind == EvalBoardKind.before_after_comparison
        assert board.cards[0].card_id == "CRD-BEFORE"
        assert board.cards[1].card_id == "CRD-AFTER"
        assert board.layout.columns == 2

    def test_reject_zero_cards_board(self):
        """Verify that trying to build a board with 0 cards raises a ValueError."""
        service = EvalBoardAssemblyService()
        with pytest.raises(ValueError) as excinfo:
            service.assemble_board(
                report_id="RPT-ABC-123",
                board_kind=EvalBoardKind.audit_spread,
                cards=[],
                title="Invalid Empty Board"
            )
        assert "must contain at least one card" in str(excinfo.value)
