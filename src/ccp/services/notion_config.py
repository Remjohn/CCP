"""
CCP Notion Conditional Color Rules & Tabbed Layouts & Formula Properties
Tasks 4.06, 4.07, 4.08 — Configuration documentation and helper utilities.

These tasks are primarily Notion UI configuration (manual setup).
This module provides:
- Documented color rule definitions
- Formula property definitions
- Setup instructions for tabbed layouts
- A helper to validate the setup against expected configuration
"""

import json
from pathlib import Path
from typing import Optional


# ═══════════════════════════════════════════════════════════════
# TASK 4.06: Conditional Color Rules
# ═══════════════════════════════════════════════════════════════

CONDITIONAL_COLOR_RULES = {
    "content_calendar": {
        "description": "Content Calendar conditional colors based on status and dates",
        "rules": [
            {
                "name": "Overdue",
                "color": "🔴 Red",
                "condition": "Publish Date < Today AND Status != Published",
                "property": "Status",
            },
            {
                "name": "On Schedule",
                "color": "🟢 Green",
                "condition": "Publish Date > Today + 2 days AND Status = Approved",
                "property": "Status",
            },
            {
                "name": "Tomorrow",
                "color": "🟡 Yellow",
                "condition": "Publish Date = Tomorrow AND Status != Published",
                "property": "Status",
            },
            {
                "name": "Seasonal Match",
                "color": "🔵 Blue",
                "condition": "Content theme matches current seasonal influence stack",
                "property": "Custom (via formula)",
            },
        ],
    },
    "client_intelligence": {
        "description": "Client Intelligence colors based on engagement",
        "rules": [
            {
                "name": "Engaged",
                "color": "🟢 Green",
                "condition": "Ritual Streak > 3 AND Sentiment = improving",
                "property": "Status",
            },
            {
                "name": "Dormant",
                "color": "🔴 Red",
                "condition": "Last Active > 7 days ago",
                "property": "Status",
            },
            {
                "name": "Declining",
                "color": "🟡 Yellow",
                "condition": "Sentiment = declining OR Ritual Streak decreasing",
                "property": "Status",
            },
        ],
    },
    "photo_deck": {
        "description": "Photo Deck colors based on usage",
        "rules": [
            {
                "name": "Overused",
                "color": "🔴 Red",
                "condition": "Usage Count > 5",
                "property": "Status",
            },
            {
                "name": "Available",
                "color": "🟢 Green",
                "condition": "Usage Count <= 3",
                "property": "Status",
            },
        ],
    },
}


# ═══════════════════════════════════════════════════════════════
# TASK 4.07: Tabbed Layout Configuration
# ═══════════════════════════════════════════════════════════════

TABBED_LAYOUTS = {
    "content_pages": {
        "description": "Content Calendar page tabs",
        "tabs": [
            {
                "name": "📄 Script",
                "sections": ["Script", "Why This Post", "Leadership Farming"],
            },
            {
                "name": "🖼️ Visuals",
                "sections": ["Coach Photo", "Visual Assets"],
            },
            {
                "name": "📊 Metrics",
                "sections": ["Validation Score", "Posting Notes", "Voice Note"],
            },
        ],
    },
    "client_pages": {
        "description": "Client Intelligence page tabs",
        "tabs": [
            {
                "name": "👤 Profile",
                "sections": ["Profile", "Context Premise"],
            },
            {
                "name": "📝 Sessions",
                "sections": ["Emotional Arc", "Pattern Alerts"],
            },
            {
                "name": "🎙️ Voice Journal",
                "sections": ["Voice Journal"],
            },
        ],
    },
}


# ═══════════════════════════════════════════════════════════════
# TASK 4.08: Notion Formula Properties
# ═══════════════════════════════════════════════════════════════

