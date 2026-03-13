"""
Artisan — Script Personalization Agent (v2.0)
===============================================
Rewired to load system prompt from artisan_SKILL.md via skill_loader.

Architecture:
    artisan_SKILL.md (300 lines of script rules)
         ↓
    skill_loader.load_skill("artisan") → system_prompt
         ↓
    Pydantic AI Agent(system_prompt=..., output_type=ScriptResponse)
"""

from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from backend.config import get_settings
from backend.core.skill_loader import skill_loader
from typing import List, Optional

import os
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

if settings.GROQ_API_KEY:
    os.environ["GROQ_API_KEY"] = settings.GROQ_API_KEY

model = GroqModel('llama-3.3-70b-versatile')


# ── Input Models ──

class ContextEntity(BaseModel):
    """Minimal entity reference for script request."""
    name: str
    type: str  # Enemy, Dream, Fear

class ScriptRequest(BaseModel):
    """Input to the Artisan from the Assembler."""
    ritual_name: str
    ritual_description: str
    user_name: str
    user_context: str
    identity_layer: Optional[str] = None  # e.g., "Challenger", "Nurturer"
    ttt_code: Optional[str] = None  # e.g., "TTT-07"
    persuasion_layer: Optional[str] = None  # e.g., "Competitive Edge"
    sentiment_report: Optional[str] = None  # From Maeva
    fact_bank: Optional[str] = None  # From Lionel
    banned_phrases: Optional[List[str]] = None
    max_duration_seconds: int = 90


# ── Output Models (v2 — extended from SKILL.md spec) ──

class ScriptSection(BaseModel):
    """One beat of the 6-beat script structure."""
    beat: str = Field(..., description="Beat name: HOOK, PAIN_MIRROR, REFRAME, RITUAL_INTRO, ACTION, CLOSE")
    text: str = Field(..., description="The spoken text for this beat")
    duration_estimate_seconds: int = Field(..., description="Estimated spoken duration")
    ttt_applied: Optional[str] = Field(None, description="Which TTT rules were applied")

class ScriptQualityReport(BaseModel):
    """13-point quality validation report."""
    identity_alignment: str = Field(..., description="How the identity pillar was expressed")
    ttt_compliance: str = Field(..., description="TTT syntax rule compliance summary")
    persuasion_layer_applied: Optional[str] = None
    entity_references: List[str] = Field(default_factory=list, description="Which entities from Aria were referenced")
    sentiment_used: bool = False
    fact_used: bool = False
    banned_phrases_check: str = "PASS (0 violations)"
    overall_quality_score: float = Field(..., ge=0, le=10, description="Self-assessed quality 0-10")

class ScriptResponse(BaseModel):
    """Full Artisan output — personalized script + quality report."""
    full_script: str = Field(..., description="The complete personalized script ready for TTS")
    sections: Optional[List[ScriptSection]] = Field(
        None, description="Breakdown by 6-beat structure"
    )
    total_duration_estimate_seconds: Optional[int] = None
    word_count: Optional[int] = None
    quality_report: Optional[ScriptQualityReport] = None
    validation_notes: Optional[List[str]] = None


# ── Agent Setup ──

# Load SKILL.md system prompt
_artisan_skill = skill_loader.load_skill("artisan")

if _artisan_skill:
    _system_prompt = _artisan_skill.system_prompt
    logger.info(f"[Artisan] Loaded SKILL.md v{_artisan_skill.version} ({len(_system_prompt)} chars)")
else:
    logger.warning("[Artisan] SKILL.md not found, using fallback prompt")
    _system_prompt = (
        "You are The Artisan, a master copywriter for the Conscious Behavioral Change System. "
        "Your goal is to rewrite the provided 'Script Template' to be deeply personal to the user. "
        "Adapt your tone based on the identity layer. "
        "Keep the script concise, impactful, and spoken-word ready."
    )

artisan = Agent(
    model,
    system_prompt=_system_prompt,
    output_type=ScriptResponse,
)
