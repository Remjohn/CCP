"""
Aria — Context Premise Extraction Agent (v2.0)
================================================
Rewired to load system prompt from aria_SKILL.md via skill_loader.

Architecture:
    aria_SKILL.md (250 lines of extraction rules)
         ↓
    skill_loader.load_skill("aria") → system_prompt
         ↓
    Pydantic AI Agent(system_prompt=..., output_type=ContextExtraction)
"""

from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Dict, Any
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from backend.config import get_settings
from backend.core.skill_loader import skill_loader

import os
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

if settings.GROQ_API_KEY:
    os.environ["GROQ_API_KEY"] = settings.GROQ_API_KEY

model = GroqModel('llama-3.3-70b-versatile')


# ── Output Models (v2 — extended from SKILL.md spec) ──

class ContextEntity(BaseModel):
    """A single extracted entity from the user's context."""
    name: str = Field(..., description="The name of the entity (e.g., 'Procrastination', 'Financial Freedom')")
    dimension: Literal['Enemy', 'Dream', 'Fear', 'Identity', 'Coach', 'Ritual', 'Trigger', 'Resistance'] = Field(
        ..., description="Which of the 12 extraction dimensions this entity belongs to"
    )
    relationship: Literal[
        'FIGHTS_AGAINST', 'CRAVES', 'FEARS', 'HAS_IDENTITY',
        'GUIDED_BY', 'RESONATES_WITH'
    ] = Field(..., description="The Neo4j relationship type")
    confidence: Literal['HIGH', 'MEDIUM', 'LOW'] = Field(
        'MEDIUM', description="Confidence in this extraction"
    )
    evidence_quote: Optional[str] = Field(
        None, description="Direct quote from source text supporting this entity"
    )
    weight: float = Field(0.5, description="Relative importance (0-1)")


class TTTState(BaseModel):
    """The user's Tension-Texture-Temperature state."""
    tension: Literal['Wired', 'Steady', 'Flat'] = Field(..., description="How wound-up or relaxed")
    texture: Literal['Sharp', 'Flowing', 'Broken'] = Field(..., description="How their language feels")
    temperature: Literal['Manic', 'Warm', 'Defeated'] = Field(..., description="How emotionally hot or cold")
    ttt_code: str = Field(..., description="TTT matrix position (TTT-01 through TTT-10)")
    confidence: Literal['HIGH', 'MEDIUM', 'LOW'] = Field('MEDIUM')


class ExtractionReasoning(BaseModel):
    """Transparent reasoning chain for the extraction."""
    consulted_files: List[str] = Field(default_factory=lambda: ["context_premise_map.json"])
    step_by_step_logic: str = Field(..., description="How the extraction was performed")
    safety_check: bool = Field(True, description="PII/safety validation passed")
    pii_detected: bool = Field(False, description="Was PII detected and redacted?")


class ExtractionFlags(BaseModel):
    """Edge case flags."""
    sarcasm_detected: bool = False
    insufficient_input: bool = False
    mixed_language: bool = False


class ContextExtraction(BaseModel):
    """Full context premise extraction — v2 output model."""
    reasoning: ExtractionReasoning
    entities: List[ContextEntity]
    ttt_state: TTTState
    identity_pillar: Optional[Literal['Challenger', 'Nurturer', 'Maker', 'Explorer', 'Rebel']] = None
    capacity_score: Optional[int] = Field(None, ge=0, le=100, description="User energy/capacity 0-100")
    resistance_pattern: Optional[str] = None
    milestone_proximity: Optional[Literal['APPROACHING_BREAKTHROUGH', 'STABLE', 'REGRESSION_RISK']] = None
    flags: ExtractionFlags = Field(default_factory=ExtractionFlags)


# ── Agent Setup ──

# Load SKILL.md system prompt (replaces inline 3-line prompt)
_aria_skill = skill_loader.load_skill("aria")

if _aria_skill:
    _system_prompt = _aria_skill.system_prompt
    logger.info(f"[Aria] Loaded SKILL.md v{_aria_skill.version} ({len(_system_prompt)} chars)")
else:
    # Fallback if SKILL.md not found — original minimal prompt
    logger.warning("[Aria] SKILL.md not found, using fallback prompt")
    _system_prompt = (
        "You are Aria, the Synthesizer. Your job is to read user text (assessments or journals) "
        "and extract the psychological 'Context Premise'. "
        "Identify the User's 'Enemy' (what blocks them), 'Dream' (what they want), 'Fear' (what scares them), "
        "and 'Identity' (who they believe they are). "
        "Map these to specific relationships."
    )

aria = Agent(
    model,
    system_prompt=_system_prompt,
    output_type=ContextExtraction,
)
