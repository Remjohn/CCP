"""
CCP Step 8 — CRAL Moment Executors M1-M7 (Unit 4)
Implements FR14 §Stage 3: The 7 Moment Executor Skills.

Architecture reference:
    FR14_CRAL_Research_Subsystem_Tech_Spec.md §Stage 3
    CRAL_Documentation_V1 — Diagonal Research Method (Bruner 1960)
    Hasson 2010 — Human Evidence Bias / Neural Coupling

Each moment executor:
    - Is a passive Skill (no loop reasoning).
    - Receives a compiled directive from the Research Planner.
    - Produces a finding constrained to ≤240 words (signal contract).
    - Runs through a moment-specific quality gate.

FR14 AC3: M4 celebrity rejection (is_celebrity → FAIL).
FR14 AC4: 240-word signal contract (>240 words → length exception).
M-02: No hardcoded TTT values.
ADR-01: coach_id scopes all operations.
"""

from __future__ import annotations

import hashlib
import logging
from typing import TYPE_CHECKING, Any, Optional

from src.ccp.models.adapter_registry_v2_models import (
    CRALFinding,
    CRALMomentKey,
)
from src.ccp.models.cral_research_models import (
    MOMENT_CONFIGS,
    EmotionalRegister,
    HumanEvidenceTarget,
    MomentConfig,
    MomentQualityGateResult,
    ResearchPlannerDirective,
    SourceDiscipline,
)

if TYPE_CHECKING:
    from src.ccp.core.receipt_chain import ReceiptChain

logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════
# Constants
# ══════════════════════════════════════════════════════════════

MAX_FINDING_WORDS = 240
MAX_EXECUTOR_RETRIES = 3
STAGE_NAME = "STAGE-3-MOMENT-EXECUTOR"
AGENT_NAME = "Research-Orchestrator"


# ══════════════════════════════════════════════════════════════
# Quality Gate Validators
# ══════════════════════════════════════════════════════════════

def _check_word_count(finding_text: str) -> tuple[int, bool]:
    """Check finding word count against the 240-word signal contract.

    FR14 AC4: Any finding >240 words trips a length limit exception.

    Returns:
        (word_count, exceeded) tuple.
    """
    word_count = len(finding_text.split())
    return word_count, word_count > MAX_FINDING_WORDS


def _check_human_evidence(finding_text: str) -> bool:
    """Check if finding contains human evidence indicators.

    Hasson 2010: Neural coupling requires named human subjects.
    Heuristic: at least one capitalized proper noun pattern.
    """
    words = finding_text.split()
    # Simple heuristic: look for consecutive capitalized words
    # (proper nouns / named entities)
    for i in range(len(words) - 1):
        if (
            words[i][0:1].isupper()
            and words[i + 1][0:1].isupper()
            and not words[i].endswith(".")
            and len(words[i]) > 1
        ):
            return True
    # Single capitalized word not at sentence start
    for i in range(1, len(words)):
        if words[i][0:1].isupper() and len(words[i]) > 2:
            prev = words[i - 1]
            if not prev.endswith((".", "!", "?")):
                return True
    return False


def _check_celebrity(finding_text: str, is_celebrity: bool = False) -> bool:
    """Check if finding references a celebrity entity.

    FR14 AC3: M4 celebrity rejection. If is_celebrity == true,
    the quality gate returns FAIL and mandates regeneration
    targeting a local/vernacular entity.

    Returns:
        True if celebrity detected (FAIL condition for M4).
    """
    return is_celebrity


def _check_source_recency(finding_text: str, metadata: dict[str, Any]) -> bool:
    """M1-specific: Source must be < 4 weeks old.

    FR14 §Stage 3 M1: "Quality Gate: Source must be < 4 weeks old
    community discourse."

    Returns:
        True if recency gate passes.
    """
    source_age_days = metadata.get("source_age_days", 0)
    return source_age_days <= 28  # 4 weeks


