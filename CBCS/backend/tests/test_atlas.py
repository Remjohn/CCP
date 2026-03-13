import pytest
from backend.core.atlas import atlas, UserProfile

def test_atlas_low_capacity():
    user = UserProfile(id="u1", capacity_score=15, identity_pillar="Seeker")
    program = atlas.generate_schedule(user)
    
    assert len(program.schedule) == 30
    
    # Week 1 should be Micro
    day1 = program.schedule[0]
    assert day1.intensity == "Micro"
    assert day1.ritual_name == "2-Min Breath" # Only micro habit in mock pantry

def test_atlas_high_capacity():
    user = UserProfile(id="u2", capacity_score=85, identity_pillar="Rebel")
    program = atlas.generate_schedule(user)
    
    assert len(program.schedule) == 30
    
    # Week 1 should be Heroic
    day1 = program.schedule[0]
    assert day1.intensity == "Heroic"
    # Should pick Cold Shower (Rebel + High Threshold)
    # Note: Mock logic picks random suitable, but let's see if it respects identity
    # Rebel fits Cold Shower. Cold Shower is threshold 80.
    # Logic: "Filter rituals by identity". Cold Shower is in suitable_rituals.
    # Logic: "Override for Micro-Habit week". This is Heroic week, so no override.
    # So it might pick Cold Shower.
    
    # Let's just check intensity for now as selection is random from suitable
    assert day1.intensity == "Heroic" 
