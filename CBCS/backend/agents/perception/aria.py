from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
import os
from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel

# Import tools
from backend.tools.groq_tools import groq_client
from backend.tools.neo4j_tools import neo4j_client

# Identity Engine imports
from backend.core.identity_models import IdentityVector
from backend.agents.perception.identity_scorers import build_identity_vector

# --- 1. DEPENDENCY INJECTION SCHEMA ---
@dataclass
class AgentDeps:
    """
    The 'Sensory Inputs' for the Agent.
    """
    # Infrastructure Clients
    groq: Any
    neo4j: Any

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

class Entity(BaseModel):
    label: str
    name: str
    weight: float
    relationship: str = Field("", description="Relationship type: FIGHTS_AGAINST, CRAVES, FEARS, HAS_IDENTITY")
    evidence_quote: str = Field("", description="Source text that triggered this extraction")
    confidence: str = Field("MEDIUM", description="HIGH/MEDIUM/LOW extraction confidence")

class SoulDataExtraction(BaseModel):
    """Output model for Aria — enhanced with Identity Engine."""
    entities: List[Entity] = Field(..., description="List of extracted entities.")
    user_ttt_state: str = Field(..., description="Calculated TTT state.")
    l3_context_premise: Optional[str] = Field(None, description="Extracted Event-Specific Knowledge (L3 Depth) context premise for CCF memory pipeline.")
    identity_vector: Optional[IdentityVector] = Field(None, description="12-dimensional identity vector computed from entities and journal text.")

class AgentOutput(BaseModel):
    """The enforced output structure."""
    reasoning: AgentReasoningLog
    actionable_data: SoulDataExtraction

# --- 3. AGENT INITIALIZATION ---
def load_protocol(agent_name: str) -> str:
    path = Path(f"backend/intelligence_library/protocols/{agent_name}_protocol.md")
    if not path.exists():
        # Try SKILL.md naming convention
        skill_path = Path(f"backend/intelligence_library/protocols/{agent_name}_SKILL.md")
        if skill_path.exists():
            return skill_path.read_text()
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
    protocol_template = load_protocol("aria")
    return protocol_template.format(
        user_identity=ctx.deps.current_state_context.get('identity_vector', {}),
        user_ttt=ctx.deps.current_state_context.get('ttt_baseline'),
        context_data=str(ctx.deps.current_state_context)
    )

