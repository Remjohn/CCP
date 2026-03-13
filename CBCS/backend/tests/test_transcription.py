import pytest
from backend.core.transcription import transcriber
from backend.config import get_settings
from unittest.mock import MagicMock, AsyncMock

settings = get_settings()

@pytest.mark.asyncio
async def test_transcription_service_mocked(mocker):
    """
    Tests the transcription logic with mocked Telegram and Groq calls.
    We don't want to actually download files from Telegram in unit tests usually.
    """
    # Mock Response Object
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "ok": True, 
        "result": {"file_path": "voice/test.ogg"}
    }
    mock_response.raise_for_status = MagicMock()
    mock_response.content = b"fake_audio_bytes"

    # Mock httpx methods to return the mock_response
    mocker.patch("httpx.AsyncClient.post", new_callable=AsyncMock, return_value=mock_response)
    mocker.patch("httpx.AsyncClient.get", new_callable=AsyncMock, return_value=mock_response)
    
    # Mock Groq
    # We need to mock the client inside the transcriber instance or patch the class
    mock_groq_create = AsyncMock()
    mock_groq_create.return_value.text = "Hello world"
    
    mocker.patch.object(
        transcriber.client.audio.transcriptions, 
        "create", 
        side_effect=mock_groq_create
    )

    # Test Flow
    file_path = await transcriber.get_file_path("file_123")
    assert file_path == "voice/test.ogg"
    
    audio_bytes = await transcriber.download_file(file_path)
    assert audio_bytes == b"fake_audio_bytes"
    
    text = await transcriber.transcribe(audio_bytes)
    assert text == "Hello world"

@pytest.mark.asyncio
async def test_transcription_integration():
    """
    Real integration test. Requires a valid file_id (hard to get without real interaction).
    So we might just test the Groq part with a dummy file if we had one.
    For now, we skip or rely on the mock.
    """
    pass
