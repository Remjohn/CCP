from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from src.ccp.models.affine_broadcast_models import (
    BroadcastLaunchRequest,
    BroadcastLaunchResult,
    BroadcastQueueItem,
    BroadcastSessionStatus,
    ClientCardProjection,
    ConvictionScoreBreakdown,
    DashboardSummary,
    DiagnosticExcerpt,
    DiagnosticExcerptSource,
    EvidencePointer,
    InterceptGateStatus,
    InterceptSessionRecord,
    InterceptStartRequest,
    ProgressArcSnapshot,
    RedFlagFeedEntry,
    RedFlagSeverity,
    ReviewAcknowledgementRecord,
    ReviewAcknowledgementRequest,
)


# ════════════════════════════════════════════════════════════════════════
# CrossSystemProgressAdapter — Task 4
# Normalizes SundayBotMeetingPayload, AFFiNE telemetry, and client
# workspace linkage into one per-client summary.
# ════════════════════════════════════════════════════════════════════════

class CrossSystemProgressAdapter:
    def __init__(self, cross_system_service: Any = None, affine_client_workspace: Any = None) -> None:
        self._cross_system = cross_system_service
        self._client_workspace = affine_client_workspace

    def build_snapshot(self, *, client_id: str, coach_id: str) -> dict:
        snapshot = {
            "client_id": client_id,
            "coach_id": coach_id,
            "completion_percent": 0.0,
            "streak_days": 0,
            "mood_indicator": "neutral",
            "current_program_step": "onboarding",
            "next_required_action": "Complete next session",
            "composite_score": 50.0,
            "workspace_url": "",
            "intelligence_available": False,
        }

        if self._cross_system is not None:
            try:
                meeting = self._cross_system.run_sunday_bot_meeting(client_data=[{"client_id": client_id}])
                if meeting and hasattr(meeting, "metrics"):
                    metrics = meeting.metrics
                    if hasattr(metrics, "completion_rate"):
                        snapshot["completion_percent"] = float(metrics.completion_rate) * 100
                    if hasattr(metrics, "streak_days"):
                        snapshot["streak_days"] = int(metrics.streak_days)
                    if hasattr(metrics, "composite_score"):
                        snapshot["composite_score"] = float(metrics.composite_score)
                    snapshot["intelligence_available"] = True
                if meeting and hasattr(meeting, "synthesis") and meeting.synthesis:
                    if hasattr(meeting.synthesis, "mood_label"):
                        snapshot["mood_indicator"] = meeting.synthesis.mood_label
            except Exception:
                pass

        if self._client_workspace is not None:
            try:
                result = self._client_workspace.get_workspace_url(client_id=client_id, coach_id=coach_id)
                if result:
                    snapshot["workspace_url"] = str(result)
            except Exception:
                pass

        return snapshot


# ════════════════════════════════════════════════════════════════════════
# ClientCardProjectionService — Task 5
# Visual completion arc, streak flame, conviction score, mood, CTA state.
# ════════════════════════════════════════════════════════════════════════

class ClientCardProjectionService:
    def __init__(self, progress_adapter: CrossSystemProgressAdapter, supabase_client: Any = None) -> None:
        self._adapter = progress_adapter
        self._supabase = supabase_client

    def build_card(self, *, client_id: str, coach_id: str, display_name: str = "Client") -> ClientCardProjection:
        snapshot = self._adapter.build_snapshot(client_id=client_id, coach_id=coach_id)

        progress_arc = ProgressArcSnapshot(
            completion_percent=snapshot["completion_percent"],
            current_program_step=snapshot["current_program_step"],
            streak_days=snapshot["streak_days"],
            mood_indicator=snapshot["mood_indicator"],
            next_required_action=snapshot["next_required_action"],
        )

        conviction = ConvictionScoreBreakdown(composite_score=snapshot["composite_score"])
        workspace_url = snapshot["workspace_url"] or f"https://affine.coach/{coach_id}/{client_id}"

        cta = snapshot["next_required_action"]
        if snapshot["completion_percent"] >= 100.0:
            cta = "Review completed program"
        elif snapshot["streak_days"] == 0:
            cta = "Re-engage client"

        projection = ClientCardProjection(
            projection_id=f"PROJ-{uuid4().hex[:8].upper()}",
            coach_id=coach_id,
            client_id=client_id,
            client_display_name=display_name,
            client_workspace_url=workspace_url,
            progress_arc=progress_arc,
            conviction=conviction,
            red_flags=[],
            primary_cta=cta,
            updated_at=datetime.now(timezone.utc),
        )

        if self._supabase is not None:
            try:
                self._supabase.table("affine_client_card_projections").upsert({
                    "projection_id": projection.projection_id,
                    "coach_id": coach_id,
                    "client_id": client_id,
                    "workspace_id": f"ws-{coach_id}",
                    "projection_json": projection.model_dump(mode="json"),
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }, on_conflict="coach_id,client_id").execute()
            except Exception:
                pass

        return projection


