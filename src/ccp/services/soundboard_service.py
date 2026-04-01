"""FR-CA11-17 — Studio Soundboard & Programmable Audio.

DEP-ENG-094: Soundboard Component (SFX buttons UI)
DEP-ENG-095: Audio Mixer Pipeline (Web Audio API graph)
DEP-ENG-096: Audio Library Browser (S3 library)
DEP-ENG-097: Audio Preferences Model (studio_preferences table)
DEP-ENG-098: Music Controller (fade transitions, stop-all)

Upstream: DEP-ENG-088 (FR-CA11-16 Recording Engine)
Stress Test: Q35 (AEC + ducking architecture — foundation laid here)
"""
from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Optional, Protocol

from src.ccp.models.ca11_models import (
    ALLOWED_AUDIO_FORMATS,
    AUDIO_MAX_FILE_SIZE_BYTES,
    DEFAULT_MUSIC_TRACKS,
    DEFAULT_SFX_SLOTS,
    MUSIC_FADE_MS,
    MUSIC_GAIN_DEFAULT,
    MUSIC_MAX_DURATION_SECONDS,
    SFX_GAIN_DEFAULT,
    SFX_MAX_DURATION_SECONDS,
    SFX_SLOT_COUNT,
    STOP_ALL_RAMP_MS,
    VOICE_GAIN_DEFAULT,
    AudioMixerConfig,
    AudioUploadRequest,
    AudioUploadValidation,
    FadeSpec,
    MixerChannelConfig,
    MusicTrackConfig,
    MusicTrackType,
    SFXSlotConfig,
    SoundboardError,
    SoundboardResult,
    StudioPreferences,
)

# ---------------------------------------------------------------------------
# SQL — studio_preferences table (§5 Data Model)
# ---------------------------------------------------------------------------

STUDIO_PREFERENCES_SQL = """
CREATE TABLE IF NOT EXISTS studio_preferences (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coach_id        UUID NOT NULL UNIQUE REFERENCES coaches(id),
    sfx_slots       JSONB DEFAULT '[]',
    music_tracks    JSONB DEFAULT '{}',
    voice_volume    REAL DEFAULT 1.0,
    guest_layout    VARCHAR(20) DEFAULT 'pip',
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);
"""

# ---------------------------------------------------------------------------
# Protocols
# ---------------------------------------------------------------------------


class PreferencesStoreProtocol(Protocol):
    async def get_preferences(self, coach_id: str) -> Optional[dict[str, Any]]: ...
    async def save_preferences(self, coach_id: str, data: dict[str, Any]) -> None: ...


class AudioStorageProtocol(Protocol):
    async def upload_audio(self, key: str, data: bytes) -> str: ...
    async def list_library(self, prefix: str) -> list[str]: ...


# ---------------------------------------------------------------------------
# Receipt utilities (FR47 DEP-ENG-041)
# ---------------------------------------------------------------------------


