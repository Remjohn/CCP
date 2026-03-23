"""
FR-CBCS-10 — Deep Disclosure Protocol
=======================================
CASA (Computers Are Social Actors) linguistic validation for AI drafts.
Enforces first-person singular, blocks robotic qualifiers, limits
reflective questions to max 1 per payload.

Spec ref: FR_CBCS_10_Deep_Disclosure_Protocol_Tech_Spec.md
"""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    DISCLOSURE_COG_PROCESS_THRESHOLD,
    DISCLOSURE_NEG_EMOTION_THRESHOLD,
    DISCLOSURE_POS_EMOTION_THRESHOLD,
    DISCLOSURE_SPT_STAGE_MIN,
    ROBOTIC_QUALIFIERS,
    CasaMetricsPayload,
    CasaVerdict,
    DisclosureError,
    DisclosureInteractionLogRow,
    InteractionMode,
)

# ── Compiled regex patterns ────────────────────────────────────────────

# First-person singular pronouns (§4 Stage 2)
_FP_SINGULAR_RE = re.compile(r"\b(I|me|my|mine)\b", re.IGNORECASE)

# Robotic qualifiers (§4 Stage 2)
_ROBOTIC_RE = re.compile(
    r"\b(" + "|".join(re.escape(q) for q in ROBOTIC_QUALIFIERS) + r")\b",
    re.IGNORECASE,
)

# Terminal question mark sentences (§4 Stage 2)
_QUESTION_RE = re.compile(r"[^.!?]*\?")


class InteractionModeRouter:
    """Pre-processor that routes client messages to interaction modes.

    Parameters
    ----------
    coach_acronym : str
        2-4 character coach identifier (ADR-01).
    receipt_chain : ReceiptChain
        Immutable audit trail.
    """

    def __init__(self, coach_acronym: str, receipt_chain: ReceiptChain) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(DisclosureError.INVALID_COACH_SCOPE.value)
        self._coach = coach_acronym
        self._rc = receipt_chain

    def route(
        self,
        negative_emotion: float = 0.0,
        positive_emotion: float = 0.0,
        cognitive_processes: float = 0.0,
        spt_stage: int = 1,
    ) -> InteractionMode:
        """Determine interaction mode from LIWC scores + SPT stage.

        Priority order (§4 Stage 1):
          1. VULNERABLE_RECEPTION — negative_emotion > 0.05
          2. ELEVATED_CHALLENGE — cognitive_processes > 0.1 AND spt_stage >= 3
          3. ACTIVE_CONSTRUCTIVE_RESPONDING — positive_emotion > 0.05
          Fallback: ACTIVE_CONSTRUCTIVE_RESPONDING (default)
        """
        if negative_emotion > DISCLOSURE_NEG_EMOTION_THRESHOLD:
            mode = InteractionMode.VULNERABLE_RECEPTION
        elif (cognitive_processes > DISCLOSURE_COG_PROCESS_THRESHOLD
              and spt_stage >= DISCLOSURE_SPT_STAGE_MIN):
            mode = InteractionMode.ELEVATED_CHALLENGE
        elif positive_emotion > DISCLOSURE_POS_EMOTION_THRESHOLD:
            mode = InteractionMode.ACTIVE_CONSTRUCTIVE_RESPONDING
        else:
            mode = InteractionMode.ACTIVE_CONSTRUCTIVE_RESPONDING

        self._rc.log(
            agent_id="interaction-mode-router",
            action="disclosure-mode-route",
            input_summary=(
                f"neg_emo={negative_emotion}, pos_emo={positive_emotion}, "
                f"cog={cognitive_processes}, spt={spt_stage}"
            ),
            output_summary=f"mode={mode.value}",
            decision=mode.value,
        )
        return mode


