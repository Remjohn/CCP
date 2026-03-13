"""
generator.py — Tier List & Rating Idea Generator

Reads weekly themes from dynamic_content_themes.json,
routes through archetype prompts, and calls OpenRouter
to generate tier list / rating video ideas.
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime, date

import httpx


# ── Archetype mapping ────────────────────────────────────────
ARCHETYPE_FILES = {
    "tierlist": {
        "authority":     "tier_lists/✨ The Authority Tier List Script.md",
        "controversial": "tier_lists/✨The Controversial Tier List Script.md",
        "red-flag":      "tier_lists/✨The Red Flag Tier List Script.md",
        "relatable":     "tier_lists/✨ The Relatable Tier List Script.md",
    },
    "rating": {
        "authority":     "ratings/✨ The Authority Rating Script.md",
        "controversial": "ratings/✨The Controversial Rating Script.md",
        "roast":         "ratings/✨The Roast Rating Script.md",
        "relatable":     "ratings/✨ The Relatable Rating Script.md",
    },
}

# ── Default system prompt for idea generation ────────────────
IDEA_SYSTEM_PROMPT = """You are a creative content strategist for a coaching brand.
You generate tier list and rating video ideas that are viral, specific, and aligned with the coach's brand.

RULES:
1. Each idea must have a TITLE (punchy, YouTube-worthy) and a DESCRIPTION (2-3 lines explaining the angle)
2. The title must be specific — never generic
3. The idea must be achievable as a recording session (filmable in 1 sitting)
4. The idea must naturally fit the archetype's emotional angle
5. Output ONLY valid JSON — no markdown, no code fences
"""


def resolve_week_id(target_date: date = None) -> str:
    """Return ISO week ID like '2026-W08'."""
    d = target_date or date.today()
    return f"{d.isocalendar()[0]}-W{d.isocalendar()[1]:02d}"


def find_latest_themes(coach_project_dir: str, week_id: str = None) -> dict | None:
    """
    Find the most recent dynamic_content_themes.json.
    If week_id is given, look for that specific week.
    Otherwise, find the latest available.
    """
    weekly_dir = Path(coach_project_dir) / "intelligence" / "weekly"
    if not weekly_dir.exists():
        return None

    if week_id:
        theme_file = weekly_dir / week_id / "dynamic_content_themes.json"
        if theme_file.exists():
            return json.loads(theme_file.read_text(encoding="utf-8"))
        return None

    # Find the most recent week folder
    week_dirs = sorted(
        [d for d in weekly_dir.iterdir() if d.is_dir()],
        key=lambda d: d.name,
        reverse=True,
    )
    for wd in week_dirs:
        theme_file = wd / "dynamic_content_themes.json"
        if theme_file.exists():
            return json.loads(theme_file.read_text(encoding="utf-8"))

    return None


def load_archetype_prompt(archetype_dir: str, content_format: str, archetype_name: str) -> str:
    """Load the archetype prompt markdown file."""
    fmt_key = "rating" if content_format == "rating" else "tierlist"
    file_map = ARCHETYPE_FILES.get(fmt_key, {})
    filename = file_map.get(archetype_name)
    if not filename:
        raise ValueError(f"Unknown archetype '{archetype_name}' for format '{content_format}'")

    filepath = Path(archetype_dir) / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Archetype file not found: {filepath}")

    return filepath.read_text(encoding="utf-8")


def load_project_context(coach_project_dir: str) -> dict | None:
    """Load the coach's project_context.json for brand/pillar data."""
    ctx_file = Path(coach_project_dir) / "intelligence" / "project_context.json"
    if ctx_file.exists():
        return json.loads(ctx_file.read_text(encoding="utf-8"))
    return None


def determine_format_for_week(config: dict, week_id: str) -> str:
    """Determine whether this week is tierlist or rating based on config."""
    fmt = config.get("content", {}).get("format", "mixed")
    if fmt in ("tierlist", "rating"):
        return fmt

    if fmt == "mixed":
        # Extract week number, odd = tierlist, even = rating
        match = re.search(r"W(\d+)", week_id)
        if match:
            week_num = int(match.group(1))
            return "tierlist" if week_num % 2 == 1 else "rating"
        return "tierlist"

    # "auto" — let the AI decide per idea (we default to mixed behavior)
    return "mixed"


def select_archetypes(config: dict, count: int = 3) -> list[str]:
    """Pick archetypes for this week's ideas based on coach preferences."""
    preferred = config.get("content", {}).get("preferred_archetypes", [
        "authority", "controversial", "roast", "relatable"
    ])
    # Cycle through preferences to fill count
    selected = []
    for i in range(count):
        selected.append(preferred[i % len(preferred)])
    return selected


