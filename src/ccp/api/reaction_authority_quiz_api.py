from fastapi import APIRouter
import uuid
from datetime import datetime, timedelta
from src.ccp.models.reaction_authority_quiz_models import (
    AuthorityQuizPromptPack,
    AuthorityQuizQuestion,
    AuthorityQuizSessionProjection,
    AuthorityQuizLevelState
)

router = APIRouter()

@router.post("/reactions/authority-quiz/session", response_model=AuthorityQuizPromptPack)
async def create_session(payload: dict):
    coach_id = payload.get("coach_id", "default")
    session_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    questions = []
    for i in range(1, 6):
        questions.append(AuthorityQuizQuestion(
            question_id=f"q_{i}",
            level_index=i,
            prompt_text=f"High Stakes Question {i}",
            answer_options=["A", "B", "C", "D"],
            correct_answer_key="A",
            stakes_label=f"Level {i}"
        ))
        
    return AuthorityQuizPromptPack(
        session_id=session_id,
        coach_id=coach_id,
        title="Authority Escalation",
        questions=questions,
        base_mood_state="authoritative",
        issued_at=now,
        expires_at=now + timedelta(hours=1),
        ttl_seconds=3600
    )

@router.post("/reactions/authority-quiz/finalize", response_model=AuthorityQuizSessionProjection)
async def finalize_session(payload: dict):
    # Pass-through finalize logic
    pass
