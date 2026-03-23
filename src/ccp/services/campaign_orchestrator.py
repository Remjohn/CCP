"""
FR59 — Campaign Orchestration Agent
=====================================
Master timeline governor that binds FR51-FR58 generative units into a
cohesive execution pipeline.

Critical architectural constraint: campaigns are **operator-triggered only**.
The Orchestrator rejects any non-human / non-admin launch attempt.

Classes
-------
CampaignStateResolver
    Derives the current MasterCampaignState enum value from the offset
    (in days) between the campaign start date and now.

CampaignInitializationGate
    Enforces the 3-condition operator authorization check before any
    campaign is permitted to launch.

CampaignOrchestrator
    Orchestrates both stages, assembles CampaignExecutionLogRow, and
    writes receipt chain entries (DEP-ENG-041).
"""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from typing import Any

from src.ccp.models.cpsc_models import (
    CampaignExecutionLogRow,
    CampaignGateVerdict,
    CampaignOrchestrationError,
    MasterCampaignState,
)
from src.ccp.core.receipt_chain import ReceiptChain

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Day thresholds for campaign state machine (§4 Stage 1)
ANCHOR_WINDOW_START_DAYS: float = 0.0     # launch day
ANCHOR_WINDOW_END_DAYS: float = 3.0       # ANCHORING → end of Day 3
CONVERSION_WINDOW_END_DAYS: float = 7.0   # CONVERSION → end of Day 7
# > Day 7 → COOLDOWN_RESOLVED

# Commercial URL detection pattern (§7 Task 3 / §10 safety test)
_COMMERCIAL_URL_PATTERN = re.compile(
    r"https?://\S+|www\.\S+",
    re.IGNORECASE,
)

# RBAC: only these role values are treated as human-admin operators (§4 Stage 2)
ADMIN_ROLES: frozenset[str] = frozenset({"admin", "operator", "coach_admin"})

# Sentinel for legacy / CSV broadcasts (no FR51/52 brief linked)
LEGACY_BRIEF_SENTINEL: int = -1


# ---------------------------------------------------------------------------
# CampaignStateResolver
# ---------------------------------------------------------------------------

class CampaignStateResolver:
    """
    Resolves MasterCampaignState from elapsed campaign days.

    Parameters
    ----------
    days_since_launch : float
        Number of days elapsed since the scheduled campaign start.
        Negative value → campaign has not started yet → QUEUED.
    """

    def __init__(self, days_since_launch: float) -> None:
        self._days = days_since_launch

    def resolve(self) -> MasterCampaignState:
        d = self._days
        if d < ANCHOR_WINDOW_START_DAYS:
            return MasterCampaignState.QUEUED_PENDING_LAUNCH
        if d <= ANCHOR_WINDOW_END_DAYS:
            return MasterCampaignState.ANCHORING_DAY_1_TO_3
        if d <= CONVERSION_WINDOW_END_DAYS:
            return MasterCampaignState.CONVERSION_WINDOW_ACTIVE
        return MasterCampaignState.COOLDOWN_RESOLVED


# ---------------------------------------------------------------------------
# CampaignInitializationGate
# ---------------------------------------------------------------------------

class CampaignInitializationGate:
    """
    Validates three conditions before campaign launch (§4 Stage 2):

    Condition 1 — caller_role must be in ADMIN_ROLES (human operator only).
    Condition 2 — roster_size > 0 (non-empty FR58 approved roster).
    Condition 3 — brief_id is not LEGACY_BRIEF_SENTINEL (linked FR51/52 brief).

    Gate outcomes
    -------------
    PASS_AUTHORIZED       : all 3 conditions pass.
    PROVISIONAL_LEGACY    : conditions 1 & 2 pass, condition 3 fails (legacy CSV).
    FAIL_ABORTED          : condition 1 or condition 2 fails (hard abort).
    """

    def __init__(
        self,
        caller_role: str,
        roster_size: int,
        brief_id: Any,
    ) -> None:
        self._role = caller_role
        self._roster = roster_size
        self._brief_id = brief_id

    def evaluate(self) -> CampaignGateVerdict:
        # Condition 1: admin role check
        cond_1 = self._role in ADMIN_ROLES
        # Condition 2: non-zero roster
        cond_2 = self._roster > 0
        # Condition 3: linked brief (not legacy sentinel)
        cond_3 = self._brief_id != LEGACY_BRIEF_SENTINEL

        if not cond_1 or not cond_2:
            return CampaignGateVerdict.FAIL_ABORTED
        if not cond_3:
            return CampaignGateVerdict.PROVISIONAL_LEGACY_MODE
        return CampaignGateVerdict.PASS_AUTHORIZED


