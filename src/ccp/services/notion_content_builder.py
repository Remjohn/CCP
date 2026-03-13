"""
CCP Content Page Builder
Task 4.02 — Creates Content Calendar entries with 7 structured sections.

Sections:
  🎙️ Voice Note (audio block)
  💡 Why This Post
  🌱 Leadership Farming
  📄 Script
  📸 Coach Photo
  🖼️ Visual Assets
  📋 Posting Notes

Uses callout blocks, toggles, dividers, colored text — not plain paragraphs.
"""

import json
from datetime import datetime, timezone
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.services.notion_sync import NotionSync


class NotionContentBuilder:
    """Build rich Content Calendar pages in Notion."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.notion = NotionSync(coach_acronym=self.coach_acronym)
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)

    async def create_content_page(
        self,
        database_id: str,
        asset_id: str,
        title: str,
        format_label: str,
        script: str,
        why_this_post: str = "",
        leadership_trait: str = "",
        voice_note_url: str = "",
        photo_url: str = "",
        visual_urls: list[str] = None,
        posting_notes: str = "",
        publish_date: Optional[datetime] = None,
    ) -> dict:
        """Create a fully structured Content Calendar page.

        Args:
            database_id: Notion Content Calendar database ID
            asset_id: Universal Asset ID
            title: Content title
            format_label: Format type (Thread, Carousel, Reel, etc.)
            script: The content script
            why_this_post: Strategic rationale
            leadership_trait: Target leadership dimension
            voice_note_url: Optional Supabase audio URL
            photo_url: Optional coach photo URL
            visual_urls: Optional list of visual asset URLs
            posting_notes: Platform-specific posting instructions
            publish_date: Target publish date

        Returns:
            Created Notion page data
        """
        # Build properties
        properties = {
            "Name": {"title": [{"text": {"content": title}}]},
            "Asset ID": {"rich_text": [{"text": {"content": asset_id}}]},
            "Format": {"select": {"name": format_label}},
            "Status": {"select": {"name": "Draft"}},
        }
        if publish_date:
            properties["Publish Date"] = {
                "date": {"start": publish_date.strftime("%Y-%m-%d")}
            }

        # Build page content blocks (the 7 sections)
        children = []

        # Section 1: 🎙️ Voice Note
        children.append(self.notion.heading_2("🎙️ Voice Note"))
        if voice_note_url:
            children.append(self.notion.audio_block(voice_note_url))
            children.append(self.notion.paragraph("Tap to listen to the coach's voice note for this piece.", color="gray"))
        else:
            children.append(self.notion.callout("No voice note attached.", emoji="🔇", color="gray_background"))
        children.append(self.notion.divider())

        # Section 2: 💡 Why This Post
        children.append(self.notion.heading_2("💡 Why This Post"))
        if why_this_post:
            children.append(self.notion.callout(why_this_post, emoji="🎯", color="blue_background"))
        else:
            children.append(self.notion.paragraph("Strategic rationale will be generated.", color="gray"))
        children.append(self.notion.divider())

        # Section 3: 🌱 Leadership Farming
        children.append(self.notion.heading_2("🌱 Leadership Farming"))
        if leadership_trait:
            children.append(self.notion.callout(
                f"This piece exercises: {leadership_trait}",
                emoji="🌱",
                color="green_background",
            ))
        children.append(self.notion.divider())

        # Section 4: 📄 Script
        children.append(self.notion.heading_2("📄 Script"))
        # Split script into paragraphs for readability
        paragraphs = script.split("\n\n") if script else ["Script pending..."]
        for para in paragraphs:
            if para.strip():
                children.append(self.notion.paragraph(para.strip()))
        children.append(self.notion.divider())

        # Section 5: 📸 Coach Photo
        children.append(self.notion.heading_2("📸 Coach Photo"))
        if photo_url:
            children.append(self.notion.image_block(photo_url, caption="Selected coach photo"))
        else:
            children.append(self.notion.callout("Select a photo from the Photo Deck.", emoji="📷", color="yellow_background"))
        children.append(self.notion.divider())

        # Section 6: 🖼️ Visual Assets
        children.append(self.notion.heading_2("🖼️ Visual Assets"))
        if visual_urls:
            for url in visual_urls:
                children.append(self.notion.image_block(url))
        else:
            children.append(self.notion.callout("Visual assets will be generated.", emoji="🎨", color="purple_background"))
        children.append(self.notion.divider())

        # Section 7: 📋 Posting Notes
        children.append(self.notion.heading_2("📋 Posting Notes"))
        if posting_notes:
            children.append(self.notion.toggle("View posting instructions", [
                self.notion.paragraph(posting_notes)
            ]))
        else:
            children.append(self.notion.paragraph("Posting notes will be generated after approval.", color="gray"))

        # Create the page
        result = await self.notion.create_page(database_id, properties, children)
        page_id = result.get("id", "")

        self.receipt_chain.log(
            agent_id="notion_content_builder",
            action="create_content_page",
            asset_id=asset_id,
            output_summary=f"Notion page: {title} ({format_label})",
            decision="created",
            metadata={"page_id": page_id, "format": format_label},
        )

        return result

    async def update_status(self, page_id: str, status: str) -> dict:
        """Update a content page's status."""
        return await self.notion.update_page(page_id, {
            "Status": {"select": {"name": status}},
        })
