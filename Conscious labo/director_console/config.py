# Configuration for CMF Director's Console V2

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Base paths
CMF_ROOT = Path("D:/Work/The Conscious Movie Factory December")
INPUTS_DIR = CMF_ROOT / "production"

# Database
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{Path(__file__).parent / 'cmf_database.db'}"
)

# ============================================================
# GAMIFICATION SETTINGS
# ============================================================
VIDEO_VALUE = 25  # Value in $ per completed video
MONTHLY_GOAL = 160  # Videos per month target (40/week x 4)
WEEKLY_GOAL = 40  # Videos per week target
DAILY_GOAL = 8  # Videos per day target (40/5 workdays)

# Currency symbol
CURRENCY = "$"

# ============================================================
# APPROVAL STAGES
# ============================================================
APPROVAL_STAGES = [
    {"id": "scripts", "name": "Scripts", "icon": "📝", "order": 1},
    {"id": "assets", "name": "Assets", "icon": "🎨", "order": 2},
    {"id": "composition", "name": "Composition", "icon": "🎬", "order": 3},
    {"id": "audio", "name": "Audio", "icon": "🔊", "order": 4},
]

# ============================================================
# ASSET TYPES
# ============================================================
ASSET_TYPES = {
    "hero": "Hero Frame (HERO.png)",
    "lit": "Lit Frame (HERO_LIT.png)",
    "start": "Start Frame (HERO_START.png)",
    "icon_raw": "Icon B-Roll (ICON_RAW.mp4)",
    "icon_fx": "Composited Scene (ICON_FX.mov)",
    "d_roll": "D-Roll (authentic footage)",
    "e_roll": "E-Roll (cultural clips)",
    "c_roll": "C-Roll (kinetic typography)",
}

# ============================================================
# FILE PATTERNS
# ============================================================
FILE_PATTERNS = {
    "transcript": ["🎙️*TRANSCRIPT*.md", "*TRANSCRIPT*.md"],
    "premise": ["*premise_analysis*.json"],
    "script": ["*final_script*.json"],
    "blueprint": ["*production_blueprint*.json", "*BLUEPRINT*.md"],
    "storyboard": ["*storyboard*.md"],
    "hero": ["*HERO.png"],
    "icon_raw": ["*ICON_RAW*.mp4"],
    "icon_fx": ["*ICON_FX*.mov"],
    "draft": ["DRAFT*.mp4"],
}

# ============================================================
# COACH TEMPLATE FILES
# ============================================================
COACH_TEMPLATE_FILES = [
    ("{name} 🟨 Tribe Soul Profile 🟨.md", "# Tribe Soul Profile: {name}\n\n## Demographic Reality\n\n## Generational Markers\n\n## Cultural Heroes\n\n## Shared Enemies\n"),
    ("🟨 {name} Philosophy 🟨.md", "# {name} Philosophy\n\n## Core Beliefs\n\n## Worldview\n\n## Key Messages\n"),
    ("{name} branding.json", '{{\n  "coach_name": "{name}",\n  "primary_color": "#000000",\n  "secondary_color": "#FFFFFF",\n  "font_family": "Inter",\n  "logo_path": null\n}}'),
    ("💰 {name} - BUSINESS MODEL.md", "# {name} - Business Model\n\n## Programs\n\n## Pricing\n\n## Target Audience\n"),
    ("🔢 {name} - 7-11-4 SOPHISTICATION.md", "# {name} - 7-11-4 Trust Framework\n\n## 7 Hours of Content\n\n## 11 Interactions\n\n## 4 Locations\n"),
    ("🎯 {name} - PRODUCTION BIBLE.md", "# {name} - Production Bible\n\n## Visual Style\n\n## Tone & Voice\n\n## Brand Guidelines\n"),
    ("Conscious_Soul_Values.md", "# {name} - Core Values\n\n## Value 1\n\n## Value 2\n\n## Value 3\n"),
]
