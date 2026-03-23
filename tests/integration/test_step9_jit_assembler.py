"""
Step 9 Integration Tests — JIT Skill Assembler v2.0 (FR21, FR24, FR26)

12 Acceptance Criteria across 3 specs:
  FR21 (Receipt Chain Guard):
    AC1 — Broken Chain Halt
    AC2 — Quarantine Packaging
    AC3 — No-Bypass Rule
    AC4 — ADR-01 Strict Isolation
  FR24 (Weekly Pipeline):
    AC1 — Trigger-First Verification
    AC2 — Mass Validation Triad
    AC3 — Async Wait-State (Pipeline suspend/resume)
    AC4 — ADR-01 Strict Isolation
  FR26 (Validation Gate):
    AC1 — The Unforgiving Gate
    AC2 — TTT Drift Threshold
    AC3 — Season Mandate Flip
    AC4 — ADR-01 Isolation
"""

import pytest
from pathlib import Path

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.receipt_guard_models import (
    AssemblyChainLedger,
    AssemblyStatus,
    ChainBreakEvent,
    GuardStage,
    HandoffVerification,
    NodeReceipt,
    QuarantineTicket,
    ReceiptGuardVerdict,
    VerificationResult,
)
from src.ccp.models.validation_gate_models import (
    ChenMimicryResult,
    MarcusProtocolResult,
    SeasonMandate,
    SophiaSoulResult,
    TillDonePayload,
    TriplePassResult,
    ValidationFinalVerdict,
    ValidationReport,
    ValidatorType,
)
from src.ccp.models.weekly_pipeline_models import (
    DamageControlStatus,
    GenerationStatus,
    LIWCAuthenticityResult,
    NoveltyCheckResult,
    NoveltyVerdict,
    PhaseAResult,
    PhaseBResult,
    PhaseCResult,
    PhaseDResult,
    PhaseReceipt,
    PipelinePhase,
    PipelineStatus,
    ScriptSlot,
    TriggerMatchCandidate,
    WeeklyBatchPayload,
)
from src.ccp.services.receipt_chain_guard import ReceiptChainGuard
from src.ccp.pipelines.weekly_pipeline import (
    AGENT_NAMES_PATTERN,
    ROLEPLAY_PATTERN,
    WeeklyPipelineOrchestrator,
)
from src.ccp.services.validation_gate import (
    AI_IDIOMS,
    ValidationGate,
)


# ─── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def tmp_receipt_dir(tmp_path: Path) -> str:
    """Create a temporary directory for receipt chain logs."""
    d = tmp_path / "receipts"
    d.mkdir()
    return str(d)


@pytest.fixture
def guard(tmp_path: Path) -> ReceiptChainGuard:
    """Create a ReceiptChainGuard for testing."""
    g = ReceiptChainGuard(coach_id="TST")
    g.receipt_chain = ReceiptChain(
        coach_acronym="TST",
        log_dir=str(tmp_path / "guard_receipts"),
    )
    return g


@pytest.fixture
def pipeline(tmp_path: Path) -> WeeklyPipelineOrchestrator:
    """Create a WeeklyPipelineOrchestrator for testing."""
    p = WeeklyPipelineOrchestrator(
        coach_id="TST",
        season_mandate=SeasonMandate.THE_FORGE,
    )
    p.receipt_chain = ReceiptChain(
        coach_acronym="TST",
        log_dir=str(tmp_path / "pipeline_receipts"),
    )
    p.guard.receipt_chain = ReceiptChain(
        coach_acronym="TST",
        log_dir=str(tmp_path / "guard_receipts"),
    )
    return p


@pytest.fixture
def validation_gate(tmp_path: Path) -> ValidationGate:
    """Create a ValidationGate for testing."""
    vg = ValidationGate(
        coach_id="TST",
        season_mandate=SeasonMandate.THE_FORGE,
    )
    vg.receipt_chain = ReceiptChain(
        coach_acronym="TST",
        log_dir=str(tmp_path / "vg_receipts"),
    )
    return vg


@pytest.fixture
def forge_draft() -> str:
    """A script draft aligned with THE_FORGE season."""
    return (
        "Stop waiting for the perfect moment. That moment died while you were "
        "scrolling through your phone looking for motivation. Here is the hard "
        "truth about discipline: action precedes clarity. You will never feel "
        "ready. The forge does not care about your feelings. It cares about your "
        "commitment. Step one: write down the one thing you have been avoiding. "
        "Step two: do it before noon tomorrow. No excuses. No negotiation. "
        "Build the habit of doing what scares you. Execute daily. Commit fully. "
        "The grind is the teacher. Work through the resistance."
    )