# ---------------------------------------------------------------------------
# Commercial URL sanitiser (§7 Task 3)
# ---------------------------------------------------------------------------

def strip_commercial_urls(payload_text: str) -> str:
    """
    Remove all http/https/www URLs from a payload string.

    Used during ANCHORING_DAY_1_TO_3 to prevent early commercial leakage
    (§7 Task 3 / §10 URL-stripping safety test).
    """
    return _COMMERCIAL_URL_PATTERN.sub("", payload_text).strip()


def payload_contains_commercial_url(payload_text: str) -> bool:
    """Return True if the payload contains a commercial URL pattern."""
    return bool(_COMMERCIAL_URL_PATTERN.search(payload_text))


# ---------------------------------------------------------------------------
# CampaignOrchestrator
# ---------------------------------------------------------------------------

class CampaignOrchestrator:
    """
    Orchestrates FR59: resolves campaign state, runs the initialization
    gate, and returns a CampaignExecutionLogRow.

    Parameters
    ----------
    coach_id : str
        ADR-01 boundary key.
    receipt_chain : ReceiptChain
        Live receipt chain (DEP-ENG-041).
    """

    _AGENT_ID = "campaign-orchestration-agent"

    def __init__(self, coach_id: str, receipt_chain: ReceiptChain) -> None:
        if not isinstance(coach_id, str) or len(coach_id) < 2:
            raise ValueError("coach_id must be a non-empty string (min 2 chars).")
        self._coach_id = coach_id
        self._rc = receipt_chain

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def launch(
        self,
        *,
        campaign_blueprint_id: str,
        operator_auth_id: str,
        caller_role: str,
        roster: list[Any],
        brief_id: Any,
        days_since_launch: float = 0.0,
    ) -> CampaignExecutionLogRow:
        """
        Attempt to launch (or evaluate) a campaign and return a log row.

        Parameters
        ----------
        campaign_blueprint_id : str
            UUID linking to FR51/52 brief.
        operator_auth_id : str
            Caller's identity from the Telegram / UI context.
        caller_role : str
            RBAC role of the caller (must be in ADMIN_ROLES to pass).
        roster : list
            FR58-approved client UUIDs. Length becomes roster_size_at_launch.
        brief_id : Any
            FR51/52 brief ID. -1 (LEGACY_BRIEF_SENTINEL) → PROVISIONAL.
        days_since_launch : float
            Days elapsed since scheduled start date (default 0 = launch day).

        Returns
        -------
        CampaignExecutionLogRow

        Raises
        ------
        ValueError(CampaignOrchestrationError.FAIL_ABORTED)
            If gate verdict is FAIL_ABORTED (receipt logged before raising).
        """
        roster_size = len(roster)

        # ── Stage 1: Campaign State Resolution ──────────────────────
        state = CampaignStateResolver(days_since_launch).resolve()

        root_receipt = self._rc.log(
            agent_id=self._AGENT_ID,
            action="campaign-state-resolve",
            output_summary=(
                f"coach={self._coach_id} campaign={campaign_blueprint_id} "
                f"days={days_since_launch} state={state.value}"
            ),
        )

        # ── Stage 2: Campaign Initialization Gate ────────────────────
        gate = CampaignInitializationGate(caller_role, roster_size, brief_id)
        verdict = gate.evaluate()

        if verdict == CampaignGateVerdict.FAIL_ABORTED:
            self._rc.log(
                agent_id=self._AGENT_ID,
                action="campaign-init-gate",
                output_summary=(
                    f"coach={self._coach_id} operator={operator_auth_id} "
                    f"role={caller_role} roster={roster_size} "
                    "verdict=FAIL_ABORTED — unauthorized or zero roster"
                ),
                parent_receipt_id=root_receipt.receipt_id,
            )
            raise ValueError(CampaignOrchestrationError.FAIL_ABORTED)

        self._rc.log(
            agent_id=self._AGENT_ID,
            action="campaign-init-gate",
            output_summary=(
                f"coach={self._coach_id} operator={operator_auth_id} "
                f"roster={roster_size} verdict={verdict.value}"
            ),
            parent_receipt_id=root_receipt.receipt_id,
        )

        return CampaignExecutionLogRow(
            execution_run_id=str(uuid.uuid4()),
            campaign_blueprint_id=campaign_blueprint_id,
            coach_id=self._coach_id,
            operator_auth_id=operator_auth_id,
            master_campaign_state=state.value,
            gate_verdict=verdict.value,
            roster_size_at_launch=roster_size,
            started_at=datetime.now(timezone.utc).isoformat(),
        )
