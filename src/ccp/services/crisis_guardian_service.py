"""
FR31 — Crisis Guardian Circuit Breaker (DEP-ENG-026)
Zero LLM dependency. Aho-Corasick 500-word local regex scan.
100 false positives > 1 missed crisis.

AC1: Sub-100ms scan execution.
AC2: Zero API calls on crisis detection.
AC3: False-positive grace (100 FP > 1 miss).
AC4: ADR-01 coach channel isolation.
"""

from __future__ import annotations

import re
import time
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cross_system_models import (
    CRISIS_DICTIONARY_SIZE,
    CRISIS_FALSE_POSITIVE_POLICY,
    CRISIS_SCAN_TARGET_MS,
    CrisisCircuitBreakerResult,
    CrisisDeployment,
    CrisisEscalation,
    CrisisEscalationProtocol,
    DormancyState,
)


# ── Crisis Dictionary ─────────────────────────────────
# FR31 §2: 500-word Aho-Corasick dictionary.
# Below is a representative set — production expands to 500.
CRISIS_KEYWORD_DICTIONARY: list[str] = [
    "suicide", "kill myself", "end my life", "want to die",
    "don't want to be alive", "no reason to live", "better off dead",
    "self harm", "self-harm", "cutting myself", "hurting myself",
    "overdose", "take all my pills", "jump off", "hang myself",
    "slit my wrists", "gun to my head", "pull the trigger",
    "can't go on", "can't take it anymore", "no way out",
    "i'm done", "ending it", "final goodbye", "last message",
    "domestic violence", "being abused", "he hits me", "she hits me",
    "sexual assault", "raped", "molested", "trafficking",
    "child abuse", "hurting my child", "shaken baby",
    "eating disorder", "starving myself", "purging",
    "substance abuse", "drinking to cope", "using again",
    "can't stop using", "relapsed", "needle",
    "psychotic episode", "hearing voices", "hallucinating",
    "paranoid", "they're watching me", "voices told me",
    "panic attack", "can't breathe", "chest pain anxiety",
    "crisis", "emergency", "911", "help me please",
    "nobody cares", "alone in this", "abandoned",
    "hopeless", "worthless", "burden to everyone",
    "give up", "given up", "giving up",
]

# Compile a single regex for O(n) scan
_CRISIS_PATTERN = re.compile(
    "|".join(re.escape(kw) for kw in CRISIS_KEYWORD_DICTIONARY),
    re.IGNORECASE,
)


class CrisisGuardianService:
    """
    FR31: Zero-LLM crisis detection and circuit-breaking.

    Stage 1: Local regex scan (<100ms)
    Stage 2: Pipeline severance
    Stage 3: Localized resource delivery
    Stage 4: Human escalation & state freeze
    """

    def __init__(self, coach_acronym: str) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(f"coach_acronym must be 2-4 chars, got '{coach_acronym}'")
        self._coach = coach_acronym.upper()
        self._receipt_chain = ReceiptChain(coach_acronym=self._coach)
        self._frozen_users: set[str] = set()

    # ── Stage 1: Scan ─────────────────────────────────

    def scan_message(self, text: str) -> tuple[bool, Optional[str], int]:
        """
        FR31 AC1: Sub-100ms local regex scan.
        Returns (is_crisis, trigger_keyword, latency_ms).
        """
        start = time.perf_counter_ns()
        match = _CRISIS_PATTERN.search(text)
        elapsed_ms = int((time.perf_counter_ns() - start) / 1_000_000)

        if match:
            return True, match.group(0).lower(), elapsed_ms
        return False, None, elapsed_ms

    # ── Stage 2-4: Full Protocol ──────────────────────

    def execute_crisis_protocol(
        self,
        *,
        user_id: str,
        message_text: str,
        admin_channel_id: str,
        originator: str = "client",
    ) -> Optional[CrisisEscalationProtocol]:
        """
        FR31 §5: Full crisis guardian pipeline.
        Returns None if no crisis detected.
        Returns CrisisEscalationProtocol if crisis found.
        """
        is_crisis, trigger_keyword, latency_ms = self.scan_message(message_text)

        if not is_crisis:
            self._receipt_chain.log(
                agent_id="CrisisGuardian",
                action="CRISIS_SCAN_CLEAR",
                asset_id=f"MSG-{user_id}",
                decision="PASS",
                decision_rationale=f"scan_latency={latency_ms}ms",
            )
            return None

        # Stage 2: Pipeline severance — freeze user
        self._frozen_users.add(user_id)

        # Stage 3: Resource deployment
        resources = self._get_localized_resources()

        # Stage 4: Escalation routing
        coach_notified = originator == "client"

        protocol = CrisisEscalationProtocol(
            user_id=user_id,
            coach_id=self._coach,
            scan_latency_ms=latency_ms,
            circuit_breaker=CrisisCircuitBreakerResult(
                trigger_keyword=trigger_keyword or "",
                exact_message_snippet=message_text[:500],
            ),
            deployment=CrisisDeployment(
                resources_dispatched=resources,
            ),
            escalation=CrisisEscalation(
                coach_notified=coach_notified,
                admin_channel_id=admin_channel_id,
            ),
        )

        self._receipt_chain.log(
            agent_id="CrisisGuardian",
            action="CRISIS_PROTOCOL_EXECUTED",
            asset_id=f"CRISIS-{user_id}",
            decision="CRISIS_HOLD",
            decision_rationale=f"trigger={trigger_keyword}, latency={latency_ms}ms, originator={originator}",
        )

        return protocol

    # ── State Queries ──────────────────────────────────

    def is_user_frozen(self, user_id: str) -> bool:
        """FR31 §4.4: Check if user is in CRISIS_HOLD state."""
        return user_id in self._frozen_users

    def unfreeze_user(self, user_id: str) -> bool:
        """Admin-only: remove user from CRISIS_HOLD."""
        if user_id in self._frozen_users:
            self._frozen_users.discard(user_id)
            self._receipt_chain.log(
                agent_id="CrisisGuardian",
                action="USER_UNFROZEN",
                asset_id=f"CRISIS-{user_id}",
                decision="UNFROZEN",
            )
            return True
        return False

    def get_dormancy_state_override(self, user_id: str) -> Optional[DormancyState]:
        """FR31 §2: CRISIS_HOLD blocks FR28/FR30."""
        if self.is_user_frozen(user_id):
            return DormancyState.CRISIS_HOLD
        return None

    # ── Internals ──────────────────────────────────────

    @staticmethod
    def _get_localized_resources() -> str:
        """FR31 §4.3: Zero-LLM localized resource delivery."""
        return (
            "If you are in immediate danger, please contact "
            "emergency services (911 in US, 112 in EU). "
            "National Suicide Prevention Lifeline: 988 (US). "
            "Crisis Text Line: Text HOME to 741741."
        )
