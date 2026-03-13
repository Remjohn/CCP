from pydantic import BaseModel, Field
from typing import List, Optional
from backend.core.assembler import Ritual, UserProfile
import random

class DailyTask(BaseModel):
    day: int
    ritual_id: str
    ritual_name: str
    intensity: str # Micro, Standard, Heroic

class ProgramSchedule(BaseModel):
    user_id: str
    schedule: List[DailyTask]

class AtlasService:
    def __init__(self):
        # Mock Pantry
        self.pantry = [
            Ritual(id="r1", name="2-Min Breath", description="Breathe", level_threshold=10, identity_fit=["Seeker", "Maker"], goal_fit="Anxiety", media_url="url", script_template="tpl"),
            Ritual(id="r2", name="Cold Shower", description="Freeze", level_threshold=80, identity_fit=["Rebel", "Challenger"], goal_fit="Energy", media_url="url", script_template="tpl"),
            Ritual(id="r3", name="Journaling", description="Write", level_threshold=40, identity_fit=["Seeker", "Nurturer"], goal_fit="Clarity", media_url="url", script_template="tpl"),
            Ritual(id="r4", name="Power Walk", description="Walk", level_threshold=30, identity_fit=["Maker", "Nurturer"], goal_fit="Energy", media_url="url", script_template="tpl"),
        ]

    def generate_schedule(self, user: UserProfile) -> ProgramSchedule:
        """
        Generates a 30-day schedule based on user capacity and identity.
        """
        schedule = []
        
        # Logic: Determine starting intensity
        start_intensity = "Micro"
        if user.capacity_score > 70:
            start_intensity = "Heroic"
        elif user.capacity_score > 40:
            start_intensity = "Standard"
            
        # Filter rituals by identity (soft filter) and intensity (hard filter for week 1)
        suitable_rituals = [r for r in self.pantry if user.identity_pillar in r.identity_fit]
        if not suitable_rituals:
            suitable_rituals = self.pantry # Fallback to all if no identity match
            
        for day in range(1, 31):
            # Week 1: Strict Adherence to Capacity
            current_intensity = start_intensity
            
            # Week 2+: Progressive Overload (Simple Logic)
            if day > 7 and start_intensity == "Micro":
                current_intensity = "Standard"
            
            # Select Ritual
            # In a real app, we'd have more complex selection logic per day
            # Here we just pick a random suitable one that fits the intensity roughly
            # For MVP, just picking from suitable_rituals
            
            selected = random.choice(suitable_rituals)
            
            # Override for Micro-Habit week if needed
            if current_intensity == "Micro" and selected.level_threshold > 20:
                # Find a micro habit
                micro_habits = [r for r in self.pantry if r.level_threshold <= 20]
                if micro_habits:
                    selected = random.choice(micro_habits)
            
            schedule.append(DailyTask(
                day=day,
                ritual_id=selected.id,
                ritual_name=selected.name,
                intensity=current_intensity
            ))
            
        return ProgramSchedule(user_id=user.id, schedule=schedule)

# Global Instance
atlas = AtlasService()
