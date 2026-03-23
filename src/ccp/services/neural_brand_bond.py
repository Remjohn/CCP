"""
FR-CBCS-11 — Neural Brand Bond Protocol
=========================================
Enforces dmPFC activation via social narrative gating. Translates
abstract brand values into concrete story structures and validates
drafts for human actors and cliché-free language.

Spec ref: FR_CBCS_11_Neural_Brand_Bond_Protocol_Tech_Spec.md
"""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    BRAND_CLICHES,
    BRAND_STORY_MIN_WORDS,
    SOCIAL_NOUNS,
    STORY_STRUCTURE_MAP,
    DmpfcGateVerdictRow,
    DmpfcMetricsPayload,
    DmpfcVerdict,
    NeuralBrandError,
    StoryStructure,
)

# ── Compiled regex patterns ────────────────────────────────────────────

_SOCIAL_NOUNS_RE = re.compile(
    r"\b(" + "|".join(re.escape(w) for w in SOCIAL_NOUNS) + r")\b",
    re.IGNORECASE,
)

_CLICHE_RE = re.compile(
    r"\b(" + "|".join(re.escape(c) for c in BRAND_CLICHES) + r")\b",
    re.IGNORECASE,
)


class BrandStoryPlanner:
    """Maps target brand values to strict story structures (§4 Stage 1).

    Parameters
    ----------
    coach_acronym : str
        2-4 character coach identifier (ADR-01).
    receipt_chain : ReceiptChain
        Immutable audit trail.
    """

    def __init__(self, coach_acronym: str, receipt_chain: ReceiptChain) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(NeuralBrandError.INVALID_COACH_SCOPE.value)
        self._coach = coach_acronym
        self._rc = receipt_chain

    def resolve_story_structure(
        self,
        target_brand_value: str,
    ) -> StoryStructure:
        """Map a brand value string to one of three story structures.

        Parameters
        ----------
        target_brand_value:
            The coach's configured brand value (e.g., "Discipline", "Growth").

        Returns
        -------
        StoryStructure
            The resolved story structure enum.

        Raises
        ------
        ValueError
            If the brand value has no mapping.
        """
        structure_key = STORY_STRUCTURE_MAP.get(target_brand_value)
        if structure_key is None:
            raise ValueError(
                f"{NeuralBrandError.UNKNOWN_BRAND_VALUE.value}: {target_brand_value}"
            )
        structure = StoryStructure(structure_key)
        self._rc.log(
            agent_id="brand-story-planner",
            action="brand-story-structure-resolve",
            input_summary=f"value={target_brand_value}",
            output_summary=f"structure={structure.value}",
            decision=structure.value,
        )
        return structure


class DmpfcSemanticEvaluator:
    """Post-generation dmPFC semantic gate for brand narratives.

    Parameters
    ----------
    coach_acronym : str
        2-4 character coach identifier (ADR-01).
    receipt_chain : ReceiptChain
        Immutable audit trail.
    """

    def __init__(self, coach_acronym: str, receipt_chain: ReceiptChain) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(NeuralBrandError.INVALID_COACH_SCOPE.value)
        self._coach = coach_acronym
        self._rc = receipt_chain

    # ── Stage 2: Metric extraction ─────────────────────────────────────

    @staticmethod
    def count_social_nouns(draft: str) -> int:
        """Count social noun words in *draft* (§4 Stage 2)."""
        return len(_SOCIAL_NOUNS_RE.findall(draft))

    @staticmethod
    def count_brand_cliches(draft: str) -> int:
        """Count brand cliché phrases in *draft* (§4 Stage 2)."""
        return len(_CLICHE_RE.findall(draft))

    @staticmethod
    def check_moral_sentiment(draft: str, target_brand_value: str) -> bool:
        """Simple moral sentiment match — checks if the target value
        or a close derivative appears in the draft text."""
        return target_brand_value.lower() in draft.lower()

    # ── Stage 3: dmPFC Semantic Gate ───────────────────────────────────

    def evaluate(
        self,
        draft_brand_story: str,
        story_structure: StoryStructure,
        target_brand_value: str,
    ) -> DmpfcGateVerdictRow:
        """Run the dmPFC Semantic Gate on *draft_brand_story*.

        Parameters
        ----------
        draft_brand_story:
            The drafted brand story text.
        story_structure:
            The pre-resolved story structure from Stage 1.
        target_brand_value:
            The coach's configured brand value.

        Returns
        -------
        DmpfcGateVerdictRow
            Complete evaluation with verdict and metrics.
        """
        eval_id = str(uuid.uuid4())
        evaluated_at = datetime.now(timezone.utc).isoformat()

        # Story too short guard (< 50 words)
        word_count = len(draft_brand_story.split())
        if word_count < BRAND_STORY_MIN_WORDS:
            result = DmpfcGateVerdictRow(
                eval_id=eval_id,
                coach_id=self._coach,
                story_structure_used=story_structure.value,
                semantic_verdict=DmpfcVerdict.FAIL_REJECTED.value,
                metrics_payload=DmpfcMetricsPayload(
                    social_nouns_found=0,
                    cliches_found=0,
                    moral_sentiment_matched=False,
                ),
                evaluated_at=evaluated_at,
            )
            self._log_receipt(result, "Story too short")
            return result

        # Stage 2 — Metric computation
        social_count = self.count_social_nouns(draft_brand_story)
        cliche_count = self.count_brand_cliches(draft_brand_story)
        moral_match = self.check_moral_sentiment(
            draft_brand_story, target_brand_value,
        )

        # Stage 3 — Gate evaluation
        cond1 = social_count >= 2
        cond2 = cliche_count == 0
        cond3 = moral_match is True

        if cond1 and cond2 and cond3:
            verdict = DmpfcVerdict.PASS
        elif cond1 and cond3 and not cond2:
            verdict = DmpfcVerdict.PROVISIONAL_REVIEW
        else:
            verdict = DmpfcVerdict.FAIL_REJECTED

        result = DmpfcGateVerdictRow(
            eval_id=eval_id,
            coach_id=self._coach,
            story_structure_used=story_structure.value,
            semantic_verdict=verdict.value,
            metrics_payload=DmpfcMetricsPayload(
                social_nouns_found=social_count,
                cliches_found=cliche_count,
                moral_sentiment_matched=moral_match,
            ),
            evaluated_at=evaluated_at,
        )
        self._log_receipt(result)
        return result

    # ── Receipt Chain ──────────────────────────────────────────────────

    def _log_receipt(
        self,
        result: DmpfcGateVerdictRow,
        extra_rationale: str = "",
    ) -> None:
        self._rc.log(
            agent_id="dmpfc-semantic-evaluator",
            action="dmpfc-semantic-evaluate",
            input_summary=f"coach={result.coach_id}, structure={result.story_structure_used}",
            output_summary=f"verdict={result.semantic_verdict}",
            decision=result.semantic_verdict,
            decision_rationale=(
                extra_rationale
                or f"social={result.metrics_payload.social_nouns_found}, "
                   f"cliches={result.metrics_payload.cliches_found}, "
                   f"moral={result.metrics_payload.moral_sentiment_matched}"
            ),
            metadata={
                "eval_id": result.eval_id,
                "social_nouns_found": result.metrics_payload.social_nouns_found,
                "cliches_found": result.metrics_payload.cliches_found,
            },
        )
