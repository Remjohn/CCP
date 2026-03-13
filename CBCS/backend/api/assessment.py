from fastapi import APIRouter, HTTPException, status
from backend.core.assessment import AssessmentSubmission, AssessmentResult, calculate_capacity_score, determine_identity_pillar
from backend.config import get_settings
# We need a Supabase client here. 
# Since we don't have a global one yet, let's create a simple one or reuse if available.
# For now, we'll use the supabase-py client directly.
from supabase import create_client, Client
import logging

router = APIRouter()
settings = get_settings()
logger = logging.getLogger(__name__)

# Initialize Supabase Client
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

@router.post("/submit", response_model=AssessmentResult, status_code=status.HTTP_201_CREATED)
async def submit_assessment(submission: AssessmentSubmission):
    """
    Receives assessment data, calculates scores, and updates the profile.
    """
    try:
        # 1. Calculate Derived Metrics
        capacity_score = calculate_capacity_score(submission.answers)
        identity_pillar = determine_identity_pillar(submission.answers)

        # 2. Upsert Profile
        # We use telegram_chat_id as the unique key for now
        profile_data = {
            "telegram_chat_id": submission.telegram_chat_id,
            "first_name": submission.first_name,
            "last_name": submission.last_name,
            "capacity_score": capacity_score,
            "identity_pillar": identity_pillar,
            "updated_at": "now()"
        }
        
        # Check if profile exists
        # Note: In a real app, we'd handle Auth User ID mapping. 
        # Here we assume the user is identified by Telegram ID.
        
        # Try to find existing profile
        res = supabase.table("profiles").select("id").eq("telegram_chat_id", submission.telegram_chat_id).execute()
        
        if res.data:
            user_id = res.data[0]["id"]
            supabase.table("profiles").update(profile_data).eq("id", user_id).execute()
        else:
            res = supabase.table("profiles").insert(profile_data).execute()
            user_id = res.data[0]["id"]

        # 3. Store Assessment
        assessment_data = {
            "user_id": user_id,
            "answers": submission.answers
        }
        supabase.table("assessments").insert(assessment_data).execute()

        logger.info(f"Assessment processed for user {user_id}. Capacity: {capacity_score}, Identity: {identity_pillar}")

        return AssessmentResult(
            capacity_score=capacity_score,
            identity_pillar=identity_pillar
        )

    except Exception as e:
        logger.error(f"Assessment submission failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/config")
async def get_assessment_config():
    """
    Returns the dynamic assessment configuration (questions, logic) from the branding file.
    """
    import json
    from pathlib import Path
    
    # Path to branding file (relative to backend/api)
    # backend/api/assessment.py -> backend/ -> frontend/Pamela branding.json
    base_dir = Path(__file__).parent.parent.parent
    branding_file = base_dir / "frontend" / "Pamela branding.json"
    
    try:
        with open(branding_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        return {
            "configuration": data["assessment_engine"]["configuration"],
            "question_bank": data["assessment_engine"]["question_bank"]
        }
    except Exception as e:
        logger.error(f"Failed to load assessment config: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load assessment configuration"
        )
