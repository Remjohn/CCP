"""
tests/services/test_phase0_delivery_orchestrator.py
====================================================
Comprehensive verification tests for the Phase-0 Delivery Orchestrator (FR-ERA3-36).
Covers all 12 Acceptance Criteria (AC1 to AC12) and quality gates.
"""

from __future__ import annotations
import pytest
from datetime import datetime, timezone, timedelta

from src.ccp.models.phase0_intake_models import (
    Phase0ProspectPacket,
    Phase0AuditTargetDescriptor as IntakeTargetDescriptor,
    Phase0CaptionAttachment,
    Phase0AuditTargetContentType,
    Phase0ProspectStatus
)
from src.ccp.models.phase0_delivery_models import (
    Phase0DeliveryRunStatus,
    Phase0SequenceStepType,
    Phase0ExecutionMode
)
from src.ccp.models.phase0_audit_models import (
    AuditIntelligenceReport,
    ContinuityBridgeRecommendation,
    BridgeTierRecommendation
)
from src.ccp.services.phase0_delivery_orchestrator import Phase0DeliveryOrchestrator
from src.ccp.services.audit_intelligence_engine import AuditIntelligenceEngine


@pytest.fixture
def test_packet():
    """Returns a valid prospect packet ready for handoff."""
    target = IntakeTargetDescriptor(
        audit_target_id="TGT-TEST-100",
        prospect_id="PRSP-TEST-999",
        content_type=Phase0AuditTargetContentType.REEL_CAPTION,
        primary_media_source_ids=[],
        caption_id="CAPT-TEST-100"
    )
    
    caption = Phase0CaptionAttachment(
        caption_id="CAPT-TEST-100",
        prospect_id="PRSP-TEST-999",
        audit_target_id="TGT-TEST-100",
        caption_text="Let delve into this authentic revolutionizing testament of authority scaling.",
        source_kind="manual_entry"
    )

    return Phase0ProspectPacket(
        prospect_id="PRSP-TEST-999",
        display_name="Audrey Sonic Beat",
        coach_id="JP1",
        status=Phase0ProspectStatus.READY_FOR_PHASE0,
        audit_targets=[target],
        captions=[caption]
    )


def test_ac1_ac2_delivery_plan_compilation(test_packet):
    """
    AC1: Produce Phase0DeliveryPlan from a valid packet.
    AC2: Differentiate internal generation order from public release order.
    """
    orchestrator = Phase0DeliveryOrchestrator()
    plan = orchestrator.create_plan(test_packet)

    assert plan.plan_id.startswith("PLN-")
    assert plan.coach_id == "JP1"
    assert plan.phase0_packet_id == test_packet.packet_id
    assert len(plan.generation_order) > 0
    assert len(plan.release_order) > 0

    # Verify that generation order has Audit first, then PDF and Video
    gen_keys = [step.step_key for step in plan.generation_order]
    assert gen_keys[0] == "audit_core"
    assert "pdf_assembly" in gen_keys
    assert "preview_assembly" in gen_keys

    # Verify release order differs (videos are released before PDF / animated audit, then payment)
    rel_keys = [step.step_key for step in plan.release_order]
    assert rel_keys[0] == "explainer_video_1"
    assert rel_keys[-1] == "payment_handoff"
    assert rel_keys != gen_keys  # Dual sequencing verified

    # 24h SLA deadline check
    time_diff = plan.sla_deadline_utc - plan.created_at_utc
    assert abs(time_diff.total_seconds() - 24 * 3600) < 10


def test_ac3_ac4_ac5_ac6_ac10_happy_path_run(test_packet):
    """
    AC3: Orchestrate PDF, board, animated audit, and proof videos.
    AC4: Operator review gate.
    AC5: Canonical Phase0OutputBundle.
    AC6: Receipt logging.
    AC10: Payment handoff packet.
    """
    orchestrator = Phase0DeliveryOrchestrator()
    plan = orchestrator.create_plan(test_packet)
    run = orchestrator.start_run(plan)

    assert run.status == Phase0DeliveryRunStatus.RUNNING

    # Step through generation sequence
    executed_steps = []
    while True:
        step = orchestrator.execute_next_step(run, test_packet)
        if not step:
            break
        executed_steps.append(step)

        # Simulating operator review approval for review gated assets
        if step.review_gate:
            orchestrator.resolve_review_gate(run.delivery_run_id, step.step_id, approved=True)

    # 1. Output Bundle completeness checks (AC5)
    bundle = orchestrator.bundles[run.output_bundle_id]
    assert bundle.delivery_ready is True
    assert bundle.audit_report_id is not None
    assert bundle.pdf_audit_payload_id is not None
    assert bundle.explainer_video_1_asset_id is not None
    assert bundle.cinematic_video_asset_id is not None
    assert bundle.preview_bundle_ids is not None

    # 2. Receipt log existence checks (AC6)
    assert len(run.receipts) > 0
    for receipt in run.receipts:
        assert receipt.delivery_run_id == run.delivery_run_id
        assert receipt.coach_id == "JP1"
        assert receipt.outcome in ["SUCCEEDED", "DEGRADED"]

    # 3. Continuity bridge / payment handoff packet check (AC10)
    engine = AuditIntelligenceEngine(coach_acronym="JP1")
    report = engine.generate_audit(packet=test_packet, target_id="TGT-TEST-100")
    handoff = orchestrator.get_payment_handoff_packet(run.delivery_run_id, report)

    assert handoff.coach_id == "JP1"
    assert handoff.payment_ready is True
    assert handoff.release_ready is True
    assert handoff.commercial_offer_key in ["phase0_proof_unlock_29", "speaking_learning_continuity_39", "coach_os_continuity_99"]


