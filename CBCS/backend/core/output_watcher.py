"""
Output File Watcher — Story 20.4
==================================
Monitors coach project directories for new files created by
CLI sessions (CMF/CCF pipelines) and delivers notifications
when key artifacts appear.

Architecture:
    scheduler.start() → output_watcher.start_watching()
                       ↓
    watchdog Observer per coach project_root
                       ↓
    File events → filter → match known patterns → Telegram notification

Key Files Watched:
    strategy_brief.json       → Story Diagnosis complete
    Quote_Manifest.md         → Arc Hunting complete
    Quote_Manifest_Enriched.md → Analysis complete
    premise_analysis.json     → Composition complete
    DIAGNOSIS_REPORT.md       → Diagnosis report ready
    COMPOSITION_LOG.md        → Composition log ready
    suno_prompt.txt           → Sonic Scribe output ready
    STORYBOARD_PRIMAL.md      → Storyboard ready
    PROMPTS_FINAL.md          → Visual prompts ready
    dynamic_content_themes.json → CCF weekly themes ready
"""

import asyncio
import logging
import os
from pathlib import Path
from typing import Dict, Optional, Set
from datetime import datetime, timedelta

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileModifiedEvent

from backend.core.telegram import send_telegram_message

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Artifact Patterns → Notification Messages
# ──────────────────────────────────────────────

ARTIFACT_NOTIFICATIONS = {
    "strategy_brief.json": {
        "emoji": "🩺",
        "title": "Story Diagnosis Complete",
        "detail": "Arc type and frame statement have been determined.",
    },
    "DIAGNOSIS_REPORT.md": {
        "emoji": "📋",
        "title": "Diagnosis Report Ready",
        "detail": "Full diagnostic report with content scan and arc detection.",
    },
    "Quote_Manifest.md": {
        "emoji": "🔎",
        "title": "Arc Hunting Complete",
        "detail": "Raw quotes have been extracted from the transcript.",
    },
    "Quote_Manifest_Enriched.md": {
        "emoji": "📊",
        "title": "Quote Analysis Complete",
        "detail": "6-layer intelligence enrichment applied to all quotes.",
    },
    "premise_analysis.json": {
        "emoji": "✍️",
        "title": "Composition Complete",
        "detail": "Final script structure assembled and ready for review.",
    },
    "COMPOSITION_LOG.md": {
        "emoji": "📝",
        "title": "Composition Log Ready",
        "detail": "Detailed log of composition decisions and quality metrics.",
    },
    "suno_prompt.txt": {
        "emoji": "🎵",
        "title": "Sonic Scribe Output Ready",
        "detail": "Music prompt with T-Code/V-Code embedded lyrics generated.",
    },
    "STORYBOARD_PRIMAL.md": {
        "emoji": "🎬",
        "title": "Storyboard Ready",
        "detail": "Scene-level visual architecture complete.",
    },
    "PROMPTS_FINAL.md": {
        "emoji": "🎨",
        "title": "Visual Prompts Ready",
        "detail": "Final T2I and I2V prompts generated for all scenes.",
    },
    "dynamic_content_themes.json": {
        "emoji": "📰",
        "title": "Weekly Themes Ready",
        "detail": "Fresh content themes from CCF weekly research pipeline.",
    },
}

# Debounce: ignore modifications within this window after creation
DEBOUNCE_SECONDS = 5


# ──────────────────────────────────────────────
# File Event Handler
# ──────────────────────────────────────────────

class ArtifactEventHandler(FileSystemEventHandler):
    """
    Handles file creation/modification events in a coach's project directory.

    Filters events to only react to known artifact patterns and
    dispatches Telegram notifications asynchronously.
    """

    def __init__(self, coach_id: str, chat_id: int, loop: asyncio.AbstractEventLoop):
        super().__init__()
        self.coach_id = coach_id
        self.chat_id = chat_id
        self.loop = loop
        self._recent_events: Dict[str, datetime] = {}  # path → last notified time

    def on_created(self, event):
        if event.is_directory:
            return
        self._handle_file_event(event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        self._handle_file_event(event.src_path)

    def _handle_file_event(self, file_path: str):
        """Check if the file matches a known artifact pattern and notify."""
        filename = os.path.basename(file_path)

        # Check suffix matches (files often have project ID prefix)
        notification = None
        for pattern, notif in ARTIFACT_NOTIFICATIONS.items():
            if filename.endswith(pattern):
                notification = notif
                break

        if not notification:
            return

        # Debounce: skip if we notified about this file recently
        now = datetime.now()
        last_notified = self._recent_events.get(file_path)
        if last_notified and (now - last_notified) < timedelta(seconds=DEBOUNCE_SECONDS):
            return

        self._recent_events[file_path] = now

        # Dispatch notification asynchronously
        message = (
            f"{notification['emoji']} *{notification['title']}*\n\n"
            f"{notification['detail']}\n\n"
            f"📁 `{filename}`"
        )

        asyncio.run_coroutine_threadsafe(
            send_telegram_message(self.chat_id, message),
            self.loop,
        )

        logger.info(
            f"[OutputWatcher] Notified coach {self.coach_id[:8]} about: {filename}"
        )


# ──────────────────────────────────────────────
# Output Watcher Manager
# ──────────────────────────────────────────────

class OutputWatcher:
    """
    Manages watchdog Observers for coach project directories.

    Lifecycle:
        start_watching(coach_id, chat_id, project_root) → creates observer
        stop_watching(coach_id) → removes observer
        stop_all() → shutdown all observers
    """

    def __init__(self):
        self._observers: Dict[str, Observer] = {}  # coach_id → Observer
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    def start_watching(self, coach_id: str, chat_id: int, project_root: str):
        """Start watching a coach's project directory for artifact outputs."""
        if coach_id in self._observers:
            logger.debug(f"[OutputWatcher] Already watching for coach {coach_id[:8]}")
            return

        project_path = Path(project_root)
        if not project_path.exists():
            logger.warning(
                f"[OutputWatcher] Project path does not exist: {project_root} "
                f"(coach {coach_id[:8]})"
            )
            return

        # Get the event loop (must be called from async context)
        if self._loop is None:
            try:
                self._loop = asyncio.get_running_loop()
            except RuntimeError:
                self._loop = asyncio.get_event_loop()

        handler = ArtifactEventHandler(
            coach_id=coach_id,
            chat_id=chat_id,
            loop=self._loop,
        )

        observer = Observer()
        observer.schedule(handler, str(project_path), recursive=True)
        observer.daemon = True
        observer.start()

        self._observers[coach_id] = observer
        logger.info(
            f"[OutputWatcher] Started watching: {project_root} "
            f"(coach {coach_id[:8]})"
        )

    def stop_watching(self, coach_id: str):
        """Stop watching a specific coach's project directory."""
        observer = self._observers.pop(coach_id, None)
        if observer:
            observer.stop()
            observer.join(timeout=5)
            logger.info(f"[OutputWatcher] Stopped watching for coach {coach_id[:8]}")

    def stop_all(self):
        """Stop all observers. Called on app shutdown."""
        for coach_id in list(self._observers.keys()):
            self.stop_watching(coach_id)
        logger.info("[OutputWatcher] All watchers stopped")

    @property
    def active_count(self) -> int:
        """Number of active watchers."""
        return len(self._observers)

    def get_status(self) -> Dict[str, bool]:
        """Return status of all watchers."""
        return {
            coach_id: observer.is_alive()
            for coach_id, observer in self._observers.items()
        }


# ──────────────────────────────────────────────
# Global Instance
# ──────────────────────────────────────────────

output_watcher = OutputWatcher()
