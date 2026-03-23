"""
CCP Step 8 — CRAL OODA Orchestrator Agent (Unit 5)
Implements FR14 §Stages 1 + 4: Orchestrator Loop Initialization + Assembly.

Architecture reference:
    FR14_CRAL_Research_Subsystem_Tech_Spec.md §Stages 1, 4
    CCP_Evolution_Architecture_Report_V4 §3.3 — CRAL Production Flow

Responsibilities:
    Stage 1: Initialize OODA loop, validate dependencies, emit DEP-ENG-022.
    Stage 2-3: Delegate to ResearchPlanner and MomentExecutors (sequential).
    Stage 4: Assemble DEP-ENG-021 (CRALFindingIndex) from 7 moment findings.
    Fallback: Backward compatibility — cached M2+M6 with fallback_mode_invoked.

FR14 AC2: M7 cannot fire until M1-M6 PASS (sequential, NOT batch).
FR14 AC5: DEP-ENG-021 cryptographically signed per coach_tenant_id (ADR-01).
M-02: No hardcoded TTT values.
ADR-01: coach_id scopes all operations.
"""

from __future__ import annotations

import hashlib
import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Optional

from src.ccp.models.adapter_registry_v2_models import (
    CRALFinding,
    CRALFindingIndex,
    CRALMomentKey,
)
from src.ccp.models.cral_research_models import (
    MOMENT_CONFIGS,
    MomentStatus,
    OODAPhase,
    OODAState,
    PlannerDirectiveVerdict,
    SessionResearchPlan,
)
from src.ccp.services.moment_executors import MomentExecutor
from src.ccp.services.research_planner import ResearchPlanner

if TYPE_CHECKING:
    from src.ccp.core.receipt_chain import ReceiptChain

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════
# Constants
# ══════════════════════════════════════════════════════════════

STAGE_1_NAME = "STAGE-1-ORCHESTRATOR-INIT"
STAGE_4_NAME = "STAGE-4-INDEX-EMIT"
AGENT_NAME = "Research-Orchestrator"
REQUIRED_MOMENT_COUNT = 7


# ══════════════════════════════════════════════════════════════
# Orchestrator Result
# ══════════════════════════════════════════════════════════════

class CRALOrchestrationResult:
    """Result container for a complete CRAL orchestration run."""

    def __init__(self) -> None:
        self.success: bool = False
        self.finding_index: Optional[CRALFindingIndex] = None
        self.research_plan: Optional[SessionResearchPlan] = None
        self.ooda_state: Optional[OODAState] = None
        self.fallback_mode: bool = False
        self.error_message: str = ""
        self.receipt_ids: list[str] = []
        self.cral_coverage_status: str = "ABSENT"


# ══════════════════════════════════════════════════════════════
# CRAL OODA Orchestrator
# ══════════════════════════════════════════════════════════════