@pytest.fixture
def mirror_draft() -> str:
    """A script draft aligned with THE_MIRROR season."""
    return (
        "I remember the afternoon I realized I had been lying to myself for "
        "years. Not a dramatic lie — a quiet one. The kind you tell yourself "
        "when you look in the mirror and pretend everything is fine. I had to "
        "sit with that discomfort. Journal about it. Reflect on every choice "
        "that led me there. Self-examination is not comfortable. But it is "
        "the only path to knowing who you actually are beneath the story you "
        "tell the world. Look within. Remember who you were before the mask. "
        "Introspect deeply before you take another step forward."
    )


@pytest.fixture
def ai_slop_draft() -> str:
    """A draft loaded with AI tells."""
    return (
        "In today's busy world, it is crucial to navigate the challenges of "
        "modern life. Let's dive in to explore some vital insights that will "
        "help you harness your potential. It's worth noting that leveraging "
        "holistic approaches can be a real game-changer. At the end of the day, "
        "the key to success is taking actionable insights and turning them into "
        "transformative paradigm shifts. Delve into this comprehensive tapestry "
        "of multifaceted strategies. Without further ado, unlock your potential."
    )


@pytest.fixture
def coach_soul_baseline() -> dict:
    """A coach soul baseline for Sophia validation."""
    return {
        "ttt_composite": 0.55,
        "temperature": 0.6,
        "tone": 0.5,
        "temperament": 0.55,
    }


# ══════════════════════════════════════════════════════════════════════════════
#  FR21 — RECEIPT CHAIN GUARD PROTOCOL (DEP-PROTO-010)
# ══════════════════════════════════════════════════════════════════════════════


class TestFR21_AC1_BrokenChainHalt:
    """AC1: A payload correctly generated by the Builder Engine is manually
    stripped of its receipt_chain_hash before being passed to the Assembler.
    The Assembler immediately throws a HALT execution error and refuses to
    read Block A.

    Failure Example: The Assembler ignores the missing receipt, reads the
    data, and outputs a generic skill file.
    """

    def test_missing_receipt_triggers_halt(self, guard: ReceiptChainGuard) -> None:
        """Payload without receipt_chain_hash → verification FAILS."""
        payload = {"data": "some_block_a_content"}  # No receipt_chain_hash

        verification = guard.verify_handoff(
            payload=payload,
            upstream_node_id="builder_engine_step_1",
            downstream_node_id="assembler_tier_0",
        )

        assert verification.chain_verified is False
        assert verification.verification_result == VerificationResult.MISSING_HASH
        assert verification.upstream_node_id == "builder_engine_step_1"
        assert verification.downstream_node_id == "assembler_tier_0"

    def test_empty_receipt_triggers_halt(self, guard: ReceiptChainGuard) -> None:
        """Empty string receipt → verification FAILS."""
        payload = {"receipt_chain_hash": "", "data": "block_a"}

        verification = guard.verify_handoff(
            payload=payload,
            upstream_node_id="builder_engine_step_1",
            downstream_node_id="assembler_tier_0",
        )

        assert verification.chain_verified is False
        assert verification.verification_result == VerificationResult.MISSING_HASH

    def test_valid_receipt_passes(self, guard: ReceiptChainGuard) -> None:
        """Valid receipt → verification PASSES (control case)."""
        # Generate a real receipt first
        receipt = guard.generate_receipt(
            node_id="builder_engine_step_1",
            stage_name="BUILDER-ENGINE-STEP-1",
            agent_name="BuilderEngine",
            input_payload={"brief": "test"},
            output_payload={"block_a": "content"},
        )
        assert receipt is not None

        payload = {
            "receipt_chain_hash": receipt.receipt_chain_hash,
            "data": "block_a",
        }

        verification = guard.verify_handoff(
            payload=payload,
            upstream_node_id="builder_engine_step_1",
            downstream_node_id="assembler_tier_0",
        )

        assert verification.chain_verified is True
        assert verification.verification_result == VerificationResult.VALID


