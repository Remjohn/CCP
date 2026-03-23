"""
Step 10 Integration Test Suite — FR22 + FR23 + FR25
Fingerprint Archive + Anti-Draft Intelligence + Boredom Ban

12 Acceptance Criteria (4 per FR) per the Build Protocol.

FR22 Anti-Draft Intelligence (DEP-PROTO-013):
  AC1: Level 1 abstract description → immediate Block C Compilation failure.
  AC2: M3 wire-up — Escape Mode compile targeting M3 belief → subversion command.
  AC3: DEP-ENG-004 Level 3 Forbidden Strings appear BEFORE DEP-ENG-003 targets.
  AC4: Critic detects 2 violations → halts, purges draft, FULL_PURGE_REGENERATE.

FR23 Skill Fingerprint ID (DEP-ENG-020):
  AC1: Synthesis validity — correct hyphenated string format.
  AC2: Hash integrity — same object produces same SHA-256 hash.
  AC3: Promotion math — 3rd successful telemetry payload → maturity=Tested.
  AC4: ADR-01 — telemetry payload for Emilio MUST NOT write to Maria's archive.

FR25 Boredom Ban (DEP-PROTO-015):
  AC1: Metaphor collision catch — 32-day-old metaphor rejected (56-day window).
  AC2: Theme similarity catch — cosine 0.85 → REJECT BOREDOM_BAN.
  AC3: Structural fatigue — 4th LIST02 in same week → REJECT: STRUCTURAL_FATIGUE.
  AC4: ADR-01 — Coach Maria's metaphor check does not read Coach Emilio's memory.
"""

from __future__ import annotations

import hashlib
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.anti_draft_models import (
    CRITIC_FULL_PURGE_THRESHOLD,
    FROZEN_ANCHOR_MODEL,
    L3_MINIMUM_DEPTH_THRESHOLD,
    AntiDraftHaltReason,
    CriticVerdict,
    FinalSemanticDistanceStatus,
    Level2Mode,
)
from src.ccp.models.boredom_ban_models import (
    BOREDOM_BAN_WINDOW_DAYS,
    STRUCTURAL_FATIGUE_MAX_USES,
    THEME_COSINE_REJECT_THRESHOLD,
    BoredomBanVectorStatus,
    MemoryFolderEntry,
    OverallNoveltyVerdict,
)
from src.ccp.models.fingerprint_archive_models import (
    TESTED_MINIMUM_OUTPUTS,
    AudienceCohort,
    ContentPerformanceMetrics,
    MoodCode,
    OutputTelemetryPayload,
    RegulatoryFrame,
    SkillIDComponents,
    SkillMaturity,
)
from src.ccp.models.voice_dna_models import (
    LexicalBlacklist,
    NegativeSpaceObject,
    StructuralExclusions,
)
from src.ccp.services.anti_draft_calibrator import (
    AntiDraftCalibrator,
    AntiDraftHaltError,
)
from src.ccp.services.boredom_ban_enforcer import BoredomBanEnforcer
from src.ccp.services.fingerprint_archive_engine import (
    ArchiveIntegrityError,
    FingerprintArchiveEngine,
    _sha256_of_object,
    _sha256_of_string,
)


# ─── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def tmp_receipts(tmp_path: Path) -> str:
    d = tmp_path / "receipts"
    d.mkdir()
    return str(d)


@pytest.fixture
def receipt_chain(tmp_receipts: str) -> ReceiptChain:
    return ReceiptChain(coach_acronym="TST", log_dir=tmp_receipts)


@pytest.fixture
def negative_space_rich() -> NegativeSpaceObject:
    """DEP-ENG-004 with >= 15 contrastive strings (passes Gate PC-03)."""
    return NegativeSpaceObject(
        lexical_blacklist=LexicalBlacklist(
            academic=["facilitate", "leverage", "synergize", "paradigm", "optimize"],
            spiritual=["manifest", "universe", "vibration", "alignment", "soul"],
            banned_intensifiers=["absolutely", "definitely", "certainly"],
        ),
        syntactic_impossibilities=[
            "In conclusion,",
            "It is important to note that",
            "As we all know,",
            "In today's world,",
        ],
        structural_exclusions=StructuralExclusions(
            forbidden_openings=["Let me tell you a story about", "Once upon a time"],
            forbidden_closings=["In summary,", "To wrap up,"],
        ),
    )


@pytest.fixture
def negative_space_thin() -> NegativeSpaceObject:
    """DEP-ENG-004 with < 15 contrastive strings (fails Gate PC-03)."""
    return NegativeSpaceObject(
        lexical_blacklist=LexicalBlacklist(
            academic=["facilitate"],
            spiritual=["manifest"],
            banned_intensifiers=[],
        ),
        syntactic_impossibilities=["In conclusion,"],
        structural_exclusions=StructuralExclusions(
            forbidden_openings=[],
            forbidden_closings=[],
        ),
    )


@pytest.fixture
def valid_archetype_container() -> str:
    """A valid archetype container block with all 4 required subsections."""
    return (
        "[Statistical Centroid Prose Example]\n"
        "Once you embrace this journey of discovery, you will unlock your potential. "
        "Life-changing results await those who believe in themselves. "
        "Hard work pays off when you follow your dreams, because you can do anything. "
        "The power of positive thinking transforms your life.\n"
        "[Mechanism Failure Diagnosis]\n"
        "The generic AI assumes emotional resonance can be told rather than earned.\n"
        "[Resolution Failure Diagnosis]\n"
        "The resolution arrives before stakes are felt — insight unearned by the reader.\n"
        "[Semantic Distance Instruction]\n"
        "Maximize vector distance from the above. Every sentence must diverge.\n"
    )


