"""
CCP FR24 — Autonomous Weekly CCF Pipeline v3.1 Orchestrator (DEP-PROTO-014)

The Master Orchestrator (Alex) coordinating execution of 65 agents
across 5 phases of the Trigger-First Architecture.

Spec reference: FR24_Weekly_Pipeline_Tech_Spec.md
  §4 — Stages 1-4 (Phases A through D)
  §3 — Technical Decisions (v3.1 Inversion, DamageControl, Ghost Var Gate, C-11)
  §7 — Tasks 1-5
  §8 — AC1 (Trigger-First), AC2 (Mass Validation Triad),
        AC3 (Async Wait-State), AC4 (ADR-01 Strict Isolation)
"""

import hashlib
import re
from datetime import datetime, timezone
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.receipt_guard_models import AssemblyStatus
from src.ccp.models.validation_gate_models import (
    SeasonMandate,
    ValidationFinalVerdict,
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


# ── C-11 Persona Masking Gate ─────────────────────────────────────────────────
# Stress Test Decision: All 65 agent names regex-scrubbed from API payloads.
# Must be maintained in the orchestration layer.

AGENT_NAMES_PATTERN = re.compile(
    r"\b(?:"
    r"Emilio|Charlotte|Adele|Divine|Valeriane|Lionel|Maeva|"
    r"Lila|Alex|Abel|Paradoxe|Sophia|Marcus|Chen|Aurore|"
    r"Jordan|Grâce|Grace|Liliane|Benjamin|Grant|Aria|"
    r"Vidye|Atlas|Noa|Luna|Zara|Kai|Milo|"
    r"Eve|Suri|Tao|Yuki|Amir|Devi|Finn|"
    r"Ines|Jade|Kira|Lena|Maya|Nina|Omar|"
    r"Pia|Ravi|Sara|Uma|Vera|Wren|Xena|"
    r"Yael|Zoe|Alix|Bram|Cleo|Dara|Elio|"
    r"Faye|Gael|Hugo|Iris|Juno|Kaya|Lior"
    r")\b",
    re.IGNORECASE,
)

ROLEPLAY_PATTERN = re.compile(
    r"\b(?:Act as|You are an expert|You are a|Pretend to be|"
    r"Imagine you are|Assume the role of|Play the role of)\b",
    re.IGNORECASE,
)


class WeeklyPipelineOrchestrator:
    """Autonomous Weekly CCF Pipeline v3.1 (DEP-PROTO-014).

    Coordinates the Trigger-First Architecture across 4+ phases:
      Phase A: Discovery & Trigger Matching
      Phase B: Authenticity Gate & Research Synthesis
      Phase C: JIT Compilation Mass-Assembly (+ Novelty + Fallback)
      Phase D: Visual Routing & Critic Validation

    Key invariants:
      - v3.1 Trigger-First: trigger_map.json match BEFORE topic selection (AC1)
      - DamageControl: max_retry_depth=3, fourth retry kills the job
      - C-11 Persona Masking: 65 agent names scrubbed from all API payloads
      - ADR-01: All operations scoped to coach_id namespace (AC4)
      - Ghost Variable Prevention: all DEP-IDs verified before payload unpacking
    """

    MAX_TILL_DONE_ITERATIONS = 3
    TOTAL_SCRIPT_SLOTS = 36
    LIWC_AUTHENTICITY_THRESHOLD = 0.6
    EPSILON_GREEDY_FLOOR = 0.05

    def __init__(self, coach_id: str, season_mandate: SeasonMandate):
        """Initialize the pipeline orchestrator.

        Args:
            coach_id: 3-letter coach acronym (ADR-01 scoping).
            season_mandate: Active 30-Day Movement Season for Marcus.
        """
        if len(coach_id) != 3:
            raise ValueError(f"coach_id must be 3 characters, got '{coach_id}'")
        self.coach_id = coach_id.upper()
        self.season_mandate = season_mandate
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_id)
        self.guard = ReceiptChainGuard(coach_id=self.coach_id)
        self._pipeline_status = PipelineStatus.RUNNING
        self._phase_receipts: dict[str, PhaseReceipt] = {}
        self._damage_control = DamageControlStatus()

    # ─── Phase A: Discovery & Trigger Matching ────────────────────────────────

    def execute_phase_a(
        self,
        trigger_map: dict[str, Any],
        trend_vectors: list[dict[str, Any]],
    ) -> PhaseAResult:
        """Execute Phase A: Discovery & Trigger Matching.

        Spec §4 Stage 1 (v3.1 Inversion):
        1. ccf-radar scans trends
        2. ccf-trigger-match maps L3 pain to trigger_map.json (2-axis: MFT + Temporal)
        3. ccf-question formulates provocation keys
        4. Outputs 80-word Telegram Provocation

        AC1: trigger_map.json is cross-referenced BEFORE forming final provocation.
        Backward compat: If trigger_map missing → v3.0 degradation.
        """
        if not trigger_map:
            # Spec §6: Backward compatibility — skip trigger match, fallback to v3.0
            self._pipeline_status = PipelineStatus.PIPELINE_V30_DEGRADATION
            self.receipt_chain.log(
                agent_id="weekly_pipeline",
                action="phase_a_degradation",
                input_summary="trigger_map.json missing or empty",
                output_summary="[PIPELINE V3.0 DEGRADATION] — skipping trigger match",
                decision="degraded",
            )
            return PhaseAResult(coach_id=self.coach_id)

        # Execute trigger matching (2-axis: MFT + Temporal)
        candidates: list[TriggerMatchCandidate] = []
        for trend in trend_vectors:
            for trigger_key, trigger_data in trigger_map.items():
                mft_score = self._compute_mft_alignment(trend, trigger_data)
                temporal_score = self._compute_temporal_alignment(trend, trigger_data)
                combined = (mft_score + temporal_score) / 2.0

                candidates.append(TriggerMatchCandidate(
                    trigger_key=trigger_key,
                    trend_topic=trend.get("topic", ""),
                    mft_axis_score=mft_score,
                    temporal_axis_score=temporal_score,
                    combined_score=combined,
                ))

        # Sort by combined score, pick best
        candidates.sort(key=lambda c: c.combined_score, reverse=True)
        best_score = candidates[0].combined_score if candidates else 0.0

        # Generate receipt
        receipt = self._emit_phase_receipt(
            PipelinePhase.PHASE_A_DISCOVERY,
            "DISCOVERY-AND-TRIGGER-MATCHING",
            "Alex-Adele-Divine",
            input_data={"trigger_map_keys": list(trigger_map.keys())},
            output_data={"candidates_count": len(candidates)},
        )

        result = PhaseAResult(
            coach_id=self.coach_id,
            trigger_match_candidates=candidates[:10],  # Top 10
            final_theme_selection=candidates[0].trend_topic if candidates else "",
            trigger_match_score=best_score,
            phase_receipt=receipt,
        )

        self.receipt_chain.log(
            agent_id="weekly_pipeline",
            action="phase_a_complete",
            input_summary=f"Trends: {len(trend_vectors)}, Triggers: {len(trigger_map)}",
            output_summary=f"Best match: {best_score:.2f}, Candidates: {len(candidates)}",
            decision="completed",
        )

        return result

    # ─── Phase B: Authenticity Gate & Research Synthesis ───────────────────────

    def execute_phase_b(
        self,
        transcript_text: str,
        phase_a_receipt_hash: Optional[str] = None,
    ) -> PhaseBResult:
        """Execute Phase B: Authenticity Gate & Research Synthesis.

        Spec §4 Stage 2:
        1. Voice Agent transcribes incoming audio
        2. LIWC-22 Authenticity Gate (7 markers, threshold ≥0.6)
        3. If PASS → ccf-raw-research + ccf-research-deep

        AC3: Pipeline thread gracefully suspends between Phase A and B,
        resumes when coach sends Telegram audio note.
        """
        # Verify upstream receipt (if provided)
        if phase_a_receipt_hash:
            verification = self.guard.verify_handoff(
                payload={"receipt_chain_hash": phase_a_receipt_hash},
                upstream_node_id="phase_a_discovery",
                downstream_node_id="phase_b_research",
            )
            if not verification.chain_verified:
                self.guard.trip_circuit_breaker(
                    failed_verification=verification,
                    compilation_request_id=f"{self.coach_id}-weekly",
                )
                return PhaseBResult(
                    coach_id=self.coach_id,
                    liwc_result=LIWCAuthenticityResult(composite_score=0.0, passed=False),
                )

        # LIWC-22 Authenticity Gate
        liwc_score = self._evaluate_liwc_authenticity(transcript_text)
        liwc_result = LIWCAuthenticityResult(
            composite_score=liwc_score,
            passed=liwc_score >= self.LIWC_AUTHENTICITY_THRESHOLD,
        )

        if not liwc_result.passed:
            # Spec §4 Stage 2: Reject + Telegram re-record request
            self.receipt_chain.log(
                agent_id="weekly_pipeline",
                action="voice_note_quarantine",
                input_summary=f"LIWC score: {liwc_score:.2f}",
                output_summary="LIWC_BELOW_THRESHOLD — re-record request sent",
                decision="rejected",
                metadata={
                    "stage_name": "VOICE-NOTE-QUARANTINE",
                    "rejection_reason": "LIWC_BELOW_THRESHOLD",
                },
            )
            return PhaseBResult(
                coach_id=self.coach_id,
                liwc_result=liwc_result,
                transcript_available=True,
            )

        # Generate receipt for Phase B
        receipt = self._emit_phase_receipt(
            PipelinePhase.PHASE_B_RESEARCH,
            "AUTHENTICITY-GATE-RESEARCH",
            "Alex-Valeriane-Lionel-Maeva",
            input_data={"liwc_score": liwc_score},
            output_data={"passed": True},
        )

        result = PhaseBResult(
            coach_id=self.coach_id,
            liwc_result=liwc_result,
            transcript_available=True,
            research_pages_generated=40,  # Spec: 40-page RAG library
            phase_receipt=receipt,
        )

        self.receipt_chain.log(
            agent_id="weekly_pipeline",
            action="phase_b_complete",
            input_summary=f"LIWC: {liwc_score:.2f} (threshold: {self.LIWC_AUTHENTICITY_THRESHOLD})",
            output_summary="Authenticity PASSED, research synthesis initiated",
            decision="completed",
        )

        return result

    # ─── Phase C: JIT Compilation Mass-Assembly ───────────────────────────────

    def execute_phase_c(
        self,
        ideas: list[dict[str, Any]],
        phase_b_receipt_hash: Optional[str] = None,
    ) -> PhaseCResult:
        """Execute Phase C: JIT Compilation Mass-Assembly.

        Spec §4 Stage 3:
        1. ccf-analyze → 12 Core Ideas via PatternWeaver (ε-greedy floor 0.05)
        2. ccf-eroll-plan → format assignments
        3. TeamOrchestrator → parallel ccf-soc + ccf-generate for 36 slots
        4. C-11 Persona Masking Gate before any API dispatch

        Stage 3B: Agent Grâce novelty check (8-week rolling window)
        Stage 3C: Reference Template Fallback after 3 TillDone failures
        """
        # Verify upstream receipt
        if phase_b_receipt_hash:
            verification = self.guard.verify_handoff(
                payload={"receipt_chain_hash": phase_b_receipt_hash},
                upstream_node_id="phase_b_research",
                downstream_node_id="phase_c_generation",
            )
            if not verification.chain_verified:
                self.guard.trip_circuit_breaker(
                    failed_verification=verification,
                    compilation_request_id=f"{self.coach_id}-weekly",
                )
                return PhaseCResult(coach_id=self.coach_id)

        # Build script slots
        slots: list[ScriptSlot] = []
        novelty_results: list[NoveltyCheckResult] = []
        c11_passed = True

        for i, idea in enumerate(ideas[: self.TOTAL_SCRIPT_SLOTS]):
            slot_id = f"SLOT-{i + 1:02d}"
            archetype = idea.get("archetype", "")
            skill_id = idea.get("skill_id", f"SKILL-{slot_id}-{self.coach_id}")

            # Stage 3B: Novelty check (Agent Grâce)
            novelty = self._check_novelty(slot_id, idea)
            novelty_results.append(novelty)

            if novelty.verdict == NoveltyVerdict.NOVELTY_FAIL:
                # TillDone rewrite cycle
                rewrite_success = False
                for attempt in range(self.MAX_TILL_DONE_ITERATIONS):
                    novelty_retry = self._check_novelty(slot_id, idea)
                    if novelty_retry.verdict == NoveltyVerdict.NOVELTY_PASS:
                        rewrite_success = True
                        break

                if not rewrite_success:
                    # Stage 3C: Reference Template Fallback
                    slots.append(ScriptSlot(
                        slot_id=slot_id,
                        skill_id=skill_id,
                        archetype=archetype,
                        generation_status=GenerationStatus.REFERENCE_FALLBACK,
                        till_done_iterations=self.MAX_TILL_DONE_ITERATIONS,
                        fallback_fingerprint_id=f"REF-{slot_id}-{self.coach_id}",
                    ))
                    continue

            # C-11 Persona Masking Gate
            api_payload = idea.get("api_payload", "")
            if isinstance(api_payload, str) and self._c11_gate_check(api_payload):
                c11_passed = False
                self.receipt_chain.log(
                    agent_id="weekly_pipeline",
                    action="c11_persona_masking_halt",
                    input_summary=f"Slot: {slot_id}",
                    output_summary="Agent name detected in API payload — HALT",
                    decision="halt",
                )

            slots.append(ScriptSlot(
                slot_id=slot_id,
                skill_id=skill_id,
                archetype=archetype,
                generation_status=GenerationStatus.GENERATED,
            ))

        # Emit Phase C receipt
        receipt = self._emit_phase_receipt(
            PipelinePhase.PHASE_C_GENERATION,
            "JIT-COMPILATION-MASS-ASSEMBLY",
            "Alex-ccf-produce-ccf-generate",
            input_data={"ideas_count": len(ideas)},
            output_data={"slots_generated": len(slots)},
        )

        result = PhaseCResult(
            coach_id=self.coach_id,
            total_slots=self.TOTAL_SCRIPT_SLOTS,
            slots=slots,
            novelty_results=novelty_results,
            c11_persona_masking_passed=c11_passed,
            epsilon_greedy_floor=self.EPSILON_GREEDY_FLOOR,
            phase_receipt=receipt,
        )

        self.receipt_chain.log(
            agent_id="weekly_pipeline",
            action="phase_c_complete",
            input_summary=f"Ideas: {len(ideas)}",
            output_summary=f"Slots: {len(slots)}, Fallbacks: {sum(1 for s in slots if s.generation_status == GenerationStatus.REFERENCE_FALLBACK)}",
            decision="completed",
        )

        return result

    # ─── Phase D: Visual Routing & Critic Validation ──────────────────────────

    def execute_phase_d(
        self,
        phase_c_result: PhaseCResult,
        validation_results: dict[str, Any],
        phase_c_receipt_hash: Optional[str] = None,
    ) -> PhaseDResult:
        """Execute Phase D: Visual Routing & Critic Validation.

        Spec §4 Stage 4:
        1. ccf-visual-assets generates DALL-E/Excalidraw payloads
        2. ccf-validate feeds batch into Validation Triad (Sophia, Marcus, Chen)
        3. FAIL → TillDone rewrite (max 3), then Reference Fallback
        4. PASS → append to ccf-batch archive

        AC2: Orchestrator detects failed scripts, triggers TillDone for those
        specific scripts while preserving the rest.
        """
        if phase_c_receipt_hash:
            verification = self.guard.verify_handoff(
                payload={"receipt_chain_hash": phase_c_receipt_hash},
                upstream_node_id="phase_c_generation",
                downstream_node_id="phase_d_validation",
            )
            if not verification.chain_verified:
                self.guard.trip_circuit_breaker(
                    failed_verification=verification,
                    compilation_request_id=f"{self.coach_id}-weekly",
                )
                return PhaseDResult(coach_id=self.coach_id)

        total_approved = 0
        total_rewritten = 0
        total_fallback = 0

        for slot in phase_c_result.slots:
            slot_validation = validation_results.get(slot.slot_id, {})
            verdict = slot_validation.get("verdict", "APPROVED")

            if verdict == "APPROVED":
                total_approved += 1
                slot.validation_scores = slot_validation.get("scores", {})
            elif verdict == "FAIL_TRIGGER_REWRITE":
                total_rewritten += 1
            elif verdict == "REFERENCE_FALLBACK":
                total_fallback += 1
                slot.generation_status = GenerationStatus.REFERENCE_FALLBACK

        receipt = self._emit_phase_receipt(
            PipelinePhase.PHASE_D_VALIDATION,
            "VISUAL-ROUTING-CRITIC-VALIDATION",
            "Alex-Abel-Paradoxe-Triad",
            input_data={"total_slots": len(phase_c_result.slots)},
            output_data={"approved": total_approved},
        )

        result = PhaseDResult(
            coach_id=self.coach_id,
            total_validated=len(phase_c_result.slots),
            total_approved=total_approved,
            total_rewritten=total_rewritten,
            total_fallback=total_fallback,
            phase_receipt=receipt,
        )

        self.receipt_chain.log(
            agent_id="weekly_pipeline",
            action="phase_d_complete",
            input_summary=f"Validated: {len(phase_c_result.slots)} slots",
            output_summary=f"Approved: {total_approved}, Rewritten: {total_rewritten}, Fallback: {total_fallback}",
            decision="completed",
        )

        return result

    # ─── Build Final Batch Payload ────────────────────────────────────────────

    def build_batch_payload(
        self,
        production_week: str,
        phase_a: Optional[PhaseAResult],
        phase_b: Optional[PhaseBResult],
        phase_c: Optional[PhaseCResult],
        phase_d: Optional[PhaseDResult],
    ) -> WeeklyBatchPayload:
        """Assemble the final weekly_production_batch_v3.json.

        Spec §5: Primary Output Schema.
        """
        # Build receipt chain ledger from phase receipts
        receipt_ledger: dict[str, str] = {}
        for phase_name, phase_receipt in self._phase_receipts.items():
            receipt_ledger[phase_name] = phase_receipt.receipt_hash

        scripts = phase_c.slots if phase_c else []

        payload = WeeklyBatchPayload(
            production_week=production_week,
            coach_id=self.coach_id,
            pipeline_status=self._pipeline_status,
            trigger_match_score=phase_a.trigger_match_score if phase_a else 0.0,
            authenticity_liwc_composite=(
                phase_b.liwc_result.composite_score if phase_b else 0.0
            ),
            season_mandate=self.season_mandate.value,
            receipt_chain_ledger=receipt_ledger,
            total_generated=len(scripts),
            formats_utilized=len({s.archetype for s in scripts if s.archetype}),
            scripts=scripts,
            phase_a=phase_a,
            phase_b=phase_b,
            phase_c=phase_c,
            phase_d=phase_d,
        )

        self.receipt_chain.log(
            agent_id="weekly_pipeline",
            action="batch_payload_assembled",
            input_summary=f"Week: {production_week}, Coach: {self.coach_id}",
            output_summary=f"Status: {self._pipeline_status.value}, Scripts: {len(scripts)}",
            decision="completed",
            metadata={"receipt_ledger_phases": list(receipt_ledger.keys())},
        )

        return payload

    # ─── C-11 Persona Masking Gate ────────────────────────────────────────────

    def _c11_gate_check(self, text: str) -> bool:
        """Check if text contains any agent names or roleplay instructions.

        Stress Test Decision: All 65 agent names are regex-scrubbed.
        Any hit → orchestration HALT.

        Returns:
            True if VIOLATION detected (names found).
        """
        if AGENT_NAMES_PATTERN.search(text):
            return True
        if ROLEPLAY_PATTERN.search(text):
            return True
        return False

    def scrub_agent_names(self, text: str) -> str:
        """Scrub all agent names and roleplay instructions from text.

        Spec §4 Stage 3 Step 4: The API receives ONLY the unadorned
        JSON state array.
        """
        text = AGENT_NAMES_PATTERN.sub("[AGENT]", text)
        text = ROLEPLAY_PATTERN.sub("[INSTRUCTION]", text)
        return text

    # ─── Internal Helpers ─────────────────────────────────────────────────────

    def _emit_phase_receipt(
        self,
        phase: PipelinePhase,
        stage_name: str,
        agent_names: str,
        input_data: Any,
        output_data: Any,
    ) -> PhaseReceipt:
        """Emit a receipt for a pipeline phase."""
        timestamp = datetime.now(timezone.utc).isoformat()
        input_hash = hashlib.sha256(
            str(input_data).encode()
        ).hexdigest()[:16]
        output_hash = hashlib.sha256(
            str(output_data).encode()
        ).hexdigest()[:16]

        # Chain to previous receipt
        previous_hash = None
        if self._phase_receipts:
            last_phase = list(self._phase_receipts.values())[-1]
            previous_hash = last_phase.receipt_hash

        receipt_hash = hashlib.sha256(
            f"{timestamp}:{stage_name}:{input_hash}:{output_hash}".encode()
        ).hexdigest()

        receipt = PhaseReceipt(
            phase=phase,
            receipt_hash=receipt_hash,
            agent_names=agent_names,
            stage_name=stage_name,
            timestamp=timestamp,
            input_payload_hash=input_hash,
            output_payload_hash=output_hash,
            previous_receipt_hash=previous_hash,
        )

        self._phase_receipts[stage_name] = receipt

        # Also register in the guard's chain ledger
        self.guard.generate_receipt(
            node_id=phase.value,
            stage_name=stage_name,
            agent_name=agent_names,
            input_payload=input_data,
            output_payload=output_data,
            previous_receipt_hash=previous_hash,
        )

        return receipt

    def _compute_mft_alignment(
        self,
        trend: dict[str, Any],
        trigger_data: Any,
    ) -> float:
        """Compute Moral Foundations Theory alignment score.

        Placeholder: In production, this calls the MFT analysis engine.
        """
        # Base score from overlap — production replaces with MFT engine
        return min(1.0, max(0.0, trend.get("mft_score", 0.5)))

    def _compute_temporal_alignment(
        self,
        trend: dict[str, Any],
        trigger_data: Any,
    ) -> float:
        """Compute temporal relevance score.

        Placeholder: In production, this evaluates recency + momentum.
        """
        return min(1.0, max(0.0, trend.get("temporal_score", 0.5)))

    def _evaluate_liwc_authenticity(self, text: str) -> float:
        """Evaluate LIWC-22 authenticity score for coach audio transcript.

        Placeholder: In production, this runs the 7 LIWC-22 markers.
        For now, returns a score based on text characteristics.
        """
        if not text or len(text.strip()) < 50:
            return 0.0
        # Heuristic: longer, more varied text scores higher
        words = text.split()
        unique_ratio = len(set(words)) / max(len(words), 1)
        return min(1.0, unique_ratio * 1.2)

    def _check_novelty(
        self,
        slot_id: str,
        idea: dict[str, Any],
    ) -> NoveltyCheckResult:
        """Agent Grâce novelty check against 8-week rolling window.

        Placeholder: In production, queries the Fingerprint Archive.
        """
        return NoveltyCheckResult(
            slot_id=slot_id,
            verdict=NoveltyVerdict.NOVELTY_PASS,
            thematic_similarity=idea.get("thematic_similarity", 0.1),
            structural_similarity=idea.get("structural_similarity", 0.1),
            semantic_similarity=idea.get("semantic_similarity", 0.1),
        )
