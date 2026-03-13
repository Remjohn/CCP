"""
CBCS Example Agent Implementation
=================================
This file demonstrates how to implement a specific agent (e.g., 'Emilio') 
using the Master Agent Container pattern.

It shows:
1. Dependency Injection (Supabase, Neo4j, Intelligence Library)
2. Protocol Loading
3. Structured Output Enforcement
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
import os
from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- 1. DEPENDENCY INJECTION SCHEMA ---
@dataclass
class AgentDeps:
    """
    The 'Sensory Inputs' for the Agent.
    This injects the static Intelligence Library and the dynamic User Context.
    """
    # Infrastructure Clients
    supabase: Any # Replace with actual Supabase Client type
    neo4j_driver: Any # Replace with actual Neo4j Driver type
    
    # Static Intelligence (The Brain Regions)
    identity_pillars: Dict[str, Any]    # identity_pillars.yaml
    persuasion_layers: Dict[str, Any]   # persuasion_layers.yaml
    ttt_matrix: Dict[str, Any]          # ttt_matrix.yaml
    story_formulas: Dict[str, Any]      # story_formulas.yaml
    context_map: Dict[str, Any]         # context_premise_map.json
    
    # Dynamic Context (The Short-Term Memory)
    user_id: str
    session_id: str
    current_state_context: Dict[str, Any] # The output from the previous agent in the chain

# --- 2. OUTPUT SCHEMAS (The Pre-Frontal Cortex) ---
class AgentReasoningLog(BaseModel):
    """Metacognition tracking - why the agent made the decision."""
    consulted_file: str = Field(..., description="Which YAML file governed this decision?")
    step_by_step_logic: str = Field(..., description="Chain of thought summary.")
    safety_check: bool = Field(..., description="Did this pass the Glass Wall protocol?")

class ExampleAgentOutput(BaseModel):
    """
    Example Output Model.
    In a real agent, this would be specific (e.g., ScriptContent, SoulDataExtraction).
    """
    reasoning: AgentReasoningLog
    actionable_data: Dict[str, Any] 

# --- 3. AGENT INITIALIZATION ---
def load_protocol(agent_name: str) -> str:
    """
    Loads the specific 'Soul' (System Prompt) for this agent.
    In this example, we return a mock protocol if the file doesn't exist.
    """
    path = Path(f"backend/intelligence_library/protocols/{agent_name}_protocol.md")
    if path.exists():
        return path.read_text()
    
    # Mock Protocol for demonstration
    return """
    # {agent_name} PROTOCOL
    You are {agent_name}.
    Your mission is to demonstrate the CBCS architecture.
    
    User Identity: {user_identity}
    User TTT: {user_ttt}
    Context: {context_data}
    """

# Define the Model
model = OpenAIModel('gpt-4o', api_key=os.getenv('OPENAI_API_KEY'))

# Instantiate the Agent
agent = Agent(
    model,
    deps_type=AgentDeps,
    result_type=ExampleAgentOutput, # Enforces strict output
    retries=3
)

# --- 4. SYSTEM PROMPT INJECTION ---
@agent.system_prompt
def inject_intelligence(ctx: RunContext[AgentDeps]) -> str:
    """
    This function acts as the 'Consciousness Bootloader'.
    It reads the Markdown Protocol and injects the specific context variables.
    """
    protocol_template = load_protocol("example_agent")
    
    # We dynamically format the system prompt with the User's current context
    return protocol_template.format(
        agent_name="ExampleAgent",
        user_identity=ctx.deps.current_state_context.get('identity_pillar', 'Unknown'),
        user_ttt=ctx.deps.current_state_context.get('ttt_baseline', 'TTT-05'),
        context_data=str(ctx.deps.current_state_context)
    )

# --- 5. TOOL DEFINITIONS (The Hands) ---
@agent.tool
async def query_knowledge_base(ctx: RunContext[AgentDeps], query: str) -> str:
    """
    Example tool to query the knowledge base.
    """
    # In a real implementation, this would use ctx.deps.supabase or ctx.deps.neo4j_driver
    return f"Mock result for query: {query}"