class CasaLinguisticValidator:
    """Post-generation validator enforcing CASA paradigm on AI drafts.

    Parameters
    ----------
    coach_acronym : str
        2-4 character coach identifier (ADR-01).
    receipt_chain : ReceiptChain
        Immutable audit trail.
    """

    def __init__(self, coach_acronym: str, receipt_chain: ReceiptChain) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(DisclosureError.INVALID_COACH_SCOPE.value)
        self._coach = coach_acronym
        self._rc = receipt_chain

    # ── Stage 2: Metric extraction ─────────────────────────────────────

    @staticmethod
    def count_first_person_singular(draft: str) -> int:
        """Count first-person singular pronouns (I, me, my, mine)."""
        return len(_FP_SINGULAR_RE.findall(draft))

    @staticmethod
    def count_robotic_qualifiers(draft: str) -> int:
        """Count robotic qualifier phrases."""
        return len(_ROBOTIC_RE.findall(draft))

    @staticmethod
    def count_reflective_questions(draft: str) -> int:
        """Count sentences ending with a question mark."""
        return len(_QUESTION_RE.findall(draft))

    @staticmethod
    def trim_to_first_question(draft: str) -> str:
        """Trim draft after first question mark — single-question rule.

        If the draft contains multiple questions, everything after the
        first ``?`` sentence-end is removed (§7 Task 3: Provisional Trimmer).
        """
        questions = _QUESTION_RE.findall(draft)
        if len(questions) <= 1:
            return draft
        # Find the position right after the first '?'
        first_q_end = draft.find("?") + 1
        return draft[:first_q_end].strip()

    # ── Stage 3: CASA Linguistic Gate ──────────────────────────────────

    def validate(
        self,
        client_id: str,
        draft_ai_reply: str,
        interaction_mode: InteractionMode,
    ) -> DisclosureInteractionLogRow:
        """Run the CASA Linguistic Gate on *draft_ai_reply*.

        Parameters
        ----------
        client_id:
            Unique client identifier.
        draft_ai_reply:
            The LLM-generated draft reply.
        interaction_mode:
            The pre-routed interaction mode from Stage 1.

        Returns
        -------
        DisclosureInteractionLogRow
            Complete interaction log with verdict and final text.
        """
        now_iso = datetime.now(timezone.utc).isoformat()
        interaction_id = str(uuid.uuid4())

        # Empty draft guard
        if not draft_ai_reply or not draft_ai_reply.strip():
            row = DisclosureInteractionLogRow(
                interaction_id=interaction_id,
                client_id=client_id,
                coach_id=self._coach,
                interaction_mode=interaction_mode.value,
                casa_verdict=CasaVerdict.FAIL_REWRITE.value,
                metrics_payload=CasaMetricsPayload(
                    fp_count=0, robotic_count=0, question_count=0,
                ),
                final_dispatched_text="",
                timestamp_utc=now_iso,
            )
            self._log_receipt(row)
            return row

        # Stage 2 — Metric computation
        fp_count = self.count_first_person_singular(draft_ai_reply)
        robotic_count = self.count_robotic_qualifiers(draft_ai_reply)
        question_count = self.count_reflective_questions(draft_ai_reply)

        # Stage 3 — Gate evaluation
        cond1 = fp_count > 0
        cond2 = robotic_count == 0
        cond3 = question_count <= 1

        if cond1 and cond2 and cond3:
            verdict = CasaVerdict.PASS
            final_text = draft_ai_reply
        elif cond1 and cond2 and not cond3:
            verdict = CasaVerdict.PROVISIONAL_TRIMMED
            final_text = self.trim_to_first_question(draft_ai_reply)
        else:
            verdict = CasaVerdict.FAIL_REWRITE
            final_text = draft_ai_reply  # Original preserved for rewrite loop

        row = DisclosureInteractionLogRow(
            interaction_id=interaction_id,
            client_id=client_id,
            coach_id=self._coach,
            interaction_mode=interaction_mode.value,
            casa_verdict=verdict.value,
            metrics_payload=CasaMetricsPayload(
                fp_count=fp_count,
                robotic_count=robotic_count,
                question_count=question_count,
            ),
            final_dispatched_text=final_text,
            timestamp_utc=now_iso,
        )
        self._log_receipt(row)
        return row

    # ── Receipt Chain ──────────────────────────────────────────────────

    def _log_receipt(self, row: DisclosureInteractionLogRow) -> None:
        self._rc.log(
            agent_id="casa-linguistic-validator",
            action="casa-linguistic-validate",
            input_summary=f"client={row.client_id}, mode={row.interaction_mode}",
            output_summary=f"verdict={row.casa_verdict}",
            decision=row.casa_verdict,
            decision_rationale=(
                f"fp={row.metrics_payload.fp_count}, "
                f"robotic={row.metrics_payload.robotic_count}, "
                f"questions={row.metrics_payload.question_count}"
            ),
            metadata={
                "interaction_id": row.interaction_id,
                "interaction_mode": row.interaction_mode,
            },
        )
