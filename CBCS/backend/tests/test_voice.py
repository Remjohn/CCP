import pytest
from unittest.mock import MagicMock, AsyncMock
from backend.core.voice import voice_engine

@pytest.mark.asyncio
async def test_generate_audio_mock(mocker):
    # Ensure credentials are None for this test to trigger mock
    mocker.patch.object(voice_engine, "api_key", None)
    mocker.patch.object(voice_engine, "endpoint_id", None)
    
    url = await voice_engine.generate_audio("Hello world")
    assert url == "https://mock.audio/output.mp3"

@pytest.mark.asyncio
async def test_generate_audio_runpod(mocker):
    # Setup credentials
    mocker.patch.object(voice_engine, "api_key", "test_key")
    mocker.patch.object(voice_engine, "endpoint_id", "test_id")
    mocker.patch.object(voice_engine, "base_url", "https://api.runpod.ai/v2/test_id/runsync")
    
    # Mock httpx
    mock_response = MagicMock()
    mock_response.json.return_value = {"output": {"audio_url": "https://runpod.io/audio.mp3"}}
    mock_response.raise_for_status = MagicMock()
    
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.post.return_value = mock_response
    
    mocker.patch("httpx.AsyncClient", return_value=mock_client)
    
    # Test
    url = await voice_engine.generate_audio("Hello world", style="Challenger")
    
    assert url == "https://runpod.io/audio.mp3"
    
    # Verify params sent
    call_args = mock_client.post.call_args
    payload = call_args[1]["json"]
    assert payload["input"]["speed"] == 1.1 # Challenger speed
