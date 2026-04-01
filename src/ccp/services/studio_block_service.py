"""FR-CA11-16 — CCP Studio Block (Recording & Streaming).

Native AFFiNE BlockSuite plugin replacing OBS (ADR-07).
7 pipeline stages:
  Stage 1: Plugin Registration & UI Shell       → DEP-ENG-087
  Stage 2: Recording Engine (WebRTC + Canvas)    → DEP-ENG-088
  Stage 3: Teleprompter Component                → DEP-ENG-089
  Stage 4: Asset Panel                           → DEP-ENG-090
  Stage 5: S3 Upload & CMF Pipeline Trigger      → DEP-ENG-091, DEP-ENG-092
  Stage 6: Streaming Engine (ccp-stream-service)  → DEP-ENG-093

Agent: Diego (Studio Session Conductor)
Stress Test Mandates: Q34 (5s IndexedDB chunks), Q35 (AEC setup), Q38 (OffscreenCanvas arch)
"""
from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Optional, Protocol

from src.ccp.models.ca11_models import (
    CRASH_RECOVERY_MIN_SECONDS,
    CMF_TEMPLATE_MAP,
    DEFAULT_FRAMERATE,
    INDEXEDDB_CHUNK_INTERVAL_SECONDS,
    QUALITY_TIERS,
    S3_PERIODIC_SAVE_INTERVAL_SECONDS,
    STUDIO_AGENT_NAME,
    TELEPROMPTER_DEFAULT_FONT_SIZE_PX,
    TELEPROMPTER_DEFAULT_SPEED_WPS,
    TELEPROMPTER_FONT_SIZES,
    TELEPROMPTER_SPEED_MAX_WPS,
    TELEPROMPTER_SPEED_MIN_WPS,
    AssetPanelEntry,
    AssetType,
    CMFTriggerPayload,
    CMFTriggerResult,
    CrashRecoveryResult,
    IndexedDBChunk,
    RecordingMode,
    RecordingQualityConfig,
    S3UploadRequest,
    S3UploadResponse,
    StudioAspectRatio,
    StudioBlockError,
    StudioBlockRegistration,
    StudioBlockResult,
    StudioResolution,
    StudioSessionRecord,
    StudioSessionStatus,
    StreamConfig,
    StreamDestination,
    StreamHealthMetrics,
    TeleprompterConfig,
    TeleprompterScrollResult,
)

# ---------------------------------------------------------------------------
# SQL — studio_sessions table (§6 Data Model)
# ---------------------------------------------------------------------------

STUDIO_SESSIONS_SQL = """
CREATE TABLE IF NOT EXISTS studio_sessions (
    id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coach_id              UUID NOT NULL REFERENCES coaches(id),
    source_page_id        VARCHAR(255),
    recording_mode        VARCHAR(30) NOT NULL,
    aspect_ratio          VARCHAR(5) NOT NULL,
    resolution            VARCHAR(10) NOT NULL,
    s3_recording_url      TEXT,
    s3_vod_url            TEXT,
    duration_seconds      INTEGER,
    is_stream             BOOLEAN DEFAULT FALSE,
    stream_destinations   JSONB,
    cmf_pipeline_template VARCHAR(50),
    cmf_job_id            UUID,
    receipt_chain_id      UUID REFERENCES receipt_chain(id),
    status                VARCHAR(20) DEFAULT 'recording',
    started_at            TIMESTAMPTZ NOT NULL,
    ended_at              TIMESTAMPTZ,
    created_at            TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_studio_sessions_coach
    ON studio_sessions(coach_id);
CREATE INDEX IF NOT EXISTS idx_studio_sessions_status
    ON studio_sessions(status);
"""

# ---------------------------------------------------------------------------
# Protocols (dependency injection boundaries)
# ---------------------------------------------------------------------------


class S3ClientProtocol(Protocol):
    async def generate_presigned_url(
        self, key: str, file_size: int, expires_in: int,
    ) -> str: ...

    async def initiate_multipart_upload(self, key: str) -> str: ...


