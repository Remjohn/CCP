import pytest
from unittest.mock import MagicMock, AsyncMock
from backend.core.maeva import maeva, MaevaDeps, SentimentReport

@pytest.mark.asyncio
async def test_maeva_mock_search(mocker):
    # Mock Model to avoid Groq call
    mock_response = MagicMock()
    mock_response.output = SentimentReport(
        top_themes=["Anxiety", "Burnout", "Hope"],
        summary="People are stressed."
    )
    mocker.patch("backend.core.maeva.maeva.run", new_callable=AsyncMock, return_value=mock_response)
    
    deps = MaevaDeps()
    deps.tavily_api_key = None # Trigger mock in tool (if tool was called, but we mocked run)
    
    # If we want to test the tool logic, we should test the tool function directly or use a real agent with mocked tool.
    # Let's test the tool function directly.
    from backend.core.maeva import search_tavily
    
    ctx = MagicMock()
    ctx.deps.tavily_api_key = None
    
    result = await search_tavily(ctx, "test query")
    assert "Mock Search Result" in result

@pytest.mark.asyncio
async def test_maeva_tavily_call(mocker):
    # Test the tool with API key
    from backend.core.maeva import search_tavily
    
    ctx = MagicMock()
    ctx.deps.tavily_api_key = "test_key"
    
    # Mock httpx
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.post.return_value = MagicMock(
        raise_for_status=lambda: None,
        json=lambda: {"answer": "Tavily says hello."}
    )
    mocker.patch("httpx.AsyncClient", return_value=mock_client)
    
    result = await search_tavily(ctx, "test query")
    assert "Tavily says hello" in result
