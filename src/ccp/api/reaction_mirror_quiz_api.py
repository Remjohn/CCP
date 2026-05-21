from fastapi import APIRouter
from src.ccp.models.reaction_mirror_quiz_models import MirrorQuizQuestionPack, MirrorQuizSessionProjection
from src.ccp.services.mirror_quiz_question_service import MirrorQuizQuestionService

router = APIRouter()
service = MirrorQuizQuestionService()

@router.post("/reactions/mirror-quiz/question-pack", response_model=MirrorQuizQuestionPack)
async def generate_question_pack(payload: dict):
    # Dependency injection mocking for integration logic
    coach_id = payload.get("coach_id", "default_coach")
    # Will use real CMM loader here in production
    return service.build_question_pack(coach_id)

@router.post("/reactions/mirror-quiz/finalize", response_model=MirrorQuizSessionProjection)
async def finalize_quiz_session(payload: dict):
    pass
