"""
Step 14 Integration Tests
V²WS + Full Cross-System Integration + Data Intelligence Layer
Covers ALL 18 specs: FR27, FR30, FR31, FR32, FR33, FR34, FR35, FR36,
                      FR37, FR41, FR42, FR43, FR45, FR46, FR47, FR48, FR49, FR50

Each test is prefixed with its FR number for traceability.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

# ── Models ─────────────────────────────────────────────
from src.ccp.models.cross_system_models import (
    ACTIVE_DAYS_PER_WEEK,
    ANTI_ESCALATION_LOCK_DAYS,
    AtlasRoadmap,
    AudienceCohort,
    CapacityTrack,
    ContentPerformanceRow,
    CrisisCheckResult,
    CrossPollinationSyllabus,
    DATA_ANALYST_MIN_ARC_N,
    DATA_ANALYST_MIN_GLOBAL_N,
    DeploymentManifest,
    DormancyRecoveryPayload,
    DormancyState,
    DormancyTier,
    ExcalidrawLayoutStrategy,
    ForensicLineage,
    FormatTag,
    GHOST_TYPING_TRIGGER_MS,
    IDGenerationPayload,
    InteractivePhase,
    InteractiveV2WSState,
    LATENCY_P95_BUDGET_MS,
    LatencyReceipt,
    ModelTier,
    MoodState,
    NOTION_PAGE_SECTIONS,
    NotionPagePayload,
    PERSON_ID_COACH_SEQUENCE_ZERO,
    ParameterUpdate,
    PipelineType,
    ReceiptBlock,
    ReceiptStatus,
    RECEIPT_GENESIS_MARKER,
    REFLECTION_DAYS_PER_WEEK,
    REST_DAYS_PER_WEEK,
    ROADMAP_DAYS,
    RoadmapDay,
    RoadmapDayType,
    SanitizedPerformanceBrief,
    SelectedPhoto,
    SkillFingerprintID,
    SovereignImageQuery,
    SovereignImageResolution,
    SovereignImageResult,
    SundayBotMeetingPayload,
    TenantRegistryRow,
    TenantStatus,
    TransparentCollageOutput,
    UnifiedExcalidrawPayload,
    UniversalAssetID,
    V2WSExcalidrawPayload,
    VisualPromptObject,
    WebinarModuleScript,
    WebinarPart,
    WEEKLY_OVERLOAD_MULTIPLIER,
    YOLO_SLIDE_HEIGHT,
    YOLO_SLIDE_WIDTH,
    YOLO_SPEAKER_NOTE_OFFSET_X,
    YoloIntake,
    RegulatoryFrame,
)

# ── Services ───────────────────────────────────────────
from src.ccp.services.receipt_chain_guard_service import ReceiptChainGuard
from src.ccp.services.universal_id_service import UniversalIDService
from src.ccp.services.crisis_guardian_service import CrisisGuardianService
from src.ccp.services.latency_protocol_service import (
    DEFAULT_TIER_MAP,
    LatencyProtocolService,
)
from src.ccp.services.dormancy_recovery_service import DormancyRecoveryService
from src.ccp.services.atlas_roadmap_service import AtlasRoadmapService
from src.ccp.services.v2ws_yolo_service import V2WSYoloService
from src.ccp.services.v2ws_interactive_service import V2WSInteractiveService
from src.ccp.services.transparent_collage_pipeline_service import (
    TransparentCollagePipelineService,
)
from src.ccp.services.unified_excalidraw_service import UnifiedExcalidrawService
from src.ccp.services.cross_system_intelligence_service import (
    CrossSystemIntelligenceService,
)
from src.ccp.services.cross_ecosystem_meeting_service import (
    CrossEcosystemMeetingService,
)
from src.ccp.services.publer_sync_service import PublerSyncService
from src.ccp.services.data_analyst_service import DataAnalystService
from src.ccp.services.notion_export_service import NotionExportService
from src.ccp.services.forensic_audit_service import ForensicAuditService
from src.ccp.services.single_tenant_deployment_service import (
    SingleTenantDeploymentService,
)
from src.ccp.services.sovereign_image_service import (
    SovereignImageService,
    SovereignViolationException,
)


COACH = "TST"


# ═════════════════════════════════════════════════════════
# FR47 — Receipt Chain Guard (DEP-ENG-041)
# ═════════════════════════════════════════════════════════

class TestFR47ReceiptChainGuard:

    def test_fr47_ac1_genesis_block_creation(self):
        """FR47 AC1: Genesis block has GENESIS previous hash + SHA-256."""
        guard = ReceiptChainGuard(coach_acronym=COACH)
        genesis = guard.create_genesis_block("ASSET-001")

        assert genesis.previous_receipt_hash == RECEIPT_GENESIS_MARKER
        assert genesis.status_code == ReceiptStatus.GENESIS
        assert len(genesis.current_receipt_hash) == 64  # SHA-256 hex

    def test_fr47_ac1_chain_linkage(self):
        """FR47 AC1: Each block links to previous via hash."""
        guard = ReceiptChainGuard(coach_acronym=COACH)
        genesis = guard.create_genesis_block("ASSET-001")
        block2 = guard.append_block(
            asset_id="ASSET-001",
            executing_agent="Artisan",
            input_payload={"text": "hello"},
            output_payload={"response": "world"},
        )

        assert block2.previous_receipt_hash == genesis.current_receipt_hash
        assert block2.current_receipt_hash != genesis.current_receipt_hash

    def test_fr47_ac2_quarantine_on_break(self):
        """FR47 AC2: QUARANTINED status on integrity violation."""
        guard = ReceiptChainGuard(coach_acronym=COACH)
        guard.create_genesis_block("ASSET-001")
        qblock = guard.quarantine_on_break("ASSET-001", "test_break")

        assert qblock.status_code == ReceiptStatus.QUARANTINED
        assert not guard.validate_chain_integrity()

    def test_fr47_ac3_publication_gate_passes(self):
        """FR47 AC3: Final gate passes on valid chain."""
        guard = ReceiptChainGuard(coach_acronym=COACH)
        guard.create_genesis_block("ASSET-001")
        guard.append_block(
            asset_id="ASSET-001",
            executing_agent="Artisan",
            input_payload="in",
            output_payload="out",
        )
        gate = guard.publication_gate("ASSET-001")

        assert gate.status_code == ReceiptStatus.SUCCESS
        assert guard.validate_chain_integrity()

    def test_fr47_ac3_publication_gate_fails_on_quarantine(self):
        """FR47 AC3: Final gate quarantines on broken chain."""
        guard = ReceiptChainGuard(coach_acronym=COACH)
        guard.create_genesis_block("ASSET-001")
        guard.quarantine_on_break("ASSET-001", "tampered")
        gate = guard.publication_gate("ASSET-001")

        assert gate.status_code == ReceiptStatus.QUARANTINED

    def test_fr47_ac4_append_only(self):
        """FR47 AC4: Chain only grows, never shrinks."""
        guard = ReceiptChainGuard(coach_acronym=COACH)
        guard.create_genesis_block("ASSET-001")
        assert guard.chain_length == 1
        guard.append_block(
            asset_id="ASSET-001",
            executing_agent="Agent",
            input_payload="a",
            output_payload="b",
        )
        assert guard.chain_length == 2


# ═════════════════════════════════════════════════════════
# FR46 — Universal Asset & Person ID (DEP-ENG-040)
# ═════════════════════════════════════════════════════════

class TestFR46UniversalID:

    def test_fr46_ac1_atomic_person_id(self):
        """FR46 AC1: Person IDs increment atomically."""
        svc = UniversalIDService(coach_acronym=COACH)
        pid1 = svc.generate_client_person_id()
        pid2 = svc.generate_client_person_id()

        assert pid1.person_id == f"PID-{COACH}-0001"
        assert pid2.person_id == f"PID-{COACH}-0002"

    def test_fr46_ac2_format_enum_guard(self):
        """FR46 AC2: Only valid pipeline/format enum values accepted."""
        svc = UniversalIDService(coach_acronym=COACH)
        uid = svc.generate_asset_id(
            pipeline=PipelineType.CCF,
            format_tag=FormatTag.CAROUSEL,
        )
        assert "CCF" in uid.asset_id
        assert "CAROUSEL" in uid.asset_id

        # Invalid enum should raise
        with pytest.raises((ValueError, KeyError)):
            PipelineType("INVALID")

    def test_fr46_ac3_coach_zero_assignment(self):
        """FR46 AC3: Coach person_id is always -0000."""
        svc = UniversalIDService(coach_acronym=COACH)
        coach_pid = svc.generate_coach_person_id()

        assert coach_pid.sequence == PERSON_ID_COACH_SEQUENCE_ZERO
        assert coach_pid.is_coach is True
        assert "0000" in coach_pid.person_id

    def test_fr46_ac4_id_format_structure(self):
        """FR46 AC4: Asset ID follows {COACH}-{PIPELINE}-{DATE}-{SEQ}-{FORMAT}."""
        svc = UniversalIDService(coach_acronym=COACH)
        uid = svc.generate_asset_id(
            pipeline=PipelineType.V2WS,
            format_tag=FormatTag.DECK,
            date_override="20250101",
        )
        parts = uid.asset_id.split("-")
        assert parts[0] == COACH
        assert parts[1] == "V2WS"
        assert parts[2] == "20250101"


# ═════════════════════════════════════════════════════════
# FR31 — Crisis Guardian (DEP-ENG-026)
# ═════════════════════════════════════════════════════════

class TestFR31CrisisGuardian:

    def test_fr31_ac1_sub_100ms_scan(self):
        """FR31 AC1: Crisis scan completes in <100ms."""
        svc = CrisisGuardianService(coach_acronym=COACH)
        is_crisis, keyword, latency = svc.scan_message("I want to kill myself")

        assert is_crisis is True
        assert keyword is not None
        assert latency < 100  # ms

    def test_fr31_ac2_zero_api_on_crisis(self):
        """FR31 AC2: Protocol triggers with zero external API calls."""
        svc = CrisisGuardianService(coach_acronym=COACH)
        result = svc.execute_crisis_protocol(
            user_id="U001",
            message_text="I want to end my life",
            admin_channel_id="ADMIN-001",
        )

        assert result is not None
        assert result.circuit_breaker.status == "TRIPPED"
        assert result.deployment.automation_halted is True

    def test_fr31_ac3_false_positive_grace(self):
        """FR31 AC3: Non-crisis text does not trigger."""
        svc = CrisisGuardianService(coach_acronym=COACH)
        result = svc.execute_crisis_protocol(
            user_id="U002",
            message_text="I had a wonderful day today",
            admin_channel_id="ADMIN-001",
        )
        assert result is None

    def test_fr31_ac4_coach_isolation(self):
        """FR31 AC4: User freeze is per-instance (coach-scoped)."""
        svc1 = CrisisGuardianService(coach_acronym="AAA")
        svc2 = CrisisGuardianService(coach_acronym="BBB")

        svc1.execute_crisis_protocol(
            user_id="U001",
            message_text="I want to kill myself",
            admin_channel_id="ADMIN",
        )

        assert svc1.is_user_frozen("U001") is True
        assert svc2.is_user_frozen("U001") is False

    def test_fr31_crisis_hold_dormancy_override(self):
        """FR31: CRISIS_HOLD blocks dormancy recovery."""
        svc = CrisisGuardianService(coach_acronym=COACH)
        svc.execute_crisis_protocol(
            user_id="U001",
            message_text="suicide",
            admin_channel_id="ADMIN",
        )
        override = svc.get_dormancy_state_override("U001")
        assert override == DormancyState.CRISIS_HOLD


# ═════════════════════════════════════════════════════════
# FR27 — <2s Latency Protocol (DEP-PROTO-017)
# ═════════════════════════════════════════════════════════

class TestFR27LatencyProtocol:

    def test_fr27_ac1_sub_2s_total(self):
        """FR27 AC1: Total pipeline latency < 2000ms."""
        svc = LatencyProtocolService(coach_acronym=COACH)
        svc.stage_1_ingress_crisis_scan(session_id="S1", raw_message="hello")
        svc.stage_2_context_intent_routing(session_id="S1", context_payload={})
        svc.stage_3_assembly_delivery(session_id="S1")

        assert svc.is_within_budget()
        assert svc.total_pipeline_latency_ms() < LATENCY_P95_BUDGET_MS

    def test_fr27_ac2_crisis_gate_stage1(self):
        """FR27 AC2: Stage 1 returns FAIL on crisis detection."""
        crisis_svc = CrisisGuardianService(coach_acronym=COACH)
        svc = LatencyProtocolService(coach_acronym=COACH)

        receipt = svc.stage_1_ingress_crisis_scan(
            session_id="S2",
            raw_message="I want to kill myself",
            crisis_scan_fn=crisis_svc.scan_message,
        )
        assert receipt.crisis_check == CrisisCheckResult.FAIL

    def test_fr27_ac4_default_tier_map(self):
        """FR27 AC4: Tier map contains expected agents."""
        agent_names = [t.agent for t in DEFAULT_TIER_MAP.tasks]
        assert "Liliane" in agent_names
        assert "Vidye" in agent_names
        assert "Artisan" in agent_names
        assert "Azaria" in agent_names

    def test_fr27_stage4_background(self):
        """FR27 Stage 4: Background offload has 0ms latency."""
        svc = LatencyProtocolService(coach_acronym=COACH)
        receipt = svc.stage_4_background_offload(session_id="S3")
        assert receipt.stage_name == "CBCS-RESPONSE-DISPATCH"
        assert receipt.latency_ms == 0


# ═════════════════════════════════════════════════════════
# FR30 — Dormancy Recovery (DEP-ENG-025)
# ═════════════════════════════════════════════════════════

class TestFR30DormancyRecovery:

    def test_fr30_ac1_3day_trigger(self):
        """FR30 AC1: Day 3 triggers TIER_1."""
        svc = DormancyRecoveryService(coach_acronym=COACH)
        tier = svc.classify_tier(3)
        assert tier == DormancyTier.TIER_1

    def test_fr30_ac1_tier_progression(self):
        """FR30 AC1: Tier escalation at correct thresholds."""
        svc = DormancyRecoveryService(coach_acronym=COACH)
        assert svc.classify_tier(2) is None
        assert svc.classify_tier(3) == DormancyTier.TIER_1
        assert svc.classify_tier(5) == DormancyTier.TIER_2
        assert svc.classify_tier(10) == DormancyTier.TIER_3
        assert svc.classify_tier(30) == DormancyTier.TIER_4

    def test_fr30_ac2_journaling_suppression(self):
        """FR30 AC2: Journaling suppressed in RECOVERY_MODE."""
        svc = DormancyRecoveryService(coach_acronym=COACH)
        assert svc.is_journaling_suppressed(DormancyState.RECOVERY_MODE_TIER_1)
        assert svc.is_journaling_suppressed(DormancyState.CRISIS_HOLD)
        assert not svc.is_journaling_suppressed(DormancyState.ACTIVE)

    def test_fr30_ac3_memory_injection(self):
        """FR30 AC3: Recovery payload contains stalled milestone."""
        svc = DormancyRecoveryService(coach_acronym=COACH)
        payload = svc.generate_recovery_payload(
            user_id="U001",
            days_silent=7,
            stalled_milestone="Week 2 Challenge",
            last_l3_fear="abandonment",
        )
        assert payload is not None
        assert payload.recovery_context.stalled_milestone == "Week 2 Challenge"
        assert payload.recovery_context.last_l3_fear == "abandonment"

    def test_fr30_ac4_coach_isolation(self):
        """FR30 AC4: Payload is scoped to coach_id."""
        svc = DormancyRecoveryService(coach_acronym=COACH)
        payload = svc.generate_recovery_payload(user_id="U001", days_silent=5)
        assert payload is not None
        assert payload.coach_id == COACH


# ═════════════════════════════════════════════════════════
# FR32 — Atlas Roadmap (DEP-ENG-027)
# ═════════════════════════════════════════════════════════

class TestFR32AtlasRoadmap:

    def test_fr32_ac1_track_classification(self):
        """FR32 AC1: Correct track from psychological profile."""
        svc = AtlasRoadmapService(coach_acronym=COACH)
        assert svc.classify_track(fear_score=0.9, agency_score=0.1) == CapacityTrack.RECOVERY
        assert svc.classify_track(fear_score=0.9, agency_score=0.1, coping_exhaustion=0.8) == CapacityTrack.RECOVERY
        assert svc.classify_track(fear_score=0.7, agency_score=0.3) == CapacityTrack.FOUNDATION
        assert svc.classify_track(fear_score=0.5, agency_score=0.6) == CapacityTrack.GROWTH
        assert svc.classify_track(fear_score=0.3, agency_score=0.7) == CapacityTrack.MOMENTUM
        assert svc.classify_track(fear_score=0.1, agency_score=0.9) == CapacityTrack.PEAK

    def test_fr32_ac2_4_1_2_matrix(self):
        """FR32 AC2: 28-day roadmap has 16 Active, 4 Reflection, 8 Rest."""
        svc = AtlasRoadmapService(coach_acronym=COACH)
        roadmap = svc.generate_roadmap(
            user_id="U001", track=CapacityTrack.GROWTH,
        )

        assert len(roadmap.roadmap_architecture) == ROADMAP_DAYS
        active = sum(1 for d in roadmap.roadmap_architecture if d.type == RoadmapDayType.ACTIVE)
        reflection = sum(1 for d in roadmap.roadmap_architecture if d.type == RoadmapDayType.REFLECTION)
        rest = sum(1 for d in roadmap.roadmap_architecture if d.type == RoadmapDayType.REST)

        assert active == ACTIVE_DAYS_PER_WEEK * 4  # 16
        assert reflection == REFLECTION_DAYS_PER_WEEK * 4  # 4
        assert rest == REST_DAYS_PER_WEEK * 4  # 8

    def test_fr32_ac3_progressive_overload(self):
        """FR32 AC3: +10% intensity per week."""
        svc = AtlasRoadmapService(coach_acronym=COACH)
        roadmap = svc.generate_roadmap(
            user_id="U001", track=CapacityTrack.GROWTH, base_intensity=0.5,
        )

        # Get first ACTIVE day of each week
        for week in range(1, 5):
            week_active = [
                d for d in roadmap.roadmap_architecture
                if d.week_number == week and d.type == RoadmapDayType.ACTIVE
            ]
            expected = round(0.5 * (WEEKLY_OVERLOAD_MULTIPLIER ** (week - 1)), 4)
            assert week_active[0].assigned_intensity_load == expected

    def test_fr32_ac3_rest_always_zero(self):
        """FR32 AC3: REST days always intensity 0.00."""
        svc = AtlasRoadmapService(coach_acronym=COACH)
        roadmap = svc.generate_roadmap(
            user_id="U001", track=CapacityTrack.PEAK,
        )

        for d in roadmap.roadmap_architecture:
            if d.type == RoadmapDayType.REST:
                assert d.assigned_intensity_load == 0.0

    def test_fr32_ac4_anti_escalation_lock(self):
        """FR32 AC4: Recovery cannot escalate before Day 15."""
        svc = AtlasRoadmapService(coach_acronym=COACH)
        assert svc.check_anti_escalation_lock(
            current_track=CapacityTrack.RECOVERY, days_in_current_track=10,
        ) is True
        assert svc.check_anti_escalation_lock(
            current_track=CapacityTrack.RECOVERY, days_in_current_track=15,
        ) is False


# ═════════════════════════════════════════════════════════
# FR33 — V²WS YOLO Mode (DEP-ENG-028)
# ═════════════════════════════════════════════════════════

class TestFR33YoloMode:

    def _make_intake(self) -> YoloIntake:
        return YoloIntake(
            actionable_lesson_thesis="Fear is a compass",
            target_audience_segment="Executive women 35-50",
            final_offer_cta="Join the 90-day program",
            key_stories_array=["Story A", "Story B"],
            tone_energy_constraint="Calm authority",
        )

    def test_fr33_ac1_five_input_gate(self):
        """FR33 AC1: All 5 inputs must be present."""
        svc = V2WSYoloService(coach_acronym=COACH)
        intake = self._make_intake()
        assert svc.validate_intake(intake) is True

        with pytest.raises(ValidationError):
            YoloIntake(
                actionable_lesson_thesis="",
                target_audience_segment="seg",
                final_offer_cta="cta",
                key_stories_array=["s"],
                tone_energy_constraint="tone",
            )

    def test_fr33_ac2_no_approval_pauses(self):
        """FR33 AC2: YOLO pipeline runs straight through."""
        svc = V2WSYoloService(coach_acronym=COACH)
        payload = svc.run_yolo_pipeline(self._make_intake())
        assert isinstance(payload, V2WSExcalidrawPayload)
        assert len(payload.elements) > 0

    def test_fr33_ac3_valid_excalidraw(self):
        """FR33 AC3: Output is valid Excalidraw JSON."""
        svc = V2WSYoloService(coach_acronym=COACH)
        payload = svc.run_yolo_pipeline(self._make_intake())

        assert payload.type == "excalidraw"
        assert payload.version == 2
        for elem in payload.elements:
            assert "id" in elem
            assert "type" in elem

    def test_fr33_ac4_speaker_notes_outside_viewport(self):
        """FR33 AC4: Speaker notes x > slide boundary."""
        svc = V2WSYoloService(coach_acronym=COACH)
        payload = svc.run_yolo_pipeline(self._make_intake())

        speaker_notes = [
            e for e in payload.elements
            if isinstance(e.get("text", ""), str)
            and e.get("text", "").startswith("SPEAKER NOTES:")
        ]
        assert len(speaker_notes) > 0
        for note in speaker_notes:
            assert note["x"] >= YOLO_SPEAKER_NOTE_OFFSET_X


# ═════════════════════════════════════════════════════════
# FR34 — V²WS Interactive Mode (DEP-ENG-029)
# ═════════════════════════════════════════════════════════

class TestFR34InteractiveMode:

    def test_fr34_ac1_algorithmic_stop(self):
        """FR34 AC1: Session stops at WAITING_FOR_MODULE_APPROVAL."""
        svc = V2WSInteractiveService(coach_acronym=COACH)
        state = svc.create_session()
        svc.submit_outline(state.session_id, "Outline text")
        state = svc.approve_outline(state.session_id)

        state = svc.submit_module(state.session_id, 1, "Hook content")
        assert state.current_phase == InteractivePhase.WAITING_FOR_MODULE_APPROVAL

    def test_fr34_ac2_revision_routing(self):
        """FR34 AC2: Rejection routes back to MODULE_ASSEMBLY."""
        svc = V2WSInteractiveService(coach_acronym=COACH)
        state = svc.create_session()
        svc.submit_outline(state.session_id, "Outline")
        svc.approve_outline(state.session_id)
        svc.submit_module(state.session_id, 1, "Draft content")

        state = svc.reject_module(state.session_id, 1, "Needs more energy")
        assert state.current_phase == InteractivePhase.MODULE_ASSEMBLY

        # Module content cleared for re-generation
        module = [m for m in state.modules if m.index == 1][0]
        assert module.status == "REVISION_REQUESTED"

    def test_fr34_ac3_image_embedding(self):
        """FR34 AC3: Images can be attached to modules."""
        svc = V2WSInteractiveService(coach_acronym=COACH)
        state = svc.create_session()
        svc.submit_outline(state.session_id, "Outline")
        svc.approve_outline(state.session_id)

        svc.attach_image_to_module(state.session_id, 1, "base64data")
        module = [m for m in state.modules if m.index == 1][0]
        assert module.asset_base64 == "base64data"

    def test_fr34_ac4_thread_isolation(self):
        """FR34 AC4: Sessions are coach-scoped."""
        svc = V2WSInteractiveService(coach_acronym=COACH)
        state = svc.create_session()
        assert state.coach_id == COACH

    def test_fr34_stale_timeout(self):
        """FR34: 12-hour stale sweep threshold."""
        svc = V2WSInteractiveService(coach_acronym=COACH)
        assert svc.stale_timeout_hours == 12


# ═════════════════════════════════════════════════════════
# FR36 — Transparent Collage Pipeline (DEP-ENG-031)
# ═════════════════════════════════════════════════════════

class TestFR36TransparentCollage:

    def test_fr36_ac1_visual_reasoning(self):
        """FR36 AC1: Visual prompt contains emotion + pose + prop."""
        svc = TransparentCollagePipelineService(coach_acronym=COACH)
        prompt = svc.generate_visual_prompt(
            emotion="confidence", pose="standing", prop="megaphone",
        )
        assert "confidence" in prompt.t2i_prompt
        assert "megaphone" in prompt.t2i_prompt

    def test_fr36_ac2_gmg03_stub(self):
        """FR36 AC2: T2I generation returns valid base64."""
        svc = TransparentCollagePipelineService(coach_acronym=COACH)
        prompt = VisualPromptObject(
            emotion="joy", pose="jumping", prop="balloon",
        )
        b64 = svc.generate_image_stub(prompt)
        assert len(b64) > 0

    def test_fr36_ac3_alpha_extraction(self):
        """FR36 AC3: Alpha extraction returns processed data."""
        svc = TransparentCollagePipelineService(coach_acronym=COACH)
        result, failed = svc.extract_alpha("base64data")
        assert failed is False

    def test_fr36_ac4_fallback_polaroid(self):
        """FR36 AC4: Polaroid fallback returns data."""
        svc = TransparentCollagePipelineService(coach_acronym=COACH)
        result = svc.apply_polaroid_fallback("base64data")
        assert result == "base64data"

    def test_fr36_full_pipeline(self):
        """FR36: Full pipeline produces TransparentCollageOutput."""
        svc = TransparentCollagePipelineService(coach_acronym=COACH)
        output = svc.run_pipeline(
            emotion="determination", pose="running", prop="torch",
        )
        assert isinstance(output, TransparentCollageOutput)
        assert len(output.base64_png) > 0
        assert output.source_emotion == "determination"


# ═════════════════════════════════════════════════════════
# FR35 — Unified Excalidraw Pipeline (DEP-ENG-030)
# ═════════════════════════════════════════════════════════

class TestFR35UnifiedExcalidraw:

    def test_fr35_ac1_transparent_collage_integration(self):
        """FR35 AC1: Images from DEP-ENG-031 embedded in output."""
        svc = UnifiedExcalidrawService(coach_acronym=COACH)
        img = TransparentCollageOutput(
            asset_id="IMG-001", base64_png="data123",
        )
        payload = svc.compile_payload(
            strategy=ExcalidrawLayoutStrategy.HORIZONTAL_SLIDE_SEQUENCE,
            titles=["Title 1"],
            body_texts=["Body 1"],
            images=[img],
        )
        assert len(payload.files) == 1

    def test_fr35_ac2_cross_format(self):
        """FR35 AC2: Both horizontal and vertical layouts work."""
        svc = UnifiedExcalidrawService(coach_acronym=COACH)

        h_payload = svc.compile_payload(
            strategy=ExcalidrawLayoutStrategy.HORIZONTAL_SLIDE_SEQUENCE,
            titles=["A", "B"],
            body_texts=["a", "b"],
        )
        v_payload = svc.compile_payload(
            strategy=ExcalidrawLayoutStrategy.VERTICAL_SCROLLING,
            titles=["A", "B"],
            body_texts=["a", "b"],
        )

        # Horizontal: x values differ, y same
        h_rects = [e for e in h_payload.elements if e["type"] == "rectangle"]
        assert h_rects[0]["x"] != h_rects[1]["x"]
        assert h_rects[0]["y"] == h_rects[1]["y"]

        # Vertical: y values differ, x same
        v_rects = [e for e in v_payload.elements if e["type"] == "rectangle"]
        assert v_rects[0]["y"] != v_rects[1]["y"]
        assert v_rects[0]["x"] == v_rects[1]["x"]

    def test_fr35_ac3_brand_consistency(self):
        """FR35 AC3: Stroke and fill colors enforced."""
        svc = UnifiedExcalidrawService(coach_acronym=COACH)
        payload = svc.compile_payload(
            strategy=ExcalidrawLayoutStrategy.HORIZONTAL_SLIDE_SEQUENCE,
            titles=["T"],
            body_texts=["B"],
        )
        rects = [e for e in payload.elements if e["type"] == "rectangle"]
        assert rects[0]["strokeColor"] == "#111827"
        assert rects[0]["backgroundColor"] == "#ffffff"

    def test_fr35_ac4_native_text(self):
        """FR35 AC4: Text elements are type='text' (editable)."""
        svc = UnifiedExcalidrawService(coach_acronym=COACH)
        payload = svc.compile_payload(
            strategy=ExcalidrawLayoutStrategy.HORIZONTAL_SLIDE_SEQUENCE,
            titles=["Title"],
            body_texts=["Body"],
        )
        texts = [e for e in payload.elements if e["type"] == "text"]
        assert len(texts) >= 2  # title + body


# ═════════════════════════════════════════════════════════
# FR37 — Cross-System Intelligence (DEP-ENG-032)
# ═════════════════════════════════════════════════════════

class TestFR37CrossSystemIntelligence:

    def _make_client_data(self, n: int) -> list[dict]:
        return [
            {
                "client_id": f"C{i:03d}",
                "pain_points": ["fear", "overwhelm"] if i % 2 == 0 else ["isolation"],
                "coping_mechanisms": ["journaling"] if i % 3 == 0 else ["exercise"],
            }
            for i in range(n)
        ]

    def test_fr37_ac1_aggregation(self):
        """FR37 AC1: Data aggregation from MemoryFolder sweep."""
        svc = CrossSystemIntelligenceService(coach_acronym=COACH)
        result = svc.run_sunday_bot_meeting(client_data=self._make_client_data(5))

        assert result is not None
        assert result.aggregation_metrics.active_clients_analyzed == 5

    def test_fr37_ac1_abort_below_min(self):
        """FR37 §6: Abort if <3 active clients."""
        svc = CrossSystemIntelligenceService(coach_acronym=COACH)
        result = svc.run_sunday_bot_meeting(client_data=self._make_client_data(2))
        assert result is None

    def test_fr37_ac2_pii_zero_trust(self):
        """FR37 AC2: No PII in output."""
        svc = CrossSystemIntelligenceService(coach_acronym=COACH)
        result = svc.run_sunday_bot_meeting(client_data=self._make_client_data(5))
        assert result is not None
        assert result.pii_leak_status == "CLEAN"

    def test_fr37_ac4_coach_scoped(self):
        """FR37 AC4: Output is scoped to coach_id."""
        svc = CrossSystemIntelligenceService(coach_acronym=COACH)
        result = svc.run_sunday_bot_meeting(client_data=self._make_client_data(4))
        assert result is not None
        assert result.coach_id == COACH


# ═════════════════════════════════════════════════════════
# FR41 — Cross-Ecosystem Meeting (DEP-ENG-036)
# ═════════════════════════════════════════════════════════

class TestFR41CrossEcosystemMeeting:

    def _make_briefs(self, n: int) -> list[SanitizedPerformanceBrief]:
        return [
            SanitizedPerformanceBrief(
                tenant_id=f"T{i:03d}",
                coach_id=f"C{i:02d}",
                format_performance={"carousel": 0.8, "reel": 0.2},
                hook_performance={"question": 0.6, "stat": 0.4},
            )
            for i in range(n)
        ]

    def test_fr41_ac1_privacy_firewall(self):
        """FR41 AC1: No string values in performance briefs."""
        with pytest.raises(ValidationError):
            SanitizedPerformanceBrief(
                tenant_id="T001",
                coach_id="TST",
                format_performance={"carousel": "high"},  # type: ignore
            )

    def test_fr41_ac2_smoothing(self):
        """FR41 AC2: Statistical smoothing with min ecosystems."""
        svc = CrossEcosystemMeetingService(coach_acronym=COACH)
        briefs = self._make_briefs(4)
        smoothed = svc.compute_smoothed_metrics(briefs)
        assert "format_avg" in smoothed
        assert smoothed["format_avg"]["carousel"] == 0.8

    def test_fr41_ac2_abort_below_min(self):
        """FR41 AC2: No syllabus if <3 ecosystems."""
        svc = CrossEcosystemMeetingService(coach_acronym=COACH)
        result = svc.generate_syllabus(briefs=self._make_briefs(2))
        assert result is None

    def test_fr41_ac3_syllabus_generation(self):
        """FR41 AC3: Syllabus has required sections."""
        svc = CrossEcosystemMeetingService(coach_acronym=COACH)
        result = svc.generate_syllabus(briefs=self._make_briefs(4))
        assert result is not None
        assert isinstance(result, CrossPollinationSyllabus)
        assert result.total_ecosystems == 4

    def test_fr41_ac4_opt_out(self):
        """FR41 AC4: Opted-out tenants are excluded."""
        svc = CrossEcosystemMeetingService(coach_acronym=COACH)
        svc.set_opt_out("T000")
        svc.set_opt_out("T001")
        briefs = self._make_briefs(5)
        result = svc.generate_syllabus(briefs=briefs)
        assert result is not None
        assert result.total_ecosystems == 3  # 5 - 2 opted out


# ═════════════════════════════════════════════════════════
# FR42 — Publer Sync (DEP-ENG-037)
# ═════════════════════════════════════════════════════════

class TestFR42PublerSync:

    def test_fr42_ac1_scheduling(self):
        """FR42 AC1: Content scheduling creates a row."""
        svc = PublerSyncService(coach_acronym=COACH)
        row = svc.schedule_content(
            universal_asset_id="ASSET-001",
            publer_post_id="PUB-123",
            platform="instagram",
        )
        assert row.universal_asset_id == "ASSET-001"
        assert svc.store_size == 1

    def test_fr42_ac2_engagement_rate_math(self):
        """FR42 AC2: (saves + shares + comments + likes) / reach."""
        svc = PublerSyncService(coach_acronym=COACH)
        svc.schedule_content(
            universal_asset_id="ASSET-001",
            publer_post_id="PUB-123",
            platform="instagram",
        )
        row = svc.ingest_48h_metrics(
            universal_asset_id="ASSET-001",
            reach=1000,
            saves=50,
            shares=30,
            comments=20,
            likes=100,
        )
        expected = (50 + 30 + 20 + 100) / 1000
        assert row.engagement_rate == expected

    def test_fr42_ac2_zero_reach(self):
        """FR42 AC2: Zero reach → 0.0 engagement rate."""
        row = ContentPerformanceRow(
            universal_asset_id="ASSET-002",
            reach=0, saves=10, shares=5, comments=2, likes=20,
        )
        assert row.computed_engagement_rate == 0.0

    def test_fr42_ac3_notion_page_creation(self):
        """FR42 AC3: Publication confirmation stores URL."""
        svc = PublerSyncService(coach_acronym=COACH)
        svc.schedule_content(
            universal_asset_id="ASSET-001",
            publer_post_id="PUB-123",
            platform="instagram",
        )
        row = svc.confirm_publication(
            universal_asset_id="ASSET-001",
            platform_post_url="https://instagram.com/p/123",
        )
        assert row.platform_post_url == "https://instagram.com/p/123"
        assert row.published_at is not None

    def test_fr42_ac4_idempotent(self):
        """FR42 AC4: Upsert by universal_asset_id is idempotent."""
        svc = PublerSyncService(coach_acronym=COACH)
        svc.schedule_content(
            universal_asset_id="ASSET-001",
            publer_post_id="PUB-123",
            platform="instagram",
        )
        svc.schedule_content(
            universal_asset_id="ASSET-001",
            publer_post_id="PUB-456",
            platform="instagram",
        )
        assert svc.store_size == 1
        row = svc.get_performance("ASSET-001")
        assert row is not None
        assert row.publer_post_id == "PUB-456"

    def test_fr42_snapshot(self):
        """FR42: 7-day and 30-day snapshots stored."""
        svc = PublerSyncService(coach_acronym=COACH)
        svc.schedule_content(
            universal_asset_id="ASSET-001",
            publer_post_id="PUB-123",
            platform="instagram",
        )
        svc.ingest_snapshot(
            universal_asset_id="ASSET-001",
            snapshot_day=7,
            snapshot_data={"reach": 2000},
        )
        row = svc.get_performance("ASSET-001")
        assert row is not None
        assert row.day_7_snapshot == {"reach": 2000}


# ═════════════════════════════════════════════════════════
# FR43 — Data Analyst Agent (DEP-ENG-038)
# ═════════════════════════════════════════════════════════

class TestFR43DataAnalyst:

    def _make_rows(self, n: int) -> list[ContentPerformanceRow]:
        return [
            ContentPerformanceRow(
                universal_asset_id=f"ASSET-{i:03d}",
                platform="instagram",
                reach=1000,
                saves=50, shares=30, comments=20, likes=100,
                engagement_rate=0.2,
            )
            for i in range(n)
        ]

    def test_fr43_ac1_minimum_sample_guard(self):
        """FR43 AC1: N >= 10 global, N >= 5 per arc."""
        svc = DataAnalystService(coach_acronym=COACH)
        rows = self._make_rows(5)

        passes, reason = svc.check_minimum_sample(
            rows=rows,
            arc_type_groups={"discovery": rows},
        )
        assert passes is False
        assert "Global" in reason

    def test_fr43_ac1_arc_minimum(self):
        """FR43 AC1: Per-arc minimum enforced."""
        svc = DataAnalystService(coach_acronym=COACH)
        rows = self._make_rows(12)

        passes, reason = svc.check_minimum_sample(
            rows=rows,
            arc_type_groups={
                "discovery": rows[:3],
                "challenge": rows[3:],
            },
        )
        assert passes is False
        assert "Arc" in reason

    def test_fr43_ac2_parameter_update(self):
        """FR43 AC2: Successful parameter update generation."""
        svc = DataAnalystService(coach_acronym=COACH)
        rows = self._make_rows(15)

        update = svc.generate_parameter_update(
            rows=rows,
            arc_type_groups={
                "discovery": rows[:8],
                "challenge": rows[8:],
            },
        )
        assert update is not None
        assert isinstance(update, ParameterUpdate)
        assert "discovery" in update.arc_priority_weights

    def test_fr43_ac3_aborts_below_min(self):
        """FR43 AC3: Returns None below minimum."""
        svc = DataAnalystService(coach_acronym=COACH)
        rows = self._make_rows(5)
        update = svc.generate_parameter_update(
            rows=rows,
            arc_type_groups={"discovery": rows},
        )
        assert update is None

    def test_fr43_ac4_idempotent_tagging(self):
        """FR43 AC4: Re-tagging already-tagged rows is a no-op."""
        svc = DataAnalystService(coach_acronym=COACH)
        rows = self._make_rows(3)
        rows[0].analyst_reviewed = True

        tagged = svc.tag_rows_as_reviewed(rows)
        assert tagged == 2

        tagged_again = svc.tag_rows_as_reviewed(rows)
        assert tagged_again == 0


# ═════════════════════════════════════════════════════════
# FR45 — Notion Export Pipeline (DEP-ENG-039)
# ═════════════════════════════════════════════════════════

class TestFR45NotionExport:

    def test_fr45_ac1_seven_sections(self):
        """FR45 AC1: Notion page has exactly 7 sections."""
        svc = NotionExportService(coach_acronym=COACH)
        payload = svc.build_page_payload(
            parent_database_id="DB-001",
            title="Test Post",
            universal_asset_id="ASSET-001",
        )
        assert svc.validate_section_count(payload)
        assert len(payload.sections) == NOTION_PAGE_SECTIONS

    def test_fr45_ac2_sovereign_image(self):
        """FR45 AC2: Coach Photo section requires a URL."""
        svc = NotionExportService(coach_acronym=COACH)
        payload_with = svc.build_page_payload(
            parent_database_id="DB-001",
            title="Test",
            universal_asset_id="ASSET-001",
            coach_photo_url="https://example.com/photo.jpg",
        )
        assert svc.validate_sovereign_image(payload_with)

        payload_without = svc.build_page_payload(
            parent_database_id="DB-001",
            title="Test",
            universal_asset_id="ASSET-002",
        )
        assert not svc.validate_sovereign_image(payload_without)

    def test_fr45_ac3_approval_polling(self):
        """FR45 AC3: Approval status tracking."""
        svc = NotionExportService(coach_acronym=COACH)
        assert svc.check_approval("ASSET-001") == "PENDING"
        svc.set_approval_status("ASSET-001", "APPROVED")
        assert svc.check_approval("ASSET-001") == "APPROVED"

    def test_fr45_ac4_backoff(self):
        """FR45 AC4: Exponential backoff computation."""
        svc = NotionExportService(coach_acronym=COACH)
        assert svc.compute_backoff_seconds(0) == 1.0
        assert svc.compute_backoff_seconds(1) == 2.0
        assert svc.compute_backoff_seconds(2) == 4.0
        assert svc.compute_backoff_seconds(10) == 120.0  # capped

    def test_fr45_block_chunking(self):
        """FR45: Blocks chunked at 100."""
        svc = NotionExportService(coach_acronym=COACH)
        blocks = [{"type": "paragraph"} for _ in range(250)]
        chunks = svc.chunk_blocks(blocks)
        assert len(chunks) == 3
        assert len(chunks[0]) == 100
        assert len(chunks[2]) == 50


# ═════════════════════════════════════════════════════════
# FR48 — Forensic Audit Protocol (DEP-ENG-042)
# ═════════════════════════════════════════════════════════

class TestFR48ForensicAudit:

    def test_fr48_ac1_fingerprint_syntax(self):
        """FR48 AC1: SKILL-{ARCH}-{COACH}-{MOOD}-{FRAME}-{COHORT}-{DATE}-{SEQ}."""
        svc = ForensicAuditService(coach_acronym=COACH)
        fp = svc.generate_skill_fingerprint(
            archetype_template_id="ARCH001",
            mood=MoodState.DISCOVERY,
            regulatory_frame=RegulatoryFrame.PROMOTION,
            audience_cohort=AudienceCohort.NEW,
        )
        parts = fp.skill_id.split("-")
        assert parts[0] == "SKILL"
        assert parts[1] == "ARCH001"
        assert parts[2] == COACH

    def test_fr48_ac2_asset_binding(self):
        """FR48 AC2: Asset bound to fingerprint."""
        svc = ForensicAuditService(coach_acronym=COACH)
        fp = svc.generate_skill_fingerprint(
            archetype_template_id="ARCH001",
            mood=MoodState.ESCAPE,
            regulatory_frame=RegulatoryFrame.PREVENTION,
            audience_cohort=AudienceCohort.LOYAL,
        )
        result = svc.bind_asset_to_fingerprint(
            asset_id="ASSET-001",
            skill_fingerprint_id=fp.skill_id,
        )
        assert result is True
        assert "ASSET-001" in fp.outputs

    def test_fr48_ac3_dep_hashing(self):
        """FR48 AC3: Dependency snapshot hashed."""
        svc = ForensicAuditService(coach_acronym=COACH)
        fp = svc.generate_skill_fingerprint(
            archetype_template_id="ARCH001",
            mood=MoodState.PROCESSING,
            regulatory_frame=RegulatoryFrame.PROMOTION,
            audience_cohort=AudienceCohort.DEVELOPING,
            dep_versions={"DEP-ENG-006": "v1.2.3", "DEP-LIB-001": "v2.0"},
        )
        assert "DEP-ENG-006" in fp.dep_snapshot
        assert len(fp.dep_snapshot["DEP-ENG-006"]) == 16  # SHA-256 truncated

    def test_fr48_ac4_forensic_reconstruction(self):
        """FR48 AC4: Full lineage trace."""
        svc = ForensicAuditService(coach_acronym=COACH)
        fp = svc.generate_skill_fingerprint(
            archetype_template_id="ARCH001",
            mood=MoodState.STATUS,
            regulatory_frame=RegulatoryFrame.PROMOTION,
            audience_cohort=AudienceCohort.NEW,
        )
        svc.bind_asset_to_fingerprint(
            asset_id="ASSET-001",
            skill_fingerprint_id=fp.skill_id,
        )
        lineage = svc.trace_lineage("ASSET-001")
        assert lineage is not None
        assert isinstance(lineage, ForensicLineage)
        assert lineage.skill_fingerprint_id == fp.skill_id

    def test_fr48_unknown_asset_returns_none(self):
        """FR48: Unknown asset returns None."""
        svc = ForensicAuditService(coach_acronym=COACH)
        assert svc.trace_lineage("NONEXISTENT") is None


# ═════════════════════════════════════════════════════════
# FR49 — Single-Tenant Deployment (DEP-ENG-043)
# ═════════════════════════════════════════════════════════

class TestFR49SingleTenantDeployment:

    def _make_manifest(self) -> DeploymentManifest:
        return DeploymentManifest(
            coach_name="Test Coach",
            coach_acronym=COACH,
            admin_email="test@example.com",
        )

    def test_fr49_ac1_full_stack(self):
        """FR49 AC1: E2E orchestration produces ACTIVE tenant."""
        svc = SingleTenantDeploymentService()
        row = svc.deploy_full_stack(self._make_manifest())

        assert row is not None
        assert row.status == TenantStatus.ACTIVE
        assert row.infrastructure.supabase_project_ref != ""
        assert row.infrastructure.neo4j_uri != ""

    def test_fr49_ac2_namespace_decoupling(self):
        """FR49 AC2: Coach acronym in infrastructure names."""
        svc = SingleTenantDeploymentService()
        row = svc.deploy_full_stack(self._make_manifest())

        assert row is not None
        assert COACH.lower() in row.infrastructure.supabase_project_ref
        assert COACH.lower() in row.infrastructure.neo4j_uri

    def test_fr49_ac3_schema_injection(self):
        """FR49 AC3: Infrastructure details populated."""
        svc = SingleTenantDeploymentService()
        row = svc.deploy_full_stack(self._make_manifest())

        assert row is not None
        assert row.infrastructure.supabase_rest_url.startswith("https://")

    def test_fr49_ac4_idempotency_guard(self):
        """FR49 AC4: Second deployment of same coach returns None."""
        svc = SingleTenantDeploymentService()
        row1 = svc.deploy_full_stack(self._make_manifest())
        row2 = svc.deploy_full_stack(self._make_manifest())

        assert row1 is not None
        assert row2 is None
        assert svc.registry_size == 1


# ═════════════════════════════════════════════════════════
# FR50 — Sovereign Image Rule (DEP-ENG-044)
# ═════════════════════════════════════════════════════════

class TestFR50SovereignImage:

    def test_fr50_ac1_metadata_intersection(self):
        """FR50 AC1: Query Photo Deck by mood + format."""
        svc = SovereignImageService(coach_acronym=COACH)
        svc.register_photo(
            notion_page_id="PAGE-001",
            temporary_s3_url="https://s3.example.com/photo1.jpg",
            mood="confident",
            format_tag="square_1080",
            usage_count=0,
        )
        result = svc.query_photo_deck(SovereignImageQuery(
            coach_id=COACH,
            target_mood="confident",
            target_format="Square_1080",
        ))
        assert result.resolution_status == SovereignImageResolution.SUCCESS
        assert result.selected_photo is not None

    def test_fr50_ac2_rotation_enforcement(self):
        """FR50 AC2: Least-used photo selected first."""
        svc = SovereignImageService(coach_acronym=COACH)
        svc.register_photo(
            notion_page_id="PAGE-001",
            temporary_s3_url="https://s3.example.com/a.jpg",
            mood="happy", format_tag="square_1080", usage_count=5,
        )
        svc.register_photo(
            notion_page_id="PAGE-002",
            temporary_s3_url="https://s3.example.com/b.jpg",
            mood="happy", format_tag="square_1080", usage_count=1,
        )

        result = svc.query_photo_deck(SovereignImageQuery(
            coach_id=COACH, target_mood="happy", target_format="Square_1080",
        ))
        assert result.selected_photo is not None
        assert result.selected_photo.notion_page_id == "PAGE-002"
        assert result.selected_photo.usage_count_updated_to == 2

    def test_fr50_ac3_sovereign_guard(self):
        """FR50 AC3: Blocks prompts with coach imagery terms."""
        svc = SovereignImageService(coach_acronym=COACH)

        assert svc.check_sovereign_violation("generate a headshot of the coach") is True
        assert svc.check_sovereign_violation("generate a stick figure holding a book") is False

        with pytest.raises(SovereignViolationException):
            svc.enforce_sovereign_guard("make a coach portrait")

    def test_fr50_ac4_clean_fallback_null(self):
        """FR50 AC4: No match returns NO_MATCH, no crash."""
        svc = SovereignImageService(coach_acronym=COACH)
        result = svc.query_photo_deck(SovereignImageQuery(
            coach_id=COACH, target_mood="angry", target_format="square_1080",
        ))
        assert result.resolution_status == SovereignImageResolution.NO_MATCH
        assert result.selected_photo is None


# ═════════════════════════════════════════════════════════
# CROSS-SPEC INTEGRATION — Composite Flows
# ═════════════════════════════════════════════════════════

class TestCrossSpecIntegration:

    def test_crisis_blocks_dormancy(self):
        """FR31 + FR30: Crisis HOLD blocks dormancy recovery."""
        crisis_svc = CrisisGuardianService(coach_acronym=COACH)
        dormancy_svc = DormancyRecoveryService(coach_acronym=COACH)

        crisis_svc.execute_crisis_protocol(
            user_id="U001",
            message_text="I want to kill myself",
            admin_channel_id="ADMIN",
        )

        override = crisis_svc.get_dormancy_state_override("U001")
        assert override == DormancyState.CRISIS_HOLD
        assert dormancy_svc.is_journaling_suppressed(override)

    def test_receipt_chain_guard_with_forensic_audit(self):
        """FR47 + FR48: Receipt chain feeds forensic lineage."""
        guard = ReceiptChainGuard(coach_acronym=COACH)
        genesis = guard.create_genesis_block("ASSET-001")
        block2 = guard.append_block(
            asset_id="ASSET-001",
            executing_agent="Artisan",
            input_payload="input",
            output_payload="output",
        )

        forensic = ForensicAuditService(coach_acronym=COACH)
        fp = forensic.generate_skill_fingerprint(
            archetype_template_id="ARCH001",
            mood=MoodState.DISCOVERY,
            regulatory_frame=RegulatoryFrame.PROMOTION,
            audience_cohort=AudienceCohort.NEW,
        )
        forensic.bind_asset_to_fingerprint(
            asset_id="ASSET-001",
            skill_fingerprint_id=fp.skill_id,
        )

        lineage = forensic.trace_lineage("ASSET-001", receipt_chain=guard.chain)
        assert lineage is not None
        assert len(lineage.receipt_chain) == 2
        assert lineage.agent_sequence == ["SYSTEM_GENESIS", "Artisan"]

    def test_yolo_with_transparent_collage(self):
        """FR33 + FR36 + FR35: YOLO pipeline → collage → unified Excalidraw."""
        yolo_svc = V2WSYoloService(coach_acronym=COACH)
        collage_svc = TransparentCollagePipelineService(coach_acronym=COACH)
        excalidraw_svc = UnifiedExcalidrawService(coach_acronym=COACH)

        # Generate YOLO modules
        intake = YoloIntake(
            actionable_lesson_thesis="Fear is a compass",
            target_audience_segment="Entrepreneurs",
            final_offer_cta="Book a call",
            key_stories_array=["Story 1"],
            tone_energy_constraint="Bold",
        )
        modules = yolo_svc.generate_module_scripts(intake)

        # Generate collages for each module
        images = []
        for m in modules:
            img = collage_svc.run_pipeline(
                emotion="focused", pose="standing", prop="microphone",
            )
            images.append(img)

        # Unified Excalidraw compilation
        payload = excalidraw_svc.compile_payload(
            strategy=ExcalidrawLayoutStrategy.HORIZONTAL_SLIDE_SEQUENCE,
            titles=[m.part.value for m in modules],
            body_texts=[m.slide_content for m in modules],
            images=images,
        )

        assert payload.type == "excalidraw"
        assert len(payload.files) == len(modules)

    def test_publer_sync_to_data_analyst(self):
        """FR42 + FR43: Publer metrics flow into Data Analyst."""
        publer = PublerSyncService(coach_acronym=COACH)
        analyst = DataAnalystService(coach_acronym=COACH)

        # Generate enough data
        for i in range(15):
            publer.schedule_content(
                universal_asset_id=f"ASSET-{i:03d}",
                publer_post_id=f"PUB-{i:03d}",
                platform="instagram",
            )
            publer.ingest_48h_metrics(
                universal_asset_id=f"ASSET-{i:03d}",
                reach=1000 + i * 100,
                saves=50, shares=30, comments=20, likes=100,
            )

        rows = [publer.get_performance(f"ASSET-{i:03d}") for i in range(15)]
        rows = [r for r in rows if r is not None]

        update = analyst.generate_parameter_update(
            rows=rows,
            arc_type_groups={
                "discovery": rows[:8],
                "challenge": rows[8:],
            },
        )

        assert update is not None
        tagged = analyst.tag_rows_as_reviewed(rows)
        assert tagged == 15

    def test_sovereign_image_in_notion_export(self):
        """FR50 + FR45: Sovereign image flows into Notion export."""
        sovereign = SovereignImageService(coach_acronym=COACH)
        notion = NotionExportService(coach_acronym=COACH)

        sovereign.register_photo(
            notion_page_id="PAGE-001",
            temporary_s3_url="https://s3.example.com/photo.jpg",
            mood="confident",
            format_tag="square_1080",
        )

        result = sovereign.query_photo_deck(SovereignImageQuery(
            coach_id=COACH, target_mood="confident", target_format="Square_1080",
        ))

        photo_url = result.selected_photo.temporary_s3_url if result.selected_photo else ""

        payload = notion.build_page_payload(
            parent_database_id="DB-001",
            title="My Post",
            universal_asset_id="ASSET-001",
            coach_photo_url=photo_url,
        )

        assert notion.validate_sovereign_image(payload)
        assert notion.validate_section_count(payload)
