import pytest
from backend.core.graph_db import context_graph
from unittest.mock import MagicMock, AsyncMock

@pytest.mark.asyncio
async def test_create_user_node(mocker):
    # Mock the driver and session
    mock_session = AsyncMock()
    mock_result = AsyncMock()
    mock_record = {"u": {"id": "123", "name": "Test User"}}
    
    mock_result.single.return_value = mock_record
    mock_session.run.return_value = mock_result
    mock_session.__aenter__.return_value = mock_session
    
    mocker.patch.object(context_graph.driver, "session", return_value=mock_session)

    # Test
    user = await context_graph.create_user_node("123", "Test User")
    
    assert user["id"] == "123"
    assert user["name"] == "Test User"
    mock_session.run.assert_called_once()

@pytest.mark.asyncio
async def test_create_context_premise(mocker):
    # Mock session
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session
    mocker.patch.object(context_graph.driver, "session", return_value=mock_session)

    entities = [
        {"name": "Procrastination", "type": "Enemy", "relationship": "FIGHTS_AGAINST"},
        {"name": "Freedom", "type": "Dream", "relationship": "CRAVES"}
    ]

    await context_graph.create_context_premise("123", entities)
    
    # Should call run twice (once for each entity)
    assert mock_session.run.call_count == 2
