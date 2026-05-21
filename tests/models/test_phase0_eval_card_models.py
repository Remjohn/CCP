"""
FR-ERA3-35C Model Validation Tests
===================================
Tests strict Pydantic model validations for card faces, thumbnail, and board layouts.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.ccp.models.phase0_eval_card_models import (
    CardThumbnailAsset,
    EvalCardFace,
    EvalCardStatLine,
    CardVerdictBlock,
    CardThemeProjection,
    EvalCard,
    EvalBoardLayout,
    EvalCardBoard,
    VisibleCardStatKey,
    EvalCardRole,
    EvalBoardKind,
    CardScoreBand
)


# Helper function to generate valid components for test isolation
def create_valid_thumbnail() -> CardThumbnailAsset:
    return CardThumbnailAsset(
        asset_id="asset_123",
        storage_uri="https://ccp.storage/123.jpg",
        width=800,
        height=600,
        alt_text="A beautiful scouting card cover",
        source_kind="reel_caption"
    )


def create_valid_verdict() -> CardVerdictBlock:
    return CardVerdictBlock(
        verdict_line="Strong authentic performance with real presence.",
        fix_line="Enhance trust indicators by quoting case study metrics.",
        confidence_note="Provisional validation active."
    )


def create_valid_stats() -> list[EvalCardStatLine]:
    return [
        EvalCardStatLine(key=VisibleCardStatKey.humanity, label="Humanity", score=85, band=CardScoreBand.strong),
        EvalCardStatLine(key=VisibleCardStatKey.presence, label="Presence", score=92, band=CardScoreBand.elite),
        EvalCardStatLine(key=VisibleCardStatKey.trust, label="Trust", score=78, band=CardScoreBand.strong),
        EvalCardStatLine(key=VisibleCardStatKey.memorability, label="Memorability", score=65, band=CardScoreBand.developing),
        EvalCardStatLine(key=VisibleCardStatKey.resonance, label="Resonance", score=80, band=CardScoreBand.strong),
        EvalCardStatLine(key=VisibleCardStatKey.signal, label="Signal", score=88, band=CardScoreBand.strong),
        EvalCardStatLine(key=VisibleCardStatKey.ai_slop_risk, label="AI Slop Risk", score=12, band=CardScoreBand.weak),
    ]


class TestPhase0EvalCardModels:

    def test_valid_eval_card_face_passes(self):
        """Verify that a fully valid EvalCardFace construction passes validation."""
        face = EvalCardFace(
            title="Dignified Human Audit Card",
            subtitle="Batch #1",
            thumbnail=create_valid_thumbnail(),
            overall_score=84,
            role=EvalCardRole.audit_primary,
            card_type_label="Reel Audit Primary",
            visible_stats=create_valid_stats(),
            verdict=create_valid_verdict()
        )
        assert face.overall_score == 84
        assert len(face.visible_stats) == 7

    def test_reject_out_of_range_overall_score(self):
        """Verify that an overall score outside [0, 99] raises a validation error."""
        with pytest.raises(ValidationError):
            EvalCardFace(
                title="Dignified Human Audit Card",
                thumbnail=create_valid_thumbnail(),
                overall_score=100,  # Invalid: score limit is 99
                role=EvalCardRole.audit_primary,
                card_type_label="Reel Audit Primary",
                visible_stats=create_valid_stats(),
                verdict=create_valid_verdict()
            )

        with pytest.raises(ValidationError):
            EvalCardFace(
                title="Dignified Human Audit Card",
                thumbnail=create_valid_thumbnail(),
                overall_score=-5,  # Invalid: score ge=0
                role=EvalCardRole.audit_primary,
                card_type_label="Reel Audit Primary",
                visible_stats=create_valid_stats(),
                verdict=create_valid_verdict()
            )

    def test_reject_out_of_range_stat_score(self):
        """Verify that an individual stat line score outside [0, 99] raises validation error."""
        with pytest.raises(ValidationError):
            EvalCardStatLine(
                key=VisibleCardStatKey.humanity,
                label="Humanity",
                score=150,  # Invalid: score ge=0, le=99
                band=CardScoreBand.strong
            )

        with pytest.raises(ValidationError):
            EvalCardStatLine(
                key=VisibleCardStatKey.humanity,
                label="Humanity",
                score=-10,  # Invalid: score ge=0
                band=CardScoreBand.strong
            )

    def test_reject_duplicate_stats(self):
        """Verify that duplicate visible stat keys are strictly rejected (AC-1)."""
        stats = create_valid_stats()
        # Duplicate humanity key in place of presence key
        stats[1].key = VisibleCardStatKey.humanity

        with pytest.raises(ValidationError) as excinfo:
            EvalCardFace(
                title="Dignified Human Audit Card",
                thumbnail=create_valid_thumbnail(),
                overall_score=84,
                role=EvalCardRole.audit_primary,
                card_type_label="Reel Audit Primary",
                visible_stats=stats,
                verdict=create_valid_verdict()
            )
        assert "visible_stats must not contain duplicate keys" in str(excinfo.value)

    def test_reject_incomplete_stat_vocabulary(self):
        """Verify that having fewer than 7 unique stats fails validation."""
        stats = create_valid_stats()[:6]  # Missing AI Slop Risk

        with pytest.raises(ValidationError):
            EvalCardFace(
                title="Dignified Human Audit Card",
                thumbnail=create_valid_thumbnail(),
                overall_score=84,
                role=EvalCardRole.audit_primary,
                card_type_label="Reel Audit Primary",
                visible_stats=stats,
                verdict=create_valid_verdict()
            )

    def test_board_layout_column_constraints(self):
        """Verify columns bounds [1, 6] are validated correctly on EvalBoardLayout."""
        layout = EvalBoardLayout(
            board_kind=EvalBoardKind.audit_spread,
            columns=3
        )
        assert layout.columns == 3

        with pytest.raises(ValidationError):
            EvalBoardLayout(
                board_kind=EvalBoardKind.audit_spread,
                columns=7  # Out of bounds
            )

        with pytest.raises(ValidationError):
            EvalBoardLayout(
                board_kind=EvalBoardKind.audit_spread,
                columns=0  # Out of bounds
            )
