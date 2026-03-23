"""
FR30 — Tiered Dormancy Recovery Service (DEP-ENG-025)
4-tier recovery escalation: Day 3 → Day 5 → Day 10 → Day 30.

AC1: 3-day trigger for Tier 1.
AC2: Journaling suppression during RECOVERY_MODE.
AC3: Memory injection from stalled milestone + last L3 fear.
AC4: ADR-01 per-coach isolation.
"""

from __future__ import annotations

from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cross_system_models import (
    DORMANCY_ARTISAN_TOKEN_CAP,
    DORMANCY_THRESHOLDS_DAYS,
    DormancyRecoveryContext,
    DormancyRecoveryPayload,
    DormancyState,
    DormancyStateUpdate,
    DormancyTier,
)


# ── Tier → Day mapping ────────────────────────────────

TIER_DAY_MAP: dict[DormancyTier, int] = {
    DormancyTier.TIER_1: 3,
    DormancyTier.TIER_2: 5,
    DormancyTier.TIER_3: 10,
    DormancyTier.TIER_4: 30,
}

TIER_PROMPT_TEMPLATES: dict[DormancyTier, str] = {
    DormancyTier.TIER_1: (
        "Hey — just checking in. No pressure. "
        "Would you like to pick up where we left off? (yes/no)"
    ),
    DormancyTier.TIER_2: (
        "I noticed you've been away. Your goal of '{goal}' is still here. "
        "Want to refocus on it? (yes/no)"
    ),
    DormancyTier.TIER_3: (
        "It's been a while. Here's something different — "
        "what if we tried a completely new angle on '{goal}'?"
    ),
    DormancyTier.TIER_4: (
        "I want you to know the door is always open. "
        "If coaching isn't right for you right now, that's okay too. "
        "Would you like to pause your program?"
    ),
}

TIER_STATE_MAP: dict[DormancyTier, DormancyState] = {
    DormancyTier.TIER_1: DormancyState.RECOVERY_MODE_TIER_1,
    DormancyTier.TIER_2: DormancyState.RECOVERY_MODE_TIER_2,
    DormancyTier.TIER_3: DormancyState.RECOVERY_MODE_TIER_3,
    DormancyTier.TIER_4: DormancyState.RECOVERY_MODE_TIER_4,
}


class DormancyRecoveryService:
    """
    FR30: 4-tier dormancy recovery with journaling suppression.
    """

    def __init__(self, coach_acronym: str) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(f"coach_acronym must be 2-4 chars, got '{coach_acronym}'")
        self._coach = coach_acronym.upper()
        self._receipt_chain = ReceiptChain(coach_acronym=self._coach)

    # ── Tier Classification ────────────────────────────

    def classify_tier(self, days_silent: int) -> Optional[DormancyTier]:
        """
        FR30 AC1: Classify dormancy tier based on days silent.
        Returns None if below minimum threshold.
        """
        if days_silent >= 30:
            return DormancyTier.TIER_4
        elif days_silent >= 10:
            return DormancyTier.TIER_3
        elif days_silent >= 5:
            return DormancyTier.TIER_2
        elif days_silent >= 3:
            return DormancyTier.TIER_1
        return None

    # ── Recovery Payload Generation ────────────────────

    def generate_recovery_payload(
        self,
        *,
        user_id: str,
        days_silent: int,
        stalled_milestone: Optional[str] = None,
        last_l3_fear: Optional[str] = None,
        current_state: DormancyState = DormancyState.ACTIVE,
    ) -> Optional[DormancyRecoveryPayload]:
        """
        FR30 §5: Full recovery payload with context injection.
        Returns None if below dormancy threshold.
        """
        tier = self.classify_tier(days_silent)
        if tier is None:
            return None

        context = DormancyRecoveryContext(
            stalled_milestone=stalled_milestone,
            last_l3_fear=last_l3_fear,
        )

        new_state = TIER_STATE_MAP[tier]

        payload = DormancyRecoveryPayload(
            user_id=user_id,
            coach_id=self._coach,
            dormancy_tier=tier,
            days_silent=days_silent,
            recovery_context=context,
            pipeline_state_update=DormancyStateUpdate(
                previous_state=current_state,
                new_state=new_state,
                journaling_queue="PAUSED",
            ),
        )

        self._receipt_chain.log(
            agent_id="DormancyRecoveryService",
            action="RECOVERY_PAYLOAD_GENERATED",
            asset_id=f"DORMANCY-{user_id}",
            person_id=user_id,
            decision=f"TIER_{tier.value}",
            decision_rationale=f"days_silent={days_silent}, milestone={stalled_milestone}",
        )

        return payload

    # ── Journaling Suppression ─────────────────────────

    def is_journaling_suppressed(self, dormancy_state: DormancyState) -> bool:
        """
        FR30 AC2: Journaling is PAUSED when user enters any RECOVERY_MODE.
        """
        return dormancy_state in {
            DormancyState.RECOVERY_MODE_TIER_1,
            DormancyState.RECOVERY_MODE_TIER_2,
            DormancyState.RECOVERY_MODE_TIER_3,
            DormancyState.RECOVERY_MODE_TIER_4,
            DormancyState.CRISIS_HOLD,
        }

    # ── Prompt Generation ──────────────────────────────

    def generate_recovery_prompt(
        self,
        tier: DormancyTier,
        goal: str = "your goal",
    ) -> str:
        """
        FR30 §4.3: Artisan-capped recovery prompt (<50 tokens).
        """
        template = TIER_PROMPT_TEMPLATES[tier]
        return template.format(goal=goal)

    # ── Artisan Token Cap ──────────────────────────────

    @property
    def artisan_token_cap(self) -> int:
        """FR30 Stage 3: Artisan caps at 50 tokens."""
        return DORMANCY_ARTISAN_TOKEN_CAP
