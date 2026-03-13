"""
CCP Notion Sync Core
Task 4.01 — Python wrapper for the Notion API with rate limiting and retry.

Handles:
- Authentication via NOTION_TOKEN
- Rate limiting (3 req/s with backoff)
- Retry logic for transient errors
- Rich block creation helpers
- Error reporting
"""

import asyncio
import json
import os
import time
from typing import Any, Optional

from notion_client import AsyncClient
from notion_client.errors import APIResponseError

from src.ccp.core.receipt_chain import ReceiptChain


class NotionSync:
    """Core Notion API wrapper with rate limiting and retry."""

    MAX_RETRIES = 3
    RATE_LIMIT_DELAY = 0.35  # ~3 requests per second
    RETRY_BACKOFF = [1, 3, 10]  # Seconds between retries

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)
        self._client: Optional[AsyncClient] = None
        self._last_request_time = 0.0

    def _get_client(self) -> AsyncClient:
        """Lazy-init Notion client."""
        if self._client is None:
            token = os.getenv("NOTION_TOKEN", "")
            if not token:
                raise ValueError("NOTION_TOKEN environment variable not set")
            self._client = AsyncClient(auth=token)
        return self._client

    async def _rate_limit(self) -> None:
        """Enforce rate limiting between requests."""
        now = time.monotonic()
        elapsed = now - self._last_request_time
        if elapsed < self.RATE_LIMIT_DELAY:
            await asyncio.sleep(self.RATE_LIMIT_DELAY - elapsed)
        self._last_request_time = time.monotonic()

    async def _retry(self, operation: str, func, *args, **kwargs) -> Any:
        """Execute a Notion API call with retry logic."""
        for attempt in range(self.MAX_RETRIES):
            try:
                await self._rate_limit()
                return await func(*args, **kwargs)
            except APIResponseError as e:
                if e.status == 429:  # Rate limited
                    wait = self.RETRY_BACKOFF[min(attempt, len(self.RETRY_BACKOFF) - 1)]
                    await asyncio.sleep(wait)
                    continue
                if e.status >= 500:  # Server error
                    wait = self.RETRY_BACKOFF[min(attempt, len(self.RETRY_BACKOFF) - 1)]
                    await asyncio.sleep(wait)
                    continue
                raise  # Client error — don't retry
            except Exception:
                if attempt < self.MAX_RETRIES - 1:
                    await asyncio.sleep(1)
                    continue
                raise

    # ── Page Operations ──────────────────────────────────────────

    async def create_page(
        self, parent_db_id: str, properties: dict, children: list[dict] = None
    ) -> dict:
        """Create a new Notion page in a database."""
        client = self._get_client()
        payload = {
            "parent": {"database_id": parent_db_id},
            "properties": properties,
        }
        if children:
            payload["children"] = children

        result = await self._retry(
            "create_page", client.pages.create, **payload
        )
        return result

    async def update_page(self, page_id: str, properties: dict) -> dict:
        """Update an existing Notion page."""
        client = self._get_client()
        return await self._retry(
            "update_page", client.pages.update, page_id=page_id, properties=properties
        )

    async def append_blocks(self, page_id: str, children: list[dict]) -> dict:
        """Append child blocks to a page."""
        client = self._get_client()
        return await self._retry(
            "append_blocks",
            client.blocks.children.append,
            block_id=page_id,
            children=children,
        )

    async def get_page(self, page_id: str) -> dict:
        """Retrieve a page by ID."""
        client = self._get_client()
        return await self._retry("get_page", client.pages.retrieve, page_id=page_id)

    # ── Database Operations ──────────────────────────────────────

    async def create_database(
        self, parent_page_id: str, title: str, properties: dict
    ) -> dict:
        """Create a new Notion database."""
        client = self._get_client()
        return await self._retry(
            "create_database",
            client.databases.create,
            parent={"page_id": parent_page_id},
            title=[{"type": "text", "text": {"content": title}}],
            properties=properties,
        )

    async def query_database(
        self, database_id: str, filter_obj: dict = None, sorts: list = None
    ) -> list[dict]:
        """Query a Notion database with optional filters and sorts."""
        client = self._get_client()
        kwargs = {"database_id": database_id}
        if filter_obj:
            kwargs["filter"] = filter_obj
        if sorts:
            kwargs["sorts"] = sorts

        result = await self._retry("query_database", client.databases.query, **kwargs)
        return result.get("results", [])

    # ── Block Builders ───────────────────────────────────────────

    @staticmethod
    def heading_1(text: str, color: str = "default") -> dict:
        return {
            "object": "block", "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": text}}],
                "color": color,
            },
        }

    @staticmethod
    def heading_2(text: str, color: str = "default") -> dict:
        return {
            "object": "block", "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": text}}],
                "color": color,
            },
        }

    @staticmethod
    def heading_3(text: str, color: str = "default") -> dict:
        return {
            "object": "block", "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": text}}],
                "color": color,
            },
        }

    @staticmethod
    def paragraph(text: str, color: str = "default", bold: bool = False) -> dict:
        return {
            "object": "block", "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": text}, "annotations": {"bold": bold}}],
                "color": color,
            },
        }

    @staticmethod
    def callout(text: str, emoji: str = "💡", color: str = "default") -> dict:
        return {
            "object": "block", "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": text}}],
                "icon": {"type": "emoji", "emoji": emoji},
                "color": color,
            },
        }

    @staticmethod
    def toggle(text: str, children: list[dict] = None) -> dict:
        block = {
            "object": "block", "type": "toggle",
            "toggle": {
                "rich_text": [{"type": "text", "text": {"content": text}}],
            },
        }
        if children:
            block["toggle"]["children"] = children
        return block

    @staticmethod
    def divider() -> dict:
        return {"object": "block", "type": "divider", "divider": {}}

    @staticmethod
    def quote(text: str, color: str = "default") -> dict:
        return {
            "object": "block", "type": "quote",
            "quote": {
                "rich_text": [{"type": "text", "text": {"content": text}}],
                "color": color,
            },
        }

    @staticmethod
    def bulleted_list(text: str) -> dict:
        return {
            "object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": text}}],
            },
        }

    @staticmethod
    def numbered_list(text: str) -> dict:
        return {
            "object": "block", "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": text}}],
            },
        }

    @staticmethod
    def embed(url: str) -> dict:
        return {"object": "block", "type": "embed", "embed": {"url": url}}

    @staticmethod
    def audio_block(url: str) -> dict:
        return {
            "object": "block", "type": "audio",
            "audio": {"type": "external", "external": {"url": url}},
        }

    @staticmethod
    def image_block(url: str, caption: str = "") -> dict:
        block = {
            "object": "block", "type": "image",
            "image": {"type": "external", "external": {"url": url}},
        }
        if caption:
            block["image"]["caption"] = [{"type": "text", "text": {"content": caption}}]
        return block
