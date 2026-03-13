from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from .state import AgentState
from ..config import get_settings
import logging
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)
settings = get_settings()

# --- Nodes ---

async def listening_node(state: AgentState):
    """
    The entry point. Analyzes the buffer to decide next steps.
    """
    logger.info(f"Listening Node: Processing {len(state.get('buffer', []))} messages.")
    return {"is_processing": True}


async def extraction_node(state: AgentState):
    """
    Story 21.5: Perception pass — Aria extracts context entities.

    Runs Aria SKILL.md to identify Enemy, Dream, Fear, Identity,
    TTT state, capacity, and resistance patterns from the buffer.
    """
    logger.info("Extraction Node: Running Aria context extraction...")

    buffer = state.get("buffer", [])
    user_text = "\n".join([msg.get("message", {}).get("text", "") for msg in buffer])

    if not user_text:
        logger.warning("Empty buffer in extraction node.")
        return {"is_processing": True}

    try:
        from .aria import aria

        result = await aria.run(user_text)
        extraction = result.data

        logger.info(
            f"Extraction complete: {len(extraction.entities)} entities, "
            f"TTT={extraction.ttt_state.ttt_code}, "
            f"Pillar={extraction.identity_pillar}"
        )

        # Store extraction in state for downstream nodes
        return {
            "context_extraction": extraction.model_dump(),
            "is_processing": True,
        }

    except Exception as e:
        logger.error(f"Aria extraction failed: {e}", exc_info=True)
        return {"is_processing": True}


from .agent import agent

async def processing_node(state: AgentState):
    """
    The core logic node. Calls the Pydantic AI Agent.

    Now receives structured context from Aria's extraction
    to make smarter decisions about response strategy.
    """
    logger.info("Processing Node: Invoking Agent...")

    user_id = state["user_id"]
    buffer = state.get("buffer", [])

    # Construct the user message from the buffer
    user_text = "\n".join([msg.get("message", {}).get("text", "") for msg in buffer])

    if not user_text:
        logger.warning("Empty buffer in processing node.")
        return {"is_processing": False}

    try:
        # Story 3.2: Inject Intelligence Library
        from .intelligence import intelligence_library
        from .agent import CBCSAgentDeps
        from langchain_core.messages import AIMessage

        # Enrich user text with context extraction if available
        context_extraction = state.get("context_extraction")
        if context_extraction:
            entities = context_extraction.get("entities", [])
            ttt = context_extraction.get("ttt_state", {})
            pillar = context_extraction.get("identity_pillar", "Unknown")

            context_summary = (
                f"\n\n[Context Extraction]\n"
                f"Identity Pillar: {pillar}\n"
                f"TTT State: {ttt.get('ttt_code', 'Unknown')}\n"
                f"Entities: {', '.join(e['name'] + ' (' + e['dimension'] + ')' for e in entities)}\n"
            )
            enriched_text = user_text + context_summary
        else:
            enriched_text = user_text

        deps = CBCSAgentDeps(
            user_id=str(user_id),
            library=intelligence_library
        )

        result = await agent.run(enriched_text, deps=deps)
        response_text = result.data

        return {"messages": [AIMessage(content=response_text)]}

    except Exception as e:
        logger.error(f"Agent execution failed: {e}")
        return {"is_processing": False}


