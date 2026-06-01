"""
FR34 — V2WS Interactive Mode Service (DEP-ENG-029)
Step-and-Lock loop with Telegram-native approval gates.

AC1: Algorithmic stop (interrupt_before) after each module.
AC2: Revision routing back to Artisan on rejection.
AC3: Image embedding via DEP-ENG-031.
AC4: ADR-01 thread isolation per coach.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cross_system_models import (
    INTERACTIVE_STALE_TIMEOUT_HOURS,
    InteractiveModuleState,
    InteractivePhase,
    InteractiveV2WSState,
    WebinarModuleScript,
    WebinarPart,
)


# ── 5-Part Flow ───────────────────────────────────────
INTERACTIVE_FLOW_ORDER: list[WebinarPart] = [
    WebinarPart.HOOK,
    WebinarPart.PROBLEM_EXPANSION,
    WebinarPart.PARADIGM_SHIFT,
    WebinarPart.THE_METHOD,
    WebinarPart.THE_OFFER,
]


class V2WSInteractiveService:
    """
    FR34: Interactive Mode — step-and-lock webinar assembly.
    Each module requires coach approval before advancing.
    """

    def __init__(self, coach_acronym: str) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(f"coach_acronym must be 2-4 chars, got '{coach_acronym}'")
        self._coach = coach_acronym.upper()
        self._receipt_chain = ReceiptChain(coach_acronym=self._coach)
        self._sessions: dict[str, InteractiveV2WSState] = {}

    # ── Session Management ─────────────────────────────

    def create_session(self) -> InteractiveV2WSState:
        """
        FR34 §4.1: Initialize a new interactive V2WS session.
        """
        modules = [
            InteractiveModuleState(
                index=idx + 1,
                title=part.value,
            )
            for idx, part in enumerate(INTERACTIVE_FLOW_ORDER)
        ]

        state = InteractiveV2WSState(
            coach_id=self._coach,
            modules=modules,
        )
        self._sessions[state.session_id] = state

        self._receipt_chain.log(
            agent_id="V2WSInteractiveService",
            action="SESSION_CREATED",
            asset_id=state.session_id,
            decision="SUCCESS",
        )

        return state

    def get_session(self, session_id: str) -> Optional[InteractiveV2WSState]:
        return self._sessions.get(session_id)

    # ── Phase Transitions ──────────────────────────────

    def submit_outline(
        self,
        session_id: str,
        outline_text: str,
    ) -> InteractiveV2WSState:
        """
        FR34 §4.1: Submit SoC outline for approval.
        """
        state = self._get_session_or_raise(session_id)
        state.current_phase = InteractivePhase.WAITING_FOR_OUTLINE_APPROVAL

        self._receipt_chain.log(
            agent_id="V2WSInteractiveService",
            action="OUTLINE_SUBMITTED",
            asset_id=session_id,
            decision="AWAITING_APPROVAL",
        )

        return state

    def approve_outline(self, session_id: str) -> InteractiveV2WSState:
        """
        FR34 §4.2: Coach approves outline → move to module assembly.
        """
        state = self._get_session_or_raise(session_id)
        if state.current_phase != InteractivePhase.WAITING_FOR_OUTLINE_APPROVAL:
            raise ValueError(
                f"Cannot approve outline in phase {state.current_phase.value}"
            )
        state.outline_approved = True
        state.current_phase = InteractivePhase.MODULE_ASSEMBLY
        state.active_module_index = 1

        self._receipt_chain.log(
            agent_id="V2WSInteractiveService",
            action="OUTLINE_APPROVED",
            asset_id=session_id,
            decision="APPROVED",
        )

        return state

    # ── Module Step-and-Lock ───────────────────────────

    def submit_module(
        self,
        session_id: str,
        module_index: int,
        script_content: str,
    ) -> InteractiveV2WSState:
        """
        FR34 AC1: Submit module content → algorithmic stop.
        """
        state = self._get_session_or_raise(session_id)
        module = self._get_module_or_raise(state, module_index)

        module.script_content = script_content
        module.status = "PENDING_APPROVAL"
        state.current_phase = InteractivePhase.WAITING_FOR_MODULE_APPROVAL

        self._receipt_chain.log(
            agent_id="V2WSInteractiveService",
            action="MODULE_SUBMITTED",
            asset_id=session_id,
            decision="AWAITING_APPROVAL",
            decision_rationale=f"module_index={module_index}",
        )

        return state

    def approve_module(
        self,
        session_id: str,
        module_index: int,
    ) -> InteractiveV2WSState:
        """
        FR34 §4.2: Coach approves module → advance to next.
        """
        state = self._get_session_or_raise(session_id)
        module = self._get_module_or_raise(state, module_index)

        module.status = "APPROVED"

        # Advance to next module or complete
        next_index = module_index + 1
        if next_index <= len(state.modules):
            state.active_module_index = next_index
            state.current_phase = InteractivePhase.MODULE_ASSEMBLY
        else:
            state.current_phase = InteractivePhase.IMAGE_RECEIPT

        self._receipt_chain.log(
            agent_id="V2WSInteractiveService",
            action="MODULE_APPROVED",
            asset_id=session_id,
            decision="APPROVED",
            decision_rationale=f"module_index={module_index}, next={next_index}",
        )

        return state

    def reject_module(
        self,
        session_id: str,
        module_index: int,
        feedback: str = "",
    ) -> InteractiveV2WSState:
        """
        FR34 AC2: Coach rejects → revision routing back to Artisan.
        """
        state = self._get_session_or_raise(session_id)
        module = self._get_module_or_raise(state, module_index)

        module.status = "REVISION_REQUESTED"
        module.script_content = ""  # Clear for re-generation
        state.current_phase = InteractivePhase.MODULE_ASSEMBLY

        self._receipt_chain.log(
            agent_id="V2WSInteractiveService",
            action="MODULE_REJECTED",
            asset_id=session_id,
            decision="REVISION_REQUESTED",
            decision_rationale=f"module_index={module_index}, feedback={feedback[:200]}",
        )

        return state

    # ── Image Receipt ──────────────────────────────────

    def attach_image_to_module(
        self,
        session_id: str,
        module_index: int,
        base64_png: str,
    ) -> InteractiveV2WSState:
        """
        FR34 AC3: Attach transparent collage (DEP-ENG-031) image.
        """
        state = self._get_session_or_raise(session_id)
        module = self._get_module_or_raise(state, module_index)

        module.asset_base64 = base64_png

        self._receipt_chain.log(
            agent_id="V2WSInteractiveService",
            action="IMAGE_ATTACHED",
            asset_id=session_id,
            decision="SUCCESS",
            decision_rationale=f"module_index={module_index}",
        )

        return state

    # ── Compilation ────────────────────────────────────

    def mark_compilation_ready(
        self,
        session_id: str,
    ) -> InteractiveV2WSState:
        """
        FR34 §4.4: Mark session as ready for Excalidraw compilation.
        """
        state = self._get_session_or_raise(session_id)
        all_approved = all(m.status == "APPROVED" for m in state.modules)
        if not all_approved:
            raise ValueError("Not all modules are approved")

        state.excalidraw_payload_ready = True
        state.current_phase = InteractivePhase.COMPILATION

        self._receipt_chain.log(
            agent_id="V2WSInteractiveService",
            action="COMPILATION_READY",
            asset_id=session_id,
            decision="SUCCESS",
        )

        return state

    def complete_session(self, session_id: str) -> InteractiveV2WSState:
        """Mark session as complete."""
        state = self._get_session_or_raise(session_id)
        state.current_phase = InteractivePhase.COMPLETE

        self._receipt_chain.log(
            agent_id="V2WSInteractiveService",
            action="SESSION_COMPLETE",
            asset_id=session_id,
            decision="COMPLETE",
        )

        return state

    # ── Stale Sweep ────────────────────────────────────

    @property
    def stale_timeout_hours(self) -> int:
        """FR34 §5: 12-hour stale sweep."""
        return INTERACTIVE_STALE_TIMEOUT_HOURS

    # ── Internals ──────────────────────────────────────

    def _get_session_or_raise(self, session_id: str) -> InteractiveV2WSState:
        state = self._sessions.get(session_id)
        if state is None:
            raise ValueError(f"Session not found: {session_id}")
        return state

    @staticmethod
    def _get_module_or_raise(
        state: InteractiveV2WSState,
        module_index: int,
    ) -> InteractiveModuleState:
        for m in state.modules:
            if m.index == module_index:
                return m
        raise ValueError(f"Module index {module_index} not found")
