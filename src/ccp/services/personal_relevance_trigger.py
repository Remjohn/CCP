"""
FR-CBCS-03 — Personal Relevance Trigger
=========================================
Identity Profile Synthesis + Identity-First Trigger Gate validation.

Spec ref: FR_CBCS_03_Personal_Relevance_Trigger_Tech_Spec.md
"""

from __future__ import annotations

import re
from datetime import datetime, timezone

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    BEHAVIORAL_PATTERNS,
    DEFENSE_FALLBACK,
    DEFENSE_MECHANISM_MAP,
    IDENTITY_PATTERNS,
    PRIMARY_DRIVER_FALLBACK,
    EmotionalArchitecture,
    IdentityTargetingVerdict,
    IdentityTriggerVerdict,
    PersonalRelevanceError,
    UnifiedIdentityProfile,
)


class IdentityProfileBuilder:
    """Synthesizes a Unified Identity Profile from upstream data streams.

    Parameters
    ----------
    coach_acronym : str
        2-4 character coach identifier (ADR-01).
    receipt_chain : ReceiptChain
        Immutable audit trail.
    """

    def __init__(self, coach_acronym: str, receipt_chain: ReceiptChain) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(PersonalRelevanceError.INVALID_COACH_SCOPE.value)
        self._coach = coach_acronym
        self._rc = receipt_chain

    # ── Stage 1 + 2: Synthesis ─────────────────────────────────────────

    def synthesize(
        self,
        client_id: str,
        coach_id: str,
        emotional_dna_dominant_theme: str | None = None,
        coping_primary_defense: str | None = None,
        moral_primary: str | None = None,
        highest_intensity_score: float | None = None,
    ) -> UnifiedIdentityProfile:
        """Build a Unified Identity Profile from upstream data.

        Parameters
        ----------
        client_id : str
            Unique client identifier.
        coach_id : str
            Coach boundary (ADR-01).
        emotional_dna_dominant_theme : str | None
            From FR4 Emotional DNA. Null → fallback "Autonomy".
        coping_primary_defense : str | None
            From FR12. Null → fallback "General Resistance".
        moral_primary : str | None
            From FR12 Moral Foundations. Null → fallback "growth".
        highest_intensity_score : float | None
            Max liwc_intensity_score from change_talk_archive.

        Returns
        -------
        UnifiedIdentityProfile
        """
        # Stage 2: Variable resolution
        primary_driver = emotional_dna_dominant_theme or PRIMARY_DRIVER_FALLBACK
        defense_mechanism = DEFENSE_MECHANISM_MAP.get(
            coping_primary_defense or "", DEFENSE_FALLBACK
        )
        moral = moral_primary or "growth"
        intensity_str = (
            f"{highest_intensity_score:.2f}"
            if highest_intensity_score is not None
            else "0.00"
        )

        # Core identity statement template (§4 Stage 2)
        core_statement = (
            f"Someone who values {moral} but struggles with "
            f"{defense_mechanism} when their {primary_driver} is threatened."
        )

        profile = UnifiedIdentityProfile(
            client_id=client_id,
            coach_id=coach_id,
            core_identity_statement=core_statement,
            emotional_architecture=EmotionalArchitecture(
                primary_driver=primary_driver,
                defense_mechanism=defense_mechanism,
            ),
            highest_intensity_change_talk=intensity_str,
            last_synthesized=datetime.now(timezone.utc).isoformat(),
        )

        self._rc.log(
            agent_id="identity-profile-builder",
            action="identity-synthesize",
            person_id=client_id,
            input_summary=(
                f"e_dna={'present' if emotional_dna_dominant_theme else 'null'}, "
                f"coping={'present' if coping_primary_defense else 'null'}, "
                f"moral={'present' if moral_primary else 'null'}"
            ),
            output_summary=f"driver={primary_driver}, defense={defense_mechanism}",
        )
        return profile


class CentralRouteTriggerValidator:
    """Validates draft campaign copy against the Identity-First Trigger Gate.

    Parameters
    ----------
    coach_acronym : str
        2-4 character coach identifier (ADR-01).
    receipt_chain : ReceiptChain
        Immutable audit trail.
    """

    def __init__(self, coach_acronym: str, receipt_chain: ReceiptChain) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(PersonalRelevanceError.INVALID_COACH_SCOPE.value)
        self._coach = coach_acronym
        self._rc = receipt_chain
        # Precompile
        self._behavioral_re = [
            re.compile(p, re.IGNORECASE) for p in BEHAVIORAL_PATTERNS
        ]
        self._identity_re = [
            re.compile(p, re.IGNORECASE) for p in IDENTITY_PATTERNS
        ]

    # ── Stage 3: Trigger Validation ────────────────────────────────────

    def validate(
        self,
        draft_text: str,
        primary_driver: str | None = None,
    ) -> IdentityTargetingVerdict:
        """Evaluate draft campaign copy against Identity-First Trigger Gate.

        Parameters
        ----------
        draft_text : str
            Draft campaign/conversion message text.
        primary_driver : str | None
            Client's primary driver for rewrite instruction.

        Returns
        -------
        IdentityTargetingVerdict
        """
        behavioral_matches = self._find_behavioral_matches(draft_text)
        behavioral_count = len(behavioral_matches)
        identity_count = self._count_identity_matches(draft_text)

        # Gate evaluation (§4 Stage 3)
        if behavioral_count == 0 and identity_count >= 1:
            verdict = IdentityTriggerVerdict.PASS
            is_valid = True
            rewrite = None
        elif behavioral_count > 0 and identity_count >= 1:
            verdict = IdentityTriggerVerdict.PROVISIONAL
            is_valid = False
            driver = primary_driver or PRIMARY_DRIVER_FALLBACK
            rewrite = (
                f"Remove behavioral markers: {behavioral_matches}. "
                f"Focus on identity trait: {driver}"
            )
        else:
            # behavioral > 0 AND identity == 0 → FAIL
            # OR behavioral == 0 AND identity == 0 → also FAIL (no identity)
            verdict = IdentityTriggerVerdict.FAIL
            is_valid = False
            driver = primary_driver or PRIMARY_DRIVER_FALLBACK
            rewrite = (
                f"Remove behavioral markers: {behavioral_matches}. "
                f"Focus on identity trait: {driver}"
            ) if behavioral_count > 0 else (
                f"Add identity-first framing targeting: {driver}"
            )

        result = IdentityTargetingVerdict(
            is_valid=is_valid,
            verdict=verdict.value,
            rewrite_instruction=rewrite,
            rejected_behavioral_phrases=behavioral_matches,
        )

        self._rc.log(
            agent_id="central-route-trigger-validator",
            action="identity-trigger-validate",
            input_summary=(
                f"behavioral_count={behavioral_count}, "
                f"identity_count={identity_count}"
            ),
            output_summary=f"verdict={verdict.value}, is_valid={is_valid}",
        )
        return result

    # ── Regex Matching ─────────────────────────────────────────────────

    def _find_behavioral_matches(self, text: str) -> list[str]:
        """Find all behavioral pattern matches in text, returning matched strings."""
        matches: list[str] = []
        for pattern in self._behavioral_re:
            for m in pattern.finditer(text):
                matches.append(m.group())
        return matches

    def _count_identity_matches(self, text: str) -> int:
        """Count identity pattern matches in text."""
        count = 0
        for pattern in self._identity_re:
            count += len(pattern.findall(text))
        return count