@pytest.fixture
def abstract_archetype_container() -> str:
    """An INVALID container: Level 1 is abstract descriptions, not concrete prose.
    AC1: This MUST fail the Block C compilation gate."""
    return (
        "[Statistical Centroid Prose Example]\n"
        "Avoid clichés and generic tone.\n"
        "[Mechanism Failure Diagnosis]\n"
        "The mechanism is wrong.\n"
        "[Resolution Failure Diagnosis]\n"
        "Resolution fails.\n"
        "[Semantic Distance Instruction]\n"
        "Stay original.\n"
    )


@pytest.fixture
def memory_entries_rich(coach_id: str = "TST") -> list[MemoryFolderEntry]:
    """8-week memory for TST coach with varied themes and metaphors."""
    today = datetime.now(timezone.utc).date()
    return [
        MemoryFolderEntry(
            skill_id="SKILL-STORY01-TST-P-PRV-L-20260201-001",
            coach_id=coach_id,
            thematic_payload="Why diets don't work for most people long-term",
            metaphor_vehicle="Building a house foundation stone by stone",
            archetype_format="STORY01",
            published_date=today - timedelta(days=32),
        ),
        MemoryFolderEntry(
            skill_id="SKILL-LIST02-TST-E-PRO-N-20260210-001",
            coach_id=coach_id,
            thematic_payload="Overcoming imposter syndrome in high-achieving women",
            metaphor_vehicle="Sailing against the current",
            archetype_format="LIST02",
            published_date=today - timedelta(days=20),
        ),
        MemoryFolderEntry(
            skill_id="SKILL-LIST02-TST-E-PRO-N-20260215-001",
            coach_id=coach_id,
            thematic_payload="Three-step framework for overcoming fear",
            metaphor_vehicle="Climbing the mountain",
            archetype_format="LIST02",
            published_date=today - timedelta(days=10),
        ),
        MemoryFolderEntry(
            skill_id="SKILL-LIST02-TST-E-PRO-N-20260218-001",
            coach_id=coach_id,
            thematic_payload="Breaking through the glass ceiling",
            metaphor_vehicle="Crossing the river",
            archetype_format="LIST02",
            published_date=today - timedelta(days=7),
        ),
        MemoryFolderEntry(
            skill_id="SKILL-LIST02-TST-E-PRO-N-20260220-001",
            coach_id=coach_id,
            thematic_payload="Building confidence after failure",
            metaphor_vehicle="Forging steel in fire",
            archetype_format="LIST02",
            published_date=today - timedelta(days=3),
        ),
    ]


# ─── FR22 Anti-Draft Intelligence Tests ──────────────────────────────────────

class TestFR22_AC1:
    """AC1: Level 1 abstract description → immediate Block C Compilation failure.

    Spec §8 AC1: 'Submitting a Block A Design Brief where Level 1 Anti-Draft
    is written as "Avoid clichés and generic tone." results in an immediate
    Block C Compilation failure.'
    Failure Example: 'The system allows the abstract list to pass.'
    """

    def test_abstract_level1_raises_halt_error(
        self,
        abstract_archetype_container: str,
        negative_space_rich: NegativeSpaceObject,
        receipt_chain: ReceiptChain,
    ) -> None:
        calibrator = AntiDraftCalibrator(coach_id="TST", receipt_chain=receipt_chain)
        with pytest.raises(AntiDraftHaltError) as exc_info:
            calibrator.stage_1_build_frozen_anchor(
                archetype_container_block=abstract_archetype_container,
                archetype_id="STORY01",
            )
        assert exc_info.value.halt_reason == AntiDraftHaltReason.L1_ABSTRACT_DESCRIPTION

    def test_valid_prose_level1_passes(
        self,
        valid_archetype_container: str,
        receipt_chain: ReceiptChain,
    ) -> None:
        calibrator = AntiDraftCalibrator(coach_id="TST", receipt_chain=receipt_chain)
        block = calibrator.stage_1_build_frozen_anchor(
            archetype_container_block=valid_archetype_container,
            archetype_id="STORY01",
        )
        assert block.is_valid_prose() is True
        assert block.has_all_subsections() is True
        assert block.archetype_id == "STORY01"
        assert block.frozen_model_used == FROZEN_ANCHOR_MODEL

    def test_full_pipeline_halts_on_abstract_level1(
        self,
        abstract_archetype_container: str,
        negative_space_rich: NegativeSpaceObject,
        receipt_chain: ReceiptChain,
    ) -> None:
        calibrator = AntiDraftCalibrator(coach_id="TST", receipt_chain=receipt_chain)
        log = calibrator.run_full_calibration(
            compilation_request_id="REQ-TEST-001",
            archetype_container_block=abstract_archetype_container,
            archetype_id="STORY01",
            routing_mode=Level2Mode.ESCAPE,
            negative_space=negative_space_rich,
            draft_text="A test draft.",
        )
        assert log.halted is True
        assert log.halt_reason == AntiDraftHaltReason.L1_ABSTRACT_DESCRIPTION
        assert log.final_semantic_distance_status == FinalSemanticDistanceStatus.FAILED