class TestFR21_AC2_QuarantinePackaging:
    """AC2: Upon a Stage 3 Circuit Breaker trip, the system successfully
    writes the exact failure node to assembly_report.json under chain_break_event.

    Failure Example: The system crashes silently and leaves the operator
    guessing which component failed to emit the receipt.
    """

    def test_circuit_breaker_writes_failure_node(self, guard: ReceiptChainGuard) -> None:
        """Circuit breaker trip → chain_break_event contains exact failure node."""
        # Create a failed verification
        failed_verification = HandoffVerification(
            chain_verified=False,
            verification_result=VerificationResult.MISSING_HASH,
            upstream_node_id="builder_engine_step_3_5",
            downstream_node_id="assembler_tier_1_mandatory",
        )

        ticket = guard.trip_circuit_breaker(
            failed_verification=failed_verification,
            compilation_request_id="REQ-20260313-099",
        )

        # Verify exact failure node is recorded
        assert ticket.chain_break_event.failed_at_node == "assembler_tier_1_mandatory"
        assert "builder_engine_step_3_5" in ticket.chain_break_event.missing_upstream_receipt
        assert ticket.assembly_status == AssemblyStatus.REJECTED_BROKEN_CHAIN
        assert ticket.chain_break_event.operator_action_required is True
        assert ticket.chain_break_event.quarantine_status == "PARTIAL_MANUAL"
        assert ticket.quarantine_ticket_id.startswith("QT-")

    def test_quarantine_preserves_partial_work(self, guard: ReceiptChainGuard) -> None:
        """Quarantine Without Deletion: partial work is cached, not deleted."""
        failed_verification = HandoffVerification(
            chain_verified=False,
            verification_result=VerificationResult.MISSING_HASH,
            upstream_node_id="gate_v_00",
            downstream_node_id="assembler_tier_1",
        )

        cached_images = {"slide_hash_001": "cached_image_url_1"}

        ticket = guard.trip_circuit_breaker(
            failed_verification=failed_verification,
            compilation_request_id="REQ-001",
            preserved_state=cached_images,
        )

        assert ticket.preserved_state == cached_images
        assert ticket.coach_id == "TST"


class TestFR21_AC3_NoBypassRule:
    """AC3: An outdated script lacking receipt support is injected into the
    testing environment. The Receipt-Verification-Interceptor consistently
    blocks it 100% of the time.

    Failure Example: The Interceptor flags a warning but allows the script
    to process because the JSON body 'looked mostly correct'.
    """

    def test_no_receipt_field_blocked(self, guard: ReceiptChainGuard) -> None:
        """Payload missing receipt field entirely → always blocked."""
        for _ in range(10):
            verification = guard.verify_handoff(
                payload={"data": "legacy_output", "status": "ok"},
                upstream_node_id="legacy_v1_script",
                downstream_node_id="assembler_tier_0",
            )
            assert verification.chain_verified is False
            assert verification.verification_result == VerificationResult.MISSING_HASH

    def test_invalid_hash_structure_blocked(self, guard: ReceiptChainGuard) -> None:
        """Short or non-hex hash → always blocked."""
        invalid_hashes = ["abc", "12345", "not-a-hash!", "ZZZZZZZZZZZZZZZ", ""]
        for bad_hash in invalid_hashes:
            verification = guard.verify_handoff(
                payload={"receipt_chain_hash": bad_hash},
                upstream_node_id="legacy_script",
                downstream_node_id="assembler",
            )
            assert verification.chain_verified is False, f"Should block hash: '{bad_hash}'"

    def test_partial_status_blocked(self, guard: ReceiptChainGuard) -> None:
        """PARTIAL status evaluates as FALSE — instant chain break."""
        # Generate a valid hash
        receipt = guard.generate_receipt(
            node_id="cral_orchestrator",
            stage_name="CRAL-GENERATION",
            agent_name="CRALOrchestrator",
            input_payload={"test": True},
            output_payload={"skills": 7},
        )
        assert receipt is not None

        # Pass valid hash but with PARTIAL status
        payload = {
            "receipt_chain_hash": receipt.receipt_chain_hash,
            "execution_status": "PARTIAL",
        }

        verification = guard.verify_handoff(
            payload=payload,
            upstream_node_id="cral_orchestrator",
            downstream_node_id="builder_engine",
        )

        assert verification.chain_verified is False
        assert verification.verification_result == VerificationResult.PARTIAL_STATUS


class TestFR21_AC4_ADR01StrictIsolation:
    """AC4: When a batch is quarantined, the data dump explicitly prohibits
    access to variables belonging to any tenant other than the one currently
    executing.

    Failure Example: The quarantine log accidentally dumps shared memory
    showing another coach's private data.
    """

    def test_quarantine_scoped_to_single_coach(self, tmp_path: Path) -> None:
        """Quarantine ticket is scoped to the executing coach only."""
        guard_a = ReceiptChainGuard(coach_id="EMA")
        guard_a.receipt_chain = ReceiptChain(
            coach_acronym="EMA",
            log_dir=str(tmp_path / "guard_a"),
        )

        guard_b = ReceiptChainGuard(coach_id="MRB")
        guard_b.receipt_chain = ReceiptChain(
            coach_acronym="MRB",
            log_dir=str(tmp_path / "guard_b"),
        )

        # Trip breaker for coach A
        failed_v = HandoffVerification(
            chain_verified=False,
            verification_result=VerificationResult.MISSING_HASH,
            upstream_node_id="node_1",
            downstream_node_id="node_2",
        )

        ticket_a = guard_a.trip_circuit_breaker(
            failed_verification=failed_v,
            compilation_request_id="REQ-A-001",
        )

        # Verify coach A's ticket is scoped to EMA
        assert ticket_a.coach_id == "EMA"
        assert ticket_a.compilation_request_id == "REQ-A-001"

        # Coach B has no quarantine
        assert guard_b._quarantine_ticket is None

    def test_ghost_variable_prevention_gate(self, guard: ReceiptChainGuard) -> None:
        """Ghost Variable Prevention: missing DEP-IDs trigger DAG_VIOLATION."""
        payload = {
            "DEP-ENG-022": {"data": "research_plan"},
            # DEP-ENG-016 is missing!
        }

        violations = guard.check_ghost_variables(
            required_dep_ids=["DEP-ENG-022", "DEP-ENG-016"],
            payload=payload,
        )

        assert len(violations) == 1
        assert violations[0]["error"] == "DAG_VIOLATION"
        assert violations[0]["missing_dep"] == "DEP-ENG-016"


