from pydantic_ai import Agent, RunContext
from pydantic_ai.models.groq import GroqModel
from backend.config import get_settings
from backend.core.intelligence import IntelligenceLibrary
from datetime import datetime
from dataclasses import dataclass
import logging
import os

logger = logging.getLogger(__name__)
settings = get_settings()

# Ensure API Key is in env for Pydantic AI
if settings.GROQ_API_KEY:
    os.environ["GROQ_API_KEY"] = settings.GROQ_API_KEY

# Initialize Model
model = GroqModel('llama-3.3-70b-versatile')

# --- Dependencies ---

@dataclass
class CBCSAgentDeps:
    user_id: str
    library: IntelligenceLibrary

# --- Agent Definition ---

agent = Agent(
    model,
    deps_type=CBCSAgentDeps,
    retries=3
)

@agent.system_prompt
def generate_system_prompt(ctx: RunContext[CBCSAgentDeps]) -> str:
    """
    Dynamically generates the system prompt based on the Intelligence Library.
    """
    lib = ctx.deps.library
    
    # Extract Identity Pillars (Example of using the library)
    pillars_text = ""
    if lib.identity_pillars:
        pillars = ", ".join([p.name for p in lib.identity_pillars.pillars])
        pillars_text = f"You are guided by these Identity Pillars: {pillars}."

    # Extract TTT Levels
    ttt_text = ""
    if lib.ttt_matrix:
        levels = ", ".join([f"{l.level}: {l.name}" for l in lib.ttt_matrix.levels])
        ttt_text = f"Your voice spectrum includes: {levels}."

    prompt = (
        "You are the Orchestrator of the Conscious Behavioral Change System (CBCS). "
        "Your goal is to help users align their behavior with their intentions. "
        "You are empathetic, precise, and action-oriented. "
        f"{pillars_text} "
        f"{ttt_text} "
        "Use tools ONLY when explicitly necessary or requested by the user."
    )
    return prompt

# --- Tools ---

@agent.tool
async def get_current_time(ctx: RunContext[CBCSAgentDeps]) -> str:
    """
    Returns the current server time. Useful for checking if the agent can use tools.
    """
    now = datetime.now().isoformat()
    logger.info(f"Tool 'get_current_time' called by user {ctx.deps.user_id}. Time: {now}")
    return now
