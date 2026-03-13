"""
CCP Distribution Pipeline
Task 4.10 — Prepares approved content for posting.

Receives an approved Asset ID and:
1. Generates posting-ready files
2. Attaches posting notes
3. Updates Receipt Chain
4. Marks Notion status as "Ready to Post"
5. Notifies coach via Notion
"""

import json
from pathlib import Path
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.services.notion_sync import NotionSync
from src.ccp.services.posting_notes import PostingNotesGenerator


class DistributionPipeline:
    """Prepare approved content for distribution."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.notion = NotionSync(coach_acronym=self.coach_acronym)
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)
        self.posting_gen = PostingNotesGenerator(coach_acronym=self.coach_acronym)

    async def distribute(
        self, page_id: str, asset_id: str = ""
    ) -> dict:
        """Run the distribution pipeline for an approved content piece.

        Args:
            page_id: Notion page ID of the approved content
            asset_id: Optional Asset ID

        Returns:
            Distribution result dict
        """
        # 1. Get the page content
        page = await self.notion.get_page(page_id)
        properties = page.get("properties", {})

        # Extract format
        format_select = properties.get("Format", {}).get("select", {})
        format_label = format_select.get("name", "Post")

        # Extract title
        title_arr = properties.get("Name", {}).get("title", [])
        title = title_arr[0].get("plain_text", "Untitled") if title_arr else "Untitled"

        # 2. Generate posting notes
        posting_notes = await self.posting_gen.generate(
            format_label=format_label,
            title=title,
            asset_id=asset_id,
        )

        # 3. Append posting notes to the page
        blocks = [
            self.notion.divider(),
            self.notion.heading_2("📋 Posting Notes (Auto-Generated)"),
            self.notion.callout(
                posting_notes.get("summary", "Ready to post."),
                emoji="📤",
                color="green_background",
            ),
        ]

        # Add platform-specific notes
        for platform, notes in posting_notes.get("platforms", {}).items():
            blocks.append(self.notion.toggle(
                f"📱 {platform}",
                children=[self.notion.paragraph(notes)]
            ))

        await self.notion.append_blocks(page_id, blocks)

        # 4. Update status to Ready to Post
        await self.notion.update_page(page_id, {
            "Status": {"select": {"name": "Ready to Post"}},
        })

        # 5. Log
        self.receipt_chain.log(
            agent_id="distribution",
            action="prepare_for_posting",
            asset_id=asset_id,
            output_summary=f"Ready to post: {title} ({format_label})",
            decision="ready_to_post",
            metadata={
                "page_id": page_id,
                "format": format_label,
                "platforms": list(posting_notes.get("platforms", {}).keys()),
            },
        )

        return {
            "status": "ready_to_post",
            "page_id": page_id,
            "asset_id": asset_id,
            "format": format_label,
            "posting_notes": posting_notes,
        }
