import pytest
from backend.core.assembler import assembler, Ritual, UserProfile, ContextPremise

def test_select_ritual_capacity_filter():
    # Setup
    rituals = [
        Ritual(id="1", name="Micro-Habit", description="", level_threshold=10, identity_fit=["The Rebel"], goal_fit="Anxiety", media_url="", script_template=""),
        Ritual(id="2", name="Heroic Quest", description="", level_threshold=80, identity_fit=["The Rebel"], goal_fit="Anxiety", media_url="", script_template="")
    ]
    
    # User with Low Capacity
    user = UserProfile(id="u1", capacity_score=20, identity_pillar="The Rebel")
    context = ContextPremise(primary_pain="Anxiety")
    
    # Test
    selected = assembler.select_ritual(user, context, rituals)
    
    # Should pick Micro-Habit because Heroic Quest is too hard (80 > 20)
    assert selected is not None
    assert selected.name == "Micro-Habit"

def test_select_ritual_identity_match():
    # Setup
    rituals = [
        Ritual(id="1", name="Rebel Ritual", description="", level_threshold=10, identity_fit=["The Rebel"], goal_fit="Anxiety", media_url="", script_template=""),
        Ritual(id="2", name="Builder Ritual", description="", level_threshold=10, identity_fit=["The Builder"], goal_fit="Anxiety", media_url="", script_template="")
    ]
    
    # User is a Rebel
    user = UserProfile(id="u1", capacity_score=50, identity_pillar="The Rebel")
    context = ContextPremise(primary_pain="Anxiety")
    
    # Test
    selected = assembler.select_ritual(user, context, rituals)
    
    # Should pick Rebel Ritual
    assert selected.name == "Rebel Ritual"
