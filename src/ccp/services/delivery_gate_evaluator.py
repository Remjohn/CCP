"""
FR-CBCS-02 — Delivery Gate Evaluator
=====================================
Triple-Condition Delivery Permission Gate (§4 Stage 3-4).

Evaluates three independent conditions before allowing campaign dispatch:
  1. spt_stage >= 3  (Affective Exchange or deeper)
  2. mood_state NOT IN ('Processing', 'Tension', 'Escape')
  3. coping_position >= 3

Verdicts:
  PASS        — all 3 conditions true → dispatch permitted
  PROVISIONAL — conditions 1+3 true, condition 2 false → 24h delay
  FAIL        — condition 1 or 3 false → held indefinitely

C-11 Persona Masking: agent names MUST NOT appear in external payloads.
ADR-01: All operations scoped to coach_id.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    BLOCKED_MOOD_STATES,
    BlockingReason,
    DELIVERY_COPING_MINIMUM,
    DELIVERY_SPT_MINIMUM,
    DeliveryPermissionGateEval,
    DeliveryVerdict,
    PROVISIONAL_DELAY_HOURS,
    SPTError,
)


class DeliveryGateEvaluator:
    """Synchronous triple-condition delivery permission gate.

    Called by Campaign Generator (FR53/FR55) before dispatch.

    Parameters
    ----------
    coach_acronym : str
        2-4 char coach scope (ADR-01).
    coach_id : str
        Coach UUID for DB scoping.
    receipt_chain : ReceiptChain
        Audit trail.
    """

    def __init__(
        self,
        coach_acronym: str,
        coach_id: str,
        receipt_chain: ReceiptChain,
    ) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(
                f"{SPTError.INVALID_COACH_ACRONYM.value}: "
                f"'{coach_acronym}' length must be 2-4."
            )
        self._coach = coach_acronym
        self._coach_id = coach_id
        self._rc = receipt_chain

    # ── public — evaluate gate ────────────────────────────────────

    def evaluate(
        self,
        client_id: str,
        spt_stage: int,
        mood_state: str,
        coping_position: int,
    ) -> DeliveryPermissionGateEval:
        """Evaluate the triple-condition delivery permission gate.

        Parameters
        ----------
        client_id : str
            Target client UUID.
        spt_stage : int
            Current SPT stage (1-4) from social_penetration_depth_gauge.
        mood_state : str
            Current mood from DEP-ENG-018.
        coping_position : int
            Current coping trajectory position (1-5) from FR-CBCS-04.

        Returns
        -------
        DeliveryPermissionGateEval
            Full evaluation payload with verdict and blocking reasons.
        """
        now = datetime.now(timezone.utc).isoformat()
        gate_id = str(uuid.uuid4())

        # ── Condition 1: SPT depth ────────────────────────────────
        spt_condition = spt_stage >= DELIVERY_SPT_MINIMUM

        # ── Condition 2: Mood safety ──────────────────────────────
        mood_condition = mood_state not in BLOCKED_MOOD_STATES

        # ── Condition 3: Coping readiness ─────────────────────────
        coping_condition = coping_position >= DELIVERY_COPING_MINIMUM

        # ── Blocking reasons ──────────────────────────────────────
        blocking: list[str] = []
        if not spt_condition:
            blocking.append(BlockingReason.SPT_FAILED.value)
        if not mood_condition:
            blocking.append(BlockingReason.MOOD_FAILED.value)
        if not coping_condition:
            blocking.append(BlockingReason.COPING_FAILED.value)

        # ── Verdict resolution (§4 Stage 3) ──────────────────────
        all_passed = spt_condition and mood_condition and coping_condition

        if all_passed:
            verdict = DeliveryVerdict.PASS.value
            delay = 0
        elif spt_condition and coping_condition and not mood_condition:
            # Conditions 1+3 true, Condition 2 false → PROVISIONAL
            verdict = DeliveryVerdict.PROVISIONAL.value
            delay = PROVISIONAL_DELAY_HOURS
        else:
            # Condition 1 or 3 is false → FAIL
            verdict = DeliveryVerdict.FAIL.value
            delay = 0

        result = DeliveryPermissionGateEval(
            gate_id=gate_id,
            client_id=client_id,
            coach_id=self._coach_id,
            spt_condition=spt_condition,
            mood_condition=mood_condition,
            coping_condition=coping_condition,
            all_passed=all_passed,
            verdict=verdict,
            blocking_reason=blocking,
            provisional_delay_hours=delay,
            last_evaluated=now,
        )

        # ── Receipt ───────────────────────────────────────────────
        self._rc.log(
            agent_id="delivery-gate-evaluator",
            action="delivery-gate-eval",
            asset_id=gate_id,
            person_id=client_id,
            input_summary=f"spt={spt_stage} mood={mood_state} coping={coping_position}",
            output_summary=f"verdict={verdict} blocking={blocking}",
            metadata={
                "coach": self._coach,
                "client_id": client_id,
                "spt_condition": spt_condition,
                "mood_condition": mood_condition,
                "coping_condition": coping_condition,
                "verdict": verdict,
            },
        )

        return result