def test_ac8_audit_failure_fail_closed(test_packet):
    """AC8: Fail-closed hard block if core audit fails."""
    orchestrator = Phase0DeliveryOrchestrator()
    plan = orchestrator.create_plan(test_packet)
    run = orchestrator.start_run(plan)

    # Force step "audit_core" to fail
    orchestrator.execute_next_step(run, test_packet, optional_failures_map={"audit_core": True})

    # The run must fail immediately
    assert run.status == Phase0DeliveryRunStatus.FAILED
    assert run.failure_state == "audit_core_failed"

    # Verify bundle is locked and not deliverable
    bundle = orchestrator.bundles[run.output_bundle_id]
    orchestrator.finalize_run(run)
    assert bundle.delivery_ready is False
    assert "missing_core_audit_report" in bundle.release_blockers


def test_ac9_preview_assembly_failure_blocks_release(test_packet):
    """AC9: Preview assembly failure blocks public release."""
    orchestrator = Phase0DeliveryOrchestrator()
    plan = orchestrator.create_plan(test_packet)
    run = orchestrator.start_run(plan)

    # Execute all steps, but fail preview assembly
    while True:
        step = orchestrator.execute_next_step(
            run,
            test_packet,
            optional_failures_map={"preview_assembly": True}
        )
        if not step:
            break
        if step.review_gate:
            orchestrator.resolve_review_gate(run.delivery_run_id, step.step_id, approved=True)

    # Finalize run
    bundle = orchestrator.bundles[run.output_bundle_id]
    orchestrator.finalize_run(run)

    assert run.status == Phase0DeliveryRunStatus.FAILED
    assert bundle.delivery_ready is False
    assert "missing_preview_bundle" in bundle.release_blockers


def test_ac7_optional_asset_honest_degradation(test_packet):
    """AC7: Optional asset failures complete run in degraded status."""
    orchestrator = Phase0DeliveryOrchestrator()
    plan = orchestrator.create_plan(test_packet)
    
    # Enable carousels and memes as optional outputs
    plan.optional_outputs_enabled = ["carousel_spread", "meme_layer"]
    for s in plan.generation_order:
        if s.step_key in ["carousel_spread", "meme_layer"]:
            s.required = True

    run = orchestrator.start_run(plan)

    # Execute steps, but fail the optional "carousel_spread"
    while True:
        step = orchestrator.execute_next_step(
            run,
            test_packet,
            optional_failures_map={"carousel_spread": True}
        )
        if not step:
            break
        if step.review_gate:
            orchestrator.resolve_review_gate(run.delivery_run_id, step.step_id, approved=True)

    # Run completes, but is explicitly marked DEGRADED_READY
    bundle = orchestrator.bundles[run.output_bundle_id]
    orchestrator.finalize_run(run)

    assert run.status == Phase0DeliveryRunStatus.DEGRADED_READY
    assert bundle.delivery_ready is True
    # The failed optional asset is missing, but core assets are fully valid
    assert bundle.audit_report_id is not None
    assert bundle.pdf_audit_payload_id is not None
    assert len(bundle.carousel_asset_ids) == 0  # failed optional is omitted honestly


def test_ac11_ac12_multi_tenant_safety_and_namespacing(test_packet):
    """
    AC11: Support shared pre-container model.
    AC12: Namespacing isolated by coach_id, phase0_packet_id, delivery_run_id.
    """
    orchestrator = Phase0DeliveryOrchestrator()

    # Create packet for Coach Audrey
    packet_audrey = Phase0ProspectPacket(
        prospect_id="PRSP-AUDREY-1",
        display_name="Audrey Beat",
        coach_id="AUDREY",
        status=Phase0ProspectStatus.READY_FOR_PHASE0,
        audit_targets=[test_packet.audit_targets[0]],
        captions=[test_packet.captions[0]]
    )

    # Create packet for Coach Sonic
    packet_sonic = Phase0ProspectPacket(
        prospect_id="PRSP-SONIC-2",
        display_name="Sonic Phase",
        coach_id="SONIC",
        status=Phase0ProspectStatus.READY_FOR_PHASE0,
        audit_targets=[test_packet.audit_targets[0]],
        captions=[test_packet.captions[0]]
    )

    # Spawn concurrent plans and runs
    plan_audrey = orchestrator.create_plan(packet_audrey)
    plan_sonic = orchestrator.create_plan(packet_sonic)

    run_audrey = orchestrator.start_run(plan_audrey)
    run_sonic = orchestrator.start_run(plan_sonic)

    # Execute their first steps
    orchestrator.execute_next_step(run_audrey, packet_audrey)
    orchestrator.execute_next_step(run_sonic, packet_sonic)

    # Assert namespacing completely isolates jobs (no crossover)
    assert run_audrey.coach_id == "AUDREY"
    assert run_sonic.coach_id == "SONIC"

    bundle_audrey = orchestrator.bundles[run_audrey.output_bundle_id]
    bundle_sonic = orchestrator.bundles[run_sonic.output_bundle_id]

    assert bundle_audrey.coach_id == "AUDREY"
    assert bundle_sonic.coach_id == "SONIC"

    # Verify that the generated audit records reflect distinct prospects
    assert bundle_audrey.audit_report_id != bundle_sonic.audit_report_id
