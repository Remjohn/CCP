"""
CCP FR19 Semantic Affinity Guard Protocol — Guard Engine (Unit 2)
3-stage pipeline: INGEST → AFFINITY ANALYSIS → C-06 ENFORCE.

Spec reference: FR19_Semantic_Affinity_Guard_Tech_Spec.md §4 Implementation Plan

Gate C-06 rules (spec §3 Technical Decisions):
  Escape + HIGH    → FAIL_TERMINAL (mathematically impossible to compile)
  Escape + MEDIUM  → OPERATOR_REVIEW
  Escape + LOW     → PASS
  Processing + HIGH → PASS (faces pain directly — productive)
  Status/Discovery + HIGH/MEDIUM → PASS (tolerated contexts)
  Any mode + LOW   → PASS

Ghost Variable Prevention (spec §3):
  Any DEP-ID resolving to NULL/UNDEFINED → DAG_VIOLATION hard halt.

Fallback (spec §6):
  NLP crash → all Escape slots = PROVISIONAL_MEDIUM → Operator Queue.

Receipt writes per FR47 DEP-ENG-041:
  STAGE-1-SA-INGEST / Batch-Finalization-Core
  STAGE-2-AFFINITY-ANALYSIS / Semantic-Distance-Analyzer
  STAGE-3-ENFORCE / Batch-Finalization-Core
"""

import hashlib
import json
import re
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.semantic_affinity_models import (
    AFFINITY_THRESHOLD_HIGH,
    AFFINITY_THRESHOLD_MEDIUM,
    AffinityRating,
    BatchClearanceStatus,
    BatchMetadata,
    BatchSlot,
    C06Clearance,
    C06ResolutionPath,
    MoodMode,
    PainMapInput,
    PROVISIONAL_MEDIUM_WARNING,
    SemanticAffinityClearance,
    SlotEvaluation,
)


# ─── Exceptions ───────────────────────────────────────────────────────────────


class DAGViolationError(Exception):
    """Ghost Variable Prevention Gate — spec §3.

    Any field resolving to NULL or UNDEFINED triggers a hard compiler pipeline halt.
    """
    def __init__(self, missing_dep: str):
        self.missing_dep = missing_dep
        super().__init__(
            json.dumps({"error": "DAG_VIOLATION", "missing_dep": missing_dep})
        )


class C06TerminalError(Exception):
    """Spec §4 Stage 3: C-06 Terminal Error — Escape + HIGH affinity.

    Compilation is permanently halted. Operator must select a resolution path.
    """
    def __init__(
        self,
        slot_id: int,
        content_domain: str,
        pain_domain: str,
        affinity_score: float,
    ):
        self.slot_id = slot_id
        self.content_domain = content_domain
        self.pain_domain = pain_domain
        self.affinity_score = affinity_score
        super().__init__(
            f"C-06 TERMINAL: Escape slot {slot_id} has HIGH semantic affinity "
            f"({affinity_score:.2f}) between content domain '{content_domain}' and "
            f"L3 pain domain '{pain_domain}'. Compilation blocked."
        )


# ─── Agent Names & Receipt Stages ─────────────────────────────────────────────

AGENT_BATCH_CORE = "Batch-Finalization-Core"
AGENT_DISTANCE = "Semantic-Distance-Analyzer"

STAGE_INGEST = "STAGE-1-SA-INGEST"
STAGE_ANALYSIS = "STAGE-2-AFFINITY-ANALYSIS"
STAGE_ENFORCE = "STAGE-3-ENFORCE"


# ─── Semantic Distance Computation ────────────────────────────────────────────


