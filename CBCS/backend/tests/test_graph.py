import pytest
from backend.core.graph import graph_simple, get_graph, init_checkpointer, close_checkpointer
from backend.core.state import AgentState
from backend.config import get_settings
import asyncio
import sys

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

settings = get_settings()

@pytest.mark.asyncio
async def test_simple_graph_execution():
    """
    Test the graph logic without persistence.
    """
    initial_state = {
        "user_id": 123,
        "buffer": [{"message": {"text": "hello"}}],
        "messages": [],
        "is_processing": True
    }
    
    # Run the graph
    result = await graph_simple.ainvoke(initial_state)
    
    # Check final state
    assert result["is_processing"] is False

@pytest.mark.asyncio
async def test_persistent_graph_execution():
    """
    Test the graph with Postgres persistence.
    """
    if not settings.POSTGRES_URL:
        pytest.skip("POSTGRES_URL not set")

    try:
        # Manually init checkpointer for test
        await init_checkpointer()
        
        graph = get_graph()
        
        user_id = 456
        config = {"configurable": {"thread_id": str(user_id)}}
        
        initial_state = {
            "user_id": user_id,
            "buffer": [{"message": {"text": "persistent hello"}}],
            "messages": [],
            "is_processing": True
        }
        
        # Run 1
        result = await graph.ainvoke(initial_state, config=config)
        assert result["is_processing"] is False
        
        # Check persistence
        snapshot = await graph.aget_state(config)
        assert snapshot.values["user_id"] == user_id
        
        # Verify if we are using Postgres or Memory
        from langgraph.checkpoint.memory import MemorySaver
        if isinstance(graph.checkpointer, MemorySaver):
            print("\nWARNING: Test ran with MemorySaver fallback.")
        
    finally:
        await close_checkpointer()
