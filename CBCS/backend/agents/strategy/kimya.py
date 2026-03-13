from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
import os
from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel

# Import tools
# None specified

# --- 1. DEPENDENCY INJECTION SCHEMA ---
@dataclass
class AgentDeps:
    """
    The 'Sensory Inputs' for the Agent.
    """
    # Infrastructure Clients
    # None specified
    
    # Static Intelligence
    identity_pillars: Dict[str, Any]
    persuasion_layers: Dict[str, Any]
    ttt_matrix: Dict[str, Any]
    story_formulas: Dict[str, Any]
    context_map: Dict[str, Any]
    
    # Dynamic Context
    user_id: str
    session_id: str
    current_state_context: Dict[str, Any]

# --- 2. OUTPUT SCHEMAS ---
class AgentReasoningLog(BaseModel):
    """Metacognition tracking."""
    consulted_file: str = Field(..., description="Which YAML file governed this decision?")
    step_by_step_logic: str = Field(..., description="Chain of thought summary.")
    safety_check: bool = Field(..., description="Did this pass the Glass Wall protocol?")

class PantryConfiguration(BaseModel):
    """Output model for Kimya."""
    pantry_config: Dict[str, Any] = Field(..., description="Configuration for the Pantry.")

class AgentOutput(BaseModel):
    """The enforced output structure."""
    reasoning: AgentReasoningLog
    actionable_data: PantryConfiguration

# --- 3. AGENT INITIALIZATION ---
def load_protocol(agent_name: str) -> str:
    path = Path(f"backend/intelligence_library/protocols/{agent_name}_protocol.md")
    if not path.exists():
        raise FileNotFoundError(f"Protocol not found for {agent_name}")
    return path.read_text()

model = OpenAIModel('gpt-4o', api_key=os.getenv('OPENAI_API_KEY'))

agent = Agent(
    model,
    deps_type=AgentDeps,
    result_type=AgentOutput,
    retries=3
)

# --- 4. SYSTEM PROMPT INJECTION ---
@agent.system_prompt
def inject_intelligence(ctx: RunContext[AgentDeps]) -> str:
    protocol_template = load_protocol("kimya")
    return protocol_template.format(
        user_identity=ctx.deps.current_state_context.get('identity_pillar'),
        user_ttt=ctx.deps.current_state_context.get('ttt_baseline'),
        context_data=str(ctx.deps.current_state_context)
    )