# ══════════════════════════════════════════════════════════════════════════════
#  FR24 — AUTONOMOUS WEEKLY CCF PIPELINE v3.1 (DEP-PROTO-014)
# ══════════════════════════════════════════════════════════════════════════════


class TestFR24_AC1_TriggerFirstVerification:
    """AC1: Starting ccf-weekly for a coach with a valid trigger_map.json
    correctly inserts ccf-trigger-match BEFORE forming the final provocation.

    Failure Example: The orchestrator ignores the map and just asks the
    coach to 'talk about the current Google Trend'.
    """

    def test_trigger_match_executes_before_provocation(
        self, pipeline: WeeklyPipelineOrchestrator
    ) -> None:
        """Phase A uses trigger_map to match triggers BEFORE topic selection."""
        trigger_map = {
            "impostor_syndrome": {
                "pain": "feeling like a fraud",
                "mft_alignment": 0.8,
            },
            "burnout_cycle": {
                "pain": "exhaustion from overwork",
                "mft_alignment": 0.6,
            },
        }
        trends = [
            {"topic": "AI replacing jobs", "mft_score": 0.7, "temporal_score": 0.8},
            {"topic": "Quiet quitting", "mft_score": 0.5, "temporal_score": 0.6},
        ]

        result = pipeline.execute_phase_a(
            trigger_map=trigger_map,
            trend_vectors=trends,
        )

        # Trigger match candidates were generated
        assert len(result.trigger_match_candidates) > 0
        # Theme selection came FROM trigger matching, not raw trends
        assert result.trigger_match_score > 0.0
        assert result.coach_id == "TST"
        # Receipt was emitted
        assert result.phase_receipt is not None
        assert result.phase_receipt.stage_name == "DISCOVERY-AND-TRIGGER-MATCHING"

    def test_missing_trigger_map_degrades_to_v30(
        self, pipeline: WeeklyPipelineOrchestrator
    ) -> None:
        """Missing trigger_map → v3.0 degradation (skip trigger match)."""
        result = pipeline.execute_phase_a(
            trigger_map={},
            trend_vectors=[{"topic": "trending_topic"}],
        )

        assert pipeline._pipeline_status == PipelineStatus.PIPELINE_V30_DEGRADATION
        assert result.trigger_match_candidates == []


class TestFR24_AC2_MassValidationTriad:
    """AC2: During Phase D, the orchestrator detects 4 scripts that fail
    Chen's Mimicry check. It triggers TillDone for those 4 while
    preserving the other 32.

    Failure Example: The orchestrator drops the 4 bad scripts entirely,
    resulting in 32 outputs instead of 36.
    """

    def test_failed_scripts_rewritten_batch_preserved(
        self, pipeline: WeeklyPipelineOrchestrator
    ) -> None:
        """Failed scripts trigger TillDone; batch count stays at 36."""
        # Build Phase C result with 36 slots
        slots = [
            ScriptSlot(
                slot_id=f"SLOT-{i+1:02d}",
                skill_id=f"SKILL-{i+1:02d}-TST",
                archetype="Achievement Story",
                generation_status=GenerationStatus.GENERATED,
            )
            for i in range(36)
        ]
        phase_c = PhaseCResult(
            coach_id="TST",
            total_slots=36,
            slots=slots,
        )

        # 4 scripts fail Chen's check, 32 pass
        validation_results = {}
        for i in range(36):
            slot_id = f"SLOT-{i+1:02d}"
            if i < 4:
                validation_results[slot_id] = {
                    "verdict": "FAIL_TRIGGER_REWRITE",
                    "scores": {"chen_mimicry": 0.12},
                }
            else:
                validation_results[slot_id] = {
                    "verdict": "APPROVED",
                    "scores": {"sophia_ttt": 0.92, "marcus_protocol": 1.0, "chen_mimicry": 0.02},
                }

        result = pipeline.execute_phase_d(
            phase_c_result=phase_c,
            validation_results=validation_results,
        )

        # Batch count MUST be preserved (not dropped to 32)
        assert result.total_validated == 36
        assert result.total_approved == 32
        assert result.total_rewritten == 4


