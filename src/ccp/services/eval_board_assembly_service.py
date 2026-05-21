"""
FR-ERA3-35C Eval Board Assembly Service
=======================================
Assembles premium, screenshot-ready card boards validating layout, density, and role boundaries.
"""

from __future__ import annotations

import uuid
from typing import List, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.phase0_eval_card_models import (
    EvalCard,
    EvalCardBoard,
    EvalBoardLayout,
    EvalBoardKind,
    EvalCardRole,
    BoardDensity
)


class EvalBoardAssemblyService:
    """Orchestrates grouping of premium cards into screenshot-ready share surfaces."""

    def __init__(self, coach_acronym: str = "NDL", log_dir: Optional[str] = None):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym, log_dir=log_dir)

    def assemble_board(
        self,
        report_id: str,
        board_kind: EvalBoardKind,
        cards: List[EvalCard],
        title: str,
        subtitle: Optional[str] = None,
        density: BoardDensity = BoardDensity.standard,
        columns: Optional[int] = None,
        featured_card_id: Optional[str] = None
    ) -> EvalCardBoard:
        """
        Assembles a list of cards into a configured EvalCardBoard.
        Enforces structural layout constraints and order laws.
        """
        # 1. Structural Validations (Failure tests: 10.7)
        if not cards:
            raise ValueError("Board creation failed: Board must contain at least one card.")

        # Resolve columns with default layouts based on board type
        if columns is None:
            if board_kind == EvalBoardKind.single_card_detail:
                resolved_columns = 1
            elif board_kind == EvalBoardKind.before_after_comparison:
                resolved_columns = 2
            elif board_kind == EvalBoardKind.audit_spread:
                resolved_columns = 3
            else:
                resolved_columns = 2
        else:
            if columns < 1 or columns > 6:
                raise ValueError("Board layout column constraint violated: must be between 1 and 6.")
            resolved_columns = columns

        # 2. Ordering Law (Phase 3 task 21 - before/after ordering)
        if board_kind == EvalBoardKind.before_after_comparison:
            # Order before_snapshot first, then after_snapshot
            cards = sorted(
                cards,
                key=lambda c: 0 if c.face.role == EvalCardRole.before_snapshot else 1
            )

        card_order = [c.card_id for c in cards]

        # 3. Create Share Caption and Summary Line (AC-7)
        scores_list = [c.face.overall_score for c in cards]
        avg_score = int(sum(scores_list) / len(scores_list))
        
        summary_line = (
            f"Overall communication signal alignment stands at {avg_score}/99 "
            f"across {len(cards)} evaluated channels."
        )

        share_caption = (
            f"Behold my CCP Communication Signal Board! Average Score: {avg_score}/99. "
            "Built with human expression refinement technology. #CCP #ConsciousCoaching"
        )

        layout = EvalBoardLayout(
            board_kind=board_kind,
            density=density,
            columns=resolved_columns,
            featured_card_id=featured_card_id,
            card_order=card_order,
            screenshot_safe=True
        )

        board_id = f"BRD-{uuid.uuid4().hex[:8].upper()}"

        board = EvalCardBoard(
            board_id=board_id,
            report_id=report_id,
            board_kind=board_kind,
            title=title,
            subtitle=subtitle,
            cards=cards,
            layout=layout,
            summary_line=summary_line,
            share_caption=share_caption
        )

        # 4. Log state mutation via Receipt Chain (Gate 4)
        self.receipt_chain.log(
            agent_id="eval_board_assembly_service",
            action="assemble_eval_board",
            asset_id=board.board_id,
            person_id=cards[0].face.title.split(" — ")[-1],
            input_summary=f"Assembling {board_kind.value} board with {len(cards)} cards",
            output_summary=f"Board assembled successfully. Avg Score={avg_score}",
            decision="approved",
            metadata={
                "board_id": board.board_id,
                "board_kind": board_kind.value,
                "card_count": len(cards),
                "columns": resolved_columns,
                "density": density.value
            }
        )

        return board