class TestFR22_AC2:
    """AC2: M3 wire-up — Escape Mode + M3 belief → explicit subversion command.

    Spec §8 AC2: 'An Escape Mode compile targeting the M3 belief "Working harder
    is the only way out" results in a Level 2 block explicitly commanding the
    subversion of that exact sentence.'
    Failure Example: 'M3 is loaded but ignored by the payload-masking-adapter.'
    """

    def test_escape_mode_m3_produces_subversion_command(
        self, receipt_chain: ReceiptChain
    ) -> None:
        calibrator = AntiDraftCalibrator(coach_id="TST", receipt_chain=receipt_chain)
        m3_belief = "Working harder is the only way out"
        block = calibrator.stage_2_generate_mode_belief(
            routing_mode=Level2Mode.ESCAPE,
            m3_undeniable_belief=m3_belief,
        )
        assert block.m3_subversion_command is not None
        assert m3_belief in block.m3_subversion_command
        assert "tear this assumption down" in block.m3_subversion_command
        assert not block.is_degraded

    def test_m3_absent_produces_degraded_not_halt(
        self, receipt_chain: ReceiptChain
    ) -> None:
        calibrator = AntiDraftCalibrator(coach_id="TST", receipt_chain=receipt_chain)
        block = calibrator.stage_2_generate_mode_belief(
            routing_mode=Level2Mode.PROCESSING,
            m3_undeniable_belief=None,
        )
        assert block.is_degraded is True
        assert block.m3_subversion_command is None
        assert "M3_ABSENT" in str(block.degradation_reason)

    def test_processing_mode_failure_scenario_differs_from_escape(
        self, receipt_chain: ReceiptChain
    ) -> None:
        calibrator = AntiDraftCalibrator(coach_id="TST", receipt_chain=receipt_chain)
        escape_block = calibrator.stage_2_generate_mode_belief(
            routing_mode=Level2Mode.ESCAPE,
            m3_undeniable_belief="Belief X",
        )
        proc_block = calibrator.stage_2_generate_mode_belief(
            routing_mode=Level2Mode.PROCESSING,
            m3_undeniable_belief="Belief X",
        )
        # Mode-failure scenarios must differ per spec §4 Stage 2 Step 2
        assert escape_block.mode_failure_scenario != proc_block.mode_failure_scenario
        assert "semantic affinity" in escape_block.mode_failure_scenario
        assert "unearned" in proc_block.mode_failure_scenario


class TestFR22_AC3:
    """AC3: DEP-ENG-004 Level 3 Forbidden Strings appear BEFORE DEP-ENG-003 targets.

    Spec §8 AC3: 'In the final SKILL.md text stream sent to the LLM,
    the DEP-ENG-004 Level 3 "Forbidden Strings" appear sequentially BEFORE
    the DEP-ENG-003 Authentic Voice targets.'
    Failure Example: 'Positive constraints load first, nullifying the negative anchor.'
    """

    def test_level3_block_has_loaded_first_flag(
        self,
        negative_space_rich: NegativeSpaceObject,
        receipt_chain: ReceiptChain,
    ) -> None:
        calibrator = AntiDraftCalibrator(coach_id="TST", receipt_chain=receipt_chain)
        block = calibrator.stage_3_load_negative_space(negative_space_rich)
        # AC3 structural invariant: loaded_first must be True
        assert block.loaded_first is True

    def test_gate_pc03_enforced_on_thin_negative_space(
        self,
        negative_space_thin: NegativeSpaceObject,
        receipt_chain: ReceiptChain,
    ) -> None:
        calibrator = AntiDraftCalibrator(coach_id="TST", receipt_chain=receipt_chain)
        with pytest.raises(AntiDraftHaltError) as exc_info:
            calibrator.stage_3_load_negative_space(negative_space_thin)
        assert exc_info.value.halt_reason == AntiDraftHaltReason.L3_INSUFFICIENT_DEPTH

    def test_all_four_vectors_extracted(
        self,
        negative_space_rich: NegativeSpaceObject,
        receipt_chain: ReceiptChain,
    ) -> None:
        calibrator = AntiDraftCalibrator(coach_id="TST", receipt_chain=receipt_chain)
        block = calibrator.stage_3_load_negative_space(negative_space_rich)
        assert len(block.cognitive_load_drift_patterns) > 0
        assert len(block.professional_register_hedges) > 0
        assert len(block.performed_vocabulary) > 0
        assert len(block.forbidden_strings_flat) >= L3_MINIMUM_DEPTH_THRESHOLD
        assert block.passes_depth_gate() is True