async def script_node(state: AgentState):
    """
    Story 21.5: Expression pass — Artisan generates personalized script.

    Only runs when the context warrants a ritual/script response
    (e.g., assessments, journal entries that reveal a context premise).
    For normal conversations, this node is a no-op.
    """
    context_extraction = state.get("context_extraction")

    if not context_extraction:
        # No extraction data → skip script generation
        return {"is_processing": False}

    entities = context_extraction.get("entities", [])
    if len(entities) < 3:
        # Not enough context for a meaningful script
        logger.info("Script Node: Insufficient entities, skipping script generation.")
        return {"is_processing": False}

    logger.info("Script Node: Generating personalized script...")

    try:
        from .assembler import assembler, UserProfile, ContextPremise, Ritual
        from .artisan import artisan
        from langchain_core.messages import AIMessage

        # Build minimal profiles from extraction
        pillar = context_extraction.get("identity_pillar", "Explorer")
        capacity = context_extraction.get("capacity_score", 50)
        ttt_code = context_extraction.get("ttt_state", {}).get("ttt_code", "TTT-05")

        # Find primary pain from entities
        enemies = [e for e in entities if e.get("dimension") == "Enemy"]
        primary_pain = enemies[0]["name"] if enemies else "General Stress"

        user_profile = UserProfile(
            id=str(state.get("user_id", "unknown")),
            capacity_score=capacity or 50,
            identity_pillar=pillar or "Explorer",
        )

        context_premise = ContextPremise(
            primary_pain=primary_pain,
            ttt_code=ttt_code,
            entities=entities,
        )

        # TODO: Load available rituals from database
        # For now, skip ritual selection if no rituals available
        logger.info(
            f"Script Node: Would generate script for "
            f"pillar={pillar}, TTT={ttt_code}, pain={primary_pain}"
        )

        return {"is_processing": False}

    except Exception as e:
        logger.error(f"Script generation failed: {e}", exc_info=True)
        return {"is_processing": False}


# --- Routing ---

def should_generate_script(state: AgentState) -> str:
    """
    Route after processing: generate script or end.

    Scripts are generated when Aria detected enough entities
    to warrant a ritual-based response.
    """
    context = state.get("context_extraction")
    if context and len(context.get("entities", [])) >= 3:
        return "script"
    return "end"


# --- Graph Definition ---

workflow = StateGraph(AgentState)

workflow.add_node("listening", listening_node)
workflow.add_node("extraction", extraction_node)
workflow.add_node("processing", processing_node)
workflow.add_node("script", script_node)

workflow.set_entry_point("listening")

# listening → extraction → processing → (script | END)
workflow.add_edge("listening", "extraction")
workflow.add_edge("extraction", "processing")
workflow.add_conditional_edges("processing", should_generate_script, {
    "script": "script",
    "end": END,
})
workflow.add_edge("script", END)

# --- Persistence Lifecycle ---

from langgraph.checkpoint.memory import MemorySaver

_checkpointer_cm = None
checkpointer = None

async def init_checkpointer():
    """
    Initializes the global checkpointer. Called on app startup.
    Falls back to MemorySaver if Postgres connection fails.
    """
    global _checkpointer_cm, checkpointer
    
    if settings.POSTGRES_URL:
        try:
            _checkpointer_cm = AsyncPostgresSaver.from_conn_string(settings.POSTGRES_URL)
            checkpointer = await _checkpointer_cm.__aenter__()
            await checkpointer.setup()
            logger.info("LangGraph Postgres Checkpointer initialized.")
            return
        except Exception as e:
            logger.error(f"Failed to connect to Postgres: {e}. Falling back to MemorySaver.")
            if _checkpointer_cm:
                await _checkpointer_cm.__aexit__(None, None, None)
                _checkpointer_cm = None
    
    # Fallback
    checkpointer = MemorySaver()
    logger.warning("Using in-memory checkpointer. State will be lost on restart.")

async def close_checkpointer():
    """
    Closes the global checkpointer. Called on app shutdown.
    """
    global _checkpointer_cm, checkpointer
    if _checkpointer_cm:
        await _checkpointer_cm.__aexit__(None, None, None)
        _checkpointer_cm = None
    
    checkpointer = None
    logger.info("LangGraph Checkpointer closed.")

def get_graph():
    """
    Returns the compiled graph, using the global checkpointer if available.
    """
    return workflow.compile(checkpointer=checkpointer)

# Simple compiled version without persistence
graph_simple = workflow.compile()