# ════════════════════════════════════════════════════════════════════════
# DiagnosticExcerptEvidenceResolver — Task 6
# Resolves transcript snippets, pause summaries, and section entry
# references from session evidence.
# ════════════════════════════════════════════════════════════════════════

class DiagnosticExcerptEvidenceResolver:
    def __init__(self, supabase_client: Any = None) -> None:
        self._supabase = supabase_client

    def resolve(self, *, session_id: str, asset_id: str, workspace_entry_id: str, transcript_snippet: str | None = None, pause_summary: str | None = None) -> DiagnosticExcerpt | None:
        if not transcript_snippet and not pause_summary:
            return None

        source_type = DiagnosticExcerptSource.transcript_snippet
        display_text = transcript_snippet or ""
        rationale = "Flagged from transcript analysis"

        if pause_summary and not transcript_snippet:
            source_type = DiagnosticExcerptSource.pause_pattern
            display_text = pause_summary
            rationale = "Flagged from pause pattern detection"
        elif pause_summary and transcript_snippet:
            display_text = f"{transcript_snippet} [Pause: {pause_summary}]"
            rationale = "Flagged from combined transcript and pause analysis"

        if len(display_text) < 8:
            return None

        excerpt_hash = hashlib.sha256(display_text.encode("utf-8")).hexdigest()

        return DiagnosticExcerpt(
            excerpt_id=f"EXC-{uuid4().hex[:8].upper()}",
            source_type=source_type,
            display_excerpt=display_text[:500],
            rationale=rationale[:300],
            excerpt_hash=excerpt_hash,
            evidence_pointer=EvidencePointer(
                session_id=session_id,
                asset_id=asset_id,
                workspace_section="client_intelligence_hub",
                workspace_entry_id=workspace_entry_id,
            ),
            flagged_at=datetime.now(timezone.utc),
            confidence_label="evidence-backed",
        )


# ════════════════════════════════════════════════════════════════════════
# RedFlagExcerptAssembler — Task 7
# Ranks and shapes actionable flag entries with excerpt hashes.
# Suppresses numeric-only flags (AC2).
# ════════════════════════════════════════════════════════════════════════

