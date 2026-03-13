from fastapi import APIRouter, HTTPException, status
from typing import List
from backend.core.analytics import analytics, Vibe
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/cohort-vibe", response_model=List[Vibe])
async def get_cohort_vibe():
    """
    Returns the aggregated vibe data for the cohort.
    """
    try:
        return analytics.get_cohort_vibes()
    except Exception as e:
        logger.error(f"Failed to get cohort vibe: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch cohort analytics"
        )