def _check_narrative_elements(
    finding_text: str, metadata: dict[str, Any],
) -> bool:
    """M4-specific: Must contain 5 narrative elements.

    FR14 §Stage 3 M4: protagonist, status, contact moment, shift, outcome.

    Returns:
        True if all 5 elements present.
    """
    elements = metadata.get("narrative_elements", {})
    required = {"protagonist", "status", "contact_moment", "shift", "outcome"}
    return required.issubset(set(elements.keys()))


def _check_prediction_contradiction(
    finding_text: str, metadata: dict[str, Any],
) -> bool:
    """M5-specific: Must contradict M3 prediction gap.

    FR14 §Stage 3 M5: "Must explicitly contradict the M3 prediction gap
    within optimal incongruity limits (Loewenstein 1994)."

    Returns:
        True if contradiction is present.
    """
    return metadata.get("contradicts_m3_prediction", False)


def _check_internal_source(
    finding_text: str, metadata: dict[str, Any],
) -> bool:
    """M6-specific: Evidence must originate internally.

    FR14 §Stage 3 M6: "Evidence must originate internally from the
    mechanism's creator/institution."

    Returns:
        True if source is internal/institutional.
    """
    return metadata.get("source_is_internal", False)


def _check_vernacular(
    finding_text: str, metadata: dict[str, Any],
) -> bool:
    """M7-specific: Must contain verified vernacular extraction.

    FR14 §Stage 3 M7: "Must contain verified vernacular extraction
    (slang/cultural syntax native to tribe)."

    Returns:
        True if vernacular is present.
    """
    return metadata.get("vernacular_present", False)


# ══════════════════════════════════════════════════════════════
# Per-Moment Quality Gate Dispatch
# ══════════════════════════════════════════════════════════════

def evaluate_quality_gate(
    moment_key: CRALMomentKey,
    finding_text: str,
    metadata: Optional[dict[str, Any]] = None,
) -> MomentQualityGateResult:
    """Evaluate the moment-specific quality gate.

    Each moment has a distinct gate (FR14 §Stage 3).

    Args:
        moment_key: Which moment to evaluate.
        finding_text: The finding text produced by the executor.
        metadata: Additional metadata for gate-specific checks.

    Returns:
        MomentQualityGateResult with verdict.
    """
    if metadata is None:
        metadata = {}

    word_count, word_limit_exceeded = _check_word_count(finding_text)
    human_evidence_present = _check_human_evidence(finding_text)
    celebrity_detected = _check_celebrity(
        finding_text, metadata.get("is_celebrity", False),
    )

    # Start with base checks
    result = MomentQualityGateResult(
        moment_key=moment_key,
        word_count=word_count,
        word_limit_exceeded=word_limit_exceeded,
        human_evidence_present=human_evidence_present,
        celebrity_detected=celebrity_detected,
    )

    # FR14 AC4: Word limit is a hard fail
    if word_limit_exceeded:
        result.verdict = "FAIL"
        result.quality_gate_details = (
            f"Word limit exceeded: {word_count}/{MAX_FINDING_WORDS}. "
            "240-word signal contract violation."
        )
        return result

    # FR14 AC3: Celebrity rejection (M4 specific)
    if moment_key == CRALMomentKey.M4_RESONANT and celebrity_detected:
        result.verdict = "FAIL"
        result.quality_gate_details = (
            "Celebrity entity detected in M4 RESONANT finding. "
            "Human Evidence Bias requires local/vernacular entity. "
            "Regeneration mandated."
        )
        return result

    # Human evidence is required for all moments
    if not human_evidence_present:
        result.verdict = "PROVISIONAL"
        result.quality_gate_details = (
            "No named human evidence detected. "
            "Neural coupling (Hasson 2010) requires named humans."
        )

    # Moment-specific gates
    moment_gate_pass = True
    gate_detail = ""

    if moment_key == CRALMomentKey.M1_TIMELY:
        if not _check_source_recency(finding_text, metadata):
            moment_gate_pass = False
            gate_detail = "M1 source recency gate failed: source > 4 weeks old."

    elif moment_key == CRALMomentKey.M4_RESONANT:
        if not _check_narrative_elements(finding_text, metadata):
            moment_gate_pass = False
            gate_detail = (
                "M4 narrative structure gate failed: missing required elements "
                "(protagonist, status, contact_moment, shift, outcome)."
            )

    elif moment_key == CRALMomentKey.M5_SURPRISING:
        if not _check_prediction_contradiction(finding_text, metadata):
            moment_gate_pass = False
            gate_detail = (
                "M5 prediction contradiction gate failed: finding does not "
                "contradict the M3 prediction gap."
            )

    elif moment_key == CRALMomentKey.M6_IRREFUTABLE:
        if not _check_internal_source(finding_text, metadata):
            moment_gate_pass = False
            gate_detail = (
                "M6 internal source gate failed: evidence does not originate "
                "from the mechanism's creator/institution."
            )

    elif moment_key == CRALMomentKey.M7_RELATABLE:
        if not _check_vernacular(finding_text, metadata):
            moment_gate_pass = False
            gate_detail = (
                "M7 vernacular gate failed: no verified slang/cultural syntax "
                "native to tribe detected."
            )

    if not moment_gate_pass:
        result.verdict = "FAIL"
        result.quality_gate_details = gate_detail
        return result

    # All gates passed
    if result.verdict != "PROVISIONAL":
        result.verdict = "PASS"
        result.quality_gate_details = (
            f"All quality gates passed for {moment_key.value}. "
            f"Word count: {word_count}/{MAX_FINDING_WORDS}."
        )

    return result


