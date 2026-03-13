import pytest
from backend.core.journal_processor import journal_processor
from backend.core.aria import ContextExtraction, ContextEntity
from unittest.mock import MagicMock, AsyncMock

@pytest.mark.asyncio
async def test_process_journal(mocker):
    # Mock Aria
    mock_aria_result = MagicMock()
    mock_aria_result.output = ContextExtraction(entities=[
        ContextEntity(name="Fear", type="Enemy", relationship="FIGHTS_AGAINST")
    ])
    
    # Patch the aria agent instance directly
    mocker.patch("backend.core.journal_processor.aria.run", new_callable=AsyncMock, return_value=mock_aria_result)
    
    # Mock Graph
    mock_create_context = mocker.patch("backend.core.journal_processor.context_graph.create_context_premise", new_callable=AsyncMock)

    # Test
    result = await journal_processor.process_journal("123", "I am afraid")
    
    assert result is not None
    assert len(result.entities) == 1
    mock_create_context.assert_called_once()
    
    # Verify arguments passed to graph
    call_args = mock_create_context.call_args
    assert call_args[0][0] == "123" # user_id
    assert call_args[0][1][0]["name"] == "Fear" # entity data