NOTION_FORMULAS = {
    "countdown_pulse": {
        "name": "Countdown Pulse",
        "description": "Days until publish → emoji indicator",
        "formula": 'if(prop("Publish Date") == now(), "🔴 TODAY", '
                  'if(dateBetween(prop("Publish Date"), now(), "days") == 1, "🟡 TOMORROW", '
                  'if(dateBetween(prop("Publish Date"), now(), "days") < 0, "⚫ OVERDUE", '
                  'if(dateBetween(prop("Publish Date"), now(), "days") <= 3, "🟠 SOON", '
                  '"🟢 " + format(dateBetween(prop("Publish Date"), now(), "days")) + "d"))))',
        "applies_to": "content_calendar",
    },
    "progress_bar": {
        "name": "Progress Bar",
        "description": "Milestone ratio → emoji bar",
        "formula": 'if(prop("Status") == "Published", "████████ 100%", '
                  'if(prop("Status") == "Ready to Post", "██████░░ 75%", '
                  'if(prop("Status") == "Approved", "████░░░░ 50%", '
                  'if(prop("Status") == "In Review", "██░░░░░░ 25%", '
                  '"░░░░░░░░ 0%"))))',
        "applies_to": "content_calendar",
    },
    "engagement_heat": {
        "name": "Engagement Heat",
        "description": "Ritual Streak → text label",
        "formula": 'if(prop("Ritual Streak") >= 21, "🔥🔥🔥 ON FIRE", '
                  'if(prop("Ritual Streak") >= 14, "🔥🔥 HOT", '
                  'if(prop("Ritual Streak") >= 7, "🔥 WARM", '
                  'if(prop("Ritual Streak") >= 3, "☀️ BUILDING", '
                  '"❄️ COLD"))))',
        "applies_to": "client_intelligence",
    },
    "seasonal_indicator": {
        "name": "Seasonal Indicator",
        "description": "Month → seasonal color emoji",
        "formula": 'if(month(now()) <= 2 or month(now()) == 12, "❄️ Winter", '
                  'if(month(now()) <= 5, "🌸 Spring", '
                  'if(month(now()) <= 8, "☀️ Summer", '
                  '"🍂 Autumn")))',
        "applies_to": "content_calendar",
    },
}


class NotionConfigValidator:
    """Validate and document Notion workspace configuration."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()

    def export_setup_guide(self) -> str:
        """Export a human-readable setup guide for Notion configuration.

        These items require manual Notion UI setup:
        - Conditional colors (Notion filter views)
        - Tabbed layouts (Notion layout configuration)
        - Formula properties (copy into Notion formula fields)
        """
        lines = [
            f"# Notion Configuration Guide for {self.coach_acronym}",
            "",
            "## 🎨 Conditional Color Rules (Task 4.06)",
            "",
        ]

        for db_name, config in CONDITIONAL_COLOR_RULES.items():
            lines.append(f"### {db_name}")
            lines.append(config["description"])
            for rule in config["rules"]:
                lines.append(f"- {rule['color']} **{rule['name']}**: {rule['condition']}")
            lines.append("")

        lines.append("## 📑 Tabbed Layouts (Task 4.07)")
        lines.append("")
        for layout_name, config in TABBED_LAYOUTS.items():
            lines.append(f"### {layout_name}")
            for tab in config["tabs"]:
                lines.append(f"- **{tab['name']}**: {', '.join(tab['sections'])}")
            lines.append("")

        lines.append("## 🔢 Formula Properties (Task 4.08)")
        lines.append("")
        for formula_key, config in NOTION_FORMULAS.items():
            lines.append(f"### {config['name']}")
            lines.append(f"*{config['description']}*")
            lines.append(f"Database: `{config['applies_to']}`")
            lines.append(f"```")
            lines.append(config["formula"])
            lines.append(f"```")
            lines.append("")

        return "\n".join(lines)

    def save_setup_guide(self) -> str:
        """Save the setup guide to docs."""
        guide = self.export_setup_guide()
        output_dir = Path(f"coaches/{self.coach_acronym}/config")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "notion_setup_guide.md"
        output_path.write_text(guide, encoding="utf-8")
        return str(output_path)