class TestFR22_AC4:
    """AC4: Critic detects 2 violations → halts, purges draft, restarts generation.

    Spec §8 AC4: 'If the Critic detects 2 violations in the draft_v1.md,
    it automatically halts, purges the draft, and restarts generation with
    the critic_report.json as context.'
    Failure Example: 'Critic successfully spots 3 violations but just logs them
    as warnings and passes the flawed script to the user.'
    """

    def test_two_violations_trigger_full_purge(
        self,
        valid_archetype_container: str,
        negative_space_rich: NegativeSpaceObject,
        receipt_chain: ReceiptChain,
    ) -> None:
        calibrator = AntiDraftCalibrator(coach_id="TST", receipt_chain=receipt_chain)
        level_1 = calibrator.stage_1_build_frozen_anchor(
            archetype_container_block=valid_archetype_container,
            archetype_id="STORY01",
        )
        level_2 = calibrator.stage_2_generate_mode_belief(
            routing_mode=Level2Mode.ESCAPE,
            m3_undeniable_belief="Working harder is the only way out",
        )
        level_3 = calibrator.stage_3_load_negative_space(negative_space_rich)

        # Draft containing: 1 cliché + 1 forbidden string → 2 violations
        forbidden = negative_space_rich.lexical_blacklist.academic[0]
        bad_draft = (
            f"This is a journey of discovery to unlock your potential. "
            f"You must {forbidden} the process to achieve results."
        )

        report = calibrator.stage_4_run_critic(
            draft_text=bad_draft,
            level_1_block=level_1,
            level_2_block=level_2,
            level_3_block=level_3,
        )
        # AC4 enforcement: 2 violations → FULL_PURGE_REGENERATE
        assert report.violation_count >= CRITIC_FULL_PURGE_THRESHOLD
        assert report.verdict == CriticVerdict.FULL_PURGE_REGENERATE
        assert report.full_purge_triggered is True
        assert report.targeted_rewrite_triggered is False

    def test_one_violation_triggers_targeted_rewrite(
        self,
        valid_archetype_container: str,
        negative_space_rich: NegativeSpaceObject,
        receipt_chain: ReceiptChain,
    ) -> None:
        calibrator = AntiDraftCalibrator(coach_id="TST", receipt_chain=receipt_chain)
        level_1 = calibrator.stage_1_build_frozen_anchor(
            valid_archetype_container, "STORY01"
        )
        level_2 = calibrator.stage_2_generate_mode_belief(Level2Mode.PROCESSING, None)
        level_3 = calibrator.stage_3_load_negative_space(negative_space_rich)

        # Draft with 1 cliché only
        one_violation_draft = "This is a journey of discovery for the audience."
        report = calibrator.stage_4_run_critic(
            draft_text=one_violation_draft,
            level_1_block=level_1,
            level_2_block=level_2,
            level_3_block=level_3,
        )
        assert report.violation_count == 1
        assert report.verdict == CriticVerdict.TARGETED_SECTION_REWRITE
        assert report.targeted_rewrite_triggered is True
        assert report.full_purge_triggered is False

    def test_zero_violations_passes_payload(
        self,
        valid_archetype_container: str,
        negative_space_rich: NegativeSpaceObject,
        receipt_chain: ReceiptChain,
    ) -> None:
        calibrator = AntiDraftCalibrator(coach_id="TST", receipt_chain=receipt_chain)
        level_1 = calibrator.stage_1_build_frozen_anchor(
            valid_archetype_container, "STORY01"
        )
        level_2 = calibrator.stage_2_generate_mode_belief(Level2Mode.SOCIAL, None)
        level_3 = calibrator.stage_3_load_negative_space(negative_space_rich)

        clean_draft = (
            "The day everything fell apart was the same day I learned what mattered. "
            "Not the metrics, not the reviews — the person sitting across from me "
            "who needed something real. That shift cost me a promotion and gave me back "
            "my voice."
        )
        report = calibrator.stage_4_run_critic(
            draft_text=clean_draft,
            level_1_block=level_1,
            level_2_block=level_2,
            level_3_block=level_3,
        )
        assert report.violation_count == 0
        assert report.verdict == CriticVerdict.PASS_GENERATION_PAYLOAD


# ─── FR23 Skill Fingerprint ID Tests ─────────────────────────────────────────

class TestFR23_AC1:
    """AC1: Synthesis validity — correct hyphenated Skill ID string.

    Spec §8 AC1: 'A design brief compiled for Ana, Shocking Listicle,
    Escape Mode, Promotion Frame, New Cohort on March 15th results perfectly
    in SKILL-LIST02-ANA-E-PRO-N-20260315-001.'
    Failure Example: 'Extraneous spaces or null pointers break the formatting.'
    """

    def test_exact_skill_id_format(self) -> None:
        components = SkillIDComponents(
            arch_id="LIST02",
            coach_id="ANA",
            mood=MoodCode.ESCAPE,
            regulatory_frame=RegulatoryFrame.PROMOTION,
            cohort=AudienceCohort.NEW,
            compilation_date=date(2026, 3, 15),
            sequence_number=1,
        )
        skill_id = components.synthesize()
        assert skill_id == "SKILL-LIST02-ANA-E-PRO-N-20260315-001"

    def test_sequence_increments_correctly(self) -> None:
        engine = FingerprintArchiveEngine(coach_id="ANA")
        day = date(2026, 3, 15)
        id1 = engine.synthesize_skill_id(
            arch_id="LIST02",
            mood=MoodCode.ESCAPE,
            regulatory_frame=RegulatoryFrame.PROMOTION,
            cohort=AudienceCohort.NEW,
            compilation_date=day,
        )
        # Register so the engine tracks the first
        engine.register_skill(
            skill_id=id1,
            assembly_status="COMPLETE",
        )
        id2 = engine.synthesize_skill_id(
            arch_id="STORY01",
            mood=MoodCode.PROCESSING,
            regulatory_frame=RegulatoryFrame.PREVENTION,
            cohort=AudienceCohort.LOYAL,
            compilation_date=day,
        )
        # Sequence number must advance
        assert id1.endswith("-001")
        assert id2.endswith("-002")

    def test_no_null_segments_in_skill_id(self) -> None:
        engine = FingerprintArchiveEngine(coach_id="EMI")
        skill_id = engine.synthesize_skill_id(
            arch_id="STORY01",
            mood=MoodCode.PROCESSING,
            regulatory_frame=RegulatoryFrame.PREVENTION,
            cohort=AudienceCohort.LOYAL,
            compilation_date=date(2026, 3, 15),
        )
        assert "null" not in skill_id.lower()
        assert "none" not in skill_id.lower()
        assert "  " not in skill_id  # No double spaces
        parts = skill_id.split("-")
        assert all(bool(p) for p in parts), "No empty segments allowed"


