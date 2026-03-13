"""
CCP Interactive Mode Webinar Session
Task 6.01 — Guided module-by-module webinar creation via Telegram.

Flow:
  1. Coach describes teaching intent for one module
  2. System generates the module using Intelligence Library
  3. Coach approves, redirects, or requests changes
  4. Move to next module
  5. Repeat until all modules are complete
  6. Final compilation into Excalidraw

This is the "co-creation" mode vs YOLO's "generate it all" mode.
"""

import json
import os
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from src.ccp.agents.webinar_module_gen import WebinarModuleGenerator
from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.services.excalidraw_compiler import ExcalidrawCompiler


class SessionState(str, Enum):
    AWAITING_INTENT = "awaiting_intent"
    GENERATING = "generating"
    AWAITING_APPROVAL = "awaiting_approval"
    MODULE_APPROVED = "module_approved"
    COMPLETED = "completed"


class InteractiveSession(BaseModel):
    """Tracks the state of an interactive webinar session."""

    session_id: str
    coach_acronym: str
    webinar_title: str = ""
    current_module: int = 1
    total_modules: int = 0
    state: SessionState = SessionState.AWAITING_INTENT
    completed_modules: list[dict] = Field(default_factory=list)
    current_draft: Optional[dict] = None
    revision_count: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class V2WSInteractiveMode:
    """Guided module-by-module webinar creation via conversation."""

    MAX_REVISIONS = 5

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.module_gen = WebinarModuleGenerator(coach_acronym=self.coach_acronym)
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)
        self._sessions_dir = Path(
            f"coaches/{self.coach_acronym}/production/webinars/sessions"
        )
        self._sessions_dir.mkdir(parents=True, exist_ok=True)

    def start_session(self, webinar_title: str, total_modules: int = 6) -> InteractiveSession:
        """Start a new interactive webinar session.

        Args:
            webinar_title: Working title for the webinar
            total_modules: Expected number of modules (adjustable)

        Returns:
            New InteractiveSession
        """
        import hashlib
        session_id = hashlib.md5(
            f"{self.coach_acronym}:{webinar_title}:{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]

        session = InteractiveSession(
            session_id=session_id,
            coach_acronym=self.coach_acronym,
            webinar_title=webinar_title,
            total_modules=total_modules,
        )
        self._save_session(session)

        self.receipt_chain.log(
            agent_id="v2ws_interactive",
            action="start_session",
            output_summary=f"Session {session_id}: '{webinar_title}', {total_modules} modules",
            decision="started",
        )

        return session

    async def process_input(
        self, session_id: str, coach_input: str
    ) -> tuple[str, InteractiveSession]:
        """Process coach's input in the interactive session.

        Args:
            session_id: Active session ID
            coach_input: Coach's text input

        Returns:
            (response_text, updated_session)
        """
        session = self._load_session(session_id)
        if not session:
            return "Session not found. Start a new one with /webinar.", session

        if session.state == SessionState.COMPLETED:
            return "This webinar session is complete! Would you like to start a new one?", session

        if session.state == SessionState.AWAITING_INTENT:
            return await self._handle_intent(session, coach_input)

        if session.state == SessionState.AWAITING_APPROVAL:
            return await self._handle_approval(session, coach_input)

        return "I'm not sure where we are. Let me reset — what would you like Module {} to teach?".format(
            session.current_module
        ), session

    async def _handle_intent(
        self, session: InteractiveSession, intent: str
    ) -> tuple[str, InteractiveSession]:
        """Coach describes what a module should teach."""
        session.state = SessionState.GENERATING

        # Generate the module
        module = await self.module_gen.generate_module(
            module_number=session.current_module,
            module_title=f"Module {session.current_module}",
            teaching_point=intent,
            duration=12,
        )

        session.current_draft = {
            "module_number": session.current_module,
            "teaching_intent": intent,
            "generated": module,
        }
        session.state = SessionState.AWAITING_APPROVAL
        session.revision_count = 0
        self._save_session(session)

        # Format preview for the coach
        slides = module.get("slides", [])
        preview_lines = [
            f"📋 **Module {session.current_module} Draft** ({len(slides)} slides)\n"
        ]
        for s in slides[:4]:  # Show first 4 slides
            preview_lines.append(f"  **Slide {s.get('slide_number', '?')}:** {s.get('headline', '')}")
            preview_lines.append(f"  {s.get('body', '')[:100]}...\n")

        if len(slides) > 4:
            preview_lines.append(f"  ... and {len(slides) - 4} more slides\n")

        preview_lines.append(f"🎯 Key takeaway: {module.get('key_takeaway', '')}")
        preview_lines.append(f"\n*Reply: ✅ approve | 🔄 redirect (say what to change) | ❌ redo*")

        return "\n".join(preview_lines), session

    async def _handle_approval(
        self, session: InteractiveSession, response: str
    ) -> tuple[str, InteractiveSession]:
        """Coach approves, redirects, or re-does the module."""
        response_lower = response.lower().strip()

        # Approve
        if any(w in response_lower for w in ["approve", "yes", "ok", "good", "✅", "👍", "perfect", "love it"]):
            session.completed_modules.append(session.current_draft)
            session.current_module += 1
            session.current_draft = None

            if session.current_module > session.total_modules:
                session.state = SessionState.COMPLETED
                self._save_session(session)
                # Compile
                compiled_path = await self._compile_session(session)
                return (
                    f"🎉 **Webinar complete!** {len(session.completed_modules)} modules generated.\n"
                    f"Excalidraw file: `{compiled_path}`\n"
                    f"You can now open it in Excalidraw for visual editing."
                ), session

            session.state = SessionState.AWAITING_INTENT
            self._save_session(session)
            return (
                f"✅ Module {session.current_module - 1} approved!\n\n"
                f"📝 **Module {session.current_module}/{session.total_modules}**\n"
                f"What should this module teach?"
            ), session

        # Redo
        if any(w in response_lower for w in ["redo", "❌", "no", "start over", "scrap"]):
            session.state = SessionState.AWAITING_INTENT
            session.current_draft = None
            session.revision_count = 0
            self._save_session(session)
            return (
                f"🔄 Scrapped. What should Module {session.current_module} teach instead?"
            ), session

        # Redirect (treat as revision)
        if session.revision_count >= self.MAX_REVISIONS:
            session.state = SessionState.AWAITING_INTENT
            session.current_draft = None
            self._save_session(session)
            return (
                f"We've hit {self.MAX_REVISIONS} revisions. Let's try a fresh approach.\n"
                f"What should Module {session.current_module} teach?"
            ), session

        session.revision_count += 1
        # Re-generate with the redirect instruction
        original_intent = session.current_draft.get("teaching_intent", "") if session.current_draft else ""
        revised_intent = f"{original_intent}\n\nREVISION REQUEST: {response}"

        session.state = SessionState.AWAITING_INTENT
        self._save_session(session)
        return await self._handle_intent(session, revised_intent)

    async def _compile_session(self, session: InteractiveSession) -> str:
        """Compile all completed modules into a webinar JSON + Excalidraw."""
        from src.ccp.core.asset_id import AssetIDGenerator, AssetType
        asset_gen = AssetIDGenerator(coach_acronym=self.coach_acronym)
        asset_id = asset_gen.generate(AssetType.WEBINAR)

        webinar = {
            "asset_id": asset_id,
            "coach_acronym": self.coach_acronym,
            "title": session.webinar_title,
            "modules": [
                {
                    "module_number": m["module_number"],
                    "title": f"Module {m['module_number']}",
                    "hook": "",
                    "teaching_point": m.get("teaching_intent", ""),
                    "slides": m.get("generated", {}).get("slides", []),
                    "duration_minutes": 12,
                }
                for m in session.completed_modules
            ],
            "total_duration_minutes": len(session.completed_modules) * 12,
        }

        output_dir = Path(f"coaches/{self.coach_acronym}/production/webinars")
        output_dir.mkdir(parents=True, exist_ok=True)
        webinar_path = output_dir / f"{asset_id}.json"
        webinar_path.write_text(json.dumps(webinar, indent=2), encoding="utf-8")

        # Compile to Excalidraw
        compiler = ExcalidrawCompiler(coach_acronym=self.coach_acronym)
        excalidraw_path = compiler.compile(str(webinar_path))

        return excalidraw_path

    def _save_session(self, session: InteractiveSession) -> None:
        path = self._sessions_dir / f"{session.session_id}.json"
        path.write_text(session.model_dump_json(indent=2), encoding="utf-8")

    def _load_session(self, session_id: str) -> Optional[InteractiveSession]:
        path = self._sessions_dir / f"{session_id}.json"
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            return InteractiveSession.model_validate(data)
        return None
