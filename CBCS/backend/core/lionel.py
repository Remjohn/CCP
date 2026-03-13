from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.groq import GroqModel
from backend.config import get_settings
from typing import List, Optional
import os
import httpx
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

if settings.GROQ_API_KEY:
    os.environ["GROQ_API_KEY"] = settings.GROQ_API_KEY

model = GroqModel('llama-3.3-70b-versatile')

# --- Models ---

class Fact(BaseModel):
    statement: str = Field(..., description="The factual statement.")
    source: str = Field(..., description="Source URL or citation.")
    category: str = Field(..., description="Scientific, Historical, or Contrarian.")

class FactBank(BaseModel):
    topic: str
    facts: List[Fact]

class LionelDeps:
    tavily_api_key: Optional[str]

# --- Agent ---

lionel = Agent(
    model,
    deps_type=LionelDeps,
    system_prompt=(
        "You are Lionel, the Deep Researcher for the CBCS. "
        "Your goal is to find verified facts to support coaching advice. "
        "You must search for Scientific studies, Historical examples, and Contrarian viewpoints. "
        "Use the 'search_tavily' tool to find this information. "
        "Synthesize the findings into a 'FactBank'."
    ),
    output_type=FactBank
)

@lionel.tool
async def search_tavily(ctx: RunContext[LionelDeps], query: str) -> str:
    """
    Searches the web using Tavily API with advanced depth.
    """
    api_key = ctx.deps.tavily_api_key
    if not api_key:
        logger.warning("Tavily API Key missing. Returning mock data.")
        return "Mock Search Result: Study X shows that procrastination is linked to fear of failure."

    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "advanced", # Deeper search for Lionel
        "include_answer": True
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=15.0)
            response.raise_for_status()
            data = response.json()
            return data.get("answer", "") or str(data.get("results", []))
    except Exception as e:
        logger.error(f"Tavily search failed: {e}")
        return "Error searching web."