class TestFR23_AC2:
    """AC2: Hash integrity — same object → same SHA-256 hash.

    Spec §8 AC2: 'Running the same hashing algorithm on the coach's Voice DNA
    file from that exact timestamp produces the exact same hash.'
    Failure Example: 'System hashes a blank RAM buffer resulting in empty strings.'
    """

    def test_same_object_same_hash(self) -> None:
        obj = {"voice_dna": {"vocabulary_fingerprint": ["authentic", "raw", "honest"]}}
        hash1 = _sha256_of_object(obj)
        hash2 = _sha256_of_object(obj)
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA-256 hex string

    def test_different_objects_different_hashes(self) -> None:
        obj_a = {"coach_id": "EMI", "data": "version_1"}
        obj_b = {"coach_id": "EMI", "data": "version_2"}
        assert _sha256_of_object(obj_a) != _sha256_of_object(obj_b)

    def test_none_produces_empty_hash(self) -> None:
        """AC2 failure guard: hashing None should NOT produce a random string."""
        result = _sha256_of_object(None)
        assert result == ""

    def test_dep_snapshot_populated_after_registration(self) -> None:
        engine = FingerprintArchiveEngine(coach_id="EMI")
        skill_id = engine.synthesize_skill_id(
            arch_id="STORY01",
            mood=MoodCode.PROCESSING,
            regulatory_frame=RegulatoryFrame.PREVENTION,
            cohort=AudienceCohort.LOYAL,
        )
        dep_eng_003 = {"vocabulary_fingerprint": ["word1", "word2"]}
        dep_eng_006 = {"emotional_baseline": 0.72}
        dep_eng_016 = {"mood_state": "Processing", "regulatory_frame": "prevention"}

        result = engine.register_skill(
            skill_id=skill_id,
            assembly_status="COMPLETE",
            dep_eng_003_obj=dep_eng_003,
            dep_eng_006_obj=dep_eng_006,
            dep_eng_016_obj=dep_eng_016,
        )

        assert result.success is True
        assert result.dep_snapshot_populated is True
        record = engine.get_record(skill_id)
        assert record is not None
        assert len(record.dep_snapshot.dep_eng_003) == 64
        assert len(record.dep_snapshot.dep_eng_006) == 64
        assert len(record.dep_snapshot.dep_eng_016) == 64


class TestFR23_AC3:
    """AC3: Promotion math — 3rd successful output → maturity = Tested.

    Spec §8 AC3: 'A draft skill receives its 3rd telemetry payload reflecting
    zero assembly errors. The asynchronous monitor immediately changes
    maturity to Tested.'
    Failure Example: 'The threshold algorithm counts an error-flagged assembly.'
    """

    def _make_payload(self, coach_id: str, skill_id: str, output_n: int) -> OutputTelemetryPayload:
        return OutputTelemetryPayload(
            output_id=f"OUT-{skill_id}-{output_n:03d}",
            skill_id=skill_id,
            coach_id=coach_id,
            content_title=f"Test output {output_n}",
            performance=ContentPerformanceMetrics(saves=500, shares=100),
            assembly_failure=False,
        )

    def test_third_successful_output_promotes_to_tested(self) -> None:
        engine = FingerprintArchiveEngine(coach_id="EMI")
        skill_id = engine.synthesize_skill_id(
            arch_id="STORY01",
            mood=MoodCode.PROCESSING,
            regulatory_frame=RegulatoryFrame.PREVENTION,
            cohort=AudienceCohort.LOYAL,
        )
        engine.register_skill(skill_id=skill_id, assembly_status="COMPLETE")

        record = engine.get_record(skill_id)
        assert record is not None, "register_skill must create a record"
        assert record.maturity == SkillMaturity.DRAFT

        # Send first 2 successful payloads — should stay Draft
        engine.receive_telemetry(self._make_payload("EMI", skill_id, 1))
        engine.receive_telemetry(self._make_payload("EMI", skill_id, 2))
        assert record.maturity == SkillMaturity.DRAFT

        # Third successful payload → Tested
        response = engine.receive_telemetry(self._make_payload("EMI", skill_id, 3))
        assert record.maturity == SkillMaturity.TESTED
        assert response.accepted is True
        assert response.promotion_result is not None
        assert response.promotion_result.promoted is True
        assert response.promotion_result.new_maturity == SkillMaturity.TESTED

    def test_error_flagged_output_does_not_count_toward_tested(self) -> None:
        """AC3 Failure Guard: error-flagged assembly MUST NOT count."""
        engine = FingerprintArchiveEngine(coach_id="EMI")
        skill_id = engine.synthesize_skill_id(
            arch_id="LIST02",
            mood=MoodCode.ESCAPE,
            regulatory_frame=RegulatoryFrame.PROMOTION,
            cohort=AudienceCohort.NEW,
        )
        engine.register_skill(skill_id=skill_id, assembly_status="COMPLETE")

        # Send 2 successful + 1 failed
        engine.receive_telemetry(self._make_payload("EMI", skill_id, 1))
        engine.receive_telemetry(self._make_payload("EMI", skill_id, 2))
        # Error-flagged
        failed_payload = OutputTelemetryPayload(
            output_id=f"OUT-{skill_id}-003",
            skill_id=skill_id,
            coach_id="EMI",
            content_title="Failed output",
            performance=ContentPerformanceMetrics(saves=0),
            assembly_failure=True,
        )
        engine.receive_telemetry(failed_payload)
        record = engine.get_record(skill_id)
        assert record is not None, "register_skill must create a record"
        # Must still be Draft (only 2 successful, not 3)
        assert record.maturity == SkillMaturity.DRAFT


