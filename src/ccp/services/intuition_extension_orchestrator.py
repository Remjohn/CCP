"""
CCP Intuition Extension Orchestrator — FR40 (DEP-ENG-035)

Spec: FR40_Intuition_Extensions_Tech_Spec.md
Produces: DEP-ENG-035_a through _d (4 reprompt injections)

§4 Stage 1: SoulResonance → The Resonance Seeker → soul_resonance_query.py
§4 Stage 2: PatternWeaver → The Connector → graph_disconnect_query.py
§4 Stage 3: GhostContext  → The Shadow Miner → ghost_context_scan.py
§4 Stage 4: AncestralWisdom → The Philosopher → framework_cross_reference.py

§6: Fallback — if Python tool fails, DamageControl catches; pipeline defaults
    to Standard Execution without the intuition spark.

§8: AC1 conditional firing, AC2 GhostContext dark truth, AC3 PatternWeaver
     disconnect, AC4 AncestralWisdom Flesch-Kincaid 8-10.

Receipt: FR47 DEP-ENG-041 per invocation.
ADR-01: coach_id + Tribe_ID scopes all queries.
"""

from __future__ import annotations

import re
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.intuition_extension_models import (
    ANCESTRAL_WISDOM_READABILITY_MAX,
    ANCESTRAL_WISDOM_READABILITY_MIN,
    EXTENSION_AGENT_MAP,
    EXTENSION_TOOL_MAP,
    METAPHOR_REUSE_THRESHOLD,
    FrameworkCrossReferenceToolResult,
    GhostContextToolResult,
    GovernanceTriggerEvaluation,
    GraphDisconnectToolResult,
    IntuitionAgentName,
    IntuitionBehaviorType,
    IntuitionExtensionName,
    IntuitionInjectionPayload,
    IntuitionTriggerCondition,
    MetaphorUsageEntry,
    PhilosophicalLens,
    SoulResonanceToolResult,
    TVRBalance,
)


