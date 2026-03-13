from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from backend.config import get_settings
import os

settings = get_settings()

# Ensure API Key is in env for Pydantic AI
if settings.GROQ_API_KEY:
    os.environ["GROQ_API_KEY"] = settings.GROQ_API_KEY

# --- Models ---

class CoachSoul(BaseModel):
    name: str = Field(..., description="Name of the coach")
    unique_mechanism: str = Field(..., description="The unique method or proprietary process the coach uses")
    promise: str = Field(..., description="The big promise or transformation offered to clients")
    voice_tone: str = Field(..., description="Adjectives describing the coach's voice (e.g., authoritative, empathetic)")
    metaphors: List[str] = Field(..., description="Common metaphors or analogies used by the coach")
    ttt_baseline: str = Field(..., description="The default TTT (Text-to-Speech) style setting")

class TribeSoul(BaseModel):
    tribe_name: str = Field(..., description="Name of the target audience or community")
    core_fears: List[str] = Field(..., description="Top 3 deep fears of the tribe")
    core_desires: List[str] = Field(..., description="Top 3 deep desires of the tribe")
    language_patterns: List[str] = Field(..., description="Slang, keywords, or phrases common in the tribe")

# --- Agents ---

model = GroqModel('llama-3.3-70b-versatile')

# 1. Kimya (The Extractor)
kimya = Agent(
    model,
    system_prompt=(
        "You are Kimya, the Extractor. Your job is to analyze a Coach's raw content "
        "and distill their 'Unique Mechanism' (their proprietary method) and their 'Promise' (the result). "
        "Be precise and look for branded terms."
    ),
    output_type=CoachSoul
)

# 2. Valeriane (The Soul Architect)
valeriane = Agent(
    model,
    system_prompt=(
        "You are Valeriane, the Soul Architect. Your job is to analyze a Coach's communication style. "
        "Identify their tone of voice, the metaphors they rely on, and their baseline energy. "
        "You are building the 'Soul' that will drive the AI's personality."
    ),
    output_type=CoachSoul
)

# 3. Dilaya (The Scout)
dilaya = Agent(
    model,
    system_prompt=(
        "You are Dilaya, the Scout. Your job is to understand the Target Audience (The Tribe). "
        "Analyze the context to find out what they fear, what they crave, and how they speak. "
        "You are building the 'Tribe Soul' to ensure relevance."
    ),
    output_type=TribeSoul
)