class TestFR23_AC4:
    """AC4: ADR-01 — Emilio's telemetry MUST NOT write to Maria's archive.

    Spec §8 AC4: 'When the Telemetry Listener receives an engagement payload for
    Emilio's output, the JSON write explicitly locks to Emilio's isolated
    fingerprint_archive.json bucket.'
    Failure Example: 'System writes Emilio's metric payload into Maria's skill JSON.'
    """

    def test_cross_tenant_write_raises_integrity_error(self) -> None:
        engine_emilio = FingerprintArchiveEngine(coach_id="EMI")
        engine_maria = FingerprintArchiveEngine(coach_id="MAR")

        # Register a skill in Maria's engine
        maria_skill = "SKILL-STORY01-MAR-P-PRV-L-20260315-001"
        engine_maria.register_skill(maria_skill, "COMPLETE")

        # Attempt to send Emilio's payload (coach_id=EMI) to Maria's engine
        emilio_payload = OutputTelemetryPayload(
            output_id="OUT-001",
            skill_id=maria_skill,
            coach_id="EMI",  # Emilio's payload
            content_title="Emilio's viral post",
            performance=ContentPerformanceMetrics(saves=2847),
            assembly_failure=False,
        )

        with pytest.raises(ArchiveIntegrityError) as exc_info:
            engine_maria.receive_telemetry(emilio_payload)
        assert "ADR-01 VIOLATION" in str(exc_info.value)
        assert "EMI" in str(exc_info.value)

    def test_correct_tenant_write_succeeds(self) -> None:
        engine = FingerprintArchiveEngine(coach_id="EMI")
        skill_id = engine.synthesize_skill_id(
            arch_id="STORY01",
            mood=MoodCode.PROCESSING,
            regulatory_frame=RegulatoryFrame.PREVENTION,
            cohort=AudienceCohort.LOYAL,
        )
        engine.register_skill(skill_id, "COMPLETE")
        payload = OutputTelemetryPayload(
            output_id="OUT-EMI-001",
            skill_id=skill_id,
            coach_id="EMI",
            performance=ContentPerformanceMetrics(saves=1500),
            assembly_failure=False,
        )
        response = engine.receive_telemetry(payload)
        assert response.accepted is True
        assert response.error is None


# ─── FR25 Boredom Ban Tests ────────────────────────────────────────────────────

class TestFR25_AC1:
    """AC1: Metaphor collision catch — 32-day-old metaphor is STILL within 56-day window.

    Spec §8 AC1: 'The coach used "Building a house foundation" 32 days ago.
    Grâce explicitly rejects it.'
    Failure Example: 'System allows it because 32 days exceeded a hardcoded
    30-day (instead of 56-day) limit.'
    """

    def test_32_day_metaphor_rejected_in_56_day_window(
        self, memory_entries_rich: list[MemoryFolderEntry]
    ) -> None:
        enforcer = BoredomBanEnforcer(coach_id="TST")
        # "Building a house foundation" should match the 32-day-old entry
        result = enforcer.check_metaphor_novelty(
            proposed_metaphor="Building a house foundation stone by stone",
            memory_entries=memory_entries_rich,
        )
        assert result.status == BoredomBanVectorStatus.REJECT_TILL_DONE_TRIGGERED
        assert result.offending_vehicle is not None
        assert result.days_since_last_use is not None
        # AC1 key check: 32 days is within 56-day window (not rejected by a 30-day limit)
        assert result.days_since_last_use <= BOREDOM_BAN_WINDOW_DAYS

    def test_till_done_command_suggests_unrelated_domain(
        self, memory_entries_rich: list[MemoryFolderEntry]
    ) -> None:
        enforcer = BoredomBanEnforcer(coach_id="TST")
        result = enforcer.check_metaphor_novelty(
            proposed_metaphor="Building a house foundation stone by stone",
            memory_entries=memory_entries_rich,
        )
        assert result.till_done_rewrite_command is not None
        # Must suggest unrelated domain per spec §4 Stage 2 Step 3
        cmd = result.till_done_rewrite_command
        assert any(
            domain in cmd.lower()
            for domain in ["biology", "architecture", "thermodynamics", "domain", "unrelated"]
        )

    def test_novel_metaphor_passes(
        self, memory_entries_rich: list[MemoryFolderEntry]
    ) -> None:
        enforcer = BoredomBanEnforcer(coach_id="TST")
        result = enforcer.check_metaphor_novelty(
            proposed_metaphor="The mitochondria of cellular respiration",
            memory_entries=memory_entries_rich,
        )
        assert result.status == BoredomBanVectorStatus.PASS