def build_idea_prompt(
    theme: dict,
    archetype_text: str,
    content_format: str,
    archetype_name: str,
    coach_context: dict | None = None,
) -> str:
    """Build the user prompt for idea generation."""
    coach_info = ""
    if coach_context:
        brand = coach_context.get("brand_identity", {})
        project = coach_context.get("project", {})
        coach_info = f"""
COACH: {project.get('coach_display_name', 'Unknown')}
BRAND ENEMY: {brand.get('enemy', {}).get('name', 'N/A')}
BRAND PROMISE: {brand.get('promise', {}).get('one_liner', 'N/A')}
"""

    format_label = "TIER LIST" if content_format == "tierlist" else "RATING"

    return f"""Generate ONE {format_label} video idea using the "{archetype_name}" emotional angle.

{coach_info}

WEEKLY THEME:
{json.dumps(theme, indent=2, ensure_ascii=False)}

ARCHETYPE REFERENCE (use the emotional angle and structural approach from this):
{archetype_text[:2000]}

OUTPUT FORMAT (strict JSON, no markdown fences):
{{
  "title": "Punchy YouTube title for the video",
  "description": "2-3 line description of the content angle, what to rank/rate, and why it fits this archetype",
  "format": "{content_format}",
  "archetype": "{archetype_name}",
  "estimated_duration": "6-8 min"
}}
"""


async def generate_ideas(
    coach_config: dict,
    coach_project_dir: str,
    archetype_base_dir: str,
    week_id: str = None,
    dry_run: bool = False,
) -> list[dict]:
    """
    Generate N tier list / rating ideas for the coach.

    Returns a list of idea dicts: [{title, description, format, archetype}, ...]
    """
    # Resolve week
    wid = week_id or resolve_week_id()

    # Load themes
    themes = find_latest_themes(coach_project_dir, wid)
    if not themes:
        # Fall back to latest available
        themes = find_latest_themes(coach_project_dir)
    if not themes:
        raise FileNotFoundError(
            f"No dynamic_content_themes.json found in {coach_project_dir}/intelligence/weekly/"
        )

    # Load coach context
    coach_context = load_project_context(coach_project_dir)

    # Determine format & archetypes
    content_format = determine_format_for_week(coach_config, wid)
    ideas_count = coach_config.get("content", {}).get("ideas_per_week", 3)
    archetypes = select_archetypes(coach_config, ideas_count)

    # Extract theme list (handle both list and dict shapes)
    if isinstance(themes, list):
        theme_list = themes
    elif isinstance(themes, dict):
        theme_list = themes.get("themes", themes.get("content_themes", [themes]))
    else:
        theme_list = [themes]

    # Generate ideas
    ideas = []
    api_key = os.environ.get("OPENROUTER_API_KEY", "")

    for i in range(ideas_count):
        archetype_name = archetypes[i]
        theme = theme_list[i % len(theme_list)] if theme_list else {}

        # For "mixed" auto format, alternate per idea
        if content_format == "mixed":
            fmt = "tierlist" if i % 2 == 0 else "rating"
        else:
            fmt = content_format

        # Map archetype name for format compatibility
        arch_name = archetype_name
        if fmt == "tierlist" and arch_name == "roast":
            arch_name = "red-flag"  # tierlist doesn't have roast, fallback to red-flag

        try:
            archetype_text = load_archetype_prompt(archetype_base_dir, fmt, arch_name)
        except (ValueError, FileNotFoundError):
            archetype_text = f"Use the '{arch_name}' emotional angle: be {arch_name} in your approach."

        user_prompt = build_idea_prompt(theme, archetype_text, fmt, arch_name, coach_context)

        if dry_run:
            # Synthetic idea for dry run
            ideas.append({
                "title": f"[DRY RUN] {fmt.title()} Idea #{i+1} — {arch_name.title()}",
                "description": f"Based on theme: {theme.get('theme', theme.get('name', 'unknown'))}. "
                               f"Archetype: {arch_name}. Format: {fmt}.",
                "format": fmt,
                "archetype": arch_name,
                "estimated_duration": "6-8 min",
            })
            continue

        # Call OpenRouter
        if not api_key:
            raise EnvironmentError("OPENROUTER_API_KEY not set. Add it to .env file.")

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "google/gemini-2.5-flash",
                    "messages": [
                        {"role": "system", "content": IDEA_SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": 0.85,
                    "max_tokens": 500,
                },
            )
            response.raise_for_status()
            result = response.json()

        raw_text = result["choices"][0]["message"]["content"].strip()

        # Parse JSON from response (handle markdown fences)
        json_text = raw_text
        if "```" in json_text:
            # Extract JSON from code fences
            match = re.search(r"```(?:json)?\s*([\s\S]*?)```", json_text)
            if match:
                json_text = match.group(1).strip()

        try:
            idea = json.loads(json_text)
        except json.JSONDecodeError:
            idea = {
                "title": f"{fmt.title()} Idea #{i+1}",
                "description": raw_text[:200],
                "format": fmt,
                "archetype": arch_name,
                "estimated_duration": "6-8 min",
            }

        ideas.append(idea)

    return ideas


def save_ideas(ideas: list[dict], coach_project_dir: str, week_id: str = None):
    """Save generated ideas to the weekly folder."""
    wid = week_id or resolve_week_id()
    output_dir = Path(coach_project_dir) / "intelligence" / "weekly" / wid
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "tierlist_rating_ideas.json"
    output_file.write_text(
        json.dumps({
            "generated_at": datetime.now().isoformat(),
            "week_id": wid,
            "ideas": ideas,
        }, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return output_file
