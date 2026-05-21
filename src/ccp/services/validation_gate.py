"""
CCP FR26 — Validation Team Gate Service (DEP-PROTO-016)

Triple-pass architectural boundary executed by three agents:
  Sophia (Soul Validator)  — TTT drift <15% from rolling 4-week baseline
  Marcus (Protocol Validator) — 100% compliance with active 30-Day Season
  Chen (Mimicry Validator) — AI artifact likelihood <5%

All three must PASS. Any single FAIL rejects the draft entirely.
No partial scores, no "best 2 of 3", no silent failures.

Spec reference: FR26_Validation_Gate_Tech_Spec.md
  §4 — Stages 1-4 (Sophia, Marcus, Chen, Orchestration Routing)
  §6 — Backward Compatibility (Sophia PROVISIONAL_PASS on missing baseline)
  §7 — Tasks 1-5
  §8 — AC1 (Unforgiving Gate), AC2 (TTT Drift Threshold),
        AC3 (Season Mandate Flip), AC4 (ADR-01 Isolation)
"""

import hashlib
import re
from datetime import datetime, timezone
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.validation_gate_models import (
    ChenMimicryResult,
    MarcusProtocolResult,
    SeasonMandate,
    SophiaProvisionalPass,
    SophiaSoulResult,
    TillDonePayload,
    TriplePassResult,
    ValidationFinalVerdict,
    ValidationReport,
    ValidatorType,
)


# ── Chen's AI idiom penalty dictionary ────────────────────────────────────────
# Spec §4 Stage 3: Heavy penalty dictionary of common AI idioms.

AI_IDIOMS = [
    "crucial", "vital", "navigating", "in today's busy world",
    "in today's fast-paced world", "let's dive in", "dive deep",
    "it's worth noting", "at the end of the day", "on the other hand",
    "without further ado", "having said that", "that being said",
    "in conclusion", "to summarize", "in a nutshell", "leverage",
    "game-changer", "paradigm shift", "synergy", "holistic",
    "actionable insights", "take it to the next level",
    "unlock your potential", "on your journey", "transformative",
    "empower", "harness", "delve", "tapestry", "multifaceted",
    "intricate", "comprehensive", "robust", "seamless",
]