class TestFR25_AC2:
    """AC2: Theme similarity catch — cosine 0.85 → REJECT.

    Spec §8 AC2: 'Divine suggests "Overcoming Imposter Syndrome" which triggers
    0.85 cosine similarity against a post from 3 weeks prior. Divine drops it.'
    Failure Example: 'System crashes computing embeddings of 50 past scripts.'
    """

    def test_highly_similar_theme_rejected(
        self, memory_entries_rich: list[MemoryFolderEntry]
    ) -> None:
        enforcer = BoredomBanEnforcer(coach_id="TST")
        # "Overcoming imposter syndrome in high-achieving women" is in memory (20 days ago)
        # Testing with a very similar phrase
        result = enforcer.check_theme_novelty(
            proposed_theme="Overcoming imposter syndrome in women who achieve",
            memory_entries=memory_entries_rich,
        )
        # Should be rejected (high similarity)
        assert result.similarity_score > THEME_COSINE_REJECT_THRESHOLD
        assert result.status == BoredomBanVectorStatus.REJECT_BOREDOM_BAN

    def test_cold_start_does_not_crash(self) -> None:
        """Spec §6: cold start returns MEMORY_ABSENT_ASSUMED_NOVEL, no crash."""
        enforcer = BoredomBanEnforcer(coach_id="TST")
        result = enforcer.check_theme_novelty(
            proposed_theme="Why diets don't work",
            memory_entries=[],  # Cold start
        )
        assert result.memory_absent is True
        assert result.status == BoredomBanVectorStatus.MEMORY_ABSENT_ASSUMED_NOVEL

    def test_distinct_theme_passes(
        self, memory_entries_rich: list[MemoryFolderEntry]
    ) -> None:
        enforcer = BoredomBanEnforcer(coach_id="TST")
        result = enforcer.check_theme_novelty(
            proposed_theme="How to structure a morning routine for peak neuroscience",
            memory_entries=memory_entries_rich,
        )
        # Novel theme should pass
        assert result.status in (
            BoredomBanVectorStatus.PASS,
            BoredomBanVectorStatus.MEMORY_ABSENT_ASSUMED_NOVEL,
        )

    def test_stage_1_full_run_cold_start_passes_without_halt(self) -> None:
        """Spec §6: Cold start → MEMORY_ABSENT → pipeline does not halt."""
        enforcer = BoredomBanEnforcer(coach_id="TST")
        result = enforcer.run_stage_1(
            proposed_themes=["Why diets don't work"],
            memory_entries=[],
        )
        assert result.final_clearance is True
        assert result.overall_verdict == OverallNoveltyVerdict.MEMORY_ABSENT
        assert result.memory_absent_log == "[MEMORY_ABSENT_ASSUMED_NOVEL]"


class TestFR25_AC3:
    """AC3: Structural fatigue — 4th LIST02 in same week → STRUCTURAL_FATIGUE.

    Spec §8 AC3: 'The orchestrator plans 4 Shocking Listicle (LIST02) layouts
    in the same week. Stage 3 throws [REJECT: STRUCTURAL_FATIGUE] on the 4th,
    forcing it to reshape into a Case Study.'
    Failure Example: 'System allows 4 identical listicles.'
    """

    def _make_list02_entries(self, count: int, coach_id: str = "TST") -> list[MemoryFolderEntry]:
        """Create `count` LIST02 entries within the last 7 days."""
        today = datetime.now(timezone.utc).date()
        return [
            MemoryFolderEntry(
                skill_id=f"SKILL-LIST02-{coach_id}-E-PRO-N-2026030{i+1}-001",
                coach_id=coach_id,
                thematic_payload=f"Theme {i}",
                metaphor_vehicle=f"Metaphor {i}",
                archetype_format="LIST02",
                published_date=today - timedelta(days=i),
            )
            for i in range(count)
        ]

    def test_fourth_list02_triggers_structural_fatigue(self) -> None:
        enforcer = BoredomBanEnforcer(coach_id="TST")
        # 4 LIST02 entries in last 7 days
        entries = self._make_list02_entries(4)
        result = enforcer.check_structural_fatigue(
            archetype_format="LIST02",
            memory_entries=entries,
            suggested_alternative="CASE03",
        )
        assert result.status == BoredomBanVectorStatus.REJECT_STRUCTURAL_FATIGUE
        assert result.frequency_14_days == 4  # > 3 = fatigued

    def test_three_list02_does_not_trigger_fatigue(self) -> None:
        enforcer = BoredomBanEnforcer(coach_id="TST")
        entries = self._make_list02_entries(3)
        result = enforcer.check_structural_fatigue(
            archetype_format="LIST02",
            memory_entries=entries,
        )
        # 3 is NOT > 3, so should pass
        assert result.status == BoredomBanVectorStatus.PASS
        assert result.frequency_14_days == 3

    def test_stage_3_full_run_produces_till_done_payload(self) -> None:
        enforcer = BoredomBanEnforcer(coach_id="TST")
        entries = self._make_list02_entries(4)
        result = enforcer.run_stage_3(
            draft_text="The 5 shocking secrets nobody tells you about...",
            archetype_format="LIST02",
            memory_entries=entries,
            suggested_alternative_archetype="CASE03",
        )
        assert result.overall_verdict == OverallNoveltyVerdict.BLOCKED
        assert result.final_clearance is False
        assert len(result.till_done_payloads) >= 1
        # TillDone must instruct mutation to an alternative archetype
        payload = result.till_done_payloads[0]
        assert "LIST02" in payload.rejection_detail
        assert "CASE03" in payload.mutation_command or "archetype" in payload.mutation_command.lower()


