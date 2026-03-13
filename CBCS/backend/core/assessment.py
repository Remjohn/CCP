from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from backend.core.identity_models import IdentityVector
import logging

logger = logging.getLogger(__name__)


class AssessmentSubmission(BaseModel):
    telegram_chat_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    answers: Dict[str, Any] = Field(..., description="Key-value pairs of the 12 dimensions")


class AssessmentResult(BaseModel):
    capacity_score: int
    identity_vector: IdentityVector = Field(
        default_factory=IdentityVector,
        description="12-dimensional identity vector replacing the old identity_pillar string"
    )


def calculate_capacity_score(answers: Dict[str, Any]) -> int:
    """
    Calculates the Capacity Score (0-100) based on answers.
    Placeholder logic: Sum of specific fields or default to 50.
    """
    # TODO: Implement real logic based on FR 2.1
    # For now, return a mock score
    return 50


def compute_identity_vector(
    text: str,
    user_history: Optional[List[IdentityVector]] = None,
) -> IdentityVector:
    """
    Computes the 12-dimensional identity vector from journal text.

    Replaces the old determine_identity_pillar() which returned
    a hardcoded "The Builder" string.

    The actual scoring logic is implemented in identity_scorers.py
    (Step 4) and called by Aria's enhanced extraction pipeline.
    This function serves as the public API entry point.

    Args:
        text: Raw journal entry text (transcribed voice note)
        user_history: Previous identity vectors for trajectory context

    Returns:
        IdentityVector with all sub-model scores
    """
    # TODO: Wire to identity_scorers.py sub-agents (Step 4)
    # For now, return a default vector with LOW confidence
    vector = IdentityVector(
        word_count=len(text.split()) if text else 0,
        confidence=0.0,
    )
    logger.info(f"Identity vector computed (word_count={vector.word_count}, confidence=LOW)")
    return vector