def compute_semantic_affinity_score(
    content_domain: str,
    pain_domain: str,
    l2_domains: list[str] | None = None,
) -> float:
    """Compute a semantic affinity score between content domain and pain domain.

    This is a token-overlap + substring heuristic that reliably detects
    when content and pain share the same L3 semantic vocabulary (spec §4 Stage 2).

    For production, this can be upgraded to an embedding-based vector distance
    (Task 1 spec), but the deterministic heuristic satisfies the contract.

    Returns:
        float in [0.0, 1.0] — higher = more affinity (more danger for Escape).
    """
    if not content_domain.strip() or not pain_domain.strip():
        return 0.0

    content_tokens = _tokenize(content_domain)
    pain_tokens = _tokenize(pain_domain)

    if not content_tokens or not pain_tokens:
        return 0.0

    # Exact token overlap ratio (Jaccard-style)
    overlap = content_tokens & pain_tokens
    union = content_tokens | pain_tokens
    jaccard = len(overlap) / len(union) if union else 0.0

    # Substring containment boost
    content_lower = content_domain.lower()
    pain_lower = pain_domain.lower()
    containment_boost = 0.0
    if pain_lower in content_lower or content_lower in pain_lower:
        containment_boost = 0.3

    # L2 adjacency check
    l2_boost = 0.0
    if l2_domains:
        for l2 in l2_domains:
            l2_tokens = _tokenize(l2)
            l2_overlap = content_tokens & l2_tokens
            if len(l2_overlap) >= 2:
                l2_boost = max(l2_boost, 0.15)

    score = min(1.0, jaccard + containment_boost + l2_boost)
    return round(score, 4)


def _tokenize(text: str) -> set[str]:
    """Tokenize text into lowercase word tokens, filtering stop words."""
    stop_words = frozenset({
        "the", "a", "an", "and", "or", "but", "is", "are", "was", "were",
        "in", "on", "at", "to", "for", "of", "with", "by", "from", "as",
        "it", "its", "this", "that", "be", "been", "being", "have", "has",
        "had", "do", "does", "did", "will", "would", "could", "should",
        "may", "might", "can", "not", "no", "so", "if", "then", "than",
        "about", "into", "over", "after", "before", "between", "through",
    })
    words = set(re.findall(r"[a-z]+", text.lower()))
    return words - stop_words


def bucket_affinity_rating(score: float) -> AffinityRating:
    """Convert a raw affinity score to an enum rating.

    Spec §4 Stage 2 verdicts:
      ≥ 0.75 → HIGH
      ≥ 0.40 → MEDIUM
      < 0.40 → LOW
    """
    if score >= AFFINITY_THRESHOLD_HIGH:
        return AffinityRating.HIGH
    elif score >= AFFINITY_THRESHOLD_MEDIUM:
        return AffinityRating.MEDIUM
    return AffinityRating.LOW


# ─── C-06 Clearance Logic ─────────────────────────────────────────────────────


def resolve_c06_clearance(
    intended_mode: MoodMode,
    affinity_rating: AffinityRating,
) -> C06Clearance:
    """Apply the C-06 gate logic per spec §3 Technical Decisions + §4 Stage 3.

    Escape + HIGH   → FAIL_TERMINAL
    Escape + MEDIUM → OPERATOR_REVIEW (AC3)
    Processing + HIGH → PASS (AC2 — faces pain directly)
    Status/Discovery + HIGH/MEDIUM → PASS (tolerated)
    Any + LOW → PASS
    """
    if intended_mode == MoodMode.ESCAPE:
        if affinity_rating == AffinityRating.HIGH:
            return C06Clearance.FAIL_TERMINAL
        elif affinity_rating == AffinityRating.MEDIUM:
            return C06Clearance.OPERATOR_REVIEW
        return C06Clearance.PASS

    # Processing, Status, Discovery — HIGH/MEDIUM are tolerated
    return C06Clearance.PASS


# ─── Guard Engine ──────────────────────────────────────────────────────────────