class RedFlagExcerptAssembler:
    def __init__(self, excerpt_resolver: DiagnosticExcerptEvidenceResolver, supabase_client: Any = None, receipt_chain: Any = None) -> None:
        self._resolver = excerpt_resolver
        self._supabase = supabase_client
        self._receipt_chain = receipt_chain

    def assemble(self, *, coach_id: str, client_id: str, signals: list[dict]) -> list[RedFlagFeedEntry]:
        entries: list[RedFlagFeedEntry] = []

        for signal in signals:
            transcript_snippet = signal.get("transcript_snippet")
            pause_summary = signal.get("pause_summary")

            excerpt = self._resolver.resolve(
                session_id=signal.get("session_id", ""),
                asset_id=signal.get("asset_id", ""),
                workspace_entry_id=signal.get("workspace_entry_id", ""),
                transcript_snippet=transcript_snippet,
                pause_summary=pause_summary,
            )

            if excerpt is None:
                # Suppress numeric-only flag — no qualitative evidence
                if self._receipt_chain is not None:
                    self._receipt_chain.log(action="flag-suppressed-no-qualitative-evidence", metadata={
                        "coach_id": coach_id, "client_id": client_id,
                        "signal": signal.get("flag_title", "unknown"),
                    })
                continue

            severity_str = signal.get("severity", "medium")
            try:
                severity = RedFlagSeverity(severity_str)
            except ValueError:
                severity = RedFlagSeverity.medium

            flag_id = signal.get("flag_id", f"FLAG-{uuid4().hex[:8].upper()}")
            entry = RedFlagFeedEntry(
                flag_id=flag_id,
                coach_id=coach_id,
                client_id=client_id,
                severity=severity,
                flag_title=signal.get("flag_title", "Attention needed")[:120],
                flag_summary=signal.get("flag_summary", "Review required for this client event")[:240],
                excerpt=excerpt,
                gate_status=InterceptGateStatus.locked,
                created_at=datetime.now(timezone.utc),
            )
            entries.append(entry)

            if self._supabase is not None:
                try:
                    self._supabase.table("affine_red_flag_evidence").insert({
                        "flag_id": flag_id,
                        "coach_id": coach_id,
                        "client_id": client_id,
                        "severity": severity.value,
                        "excerpt_hash": excerpt.excerpt_hash,
                        "excerpt_text": excerpt.display_excerpt,
                        "source_type": excerpt.source_type.value,
                        "session_id": excerpt.evidence_pointer.session_id,
                        "asset_id": excerpt.evidence_pointer.asset_id,
                        "workspace_entry_id": excerpt.evidence_pointer.workspace_entry_id,
                        "created_at": datetime.now(timezone.utc).isoformat(),
                    }).execute()
                except Exception:
                    pass

        # Sort by severity
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        entries.sort(key=lambda e: severity_order.get(e.severity.value, 99))

        return entries


# ════════════════════════════════════════════════════════════════════════
# InterceptReviewGateService — Task 8
# Phase4-M01 enforcement: persist exact ack phrase, compute gate state.
# ════════════════════════════════════════════════════════════════════════

class InterceptReviewGateService:
    def __init__(self, supabase_client: Any = None, receipt_chain: Any = None) -> None:
        self._supabase = supabase_client
        self._receipt_chain = receipt_chain

    def acknowledge_review(self, *, flag_id: str, request: ReviewAcknowledgementRequest, current_excerpt_hash: str) -> ReviewAcknowledgementRecord | None:
        """Persist review ack. Returns None if excerpt_hash does not match current."""
        if request.excerpt_hash != current_excerpt_hash:
            return None

        ack_id = f"ACK-{uuid4().hex[:8].upper()}"
        now = datetime.now(timezone.utc)

        record = ReviewAcknowledgementRecord(
            acknowledgement_id=ack_id,
            flag_id=flag_id,
            coach_id=request.coach_id,
            client_id=request.client_id,
            excerpt_hash=request.excerpt_hash,
            acknowledged_at=now,
            gate_status_after_ack=InterceptGateStatus.ready,
        )

        if self._supabase is not None:
            try:
                self._supabase.table("affine_intercept_review_acks").upsert({
                    "acknowledgement_id": ack_id,
                    "flag_id": flag_id,
                    "coach_id": request.coach_id,
                    "client_id": request.client_id,
                    "excerpt_hash": request.excerpt_hash,
                    "ack_phrase": request.acknowledgement_phrase,
                    "acknowledged_at": now.isoformat(),
                }, on_conflict="flag_id,coach_id,excerpt_hash").execute()
            except Exception:
                return None

        if self._receipt_chain is not None:
            self._receipt_chain.log(action="excerpt-review-acknowledged", metadata={
                "flag_id": flag_id, "coach_id": request.coach_id,
                "excerpt_hash": request.excerpt_hash,
            })

        return record

    def check_gate_status(self, *, flag_id: str, coach_id: str, current_excerpt_hash: str) -> InterceptGateStatus:
        """Check if a valid acknowledgement exists for the current excerpt hash."""
        if self._supabase is not None:
            try:
                result = self._supabase.table("affine_intercept_review_acks").select("*").eq("flag_id", flag_id).eq("coach_id", coach_id).eq("excerpt_hash", current_excerpt_hash).execute()
                if result and hasattr(result, "data") and result.data:
                    return InterceptGateStatus.ready
            except Exception:
                pass
        return InterceptGateStatus.locked