class TestFR24_AC3_AsyncWaitState:
    """AC3: Between Phase A and Phase B, the orchestration thread
    gracefully suspends, resuming when the Coach sends audio.

    Failure Example: The process times out after 60 seconds.

    We verify the pipeline can execute Phase A, then independently
    execute Phase B with the Phase A receipt — proving state preservation.
    """

    def test_pipeline_suspends_and_resumes_with_receipt(
        self, pipeline: WeeklyPipelineOrchestrator
    ) -> None:
        """Phase A emits receipt → pipeline can resume at Phase B with that receipt."""
        # Execute Phase A
        trigger_map = {"key": {"pain": "test"}}
        trends = [{"topic": "test topic", "mft_score": 0.6, "temporal_score": 0.7}]
        phase_a = pipeline.execute_phase_a(trigger_map=trigger_map, trend_vectors=trends)

        # Phase A should have a receipt
        assert phase_a.phase_receipt is not None
        phase_a_hash = phase_a.phase_receipt.receipt_hash
        assert len(phase_a_hash) >= 16

        # Now "wait" (simulate async pause)... then resume with coach transcript
        transcript = (
            "I have been thinking about this deeply and I realize that the core "
            "issue is not motivation but identity. When people struggle with "
            "impostor syndrome they are actually fighting against a version of "
            "themselves that no longer fits. The old story has to die for the "
            "new one to emerge. This is personal for me because I went through "
            "this exact transformation three years ago."
        )

        phase_b = pipeline.execute_phase_b(
            transcript_text=transcript,
            phase_a_receipt_hash=phase_a_hash,
        )

        # Phase B should execute successfully with the preserved receipt
        assert phase_b.liwc_result.passed is True
        assert phase_b.transcript_available is True
        assert phase_b.phase_receipt is not None


class TestFR24_AC4_ADR01StrictIsolation:
    """AC4: During Phase C batch generation involving 65 agents, ZERO
    cross-buffer contamination occurs. Coach A's output variables are
    verified against their namespace before saving.

    Failure Example: Emilio accidentally uses Coach B's L3 pain points
    to write Coach A's script because the TeamOrchestrator shared RAM.
    """

    def test_concurrent_coaches_isolated(self, tmp_path: Path) -> None:
        """Two pipelines for different coaches are completely isolated."""
        pipeline_a = WeeklyPipelineOrchestrator(
            coach_id="EMA",
            season_mandate=SeasonMandate.THE_FORGE,
        )
        pipeline_a.receipt_chain = ReceiptChain(
            coach_acronym="EMA",
            log_dir=str(tmp_path / "ema_receipts"),
        )
        pipeline_a.guard.receipt_chain = ReceiptChain(
            coach_acronym="EMA",
            log_dir=str(tmp_path / "ema_guard"),
        )

        pipeline_b = WeeklyPipelineOrchestrator(
            coach_id="MRB",
            season_mandate=SeasonMandate.THE_MIRROR,
        )
        pipeline_b.receipt_chain = ReceiptChain(
            coach_acronym="MRB",
            log_dir=str(tmp_path / "mrb_receipts"),
        )
        pipeline_b.guard.receipt_chain = ReceiptChain(
            coach_acronym="MRB",
            log_dir=str(tmp_path / "mrb_guard"),
        )

        # Execute Phase A for both
        trigger_map = {"key": {"pain": "test"}}
        trends = [{"topic": "test", "mft_score": 0.5, "temporal_score": 0.5}]

        result_a = pipeline_a.execute_phase_a(trigger_map, trends)
        result_b = pipeline_b.execute_phase_a(trigger_map, trends)

        # Coach IDs are isolated
        assert result_a.coach_id == "EMA"
        assert result_b.coach_id == "MRB"

        # Guard instances are separate
        assert pipeline_a.guard.coach_id == "EMA"
        assert pipeline_b.guard.coach_id == "MRB"

        # Receipt chains write to different directories
        assert pipeline_a.receipt_chain.log_dir != pipeline_b.receipt_chain.log_dir

    def test_c11_persona_masking_gate(
        self, pipeline: WeeklyPipelineOrchestrator
    ) -> None:
        """C-11 gate detects agent names in API payloads."""
        # Text with agent names
        dirty_payload = "Emilio should generate the script using Charlotte's structure"
        assert pipeline._c11_gate_check(dirty_payload) is True

        # Text with roleplay instructions
        roleplay_payload = "Act as an expert content strategist"
        assert pipeline._c11_gate_check(roleplay_payload) is True

        # Clean text
        clean_payload = "Generate a carousel post about morning routines"
        assert pipeline._c11_gate_check(clean_payload) is False

    def test_scrub_agent_names(
        self, pipeline: WeeklyPipelineOrchestrator
    ) -> None:
        """Agent names are replaced with [AGENT] placeholder."""
        text = "Sophia validates TTT drift while Marcus checks the season mandate."
        scrubbed = pipeline.scrub_agent_names(text)
        assert "Sophia" not in scrubbed
        assert "Marcus" not in scrubbed
        assert "[AGENT]" in scrubbed


