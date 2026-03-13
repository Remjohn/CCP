import pytest
from unittest.mock import MagicMock, AsyncMock
from backend.core.assembler import assembler, Ritual
from backend.core.artisan import ScriptResponse

@pytest.mark.asyncio
async def test_synthesize_script(mocker):
    # Mock Artisan
    mock_result = MagicMock()
    mock_result.output = ScriptResponse(final_script="Defeat Procrastination today.")
    
    # Patch the artisan agent run method where it is defined
    mocker.patch("backend.core.artisan.artisan.run", new_callable=AsyncMock, return_value=mock_result)
    
    # Setup
    ritual = Ritual(
        id="1", 
        name="Test Ritual", 
        description="", 
        level_threshold=10, 
        identity_fit=[], 
        goal_fit="", 
        media_url="", 
        script_template="Defeat [Enemy] today."
    )
    
    context_entities = [{"name": "Procrastination", "type": "Enemy"}]
    
    # Test
    script = await assembler.synthesize_script(ritual, context_entities)
    
    assert script == "Defeat Procrastination today."

@pytest.mark.asyncio
async def test_synthesize_script_challenger(mocker):
    # Mock Artisan
    mock_result = MagicMock()
    mock_result.output = ScriptResponse(final_script="Maybe you are comfortable letting Procrastination win.")
    
    # Patch the artisan agent run method where it is defined
    mocker.patch("backend.core.artisan.artisan.run", new_callable=AsyncMock, return_value=mock_result)
    
    # Setup
    ritual = Ritual(
        id="1", 
        name="Challenger Ritual", 
        description="", 
        level_threshold=10, 
        identity_fit=[], 
        goal_fit="", 
        media_url="", 
        script_template="Defeat [Enemy] today."
    )
    
    context_entities = [{"name": "Procrastination", "type": "Enemy"}]
    
    # Test
    script = await assembler.synthesize_script(ritual, context_entities, identity_layer="Challenger")
    
    assert "comfortable letting Procrastination win" in script