# ════════════════════════════════════════════════════════════════════════
# OperatorInterceptSessionService — Task 9
# Creates intercept sessions only after valid acknowledgement (M-01).
# ════════════════════════════════════════════════════════════════════════

class OperatorInterceptSessionService:
    def __init__(self, gate_service: InterceptReviewGateService, supabase_client: Any = None, receipt_chain: Any = None) -> None:
        self._gate = gate_service
        self._supabase = supabase_client
        self._receipt_chain = receipt_chain

    def start_intercept(self, *, request: InterceptStartRequest, current_excerpt_hash: str) -> InterceptSessionRecord | None:
        """Returns None with 409 reason if gate is still locked."""
        gate_status = self._gate.check_gate_status(
            flag_id=request.flag_id,
            coach_id=request.coach_id,
            current_excerpt_hash=current_excerpt_hash,
        )

        if gate_status != InterceptGateStatus.ready:
            if self._receipt_chain is not None:
                self._receipt_chain.log(action="intercept-blocked-no-review", metadata={
                    "flag_id": request.flag_id, "coach_id": request.coach_id,
                    "gate_status": gate_status.value,
                })
            return None

        intercept_id = f"INT-{uuid4().hex[:8].upper()}"
        now = datetime.now(timezone.utc)

        record = InterceptSessionRecord(
            intercept_id=intercept_id,
            coach_id=request.coach_id,
            client_id=request.client_id,
            flag_id=request.flag_id,
            gate_status=InterceptGateStatus.recording,
            excerpt_hash=current_excerpt_hash,
            started_at=now,
            workspace_id=request.workspace_id,
        )

        if self._supabase is not None:
            try:
                self._supabase.table("affine_intercept_sessions").insert({
                    "intercept_id": intercept_id,
                    "flag_id": request.flag_id,
                    "coach_id": request.coach_id,
                    "client_id": request.client_id,
                    "workspace_id": request.workspace_id,
                    "recorder_session_id": "",
                    "gate_status": InterceptGateStatus.recording.value,
                    "started_at": now.isoformat(),
                }).execute()
            except Exception:
                pass

        if self._receipt_chain is not None:
            self._receipt_chain.log(action="intercept-session-started", metadata={
                "intercept_id": intercept_id, "flag_id": request.flag_id,
                "coach_id": request.coach_id,
            })

        return record


# ════════════════════════════════════════════════════════════════════════
# StudioBlockLaunchBridge — Task 10
# Routes AFFiNE broadcast actions into existing Studio Block service.
# ════════════════════════════════════════════════════════════════════════

class StudioBlockLaunchBridge:
    def __init__(self, studio_block_service: Any = None, receipt_chain: Any = None) -> None:
        self._studio = studio_block_service
        self._receipt_chain = receipt_chain

    def launch(self, *, request: BroadcastLaunchRequest) -> BroadcastLaunchResult:
        broadcast_id = f"BRD-{uuid4().hex[:8].upper()}"
        studio_session_id = ""
        status = BroadcastSessionStatus.queued

        if self._studio is not None:
            try:
                result = self._studio.create_session(
                    coach_id=request.coach_id,
                    program_id=request.program_id,
                    title=request.title,
                )
                if result and hasattr(result, "session_id"):
                    studio_session_id = result.session_id
                    status = BroadcastSessionStatus.ready
            except Exception:
                status = BroadcastSessionStatus.failed

        receipt_id = f"RCP-{uuid4().hex[:6].upper()}"
        if self._receipt_chain is not None:
            self._receipt_chain.log(action="broadcast-launched", metadata={
                "broadcast_session_id": broadcast_id,
                "studio_session_id": studio_session_id,
                "coach_id": request.coach_id,
                "status": status.value,
            })

        return BroadcastLaunchResult(
            broadcast_session_id=broadcast_id,
            studio_session_id=studio_session_id or "pending",
            status=status,
            launch_receipt_id=receipt_id,
        )