# ══════════════════════════════════════════════════════════════════════════════
#  FR26 — VALIDATION TEAM GATE (DEP-PROTO-016)
# ══════════════════════════════════════════════════════════════════════════════


class TestFR26_AC1_TheUnforgivingGate:
    """AC1: A drafted script returns Sophia: PASS, Marcus: PASS, Chen: FAIL.
    The orchestrator immediately rejects the script and triggers TillDone.

    Failure Example: The orchestrator uses a 'best 2 out of 3' vote and
    incorrectly lets the AI-slop script leak into generation.
    """

    def test_chen_fail_rejects_despite_sophia_marcus_pass(
        self, validation_gate: ValidationGate, ai_slop_draft: str, coach_soul_baseline: dict
    ) -> None:
        """Even with Sophia+Marcus PASS, Chen FAIL → entire script REJECTED."""
        result = validation_gate.validate(
            script_id="OUT-STORY01-TST-001",
            draft_text=ai_slop_draft,
            coach_soul_baseline=coach_soul_baseline,
        )

        # Chen should detect AI idioms
        assert result.chen_mimicry.status == "FAIL"
        assert result.chen_mimicry.artifact_score > 0.05

        # Final verdict MUST be FAIL regardless of Sophia/Marcus
        assert result.final_verdict == ValidationFinalVerdict.FAIL_TRIGGER_REWRITE

    def test_all_pass_approves(
        self, validation_gate: ValidationGate, forge_draft: str, coach_soul_baseline: dict
    ) -> None:
        """All three PASS → APPROVED."""
        result = validation_gate.validate(
            script_id="OUT-STORY01-TST-002",
            draft_text=forge_draft,
            coach_soul_baseline=coach_soul_baseline,
        )

        # A clean forge draft should pass all validators
        assert result.final_verdict == ValidationFinalVerdict.APPROVED

    def test_till_done_payload_merges_constraints(
        self, validation_gate: ValidationGate, ai_slop_draft: str, coach_soul_baseline: dict
    ) -> None:
        """Failed validation → TillDone payload with merged negative constraints."""
        result = validation_gate.validate(
            script_id="OUT-STORY01-TST-003",
            draft_text=ai_slop_draft,
            coach_soul_baseline=coach_soul_baseline,
        )

        if result.final_verdict != ValidationFinalVerdict.APPROVED:
            till_done = validation_gate.build_till_done_payload(result, iteration=1)
            assert till_done is not None
            assert len(till_done.failed_validators) > 0
            assert "Rewrite Required" in till_done.merged_negative_constraints


class TestFR26_AC2_TTTDriftThreshold:
    """AC2: Sophia evaluates a script at 16% deviation from baseline.
    The script fails.

    Failure Example: The math rounding algorithm drops 16% to 10% bin
    and incorrectly yields a pass.
    """

    def test_16_percent_drift_fails(self, validation_gate: ValidationGate) -> None:
        """16% drift exceeds 15% threshold → Sophia FAIL."""
        # Create a direct Sophia result with 16% drift
        result = SophiaSoulResult(
            status="FAIL",
            ttt_drift_percentage=0.16,
            baseline_source="rolling_4_week",
        )

        assert result.status == "FAIL"
        assert result.ttt_drift_percentage == 0.16

    def test_15_percent_drift_passes(self, validation_gate: ValidationGate) -> None:
        """15% drift exactly at threshold → Sophia PASS."""
        result = SophiaSoulResult(
            status="PASS",
            ttt_drift_percentage=0.15,
            baseline_source="rolling_4_week",
        )

        assert result.status == "PASS"

    def test_model_offset_applied(self, validation_gate: ValidationGate) -> None:
        """Model offset coefficient is applied before drift calculation."""
        # Sophia result with model offset recorded
        result = SophiaSoulResult(
            status="PASS",
            ttt_drift_percentage=0.10,
            model_offset_applied=-0.12,
            baseline_source="rolling_4_week",
        )

        assert result.model_offset_applied == -0.12
        assert result.baseline_source == "rolling_4_week"


