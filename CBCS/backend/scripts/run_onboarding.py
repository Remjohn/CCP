import asyncio
import json
import os
from backend.core.setup_agents import valeriane, dilaya, CoachSoul, TribeSoul

# Mock Content for the "Coach" (The User)
# In a real app, this would come from uploaded videos/docs.
MOCK_COACH_CONTENT = """
I'm Coach Carter. My method is called the "Titan Protocol". It's about forging iron discipline through 
daily micro-habits. I promise that in 30 days, you will double your productivity or I quit.
I speak like a drill sergeant but with a heart of gold. I use metaphors about war, forging steel, and climbing mountains.
My tribe is "The Driftless Men" - guys who feel lost in their 30s. They fear being average. They crave legacy.
They say things like "grind", "locked in", and "zero compromise".
"""

LIBRARY_PATH = "backend/intelligence_library"

async def run_onboarding():
    print("--- Starting Coach Onboarding ---")
    
    # Ensure library exists
    os.makedirs(LIBRARY_PATH, exist_ok=True)

    # 1. Run Valeriane (Coach Soul)
    print("\n[Valeriane] Analyzing Coach Essence...")
    coach_result = await valeriane.run(MOCK_COACH_CONTENT)
    coach_soul: CoachSoul = coach_result.output
    
    print(f"  > Unique Mechanism: {coach_soul.unique_mechanism}")
    print(f"  > Promise: {coach_soul.promise}")
    
    # Save Coach Soul
    with open(f"{LIBRARY_PATH}/client_soul.json", "w") as f:
        json.dump(coach_soul.model_dump(), f, indent=2)
    print(f"  > Saved to {LIBRARY_PATH}/client_soul.json")

    # 2. Run Dilaya (Tribe Soul)
    print("\n[Dilaya] Scouting the Tribe...")
    tribe_result = await dilaya.run(MOCK_COACH_CONTENT)
    tribe_soul: TribeSoul = tribe_result.output
    
    print(f"  > Tribe: {tribe_soul.tribe_name}")
    print(f"  > Core Fears: {tribe_soul.core_fears}")
    
    # Save Tribe Soul
    with open(f"{LIBRARY_PATH}/tribe_soul.json", "w") as f:
        json.dump(tribe_soul.model_dump(), f, indent=2)
    print(f"  > Saved to {LIBRARY_PATH}/tribe_soul.json")
    
    print("\n--- Onboarding Complete ---")

if __name__ == "__main__":
    asyncio.run(run_onboarding())