class SemanticAffinityGuard:
    """FR19 — Semantic Affinity Guard Protocol (DEP-PROTO-011).

    3-stage pipeline implementing the C-06 kill switch for Escape + HIGH affinity.

    Spec §2: "It is mathematically impossible for the compiler to produce
    Escape Mode content with a HIGH semantic affinity rating."

    Usage:
        guard = SemanticAffinityGuard(receipt_chain=rc)
        clearance = guard.evaluate(batch_metadata=batch, pain_map=pain_map)
        if clearance.batch_clearance_status == BatchClearanceStatus.BLOCKED:
            # Handle terminal block — present resolution paths to operator
            ...
    """

    def __init__(
        self,
        receipt_chain: ReceiptChain,
        *,
        nlp_available: bool = True,
    ):
        """Initialize the guard.

        Args:
            receipt_chain: ReceiptChain instance scoped to the coach.
            nlp_available: If False, triggers PROVISIONAL_MEDIUM fallback (spec §6).
        """
        self._receipt_chain = receipt_chain
        self._nlp_available = nlp_available

    def evaluate(
        self,
        batch_metadata: BatchMetadata,
        pain_map: PainMapInput,
    ) -> SemanticAffinityClearance:
        """Execute the full Semantic Affinity Guard evaluation.

        Args:
            batch_metadata: All batch slots to evaluate.
            pain_map: Active pain map from DEP-ENG-006.

        Returns:
            SemanticAffinityClearance with per-slot evaluations and overall status.

        Raises:
            DAGViolationError: If pain_map or batch_metadata contains null fields.
        """
        # ── Ghost Variable Prevention Gate ────────────────────────────────────
        self._validate_inputs(batch_metadata, pain_map)

        # ── ADR-01 Isolation (AC4) ────────────────────────────────────────────
        if pain_map.coach_id != batch_metadata.coach_id:
            raise ValueError(
                f"ADR-01 isolation violation: pain_map.coach_id='{pain_map.coach_id}' "
                f"!= batch_metadata.coach_id='{batch_metadata.coach_id}'."
            )

        # ── Stage 1: Ingest ───────────────────────────────────────────────────
        escape_slots = [s for s in batch_metadata.slots if s.intended_mode == MoodMode.ESCAPE]
        non_escape_slots = [s for s in batch_metadata.slots if s.intended_mode != MoodMode.ESCAPE]

        self._receipt_chain.log(
            agent_id=AGENT_BATCH_CORE,
            action=STAGE_INGEST,
            asset_id=batch_metadata.batch_id,
            input_summary=(
                f"batch_id={batch_metadata.batch_id}, "
                f"total_slots={len(batch_metadata.slots)}, "
                f"escape_slots={len(escape_slots)}, "
                f"l3_pain_domain='{pain_map.active_l3_pain_domain[:80]}'"
            ),
            output_summary=f"Normalized {len(batch_metadata.slots)} slots for affinity check.",
            decision="ingested",
            metadata={
                "coach_id": batch_metadata.coach_id,
                "escape_count": len(escape_slots),
                "non_escape_count": len(non_escape_slots),
            },
        )

        # ── Stage 2: Cross-Reference Affinity Analysis ────────────────────────
        evaluations: list[SlotEvaluation] = []
        is_fallback = not self._nlp_available

        for slot in batch_metadata.slots:
            eval_result = self._evaluate_slot(slot, pain_map, is_fallback)
            evaluations.append(eval_result)

        self._receipt_chain.log(
            agent_id=AGENT_DISTANCE,
            action=STAGE_ANALYSIS,
            asset_id=batch_metadata.batch_id,
            input_summary=f"Evaluated {len(evaluations)} slots against L3 pain domain.",
            output_summary=self._summarize_evaluations(evaluations),
            decision="analyzed",
            metadata={
                "coach_id": batch_metadata.coach_id,
                "slot_ratings": {
                    str(e.slot_id): e.affinity_rating.value for e in evaluations
                },
                "is_fallback": is_fallback,
            },
        )

        # ── Stage 3: Enforcement Gate C-06 ────────────────────────────────────
        has_terminal = any(e.c06_clearance == C06Clearance.FAIL_TERMINAL for e in evaluations)
        has_review = any(e.c06_clearance == C06Clearance.OPERATOR_REVIEW for e in evaluations)

        if has_terminal:
            batch_status = BatchClearanceStatus.BLOCKED
        elif has_review:
            batch_status = BatchClearanceStatus.PENDING_REVIEW
        else:
            batch_status = BatchClearanceStatus.CLEARED

        receipt = self._receipt_chain.log(
            agent_id=AGENT_BATCH_CORE,
            action=STAGE_ENFORCE,
            asset_id=batch_metadata.batch_id,
            input_summary=f"C-06 enforcement on {len(evaluations)} slots.",
            output_summary=(
                f"batch_clearance_status={batch_status.value}, "
                f"terminal_blocks={sum(1 for e in evaluations if e.c06_clearance == C06Clearance.FAIL_TERMINAL)}, "
                f"operator_reviews={sum(1 for e in evaluations if e.c06_clearance == C06Clearance.OPERATOR_REVIEW)}"
            ),
            decision=batch_status.value.lower(),
            metadata={
                "coach_id": batch_metadata.coach_id,
                "batch_clearance_status": batch_status.value,
            },
        )

        return SemanticAffinityClearance(
            tenant_id=batch_metadata.coach_id,
            receipt_chain_hash=receipt.receipt_id,
            active_l3_pain_domain=pain_map.active_l3_pain_domain,
            batch_evaluation=evaluations,
            batch_clearance_status=batch_status,
            is_fallback=is_fallback,
            operator_warning=PROVISIONAL_MEDIUM_WARNING if is_fallback else None,
        )

    # ─── Private Helpers ───────────────────────────────────────────────────────

    def _validate_inputs(
        self, batch: BatchMetadata, pain_map: PainMapInput
    ) -> None:
        """Ghost Variable Prevention Gate — spec §3."""
        if not pain_map.active_l3_pain_domain.strip():
            raise DAGViolationError("DEP-ENG-006.active_l3_pain_domain")
        if not batch.slots:
            raise DAGViolationError("batch_metadata.slots")

    def _evaluate_slot(
        self,
        slot: BatchSlot,
        pain_map: PainMapInput,
        is_fallback: bool,
    ) -> SlotEvaluation:
        """Evaluate a single batch slot against the pain map."""
        # Only Escape slots matter for the guard — others always PASS
        if slot.intended_mode != MoodMode.ESCAPE:
            return SlotEvaluation(
                slot_id=slot.slot_id,
                intended_mode=slot.intended_mode,
                content_domain=slot.content_domain,
                affinity_rating=AffinityRating.LOW,
                c06_clearance=C06Clearance.PASS,
                affinity_score=0.0,
            )

        # Fallback: NLP unavailable → all Escape = PROVISIONAL_MEDIUM (spec §6)
        if is_fallback:
            return SlotEvaluation(
                slot_id=slot.slot_id,
                intended_mode=slot.intended_mode,
                content_domain=slot.content_domain,
                affinity_rating=AffinityRating.MEDIUM,
                c06_clearance=C06Clearance.OPERATOR_REVIEW,
                affinity_score=0.5,  # synthetic mid-score
            )

        # Normal: compute semantic distance
        score = compute_semantic_affinity_score(
            content_domain=slot.content_domain,
            pain_domain=pain_map.active_l3_pain_domain,
            l2_domains=pain_map.l2_pain_domains,
        )
        rating = bucket_affinity_rating(score)
        clearance = resolve_c06_clearance(slot.intended_mode, rating)

        resolution_paths: list[C06ResolutionPath] = []
        if clearance == C06Clearance.FAIL_TERMINAL:
            resolution_paths = [
                C06ResolutionPath.DOMAIN_SWAP,
                C06ResolutionPath.RECLASSIFY_PROCESSING,
            ]

        return SlotEvaluation(
            slot_id=slot.slot_id,
            intended_mode=slot.intended_mode,
            content_domain=slot.content_domain,
            affinity_rating=rating,
            c06_clearance=clearance,
            affinity_score=score,
            resolution_paths=resolution_paths,
        )

    def _summarize_evaluations(self, evaluations: list[SlotEvaluation]) -> str:
        high = sum(1 for e in evaluations if e.affinity_rating == AffinityRating.HIGH)
        med = sum(1 for e in evaluations if e.affinity_rating == AffinityRating.MEDIUM)
        low = sum(1 for e in evaluations if e.affinity_rating == AffinityRating.LOW)
        return f"HIGH={high}, MEDIUM={med}, LOW={low} across {len(evaluations)} slots."
