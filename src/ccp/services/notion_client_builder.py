"""
CCP Client Page Builder
Task 4.03 — Creates/updates Client Intelligence entries in Notion.

Surfaces the psychological profile as clean narrative.
Populates properties: Person ID, Status, Ritual Streak, Sentiment Trend.
Adds pattern alerts as Notion comments.
"""

import json
from datetime import datetime, timezone
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.services.notion_sync import NotionSync


class NotionClientBuilder:
    """Build and maintain Client Intelligence pages in Notion."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.notion = NotionSync(coach_acronym=self.coach_acronym)
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)

    async def create_client_page(
        self,
        database_id: str,
        person_id: str,
        name: str,
        context_narrative: str = "",
        status: str = "Active",
        ritual_streak: int = 0,
        sentiment: str = "neutral",
    ) -> dict:
        """Create a new Client Intelligence page.

        Args:
            database_id: Notion Client Intelligence database ID
            person_id: Client Person ID (CCC-NNNN)
            name: Client display name
            context_narrative: Context Premise narrative
            status: Client status (Active, Dormant, New, Graduating)
            ritual_streak: Current engagement streak
            sentiment: Current sentiment trend

        Returns:
            Created Notion page data
        """
        properties = {
            "Name": {"title": [{"text": {"content": name}}]},
            "Person ID": {"rich_text": [{"text": {"content": person_id}}]},
            "Status": {"select": {"name": status}},
            "Ritual Streak": {"number": ritual_streak},
            "Sentiment": {"select": {"name": sentiment}},
        }

        children = []

        # Profile section
        children.append(self.notion.heading_2("👤 Profile"))
        children.append(self.notion.callout(
            f"Person ID: {person_id}\nStatus: {status}\nStreak: {ritual_streak} days",
            emoji="📋", color="blue_background",
        ))
        children.append(self.notion.divider())

        # Context Premise section
        children.append(self.notion.heading_2("🧠 Context Premise"))
        if context_narrative:
            for line in context_narrative.split("\n"):
                if line.strip():
                    if line.startswith("**"):
                        children.append(self.notion.paragraph(line.strip("* "), bold=True))
                    else:
                        children.append(self.notion.paragraph(line))
        else:
            children.append(self.notion.callout(
                "Context building from conversations...", emoji="🔄", color="gray_background"
            ))
        children.append(self.notion.divider())

        # Emotional Arc section
        children.append(self.notion.heading_2("📈 Emotional Arc"))
        children.append(self.notion.callout(
            f"Current sentiment: {sentiment}", emoji="💭",
            color="green_background" if sentiment == "improving" else
                  "red_background" if sentiment == "declining" else "default",
        ))
        children.append(self.notion.divider())

        # Voice Journal section (toggle)
        children.append(self.notion.heading_2("🎙️ Voice Journal"))
        children.append(self.notion.callout(
            "Voice note transcripts appear here as the client shares.", emoji="🎧", color="purple_background"
        ))
        children.append(self.notion.divider())

        # Pattern Alerts section
        children.append(self.notion.heading_2("⚠️ Pattern Alerts"))
        children.append(self.notion.paragraph("No alerts yet. Patterns are detected automatically.", color="gray"))

        result = await self.notion.create_page(database_id, properties, children)

        self.receipt_chain.log(
            agent_id="notion_client_builder",
            action="create_client_page",
            person_id=person_id,
            output_summary=f"Notion client page: {name} ({person_id})",
            decision="created",
            metadata={"page_id": result.get("id", "")},
        )

        return result

    async def update_context(
        self, page_id: str, context_narrative: str, sentiment: str = ""
    ) -> dict:
        """Update a client page's context and sentiment."""
        props = {}
        if sentiment:
            props["Sentiment"] = {"select": {"name": sentiment}}
        if props:
            await self.notion.update_page(page_id, props)

        # Append new context as a block
        blocks = [
            self.notion.callout(
                f"Updated {datetime.now(timezone.utc).strftime('%Y-%m-%d')}: {context_narrative}",
                emoji="🔄", color="yellow_background",
            )
        ]
        return await self.notion.append_blocks(page_id, blocks)

    async def add_pattern_alert(self, page_id: str, alert: str) -> dict:
        """Add a pattern alert as a callout block."""
        blocks = [
            self.notion.callout(
                f"🟡 {alert}", emoji="⚠️", color="yellow_background"
            )
        ]
        return await self.notion.append_blocks(page_id, blocks)

    async def update_streak(self, page_id: str, streak: int) -> dict:
        """Update the ritual streak counter."""
        return await self.notion.update_page(page_id, {
            "Ritual Streak": {"number": streak},
        })

    async def add_voice_transcript(
        self, page_id: str, transcript: str, duration_seconds: float = 0
    ) -> dict:
        """Add a voice note transcript to the Voice Journal."""
        blocks = [
            self.notion.toggle(
                f"🎙️ Voice note ({datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}) — {duration_seconds:.0f}s",
                children=[self.notion.paragraph(transcript)]
            )
        ]
        return await self.notion.append_blocks(page_id, blocks)