class IntuitionExtensionOrchestrator:
    """Orchestrator for the 4 Intuition Extensions.

    FR40 §2: "Emergent Sparks" triggered contextually by the Governance Layer.
    They are NOT run on a rigid schedule — only when staleness, flatness,
    or information gaps are detected.

    §6 Fallback: If the Python tool fails, DamageControl catches. Pipeline
    defaults to Standard Execution without the intuition spark.

    ADR-01: coach_id + Tribe_ID scopes ALL tool queries.
    """

    def __init__(
        self,
        coach_id: str,
        receipt_chain: Optional[ReceiptChain] = None,
    ) -> None:
        if len(coach_id) != 3:
            raise ValueError(f"coach_id must be 3 characters, got '{coach_id}'")
        self.coach_id = coach_id.upper()
        self.receipt_chain = receipt_chain or ReceiptChain(
            coach_acronym=self.coach_id
        )
        self._run_counter = 0

    # ──────────────────────────────────────────────────────────────────────────
    # Governance Layer Trigger Evaluation
    # ──────────────────────────────────────────────────────────────────────────

    def evaluate_trigger(
        self,
        metaphor_reuse_count: int = 0,
        sentiment_positive_ratio: float = 0.0,
        tvr_balance: Optional[TVRBalance] = None,
        coach_echo_detected: bool = False,
    ) -> GovernanceTriggerEvaluation:
        """§8 AC1: Evaluate whether an intuition extension should fire.

        5 unique scripts → no fire. Stale metaphor 3+ → PatternWeaver fires.
        """
        evaluation = GovernanceTriggerEvaluation(
            coach_id=self.coach_id,
            metaphor_reuse_count=metaphor_reuse_count,
            sentiment_positive_ratio=sentiment_positive_ratio,
            tvr_balance=tvr_balance,
            coach_echo_detected=coach_echo_detected,
        )

        self.receipt_chain.log(
            agent_id="Intuition-Orchestrator",
            action="governance-trigger-evaluation",
            input_summary=(
                f"metaphor_reuse={metaphor_reuse_count}, "
                f"positive_ratio={sentiment_positive_ratio:.2f}, "
                f"echo_detected={coach_echo_detected}"
            ),
            output_summary=(
                f"should_fire={evaluation.should_fire}, "
                f"target={evaluation.target_extension}"
            ),
            decision="FIRE" if evaluation.should_fire else "NO_FIRE",
            decision_rationale=evaluation.evidence or "All signals within normal range",
            metadata={"stage_name": "STAGE-GOVERNANCE-EVAL"},
        )

        return evaluation

    # ──────────────────────────────────────────────────────────────────────────
    # SoulResonance (§4 Stage 1)
    # ──────────────────────────────────────────────────────────────────────────

    def run_soul_resonance(
        self,
        draft_text: str,
        tool_result: SoulResonanceToolResult,
        behavior: IntuitionBehaviorType = IntuitionBehaviorType.VIBE_PASS_REWRITE,
    ) -> IntuitionInjectionPayload:
        """§4 Stage 1: SoulResonance — The Vibe Checker.

        Demands visceral, emotionally contrasting analogy from Sacred Audio.
        """
        self._run_counter += 1
        run_id = f"INT-{self._run_counter:04d}"

        directive = self._build_soul_resonance_directive(
            tool_result, behavior, draft_text
        )

        payload = IntuitionInjectionPayload(
            intuition_run_id=run_id,
            triggering_condition=IntuitionTriggerCondition.TVR_IMBALANCE.value,
            extension_fired=IntuitionExtensionName.SOUL_RESONANCE.value,
            sub_agent_deployed=IntuitionAgentName.RESONANCE_SEEKER.value,
            tool_invoked=EXTENSION_TOOL_MAP[IntuitionExtensionName.SOUL_RESONANCE],
            injection_payload={
                "directive": behavior.value,
                "constraint_added": directive,
            },
            coach_id=self.coach_id,
        )

        self.receipt_chain.log(
            agent_id="Intuition-SoulResonance",
            action="soul-resonance-injection",
            input_summary=f"draft_len={len(draft_text)}, behavior={behavior.value}",
            output_summary=f"run_id={run_id}, directive_len={len(directive)}",
            decision="INJECTION_APPLIED",
            metadata={"stage_name": "STAGE-INTUITION-SOUL-RESONANCE"},
        )

        return payload

    # ──────────────────────────────────────────────────────────────────────────
    # PatternWeaver (§4 Stage 2)
    # ──────────────────────────────────────────────────────────────────────────

    def run_pattern_weaver(
        self,
        draft_text: str,
        tool_result: GraphDisconnectToolResult,
        behavior: IntuitionBehaviorType = IntuitionBehaviorType.CROSS_DOMAIN_SYNTHESIS,
    ) -> IntuitionInjectionPayload:
        """§4 Stage 2: PatternWeaver — The Synthesizer.

        §8 AC3: Forces connection between primary topic and farthest graph node.
        """
        self._run_counter += 1
        run_id = f"INT-{self._run_counter:04d}"

        directive = self._build_pattern_weaver_directive(
            tool_result, behavior
        )

        payload = IntuitionInjectionPayload(
            intuition_run_id=run_id,
            triggering_condition=IntuitionTriggerCondition.STALENESS_METAPHOR_REUSED.value,
            extension_fired=IntuitionExtensionName.PATTERN_WEAVER.value,
            sub_agent_deployed=IntuitionAgentName.CONNECTOR.value,
            tool_invoked=EXTENSION_TOOL_MAP[IntuitionExtensionName.PATTERN_WEAVER],
            injection_payload={
                "directive": behavior.value,
                "constraint_added": directive,
            },
            coach_id=self.coach_id,
        )

        self.receipt_chain.log(
            agent_id="Intuition-PatternWeaver",
            action="pattern-weaver-injection",
            input_summary=(
                f"source_topic={tool_result.source_topic}, "
                f"farthest_node={tool_result.farthest_node}"
            ),
            output_summary=f"run_id={run_id}, behavior={behavior.value}",
            decision="INJECTION_APPLIED",
            metadata={"stage_name": "STAGE-INTUITION-PATTERN-WEAVER"},
        )

        return payload

    # ──────────────────────────────────────────────────────────────────────────
    # GhostContext (§4 Stage 3)
    # ──────────────────────────────────────────────────────────────────────────

    def run_ghost_context(
        self,
        draft_text: str,
        tool_result: GhostContextToolResult,
        behavior: IntuitionBehaviorType = IntuitionBehaviorType.INDUSTRY_DARK_TRUTH_INJECTION,
    ) -> IntuitionInjectionPayload:
        """§4 Stage 3: GhostContext — The Shadow Miner.

        §8 AC2: Injected prompt MUST contain directive addressing 'industry dark truth'.
        """
        self._run_counter += 1
        run_id = f"INT-{self._run_counter:04d}"

        # §8 AC2: dark_truth_directive MUST be non-empty
        if not tool_result.dark_truth_directive:
            raise ValueError(
                "GhostContext tool must provide a non-empty dark_truth_directive. "
                "§8 AC2: 'The Shadow Miner simply tells the writer to be more cynical "
                "without providing concrete, sourced data' is a failure."
            )

        directive = self._build_ghost_context_directive(tool_result, behavior)

        payload = IntuitionInjectionPayload(
            intuition_run_id=run_id,
            triggering_condition=IntuitionTriggerCondition.POSITIVE_ONLY_SENTIMENT.value,
            extension_fired=IntuitionExtensionName.GHOST_CONTEXT.value,
            sub_agent_deployed=IntuitionAgentName.SHADOW_MINER.value,
            tool_invoked=EXTENSION_TOOL_MAP[IntuitionExtensionName.GHOST_CONTEXT],
            injection_payload={
                "directive": behavior.value,
                "constraint_added": directive,
            },
            coach_id=self.coach_id,
        )

        self.receipt_chain.log(
            agent_id="Intuition-GhostContext",
            action="ghost-context-injection",
            input_summary=f"draft_len={len(draft_text)}, behavior={behavior.value}",
            output_summary=(
                f"run_id={run_id}, "
                f"dark_truth_len={len(tool_result.dark_truth_directive)}"
            ),
            decision="INJECTION_APPLIED",
            metadata={"stage_name": "STAGE-INTUITION-GHOST-CONTEXT"},
        )

        return payload

    # ──────────────────────────────────────────────────────────────────────────
    # AncestralWisdom (§4 Stage 4)
    # ──────────────────────────────────────────────────────────────────────────

    def run_ancestral_wisdom(
        self,
        draft_text: str,
        tool_result: FrameworkCrossReferenceToolResult,
        behavior: IntuitionBehaviorType = IntuitionBehaviorType.PHILOSOPHICAL_LENS_ROTATION,
    ) -> IntuitionInjectionPayload:
        """§4 Stage 4: AncestralWisdom — The Philosopher.

        §8 AC4: Flesch-Kincaid Grade 8-10 required — reject if outside range.
        """
        self._run_counter += 1
        run_id = f"INT-{self._run_counter:04d}"

        # §8 AC4: Readability compliance check
        if not tool_result.readability_compliant:
            raise ValueError(
                f"AncestralWisdom output Flesch-Kincaid Grade "
                f"{tool_result.flesch_kincaid_grade} is outside the required "
                f"Grade {ANCESTRAL_WISDOM_READABILITY_MIN}-"
                f"{ANCESTRAL_WISDOM_READABILITY_MAX} range. "
                f"§8 AC4 Failure: 'reads like a 19th-century academic thesis.'"
            )

        directive = self._build_ancestral_wisdom_directive(tool_result, behavior)

        payload = IntuitionInjectionPayload(
            intuition_run_id=run_id,
            triggering_condition=IntuitionTriggerCondition.COACH_ECHO_FAILURE.value,
            extension_fired=IntuitionExtensionName.ANCESTRAL_WISDOM.value,
            sub_agent_deployed=IntuitionAgentName.PHILOSOPHER.value,
            tool_invoked=EXTENSION_TOOL_MAP[IntuitionExtensionName.ANCESTRAL_WISDOM],
            injection_payload={
                "directive": behavior.value,
                "constraint_added": directive,
            },
            coach_id=self.coach_id,
        )

        self.receipt_chain.log(
            agent_id="Intuition-AncestralWisdom",
            action="ancestral-wisdom-injection",
            input_summary=(
                f"lens={tool_result.philosophical_lens}, "
                f"fk_grade={tool_result.flesch_kincaid_grade}"
            ),
            output_summary=f"run_id={run_id}, behavior={behavior.value}",
            decision="INJECTION_APPLIED",
            metadata={"stage_name": "STAGE-INTUITION-ANCESTRAL-WISDOM"},
        )

        return payload

    # ──────────────────────────────────────────────────────────────────────────
    # Full Orchestration Run
    # ──────────────────────────────────────────────────────────────────────────

    def run_if_triggered(
        self,
        draft_text: str,
        evaluation: GovernanceTriggerEvaluation,
        tool_result: Any = None,
    ) -> Optional[IntuitionInjectionPayload]:
        """Run the appropriate intuition extension if the trigger fired.

        §8 AC1: Returns None if no trigger — no extension fires.
        """
        if not evaluation.should_fire or evaluation.target_extension is None:
            return None

        ext = evaluation.target_extension

        if ext == IntuitionExtensionName.SOUL_RESONANCE:
            if not isinstance(tool_result, SoulResonanceToolResult):
                return None
            return self.run_soul_resonance(draft_text, tool_result)

        if ext == IntuitionExtensionName.PATTERN_WEAVER:
            if not isinstance(tool_result, GraphDisconnectToolResult):
                return None
            return self.run_pattern_weaver(draft_text, tool_result)

        if ext == IntuitionExtensionName.GHOST_CONTEXT:
            if not isinstance(tool_result, GhostContextToolResult):
                return None
            return self.run_ghost_context(draft_text, tool_result)

        if ext == IntuitionExtensionName.ANCESTRAL_WISDOM:
            if not isinstance(tool_result, FrameworkCrossReferenceToolResult):
                return None
            return self.run_ancestral_wisdom(draft_text, tool_result)

        return None

    # ──────────────────────────────────────────────────────────────────────────
    # Directive Builders
    # ──────────────────────────────────────────────────────────────────────────

    @staticmethod
    def _build_soul_resonance_directive(
        result: SoulResonanceToolResult,
        behavior: IntuitionBehaviorType,
        draft_text: str,
    ) -> str:
        """Build the SoulResonance injection directive."""
        parts: list[str] = []

        if behavior == IntuitionBehaviorType.VIBE_PASS_REWRITE:
            nodes = ", ".join(result.emotional_nodes_found[:3])
            parts.append(
                f"Rewrite using a visceral, emotionally contrasting analogy "
                f"drawn from the coach's Sacred Audio. Emotional anchors: [{nodes}]."
            )
        elif behavior == IntuitionBehaviorType.EMOTIONAL_POLARITY_INJECTION:
            if result.polarity_imbalance:
                parts.append(result.polarity_imbalance)
            else:
                parts.append(
                    "Inject dimensional contrast: if purely Analytical, "
                    "add Dark Humor or Vulnerability."
                )
        elif behavior == IntuitionBehaviorType.TRIBE_MIRROR_CHECK:
            match = "MATCH" if result.emotional_register_match else "MISMATCH"
            parts.append(
                f"Tribe Mirror: Emotional register {match} with Real Time Tribe Relevance."
            )
        elif behavior == IntuitionBehaviorType.SACRED_MOMENT_SURFACING:
            if result.sacred_moment:
                parts.append(
                    f"Surface sacred moment as narrative anchor: '{result.sacred_moment}'"
                )

        return " ".join(parts) if parts else "Apply emotional resonance enhancement."

    @staticmethod
    def _build_pattern_weaver_directive(
        result: GraphDisconnectToolResult,
        behavior: IntuitionBehaviorType,
    ) -> str:
        """Build the PatternWeaver injection directive."""
        if behavior == IntuitionBehaviorType.CROSS_DOMAIN_SYNTHESIS:
            return (
                f"You must link the concept of '{result.source_topic}' to "
                f"'{result.farthest_node}'. "
                f"Do not use any obvious metaphors. "
                f"Topological distance: {result.topological_distance} edges."
            )
        elif behavior == IntuitionBehaviorType.CONTRADICTION_MINING:
            return (
                f"Surface an honest contradiction in the coach's philosophy about "
                f"'{result.source_topic}' — build the post around the paradox."
            )
        elif behavior == IntuitionBehaviorType.ADJACENT_INDUSTRY_TRANSPLANT:
            return (
                f"Graft the framework from '{result.farthest_node}' onto "
                f"'{result.source_topic}'. The audience must feel the foreign "
                f"industry structure applied to their world."
            )
        elif behavior == IntuitionBehaviorType.TEMPORAL_PATTERN_DETECTION:
            return (
                f"Inject a 'Then vs. Now' tension about '{result.source_topic}' "
                f"using early-career vs. current-day coach data."
            )
        return result.synthesis_directive or "Apply cross-domain pattern synthesis."

    @staticmethod
    def _build_ghost_context_directive(
        result: GhostContextToolResult,
        behavior: IntuitionBehaviorType,
    ) -> str:
        """Build the GhostContext injection directive."""
        if behavior == IntuitionBehaviorType.INDUSTRY_DARK_TRUTH_INJECTION:
            return (
                f"INDUSTRY DARK TRUTH: {result.dark_truth_directive} "
                f"Do not soften this. State it plainly."
            )
        elif behavior == IntuitionBehaviorType.AUDIENCE_FEAR_MAPPING:
            return (
                f"Name the objection the audience has but won't say: "
                f"'{result.audience_fear or 'unidentified L3 fear'}'"
            )
        elif behavior == IntuitionBehaviorType.HISTORICAL_FAILURE_PATTERN:
            return (
                f"Cautionary context: {result.historical_failure or 'no historical failure on record'}"
            )
        elif behavior == IntuitionBehaviorType.COUNTER_NARRATIVE_GENERATION:
            return (
                f"Disprove the mainstream consensus: "
                f"'{result.counter_narrative or 'unidentified consensus'}' "
                f"using the coach's data."
            )
        return result.dark_truth_directive

    @staticmethod
    def _build_ancestral_wisdom_directive(
        result: FrameworkCrossReferenceToolResult,
        behavior: IntuitionBehaviorType,
    ) -> str:
        """Build the AncestralWisdom injection directive."""
        if behavior == IntuitionBehaviorType.CMA_FRAMEWORK_REFRAMING:
            return (
                f"Cross-reference against CMA principle: "
                f"'{result.matched_principle or 'unidentified principle'}'. "
                f"Elevate advice to structural principle."
            )
        elif behavior == IntuitionBehaviorType.PHILOSOPHICAL_LENS_ROTATION:
            lens = result.philosophical_lens.value if result.philosophical_lens else "unspecified"
            return (
                f"Map this topic through the {lens} lens. "
                f"Alter the framing angle completely."
            )
        elif behavior == IntuitionBehaviorType.FIRST_PRINCIPLES_DECOMPOSITION:
            return (
                "Strip the surface claim to its atomic truth. "
                "Build upward from first principles."
            )
        elif behavior == IntuitionBehaviorType.LEGACY_PATTERN_RECOGNITION:
            return (
                f"Link to timeless wisdom: "
                f"'{result.legacy_pattern or 'What you describe is what ... called ...'}'"
            )
        return result.reframing_directive or "Apply philosophical reframing."
