"""Unit tests for FR-ERA3-17 — Voice Prompt Engine.
Job selection, prestige gate, and fallback policy."""
from src.ccp.models.voice_prompt_engine_models import (
    DeliverySurface, EmotionalJob, JobSelectionReason, PreRecordedFallbackPack,
    PromptStatus, RenderSource, VoicePromptTriggerContext,
)
from src.ccp.services.voice_prompt_engine import (
    ConsciousVoiceSynthesisAdapter, PreRecordedFallbackPackResolver,
    SonicPrestigeGate, VoicePromptDecisionResolver, VoicePromptEngineService,
)

def _ctx(reason: JobSelectionReason) -> VoicePromptTriggerContext:
    return VoicePromptTriggerContext(coach_id="coach-001", user_id="user-001", surface=DeliverySurface.TELEGRAM, reason=reason, locale="en")

# ── AC1: One-job selection ──
class TestSessionStartSelectsOrientOnly:
    def test(self):
        assert VoicePromptDecisionResolver().resolve(_ctx(JobSelectionReason.SESSION_START)) == EmotionalJob.ORIENT

class TestHesitationRecoverySelectsRelieveOnly:
    def test(self):
        assert VoicePromptDecisionResolver().resolve(_ctx(JobSelectionReason.HESITATION_RECOVERY)) == EmotionalJob.RELIEVE

class TestCorrectionRequiredSelectsRedirectOnly:
    def test(self):
        assert VoicePromptDecisionResolver().resolve(_ctx(JobSelectionReason.CORRECTION_REQUIRED)) == EmotionalJob.REDIRECT

class TestWinConfirmedSelectsCelebrateOnly:
    def test(self):
        assert VoicePromptDecisionResolver().resolve(_ctx(JobSelectionReason.WIN_CONFIRMED)) == EmotionalJob.CELEBRATE

# ── AC4: Prestige gate ──
class TestRoboticRenderFailsPrestigeGate:
    def test(self):
        synth = ConsciousVoiceSynthesisAdapter()
        attempt = synth.synthesize(script="test", voice_dna_ref="ref", duration_target=20)
        gate = SonicPrestigeGate()
        result = gate.evaluate(attempt, provider_confidence=0.60, clipping_ratio=0.02, tonal_match=0.50)
        assert result.prestige_gate_passed is False
        assert result.rejection_reason is not None

class TestTonallyMismatchedRelievePromptFailsGate:
    def test(self):
        synth = ConsciousVoiceSynthesisAdapter()
        attempt = synth.synthesize(script="test", voice_dna_ref="ref", duration_target=20)
        gate = SonicPrestigeGate()
        result = gate.evaluate(attempt, provider_confidence=0.90, clipping_ratio=0.005, tonal_match=0.60)
        assert result.prestige_gate_passed is False

class TestCleanConsciousVoiceRenderPassesGate:
    def test(self):
        synth = ConsciousVoiceSynthesisAdapter()
        attempt = synth.synthesize(script="test", voice_dna_ref="ref", duration_target=20)
        gate = SonicPrestigeGate()
        result = gate.evaluate(attempt, provider_confidence=0.92, clipping_ratio=0.003, tonal_match=0.90)
        assert result.prestige_gate_passed is True

# ── AC3: Fallback policy ──
class TestConsciousVoiceOutageSetsRetryPendingWhenNoHumanPack:
    def test(self):
        engine = VoicePromptEngineService(synthesis_adapter=ConsciousVoiceSynthesisAdapter(available=False))
        result = engine.issue(_ctx(JobSelectionReason.WIN_CONFIRMED))
        assert result["status"] == PromptStatus.RETRY_PENDING

class TestJobMatchedHumanPackIsUsedWhenAvailable:
    def test(self):
        pack = PreRecordedFallbackPack(fallback_pack_id="FBP-001", coach_id="coach-001", emotional_job=EmotionalJob.CELEBRATE, locale="en", audio_asset_id="AST-HUM-001", transcript_reference="Congrats!", duration_seconds=15)
        engine = VoicePromptEngineService(synthesis_adapter=ConsciousVoiceSynthesisAdapter(available=False), fallback_packs=[pack])
        result = engine.issue(_ctx(JobSelectionReason.WIN_CONFIRMED))
        assert result["status"] == PromptStatus.FALLBACK_RENDERED
        assert result["attempt"].render_source == RenderSource.PRE_RECORDED_HUMAN

class TestGenericTtsProviderIsRejectedAtModelValidation:
    def test(self):
        import pytest
        with pytest.raises(ValueError):
            RenderSource("generic_tts")
