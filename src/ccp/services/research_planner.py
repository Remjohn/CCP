"""
CCP Step 8 — Research Planner JIT Directive Compiler (Unit 3)
Implements FR14 §Stage 2: Research Planner Directive Generation.

Architecture reference:
    FR14_CRAL_Research_Subsystem_Tech_Spec.md §Stage 2
    CRAL_Documentation_V1 — Previous-Finding Exclusion Constraint

Responsibilities:
    1. Compile a 40-60 word directive for a target moment executor.
    2. Inject previous-finding exclusion constraints.
    3. Validate directive compliance (PASS / PROVISIONAL / FAIL).
    4. Retry up to 3 times on FAIL before aborting session.
    5. Write receipt chain at every directive generation.

FR14 AC1: System rejects directive < 40 words (e.g. 28-word example).
M-02: No hardcoded TTT values — directives are JIT-compiled from state.
ADR-01: coach_id scopes all operations.
"""

from __future__ import annotations

import hashlib
import logging
from typing import TYPE_CHECKING, Any, Optional

from src.ccp.models.adapter_registry_v2_models import CRALMomentKey
from src.ccp.models.cral_research_models import (
    MOMENT_CONFIGS,
    MomentConfig,
    MomentStatus,
    OODAState,
    PlannerDirectiveVerdict,
    ResearchPlannerDirective,
)

if TYPE_CHECKING:
    from src.ccp.core.receipt_chain import ReceiptChain

logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════
# Constants
# ══════════════════════════════════════════════════════════════

MAX_PLANNER_RETRIES = 3
STAGE_NAME = "STAGE-2-RESEARCH-PLANNER"
AGENT_NAME = "Research-Orchestrator"


# ══════════════════════════════════════════════════════════════
# Directive Template Builder
# ══════════════════════════════════════════════════════════════

def _build_exclusion_block(
    ooda_state: OODAState,
    target_moment: CRALMomentKey,
    prior_findings: dict[str, str],
) -> str:
    """Build the Previous-Finding Exclusion constraint text.

    FR14 Technical Decision 2: The Research Planner JIT compiler
    dynamically injects all *previous* moment findings into the
    constraint list, instructing the model to mathematically exclude
    overlapping data.

    Args:
        ooda_state: Current OODA loop state.
        target_moment: The moment we're generating a directive for.
        prior_findings: Keyed by CRALMomentKey value — the finding
                        content text from each already-completed moment.

    Returns:
        Exclusion constraint text (may be empty if no prior findings).
    """
    completed = []
    for mk in CRALMomentKey:
        if mk == target_moment:
            break
        state = ooda_state.moments.get(mk.value)
        if state and state.status == MomentStatus.PASS:
            finding_text = prior_findings.get(mk.value, "")
            if finding_text:
                completed.append(f"[{mk.value}]: {finding_text[:120]}")

    if not completed:
        return ""

    return (
        "DO NOT return findings repeating: "
        + "; ".join(completed)
        + "."
    )


def _build_directive_prompt(
    config: MomentConfig,
    theme: str,
    exclusion_block: str,
    archetype_context: str = "",
) -> str:
    """Build the raw directive text for a moment executor.

    This is the JIT compilation step. The output is a 40-60 word
    directive that the moment executor will use as its research brief.

    Args:
        config: MomentConfig for the target moment.
        theme: Content theme for the research session.
        exclusion_block: Previous-Finding Exclusion constraints.
        archetype_context: Optional archetype context for targeting.

    Returns:
        Compiled directive text string.
    """
    # Base directive components
    parts = [
        f"Research {config.source_discipline.value} for theme '{theme}'.",
        f"Target emotional register: {config.emotional_register.value}.",
        f"Find {config.human_evidence_target.value} evidence.",
        "human_evidence_required.",
        f"Quality gate: {config.quality_gate_description}.",
        "You must target high-quality, verified sources and focus on obtaining concrete facts.",
    ]

    if archetype_context:
        parts.append(f"Archetype context: {archetype_context}.")

    if exclusion_block:
        parts.append(exclusion_block)

    directive = " ".join(parts)

    # Trim to stay within 40-60 word range if possible
    words = directive.split()
    if len(words) > 65:
        directive = " ".join(words[:60])

    return directive


# ══════════════════════════════════════════════════════════════
# Research Planner
# ══════════════════════════════════════════════════════════════

