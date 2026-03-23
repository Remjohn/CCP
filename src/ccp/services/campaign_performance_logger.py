"""
FR56: Campaign Performance Registry
=====================================
Two classes:
  ConversionOutcomeResolver   — Stage 1: webhook → ConversionOutcome enum
  CampaignPerformanceLogger   — Stage 2: completeness gate + CampaignPerformanceRegistryRow
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cpsc_models import (
    BOOKED_WEBHOOK_KEYS,
    CAMPAIGN_DORMANCY_HOURS,
    DECLINED_WEBHOOK_KEYS,
    CampaignPerformanceRegistryRow,
    CampaignRegistryError,
    ConversionOutcome,
    PsychSnapshotAtLaunch,
    RegistryGateVerdict,
)

_ADR01_MIN = 2
_ADR01_MAX = 4


def _validate_coach_id(coach_id: str) -> None:
    if not (_ADR01_MIN <= len(coach_id) <= _ADR01_MAX):
        raise ValueError(
            f"ADR-01: coach_id must be {_ADR01_MIN}-{_ADR01_MAX} chars; "
            f"got {len(coach_id)!r}"
        )


# ══════════════════════════════════════════════════════════════════════
# Stage 1 — ConversionOutcomeResolver
# ══════════════════════════════════════════════════════════════════════


class ConversionOutcomeResolver:
    """
    Resolves ConversionOutcome from a commercial webhook payload (§4 Stage 1).

    Resolution rules (in priority order):
      BOOKED_CONVERTED  — payload contains any BOOKED_WEBHOOK_KEY
                          (checkout.session.completed / charge.succeeded / invitee.created)
      DECLINED_OPT_OUT  — payload contains "/stop" or "no thanks" (case-insensitive)
      NO_RESPONSE_DORMANT — hours_elapsed_since_offer > 72.0 and no positive/negative signal

    If client_id is missing from webhook, raises ValueError(MISSING_CLIENT_ID).
    """

    def __init__(self, coach_id: str) -> None:
        _validate_coach_id(coach_id)
        self._coach_id = coach_id

    # ------------------------------------------------------------------

    def resolve(
        self,
        webhook_payload: dict[str, Any],
        hours_elapsed_since_offer: float | None = None,
    ) -> tuple[str, ConversionOutcome]:
        """
        Resolve client_id and ConversionOutcome from a webhook payload.

        Parameters
        ----------
        webhook_payload:
            Raw dict representing the incoming webhook (Stripe / Calendly / Telegram).
        hours_elapsed_since_offer:
            Hours since the offer was delivered. Used for dormancy check.

        Returns
        -------
        (client_id, ConversionOutcome)

        Raises
        ------
        ValueError if client_id is absent from payload.
        """
        # Guard: client_id must be present
        client_id = webhook_payload.get("client_id") or webhook_payload.get("metadata", {}).get("client_id")
        if not client_id:
            raise ValueError(
                f"{CampaignRegistryError.MISSING_CLIENT_ID.value}: "
                "webhook payload must contain a traceable client_id"
            )

        # Flatten payload to a single searchable string for key scanning
        payload_str = _flatten_payload(webhook_payload)

        # BOOKED_CONVERTED: any booking/charge key present
        for key in BOOKED_WEBHOOK_KEYS:
            if key.lower() in payload_str.lower():
                return client_id, ConversionOutcome.BOOKED_CONVERTED

        # DECLINED_OPT_OUT: opt-out signal present
        for key in DECLINED_WEBHOOK_KEYS:
            if key.lower() in payload_str.lower():
                return client_id, ConversionOutcome.DECLINED_OPT_OUT

        # NO_RESPONSE_DORMANT: time-based fallback
        hours = hours_elapsed_since_offer if hours_elapsed_since_offer is not None else 0.0
        if hours > CAMPAIGN_DORMANCY_HOURS:
            return client_id, ConversionOutcome.NO_RESPONSE_DORMANT

        # Default: still within window, no signal — treat as dormant pending
        return client_id, ConversionOutcome.NO_RESPONSE_DORMANT


def _flatten_payload(payload: dict[str, Any], depth: int = 0) -> str:
    """Recursively flatten a dict into a single space-separated string of keys and values."""
    if depth > 5:
        return ""
    parts: list[str] = []
    for k, v in payload.items():
        parts.append(str(k))
        if isinstance(v, dict):
            parts.append(_flatten_payload(v, depth + 1))
        elif isinstance(v, (list, tuple)):
            for item in v:
                if isinstance(item, dict):
                    parts.append(_flatten_payload(item, depth + 1))
                else:
                    parts.append(str(item))
        else:
            parts.append(str(v))
    return " ".join(parts)


# ══════════════════════════════════════════════════════════════════════
# Stage 2 — CampaignPerformanceLogger
# ══════════════════════════════════════════════════════════════════════


class CampaignPerformanceLogger:
    """
    Registry Completeness Gate + CampaignPerformanceRegistryRow emission (§4 Stage 2).

    Gate verdicts:
      PASS              — coping_tier, spt_stage, AND intimacy_score all non-null
      PROVISIONAL_PARTIAL — coping_tier non-null but non-critical fields (spt/intimacy) missing
      FAIL_CORRUPTED    — coping_tier is null → row MUST NOT write to DB (raises ValueError)
    """

    def __init__(
        self,
        coach_id: str,
        receipt_chain: ReceiptChain | None = None,
    ) -> None:
        _validate_coach_id(coach_id)
        self._coach_id = coach_id
        self._rc = receipt_chain
        self._resolver = ConversionOutcomeResolver(coach_id=coach_id)

    # ------------------------------------------------------------------

    def log_outcome(
        self,
        campaign_execution_id: str,
        webhook_payload: dict[str, Any],
        psych_snapshot: PsychSnapshotAtLaunch | None = None,
        time_to_conversion_hours: float | None = None,
        hours_elapsed_since_offer: float | None = None,
    ) -> CampaignPerformanceRegistryRow:
        """
        Full pipeline: resolve outcome → gate → emit registry row.

        Parameters
        ----------
        campaign_execution_id:
            UUID from FR59 Campaign Orchestrator.
        webhook_payload:
            Raw webhook dict. Must contain traceable client_id.
        psych_snapshot:
            T-1 psychological state snapshot. May be partial.
        time_to_conversion_hours:
            Float hours from launch to conversion, or None if not converted.
        hours_elapsed_since_offer:
            Hours since the offer was delivered (for dormancy resolution).

        Returns
        -------
        CampaignPerformanceRegistryRow (DEP-ENG-051)

        Raises
        ------
        ValueError if coping_tier is null (FAIL_CORRUPTED) or client_id missing.
        """
        # Stage 1 — Resolve outcome
        client_id, outcome = self._resolver.resolve(
            webhook_payload=webhook_payload,
            hours_elapsed_since_offer=hours_elapsed_since_offer,
        )

        if self._rc is not None:
            self._rc.log(
                agent_id="campaign-performance-logger",
                action="conversion-outcome-resolve",
                output_summary=(
                    f"client={client_id} outcome={outcome.value} "
                    f"campaign={campaign_execution_id}"
                ),
            )

        # Stage 2 — Registry Completeness Gate
        snapshot = psych_snapshot or PsychSnapshotAtLaunch()
        gate_verdict = self._evaluate_gate(snapshot)

        # FAIL_CORRUPTED — hard reject, do not produce row
        if gate_verdict == RegistryGateVerdict.FAIL_CORRUPTED:
            if self._rc is not None:
                self._rc.log(
                    agent_id="campaign-performance-logger",
                    action="registry-completeness-gate",
                    output_summary=(
                        f"client={client_id} verdict=FAIL_CORRUPTED "
                        f"reason=coping_tier_null campaign={campaign_execution_id}"
                    ),
                )
            raise ValueError(
                f"{CampaignRegistryError.CORRUPTED_PSYCH_SNAPSHOT.value}: "
                "Attempting to log commercial run without psychological context "
                "invalidates data integrity."
            )

        row = CampaignPerformanceRegistryRow(
            registry_id=str(uuid.uuid4()),
            campaign_execution_id=campaign_execution_id,
            client_id=client_id,
            coach_id=self._coach_id,
            conversion_outcome=outcome.value,
            psych_snapshot_at_launch=snapshot,
            time_to_conversion_hours=time_to_conversion_hours,
            gate_verdict=gate_verdict.value,
            log_timestamp=datetime.now(timezone.utc).isoformat(),
        )

        if self._rc is not None:
            self._rc.log(
                agent_id="campaign-performance-logger",
                action="registry-completeness-gate",
                output_summary=(
                    f"client={client_id} verdict={gate_verdict.value} "
                    f"registry_id={row.registry_id}"
                ),
            )

        return row

    # ------------------------------------------------------------------

    @staticmethod
    def _evaluate_gate(snapshot: PsychSnapshotAtLaunch) -> RegistryGateVerdict:
        """
        Evaluate the Registry Completeness Gate (§4 Stage 2).

        PASS              — all three fields non-null
        PROVISIONAL_PARTIAL — coping_tier present, but spt or intimacy null
        FAIL_CORRUPTED    — coping_tier null
        """
        if snapshot.coping_tier is None:
            return RegistryGateVerdict.FAIL_CORRUPTED

        if snapshot.spt_stage is None or snapshot.intimacy_score is None:
            return RegistryGateVerdict.PROVISIONAL_PARTIAL

        return RegistryGateVerdict.PASS
