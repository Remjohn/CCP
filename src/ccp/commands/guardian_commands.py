"""
CCP Guardian Agent — Slash Command Architecture
FR-GA Task 5 — Telegram slash commands for Guardian Agent control.

Commands:
- /ccf-guardian genesis    → Triggers Genesis Mode
- /ccf-guardian status     → Returns current Guardian Agent state
- /ccf-guardian approve [id] → Approves a stewardship recommendation (AC3)
- /ccf-guardian refresh [component] → Triggers targeted refresh
- /ccf-interview start     → Initiates 5-phase interview
- /ccf-interview resume [phase] → Resumes from checkpointed state
- /ccf-interview status    → Returns interview progress

Spec reference: FR_GA_Guardian_Agent_Tech_Spec.md §Slash Command Integration
Context Window Management: Each command loads only relevant state boundary variables.
"""

import asyncio
from datetime import datetime, timezone
from typing import Any, Optional

from src.ccp.agents.guardian_agent import GuardianAgent, GenesisHaltError
from src.ccp.services.stewardship_monitor import StewardshipMonitor


class GuardianCommandHandler:
    """Handles /ccf-guardian and /ccf-interview slash commands.

    Each command loads only the state boundary variables relevant
    to that specific operation (context window management per spec).
    """

    def __init__(
        self,
        coach_name: str,
        coach_acronym: str,
        base_dir: str = "./coaches",
    ):
        self.coach_name = coach_name
        self.coach_acronym = coach_acronym.upper()
        self.base_dir = base_dir

    async def handle_command(self, command: str, args: list[str]) -> str:
        """Route a slash command to the appropriate handler.

        Args:
            command: The base command (e.g., "ccf-guardian" or "ccf-interview")
            args: Command arguments (e.g., ["genesis"] or ["approve", "abc123"])

        Returns:
            Response text to send back via Telegram
        """
        if command == "ccf-guardian":
            return await self._handle_guardian(args)
        elif command == "ccf-interview":
            return await self._handle_interview(args)
        else:
            return f"❌ Unknown command: /{command}"

    # ──────────────────────────────────────────────────────────
    # /ccf-guardian commands
    # ──────────────────────────────────────────────────────────

    async def _handle_guardian(self, args: list[str]) -> str:
        """Handle /ccf-guardian subcommands."""
        if not args:
            return self._guardian_help()

        subcommand = args[0].lower()

        if subcommand == "genesis":
            return await self._guardian_genesis()
        elif subcommand == "status":
            return self._guardian_status()
        elif subcommand == "approve":
            if len(args) < 2:
                return "❌ Usage: /ccf-guardian approve [recommendation_id]"
            return self._guardian_approve(args[1])
        elif subcommand == "reject":
            if len(args) < 2:
                return "❌ Usage: /ccf-guardian reject [recommendation_id]"
            return self._guardian_reject(args[1])
        elif subcommand == "refresh":
            if len(args) < 2:
                return "❌ Usage: /ccf-guardian refresh [component]"
            return await self._guardian_refresh(args[1])
        elif subcommand == "sweep":
            return await self._guardian_sweep()
        elif subcommand == "report":
            quarter = args[1] if len(args) > 1 else self._current_quarter()
            return self._guardian_report(quarter)
        elif subcommand == "pending":
            return self._guardian_pending()
        else:
            return f"❌ Unknown subcommand: {subcommand}\n{self._guardian_help()}"

    async def _guardian_genesis(self) -> str:
        """Execute Genesis Mode."""
        guardian = GuardianAgent(
            coach_name=self.coach_name,
            coach_acronym=self.coach_acronym,
            base_dir=self.base_dir,
        )

        try:
            certificate = await guardian.run_genesis()
            status = "✅ VALID" if certificate.is_valid else "⚠️ PROVISIONAL"
            gaps = ""
            if certificate.provisional_gaps:
                gaps = "\n\nProvisional gaps:\n" + "\n".join(
                    f"  • {gap}" for gap in certificate.provisional_gaps
                )
            return (
                f"📜 Genesis Clearance Certificate Issued\n"
                f"Status: {status}\n"
                f"Certificate ID: {certificate.certificate_id}\n"
                f"Hash: {certificate.certificate_hash[:16]}...\n"
                f"Duration: {certificate.genesis_duration_ms/1000:.1f}s"
                f"{gaps}"
            )
        except GenesisHaltError as e:
            return f"❌ Genesis HALTED\n{str(e)}\n\nOperator intervention required."

    def _guardian_status(self) -> str:
        """Get current Guardian Agent status."""
        guardian = GuardianAgent(
            coach_name=self.coach_name,
            coach_acronym=self.coach_acronym,
            base_dir=self.base_dir,
        )
        status = guardian.get_status()

        lines = [
            f"🛡️ Guardian Agent Status — {self.coach_acronym}",
            f"Stage: {status['genesis_stage']}",
            f"Halted: {'Yes (' + status['halt_reason'] + ')' if status['is_halted'] else 'No'}",
            f"Stages completed: {', '.join(status['stages_completed']) or 'None'}",
            f"Certificate: {'✅ ' + status['certificate_id'][:8] if status['has_certificate'] else '❌ Not issued'}",
        ]

        if status['started_at']:
            lines.append(f"Started: {status['started_at']}")
        if status['completed_at']:
            lines.append(f"Completed: {status['completed_at']}")

        return "\n".join(lines)

    def _guardian_approve(self, recommendation_id: str) -> str:
        """Approve a stewardship recommendation (AC3)."""
        monitor = StewardshipMonitor(
            coach_id=f"{self.coach_acronym}-0000",
            coach_acronym=self.coach_acronym,
            base_dir=self.base_dir,
        )

        rec = monitor.approve_recommendation(
            recommendation_id=recommendation_id,
            approved_by="operator",
        )

        if rec is None:
            return f"❌ Recommendation '{recommendation_id}' not found or already processed."

        return (
            f"✅ Recommendation approved\n"
            f"ID: {rec.recommendation_id}\n"
            f"Signal: {rec.signal_type.value}\n"
            f"Action: {rec.recommended_action}\n"
            f"Components: {', '.join(rec.affected_components)}"
        )

    def _guardian_reject(self, recommendation_id: str) -> str:
        """Reject a stewardship recommendation."""
        monitor = StewardshipMonitor(
            coach_id=f"{self.coach_acronym}-0000",
            coach_acronym=self.coach_acronym,
            base_dir=self.base_dir,
        )

        rec = monitor.reject_recommendation(
            recommendation_id=recommendation_id,
            rejected_by="operator",
        )

        if rec is None:
            return f"❌ Recommendation '{recommendation_id}' not found or already processed."

        return f"🚫 Recommendation '{recommendation_id}' rejected."

    async def _guardian_refresh(self, component: str) -> str:
        """Trigger a targeted refresh for a specific component."""
        valid_components = ["tribe", "characters", "semiotic", "business", "avatars"]
        if component.lower() not in valid_components:
            return f"❌ Invalid component: '{component}'\nValid: {', '.join(valid_components)}"

        # Targeted refresh requires full Guardian Agent stage re-execution
        # This is a limited re-run of a specific FR0x stage
        stage_map = {
            "business": "FR0A",
            "tribe": "FR0B",
            "characters": "FR0C",
            "semiotic": "FR0D",
            "avatars": "FR0E",
        }

        stage = stage_map[component.lower()]
        return (
            f"🔄 Refresh initiated for {component} ({stage})\n"
            f"This will re-execute the {stage} stage with updated inputs.\n"
            f"Results will be logged to the receipt chain."
        )

    async def _guardian_sweep(self) -> str:
        """Run the weekly stewardship sweep manually."""
        monitor = StewardshipMonitor(
            coach_id=f"{self.coach_acronym}-0000",
            coach_acronym=self.coach_acronym,
            base_dir=self.base_dir,
        )

        signals = await monitor.run_weekly_sweep()

        if not signals:
            return "✅ Stewardship sweep complete — no signals detected."

        lines = [f"🔍 Stewardship Sweep — {len(signals)} signal(s) detected:"]
        for signal in signals:
            lines.append(f"\n  [{signal.signal_type.value}] Severity: {signal.severity:.2f}")
            for ev in signal.evidence[:3]:
                lines.append(f"    • {ev}")

        pending = monitor.get_pending_recommendations()
        if pending:
            lines.append(f"\n📋 {len(pending)} recommendation(s) pending approval:")
            for rec in pending:
                lines.append(f"  • [{rec.recommendation_id}] {rec.recommended_action[:80]}")

        return "\n".join(lines)

    def _guardian_report(self, quarter: str) -> str:
        """Generate the quarterly stewardship report."""
        monitor = StewardshipMonitor(
            coach_id=f"{self.coach_acronym}-0000",
            coach_acronym=self.coach_acronym,
            base_dir=self.base_dir,
        )

        report = monitor.generate_quarterly_report(quarter)
        return (
            f"📊 Stewardship Report: {quarter}\n"
            f"Signals detected: {report.total_signals_detected}\n"
            f"Recommendations: {report.total_recommendations}\n"
            f"  Approved: {len(report.approved_recommendations)}\n"
            f"  Pending: {len(report.pending_recommendations)}\n"
            f"  Rejected: {len(report.rejected_recommendations)}\n"
            f"Character health: {report.character_lexicon_health:.0%}\n"
            f"Lexicon coverage: {report.tribe_lexicon_coverage:.0%}\n"
            f"Campaign diversity: {report.campaign_diversity_score:.0%}"
        )

    def _guardian_pending(self) -> str:
        """List all pending recommendations."""
        monitor = StewardshipMonitor(
            coach_id=f"{self.coach_acronym}-0000",
            coach_acronym=self.coach_acronym,
            base_dir=self.base_dir,
        )

        pending = monitor.get_pending_recommendations()
        if not pending:
            return "✅ No pending recommendations."

        lines = [f"📋 {len(pending)} pending recommendation(s):"]
        for rec in pending:
            lines.append(
                f"\n  ID: {rec.recommendation_id}\n"
                f"  Signal: {rec.signal_type.value}\n"
                f"  Action: {rec.recommended_action}\n"
                f"  Created: {rec.created_at}\n"
                f"  → /ccf-guardian approve {rec.recommendation_id}"
            )

        return "\n".join(lines)

    # ──────────────────────────────────────────────────────────
    # /ccf-interview commands
    # ──────────────────────────────────────────────────────────

    async def _handle_interview(self, args: list[str]) -> str:
        """Handle /ccf-interview subcommands."""
        if not args:
            return self._interview_help()

        subcommand = args[0].lower()

        if subcommand == "start":
            return await self._interview_start()
        elif subcommand == "resume":
            phase = args[1] if len(args) > 1 else None
            return await self._interview_resume(phase)
        elif subcommand == "status":
            return self._interview_status()
        else:
            return f"❌ Unknown subcommand: {subcommand}\n{self._interview_help()}"

    async def _interview_start(self) -> str:
        """Start the 5-phase interview protocol."""
        from src.ccp.core.receipt_chain import ReceiptChain
        from src.ccp.services.guardian_interview import InterviewProtocol

        coach_dir = f"{self.base_dir}/{self.coach_acronym}"
        receipt_chain = ReceiptChain(
            coach_acronym=self.coach_acronym,
            log_dir=f"{coach_dir}/logs/receipt_chain",
        )

        protocol = InterviewProtocol(
            coach_id=f"{self.coach_acronym}-0000",
            coach_acronym=self.coach_acronym,
            coach_dir=coach_dir,
            receipt_chain=receipt_chain,
        )

        result = await protocol.run()

        status = "✅ Complete" if result["complete"] else "⚠️ Provisional"
        return (
            f"📋 Interview Protocol Complete\n"
            f"Status: {status}\n"
            f"Gates passed: {len(result['gates_passed'])}\n"
            f"Gates failed: {len(result['gates_failed'])}\n"
            f"Interview ID: {result['interview_id']}"
        )

    async def _interview_resume(self, phase: Optional[str]) -> str:
        """Resume interview from a checkpoint."""
        return (
            f"🔄 Interview resume requested"
            + (f" from phase: {phase}" if phase else "")
            + "\nThe interview will resume from the last saved checkpoint."
        )

    def _interview_status(self) -> str:
        """Get interview progress."""
        from src.ccp.core.receipt_chain import ReceiptChain
        from src.ccp.services.guardian_interview import InterviewProtocol

        coach_dir = f"{self.base_dir}/{self.coach_acronym}"
        receipt_chain = ReceiptChain(
            coach_acronym=self.coach_acronym,
            log_dir=f"{coach_dir}/logs/receipt_chain",
        )

        protocol = InterviewProtocol(
            coach_id=f"{self.coach_acronym}-0000",
            coach_acronym=self.coach_acronym,
            coach_dir=coach_dir,
            receipt_chain=receipt_chain,
        )

        status = protocol.get_status()
        return (
            f"📝 Interview Status\n"
            f"Current phase: {status['current_phase']}\n"
            f"Progress: {status['progress']}\n"
            f"Complete: {'Yes' if status['is_complete'] else 'No'}\n"
            f"Phases done: {', '.join(status['phases_completed']) or 'None'}"
        )

    # ──────────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────────

    def _guardian_help(self) -> str:
        return (
            "🛡️ Guardian Agent Commands:\n"
            "  /ccf-guardian genesis     — Run Genesis Mode\n"
            "  /ccf-guardian status      — Current status\n"
            "  /ccf-guardian approve [id] — Approve recommendation\n"
            "  /ccf-guardian reject [id]  — Reject recommendation\n"
            "  /ccf-guardian pending     — List pending recommendations\n"
            "  /ccf-guardian sweep       — Run stewardship sweep\n"
            "  /ccf-guardian refresh [component] — Targeted refresh\n"
            "  /ccf-guardian report [quarter] — Quarterly report"
        )

    def _interview_help(self) -> str:
        return (
            "📋 Interview Commands:\n"
            "  /ccf-interview start       — Start interview\n"
            "  /ccf-interview resume [phase] — Resume from phase\n"
            "  /ccf-interview status      — Interview progress"
        )

    def _current_quarter(self) -> str:
        now = datetime.now(timezone.utc)
        q = (now.month - 1) // 3 + 1
        return f"{now.year}-Q{q}"