def _sha256(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _build_receipt(
    stage_name: str,
    agent_name: str,
    input_payload: Any,
    output_payload: Any,
    previous_receipt_hash: str = "",
) -> dict[str, Any]:
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
# Stage 1: Audio Mixer Pipeline — DEP-ENG-095
# ---------------------------------------------------------------------------


def build_audio_mixer_config(voice_volume: float = VOICE_GAIN_DEFAULT) -> AudioMixerConfig:
    """§4 Stage 1: Web Audio API mixer graph configuration.

    Creates: voice GainNode, 5 SFX GainNodes, 1 music GainNode,
    all routed to AudioContext.destination.
    """
    sfx_channels = [
        MixerChannelConfig(channel_name=f"sfx_{i+1}", gain=SFX_GAIN_DEFAULT)
        for i in range(SFX_SLOT_COUNT)
    ]
    return AudioMixerConfig(
        voice_channel=MixerChannelConfig(channel_name="voice", gain=voice_volume),
        sfx_channels=sfx_channels,
        music_channel=MixerChannelConfig(channel_name="music", gain=MUSIC_GAIN_DEFAULT),
    )


# ---------------------------------------------------------------------------
# Stage 2 + 3: SFX & Music — DEP-ENG-094, DEP-ENG-098
# ---------------------------------------------------------------------------


def resolve_default_preferences(coach_id: str) -> StudioPreferences:
    """Create default preferences with 5 SFX slots + 4 music tracks."""
    sfx_slots = [
        SFXSlotConfig(slot=s["slot"], label=s["label"], s3_url=s["s3_url"], volume=s["volume"])
        for s in DEFAULT_SFX_SLOTS
    ]
    music_tracks = {
        k: MusicTrackConfig(s3_url=v["s3_url"], volume=v["volume"], fade_ms=v["fade_ms"])
        for k, v in DEFAULT_MUSIC_TRACKS.items()
    }
    return StudioPreferences(
        coach_id=coach_id,
        sfx_slots=sfx_slots,
        music_tracks=music_tracks,
    )


def calculate_fade(
    current_volume: float,
    target_volume: float,
    duration_ms: int = MUSIC_FADE_MS,
) -> FadeSpec:
    """§4 Stage 3 Step 2: Compute fade transition between volumes."""
    return FadeSpec(
        start_volume=max(0.0, min(1.0, current_volume)),
        end_volume=max(0.0, min(1.0, target_volume)),
        duration_ms=max(0, duration_ms),
    )


def calculate_stop_all_fade() -> FadeSpec:
    """§4 Stage 3 Step 3: Stop-All ramp to 0 in 100ms."""
    return FadeSpec(start_volume=1.0, end_volume=0.0, duration_ms=STOP_ALL_RAMP_MS)


# ---------------------------------------------------------------------------
# Stage 4: Upload Validation — DEP-ENG-096
# ---------------------------------------------------------------------------


def validate_audio_upload(request: AudioUploadRequest) -> AudioUploadValidation:
    """§4 Stage 4 Step 4: Validate audio upload constraints.

    SFX: max 10s, max 5MB, MP3/WAV.
    Music: max 60s, max 5MB, MP3/WAV.
    """
    ext = request.file_name.rsplit(".", 1)[-1].lower() if "." in request.file_name else ""
    if ext not in ALLOWED_AUDIO_FORMATS:
        return AudioUploadValidation(
            is_valid=False,
            error=f"{SoundboardError.INVALID_FORMAT.value}: "
                  f"Must be {', '.join(ALLOWED_AUDIO_FORMATS)}. Got '{ext}'.",
        )

    if request.file_size_bytes > AUDIO_MAX_FILE_SIZE_BYTES:
        return AudioUploadValidation(
            is_valid=False,
            error=f"{SoundboardError.UPLOAD_TOO_LARGE.value}: "
                  f"Max {AUDIO_MAX_FILE_SIZE_BYTES} bytes. Got {request.file_size_bytes}.",
        )

    max_dur = SFX_MAX_DURATION_SECONDS if request.is_sfx else MUSIC_MAX_DURATION_SECONDS
    if request.duration_seconds > max_dur:
        return AudioUploadValidation(
            is_valid=False,
            error=f"{SoundboardError.UPLOAD_TOO_LONG.value}: "
                  f"Max {max_dur}s for {'SFX' if request.is_sfx else 'music'}. "
                  f"Got {request.duration_seconds}s.",
        )

    return AudioUploadValidation(
        is_valid=True,
        max_duration=max_dur,
        max_size=AUDIO_MAX_FILE_SIZE_BYTES,
    )


# ---------------------------------------------------------------------------
# Soundboard Service
# ---------------------------------------------------------------------------


class SoundboardService:
    """FR-CA11-17 — Soundboard & Programmable Audio service.

    Manages SFX/music preferences, upload validation, mixer config,
    and fade transitions. All preference mutations emit FR47 receipts.
    """

    AGENT_NAME = "Diego"

    def __init__(
        self,
        store: PreferencesStoreProtocol | None = None,
        audio_storage: AudioStorageProtocol | None = None,
    ) -> None:
        self._store = store
        self._audio = audio_storage
        self._receipt_chain: list[dict[str, Any]] = []

    @property
    def receipt_chain(self) -> list[dict[str, Any]]:
        return list(self._receipt_chain)

    def _emit_receipt(
        self, stage_name: str, input_payload: Any, output_payload: Any,
    ) -> dict[str, Any]:
        prev_hash = ""
        if self._receipt_chain:
            prev_hash = _sha256(self._receipt_chain[-1])
        receipt = _build_receipt(
            stage_name=stage_name,
            agent_name=self.AGENT_NAME,
            input_payload=input_payload,
            output_payload=output_payload,
            previous_receipt_hash=prev_hash,
        )
        self._receipt_chain.append(receipt)
        return receipt

    # -- Load / resolve preferences --

    async def get_preferences(self, coach_id: str) -> StudioPreferences:
        """Load coach preferences, falling back to defaults."""
        if self._store:
            data = await self._store.get_preferences(coach_id)
            if data:
                return StudioPreferences(**data)
        return resolve_default_preferences(coach_id)

    # -- Save preferences (state mutation → receipt) --

    async def save_preferences(self, prefs: StudioPreferences) -> SoundboardResult:
        """Persist preferences. §4 Stage 4 Step 5 + receipt."""
        if self._store:
            await self._store.save_preferences(
                prefs.coach_id, prefs.model_dump(mode="json"),
            )

        self._emit_receipt(
            stage_name="preferences-update",
            input_payload={"coach_id": prefs.coach_id},
            output_payload={
                "coach_id": prefs.coach_id,
                "sfx_count": len(prefs.sfx_slots),
                "music_count": len(prefs.music_tracks),
            },
        )
        return SoundboardResult(success=True, preferences=prefs)

    # -- Update SFX slot --

    async def update_sfx_slot(
        self,
        coach_id: str,
        slot_index: int,
        label: str,
        s3_url: str,
        volume: float = SFX_GAIN_DEFAULT,
    ) -> SoundboardResult:
        """Replace a specific SFX slot. AC4 (customization persistence)."""
        if slot_index < 1 or slot_index > SFX_SLOT_COUNT:
            return SoundboardResult(
                success=False,
                error=f"{SoundboardError.INVALID_SLOT_INDEX.value}: "
                      f"Slot must be 1-{SFX_SLOT_COUNT}. Got {slot_index}.",
            )

        prefs = await self.get_preferences(coach_id)
        new_slot = SFXSlotConfig(slot=slot_index, label=label, s3_url=s3_url, volume=volume)

        updated_slots = [s for s in prefs.sfx_slots if s.slot != slot_index]
        updated_slots.append(new_slot)
        updated_slots.sort(key=lambda s: s.slot)
        prefs.sfx_slots = updated_slots

        return await self.save_preferences(prefs)

    # -- Update music track --

    async def update_music_track(
        self,
        coach_id: str,
        track_type: str,
        s3_url: str,
        volume: float = MUSIC_GAIN_DEFAULT,
        fade_ms: int = MUSIC_FADE_MS,
    ) -> SoundboardResult:
        """Replace a music track. §4 Stage 4."""
        valid_types = [t.value for t in MusicTrackType]
        if track_type not in valid_types:
            return SoundboardResult(
                success=False,
                error=f"{SoundboardError.INVALID_TRACK_TYPE.value}: "
                      f"Must be one of {valid_types}. Got '{track_type}'.",
            )

        prefs = await self.get_preferences(coach_id)
        prefs.music_tracks[track_type] = MusicTrackConfig(
            s3_url=s3_url, volume=volume, fade_ms=fade_ms,
        )
        return await self.save_preferences(prefs)

    # -- Mixer config --

    def build_mixer(self, voice_volume: float = VOICE_GAIN_DEFAULT) -> AudioMixerConfig:
        """Build the Web Audio API mixer graph config."""
        return build_audio_mixer_config(voice_volume)

    # -- Fade calculations --

    @staticmethod
    def fade_transition(
        current_volume: float, target_volume: float, duration_ms: int = MUSIC_FADE_MS,
    ) -> FadeSpec:
        """Calculate a volume fade transition."""
        return calculate_fade(current_volume, target_volume, duration_ms)

    @staticmethod
    def stop_all() -> FadeSpec:
        """AC6: Stop-all ramp to 0 in 100ms."""
        return calculate_stop_all_fade()

    # -- Receipt chain verification --

    def verify_receipt_chain(self) -> bool:
        if not self._receipt_chain:
            return True
        if self._receipt_chain[0]["previous_receipt_hash"] != "":
            return False
        for i in range(1, len(self._receipt_chain)):
            expected = _sha256(self._receipt_chain[i - 1])
            if self._receipt_chain[i]["previous_receipt_hash"] != expected:
                return False
        return True
