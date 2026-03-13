import pytest
from unittest.mock import MagicMock, AsyncMock
from backend.core.graph import processing_node
from langchain_core.messages import HumanMessage

@pytest.mark.asyncio
async def test_processing_node_sequence(mocker):
    # Mock Agent
    mock_agent = MagicMock()
    mock_agent.run = AsyncMock(return_value=MagicMock(data="Test Response"))
    mocker.patch("backend.core.graph.agent", mock_agent)
    
    # Mock Deps
    # We don't need to patch CBCSAgentDeps if we don't inspect it, 
    # but if we want to avoid import errors, we can patch the module where it is defined.
    mocker.patch("backend.core.agent.CBCSAgentDeps")
    mocker.patch("backend.core.intelligence.intelligence_library")
    
    state = {
        "messages": [], 
        "buffer": [{"message": {"text": "Hello"}}], 
        "user_id": "123"
    }
    
    result = await processing_node(state)
    
    assert len(result["messages"]) == 1
    assert result["messages"][0].content == "Test Response"
    
    # Note: The actual delay logic is hard to test here without refactoring the graph to send side-effects.
    # For now, we verified the node still works.
