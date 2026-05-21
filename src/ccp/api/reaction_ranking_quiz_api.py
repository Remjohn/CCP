from fastapi import APIRouter
import uuid
from datetime import datetime
from src.ccp.models.reaction_ranking_quiz_models import (
    RankingQuizSessionProjection,
    RankingQuizProposalArtifact,
    RankingQuizComparisonProjection,
    RankingQuizOriginalRanking,
    RankingQuizSourceItem,
    ResolvedPalette,
    RankingQuizProposalItem,
    RankingQuizDiffEntry
)

router = APIRouter()

@router.get("/reactions/ranking-quiz/{session_id}", response_model=RankingQuizSessionProjection)
async def get_session(session_id: str):
    now = datetime.utcnow()
    items = [
        RankingQuizSourceItem(item_id="i1", label="Item 1", original_slot_index=0),
        RankingQuizSourceItem(item_id="i2", label="Item 2", original_slot_index=1),
    ]
    
    original = RankingQuizOriginalRanking(
        source_artifact_id="tierlist_123",
        published_by_person_id="coach_1",
        title="My Tierlist",
        frozen_at=now,
        items=items
    )
    
    return RankingQuizSessionProjection(
        session_id=session_id,
        palette=ResolvedPalette(background_primary="#1e293b", background_secondary="#0f172a", accent="#38bdf8"),
        original_ranking=original,
        working_order=[RankingQuizProposalItem(item_id="i1", label="Item 1", proposed_slot_index=0), RankingQuizProposalItem(item_id="i2", label="Item 2", proposed_slot_index=1)],
        share_token="tok_123"
    )

@router.post("/reactions/ranking-quiz/{session_id}/proposal", response_model=RankingQuizComparisonProjection)
async def submit_proposal(session_id: str, payload: dict):
    now = datetime.utcnow()
    
    items = [
        RankingQuizSourceItem(item_id="i1", label="Item 1", original_slot_index=0),
        RankingQuizSourceItem(item_id="i2", label="Item 2", original_slot_index=1),
    ]
    
    original = RankingQuizOriginalRanking(
        source_artifact_id="tierlist_123",
        published_by_person_id="coach_1",
        title="My Tierlist",
        frozen_at=now,
        items=items
    )
    
    session = RankingQuizSessionProjection(
        session_id=session_id,
        palette=ResolvedPalette(background_primary="#1e293b", background_secondary="#0f172a", accent="#38bdf8"),
        original_ranking=original,
        working_order=[],
        share_token="tok_123"
    )
    
    proposal = RankingQuizProposalArtifact(
        proposal_id=str(uuid.uuid4()),
        session_id=session_id,
        proposer_person_id="viewer_1",
        proposal_items=[RankingQuizProposalItem(item_id="i2", label="Item 2", proposed_slot_index=0), RankingQuizProposalItem(item_id="i1", label="Item 1", proposed_slot_index=1)],
        diff_entries=[
            RankingQuizDiffEntry(item_id="i2", label="Item 2", original_slot_index=1, proposed_slot_index=0, slot_delta=1),
            RankingQuizDiffEntry(item_id="i1", label="Item 1", original_slot_index=0, proposed_slot_index=1, slot_delta=-1)
        ],
        changed_item_count=2,
        submitted_at=now
    )
    
    return RankingQuizComparisonProjection(
        session=session,
        proposal=proposal
    )
