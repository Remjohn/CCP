"""
FR51 — Challenge Funnel Intelligence Builder
============================================
Compiles psychological inputs into a structured ChallengeFunnelBriefRow
(DEP-ENG-072) consumed by FR54 and FR59.

Classes
-------
ICTModeCalculator
    Resolves tribe modal coping position from a coping_position array,
    then derives challenge_duration_days and StructureFocus.

CommitmentDeviceGate
    Evaluates user_requested_price against thresholds and returns a
    CommitmentGateVerdict.  Hard-blocks FAIL_OVERPRICED > $17.

ChallengeFunnelArchitect
    Orchestrates both gates, binds lexicon anchors, and emits the
    ChallengeFunnelBriefRow with receipt chain entries.
"""

from __future__ import annotations

import statistics
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.ccp.models.cpsc_models import (
    ChallengeFunnelBriefRow,
    ChallengeFunnelError,
    CommitmentGateVerdict,
    StructureFocus,
)
from src.ccp.core.receipt_chain import ReceiptChain

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Stage 2 commitment price thresholds (§4)
COMMITMENT_PRICE_MIN: float = 1.0
COMMITMENT_PRICE_MAX: float = 17.0

# flyer_hook_text word-count hard limit (§4 Phase 3)
FLYER_HOOK_MAX_WORDS: int = 6

# ICT mode threshold — coping position ≤ this → 5-day funnel (§4 Stage 1)
ICT_SHORT_FUNNEL_THRESHOLD: int = 2


# ---------------------------------------------------------------------------
# ICTModeCalculator
# ---------------------------------------------------------------------------

class ICTModeCalculator:
    """
    Resolves challenge duration and structure focus from a tribe's
    coping_position array using the statistical mode.

    Parameters
    ----------
    coping_positions : list[int]
        Array of individual coping position integers from DEP-ENG-058.

    Raises
    ------
    ValueError(ChallengeFunnelError.EMPTY_COPING_ARRAY)
        If the supplied array is empty.
    """

    def __init__(self, coping_positions: list[int]) -> None:
        if not coping_positions:
            raise ValueError(ChallengeFunnelError.EMPTY_COPING_ARRAY)
        self._positions = coping_positions

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def modal_position(self) -> int:
        """Return the statistical mode of the coping_position array.

        When multiple modes exist, ``statistics.mode`` returns the first
        encountered (lowest) value — consistent with a conservative
        "shorter-is-safer" bias.
        """
        return statistics.mode(self._positions)

    def resolve(self) -> tuple[int, StructureFocus]:
        """Return ``(challenge_duration_days, StructureFocus)``.

        Resolution rule (§4 Stage 1):
        - modal ≤ 2  → 5 days, 5_DAY_MOMENTUM
        - modal ≥ 3  → 7 days, 7_DAY_IDENTITY
        """
        modal = self.modal_position()
        if modal <= ICT_SHORT_FUNNEL_THRESHOLD:
            return 5, StructureFocus.FIVE_DAY_MOMENTUM
        return 7, StructureFocus.SEVEN_DAY_IDENTITY


# ---------------------------------------------------------------------------
# CommitmentDeviceGate
# ---------------------------------------------------------------------------

class CommitmentDeviceGate:
    """
    Validates the operator-supplied challenge price against the commitment
    device thresholds derived from hyperbolic discounting research (§4 Stage 2).

    Parameters
    ----------
    user_requested_price : float
        Price supplied by the operator dashboard.
    """

    def __init__(self, user_requested_price: float) -> None:
        self._price = user_requested_price

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def evaluate(self) -> CommitmentGateVerdict:
        """Return the gate verdict for the supplied price.

        - price == 0            → PROVISIONAL_FREE_ACCEPTED
        - 1 ≤ price ≤ 17       → PASS
        - price > 17            → FAIL_OVERPRICED
        - price < 0             → FAIL_OVERPRICED (invalid negative)
        """
        p = self._price
        if p == 0.0:
            return CommitmentGateVerdict.PROVISIONAL_FREE_ACCEPTED
        if COMMITMENT_PRICE_MIN <= p <= COMMITMENT_PRICE_MAX:
            return CommitmentGateVerdict.PASS
        # > 17 or negative
        return CommitmentGateVerdict.FAIL_OVERPRICED


# ---------------------------------------------------------------------------
# ChallengeFunnelArchitect
# ---------------------------------------------------------------------------

