"""
FR53 — Conversion Sequence Generator
======================================
Executes the 72-Hour Identity Anchor Protocol at scale by combining
SPT stage vulnerability calibration with a real-time Dormancy Recovery
Gate, producing ConversionSequencePayloadRow (DEP-ENG-074).

Classes
-------
VulnerabilityModeResolver
    Maps an SPT stage integer to a SequenceVulnerabilityMode enum,
    falling back to OBJECTIVE_REFLECTIVE for null/missing history.

DormancyRecoveryGate
    Evaluates hours_since_last_client_message against thresholds and
    returns a DormancyGateVerdict.

ConversionSequenceRouter
    Orchestrates both stages, assembles the payload, and writes receipt
    chain entries (DEP-ENG-041).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from src.ccp.models.cpsc_models import (
    ConversionSequencePayloadRow,
    DormancyGateVerdict,
    SequenceError,
    SequenceVulnerabilityMode,
)
from src.ccp.core.receipt_chain import ReceiptChain

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# SPT stage threshold for linguistic mode (§4 Stage 1)
SPT_AFFECTIVE_THRESHOLD: int = 3   # spt_stage ≥ 3 → AFFECTIVE_ATTACHMENT
SPT_NULL_FALLBACK: int = -1        # null spt → defaults to -1 → OBJECTIVE_REFLECTIVE

# Dormancy gate thresholds in hours (§4 Stage 2)
DORMANCY_PASS_MAX_HOURS: float = 36.0    # < 36 h → PASS_ACTIVE
DORMANCY_PROVISIONAL_MAX_HOURS: float = 72.0  # 36 ≤ h < 72 → PROVISIONAL
# ≥ 72 h → FAIL_DORMANT_ABORT


# ---------------------------------------------------------------------------
# VulnerabilityModeResolver
# ---------------------------------------------------------------------------

class VulnerabilityModeResolver:
    """
    Maps SPT stage to SequenceVulnerabilityMode.

    Parameters
    ----------
    spt_stage : int | None
        Social penetration depth stage from FR-CBCS-02.
        None → treated as -1 → OBJECTIVE_REFLECTIVE (§6 fallback).
    """

    def __init__(self, spt_stage: int | None) -> None:
        self._stage = spt_stage if spt_stage is not None else SPT_NULL_FALLBACK

    def resolve(self) -> SequenceVulnerabilityMode:
        """Return the linguistic depth mode for this SPT stage.

        Resolution (§4 Stage 1):
        - spt_stage >= 3 → AFFECTIVE_ATTACHMENT
        - spt_stage <= 2 (or null fallback -1) → OBJECTIVE_REFLECTIVE
        """
        if self._stage >= SPT_AFFECTIVE_THRESHOLD:
            return SequenceVulnerabilityMode.AFFECTIVE_ATTACHMENT
        return SequenceVulnerabilityMode.OBJECTIVE_REFLECTIVE


# ---------------------------------------------------------------------------
# DormancyRecoveryGate
# ---------------------------------------------------------------------------

class DormancyRecoveryGate:
    """
    Evaluates client engagement lag against dormancy thresholds.

    Parameters
    ----------
    hours_since_last_message : float
        Float hours elapsed since the client's last webhook interaction.
    """

    def __init__(self, hours_since_last_message: float) -> None:
        self._hours = hours_since_last_message

    def evaluate(self) -> DormancyGateVerdict:
        """
        Return the dormancy gate verdict.

        - hours < 36   → PASS_ACTIVE
        - 36 ≤ hours < 72 → PROVISIONAL_DORMANT_RECOVERY
        - hours ≥ 72   → FAIL_DORMANT_ABORT
        """
        h = self._hours
        if h < DORMANCY_PASS_MAX_HOURS:
            return DormancyGateVerdict.PASS_ACTIVE
        if h < DORMANCY_PROVISIONAL_MAX_HOURS:
            return DormancyGateVerdict.PROVISIONAL_DORMANT_RECOVERY
        return DormancyGateVerdict.FAIL_DORMANT_ABORT


# ---------------------------------------------------------------------------
# ConversionSequenceRouter
# ---------------------------------------------------------------------------

class ConversionSequenceRouter:
    """
    Orchestrates FR53: resolves vulnerability mode, evaluates dormancy,
    and returns a ConversionSequencePayloadRow.

    Parameters
    ----------
    coach_id : str
        ADR-01 boundary key.
    receipt_chain : ReceiptChain
        Live receipt chain (DEP-ENG-041).
    """

    _AGENT_ID = "conversion-sequence-router"

    def __init__(self, coach_id: str, receipt_chain: ReceiptChain) -> None:
        if not isinstance(coach_id, str) or len(coach_id) < 2:
            raise ValueError("coach_id must be a non-empty string (min 2 chars).")
        self._coach_id = coach_id
        self._rc = receipt_chain

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def route(
        self,
        *,
        client_id: str,
        spt_stage: int | None,
        hours_since_last_message: float,
        current_sequence_step: int,
        next_payload_string: str | None,
    ) -> ConversionSequencePayloadRow:
        """
        Compile and return a ConversionSequencePayloadRow.

        Parameters
        ----------
        client_id : str
            Target prospect / client identifier.
        spt_stage : int | None
            Social penetration depth stage. None → OBJECTIVE_REFLECTIVE.
        hours_since_last_message : float
            Hours since last client-initiated message.
        current_sequence_step : int
            Day step (1, 2, or 3).
        next_payload_string : str | None
            Draft message text. Overridden to None if FAIL_DORMANT_ABORT.

        Returns
        -------
        ConversionSequencePayloadRow

        Raises
        ------
        ValueError(SequenceError.FAIL_DORMANT_ABORT)
            If dormancy gate returns FAIL_DORMANT_ABORT (hard abort,
            receipt logged before raising).
        """
        # ── Stage 1: Vulnerability Mode Resolution ────────────────────
        mode = VulnerabilityModeResolver(spt_stage).resolve()

        root_receipt = self._rc.log(
            agent_id=self._AGENT_ID,
            action="sequence-vulnerability-resolve",
            output_summary=(
                f"coach={self._coach_id} client={client_id} "
                f"spt_stage={spt_stage} mode={mode.value}"
            ),
        )

        # ── Stage 2: Dormancy Recovery Gate ───────────────────────────
        gate = DormancyRecoveryGate(hours_since_last_message)
        verdict = gate.evaluate()

        if verdict == DormancyGateVerdict.FAIL_DORMANT_ABORT:
            self._rc.log(
                agent_id=self._AGENT_ID,
                action="sequence-dormancy-gate",
                output_summary=(
                    f"coach={self._coach_id} client={client_id} "
                    f"hours={hours_since_last_message} verdict=FAIL_DORMANT_ABORT — "
                    "campaign sequence aborted"
                ),
                parent_receipt_id=root_receipt.receipt_id,
            )
            raise ValueError(SequenceError.FAIL_DORMANT_ABORT)

        # PROVISIONAL → pivot next_payload_string to recovery ping instruction
        if verdict == DormancyGateVerdict.PROVISIONAL_DORMANT_RECOVERY:
            final_payload = (
                "[RECOVERY PING] Lightweight re-engagement prompt — "
                "commercial progression halted."
            )
        else:
            # PASS_ACTIVE — use provided payload
            final_payload = next_payload_string

        self._rc.log(
            agent_id=self._AGENT_ID,
            action="sequence-dormancy-gate",
            output_summary=(
                f"coach={self._coach_id} client={client_id} "
                f"hours={hours_since_last_message} verdict={verdict.value}"
            ),
            parent_receipt_id=root_receipt.receipt_id,
        )

        return ConversionSequencePayloadRow(
            sequence_execution_id=str(uuid.uuid4()),
            client_id=client_id,
            coach_id=self._coach_id,
            sequence_vulnerability_mode=mode.value,
            gate_verdict=verdict.value,
            current_sequence_step_integer=current_sequence_step,
            next_payload_string=final_payload,
            execution_timestamp=datetime.now(timezone.utc).isoformat(),
        )
