import pytest
import yaml
import json
import os
from backend.core.intelligence import IntelligenceLibrary, IdentityPillarsConfig

@pytest.fixture
def mock_library_path(tmp_path):
    # Create dummy files
    path = tmp_path / "intelligence_library"
    path.mkdir()
    
    # identity_pillars.yaml
    pillars = {
        "pillars": [
            {"name": "The Builder", "description": "Builds things", "keywords": ["structure", "foundation"]}
        ]
    }
    with open(path / "identity_pillars.yaml", "w") as f:
        yaml.dump(pillars, f)
        
    # ttt_matrix.yaml
    ttt = {
        "levels": [
            {"level": 1, "name": "Soft", "description": "Gentle", "voice_params": {"speed": 0.9}}
        ]
    }
    with open(path / "ttt_matrix.yaml", "w") as f:
        yaml.dump(ttt, f)

    # persuasion_layers.yaml
    layers = {
        "layers": [
            {"name": "Logic", "description": "Uses facts", "logic": "If A then B"}
        ]
    }
    with open(path / "persuasion_layers.yaml", "w") as f:
        yaml.dump(layers, f)

    # story_formulas.yaml
    formulas = {
        "formulas": [
            {"name": "Hero's Journey", "structure": ["Call", "Refusal", "Acceptance"]}
        ]
    }
    with open(path / "story_formulas.yaml", "w") as f:
        yaml.dump(formulas, f)

    # context_premise_map.json
    context = {
        "dimensions": [
            {"name": "Fear", "description": "What scares you"}
        ]
    }
    with open(path / "context_premise_map.json", "w") as f:
        json.dump(context, f)
        
    return str(path)

def test_load_library_success(mock_library_path):
    lib = IntelligenceLibrary(library_path=mock_library_path)
    lib.load()
    
    assert lib.identity_pillars is not None
    assert len(lib.identity_pillars.pillars) == 1
    assert lib.identity_pillars.pillars[0].name == "The Builder"
    
    assert lib.ttt_matrix is not None
    assert lib.persuasion_layers is not None
    assert lib.story_formulas is not None
    assert lib.context_premise_map is not None

def test_load_library_missing_file(tmp_path):
    # Empty dir
    path = tmp_path / "empty_lib"
    path.mkdir()
    
    lib = IntelligenceLibrary(library_path=str(path))
    
    with pytest.raises(FileNotFoundError):
        lib.load()