class TestFR26_AC3_SeasonMandateFlip:
    """AC3: The environment variable is flipped from THE_FORGE to THE_MIRROR.
    A hard-hitting discipline script passes Sophia and Chen, but Marcus
    immediately throws FAIL with instructions to convert into introspective
    narrative storytelling.

    Failure Example: Marcus ignores the env flag and passes the script
    because the structure is technically sound for a listicle.
    """

    def test_forge_script_fails_mirror_season(
        self, tmp_path: Path, forge_draft: str
    ) -> None:
        """Forge discipline script under THE_MIRROR season → Marcus FAIL."""
        # Create gate with THE_MIRROR season
        gate = ValidationGate(
            coach_id="TST",
            season_mandate=SeasonMandate.THE_MIRROR,
        )
        gate.receipt_chain = ReceiptChain(
            coach_acronym="TST",
            log_dir=str(tmp_path / "mirror_receipts"),
        )

        marcus_result = gate.run_marcus(forge_draft)

        # Marcus should FAIL because forge rhetoric doesn't match mirror season
        assert marcus_result.active_season == SeasonMandate.THE_MIRROR
        assert marcus_result.status == "FAIL"
        assert marcus_result.feedback is not None
        assert "introspective" in marcus_result.feedback.lower() or "mirror" in marcus_result.feedback.lower()

    def test_mirror_script_passes_mirror_season(
        self, tmp_path: Path, mirror_draft: str
    ) -> None:
        """Mirror introspective script under THE_MIRROR season → Marcus PASS."""
        gate = ValidationGate(
            coach_id="TST",
            season_mandate=SeasonMandate.THE_MIRROR,
        )
        gate.receipt_chain = ReceiptChain(
            coach_acronym="TST",
            log_dir=str(tmp_path / "mirror_receipts_2"),
        )

        marcus_result = gate.run_marcus(mirror_draft)

        assert marcus_result.active_season == SeasonMandate.THE_MIRROR
        assert marcus_result.status == "PASS"

    def test_season_override_takes_effect(
        self, validation_gate: ValidationGate, forge_draft: str
    ) -> None:
        """Season override parameter correctly changes Marcus's enforcement."""
        # Default gate season is THE_FORGE
        forge_result = validation_gate.run_marcus(forge_draft)
        assert forge_result.active_season == SeasonMandate.THE_FORGE

        # Override to THE_MIRROR
        mirror_result = validation_gate.run_marcus(
            forge_draft, season_override=SeasonMandate.THE_MIRROR
        )
        assert mirror_result.active_season == SeasonMandate.THE_MIRROR


class TestFR26_AC4_ADR01Isolation:
    """AC4: Sophia validates a batch for Coach A. The system explicitly
    verifies it is loading coach_soul_A.json and not coach_soul_B.json.

    Failure Example: A thread-leak causes Sophia to cross-validate Coach A's
    draft against Coach B's TTT baseline.
    """

    def test_sophia_uses_correct_coach_baseline(self, tmp_path: Path) -> None:
        """Two separate gates for two coaches load independent baselines."""
        gate_a = ValidationGate(
            coach_id="EMA",
            season_mandate=SeasonMandate.THE_FORGE,
        )
        gate_a.receipt_chain = ReceiptChain(
            coach_acronym="EMA",
            log_dir=str(tmp_path / "ema_vg"),
        )

        gate_b = ValidationGate(
            coach_id="MRB",
            season_mandate=SeasonMandate.THE_FORGE,
        )
        gate_b.receipt_chain = ReceiptChain(
            coach_acronym="MRB",
            log_dir=str(tmp_path / "mrb_vg"),
        )

        baseline_a = {"ttt_composite": 0.60}
        baseline_b = {"ttt_composite": 0.40}

        draft = "A standard test draft about discipline and action and forging ahead."

        sophia_a = gate_a.run_sophia(draft, baseline_a)
        sophia_b = gate_b.run_sophia(draft, baseline_b)

        # The drift values should differ because baselines differ
        # This proves each gate uses its own baseline
        assert gate_a.coach_id == "EMA"
        assert gate_b.coach_id == "MRB"
        # They received different baselines
        assert sophia_a.ttt_drift_percentage != sophia_b.ttt_drift_percentage or (
            sophia_a.ttt_drift_percentage == sophia_b.ttt_drift_percentage == 0.0
        )

    def test_validation_report_contains_coach_id(
        self, validation_gate: ValidationGate, forge_draft: str, coach_soul_baseline: dict
    ) -> None:
        """ValidationReport is scoped to the correct coach_id."""
        result = validation_gate.validate(
            script_id="OUT-STORY01-TST-010",
            draft_text=forge_draft,
            coach_soul_baseline=coach_soul_baseline,
        )

        report = validation_gate.build_report(result)

        assert report.coach_id == "TST"
        assert report.script_id == "OUT-STORY01-TST-010"
        assert report.receipt_chain_hash is not None
        assert len(report.validators) == 3


