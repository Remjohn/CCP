"""
CCP Coach Repo Scaffolder
Task 1.01 — Creates the canonical directory layout for a new coach instance.

Usage:
    python -m src.ccp.scripts.scaffold_coach --coach-name "Nadia Lefèvre" --acronym NDL --output ./coaches/NDL
"""

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path


COACH_DIRECTORIES = [
    "config",
    "intelligence/research",
    "intelligence/tribe",
    "intelligence/memory/working",
    "intelligence/memory/episodic",
    "intelligence/memory/semantic",
    "production/scripts",
    "production/visuals",
    "production/audio",
    "production/webinars",
    "production/tierlists",
    "production/exports",
    "logs/receipt_chain",
    "logs/pipeline",
    "clients",
    "branding/photos",
]

TEMPLATE_FILES = {
    "config/coach_registry.json": lambda name, acronym: json.dumps(
        {
            "coach_name": name,
            "coach_acronym": acronym,
            "coach_id": f"{acronym}-0000",
            "next_client_id": 1,
            "notion_workspace_id": "",
            "notion_token_ref": f"NOTION_TOKEN_{acronym}",
            "supabase_bucket": f"coach-{acronym.lower()}",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        indent=2,
    ),
    "config/coach_soul.json": lambda name, acronym: json.dumps(
        {
            "version": 1,
            "coach_name": name,
            "coach_id": f"{acronym}-0000",
            "voice_dna": {
                "sentence_rhythm": [],
                "metaphor_patterns": [],
                "vocabulary_fingerprint": [],
                "emotional_peak_markers": [],
                "pause_cadence": None,
                "humor_style": None,
                "ttt_baseline_hash": None,
            },
            "coaching_philosophy": "",
            "core_message": "",
            "tribe_archetype": "",
            "ideal_client": {
                "demographics": "",
                "psychographics": "",
                "pain_points": [],
                "aspirations": [],
            },
            "leadership_scores": {
                "deep_empathy": 0,
                "authentic_vulnerability": 0,
                "embodied_confidence": 0,
                "strategic_patience": 0,
                "radical_honesty": 0,
                "grounded_presence": 0,
                "visionary_clarity": 0,
                "playful_irreverence": 0,
                "fierce_compassion": 0,
                "sacred_boundaries": 0,
                "intuitive_timing": 0,
                "sovereign_authority": 0,
            },
            "content_tone": {
                "warmth": 0.0,
                "directness": 0.0,
                "humor_weight": 0.0,
                "formality": 0.0,
            },
            "signature_frameworks": [],
            "competitive_positioning": "",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        indent=2,
    ),
    "config/.env.template": lambda name, acronym: "\n".join(
        [
            f"# Environment variables for coach: {name} ({acronym})",
            f"COACH_ACRONYM={acronym}",
            f"COACH_ID={acronym}-0000",
            "",
            "# Notion",
            f"NOTION_TOKEN_{acronym}=",
            "NOTION_CONTENT_CALENDAR_DB=",
            "NOTION_CLIENT_INTELLIGENCE_DB=",
            "NOTION_WEBINAR_ASSETS_DB=",
            "NOTION_PHOTO_DECK_DB=",
            "",
            "# Supabase",
            "SUPABASE_URL=",
            "SUPABASE_SERVICE_KEY=",
            "",
            "# LLM",
            "GEMINI_API_KEY=",
            "GROQ_API_KEY=",
            "",
            "# Telegram",
            "TELEGRAM_BOT_TOKEN=",
            "TELEGRAM_SECRET_TOKEN=",
            "",
            "# Neo4j",
            "NEO4J_URI=",
            "NEO4J_USER=",
            "NEO4J_PASSWORD=",
            "",
            "# Redis",
            "REDIS_URL=redis://localhost:6379/0",
        ]
    ),
}


def scaffold_coach(coach_name: str, acronym: str, output_dir: str) -> Path:
    """Create the full directory structure and template files for a new coach."""
    base = Path(output_dir)

    if base.exists() and any(base.iterdir()):
        raise FileExistsError(
            f"Directory {base} already exists and is not empty. "
            "Use a clean directory or remove existing files first."
        )

    # Create directories
    for directory in COACH_DIRECTORIES:
        dir_path = base / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        # Add .gitkeep to empty directories
        gitkeep = dir_path / ".gitkeep"
        if not any(dir_path.iterdir()):
            gitkeep.touch()

    # Create template files
    for filepath, generator in TEMPLATE_FILES.items():
        file_path = base / filepath
        file_path.parent.mkdir(parents=True, exist_ok=True)
        content = generator(coach_name, acronym)
        file_path.write_text(content, encoding="utf-8")

    # Create README
    readme_content = f"""# Coach Instance: {coach_name} ({acronym})

**Coach ID:** `{acronym}-0000`  
**Created:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')}

## Directory Structure

```
config/              — Coach identity, registry, environment
intelligence/        — Research, tribe data, 3-tier memory
  research/          — DEEP/FRESH research outputs
  tribe/             — Tribe distillation data
  memory/            — Working → Episodic → Semantic
production/          — All generated outputs
  scripts/           — Content scripts (SCRP assets)
  visuals/           — Visual assets (VIMG, QUOT, MEME)
  audio/             — Voice notes, Sacred Audio (SAUD, VOIC)
  webinars/          — Webinar packages (WBNR, WSLD)
  tierlists/         — Tierlist assets (TIER)
  exports/           — Final export files (.excalidraw, PDF)
logs/                — Receipt Chain + pipeline logs
clients/             — Per-client data directories
branding/photos/     — Personal Branding Photo Deck source files
```
"""
    (base / "README.md").write_text(readme_content, encoding="utf-8")

    return base


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a new CCP coach instance directory"
    )
    parser.add_argument(
        "--coach-name",
        required=True,
        help='Full name of the coach (e.g. "Nadia Lefèvre")',
    )
    parser.add_argument(
        "--acronym",
        required=True,
        help="3-letter coach acronym (e.g. NDL)",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output directory path (e.g. ./coaches/NDL)",
    )
    args = parser.parse_args()

    # Validate acronym
    if len(args.acronym) != 3 or not args.acronym.isalpha():
        parser.error("Acronym must be exactly 3 alphabetic characters")

    acronym = args.acronym.upper()

    try:
        result = scaffold_coach(args.coach_name, acronym, args.output)
        print(f"✅ Coach instance scaffolded at: {result}")
        print(f"   Coach ID: {acronym}-0000")
        print(f"   Next steps:")
        print(f"   1. Fill in config/.env.template and rename to .env")
        print(f"   2. Run the Genesis Pipeline: ccf-init")
    except FileExistsError as e:
        print(f"❌ {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