# ══════════════════════════════════════════════════════════════
# Moment Executor
# ══════════════════════════════════════════════════════════════

class MomentExecutor:
    """Executes a single CRAL research moment.

    FR14 §Stage 3: Each Moment executor is a passive Skill governed
    by a strict 240-word signal contract. It receives a compiled
    directive and produces a finding.

    In a production environment, execute() would invoke an LLM API
    with the directive. In this structural implementation, we validate
    the finding against quality gates and produce the CRALFinding
    output model.

    Usage:
        executor = MomentExecutor(coach_id="coach_88ab")
        finding, gate = executor.execute(
            moment_key=CRALMomentKey.M3_UNDENIABLE,
            directive=planner_directive,
            finding_text="Research finding...",
            metadata={"researcher_name": "Kahneman"},
        )
    """

    def __init__(
        self,
        coach_id: str,
        receipt_chain: Optional[ReceiptChain] = None,
    ):
        self.coach_id = coach_id
        self.receipt_chain = receipt_chain

    def execute(
        self,
        moment_key: CRALMomentKey,
        directive: ResearchPlannerDirective,
        finding_text: str,
        metadata: Optional[dict[str, Any]] = None,
    ) -> tuple[Optional[CRALFinding], MomentQualityGateResult]:
        """Execute a moment and evaluate its quality gate.

        Args:
            moment_key: Which moment to execute.
            directive: The compiled research directive.
            finding_text: The finding text (from LLM or test fixture).
            metadata: Additional metadata for quality gate checks.

        Returns:
            (CRALFinding | None, MomentQualityGateResult) tuple.
            Finding is None if quality gate FAILs.
        """
        if metadata is None:
            metadata = {}

        config = MOMENT_CONFIGS.get(moment_key)
        if config is None:
            logger.error("No MomentConfig for %s", moment_key.value)
            gate = MomentQualityGateResult(
                moment_key=moment_key,
                verdict="FAIL",
                quality_gate_details=f"No configuration found for {moment_key.value}.",
            )
            return None, gate

        # Evaluate quality gate
        gate = evaluate_quality_gate(moment_key, finding_text, metadata)

        logger.info(
            "Moment %s quality gate: %s (words=%d)",
            moment_key.value,
            gate.verdict,
            gate.word_count,
        )

        # Write receipt
        self._write_receipt(moment_key, directive, gate)

        if gate.verdict == "FAIL":
            return None, gate

        # Build CRALFinding
        finding = CRALFinding(
            moment_key=moment_key,
            finding_text=finding_text,
            source_quality="verified" if gate.verdict == "PASS" else "partial",
            human_evidence_count=1 if gate.human_evidence_present else 0,
        )

        return finding, gate

    def execute_with_retry(
        self,
        moment_key: CRALMomentKey,
        directive: ResearchPlannerDirective,
        finding_texts: list[str],
        metadata_list: Optional[list[dict[str, Any]]] = None,
    ) -> tuple[Optional[CRALFinding], MomentQualityGateResult]:
        """Execute a moment with retry on FAIL.

        Accepts a list of finding_texts for sequential retry attempts.
        In production, each retry would re-invoke the LLM with a
        modified prompt.

        Args:
            moment_key: Which moment to execute.
            directive: The compiled research directive.
            finding_texts: List of finding texts (one per attempt).
            metadata_list: Optional list of metadata dicts per attempt.

        Returns:
            Best result achieved within retry limit.
        """
        if metadata_list is None:
            metadata_list = [{}] * len(finding_texts)

        best_finding: Optional[CRALFinding] = None
        best_gate = MomentQualityGateResult(
            moment_key=moment_key,
            verdict="FAIL",
            quality_gate_details="No attempts executed.",
        )

        for i, finding_text in enumerate(finding_texts[:MAX_EXECUTOR_RETRIES]):
            meta = metadata_list[i] if i < len(metadata_list) else {}
            finding, gate = self.execute(
                moment_key, directive, finding_text, meta,
            )
            gate.retry_count = i

            if gate.verdict in ("PASS", "PROVISIONAL"):
                return finding, gate

            best_gate = gate
            logger.warning(
                "Moment %s attempt %d/%d: %s",
                moment_key.value,
                i + 1,
                MAX_EXECUTOR_RETRIES,
                gate.verdict,
            )

        logger.error(
            "Moment %s exhausted %d retries. Final: FAIL.",
            moment_key.value,
            MAX_EXECUTOR_RETRIES,
        )
        return best_finding, best_gate

    def _write_receipt(
        self,
        moment_key: CRALMomentKey,
        directive: ResearchPlannerDirective,
        gate: MomentQualityGateResult,
    ) -> None:
        """Write receipt chain entry for this moment execution.

        FR47 DEP-ENG-041: stage_name='STAGE-3-MOMENT-EXECUTOR'
        """
        if self.receipt_chain is None:
            return

        input_hash = hashlib.sha256(
            directive.directive_text.encode()
        ).hexdigest()[:16]

        output_hash = hashlib.sha256(
            f"{moment_key.value}_{gate.verdict}_{gate.word_count}".encode()
        ).hexdigest()[:16]

        self.receipt_chain.log(
            agent_id=AGENT_NAME,
            action=STAGE_NAME,
            asset_id=f"moment_{moment_key.value}",
            input_summary=f"directive_hash={input_hash}, moment={moment_key.value}",
            output_summary=(
                f"verdict={gate.verdict}, words={gate.word_count}, "
                f"output_hash={output_hash}"
            ),
            decision=gate.verdict,
            decision_rationale=gate.quality_gate_details,
            metadata={
                "stage_name": STAGE_NAME,
                "moment_key": moment_key.value,
                "word_count": gate.word_count,
                "verdict": gate.verdict,
                "word_limit_exceeded": gate.word_limit_exceeded,
                "celebrity_detected": gate.celebrity_detected,
                "human_evidence_present": gate.human_evidence_present,
                "retry_count": gate.retry_count,
            },
        )
