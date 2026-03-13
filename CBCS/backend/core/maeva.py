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

class SentimentReport(BaseModel):
    top_themes: List[str] = Field(..., description="Top 3 emotional themes found.")
    summary: str = Field(..., description="Brief summary of the 'vibe'.")

class MaevaDeps:
    tavily_api_key: Optional[str]

# --- Agent ---

maeva = Agent(
    model,
    deps_type=MaevaDeps,
    system_prompt=(
        "You are Maeva, the Social Researcher for the CBCS. "
        "Your goal is to scan the internet for the current 'Zeitgeist' related to specific tribes. "
        "Use the 'search_tavily' tool to find recent discussions, news, and forums. "
        "Synthesize the findings into a 'Sentiment Report' identifying the top 3 emotional themes."
    ),
    output_type=SentimentReport
)

@maeva.tool
async def search_tavily(ctx: RunContext[MaevaDeps], query: str) -> str:
    """
    Searches the web using Tavily API.
    """
    api_key = ctx.deps.tavily_api_key
    if not api_key:
        logger.warning("Tavily API Key missing. Returning mock data.")
        return "Mock Search Result: People are feeling anxious about the economy and burnt out from work."

    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "include_answer": True
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            return data.get("answer", "") or str(data.get("results", []))
    except Exception as e:
        logger.error(f"Tavily search failed: {e}")
        return "Error searching web."
