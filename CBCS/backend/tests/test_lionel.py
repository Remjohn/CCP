import pytest
from unittest.mock import MagicMock, AsyncMock
from backend.core.lionel import lionel, LionelDeps, FactBank, Fact

@pytest.mark.asyncio
async def test_lionel_mock_search(mocker):
    # Mock Model
    mock_response = MagicMock()
    mock_response.output = FactBank(
        topic="Procrastination",
        facts=[
            Fact(statement="Procrastination is emotional regulation.", source="Study X", category="Scientific")
        ]
    )
    mocker.patch("backend.core.lionel.lionel.run", new_callable=AsyncMock, return_value=mock_response)
    
    deps = LionelDeps()
    deps.tavily_api_key = None
    
    # Test tool directly
    from backend.core.lionel import search_tavily
    ctx = MagicMock()
    ctx.deps.tavily_api_key = None
    
    result = await search_tavily(ctx, "test query")
    assert "Mock Search Result" in result

@pytest.mark.asyncio
async def test_lionel_tavily_advanced(mocker):
    # Test the tool with API key and verify advanced depth
    from backend.core.lionel import search_tavily
    
    ctx = MagicMock()
    ctx.deps.tavily_api_key = "test_key"
    
    # Mock httpx
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.post.return_value = MagicMock(
        raise_for_status=lambda: None,
        json=lambda: {"answer": "Deep facts found."}
    )
    mocker.patch("httpx.AsyncClient", return_value=mock_client)
    
    result = await search_tavily(ctx, "test query")
    assert "Deep facts found" in result
    
    # Verify payload
    call_args = mock_client.post.call_args
    payload = call_args[1]["json"]
    assert payload["search_depth"] == "advanced"