class ResearchPlanner:
    """FR14 §Stage 2 — JIT Directive Compiler.

    Generates 40-60 word research directives for moment executors.
    Implements Previous-Finding Exclusion to prevent horizontal
    research collapse (Bruner 1960 / Diagonal Method).

    Usage:
        planner = ResearchPlanner(coach_id="coach_88ab")
        directive = planner.compile_directive(
            target_moment=CRALMomentKey.M3_UNDENIABLE,
            theme="algorithm taxation impact on creators",
            ooda_state=state,
            prior_findings={"M1_TIMELY": "...", "M2_BELIEVABLE": "..."},
        )
    """

    def __init__(
        self,
        coach_id: str,
        receipt_chain: Optional[ReceiptChain] = None,
    ):
        self.coach_id = coach_id
        self.receipt_chain = receipt_chain

    def compile_directive(
        self,
        target_moment: CRALMomentKey,
        theme: str,
        ooda_state: OODAState,
        prior_findings: Optional[dict[str, str]] = None,
        archetype_context: str = "",
    ) -> ResearchPlannerDirective:
        """Compile a research directive for a target moment.

        FR14 §Stage 2 Logic Gate:
            PASS: 40-60 words + contains human_evidence_required
            PROVISIONAL: 61-65 words + contains human_evidence_required
            FAIL: < 40 words OR > 65 words OR lacks human_evidence_required

        Args:
            target_moment: The moment to generate a directive for.
            theme: Content theme.
            ooda_state: Current OODA state.
            prior_findings: Keyed by CRALMomentKey value.
            archetype_context: Optional archetype targeting.

        Returns:
            Validated ResearchPlannerDirective with verdict.
        """
        config = MOMENT_CONFIGS.get(target_moment)
        if config is None:
            logger.error(
                "No MomentConfig found for %s", target_moment.value,
            )
            return ResearchPlannerDirective(
                moment_key=target_moment,
                directive_text="",
                verdict=PlannerDirectiveVerdict.FAIL,
            )

        if prior_findings is None:
            prior_findings = {}

        # Build exclusion block from prior findings
        exclusion_block = _build_exclusion_block(
            ooda_state, target_moment, prior_findings,
        )

        # Build directive text
        directive_text = _build_directive_prompt(
            config=config,
            theme=theme,
            exclusion_block=exclusion_block,
            archetype_context=archetype_context,
        )

        # Track which findings were excluded
        excluded_keys: list[CRALMomentKey] = []
        for mk in CRALMomentKey:
            if mk == target_moment:
                break
            state = ooda_state.moments.get(mk.value)
            if state and state.status == MomentStatus.PASS:
                if mk.value in prior_findings:
                    excluded_keys.append(mk)

        # Create directive model
        directive = ResearchPlannerDirective(
            moment_key=target_moment,
            directive_text=directive_text,
            previous_findings_excluded=excluded_keys,
        )

        # Validate
        verdict = directive.validate_directive()

        logger.info(
            "Planner directive for %s: %d words, verdict=%s",
            target_moment.value,
            directive.word_count,
            verdict.value,
        )

        # Write receipt
        self._write_receipt(directive)

        return directive

    def compile_directive_with_retry(
        self,
        target_moment: CRALMomentKey,
        theme: str,
        ooda_state: OODAState,
        prior_findings: Optional[dict[str, str]] = None,
        archetype_context: str = "",
    ) -> ResearchPlannerDirective:
        """Compile a directive with automatic retry on FAIL.

        FR14 AC1: Rejects < 40 words. Retries up to 3 times.
        After 3 FAILs, returns the last FAIL directive for
        the orchestrator to handle.

        Returns:
            The best directive achieved within retry limit.
        """
        best_directive: Optional[ResearchPlannerDirective] = None

        for attempt in range(MAX_PLANNER_RETRIES):
            # On retry, extend the archetype context to push word count up
            retry_context = archetype_context
            if attempt > 0:
                retry_context = (
                    f"{archetype_context} "
                    f"Expand research scope to include adjacent evidence domains. "
                    f"Attempt {attempt + 1} of {MAX_PLANNER_RETRIES}."
                )

            directive = self.compile_directive(
                target_moment=target_moment,
                theme=theme,
                ooda_state=ooda_state,
                prior_findings=prior_findings,
                archetype_context=retry_context,
            )

            if directive.verdict in (
                PlannerDirectiveVerdict.PASS,
                PlannerDirectiveVerdict.PROVISIONAL,
            ):
                return directive

            best_directive = directive
            logger.warning(
                "Planner directive FAIL for %s (attempt %d/%d): %d words",
                target_moment.value,
                attempt + 1,
                MAX_PLANNER_RETRIES,
                directive.word_count,
            )

        # All retries exhausted — return last FAIL
        assert best_directive is not None
        logger.error(
            "Planner exhausted %d retries for %s. Final verdict: FAIL.",
            MAX_PLANNER_RETRIES,
            target_moment.value,
        )
        return best_directive

    def _write_receipt(self, directive: ResearchPlannerDirective) -> None:
        """Write receipt chain entry for this directive generation.

        FR47 DEP-ENG-041: stage_name='STAGE-2-RESEARCH-PLANNER'
        """
        if self.receipt_chain is None:
            return

        input_hash = hashlib.sha256(
            directive.moment_key.value.encode()
        ).hexdigest()[:16]

        output_hash = hashlib.sha256(
            directive.directive_text.encode()
        ).hexdigest()[:16]

        self.receipt_chain.log(
            agent_id=AGENT_NAME,
            action=STAGE_NAME,
            asset_id=f"directive_{directive.moment_key.value}",
            input_summary=f"moment={directive.moment_key.value}, input_hash={input_hash}",
            output_summary=(
                f"verdict={directive.verdict.value}, "
                f"words={directive.word_count}, "
                f"output_hash={output_hash}"
            ),
            decision=directive.verdict.value,
            decision_rationale=(
                f"Word count: {directive.word_count}. "
                f"Human evidence constraint: {directive.contains_human_evidence_constraint}."
            ),
            metadata={
                "stage_name": STAGE_NAME,
                "moment_key": directive.moment_key.value,
                "word_count": directive.word_count,
                "verdict": directive.verdict.value,
                "verbosity_warning": directive.verbosity_warning,
                "exclusions": [mk.value for mk in directive.previous_findings_excluded],
            },
        )