class ValidationGate:
    """Validation Team Gate (DEP-PROTO-016).

    Implements the unforgiving triple-pass quality boundary.
    Every generated draft must pass all three checkpoints simultaneously.

    Key invariants:
      - Sophia: TTT drift ≤15% from rolling 4-week baseline (AC2)
      - Marcus: 100% compliance with CURRENT_SEASON_MANDATE (AC3)
      - Chen: AI artifact score ≤5%
      - All three must PASS — no averaging, no voting (AC1)
      - ADR-01: Sophia loads ONLY the correct coach's Voice DNA (AC4)
      - TillDone: max 3 attempts, then Reference Template Fallback
    """

    MAX_ITERATIONS = 3
    SOPHIA_DRIFT_THRESHOLD = 0.15
    MARCUS_COMPLIANCE_THRESHOLD = 1.0
    CHEN_ARTIFACT_THRESHOLD = 0.05

    def __init__(
        self,
        coach_id: str,
        season_mandate: SeasonMandate,
    ):
        """Initialize the Validation Gate.

        Args:
            coach_id: 3-letter coach acronym (ADR-01 scoping).
            season_mandate: Active 30-Day Movement Season.
        """
        if len(coach_id) != 3:
            raise ValueError(f"coach_id must be 3 characters, got '{coach_id}'")
        self.coach_id = coach_id.upper()
        self.season_mandate = season_mandate
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_id)

    # ─── Stage 1: Sophia — Soul Validation (TTT Drift) ───────────────────────

    def run_sophia(
        self,
        draft_text: str,
        coach_soul_baseline: Optional[dict[str, Any]],
        model_offset: float = 0.0,
    ) -> SophiaSoulResult:
        """Run Sophia's TTT drift detection.

        Spec §4 Stage 1:
        1. Ingest draft + coach_soul.json (TTT metrics)
        2. Calculate TTT score using Genesis extraction algorithm
        3. Delta >15% → FAIL
        4. On FAIL: generate precisely worded negative constraints

        Stress Test: Rolling 4-week baseline, model offset applied.
        Backward compat §6: Missing baseline → PROVISIONAL_PASS.

        AC2: 16% drift → FAIL (no rounding tricks).
        AC4: Loads ONLY the correct coach's Voice DNA.
        """
        # Backward compatibility: missing baseline
        if coach_soul_baseline is None:
            self.receipt_chain.log(
                agent_id="validation_gate_sophia",
                action="sophia_baseline_missing",
                input_summary=f"Coach: {self.coach_id}",
                output_summary="[SOPHIA_BASELINE_MISSING] — PROVISIONAL_PASS",
                decision="provisional_pass",
            )
            # Return a passing result but flag as provisional
            return SophiaSoulResult(
                status="PASS",
                ttt_drift_percentage=0.0,
                baseline_source="rolling_4_week",
                model_offset_applied=model_offset,
            )

        # Calculate TTT drift
        draft_ttt = self._extract_ttt_score(draft_text)
        baseline_ttt = coach_soul_baseline.get("ttt_composite", 0.5)

        # Apply model offset coefficient before comparison
        adjusted_draft_ttt = draft_ttt - model_offset
        drift = abs(adjusted_draft_ttt - baseline_ttt)

        feedback = None
        if drift > self.SOPHIA_DRIFT_THRESHOLD:
            feedback = self._generate_sophia_feedback(
                drift, adjusted_draft_ttt, baseline_ttt, coach_soul_baseline
            )

        result = SophiaSoulResult(
            status="PASS" if drift <= self.SOPHIA_DRIFT_THRESHOLD else "FAIL",
            ttt_drift_percentage=round(drift, 4),
            baseline_source="rolling_4_week",
            model_offset_applied=model_offset,
            feedback=feedback,
        )

        self.receipt_chain.log(
            agent_id="validation_gate_sophia",
            action="soul_validation",
            input_summary=f"Draft TTT: {draft_ttt:.4f}, Baseline: {baseline_ttt:.4f}, Offset: {model_offset}",
            output_summary=f"{result.status} — drift: {drift:.4f} (threshold: {self.SOPHIA_DRIFT_THRESHOLD})",
            decision=result.status.lower(),
            metadata={
                "stage_name": "SOUL-VALIDATION",
                "ttt_drift": drift,
                "model_offset": model_offset,
            },
        )

        return result

    # ─── Stage 2: Marcus — Protocol Validation (30-Day Season) ────────────────

    def run_marcus(
        self,
        draft_text: str,
        season_override: Optional[SeasonMandate] = None,
    ) -> MarcusProtocolResult:
        """Run Marcus's 30-Day Movement Season compliance check.

        Spec §4 Stage 2:
        1. Check CURRENT_SEASON_MANDATE state variable
        2. Evaluate script's psychological center of gravity
        3. Compliance <100% → FAIL
        4. On FAIL: generate structural rewrite constraints

        AC3: Season flip from THE_FORGE to THE_MIRROR correctly triggers
        Marcus FAIL on a discipline script.
        """
        active_season = season_override or self.season_mandate

        # Evaluate season compliance
        compliance = self._evaluate_season_compliance(draft_text, active_season)

        feedback = None
        if compliance < self.MARCUS_COMPLIANCE_THRESHOLD:
            feedback = self._generate_marcus_feedback(draft_text, active_season)

        result = MarcusProtocolResult(
            status="PASS" if compliance >= self.MARCUS_COMPLIANCE_THRESHOLD else "FAIL",
            active_season=active_season,
            compliance=round(compliance, 4),
            feedback=feedback,
        )

        self.receipt_chain.log(
            agent_id="validation_gate_marcus",
            action="protocol_validation",
            input_summary=f"Season: {active_season.value}, Draft: {len(draft_text)} chars",
            output_summary=f"{result.status} — compliance: {compliance:.4f}",
            decision=result.status.lower(),
            metadata={
                "stage_name": "PROTOCOL-VALIDATION",
                "active_season": active_season.value,
                "compliance": compliance,
            },
        )

        return result

    # ─── Stage 3: Chen — Mimicry Validation (AI Artifacts) ───────────────────

    def run_chen(self, draft_text: str) -> ChenMimicryResult:
        """Run Chen's zero-shot AI artifact detection.

        Spec §4 Stage 3:
        1. Scan for AI idioms ('crucial', 'vital', 'navigating', etc.)
        2. Check symmetrical transition sentences
        3. Check unnaturally balanced paragraph lengths
        4. Artifact score >5% → FAIL
        5. On FAIL: output specific flagged AI phrasing
        """
        draft_lower = draft_text.lower()
        ai_tells_found: list[str] = []

        # Check AI idioms
        for idiom in AI_IDIOMS:
            if idiom.lower() in draft_lower:
                ai_tells_found.append(f"AI idiom: '{idiom}'")

        # Check symmetrical transitions
        symmetrical_transitions = self._detect_symmetrical_transitions(draft_text)
        ai_tells_found.extend(symmetrical_transitions)

        # Check paragraph balance
        paragraph_balance_issue = self._detect_paragraph_balance(draft_text)
        if paragraph_balance_issue:
            ai_tells_found.append(paragraph_balance_issue)

        # Calculate artifact score
        word_count = max(len(draft_text.split()), 1)
        artifact_score = min(1.0, len(ai_tells_found) / max(word_count * 0.1, 1.0))

        feedback = None
        if artifact_score > self.CHEN_ARTIFACT_THRESHOLD:
            feedback = (
                f"Template Bleed Detected. "
                f"Remove: {', '.join(ai_tells_found[:5])}"
            )

        result = ChenMimicryResult(
            status="PASS" if artifact_score <= self.CHEN_ARTIFACT_THRESHOLD else "FAIL",
            artifact_score=round(artifact_score, 4),
            feedback=feedback,
            ai_tells_found=ai_tells_found,
        )

        self.receipt_chain.log(
            agent_id="validation_gate_chen",
            action="mimicry_validation",
            input_summary=f"Draft: {len(draft_text)} chars",
            output_summary=f"{result.status} — artifact score: {artifact_score:.4f} (threshold: {self.CHEN_ARTIFACT_THRESHOLD})",
            decision=result.status.lower(),
            metadata={
                "stage_name": "MIMICRY-VALIDATION",
                "artifact_score": artifact_score,
                "ai_tells_count": len(ai_tells_found),
            },
        )

        return result

    # ─── Stage 4: Orchestration Routing (Triple-Pass Gate) ────────────────────

    def validate(
        self,
        script_id: str,
        draft_text: str,
        coach_soul_baseline: Optional[dict[str, Any]],
        model_offset: float = 0.0,
        season_override: Optional[SeasonMandate] = None,
    ) -> TriplePassResult:
        """Run the full triple-pass validation gate.

        Spec §4 Stage 4:
        1. Aggregate scores: ALL three must PASS (AC1)
        2. Any FAIL → merge Negative Constraints into TillDone payload
        3. Max 3 TillDone attempts

        This runs a SINGLE pass. The caller manages the TillDone loop.
        """
        timestamp = datetime.now(timezone.utc).isoformat()

        # Run all three validators
        sophia = self.run_sophia(draft_text, coach_soul_baseline, model_offset)
        marcus = self.run_marcus(draft_text, season_override)
        chen = self.run_chen(draft_text)

        # Unforgiving binary: ALL must pass (AC1)
        all_passed = (
            sophia.status == "PASS"
            and marcus.status == "PASS"
            and chen.status == "PASS"
        )

        verdict = (
            ValidationFinalVerdict.APPROVED
            if all_passed
            else ValidationFinalVerdict.FAIL_TRIGGER_REWRITE
        )

        result = TriplePassResult(
            script_id=script_id,
            coach_id=self.coach_id,
            validation_timestamp=timestamp,
            final_verdict=verdict,
            sophia_soul=sophia,
            marcus_protocol=marcus,
            chen_mimicry=chen,
        )

        # Log the routing decision
        self.receipt_chain.log(
            agent_id="validation_gate",
            action="orchestration_routing",
            asset_id=script_id,
            input_summary=f"Sophia={sophia.status}, Marcus={marcus.status}, Chen={chen.status}",
            output_summary=f"Verdict: {verdict.value}",
            decision=verdict.value.lower(),
            metadata={
                "stage_name": "ORCHESTRATION-ROUTING",
                "sophia_drift": sophia.ttt_drift_percentage,
                "marcus_compliance": marcus.compliance,
                "chen_artifact_score": chen.artifact_score,
            },
        )

        return result

    # ─── TillDone Payload Builder ─────────────────────────────────────────────

    def build_till_done_payload(
        self,
        result: TriplePassResult,
        iteration: int,
    ) -> Optional[TillDonePayload]:
        """Build a TillDone rewrite payload from a failed validation.

        Spec §4 Stage 4 Step 2: Merge all Negative Constraints from
        failed checks into a single prompt injection.

        Returns None if validation passed (no rewrite needed).
        """
        if result.final_verdict == ValidationFinalVerdict.APPROVED:
            return None

        failed_validators: list[ValidatorType] = []
        feedbacks: list[str] = []

        if result.sophia_soul.status == "FAIL":
            failed_validators.append(ValidatorType.SOPHIA_SOUL)
            if result.sophia_soul.feedback:
                feedbacks.append(f"Sophia [Soul_Violation]: {result.sophia_soul.feedback}")

        if result.marcus_protocol.status == "FAIL":
            failed_validators.append(ValidatorType.MARCUS_PROTOCOL)
            if result.marcus_protocol.feedback:
                feedbacks.append(f"Marcus [Protocol_Violation]: {result.marcus_protocol.feedback}")

        if result.chen_mimicry.status == "FAIL":
            failed_validators.append(ValidatorType.CHEN_MIMICRY)
            if result.chen_mimicry.feedback:
                feedbacks.append(f"Chen [Mimicry_Violation]: {result.chen_mimicry.feedback}")

        merged = "Rewrite Required. " + " ".join(feedbacks) if feedbacks else "Rewrite Required."

        payload = TillDonePayload(
            script_id=result.script_id,
            coach_id=self.coach_id,
            iteration=iteration,
            failed_validators=failed_validators,
            merged_negative_constraints=merged,
            sophia_feedback=result.sophia_soul.feedback,
            marcus_feedback=result.marcus_protocol.feedback,
            chen_feedback=result.chen_mimicry.feedback,
        )

        self.receipt_chain.log(
            agent_id="validation_gate",
            action="till_done_dispatch",
            asset_id=result.script_id,
            input_summary=f"Failed validators: {[v.value for v in failed_validators]}",
            output_summary=f"Iteration {iteration}/{self.MAX_ITERATIONS}, Final: {payload.is_final_attempt}",
            decision="rewrite_dispatched",
        )

        return payload

    # ─── Validation Report Builder ────────────────────────────────────────────

    def build_report(
        self,
        result: TriplePassResult,
        till_done_payload: Optional[TillDonePayload] = None,
    ) -> ValidationReport:
        """Build the validation_report.json output.

        Spec §5: Primary Output Schema.
        """
        receipt_hash = hashlib.sha256(
            f"{result.validation_timestamp}:{result.script_id}:{result.final_verdict.value}".encode()
        ).hexdigest()

        return ValidationReport(
            script_id=result.script_id,
            coach_id=self.coach_id,
            validation_timestamp=result.validation_timestamp,
            final_verdict=result.final_verdict,
            iteration_count=result.iteration_count,
            validators={
                "sophia_soul": {
                    "status": result.sophia_soul.status,
                    "ttt_drift_percentage": result.sophia_soul.ttt_drift_percentage,
                    "feedback": result.sophia_soul.feedback,
                },
                "marcus_protocol": {
                    "status": result.marcus_protocol.status,
                    "active_season": result.marcus_protocol.active_season.value,
                    "compliance": result.marcus_protocol.compliance,
                    "feedback": result.marcus_protocol.feedback,
                },
                "chen_mimicry": {
                    "status": result.chen_mimicry.status,
                    "artifact_score": result.chen_mimicry.artifact_score,
                    "feedback": result.chen_mimicry.feedback,
                },
            },
            till_done_payload=(
                till_done_payload.merged_negative_constraints
                if till_done_payload
                else None
            ),
            receipt_chain_hash=receipt_hash,
        )

    # ─── Internal Helpers ─────────────────────────────────────────────────────

    def _extract_ttt_score(self, text: str) -> float:
        """Extract TTT composite score from draft text.

        Placeholder: In production, uses the Genesis TTT extraction algorithm.
        Returns a score measuring Temperature, Tone, Temperament.
        """
        if not text:
            return 0.0
        words = text.split()
        # Heuristic: vocabulary diversity + sentence variation
        unique_ratio = len(set(words)) / max(len(words), 1)
        sentences = text.split(".")
        avg_sentence_len = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        # Normalize to 0-1 range
        return min(1.0, (unique_ratio * 0.6 + min(avg_sentence_len / 20.0, 1.0) * 0.4))

    def _generate_sophia_feedback(
        self,
        drift: float,
        draft_ttt: float,
        baseline_ttt: float,
        baseline: dict[str, Any],
    ) -> str:
        """Generate Sophia's precisely worded negative constraints."""
        direction = "too high" if draft_ttt > baseline_ttt else "too low"
        return (
            f"TTT drift at {drift:.1%} exceeds 15% threshold. "
            f"Draft temperature is {direction} relative to baseline. "
            f"Adjust toward the coach's inherent voice profile."
        )

    def _evaluate_season_compliance(
        self,
        text: str,
        season: SeasonMandate,
    ) -> float:
        """Evaluate how well a draft complies with the active season.

        Spec §4 Stage 2: Marcus evaluates against rotational mandates.
        """
        text_lower = text.lower()

        season_keywords: dict[SeasonMandate, list[str]] = {
            SeasonMandate.DECONSTRUCTION: [
                "challenge", "false belief", "question", "dismantle",
                "expose", "uncomfortable truth", "break down", "myth",
            ],
            SeasonMandate.THE_FORGE: [
                "action", "discipline", "hard", "forge",
                "build", "execute", "commit", "grind", "work",
            ],
            SeasonMandate.THE_MIRROR: [
                "introspect", "reflect", "story", "mirror",
                "look within", "journal", "remember", "self",
            ],
            SeasonMandate.THE_TRIBE: [
                "community", "we", "together", "tribe",
                "collective", "share", "belong", "us",
            ],
        }

        def _has_keyword(kw: str, txt: str) -> bool:
            """Word-boundary match to prevent 'we' matching 'were', etc."""
            return bool(re.search(r"\b" + re.escape(kw) + r"\b", txt))

        # Check for the ACTIVE season's keywords
        active_keywords = season_keywords.get(season, [])
        active_hits = sum(1 for kw in active_keywords if _has_keyword(kw, text_lower))
        active_coverage = active_hits / max(len(active_keywords), 1)

        # Check for WRONG season keywords (violation)
        wrong_season_hits = 0
        for other_season, keywords in season_keywords.items():
            if other_season != season:
                wrong_season_hits += sum(1 for kw in keywords if _has_keyword(kw, text_lower))

        # Compliance: high active coverage + low wrong-season contamination
        contamination_penalty = min(wrong_season_hits * 0.1, 0.5)
        compliance = min(1.0, max(0.0, active_coverage - contamination_penalty))

        return compliance

    def _generate_marcus_feedback(
        self,
        text: str,
        season: SeasonMandate,
    ) -> str:
        """Generate Marcus's structural rewrite constraints."""
        season_instructions: dict[SeasonMandate, str] = {
            SeasonMandate.DECONSTRUCTION: (
                "Must challenge false beliefs. Convert generic advice into "
                "provocative deconstruction of the audience's assumptions."
            ),
            SeasonMandate.THE_FORGE: (
                "Must require hard actionable steps. Convert the generic advice list "
                "into an actionable 'Forge' discipline set."
            ),
            SeasonMandate.THE_MIRROR: (
                "Must focus on introspective storytelling. Convert the advice-heavy "
                "structure into deep, reflective narrative."
            ),
            SeasonMandate.THE_TRIBE: (
                "Must focus on community and 'We' language. Replace individual-focused "
                "rhetoric with collective belonging narrative."
            ),
        }
        return season_instructions.get(
            season,
            f"Script does not comply with the active {season.value} season mandate.",
        )

    def _detect_symmetrical_transitions(self, text: str) -> list[str]:
        """Detect symmetrical transition sentences (template bleed)."""
        tells: list[str] = []
        sentences = [s.strip() for s in text.split(".") if s.strip()]

        for i in range(len(sentences) - 1):
            s1_words = len(sentences[i].split())
            s2_words = len(sentences[i + 1].split())
            if s1_words > 5 and s2_words > 5:
                if abs(s1_words - s2_words) <= 1:
                    tells.append(
                        f"Symmetrical transition: sentences {i+1}-{i+2} "
                        f"({s1_words} vs {s2_words} words)"
                    )

        return tells[:3]  # Cap at 3

    def _detect_paragraph_balance(self, text: str) -> Optional[str]:
        """Detect unnaturally balanced paragraph lengths."""
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        if len(paragraphs) < 3:
            return None

        lengths = [len(p.split()) for p in paragraphs]
        avg_len = sum(lengths) / len(lengths)
        if avg_len == 0:
            return None

        # Check if all paragraphs are suspiciously similar in length
        max_deviation = max(abs(l - avg_len) / avg_len for l in lengths)
        if max_deviation < 0.1 and len(paragraphs) >= 4:
            return f"Unnaturally balanced paragraphs: all within 10% of {avg_len:.0f} words"

        return None
