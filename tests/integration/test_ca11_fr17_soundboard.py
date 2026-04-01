"""FR-CA11-17 — Studio Soundboard & Programmable Audio — Integration Tests.

Covers all 6 Acceptance Criteria:
  AC1: SFX Playback (5 distinct SFX slots, pre-fetched, click-to-play)
  AC2: Music Fade (500ms fade-out → 500ms fade-in, no overlap)
  AC3: Volume Control (per-slot gain 0.0–1.0)
  AC4: Customization Persistence (save/load roundtrip)
  AC5: Recording Integration (mixer feeds into MediaRecorder)
  AC6: Stop All (ramp to 0 in 100ms)

DEP-IDs produced: DEP-ENG-094 through DEP-ENG-098
DEP-IDs consumed: DEP-ENG-088 (Recording Engine from FR-CA11-16)
"""
from __future__ import annotations

import asyncio

import pytest

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
    FadeSpec,
    MusicTrackConfig,
    MusicTrackType,
    SFXSlotConfig,
    SoundboardError,
    SoundboardResult,
    StudioPreferences,
)
from src.ccp.services.soundboard_service import (
    STUDIO_PREFERENCES_SQL,
    SoundboardService,
    build_audio_mixer_config,
    calculate_fade,
    calculate_stop_all_fade,
    resolve_default_preferences,
    validate_audio_upload,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

COACH_ID = "coach-sound-001"


def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# ===================================================================
# AC1 — SFX Playback (5 distinct SFX slots)  [6 tests]
# ===================================================================


class TestSFXSlots:
    def test_default_five_sfx_slots(self):
        prefs = resolve_default_preferences(COACH_ID)
        assert len(prefs.sfx_slots) == 5

    def test_default_slot_labels(self):
        prefs = resolve_default_preferences(COACH_ID)
        labels = [s.label for s in prefs.sfx_slots]
        assert "Drumroll" in labels
        assert "Comedy Horn" in labels
        assert "Applause" in labels
        assert "Record Scratch" in labels
        assert "Ding" in labels

    def test_slots_numbered_1_to_5(self):
        prefs = resolve_default_preferences(COACH_ID)
        slots = sorted([s.slot for s in prefs.sfx_slots])
        assert slots == [1, 2, 3, 4, 5]

    def test_default_sfx_volume(self):
        prefs = resolve_default_preferences(COACH_ID)
        for sfx in prefs.sfx_slots:
            assert sfx.volume == SFX_GAIN_DEFAULT

    def test_sfx_urls_point_to_s3(self):
        prefs = resolve_default_preferences(COACH_ID)
        for sfx in prefs.sfx_slots:
            assert sfx.s3_url.startswith("s3://ccp-assets/studio/sfx/defaults/")

    def test_service_get_default_preferences(self):
        svc = SoundboardService()
        prefs = _run(svc.get_preferences(COACH_ID))
        assert isinstance(prefs, StudioPreferences)
        assert len(prefs.sfx_slots) == 5


# ===================================================================
# AC2 — Music Fade (500ms transitions)  [7 tests]
# ===================================================================


class TestMusicFade:
    def test_default_four_music_tracks(self):
        prefs = resolve_default_preferences(COACH_ID)
        assert len(prefs.music_tracks) == 4
        for track_type in MusicTrackType:
            assert track_type.value in prefs.music_tracks

    def test_default_fade_duration(self):
        prefs = resolve_default_preferences(COACH_ID)
        for cfg in prefs.music_tracks.values():
            assert cfg.fade_ms == MUSIC_FADE_MS

    def test_fade_out_spec(self):
        fade = calculate_fade(0.5, 0.0, MUSIC_FADE_MS)
        assert fade.start_volume == 0.5
        assert fade.end_volume == 0.0
        assert fade.duration_ms == 500

    def test_fade_in_spec(self):
        fade = calculate_fade(0.0, 0.5, MUSIC_FADE_MS)
        assert fade.start_volume == 0.0
        assert fade.end_volume == 0.5
        assert fade.duration_ms == 500

    def test_crossfade_no_overlap(self):
        """Fade out intro → fade in celebration. Total transition = 1000ms."""
        fade_out = calculate_fade(0.5, 0.0, MUSIC_FADE_MS)
        fade_in = calculate_fade(0.0, 0.6, MUSIC_FADE_MS)
        total_ms = fade_out.duration_ms + fade_in.duration_ms
        assert total_ms == 1000

    def test_clamp_volume_above_one(self):
        fade = calculate_fade(1.5, 0.0, 500)
        assert fade.start_volume == 1.0

    def test_clamp_volume_below_zero(self):
        fade = calculate_fade(-0.5, 0.0, 500)
        assert fade.start_volume == 0.0

    def test_service_fade_transition(self):
        svc = SoundboardService()
        fade = svc.fade_transition(0.5, 0.0)
        assert isinstance(fade, FadeSpec)
        assert fade.duration_ms == MUSIC_FADE_MS


# ===================================================================
# AC3 — Volume Control (per-slot gain)  [5 tests]
# ===================================================================


class TestVolumeControl:
    def test_sfx_slot_custom_volume(self):
        slot = SFXSlotConfig(slot=1, label="Custom", s3_url="s3://test.mp3", volume=0.3)
        assert slot.volume == 0.3

    def test_music_track_custom_volume(self):
        track = MusicTrackConfig(s3_url="s3://track.mp3", volume=0.7)
        assert track.volume == 0.7

    def test_mixer_voice_gain(self):
        mixer = build_audio_mixer_config(voice_volume=0.9)
        assert mixer.voice_channel.gain == 0.9

    def test_mixer_sfx_channels_count(self):
        mixer = build_audio_mixer_config()
        assert len(mixer.sfx_channels) == SFX_SLOT_COUNT
        for ch in mixer.sfx_channels:
            assert ch.gain == SFX_GAIN_DEFAULT

    def test_mixer_music_default_gain(self):
        mixer = build_audio_mixer_config()
        assert mixer.music_channel.gain == MUSIC_GAIN_DEFAULT


# ===================================================================
# AC4 — Customization Persistence  [5 tests]
# ===================================================================


class TestCustomizationPersistence:
    def test_update_sfx_slot(self):
        svc = SoundboardService()
        result = _run(svc.update_sfx_slot(
            coach_id=COACH_ID,
            slot_index=3,
            label="Air Horn",
            s3_url="s3://custom/airhorn.mp3",
            volume=0.9,
        ))
        assert result.success is True
        slot3 = [s for s in result.preferences.sfx_slots if s.slot == 3][0]
        assert slot3.label == "Air Horn"
        assert slot3.s3_url == "s3://custom/airhorn.mp3"
        assert slot3.volume == 0.9

    def test_update_sfx_invalid_slot(self):
        svc = SoundboardService()
        result = _run(svc.update_sfx_slot(
            coach_id=COACH_ID, slot_index=6,
            label="Extra", s3_url="s3://test.mp3",
        ))
        assert result.success is False
        assert SoundboardError.INVALID_SLOT_INDEX.value in result.error

    def test_update_music_track(self):
        svc = SoundboardService()
        result = _run(svc.update_music_track(
            coach_id=COACH_ID,
            track_type=MusicTrackType.CELEBRATION.value,
            s3_url="s3://custom/my_celebration.mp3",
            volume=0.7,
        ))
        assert result.success is True
        cel = result.preferences.music_tracks[MusicTrackType.CELEBRATION.value]
        assert cel.s3_url == "s3://custom/my_celebration.mp3"
        assert cel.volume == 0.7

    def test_update_music_invalid_type(self):
        svc = SoundboardService()
        result = _run(svc.update_music_track(
            coach_id=COACH_ID, track_type="invalid",
            s3_url="s3://test.mp3",
        ))
        assert result.success is False
        assert SoundboardError.INVALID_TRACK_TYPE.value in result.error

    def test_preferences_roundtrip(self):
        svc = SoundboardService()
        prefs = _run(svc.get_preferences(COACH_ID))
        result = _run(svc.save_preferences(prefs))
        assert result.success is True
        assert result.preferences.coach_id == COACH_ID


# ===================================================================
# AC5 — Recording Integration (mixer graph)  [4 tests]
# ===================================================================


class TestRecordingIntegration:
    def test_mixer_config_has_all_channels(self):
        mixer = build_audio_mixer_config()
        assert mixer.voice_channel is not None
        assert mixer.music_channel is not None
        assert len(mixer.sfx_channels) == 5

    def test_mixer_sample_rate(self):
        mixer = build_audio_mixer_config()
        assert mixer.sample_rate == 48000

    def test_service_build_mixer(self):
        svc = SoundboardService()
        mixer = svc.build_mixer(voice_volume=0.8)
        assert isinstance(mixer, AudioMixerConfig)
        assert mixer.voice_channel.gain == 0.8

    def test_sfx_channel_names(self):
        mixer = build_audio_mixer_config()
        names = [ch.channel_name for ch in mixer.sfx_channels]
        assert names == ["sfx_1", "sfx_2", "sfx_3", "sfx_4", "sfx_5"]


# ===================================================================
# AC6 — Stop All (100ms ramp)  [3 tests]
# ===================================================================


class TestStopAll:
    def test_stop_all_ramp(self):
        fade = calculate_stop_all_fade()
        assert fade.end_volume == 0.0
        assert fade.duration_ms == STOP_ALL_RAMP_MS == 100

    def test_stop_all_from_max(self):
        fade = calculate_stop_all_fade()
        assert fade.start_volume == 1.0

    def test_service_stop_all(self):
        svc = SoundboardService()
        fade = svc.stop_all()
        assert isinstance(fade, FadeSpec)
        assert fade.duration_ms == 100
        assert fade.end_volume == 0.0


# ===================================================================
# Upload Validation  [6 tests]
# ===================================================================


class TestUploadValidation:
    def test_valid_sfx_upload(self):
        req = AudioUploadRequest(
            coach_id=COACH_ID, file_name="horn.mp3",
            file_size_bytes=500_000, duration_seconds=5.0, is_sfx=True,
        )
        result = validate_audio_upload(req)
        assert result.is_valid is True

    def test_sfx_too_long(self):
        req = AudioUploadRequest(
            coach_id=COACH_ID, file_name="long.mp3",
            file_size_bytes=500_000, duration_seconds=15.0, is_sfx=True,
        )
        result = validate_audio_upload(req)
        assert result.is_valid is False
        assert SoundboardError.UPLOAD_TOO_LONG.value in result.error

    def test_music_max_60s(self):
        req = AudioUploadRequest(
            coach_id=COACH_ID, file_name="track.wav",
            file_size_bytes=1_000_000, duration_seconds=59.0, is_sfx=False,
        )
        result = validate_audio_upload(req)
        assert result.is_valid is True

    def test_music_too_long(self):
        req = AudioUploadRequest(
            coach_id=COACH_ID, file_name="track.mp3",
            file_size_bytes=1_000_000, duration_seconds=65.0, is_sfx=False,
        )
        result = validate_audio_upload(req)
        assert result.is_valid is False

    def test_file_too_large(self):
        req = AudioUploadRequest(
            coach_id=COACH_ID, file_name="big.mp3",
            file_size_bytes=6_000_000, duration_seconds=5.0, is_sfx=True,
        )
        result = validate_audio_upload(req)
        assert result.is_valid is False
        assert SoundboardError.UPLOAD_TOO_LARGE.value in result.error

    def test_invalid_format(self):
        req = AudioUploadRequest(
            coach_id=COACH_ID, file_name="track.ogg",
            file_size_bytes=500_000, duration_seconds=5.0, is_sfx=True,
        )
        result = validate_audio_upload(req)
        assert result.is_valid is False
        assert SoundboardError.INVALID_FORMAT.value in result.error


# ===================================================================
# Receipt Chain  [4 tests]
# ===================================================================


class TestSoundboardReceipt:
    def test_save_preferences_emits_receipt(self):
        svc = SoundboardService()
        prefs = resolve_default_preferences(COACH_ID)
        _run(svc.save_preferences(prefs))
        assert len(svc.receipt_chain) == 1
        assert svc.receipt_chain[0]["stage_name"] == "preferences-update"

    def test_update_slot_emits_receipt(self):
        svc = SoundboardService()
        _run(svc.update_sfx_slot(COACH_ID, 1, "Custom", "s3://x.mp3"))
        assert len(svc.receipt_chain) == 1

    def test_multiple_updates_chain(self):
        svc = SoundboardService()
        _run(svc.update_sfx_slot(COACH_ID, 1, "A", "s3://a.mp3"))
        _run(svc.update_music_track(COACH_ID, "intro", "s3://b.mp3"))
        assert len(svc.receipt_chain) == 2
        assert svc.verify_receipt_chain() is True

    def test_receipt_chain_integrity(self):
        svc = SoundboardService()
        _run(svc.save_preferences(resolve_default_preferences(COACH_ID)))
        _run(svc.update_sfx_slot(COACH_ID, 2, "New", "s3://n.mp3"))
        _run(svc.update_music_track(COACH_ID, "celebration", "s3://c.mp3"))
        assert len(svc.receipt_chain) == 3
        assert svc.verify_receipt_chain() is True


# ===================================================================
# SQL & Constants  [3 tests]
# ===================================================================


class TestSQLAndConstants:
    def test_studio_preferences_sql(self):
        assert "studio_preferences" in STUDIO_PREFERENCES_SQL
        assert "coach_id" in STUDIO_PREFERENCES_SQL
        assert "sfx_slots" in STUDIO_PREFERENCES_SQL

    def test_default_sfx_count(self):
        assert len(DEFAULT_SFX_SLOTS) == 5

    def test_default_music_count(self):
        assert len(DEFAULT_MUSIC_TRACKS) == 4