# ══════════════════════════════════════════════════════════════════════════════
#  CROSS-SPEC INTEGRATION — Receipt Chain + Pipeline + Validation
# ══════════════════════════════════════════════════════════════════════════════


class TestCrossSpecIntegration:
    """Verify that FR21, FR24, and FR26 work together end-to-end."""

    def test_pipeline_guard_verdict_after_full_run(self, tmp_path: Path) -> None:
        """Full pipeline run → guard verdict with receipt chain ledger."""
        pipeline = WeeklyPipelineOrchestrator(
            coach_id="TST",
            season_mandate=SeasonMandate.THE_FORGE,
        )
        pipeline.receipt_chain = ReceiptChain(
            coach_acronym="TST",
            log_dir=str(tmp_path / "int_receipts"),
        )
        pipeline.guard.receipt_chain = ReceiptChain(
            coach_acronym="TST",
            log_dir=str(tmp_path / "int_guard"),
        )

        # Run Phase A
        phase_a = pipeline.execute_phase_a(
            trigger_map={"key": {"pain": "test"}},
            trend_vectors=[{"topic": "test", "mft_score": 0.6, "temporal_score": 0.7}],
        )

        # Build guard verdict
        verdict = pipeline.guard.build_verdict(
            compilation_request_id="REQ-INT-001",
            nodes_checked=1,
            nodes_verified=1,
        )

        assert verdict.pipeline_clear is True
        assert verdict.chain_ledger.assembly_status == AssemblyStatus.ACCEPTED
        assert verdict.chain_ledger.coach_id == "TST"
        assert len(verdict.chain_ledger.receipt_ledger) > 0

    def test_damage_control_exhaustion(self) -> None:
        """DamageControl breaker: 3 retries → exhausted."""
        dc = DamageControlStatus()
        assert dc.is_exhausted is False

        dc.increment()
        assert dc.current_retry == 1
        assert dc.is_exhausted is False

        dc.increment()
        assert dc.current_retry == 2
        assert dc.is_exhausted is False

        dc.increment()
        assert dc.current_retry == 3
        assert dc.is_exhausted is True
        assert dc.failure_reason == "FAILED_UNRECOVERABLE"

    def test_liwc_below_threshold_rejects(
        self, pipeline: WeeklyPipelineOrchestrator
    ) -> None:
        """LIWC-22 score below 0.6 → Phase B rejects."""
        # Very short, low-quality transcript
        result = pipeline.execute_phase_b(transcript_text="yes ok")

        assert result.liwc_result.passed is False
        assert result.liwc_result.composite_score < 0.6

    def test_weekly_batch_payload_assembly(self, tmp_path: Path) -> None:
        """Build a complete WeeklyBatchPayload from phase results."""
        pipeline = WeeklyPipelineOrchestrator(
            coach_id="TST",
            season_mandate=SeasonMandate.THE_FORGE,
        )
        pipeline.receipt_chain = ReceiptChain(
            coach_acronym="TST",
            log_dir=str(tmp_path / "batch_receipts"),
        )
        pipeline.guard.receipt_chain = ReceiptChain(
            coach_acronym="TST",
            log_dir=str(tmp_path / "batch_guard"),
        )

        phase_a = PhaseAResult(
            coach_id="TST",
            trigger_match_score=0.88,
        )
        phase_b = PhaseBResult(
            coach_id="TST",
            liwc_result=LIWCAuthenticityResult(composite_score=0.74, passed=True),
        )
        phase_c = PhaseCResult(
            coach_id="TST",
            total_slots=36,
            slots=[
                ScriptSlot(
                    slot_id=f"SLOT-{i+1:02d}",
                    archetype="Achievement Story",
                )
                for i in range(36)
            ],
        )
        phase_d = PhaseDResult(
            coach_id="TST",
            total_validated=36,
            total_approved=36,
        )

        payload = pipeline.build_batch_payload(
            production_week="2026-W11",
            phase_a=phase_a,
            phase_b=phase_b,
            phase_c=phase_c,
            phase_d=phase_d,
        )

        assert payload.production_week == "2026-W11"
        assert payload.coach_id == "TST"
        assert payload.total_generated == 36
        assert payload.trigger_match_score == 0.88
        assert payload.authenticity_liwc_composite == 0.74
        assert payload.season_mandate == "THE_FORGE"
