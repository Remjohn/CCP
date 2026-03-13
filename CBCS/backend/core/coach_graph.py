"""
Coach LangGraph Subgraph — Story 18.4
======================================
Handles coach-specific flows: interview processing, content ideation,
pipeline triggers, and user monitoring.

Architecture:
    ingress.py → role_router → coach_graph.py

    Nodes:
        coach_listening → [intent classifier] →
            ├── content_ideation (generate tier list/rating ideas)
            ├── pipeline_trigger (spawn CMF/CCF CLI sessions)
            ├── user_monitor (check user activity, send alerts)
            ├── idea_selection (coach picked an idea)
            └── general_response (regular conversation)

    State passes through the file system for CCF/CMF — this graph
    doesn't replicate their prompt logic, it coordinates WHEN to run them.
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage

from backend.core.state import AgentState

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# Intent Classification
# ──────────────────────────────────────────────

COACH_INTENTS = {
    "idea_selection": ["1️⃣", "2️⃣", "3️⃣", "option 1", "option 2", "option 3",
                       "first one", "second one", "third one", "pick 1", "pick 2", "pick 3"],
    "pipeline_trigger": ["run pipeline", "start production", "generate video",
                         "run cmf", "start cmf", "create video"],
    "user_check": ["how are my users", "user status", "who's inactive",
                   "check users", "user report", "activity report"],
    "interview": ["here's my interview", "weekly update", "this week",
                  "new topic", "content idea", "this week's theme"],
}


def classify_coach_intent(text: str) -> str:
    """
    Simple intent classification for coach messages.

    In production, this could be an LLM call for better accuracy.
    For MVP, keyword matching is sufficient since coach interactions
    are typically structured (reply to bot prompts).
    """
    if not text:
        return "general"

    text_lower = text.strip().lower()

    # Check emoji selections first (most common interaction)
    for intent, keywords in COACH_INTENTS.items():
        for keyword in keywords:
            if keyword in text_lower:
                return intent

    # Check if it's a voice transcription (interview)
    if text_lower.startswith("[transcription]:"):
        return "interview"

    return "general"


# ──────────────────────────────────────────────
# Graph Nodes
# ──────────────────────────────────────────────

async def coach_listening(state: AgentState) -> dict:
    """
    Entry node: Analyze buffered messages and classify intent.

    This is the coach equivalent of Aria (perception layer).
    Instead of extracting psychological entities, it determines
    what the coach wants to do.
    """
    buffer = state.get("buffer", [])
    if not buffer:
        return {"is_processing": False}

    # Extract text from buffer
    texts = []
    for msg in buffer:
        message_data = msg.get("message", {})
        text = message_data.get("text", "")
        if text:
            texts.append(text)

    combined_text = " ".join(texts)
    intent = classify_coach_intent(combined_text)

    logger.info(f"[Coach Graph] Intent classified: '{intent}' for coach {state.get('user_id')}")

    # Add the coach's message to conversation history
    return {
        "messages": [HumanMessage(content=combined_text)],
        "is_processing": True,
    }


async def content_ideation(state: AgentState) -> dict:
    """
    Generate tier list/rating ideas based on weekly themes.

    This node:
        1. Reads dynamic_content_themes.json (from CCF weekly pipeline)
        2. Generates 3 ideas using the archetype prompts
        3. Formats them for Telegram delivery
        4. Sends via Telegram API

    Note: The actual idea generation logic comes from
    tools/telegram-tierlist-bot/generator.py — ported here.
    """
    coach_id = state.get("user_id")
    logger.info(f"[Coach Graph] Content ideation triggered for coach {coach_id}")

    # TODO: Port generator.py logic here or call it as subprocess
    # For now, log the intent and return a placeholder
    response = (
        "📊 *Content Ideas for This Week*\n\n"
        "I'll generate your tier list/rating ideas once the weekly themes are ready.\n"
        "This feature is being wired up — stay tuned!"
    )

    return {
        "messages": [AIMessage(content=response)],
        "is_processing": False,
    }


async def pipeline_trigger(state: AgentState) -> dict:
    """
    Spawn CMF/CCF CLI sessions via the CLI Runner.

    This node coordinates WHEN to run Gemini CLI sessions and
    reports progress. The creative work happens inside Gemini CLI.
    """
    coach_id = state.get("user_id")
    coach_config = state.get("coach_config")
    logger.info(f"[Coach Graph] Pipeline trigger requested by coach {coach_id}")

    # Get project_id from coach config
    project_root = None
    if coach_config:
        project_root = coach_config.get("project_root")

    if not project_root:
        return {
            "messages": [AIMessage(content=(
                "⚠️ *No project configured*\n\n"
                "I need a project root to run the pipeline.\n"
                "Ask your admin to set `project_root` in your coach config."
            ))],
            "is_processing": False,
        }

    try:
        from backend.core.cli_runner import cli_runner, build_cmf_phase1a_pipeline
        from backend.core.telegram import send_telegram_message
        import os

        # Extract project_id from the project root path
        # e.g., "production/Coach Adele/03_50-12 Jean Pierre" → "03_50-12 Jean Pierre"
        project_id = os.path.basename(project_root)
        workspace_root = os.path.dirname(os.path.dirname(project_root))

        # Send acknowledgment immediately
        ack_msg = (
            "🎬 *Pipeline Starting!*\n\n"
            f"Project: `{project_id}`\n\n"
            "Running CMF Phase 1A pipeline:\n"
            "1. 🩺 Story Diagnosis\n"
            "2. 🔎 Arc Hunting\n"
            "3. 📊 Analysis & Enrichment\n"
            "4. ✍️ Composition\n\n"
            "I'll notify you as each step completes. This takes ~10 min."
        )
        await send_telegram_message(coach_id, ack_msg)

        # Build and run the pipeline
        pipeline_configs = build_cmf_phase1a_pipeline(
            project_id=project_id,
            workspace_root=workspace_root,
        )

        results = await cli_runner.run_pipeline(
            configs=pipeline_configs,
            stop_on_failure=True,
        )

        # Build results summary
        step_names = ["Story Diagnosis", "Arc Hunting", "Analysis", "Composition"]
        summary_lines = ["✅ *Pipeline Complete!*\n"]
        all_success = True

        for i, result in enumerate(results):
            step_name = step_names[i] if i < len(step_names) else f"Step {i+1}"
            if result.success:
                summary_lines.append(f"✅ {step_name} ({result.duration_seconds:.0f}s)")
            else:
                summary_lines.append(f"❌ {step_name} — failed")
                all_success = False

        if not all_success:
            summary_lines[0] = "⚠️ *Pipeline Completed With Errors*\n"

        response = "\n".join(summary_lines)

    except ImportError:
        response = "⚠️ CLI Runner module not available."
    except Exception as e:
        logger.error(f"[Coach Graph] Pipeline trigger failed: {e}", exc_info=True)
        response = f"❌ *Pipeline Error*\n\n{str(e)[:200]}"

    return {
        "messages": [AIMessage(content=response)],
        "is_processing": False,
    }


async def user_monitor(state: AgentState) -> dict:
    """
    Check user activity and generate alerts for the coach.

    Queries the user_activity_log table to find:
        - Users inactive for > 3 days
        - Users who completed milestones
        - Users flagged by the safety agent
    """
    coach_id = state.get("user_id")
    logger.info(f"[Coach Graph] User monitor requested by coach {coach_id}")

    # TODO: Query user_activity_log table
    response = (
        "👥 *User Activity Report*\n\n"
        "User monitoring is being connected to the activity tracking system.\n"
        "Soon you'll see:\n"
        "• Inactive users (>3 days)\n"
        "• Recent milestones\n"
        "• Safety alerts"
    )

    return {
        "messages": [AIMessage(content=response)],
        "is_processing": False,
    }


async def idea_selection(state: AgentState) -> dict:
    """
    Handle coach's selection of a content idea (1️⃣, 2️⃣, or 3️⃣).

    After selection:
        1. Store the selected idea in coach_content_ideas table
        2. Begin recording preparation
        3. Generate script + visual prompts for the selected idea
    """
    coach_id = state.get("user_id")
    buffer = state.get("buffer", [])

    # Extract selection from the latest message
    for msg in reversed(buffer):
        text = msg.get("message", {}).get("text", "")
        if "1" in text:
            selected = 0
        elif "2" in text:
            selected = 1
        elif "3" in text:
            selected = 2
        else:
            selected = None

        if selected is not None:
            break
    else:
        selected = None

    logger.info(f"[Coach Graph] Coach {coach_id} selected idea index: {selected}")

    if selected is not None:
        response = (
            f"✅ *Idea #{selected + 1} Selected!*\n\n"
            "I'm preparing your recording package:\n"
            "• 📝 Script generation\n"
            "• 🎨 Visual prompts\n"
            "• 🔗 Recording page link\n\n"
            "This will be ready shortly."
        )
    else:
        response = "I didn't catch which idea you picked. Reply with 1️⃣, 2️⃣, or 3️⃣."

    return {
        "messages": [AIMessage(content=response)],
        "selected_idea_index": selected,
        "is_processing": False,
    }


async def general_response(state: AgentState) -> dict:
    """
    Handle general coach messages that don't match a specific intent.

    Uses the main Pydantic AI agent for free-form conversation.
    """
    coach_id = state.get("user_id")
    logger.info(f"[Coach Graph] General response for coach {coach_id}")

    response = (
        "I'm your coaching assistant. Here's what I can do:\n\n"
        "📊 Send you weekly content ideas (automatic)\n"
        "🎬 Trigger video production pipelines\n"
        "👥 Monitor your users' activity\n"
        "🎤 Process your weekly interview voice notes\n\n"
        "Just tell me what you need, or reply to my prompts!"
    )

    return {
        "messages": [AIMessage(content=response)],
        "is_processing": False,
    }


# ──────────────────────────────────────────────
# Intent Router (Conditional Edge)
# ──────────────────────────────────────────────

def route_coach_intent(state: AgentState) -> str:
    """
    Conditional edge: Route to the appropriate node based on intent.

    Called after coach_listening to determine which flow to enter.
    """
    buffer = state.get("buffer", [])

    # Extract text from buffer
    texts = []
    for msg in buffer:
        message_data = msg.get("message", {})
        text = message_data.get("text", "")
        if text:
            texts.append(text)

    combined_text = " ".join(texts)
    intent = classify_coach_intent(combined_text)

    logger.info(f"[Coach Graph] Routing to intent: {intent}")

    return intent


# ──────────────────────────────────────────────
# Graph Construction
# ──────────────────────────────────────────────

def build_coach_graph() -> StateGraph:
    """
    Build the coach LangGraph subgraph.

    Flow:
        START → coach_listening → [intent router] →
            ├── content_ideation → END
            ├── pipeline_trigger → END
            ├── user_monitor → END (user_check)
            ├── idea_selection → END
            ├── interview → content_ideation → END
            └── general → END (general)
    """
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("coach_listening", coach_listening)
    graph.add_node("content_ideation", content_ideation)
    graph.add_node("pipeline_trigger", pipeline_trigger)
    graph.add_node("user_monitor", user_monitor)
    graph.add_node("idea_selection", idea_selection)
    graph.add_node("general_response", general_response)

    # Entry edge
    graph.add_edge(START, "coach_listening")

    # Conditional routing based on intent
    graph.add_conditional_edges(
        "coach_listening",
        route_coach_intent,
        {
            "content_ideation": "content_ideation",
            "pipeline_trigger": "pipeline_trigger",
            "user_check": "user_monitor",
            "idea_selection": "idea_selection",
            "interview": "content_ideation",  # Interview → generate ideas from themes
            "general": "general_response",
        }
    )

    # All terminal nodes go to END
    graph.add_edge("content_ideation", END)
    graph.add_edge("pipeline_trigger", END)
    graph.add_edge("user_monitor", END)
    graph.add_edge("idea_selection", END)
    graph.add_edge("general_response", END)

    return graph


# ──────────────────────────────────────────────
# Graph Accessor (matches pattern from graph.py)
# ──────────────────────────────────────────────

_coach_graph = None


def get_coach_graph():
    """Get or create the compiled coach graph."""
    global _coach_graph
    if _coach_graph is None:
        builder = build_coach_graph()
        _coach_graph = builder.compile()
        logger.info("[Coach Graph] Compiled successfully")
    return _coach_graph
