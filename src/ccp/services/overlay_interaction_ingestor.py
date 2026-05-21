from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
from src.ccp.models.overlay_capture_models import CompositeCaptureMetadata, OverlayInteractionEvent


class OverlayInteractionIngestor:
    """DEP-OVR-008: Backend service receiving interaction journal events.
    Persists events to overlay_interaction_events table.
    Logs capture lifecycle receipts through receipt_chain."""

    def __init__(self, supabase_client: Any = None, receipt_chain: Any = None) -> None:
        self._supabase = supabase_client
        self._receipt_chain = receipt_chain

    async def ingest_events(self, *, session_id: str, events: list[dict]) -> int:
        """Ingest a batch of overlay interaction events. Returns count persisted."""
        persisted = 0
        for raw_event in events:
            try:
                event = OverlayInteractionEvent(**raw_event)
                if self._supabase is not None:
                    self._supabase.table("overlay_interaction_events").insert({
                        "id": str(uuid4()),
                        "session_id": event.session_id,
                        "event_type": event.event_type,
                        "timestamp_ms": event.timestamp_ms,
                        "round_index": event.round_index,
                        "from_state": event.from_state,
                        "to_state": event.to_state,
                        "overlay_elements": event.overlay_elements,
                        "capture_state": event.capture_state,
                        "created_at": datetime.now(timezone.utc).isoformat(),
                    }).execute()
                persisted += 1
            except Exception:
                continue

        if self._receipt_chain is not None:
            self._receipt_chain.log(action="journal-persisted", metadata={
                "session_id": session_id,
                "events_received": len(events),
                "events_persisted": persisted,
            })

        return persisted

    async def ingest_capture_metadata(self, *, metadata: dict) -> str:
        """Persist composite capture metadata. Returns capture record ID."""
        capture = CompositeCaptureMetadata(**metadata)
        record_id = str(uuid4())

        if self._supabase is not None:
            self._supabase.table("overlay_capture_metadata").insert({
                "id": record_id,
                "session_id": capture.session_id,
                "coach_id": capture.coach_id,
                "width": capture.resolution.width,
                "height": capture.resolution.height,
                "frame_rate": capture.resolution.frame_rate,
                "media_format": capture.resolution.media_format.value,
                "device_tier": capture.resolution.device_tier,
                "resolution_downgraded": capture.resolution.resolution_downgraded,
                "capture_status": capture.capture_status.value,
                "started_at": capture.started_at.isoformat() if capture.started_at else None,
                "stopped_at": capture.stopped_at.isoformat() if capture.stopped_at else None,
                "duration_ms": capture.duration_ms,
                "blob_size_bytes": capture.blob_size_bytes,
                "upload_status": capture.upload_status,
                "interaction_event_count": capture.interaction_event_count,
                "audio_track_present": capture.audio_track_present,
                "video_track_present": capture.video_track_present,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }).execute()

        if self._receipt_chain is not None:
            self._receipt_chain.log(action="capture-stopped", metadata={
                "record_id": record_id,
                "session_id": capture.session_id,
                "capture_status": capture.capture_status.value,
                "duration_ms": capture.duration_ms,
            })

        return record_id