class CMFPipelineProtocol(Protocol):
    async def trigger(
        self, template: str, s3_url: str, coach_id: str, metadata: dict[str, Any],
    ) -> str: ...


class DatabaseProtocol(Protocol):
    async def insert_session(self, record: dict[str, Any]) -> str: ...
    async def update_session(self, session_id: str, fields: dict[str, Any]) -> None: ...
    async def get_session(self, session_id: str) -> Optional[dict[str, Any]]: ...


# ---------------------------------------------------------------------------
# Receipt Chain utilities (FR47 DEP-ENG-041)
# ---------------------------------------------------------------------------


def _sha256(payload: Any) -> str:
    """Deterministic SHA-256 hash for receipt chain payloads."""
    raw = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _build_receipt(
    stage_name: str,
    agent_name: str,
    input_payload: Any,
    output_payload: Any,
    previous_receipt_hash: str = "",
) -> dict[str, Any]:
    """Construct a FR47 DEP-ENG-041 receipt."""
    return {
        "receipt_id": str(uuid.uuid4()),
        "previous_receipt_hash": previous_receipt_hash,
        "input_payload_hash": _sha256(input_payload),
        "output_payload_hash": _sha256(output_payload),
        "stage_name": stage_name,
        "agent_name": agent_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Stage 1: Plugin Registration & UI Shell — DEP-ENG-087
# ---------------------------------------------------------------------------


def register_studio_plugin() -> StudioBlockRegistration:
    """Register the /studio slash command in AFFiNE BlockSuite.

    §4 Stage 1 Steps 1-6: Plugin scaffolding with 5 UI panels.
    """
    return StudioBlockRegistration()


# ---------------------------------------------------------------------------
# Stage 2: Recording Engine — DEP-ENG-088
# ---------------------------------------------------------------------------


def resolve_quality_config(
    mode: str,
    resolution: Optional[str] = None,
) -> RecordingQualityConfig:
    """Resolve the recording quality configuration for a given mode.

    §4 Stage 2 + FB §3.2 Quality Tiers.
    AC3 enforcement: short_form_vertical forces 1080p only.
    """
    if mode not in QUALITY_TIERS:
        raise ValueError(
            f"{StudioBlockError.INVALID_MODE_RESOLUTION.value}: "
            f"Unknown recording mode '{mode}'"
        )

    tier = QUALITY_TIERS[mode]
    target_resolution = resolution or tier["default_resolution"]

    # AC3: Shorts mode — 1080p mandatory, 720p disabled
    if mode == RecordingMode.SHORT_FORM_VERTICAL.value:
        if target_resolution != StudioResolution.HD_1080.value:
            raise ValueError(
                f"{StudioBlockError.INVALID_MODE_RESOLUTION.value}: "
                f"Short-form vertical mode requires 1080p. "
                f"720p is disabled for this mode."
            )

    if target_resolution not in tier["selectable_resolutions"]:
        raise ValueError(
            f"{StudioBlockError.INVALID_MODE_RESOLUTION.value}: "
            f"Resolution '{target_resolution}' not available for mode '{mode}'. "
            f"Available: {tier['selectable_resolutions']}"
        )

    # Compute width/height based on resolution selection
    width = tier["width"]
    height = tier["height"]
    if target_resolution == StudioResolution.HD_720.value:
        if tier["aspect_ratio"] == StudioAspectRatio.LANDSCAPE_16_9.value:
            width, height = 1280, 720
        else:
            width, height = 720, 1280

    return RecordingQualityConfig(
        resolution=target_resolution,
        aspect_ratio=tier["aspect_ratio"],
        width=width,
        height=height,
        video_bitrate_bps=tier["bitrate_bps"],
        framerate=DEFAULT_FRAMERATE,
    )


def validate_indexeddb_chunk(chunk: IndexedDBChunk) -> bool:
    """Stress Test Q34: Validate an IndexedDB chunk meets the 5s Blob spec.

    Every chunk must have a valid session_id, non-negative sequence, and
    duration matching the mandated 5-second interval.
    """
    return (
        len(chunk.session_id) > 0
        and chunk.sequence_number >= 0
        and chunk.blob_size_bytes >= 0
        and chunk.duration_seconds == INDEXEDDB_CHUNK_INTERVAL_SECONDS
    )


# ---------------------------------------------------------------------------
# Stage 3: Teleprompter Component — DEP-ENG-089
# ---------------------------------------------------------------------------


def calculate_teleprompter_scroll(
    word_count: int,
    speed_wps: float = TELEPROMPTER_DEFAULT_SPEED_WPS,
) -> TeleprompterScrollResult:
    """Calculate scroll duration for teleprompter text.

    §4 Stage 3 Step 4: Speed control 1.0–5.0 words-per-second.
    AC4: 500 words at 2.5 w/s → ~200 seconds (±10%).
    """
    if speed_wps < TELEPROMPTER_SPEED_MIN_WPS:
        speed_wps = TELEPROMPTER_SPEED_MIN_WPS
    elif speed_wps > TELEPROMPTER_SPEED_MAX_WPS:
        speed_wps = TELEPROMPTER_SPEED_MAX_WPS

    if word_count <= 0:
        return TeleprompterScrollResult(
            word_count=0, speed_wps=speed_wps, scroll_duration_seconds=0.0,
        )

    duration = word_count / speed_wps

    return TeleprompterScrollResult(
        word_count=word_count,
        speed_wps=speed_wps,
        scroll_duration_seconds=round(duration, 2),
    )


def validate_teleprompter_config(config: TeleprompterConfig) -> bool:
    """Validate teleprompter configuration."""
    return (
        TELEPROMPTER_SPEED_MIN_WPS <= config.speed_wps <= TELEPROMPTER_SPEED_MAX_WPS
        and config.font_size_px in TELEPROMPTER_FONT_SIZES
    )


def extract_text_blocks(page_blocks: list[dict[str, Any]]) -> str:
    """§4 Stage 3 Step 2: Extract text from AFFiNE page blocks.

    Strip non-text blocks (images, embeds).
    """
    text_parts: list[str] = []
    for block in page_blocks:
        block_type = block.get("type", "")
        if block_type in ("text", "paragraph", "heading", "list", "quote"):
            content = block.get("content", "")
            if isinstance(content, str) and content.strip():
                text_parts.append(content.strip())
    return " ".join(text_parts)


# ---------------------------------------------------------------------------
# Stage 4: Asset Panel — DEP-ENG-090
# ---------------------------------------------------------------------------


def scan_block_tree(page_blocks: list[dict[str, Any]]) -> list[AssetPanelEntry]:
    """§4 Stage 4 Steps 1-2: Scan block tree for visual assets.

    Filters for: image blocks, Excalidraw embed blocks, CVE Canva blocks.
    Returns clickable thumbnail entries.
    """
    assets: list[AssetPanelEntry] = []
    for block in page_blocks:
        block_type = block.get("type", "")
        block_id = block.get("id", str(uuid.uuid4()))

        if block_type == "image":
            assets.append(AssetPanelEntry(
                asset_type=AssetType.IMAGE.value,
                source_block_id=block_id,
                thumbnail_url=block.get("url", None),
            ))
        elif block_type == "excalidraw":
            assets.append(AssetPanelEntry(
                asset_type=AssetType.EXCALIDRAW.value,
                source_block_id=block_id,
                thumbnail_url=block.get("thumbnail_url", None),
            ))
        elif block_type == "canva":
            assets.append(AssetPanelEntry(
                asset_type=AssetType.CANVA.value,
                source_block_id=block_id,
                thumbnail_url=block.get("thumbnail_url", None),
            ))

    return assets


def toggle_asset_overlay(asset: AssetPanelEntry) -> AssetPanelEntry:
    """§4 Stage 4 Steps 3-4: Click-to-overlay toggle.

    On click: display asset full-screen on recording canvas.
    On click again: dismiss overlay, return to webcam-only.
    """
    return AssetPanelEntry(
        asset_id=asset.asset_id,
        asset_type=asset.asset_type,
        source_block_id=asset.source_block_id,
        thumbnail_url=asset.thumbnail_url,
        is_overlay_active=not asset.is_overlay_active,
    )


# ---------------------------------------------------------------------------
# Stage 5: S3 Upload & CMF Pipeline Trigger — DEP-ENG-091, DEP-ENG-092
# ---------------------------------------------------------------------------


def resolve_cmf_template(recording_mode: str) -> str:
    """§4 Stage 5 Step 4: Mode → CMF pipeline template mapping.

    AC7: youtube_longform → 'youtube_longform' template.
    """
    template = CMF_TEMPLATE_MAP.get(recording_mode)
    if not template:
        raise ValueError(
            f"{StudioBlockError.CMF_TRIGGER_FAILED.value}: "
            f"No CMF template for mode '{recording_mode}'"
        )
    return template


def compute_crash_recovery(
    chunks: list[IndexedDBChunk],
) -> CrashRecoveryResult:
    """Stress Test Q34 + AC9: Aggregate IndexedDB chunks for crash recovery.

    When browser tab is killed, recoverable duration = sum of chunk durations.
    AC9: At least 60 seconds must be recoverable from a 2-minute recording.
    """
    if not chunks:
        return CrashRecoveryResult(
            session_id="",
            chunks_recovered=0,
            total_duration_seconds=0.0,
            is_recoverable=False,
        )

    session_id = chunks[0].session_id
    sorted_chunks = sorted(chunks, key=lambda c: c.sequence_number)
    total_duration = sum(c.duration_seconds for c in sorted_chunks)

    return CrashRecoveryResult(
        session_id=session_id,
        chunks_recovered=len(sorted_chunks),
        total_duration_seconds=total_duration,
        is_recoverable=total_duration >= CRASH_RECOVERY_MIN_SECONDS,
    )


# ---------------------------------------------------------------------------
# Stage 6: Streaming Engine — DEP-ENG-093
# ---------------------------------------------------------------------------


def build_stream_config(
    session_id: str,
    destinations: list[StreamDestination],
    service_base_url: str = "wss://stream.ccp.aws.com",
) -> StreamConfig:
    """§4 Stage 6 Steps 1-7: Build streaming configuration.

    WebSocket endpoint: /ws/stream/{session_id}
    RTMP destinations: YouTube Live, Facebook Live, Custom RTMP.
    Parallel S3 VOD archive enabled by default.
    """
    ws_url = f"{service_base_url}/ws/stream/{session_id}"
    return StreamConfig(
        session_id=session_id,
        websocket_url=ws_url,
        destinations=destinations,
        parallel_s3_archive=True,
        health=StreamHealthMetrics(connection_status="connecting"),
    )


# ---------------------------------------------------------------------------
# CCP Studio Block Service (orchestrates all 7 stages)
# ---------------------------------------------------------------------------


class StudioBlockService:
    """CCP Studio Block service — orchestrates recording, streaming, and content pipeline.

    Implements all 7 pipeline stages (DEP-ENG-087 through DEP-ENG-093).
    All state mutations emit FR47 DEP-ENG-041 receipts.
    """

    def __init__(
        self,
        s3_client: S3ClientProtocol | None = None,
        cmf_pipeline: CMFPipelineProtocol | None = None,
        db: DatabaseProtocol | None = None,
    ) -> None:
        self._s3 = s3_client
        self._cmf = cmf_pipeline
        self._db = db
        self._receipt_chain: list[dict[str, Any]] = []

    @property
    def receipt_chain(self) -> list[dict[str, Any]]:
        """Access the receipt chain for verification."""
        return list(self._receipt_chain)

    def _emit_receipt(
        self,
        stage_name: str,
        input_payload: Any,
        output_payload: Any,
    ) -> dict[str, Any]:
        """Emit an FR47 DEP-ENG-041 receipt and append to chain."""
        prev_hash = ""
        if self._receipt_chain:
            prev_hash = _sha256(self._receipt_chain[-1])
        receipt = _build_receipt(
            stage_name=stage_name,
            agent_name=STUDIO_AGENT_NAME,
            input_payload=input_payload,
            output_payload=output_payload,
            previous_receipt_hash=prev_hash,
        )
        self._receipt_chain.append(receipt)
        return receipt

    # -- Stage 1: Plugin Registration (DEP-ENG-087) --

    def register(self) -> StudioBlockRegistration:
        """Register the CCP Studio Block plugin."""
        return register_studio_plugin()

    # -- Stage 2: Session Create + Recording Engine (DEP-ENG-088) --

    async def create_session(
        self,
        coach_id: str,
        recording_mode: str,
        resolution: Optional[str] = None,
        source_page_id: Optional[str] = None,
        is_stream: bool = False,
        stream_destinations: Optional[list[str]] = None,
    ) -> StudioBlockResult:
        """Create a new Studio session. State mutation → receipt."""
        try:
            quality = resolve_quality_config(recording_mode, resolution)
        except ValueError as exc:
            return StudioBlockResult(success=False, error=str(exc))

        session = StudioSessionRecord(
            coach_id=coach_id,
            source_page_id=source_page_id,
            recording_mode=recording_mode,
            aspect_ratio=quality.aspect_ratio,
            resolution=quality.resolution,
            is_stream=is_stream,
            stream_destinations=stream_destinations or [],
            status=(
                StudioSessionStatus.STREAMING.value
                if is_stream
                else StudioSessionStatus.RECORDING.value
            ),
        )

        # Persist session
        if self._db:
            await self._db.insert_session(session.model_dump(mode="json"))

        # Receipt: session-create (state mutation: INSERT studio_sessions)
        self._emit_receipt(
            stage_name="session-create",
            input_payload={
                "coach_id": coach_id,
                "recording_mode": recording_mode,
                "resolution": quality.resolution,
            },
            output_payload={
                "session_id": session.session_id,
                "status": session.status,
            },
        )

        return StudioBlockResult(success=True, session=session)

    # -- Stage 5: S3 Upload Completion (DEP-ENG-091) --

    async def complete_upload(
        self,
        session_id: str,
        s3_url: str,
        recording_mode: str,
        coach_id: str,
        source_page_id: Optional[str],
        duration: int,
    ) -> StudioBlockResult:
        """Handle upload completion and trigger CMF pipeline.

        §4 Stage 5 Steps 1-6.
        State mutations: UPDATE status → 'uploading' then 'processing'.
        """
        # Resolve CMF template (AC7)
        try:
            template = resolve_cmf_template(recording_mode)
        except ValueError as exc:
            return StudioBlockResult(success=False, error=str(exc))

        # CMF trigger
        cmf_job_id = str(uuid.uuid4())
        if self._cmf:
            cmf_job_id = await self._cmf.trigger(
                template=template,
                s3_url=s3_url,
                coach_id=coach_id,
                metadata={
                    "source_page_id": source_page_id,
                    "duration": duration,
                },
            )

        # Build updated session
        session = StudioSessionRecord(
            session_id=session_id,
            coach_id=coach_id,
            source_page_id=source_page_id,
            recording_mode=recording_mode,
            aspect_ratio=QUALITY_TIERS[recording_mode]["aspect_ratio"],
            resolution=QUALITY_TIERS[recording_mode]["default_resolution"],
            s3_recording_url=s3_url,
            duration_seconds=duration,
            cmf_pipeline_template=template,
            cmf_job_id=cmf_job_id,
            status=StudioSessionStatus.PROCESSING.value,
        )

        # Persist state update
        if self._db:
            await self._db.update_session(session_id, {
                "s3_recording_url": s3_url,
                "duration_seconds": duration,
                "cmf_pipeline_template": template,
                "cmf_job_id": cmf_job_id,
                "status": StudioSessionStatus.PROCESSING.value,
            })

        # Receipt: upload-complete (state mutation: UPDATE studio_sessions)
        self._emit_receipt(
            stage_name="upload-complete",
            input_payload={
                "session_id": session_id,
                "s3_url": s3_url,
                "recording_mode": recording_mode,
            },
            output_payload={
                "session_id": session_id,
                "status": StudioSessionStatus.PROCESSING.value,
                "s3_recording_url": s3_url,
            },
        )

        # Receipt: cmf-trigger (state mutation: CMF job created)
        self._emit_receipt(
            stage_name="cmf-trigger",
            input_payload={
                "session_id": session_id,
                "s3_url": s3_url,
                "recording_mode": recording_mode,
                "template": template,
            },
            output_payload={
                "cmf_job_id": cmf_job_id,
                "cmf_pipeline_template": template,
            },
        )

        return StudioBlockResult(success=True, session=session)

    # -- Stage 6: Streaming (DEP-ENG-093) --

    async def start_stream(
        self,
        session_id: str,
        coach_id: str,
        recording_mode: str,
        destinations: list[StreamDestination],
        source_page_id: Optional[str] = None,
    ) -> StudioBlockResult:
        """Start a live stream via ccp-stream-service.

        §4 Stage 6: WebSocket → RTMP mux + parallel S3 VOD archive.
        """
        stream_config = build_stream_config(session_id, destinations)

        session = StudioSessionRecord(
            session_id=session_id,
            coach_id=coach_id,
            source_page_id=source_page_id,
            recording_mode=recording_mode,
            aspect_ratio=QUALITY_TIERS.get(
                recording_mode, QUALITY_TIERS[RecordingMode.WEBINAR_VOD.value],
            )["aspect_ratio"],
            resolution=QUALITY_TIERS.get(
                recording_mode, QUALITY_TIERS[RecordingMode.WEBINAR_VOD.value],
            )["default_resolution"],
            is_stream=True,
            stream_destinations=[d.rtmp_url for d in destinations],
            status=StudioSessionStatus.STREAMING.value,
        )

        if self._db:
            await self._db.insert_session(session.model_dump(mode="json"))

        # Receipt: session-create (streaming session)
        self._emit_receipt(
            stage_name="session-create",
            input_payload={
                "session_id": session_id,
                "coach_id": coach_id,
                "recording_mode": recording_mode,
                "is_stream": True,
                "destinations": [d.rtmp_url for d in destinations],
            },
            output_payload={
                "session_id": session_id,
                "status": StudioSessionStatus.STREAMING.value,
                "websocket_url": stream_config.websocket_url,
            },
        )

        return StudioBlockResult(success=True, session=session)

    # -- Recovery (Stress Test Q34) --

    async def recover_from_crash(
        self,
        session_id: str,
        chunks: list[IndexedDBChunk],
    ) -> CrashRecoveryResult:
        """Recover a recording from IndexedDB chunks after browser crash.

        Stress Test Q34 + AC9: Background Web Worker aggregates immutable
        IndexedDB chunks and executes S3 multipart upload.
        """
        result = compute_crash_recovery(chunks)

        if result.is_recoverable and self._s3:
            s3_key = f"crash-recovery/{session_id}/{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}.webm"
            upload_url = await self._s3.initiate_multipart_upload(s3_key)
            result.s3_multipart_upload_url = upload_url

        return result

    # -- Receipt chain verification --

    def verify_receipt_chain(self) -> bool:
        """Verify the receipt chain is unbroken.

        Each receipt's previous_receipt_hash must match the SHA-256 of the
        prior receipt. First receipt has empty previous_receipt_hash.
        """
        if not self._receipt_chain:
            return True

        if self._receipt_chain[0]["previous_receipt_hash"] != "":
            return False

        for i in range(1, len(self._receipt_chain)):
            expected_hash = _sha256(self._receipt_chain[i - 1])
            if self._receipt_chain[i]["previous_receipt_hash"] != expected_hash:
                return False

        return True
