"""
FR57: Social Proof Intelligence Engine
========================================
Two classes:
  SocialProofRetriever     — Stage 1: 3-point segment filtering against archive
  RelevanceStringencyGate  — Stage 2: gate verdict + MatchedTestimonialPayloadRow
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cpsc_models import (
    MatchTierRating,
    MatchedTestimonialPayloadRow,
    SocialProofError,
    SocialProofGateVerdict,
    TestimonialArchiveEntry,
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
# Stage 1 — SocialProofRetriever
# ══════════════════════════════════════════════════════════════════════


class SocialProofRetriever:
    """
    3-point segment filtering against a testimonial archive (§4 Stage 1).

    Filter Precision rules (in priority order):
      PERFECT_MATCH  — exact coping AND exact spt match found in archive
      ADJACENT_MATCH — coping ±1 AND exact spt match found (no exact coping available)
      BASELINE_DEFAULT — no match within either bound → fallback / empty archive

    ADR-01: only archive entries where entry.coach_id == self._coach_id are searched.
    Anti-Fabrication Rule: testimonial_text is returned verbatim; no LLM rewrite.
    """

    def __init__(self, coach_id: str) -> None:
        _validate_coach_id(coach_id)
        self._coach_id = coach_id

    # ------------------------------------------------------------------

    def retrieve(
        self,
        target_client_id: str,
        target_coping: int,
        target_spt: int,
        archive: list[TestimonialArchiveEntry],
    ) -> tuple[MatchTierRating, TestimonialArchiveEntry | None]:
        """
        Run 3-point segment filtering against the archive.

        Parameters
        ----------
        target_client_id:
            ID of the prospect being matched.
        target_coping:
            Coping position (1-5) from FR-CBCS-04.
        target_spt:
            SPT stage (1-5) from FR-CBCS-02.
        archive:
            List of TestimonialArchiveEntry records (coach-scoped).

        Returns
        -------
        (MatchTierRating, matched_entry_or_None)
        """
        # ADR-01: scope to this coach's entries only
        scoped = [e for e in archive if e.coach_id == self._coach_id]

        # PERFECT_MATCH: exact coping AND exact spt
        perfect = [
            e for e in scoped
            if e.coping_tier == target_coping and e.spt_stage == target_spt
        ]
        if perfect:
            return MatchTierRating.PERFECT_MATCH, perfect[0]

        # ADJACENT_MATCH: coping ±1 AND exact spt
        adjacent = [
            e for e in scoped
            if abs(e.coping_tier - target_coping) == 1 and e.spt_stage == target_spt
        ]
        if adjacent:
            return MatchTierRating.ADJACENT_MATCH, adjacent[0]

        # BASELINE_DEFAULT: no match
        return MatchTierRating.BASELINE_DEFAULT, None


# ══════════════════════════════════════════════════════════════════════
# Stage 2 — RelevanceStringencyGate
# ══════════════════════════════════════════════════════════════════════


class RelevanceStringencyGate:
    """
    Relevance Stringency Gate + MatchedTestimonialPayloadRow emission (§4 Stage 2).

    Gate verdicts:
      PERFECT_MATCH    → PASS        → testimonial text passed to compiler
      ADJACENT_MATCH   → PROVISIONAL → text passed + PROVISIONAL_ADJACENT metadata
      BASELINE_DEFAULT → FAIL_OMIT_REQUIRED → testimonial_text_raw=null, section disabled
    """

    def __init__(
        self,
        coach_id: str,
        receipt_chain: ReceiptChain | None = None,
    ) -> None:
        _validate_coach_id(coach_id)
        self._coach_id = coach_id
        self._rc = receipt_chain
        self._retriever = SocialProofRetriever(coach_id=coach_id)

    # ------------------------------------------------------------------

    def evaluate(
        self,
        target_client_id: str,
        target_coping: int,
        target_spt: int,
        archive: list[TestimonialArchiveEntry],
    ) -> MatchedTestimonialPayloadRow:
        """
        Full pipeline: segment filter → gate → matched payload row.

        Parameters
        ----------
        target_client_id:
            Prospect ID to link in the output row.
        target_coping:
            Coping position (1-5) from FR-CBCS-04.
        target_spt:
            SPT stage (1-5) from FR-CBCS-02.
        archive:
            Coach Story Archive (DEP-ENG-024) entries.

        Returns
        -------
        MatchedTestimonialPayloadRow (DEP-ENG-077)
        """
        # Stage 1 — Segment filtering
        match_tier, matched_entry = self._retriever.retrieve(
            target_client_id=target_client_id,
            target_coping=target_coping,
            target_spt=target_spt,
            archive=archive,
        )

        # Log retrieval receipt
        if self._rc is not None:
            self._rc.log(
                agent_id="social-proof-retriever",
                action="social-proof-retrieve",
                output_summary=(
                    f"client={target_client_id} coping={target_coping} "
                    f"spt={target_spt} tier={match_tier.value}"
                ),
            )

        # Stage 2 — Gate verdict
        gate_verdict = self._map_gate_verdict(match_tier)

        # FAIL_OMIT_REQUIRED → null out testimonial
        if gate_verdict == SocialProofGateVerdict.FAIL_OMIT_REQUIRED:
            testimonial_text = None
            record_id = None
        else:
            testimonial_text = matched_entry.testimonial_text if matched_entry else None
            record_id = matched_entry.record_id if matched_entry else None

        row = MatchedTestimonialPayloadRow(
            retrieval_id=str(uuid.uuid4()),
            target_client_id_linked=target_client_id,
            coach_id=self._coach_id,
            match_tier_rating=match_tier.value,
            gate_verdict=gate_verdict.value,
            testimonial_text_raw=testimonial_text,
            matched_historical_record_id=record_id,
            computation_timestamp=datetime.now(timezone.utc).isoformat(),
        )

        # Log gate receipt
        if self._rc is not None:
            self._rc.log(
                agent_id="social-proof-retriever",
                action="social-proof-gate",
                output_summary=(
                    f"client={target_client_id} verdict={gate_verdict.value} "
                    f"retrieval_id={row.retrieval_id}"
                ),
            )

        return row

    # ------------------------------------------------------------------

    @staticmethod
    def _map_gate_verdict(tier: MatchTierRating) -> SocialProofGateVerdict:
        """Map match tier to gate verdict (§4 Stage 2)."""
        if tier == MatchTierRating.PERFECT_MATCH:
            return SocialProofGateVerdict.PASS
        if tier == MatchTierRating.ADJACENT_MATCH:
            return SocialProofGateVerdict.PROVISIONAL
        return SocialProofGateVerdict.FAIL_OMIT_REQUIRED