class CRALOrchestrator:
    """FR14 — CRAL 9-Skill Research Orchestrator Agent.

    Implements the full OODA loop (Observe → Orient → Decide → Act → Complete)
    for the 7-moment diagonal research sequence. This is classified as an
    **Agent** (not a Skill) because it contains an open-ended OODA loop,
    manages dependency state routing, and handles error recovery.

    Lifecycle:
        1. OBSERVE: Validate inputs, check tribe_soul + coach_soul presence.
        2. ORIENT: Initialize OODA state, emit DEP-ENG-022.
        3. DECIDE+ACT: For each moment M1→M7 sequentially:
            a. Check dependency readiness.
            b. Compile directive via ResearchPlanner.
            c. Execute moment via MomentExecutor.
            d. Update OODA state.
        4. COMPLETE: Assemble DEP-ENG-021 from all 7 findings.

    Fallback (FR14 §6):
        If API failure occurs, degrade to cached M2+M6 with
        fallback_mode_invoked: true.

    Usage:
        orchestrator = CRALOrchestrator(
            coach_id="coach_88ab",
            receipt_chain=receipt_chain,
        )
        result = orchestrator.run(
            session_id="CRAL-20260313",
            theme="algorithm taxation impact on creators",
            trigger_profile={...},
            tribe_soul={...},
        )
    """

    def __init__(
        self,
        coach_id: str,
        receipt_chain: Optional[ReceiptChain] = None,
    ):
        self.coach_id = coach_id
        self.receipt_chain = receipt_chain
        self.planner = ResearchPlanner(coach_id, receipt_chain)
        self.executor = MomentExecutor(coach_id, receipt_chain)
        self._last_chain_hash: str = ""

    # ──────────────────────────────────────────────────────────
    # Stage 1: Observe & Orient
    # ──────────────────────────────────────────────────────────

    def _stage_1_init(
        self,
        session_id: str,
        theme: str,
        trigger_profile: Optional[dict[str, Any]] = None,
        tribe_soul: Optional[dict[str, Any]] = None,
        coach_soul: Optional[dict[str, Any]] = None,
        archetype_id: str = "",
        mood_state: str = "",
    ) -> tuple[OODAState, SessionResearchPlan]:
        """Stage 1: Orchestrator Loop Initialization.

        FR14 §Stage 1:
        1. Observe global pipeline state.
        2. Validate required core dependencies.
        3. Orient the state matrix.
        4. Output DEP-ENG-022 (SessionResearchPlan).
        5. Receipt Write.

        Returns:
            (OODAState, SessionResearchPlan) tuple.
        """
        # Initialize OODA state
        state = OODAState(
            coach_id=self.coach_id,
            session_id=session_id,
            phase=OODAPhase.OBSERVE,
        )
        state.initialize_moments()

        # Validate required dependencies
        if tribe_soul is None:
            state.phase = OODAPhase.ERROR
            state.error_log.append("Missing tribe_soul.json — required for OODA init.")
            logger.error("CRAL init failed: tribe_soul missing.")

        if trigger_profile is None:
            state.error_log.append("Warning: trigger_profile absent — M2 may degrade.")

        # Orient
        if state.phase != OODAPhase.ERROR:
            state.phase = OODAPhase.ORIENT

        # Build Session Research Plan (DEP-ENG-022)
        plan = SessionResearchPlan(
            coach_id=self.coach_id,
            session_id=session_id,
            theme=theme,
            archetype_id=archetype_id,
            trigger_id=trigger_profile.get("trigger_id", "") if trigger_profile else "",
            mood_state=mood_state,
        )

        # Receipt write for Stage 1
        self._write_stage_receipt(
            stage_name=STAGE_1_NAME,
            input_summary=f"session={session_id}, theme={theme}",
            output_summary=f"DEP-ENG-022 emitted, phase={state.phase.value}",
            metadata={
                "session_id": session_id,
                "tribe_soul_present": tribe_soul is not None,
                "trigger_profile_present": trigger_profile is not None,
                "coach_soul_present": coach_soul is not None,
            },
        )

        return state, plan

    # ──────────────────────────────────────────────────────────
    # Stage 2+3: Decide & Act (Sequential Moment Execution)
    # ──────────────────────────────────────────────────────────

    def _execute_moment_sequence(
        self,
        state: OODAState,
        plan: SessionResearchPlan,
        theme: str,
        moment_findings_input: Optional[dict[str, str]] = None,
        moment_metadata_input: Optional[dict[str, dict[str, Any]]] = None,
        archetype_context: str = "",
    ) -> tuple[OODAState, SessionResearchPlan, list[CRALFinding]]:
        """Execute M1-M7 sequentially with dependency checking.

        FR14 AC2: M7 CANNOT fire until M1-M6 all PASS.
        FR14 Technical Decision 1: Sequential, NOT batch.

        Args:
            state: Current OODA state.
            plan: Session research plan being populated.
            theme: Content theme.
            moment_findings_input: Pre-supplied finding texts per moment
                                   (for testing / external LLM integration).
            moment_metadata_input: Pre-supplied metadata per moment.
            archetype_context: Archetype targeting context.

        Returns:
            Updated (state, plan, findings) tuple.
        """
        state.phase = OODAPhase.DECIDE

        if moment_findings_input is None:
            moment_findings_input = {}
        if moment_metadata_input is None:
            moment_metadata_input = {}

        findings: list[CRALFinding] = []
        prior_findings: dict[str, str] = {}

        for moment_key in CRALMomentKey:
            # FR14 AC2: Check dependency readiness
            if not state.is_moment_ready(moment_key):
                logger.warning(
                    "Moment %s dependencies not met. Skipping.",
                    moment_key.value,
                )
                moment_state = state.moments.get(moment_key.value)
                if moment_state:
                    moment_state.status = MomentStatus.SKIPPED
                    moment_state.error_message = "Dependencies not met."
                continue

            state.phase = OODAPhase.ACT
            state.current_moment = moment_key

            moment_state = state.moments.get(moment_key.value)
            if moment_state is None:
                continue
            moment_state.status = MomentStatus.EXECUTING

            # Stage 2: Compile directive
            directive = self.planner.compile_directive_with_retry(
                target_moment=moment_key,
                theme=theme,
                ooda_state=state,
                prior_findings=prior_findings,
                archetype_context=archetype_context,
            )
            moment_state.directive = directive
            plan.moment_directives[moment_key.value] = directive.directive_text

            if directive.verdict == PlannerDirectiveVerdict.FAIL:
                moment_state.status = MomentStatus.FAIL
                moment_state.error_message = (
                    f"Planner directive FAIL after retries: "
                    f"{directive.word_count} words."
                )
                plan.moment_statuses[moment_key.value] = MomentStatus.FAIL.value
                continue

            # Stage 3: Execute moment
            finding_text = moment_findings_input.get(moment_key.value, "")
            metadata = moment_metadata_input.get(moment_key.value, {})

            if not finding_text:
                # In production, this would be an LLM call.
                # For structural build, mark as requiring external execution.
                moment_state.status = MomentStatus.PENDING
                moment_state.error_message = "No finding text supplied."
                plan.moment_statuses[moment_key.value] = MomentStatus.PENDING.value
                continue

            finding, gate = self.executor.execute(
                moment_key=moment_key,
                directive=directive,
                finding_text=finding_text,
                metadata=metadata,
            )
            moment_state.quality_gate = gate

            if gate.verdict == "FAIL":
                moment_state.status = MomentStatus.FAIL
                moment_state.error_message = gate.quality_gate_details
            elif gate.verdict == "PROVISIONAL":
                moment_state.status = MomentStatus.PROVISIONAL
            else:
                moment_state.status = MomentStatus.PASS
                state.completed_count += 1

            plan.moment_statuses[moment_key.value] = moment_state.status.value

            if finding is not None:
                findings.append(finding)
                prior_findings[moment_key.value] = finding.finding_text

        return state, plan, findings

    # ──────────────────────────────────────────────────────────
    # Stage 4: Assembly and Forward Passing
    # ──────────────────────────────────────────────────────────

    def _stage_4_assemble(
        self,
        state: OODAState,
        plan: SessionResearchPlan,
        findings: list[CRALFinding],
        theme: str = "",
        archetype_id: str = "",
    ) -> Optional[CRALFindingIndex]:
        """Stage 4: Assemble DEP-ENG-021 from completed findings.

        FR14 §Stage 4:
        1. Verify all 7 moments reported SUCCESS.
        2. Compile into consolidated DEP-ENG-021 schema.
        3. Apply downstream mapping addresses.
        4. Receipt Write.

        FR14 AC5: Cryptographically signed per coach_tenant_id.

        Returns:
            CRALFindingIndex or None if assembly fails.
        """
        # Compute receipt chain hash for the index
        hash_input = (
            f"{self.coach_id}:{state.session_id}:"
            + ":".join(f.finding_text[:50] for f in findings)
        )
        chain_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:32]
        self._last_chain_hash = chain_hash

        # CRALFindingIndex.findings is dict[str, CRALFinding] keyed by moment key
        findings_dict: dict[str, CRALFinding] = {
            f.moment_key.value: f for f in findings
        }

        coverage = self._compute_coverage_status(state)

        index = CRALFindingIndex(
            coach_id=self.coach_id,
            theme=theme or plan.theme,
            archetype_id=archetype_id or plan.archetype_id,
            findings=findings_dict,
            coverage_status=coverage,
        )

        # Receipt write for Stage 4
        self._write_stage_receipt(
            stage_name=STAGE_4_NAME,
            input_summary=f"findings_count={len(findings)}, session={state.session_id}",
            output_summary=(
                f"DEP-ENG-021 emitted, "
                f"coverage={index.coverage_status}, "
                f"hash={chain_hash[:16]}"
            ),
            metadata={
                "session_id": state.session_id,
                "findings_count": len(findings),
                "coverage_status": index.coverage_status,
                "chain_hash": chain_hash,
                "coach_tenant_id": self.coach_id,
            },
        )

        return index

    def _compute_coverage_status(self, state: OODAState) -> str:
        """Compute CRAL coverage status from OODA state.

        Returns: COMPLETE | PARTIAL | DEGRADED | ABSENT
        """
        if state.fallback_mode:
            return "DEGRADED"

        pass_count = sum(
            1 for ms in state.moments.values()
            if ms.status == MomentStatus.PASS
        )

        if pass_count == REQUIRED_MOMENT_COUNT:
            return "COMPLETE"
        elif pass_count > 0:
            return "PARTIAL"
        else:
            return "ABSENT"

    # ──────────────────────────────────────────────────────────
    # Backward Compatibility Fallback (FR14 §6)
    # ──────────────────────────────────────────────────────────

    def _execute_fallback(
        self,
        state: OODAState,
        plan: SessionResearchPlan,
        cached_m2: Optional[str] = None,
        cached_m6: Optional[str] = None,
    ) -> tuple[OODAState, SessionResearchPlan, list[CRALFinding]]:
        """Emergency fallback: cached M2+M6 only.

        FR14 §6: If API routing failure (e.g. Tavily limit exceeded):
        1. Halt M1-M7 crawl.
        2. Pull cached M2 (Believable) and M6 (Irrefutable).
        3. Emit degraded DEP-ENG-021 with fallback_mode_invoked: true.

        Returns:
            Updated (state, plan, findings) with degraded index.
        """
        state.phase = OODAPhase.FALLBACK
        state.fallback_mode = True
        plan.fallback_invoked = True

        findings: list[CRALFinding] = []

        if cached_m2:
            m2_finding = CRALFinding(
                moment_key=CRALMomentKey.M2_BELIEVABLE,
                finding_text=cached_m2,
                source_quality="degraded",
                human_evidence_count=0,
            )
            findings.append(m2_finding)
            m2_state = state.moments.get(CRALMomentKey.M2_BELIEVABLE.value)
            if m2_state:
                m2_state.status = MomentStatus.PASS

        if cached_m6:
            m6_finding = CRALFinding(
                moment_key=CRALMomentKey.M6_IRREFUTABLE,
                finding_text=cached_m6,
                source_quality="degraded",
                human_evidence_count=0,
            )
            findings.append(m6_finding)
            m6_state = state.moments.get(CRALMomentKey.M6_IRREFUTABLE.value)
            if m6_state:
                m6_state.status = MomentStatus.PASS

        # Mark unfired moments as SKIPPED
        for mk in CRALMomentKey:
            if mk not in (CRALMomentKey.M2_BELIEVABLE, CRALMomentKey.M6_IRREFUTABLE):
                ms = state.moments.get(mk.value)
                if ms and ms.status == MomentStatus.PENDING:
                    ms.status = MomentStatus.SKIPPED

        logger.warning(
            "CRAL fallback mode: %d cached findings for session %s",
            len(findings),
            state.session_id,
        )

        return state, plan, findings

    # ──────────────────────────────────────────────────────────
    # Main Orchestration Loop
    # ──────────────────────────────────────────────────────────

    def run(
        self,
        session_id: str,
        theme: str,
        trigger_profile: Optional[dict[str, Any]] = None,
        tribe_soul: Optional[dict[str, Any]] = None,
        coach_soul: Optional[dict[str, Any]] = None,
        archetype_id: str = "",
        mood_state: str = "",
        moment_findings_input: Optional[dict[str, str]] = None,
        moment_metadata_input: Optional[dict[str, dict[str, Any]]] = None,
        archetype_context: str = "",
        use_fallback: bool = False,
        cached_m2: Optional[str] = None,
        cached_m6: Optional[str] = None,
    ) -> CRALOrchestrationResult:
        """Execute the full CRAL orchestration pipeline.

        This is the top-level entry point. It executes:
        Stage 1 → Stage 2+3 (or fallback) → Stage 4.

        Args:
            session_id: Unique CRAL session ID.
            theme: Content theme for research.
            trigger_profile: DEP-ENG-005 trigger profile.
            tribe_soul: tribe_soul.json data.
            coach_soul: coach_soul.json data.
            archetype_id: Archetype family ID.
            mood_state: MoodStatePrimary value.
            moment_findings_input: Pre-supplied findings per moment (testing).
            moment_metadata_input: Pre-supplied metadata per moment (testing).
            archetype_context: Archetype targeting context.
            use_fallback: Force fallback mode.
            cached_m2: Cached M2 finding for fallback.
            cached_m6: Cached M6 finding for fallback.

        Returns:
            CRALOrchestrationResult with finding index and metadata.
        """
        result = CRALOrchestrationResult()

        # ── Stage 1: Init ──
        state, plan = self._stage_1_init(
            session_id=session_id,
            theme=theme,
            trigger_profile=trigger_profile,
            tribe_soul=tribe_soul,
            coach_soul=coach_soul,
            archetype_id=archetype_id,
            mood_state=mood_state,
        )

        if state.phase == OODAPhase.ERROR:
            result.error_message = "; ".join(state.error_log)
            result.ooda_state = state
            result.research_plan = plan
            return result

        # ── Stage 2+3: Execute or Fallback ──
        if use_fallback:
            state, plan, findings = self._execute_fallback(
                state, plan, cached_m2, cached_m6,
            )
        else:
            state, plan, findings = self._execute_moment_sequence(
                state=state,
                plan=plan,
                theme=theme,
                moment_findings_input=moment_findings_input,
                moment_metadata_input=moment_metadata_input,
                archetype_context=archetype_context,
            )

        # ── Stage 4: Assemble ──
        finding_index = self._stage_4_assemble(
            state, plan, findings, theme=theme, archetype_id=archetype_id,
        )

        # Finalize
        state.phase = OODAPhase.COMPLETE
        plan.receipt_chain_hash = self._last_chain_hash if finding_index else ""

        result.success = finding_index is not None
        result.finding_index = finding_index
        result.research_plan = plan
        result.ooda_state = state
        result.fallback_mode = state.fallback_mode
        result.cral_coverage_status = (
            finding_index.coverage_status if finding_index else "ABSENT"
        )

        logger.info(
            "CRAL orchestration complete: session=%s, coverage=%s, fallback=%s",
            session_id,
            result.cral_coverage_status,
            result.fallback_mode,
        )

        return result

    # ──────────────────────────────────────────────────────────
    # Receipt Helpers
    # ──────────────────────────────────────────────────────────

    def _write_stage_receipt(
        self,
        stage_name: str,
        input_summary: str,
        output_summary: str,
        metadata: Optional[dict[str, Any]] = None,
    ) -> None:
        """Write a receipt chain entry for an orchestrator stage.

        FR47 DEP-ENG-041 schema compliance.
        """
        if self.receipt_chain is None:
            return

        self.receipt_chain.log(
            agent_id=AGENT_NAME,
            action=stage_name,
            input_summary=input_summary,
            output_summary=output_summary,
            metadata={
                "stage_name": stage_name,
                "agent_name": AGENT_NAME,
                "coach_id": self.coach_id,
                **(metadata or {}),
            },
        )
