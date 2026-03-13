import pytest
from unittest.mock import MagicMock, AsyncMock
from backend.core.assembler import AssemblerService
from backend.core.artisan import artisan, ScriptResponse

@pytest.mark.asyncio
async def test_assembler_injection(mocker):
    # Mock Artisan
    mock_response = MagicMock()
    mock_response.output = ScriptResponse(final_script="Script with Fact X")
    mocker.patch("backend.core.artisan.artisan.run", new_callable=AsyncMock, return_value=mock_response)
    
    service = AssemblerService()
    ritual = {"name": "Test Ritual", "description": "Desc", "script_template": "Template"}
    profile = {"name": "User", "capacity_score": 50, "identity_pillar": "Stoic"}
    
    script = await service.synthesize_script(
        ritual, 
        profile, 
        sentiment_report="Vibe is anxious", 
        fact_bank="Fact X: Breathing helps."
    )
    
    assert script == "Script with Fact X"
    
    # Verify arguments passed to agent
    call_args = artisan.run.call_args
    arg_str = call_args[0][0]
    assert "Vibe is anxious" in arg_str
    assert "Fact X" in arg_str
