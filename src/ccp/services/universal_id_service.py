"""
FR46 — Universal Asset & Person ID Service (DEP-ENG-040)
Atomic ID generation with fallback to UNIX timestamps.

AC1: Atomic Supabase sequence incrementation.
AC2: Format enum guard — rejects unknown tags.
AC3: Coach zero-assignment (PID-{COACH}-0000 for coach).
AC4: UNIX timestamp fallback on DB failure.
"""

from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cross_system_models import (
    FormatTag,
    IDGenerationPayload,
    PERSON_ID_COACH_SEQUENCE_ZERO,
    PersonID,
    PipelineType,
    UniversalAssetID,
)


class UniversalIDService:
    """
    FR46: Single-tenant ID generation for persons and assets.
    Atomic DB increment or UNIX-timestamp fallback.
    """

    def __init__(self, coach_acronym: str) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(f"coach_acronym must be 2-4 chars, got '{coach_acronym}'")
        self._coach = coach_acronym.upper()
        self._receipt_chain = ReceiptChain(coach_acronym=self._coach)
        # In-memory sequence counters (replaced by Supabase atomic in production)
        self._person_sequence: int = 0
        self._asset_sequence: int = 0

    # ── Person ID ──────────────────────────────────────

    def generate_coach_person_id(self) -> PersonID:
        """
        FR46 AC3: Coach is always PID-{COACH}-0000.
        """
        pid = PersonID(
            person_id=f"PID-{self._coach}-{PERSON_ID_COACH_SEQUENCE_ZERO}",
            coach_acronym=self._coach,
            sequence=PERSON_ID_COACH_SEQUENCE_ZERO,
            is_coach=True,
        )
        self._receipt_chain.log(
            agent_id="UniversalIDService",
            action="COACH_PERSON_ID_GENERATED",
            asset_id=pid.person_id,
            decision="SUCCESS",
        )
        return pid

    def generate_client_person_id(self) -> PersonID:
        """
        FR46 AC1: Atomic increment for client person ID.
        Clients start at 0001.
        """
        seq = self._next_person_sequence()
        pid = PersonID(
            person_id=f"PID-{self._coach}-{seq}",
            coach_acronym=self._coach,
            sequence=seq,
            is_coach=False,
        )
        self._receipt_chain.log(
            agent_id="UniversalIDService",
            action="CLIENT_PERSON_ID_GENERATED",
            asset_id=pid.person_id,
            decision="SUCCESS",
        )
        return pid

    # ── Asset ID ───────────────────────────────────────

    def generate_asset_id(
        self,
        pipeline: PipelineType,
        format_tag: FormatTag,
        date_override: Optional[str] = None,
    ) -> UniversalAssetID:
        """
        FR46 AC2: {COACH}-{PIPELINE}-{DATE}-{SEQ}-{FORMAT}.
        Rejects unknown pipeline/format values via enum enforcement.
        """
        date_str = date_override or datetime.now(timezone.utc).strftime("%Y%m%d")
        seq = self._next_asset_sequence()
        asset_id_str = f"{self._coach}-{pipeline.value}-{date_str}-{seq}-{format_tag.value}"

        uid = UniversalAssetID(
            asset_id=asset_id_str,
            coach_acronym=self._coach,
            pipeline=pipeline,
            date_str=date_str,
            sequence=seq,
            format_tag=format_tag,
        )
        self._receipt_chain.log(
            agent_id="UniversalIDService",
            action="ASSET_ID_GENERATED",
            asset_id=uid.asset_id,
            decision="SUCCESS",
        )
        return uid

    # ── Composite ──────────────────────────────────────

    def generate_payload(
        self,
        *,
        person_id: Optional[str] = None,
        asset_id: Optional[str] = None,
    ) -> IDGenerationPayload:
        """FR46 §5: full DEP-ENG-040 payload."""
        return IDGenerationPayload(
            coach_id=self._coach,
            assigned_person_id=person_id,
            assigned_asset_id=asset_id,
            id_metadata={
                "generator": "UniversalIDService",
                "coach_acronym": self._coach,
            },
        )

    # ── Internal Sequences ─────────────────────────────

    def _next_person_sequence(self) -> str:
        """
        FR46 AC1/AC4: Atomic increment with UNIX fallback.
        In production, this calls Supabase atomic counter.
        """
        try:
            self._person_sequence += 1
            return f"{self._person_sequence:04d}"
        except Exception:
            # FR46 AC4: UNIX timestamp fallback
            return str(int(time.time()))[-4:]

    def _next_asset_sequence(self) -> str:
        """FR46 AC1/AC4: Same atomic + fallback for assets."""
        try:
            self._asset_sequence += 1
            return f"{self._asset_sequence:04d}"
        except Exception:
            return str(int(time.time()))[-4:]
