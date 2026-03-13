"""
CBCS MASTER AGENT CONTAINER TEMPLATE v2.0
=========================================
This container represents the "Physical Body" and "Nervous System" of a specific agent.
It does NOT contain the personality or psychological logic (that lives in the Protocol).
It handles the I/O, the tool execution, and the structural validation of thoughts.

Core Responsibilities:
1. Dependency Injection: Loading the Intelligence Library (YAMLs) into the agent's context.
2. Tool Binding: Connecting the agent to specific capabilities (Neo4j, Groq, Supabase).
3. Schema Enforcement: Using Pydantic models to force structured reasoning (No raw text).
4. State Management: interfacing with the LangGraph orchestrator.

Usage:
Copy this file to /backend/agents/[category]/[agent_name].py and fill in the specific
Models and Protocol references.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
import os
import yaml
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError
from pydantic_ai import Agent, RunContext, ModelRetry
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.minimax import MinimaxModel  # If using MiniMax-M2 specifically

# --- 1. DEPENDENCY INJECTION SCHEMA ---
@dataclass
class AgentDeps:
    """
    The 'Sensory Inputs' for the Agent.
    This injects the static Intelligence Library and the dynamic User Context.
    """
    # Infrastructure Clients
    supabase: Any
    neo4j_driver: Any
    
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
# NOTE: Replace this with the specific agent's Output Model
class AgentReasoningLog(BaseModel):
    """Metacognition tracking - why the agent made the decision."""
    consulted_file: str = Field(..., description="Which YAML file governed this decision?")
    step_by_step_logic: str = Field(..., description="Chain of thought summary.")
    safety_check: bool = Field(..., description="Did this pass the Glass Wall protocol?")

class AgentOutput(BaseModel):
    """The enforced output structure. Agents NEVER return raw strings."""
    reasoning: AgentReasoningLog
    # Specific fields will be defined in the implementation class
    # e.g., script_content, extracted_entities, strategy_object
    actionable_data: Dict[str, Any] 

# --- 3. AGENT INITIALIZATION ---
def load_protocol(agent_name: str) -> str:
    """Loads the specific 'Soul' (System Prompt) for this agent."""
    path = Path(f"backend/intelligence_library/protocols/{agent_name}_protocol.md")
    if not path.exists():
        raise FileNotFoundError(f"Protocol not found for {agent_name}")
    return path.read_text()

# Define the Model (MiniMax-M2 or GPT-4o) based on config
model = OpenAIModel('gpt-4o', api_key=os.getenv('OPENAI_API_KEY'))

# Instantiate the Agent
agent = Agent(
    model,
    deps_type=AgentDeps,
    result_type=AgentOutput, # Enforces strict output
    retries=3
)

# --- 4. SYSTEM PROMPT INJECTION ---
@agent.system_prompt
def inject_intelligence(ctx: RunContext[AgentDeps]) -> str:
    """
    This function acts as the 'Consciousness Bootloader'.
    It reads the Markdown Protocol and injects the specific context variables.
    """
    protocol_template = load_protocol("AGENT_NAME_PLACEHOLDER")
    
    # We dynamically format the system prompt with the User's current context
    # This ensures the agent isn't just 'An Agent' but 'The Agent for THIS User'
    return protocol_template.format(
        user_identity=ctx.deps.current_state_context.get('identity_pillar'),
        user_ttt=ctx.deps.current_state_context.get('ttt_baseline'),
        context_data=str(ctx.deps.current_state_context)
    )

# --- 5. TOOL DEFINITIONS (The Hands) ---
# Specific tools will be decorated here using @agent.tool
# Example:
# @agent.tool
# async def query_graph(ctx: RunContext[AgentDeps], cypher: str) -> str:
#     ...
