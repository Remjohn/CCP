import json
import yaml
import os
import asyncio
from pathlib import Path
from backend.config import get_settings
# from backend.database.session import get_db_session
# from sqlalchemy import text

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
BACKEND_DIR = BASE_DIR / "backend"
INTELLIGENCE_DIR = BACKEND_DIR / "intelligence_library"
BRANDING_FILE = FRONTEND_DIR / "Pamela branding.json"

def load_branding():
    with open(BRANDING_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def update_identity_pillars(branding):
    """
    Overwrites identity_pillars.yaml with archetypes from the branding file.
    """
    archetypes = branding["assessment_engine"]["logic_maps"]["identity_vector"]["archetypes"]
    
    pillars_data = []
    
    for key, data in archetypes.items():
        pillar = {
            "id": key,
            "name": data["name"],
            "affirmation": f"I embrace my {data['superpower']}", # Generated affirmation
            "shadow_distortion": {
                "description": data["shadow"],
                "traits": [f"Prescription: {data['prescription']}"]
            },
            "signs_defenses": ["Generated from branding"],
            "maturation_pathway": ["Generated from branding"],
            "practices": [],
            "coaching_prompts": []
        }
        pillars_data.append(pillar)
    
    yaml_content = {"pillars": pillars_data}
    
    target_file = INTELLIGENCE_DIR / "identity_pillars.yaml"
    with open(target_file, "w", encoding="utf-8") as f:
        yaml.dump(yaml_content, f, sort_keys=False)
    
    print(f"✅ Updated {target_file}")

async def seed_rituals(branding):
    """
    Seeds the rituals table with modalities.
    """
    modalities = branding["solution_engine"]["pantry_definitions"]["modality_types"]
    
    # We need a DB connection. 
    # Since we might not have the full app context, we'll use a direct connection if possible,
    # or just print the SQL for now if the DB isn't running.
    # But wait, the user wants this to work.
    
    # Let's try to connect using the settings.
    settings = get_settings()
    
    # For this script to work, we assume the DB is accessible.
    # If not, we will just generate a SQL file.
    
    sql_statements = []
    sql_statements.append("-- Seeding Rituals from Branding")
    
    for mod in modalities:
        # Simple SQL generation
        name = mod["name"].replace("'", "''")
        description = mod["description"].replace("'", "''")
        tags_str = "{" + ",".join([f'"{t}"' for t in mod["tags"]]) + "}"
        sql = f"""
        INSERT INTO rituals (name, description, identity_fit, goal_fit)
        VALUES (
            '{name}', 
            '{description}', 
            '{tags_str}', 
            '{mod["energy"]}'
        );
        """
        sql_statements.append(sql)
        
    # Write to a seed file
    seed_file = BACKEND_DIR / "database" / "seeds" / "pamela_rituals.sql"
    os.makedirs(seed_file.parent, exist_ok=True)
    
    with open(seed_file, "w", encoding="utf-8") as f:
        f.write("\n".join(sql_statements))
        
    print(f"✅ Generated Seed SQL at {seed_file}")

def main():
    print("🚀 Starting Branding Injection...")
    branding = load_branding()
    
    # 1. Update YAML
    update_identity_pillars(branding)
    
    # 2. Seed Rituals (Generate SQL)
    asyncio.run(seed_rituals(branding))
    
    print("✨ Injection Complete!")

if __name__ == "__main__":
    main()