class ChallengeFunnelArchitect:
    """
    Orchestrates FR51: resolves ICT mode, evaluates commitment gate, binds
    character lexicon anchors, and returns a ``ChallengeFunnelBriefRow``.

    Parameters
    ----------
    coach_id : str
        ADR-01 boundary key — all output is scoped to this coach.
    receipt_chain : ReceiptChain
        Live receipt chain for DEP-ENG-041 cryptographic logging.
    """

    _AGENT_ID = "challenge-funnel-architect"

    def __init__(self, coach_id: str, receipt_chain: ReceiptChain) -> None:
        if not isinstance(coach_id, str) or len(coach_id) < 2:
            raise ValueError("coach_id must be a non-empty string (min 2 chars).")
        self._coach_id = coach_id
        self._rc = receipt_chain

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def compile_brief(
        self,
        *,
        coping_positions: list[int],
        character_lexicon: dict[str, Any],
        user_requested_price: float,
        flyer_hook_text: str,
    ) -> ChallengeFunnelBriefRow:
        """
        Compile and return a ``ChallengeFunnelBriefRow``.

        Parameters
        ----------
        coping_positions : list[int]
            Tribe ICT aggregate coping_position array (DEP-ENG-058).
        character_lexicon : dict
            Must contain keys ``"category_1_heroes"`` (list) and
            ``"category_4_enemies"`` (list).  Index 0 of each is used.
        user_requested_price : float
            Operator-supplied challenge price.
        flyer_hook_text : str
            Hook text for the funnel flyer — MUST be ≤ 6 words.

        Returns
        -------
        ChallengeFunnelBriefRow

        Raises
        ------
        ValueError(ChallengeFunnelError.MISSING_TRIBAL_ANCHOR)
            If ``character_lexicon["category_1_heroes"]`` is null/empty.
        ValueError(ChallengeFunnelError.LEXICON_KEY_MISSING)
            If required lexicon keys are absent.
        ValueError(ChallengeFunnelError.FAIL_OVERPRICED)
            If commitment gate returns FAIL_OVERPRICED (hard abort).
        ValueError(ChallengeFunnelError.EMPTY_COPING_ARRAY)
            If coping_positions is empty.
        """
        # ── Stage 1: ICT Mode Resolution ──────────────────────────────
        calc = ICTModeCalculator(coping_positions)
        modal = calc.modal_position()
        duration, focus = calc.resolve()

        root_receipt = self._rc.log(
            agent_id=self._AGENT_ID,
            action="challenge-ict-resolve",
            output_summary=(
                f"coach={self._coach_id} modal_coping={modal} "
                f"duration={duration} focus={focus.value}"
            ),
        )

        # ── Lexicon Binding ───────────────────────────────────────────
        try:
            heroes: list[str] = character_lexicon["category_1_heroes"]
            enemies: list[str] = character_lexicon["category_4_enemies"]
        except KeyError as exc:
            raise ValueError(ChallengeFunnelError.LEXICON_KEY_MISSING) from exc

        if not heroes:
            raise ValueError(ChallengeFunnelError.MISSING_TRIBAL_ANCHOR)
        if not enemies:
            raise ValueError(ChallengeFunnelError.LEXICON_KEY_MISSING)

        hero_anchor = heroes[0]
        enemy_contrast = enemies[0]

        # ── flyer_hook_text word-count enforcement ────────────────────
        hook_words = len(flyer_hook_text.split())
        if hook_words > FLYER_HOOK_MAX_WORDS:
            raise ValueError(
                f"flyer_hook_text exceeds {FLYER_HOOK_MAX_WORDS} words "
                f"({hook_words} words supplied)."
            )

        # ── Stage 2: Commitment Device Gate ───────────────────────────
        gate = CommitmentDeviceGate(user_requested_price)
        verdict = gate.evaluate()

        if verdict == CommitmentGateVerdict.FAIL_OVERPRICED:
            # Hard abort — log before raising
            self._rc.log(
                agent_id=self._AGENT_ID,
                action="challenge-gate-evaluate",
                output_summary=(
                    f"coach={self._coach_id} price={user_requested_price} "
                    f"verdict=FAIL_OVERPRICED — generation aborted"
                ),
                parent_receipt_id=root_receipt.receipt_id,
            )
            raise ValueError(ChallengeFunnelError.FAIL_OVERPRICED)

        locked_price = user_requested_price

        gate_receipt = self._rc.log(
            agent_id=self._AGENT_ID,
            action="challenge-gate-evaluate",
            output_summary=(
                f"coach={self._coach_id} price={locked_price} "
                f"verdict={verdict.value}"
            ),
            parent_receipt_id=root_receipt.receipt_id,
        )

        # ── Assemble output ───────────────────────────────────────────
        return ChallengeFunnelBriefRow(
            funnel_blueprint_id=str(uuid.uuid4()),
            coach_id=self._coach_id,
            challenge_duration_days=duration,
            structure_focus=focus.value,
            commitment_price=locked_price,
            hero_anchor_noun=hero_anchor,
            enemy_contrast_noun=enemy_contrast,
            flyer_hook_text=flyer_hook_text,
            gate_verdict=verdict.value,
            generated_at=datetime.now(timezone.utc).isoformat(),
        )
