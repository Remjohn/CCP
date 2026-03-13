"""
CCP Notion Workspace Provisioner
Task 4.05 — Creates the 4 databases in a coach's Notion workspace.

Databases:
  1. Content Calendar — all content pieces with 7 sections
  2. Client Intelligence — client profiles with Context Premises
  3. Webinar & Tierlist Assets — V²WS modules and tier lists
  4. Personal Branding Photo Deck — coach photos with usage tracking
"""

import json
from pathlib import Path
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.services.notion_sync import NotionSync


# Database property schemas
CONTENT_CALENDAR_PROPS = {
    "Name": {"title": {}},
    "Asset ID": {"rich_text": {}},
    "Format": {
        "select": {
            "options": [
                {"name": "Thread", "color": "blue"},
                {"name": "Carousel", "color": "purple"},
                {"name": "Reel", "color": "pink"},
                {"name": "Quote Card", "color": "yellow"},
                {"name": "Meme", "color": "orange"},
                {"name": "Article", "color": "green"},
                {"name": "Newsletter", "color": "red"},
                {"name": "Podcast Clip", "color": "brown"},
                {"name": "Live Recap", "color": "gray"},
                {"name": "Story Series", "color": "default"},
                {"name": "Poll", "color": "blue"},
                {"name": "Community Post", "color": "green"},
                {"name": "Video Essay", "color": "red"},
                {"name": "Micro-Workshop", "color": "purple"},
            ]
        }
    },
    "Status": {
        "select": {
            "options": [
                {"name": "Draft", "color": "gray"},
                {"name": "In Review", "color": "yellow"},
                {"name": "Approved", "color": "green"},
                {"name": "Ready to Post", "color": "blue"},
                {"name": "Published", "color": "purple"},
                {"name": "Rejected", "color": "red"},
            ]
        }
    },
    "Publish Date": {"date": {}},
    "Leadership Trait": {"rich_text": {}},
    "Validation Score": {"number": {"format": "percent"}},
}

CLIENT_INTELLIGENCE_PROPS = {
    "Name": {"title": {}},
    "Person ID": {"rich_text": {}},
    "Status": {
        "select": {
            "options": [
                {"name": "New", "color": "blue"},
                {"name": "Active", "color": "green"},
                {"name": "Declining", "color": "yellow"},
                {"name": "Dormant", "color": "red"},
                {"name": "Graduating", "color": "purple"},
            ]
        }
    },
    "Ritual Streak": {"number": {"format": "number"}},
    "Sentiment": {
        "select": {
            "options": [
                {"name": "improving", "color": "green"},
                {"name": "stable", "color": "blue"},
                {"name": "declining", "color": "red"},
                {"name": "neutral", "color": "gray"},
            ]
        }
    },
    "Last Active": {"date": {}},
    "Telegram ID": {"rich_text": {}},
}

WEBINAR_ASSETS_PROPS = {
    "Name": {"title": {}},
    "Asset ID": {"rich_text": {}},
    "Type": {
        "select": {
            "options": [
                {"name": "Webinar Module", "color": "blue"},
                {"name": "Tier List", "color": "purple"},
                {"name": "Visual Asset", "color": "green"},
                {"name": "Excalidraw", "color": "orange"},
            ]
        }
    },
    "Status": {
        "select": {
            "options": [
                {"name": "Draft", "color": "gray"},
                {"name": "Complete", "color": "green"},
                {"name": "In Use", "color": "blue"},
            ]
        }
    },
    "Module Number": {"number": {"format": "number"}},
    "Duration (min)": {"number": {"format": "number"}},
}

PHOTO_DECK_PROPS = {
    "Name": {"title": {}},
    "Asset ID": {"rich_text": {}},
    "Usage Count": {"number": {"format": "number"}},
    "Status": {
        "select": {
            "options": [
                {"name": "Available", "color": "green"},
                {"name": "Overused", "color": "red"},
                {"name": "Reserved", "color": "yellow"},
            ]
        }
    },
    "Tags": {"multi_select": {
        "options": [
            {"name": "Portrait", "color": "blue"},
            {"name": "Action", "color": "orange"},
            {"name": "Lifestyle", "color": "green"},
            {"name": "Professional", "color": "purple"},
            {"name": "Casual", "color": "pink"},
        ]
    }},
    "Storage URL": {"url": {}},
}


class NotionWorkspaceProvisioner:
    """Create and configure a coach's full Notion workspace."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.notion = NotionSync(coach_acronym=self.coach_acronym)
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)

    async def provision(self, parent_page_id: str) -> dict:
        """Create all 4 databases in the coach's Notion workspace.

        Args:
            parent_page_id: The Notion page ID to create databases under

        Returns:
            Dict mapping database names to their IDs
        """
        databases = {}

        # 1. Content Calendar
        result = await self.notion.create_database(
            parent_page_id, "📅 Content Calendar", CONTENT_CALENDAR_PROPS
        )
        databases["content_calendar"] = result.get("id", "")

        # 2. Client Intelligence
        result = await self.notion.create_database(
            parent_page_id, "🧠 Client Intelligence", CLIENT_INTELLIGENCE_PROPS
        )
        databases["client_intelligence"] = result.get("id", "")

        # 3. Webinar & Tierlist Assets
        result = await self.notion.create_database(
            parent_page_id, "🎬 Webinar & Tierlist Assets", WEBINAR_ASSETS_PROPS
        )
        databases["webinar_assets"] = result.get("id", "")

        # 4. Photo Deck
        result = await self.notion.create_database(
            parent_page_id, "📸 Personal Branding Photo Deck", PHOTO_DECK_PROPS
        )
        databases["photo_deck"] = result.get("id", "")

        # Save database IDs to config
        config_dir = Path(f"coaches/{self.coach_acronym}/config")
        config_dir.mkdir(parents=True, exist_ok=True)
        db_config = config_dir / "notion_databases.json"
        db_config.write_text(json.dumps(databases, indent=2), encoding="utf-8")

        self.receipt_chain.log(
            agent_id="workspace_provisioner",
            action="provision_workspace",
            output_summary=f"Created 4 databases: {', '.join(databases.keys())}",
            decision="completed",
            metadata=databases,
        )

        return databases