# ════════════════════════════════════════════════════════════════════════
# BroadcastQueueProjector — Task 11
# Lean active/pending program control list for AFFiNE command center.
# ════════════════════════════════════════════════════════════════════════

class BroadcastQueueProjector:
    def __init__(self, supabase_client: Any = None) -> None:
        self._supabase = supabase_client

    def get_queue(self, *, coach_id: str) -> list[BroadcastQueueItem]:
        if self._supabase is not None:
            try:
                result = self._supabase.table("affine_broadcast_queue").select("*").eq("coach_id", coach_id).in_("status", ["draft", "queued", "ready", "live"]).order("created_at", desc=True).execute()
                if result and hasattr(result, "data") and result.data:
                    items = []
                    for row in result.data:
                        items.append(BroadcastQueueItem(
                            broadcast_session_id=row["broadcast_session_id"],
                            coach_id=row["coach_id"],
                            program_id=row["program_id"],
                            title=row.get("title", "Untitled"),
                            status=BroadcastSessionStatus(row["status"]),
                            planned_start_at=row.get("planned_start_at"),
                            studio_session_id=row.get("studio_session_id", ""),
                            audience_surface=row.get("audience_surface", "telegram"),
                        ))
                    return items
            except Exception:
                pass
        return []


# ════════════════════════════════════════════════════════════════════════
# AFFiNEStudioOrchestrationService — Task 12
# Single orchestration facade consumed by API routes.
# ════════════════════════════════════════════════════════════════════════

class AFFiNEStudioOrchestrationService:
    def __init__(self, card_service: ClientCardProjectionService, flag_assembler: RedFlagExcerptAssembler, gate_service: InterceptReviewGateService, intercept_service: OperatorInterceptSessionService, broadcast_projector: BroadcastQueueProjector, launch_bridge: StudioBlockLaunchBridge, receipt_chain: Any = None) -> None:
        self._cards = card_service
        self._flags = flag_assembler
        self._gate = gate_service
        self._intercept = intercept_service
        self._broadcast = broadcast_projector
        self._launch = launch_bridge
        self._receipt_chain = receipt_chain

    def get_dashboard(self, *, coach_id: str, workspace_id: str, client_data: list[dict]) -> DashboardSummary:
        cards: list[ClientCardProjection] = []
        for client in client_data:
            client_id = client.get("client_id", "")
            display_name = client.get("display_name", "Client")
            signals = client.get("flag_signals", [])

            card = self._cards.build_card(client_id=client_id, coach_id=coach_id, display_name=display_name)
            flags = self._flags.assemble(coach_id=coach_id, client_id=client_id, signals=signals)
            card.red_flags = flags
            cards.append(card)

        broadcast_queue = self._broadcast.get_queue(coach_id=coach_id)

        if self._receipt_chain is not None:
            self._receipt_chain.log(action="dashboard-read", metadata={
                "coach_id": coach_id, "client_count": len(cards),
            })

        return DashboardSummary(
            coach_id=coach_id,
            workspace_id=workspace_id,
            generated_at=datetime.now(timezone.utc),
            client_cards=cards,
            broadcast_queue=broadcast_queue,
        )

    def review_flag(self, *, flag_id: str, request: ReviewAcknowledgementRequest, current_excerpt_hash: str) -> ReviewAcknowledgementRecord | None:
        return self._gate.acknowledge_review(
            flag_id=flag_id, request=request,
            current_excerpt_hash=current_excerpt_hash,
        )

    def start_intercept(self, *, request: InterceptStartRequest, current_excerpt_hash: str) -> InterceptSessionRecord | None:
        return self._intercept.start_intercept(
            request=request, current_excerpt_hash=current_excerpt_hash,
        )

    def launch_broadcast(self, *, request: BroadcastLaunchRequest) -> BroadcastLaunchResult:
        return self._launch.launch(request=request)