class TestFR25_AC4:
    """AC4: ADR-01 — Coach Maria's memory check does NOT use Coach Emilio's data.

    Spec §8 AC4: 'When tracking the 8-week history of Coach Maria's metaphors,
    the query absolutely cannot read Coach Emilio's Episodic Memory.'
    Failure Example: 'System prevents Maria from using a marathon metaphor
    simply because Emilio used it yesterday.'
    """

    def test_coach_b_not_blocked_by_coach_a_metaphor(self) -> None:
        today = datetime.now(timezone.utc).date()

        # Emilio used "marathon" metaphor yesterday
        emilio_entries = [
            MemoryFolderEntry(
                skill_id="SKILL-STORY01-EMI-P-PRV-L-20260314-001",
                coach_id="EMI",
                thematic_payload="Running a business is like running a marathon",
                metaphor_vehicle="Running a marathon",
                archetype_format="STORY01",
                published_date=today - timedelta(days=1),
            )
        ]

        # Maria's enforcer must NOT use Emilio's entries (ADR-01)
        maria_enforcer = BoredomBanEnforcer(coach_id="MAR")
        result = maria_enforcer.check_metaphor_novelty(
            proposed_metaphor="Running a marathon through obstacles",
            memory_entries=emilio_entries,  # These are Emilio's entries!
        )
        # Maria should get MEMORY_ABSENT (her coach_id filtered out Emilio's entries)
        # OR PASS — she must NOT get REJECT due to Emilio's usage
        assert result.status != BoredomBanVectorStatus.REJECT_TILL_DONE_TRIGGERED, (
            "AC4 VIOLATION: Maria was blocked by Emilio's metaphor history!"
        )

    def test_coach_a_entries_filtered_for_coach_b_stage_3(self) -> None:
        today = datetime.now(timezone.utc).date()

        # Emilio has 4 LIST02s (would trigger structural fatigue)
        emilio_entries = [
            MemoryFolderEntry(
                skill_id=f"SKILL-LIST02-EMI-E-PRO-N-2026030{i}-001",
                coach_id="EMI",
                thematic_payload=f"Emilio theme {i}",
                metaphor_vehicle=f"Emilio metaphor {i}",
                archetype_format="LIST02",
                published_date=today - timedelta(days=i),
            )
            for i in range(4)
        ]

        # Maria's enforcer checking LIST02 — must NOT be blocked by Emilio's history
        maria_enforcer = BoredomBanEnforcer(coach_id="MAR")
        result = maria_enforcer.run_stage_3(
            draft_text="Maria's listicle content.",
            archetype_format="LIST02",
            memory_entries=emilio_entries,  # Emilio's entries only
        )
        # Maria should see cold start (no her own entries) → CLEAR or MEMORY_ABSENT
        assert result.overall_verdict in (
            OverallNoveltyVerdict.CLEAR,
            OverallNoveltyVerdict.MEMORY_ABSENT,
        ), (
            f"AC4 VIOLATION: Maria blocked with verdict={result.overall_verdict.value}. "
            "Emilio's data must not affect Maria's compilation."
        )


# ─── Cross-Spec Integration ────────────────────────────────────────────────────

class TestCrossSpecIntegration:
    """Cross-spec integration: FR22 + FR23 + FR25 working together."""

    def test_full_step10_pipeline(
        self,
        valid_archetype_container: str,
        negative_space_rich: NegativeSpaceObject,
        tmp_receipts: str,
    ) -> None:
        """Full pipeline: synthesize ID → register → run anti-draft → boredom ban."""
        receipt_chain = ReceiptChain(
            coach_acronym="EMI", log_dir=tmp_receipts
        )

        # FR23: Synthesize and register a skill
        archive = FingerprintArchiveEngine(coach_id="EMI", receipt_chain=receipt_chain)
        skill_id = archive.synthesize_skill_id(
            arch_id="STORY01",
            mood=MoodCode.PROCESSING,
            regulatory_frame=RegulatoryFrame.PREVENTION,
            cohort=AudienceCohort.LOYAL,
        )
        reg_result = archive.register_skill(
            skill_id=skill_id,
            assembly_status="COMPLETE",
            dep_eng_003_obj={"voice_dna": {"vocabulary": ["raw", "honest"]}},
            dep_eng_006_obj={"emotional_baseline": 0.72},
            dep_eng_016_obj={"mood_state": "Processing"},
        )
        assert reg_result.success is True
        assert skill_id.startswith("SKILL-STORY01-EMI-P-PRV-L-")

        # FR22: Run anti-draft calibration
        calibrator = AntiDraftCalibrator(coach_id="EMI", receipt_chain=receipt_chain)
        log = calibrator.run_full_calibration(
            compilation_request_id=skill_id,
            archetype_container_block=valid_archetype_container,
            archetype_id="STORY01",
            routing_mode=Level2Mode.PROCESSING,
            negative_space=negative_space_rich,
            draft_text=(
                "The meeting ended before anyone said what they actually meant. "
                "I'd watched this happen forty times — and I kept my mouth shut. "
                "That restraint felt professional. Looking back, it was cowardice."
            ),
            m3_undeniable_belief="Success requires sacrificing authenticity",
        )
        assert not log.halted
        assert log.validation_pass.all_loaded()
        assert log.level_3_block is not None, "Level 3 must be loaded after successful calibration"
        assert log.level_3_block.loaded_first is True  # AC3: Level 3 first

        # FR25: Boredom Ban check
        enforcer = BoredomBanEnforcer(coach_id="EMI", receipt_chain=receipt_chain)
        ban_result = enforcer.run_stage_3(
            draft_text="EMI's compiled draft.",
            archetype_format="STORY01",
            memory_entries=[],  # Cold start for new coach
        )
        assert ban_result.final_clearance is True
        assert ban_result.overall_verdict == OverallNoveltyVerdict.MEMORY_ABSENT
