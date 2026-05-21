from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
from src.ccp.models.voice_prompt_engine_models import (
    DeliverySurface, EmotionalJob, JobSelectionReason, PreRecordedFallbackPack,
    PromptStatus, RenderSource, SonicBedProfile, VoicePromptDeliveryRecord,
    VoicePromptPacket, VoicePromptRenderAttempt, VoicePromptTelemetryRecord,
    VoicePromptTriggerContext,
)

def _now() -> datetime: return datetime.now(timezone.utc)
def _id(p: str) -> str: return f"{p}-{uuid4().hex[:8].upper()}"

# ── Deterministic one-job mapping (§5.3) ──
REASON_TO_JOB: dict[JobSelectionReason, EmotionalJob] = {
    JobSelectionReason.SESSION_START: EmotionalJob.ORIENT,
    JobSelectionReason.HESITATION_RECOVERY: EmotionalJob.RELIEVE,
    JobSelectionReason.DISCLOSURE_ACK: EmotionalJob.VALIDATE,
    JobSelectionReason.ACTION_READY: EmotionalJob.INVITE,
    JobSelectionReason.CORRECTION_REQUIRED: EmotionalJob.REDIRECT,
    JobSelectionReason.WIN_CONFIRMED: EmotionalJob.CELEBRATE,
}

# ── Controlled sonic bed registry (AC5) ──
SONIC_BED_REGISTRY: dict[EmotionalJob, SonicBedProfile] = {
    EmotionalJob.ORIENT: SonicBedProfile(bed_id="bed_orient_01", display_name="Grounded Clarity", emotional_job=EmotionalJob.ORIENT, fade_in_ms=150, fade_out_ms=200, target_gain=0.38, duration_ceiling_seconds=30),
    EmotionalJob.RELIEVE: SonicBedProfile(bed_id="bed_relieve_01", display_name="Soft Landing", emotional_job=EmotionalJob.RELIEVE, fade_in_ms=200, fade_out_ms=300, target_gain=0.32, duration_ceiling_seconds=25),
    EmotionalJob.VALIDATE: SonicBedProfile(bed_id="bed_validate_01", display_name="Warm Mirror", emotional_job=EmotionalJob.VALIDATE, fade_in_ms=180, fade_out_ms=250, target_gain=0.35, duration_ceiling_seconds=28),
    EmotionalJob.INVITE: SonicBedProfile(bed_id="bed_invite_01", display_name="Forward Pull", emotional_job=EmotionalJob.INVITE, fade_in_ms=100, fade_out_ms=180, target_gain=0.40, duration_ceiling_seconds=22),
    EmotionalJob.REDIRECT: SonicBedProfile(bed_id="bed_redirect_01", display_name="Steady Reset", emotional_job=EmotionalJob.REDIRECT, fade_in_ms=120, fade_out_ms=200, target_gain=0.36, duration_ceiling_seconds=24),
    EmotionalJob.CELEBRATE: SonicBedProfile(bed_id="bed_celebrate_01", display_name="Warm Lift", emotional_job=EmotionalJob.CELEBRATE, fade_in_ms=120, fade_out_ms=220, target_gain=0.42, duration_ceiling_seconds=24),
}

# ── Script templates per emotional job ──
JOB_SCRIPT_TEMPLATES: dict[EmotionalJob, str] = {
    EmotionalJob.ORIENT: "Here's where you are right now. {context}. Let's get clear on what this moment asks of you.",
    EmotionalJob.RELIEVE: "Take a breath. {context}. This is not a failure — it's friction, and friction is part of the work.",
    EmotionalJob.VALIDATE: "I see what you did there. {context}. That took honesty, and your honesty is the foundation.",
    EmotionalJob.INVITE: "You're ready for the next step. {context}. One clear move forward.",
    EmotionalJob.REDIRECT: "Let's reset. {context}. The direction needs adjusting, not you.",
    EmotionalJob.CELEBRATE: "That was a strong finish. {context}. You held the line and earned this.",
}

class VoicePromptDecisionResolver:
    def resolve(self, ctx: VoicePromptTriggerContext) -> EmotionalJob:
        return REASON_TO_JOB[ctx.reason]

class VoicePromptComposer:
    def compose(self, *, ctx: VoicePromptTriggerContext, job: EmotionalJob) -> str:
        context_parts = []
        if ctx.score_delta is not None:
            context_parts.append(f"Your score moved {ctx.score_delta:+.1f} points")
        if ctx.streak_days is not None and ctx.streak_days > 0:
            context_parts.append(f"{ctx.streak_days} days in a row")
        if ctx.source_session_id:
            context_parts.append(f"from session {ctx.source_session_id}")
        context_str = ", ".join(context_parts) if context_parts else "based on your recent activity"
        return JOB_SCRIPT_TEMPLATES[job].format(context=context_str)

class VoiceDNAAlignmentBridge:
    def resolve_profile_ref(self, coach_id: str) -> str:
        return f"VDNA-{coach_id.upper()}"

class SonicBedResolver:
    def resolve(self, job: EmotionalJob) -> SonicBedProfile:
        return SONIC_BED_REGISTRY[job]

class ConsciousVoiceSynthesisAdapter:
    def __init__(self, available: bool = True) -> None:
        self._available = available
    def is_available(self) -> bool:
        return self._available
    def synthesize(self, *, script: str, voice_dna_ref: str, duration_target: int) -> VoicePromptRenderAttempt:
        return VoicePromptRenderAttempt(
            render_attempt_id=_id("VPR"), voice_prompt_id="pending",
            render_source=RenderSource.CONSCIOUS_VOICE, provider_reference=_id("cv-job"),
            audio_asset_id=_id("AST-AUDIO"), sample_rate_hz=48000,
            duration_seconds=min(duration_target, 90), prestige_gate_passed=False,
            created_at=_now(),
        )

class SonicPrestigeGate:
    CONFIDENCE_THRESHOLD = 0.85
    CLIPPING_THRESHOLD = 0.01
    TONAL_MATCH_THRESHOLD = 0.80

    def evaluate(self, attempt: VoicePromptRenderAttempt, *, provider_confidence: float = 0.90, clipping_ratio: float = 0.005, tonal_match: float = 0.88) -> VoicePromptRenderAttempt:
        reasons = []
        if provider_confidence < self.CONFIDENCE_THRESHOLD:
            reasons.append(f"provider_confidence={provider_confidence:.2f}<{self.CONFIDENCE_THRESHOLD}")
        if clipping_ratio > self.CLIPPING_THRESHOLD:
            reasons.append(f"clipping_ratio={clipping_ratio:.3f}>{self.CLIPPING_THRESHOLD}")
        if tonal_match < self.TONAL_MATCH_THRESHOLD:
            reasons.append(f"tonal_match={tonal_match:.2f}<{self.TONAL_MATCH_THRESHOLD}")
        if reasons:
            attempt.prestige_gate_passed = False
            attempt.rejection_reason = "; ".join(reasons)
        else:
            attempt.prestige_gate_passed = True
            attempt.rejection_reason = None
        return attempt

class PreRecordedFallbackPackResolver:
    def __init__(self, packs: list[PreRecordedFallbackPack] | None = None) -> None:
        self._packs = packs or []
    def find(self, *, coach_id: str, job: EmotionalJob, locale: str) -> PreRecordedFallbackPack | None:
        for p in self._packs:
            if p.coach_id == coach_id and p.emotional_job == job and p.locale == locale:
                return p
        return None

class VoicePromptDispatchCoordinator:
    def dispatch(self, *, packet: VoicePromptPacket, attempt: VoicePromptRenderAttempt) -> VoicePromptDeliveryRecord:
        return VoicePromptDeliveryRecord(
            delivery_id=_id("VPD"), voice_prompt_id=packet.voice_prompt_id,
            surface=packet.surface, dispatched_at=_now(),
            delivery_status=PromptStatus.DISPATCHED, retry_count=0,
        )

class VoicePromptTelemetryBridge:
    def record(self, *, voice_prompt_id: str, telemetry_fails: bool = False) -> VoicePromptTelemetryRecord | None:
        if telemetry_fails:
            return None
        return VoicePromptTelemetryRecord(
            telemetry_id=_id("VPT"), voice_prompt_id=voice_prompt_id,
            replay_count=0, completion_count=0, forward_count=0, reply_count=0,
            resonance_marker=False, recorded_at=_now(),
        )

class VoicePromptEngineService:
    def __init__(self, *, synthesis_adapter: ConsciousVoiceSynthesisAdapter | None = None,
                 fallback_packs: list[PreRecordedFallbackPack] | None = None,
                 receipt_chain: Any = None) -> None:
        self._resolver = VoicePromptDecisionResolver()
        self._composer = VoicePromptComposer()
        self._dna_bridge = VoiceDNAAlignmentBridge()
        self._bed_resolver = SonicBedResolver()
        self._synth = synthesis_adapter or ConsciousVoiceSynthesisAdapter()
        self._gate = SonicPrestigeGate()
        self._fallback = PreRecordedFallbackPackResolver(fallback_packs)
        self._dispatch = VoicePromptDispatchCoordinator()
        self._telemetry = VoicePromptTelemetryBridge()
        self._receipt = receipt_chain

    def issue(self, ctx: VoicePromptTriggerContext) -> dict:
        job = self._resolver.resolve(ctx)
        script = self._composer.compose(ctx=ctx, job=job)
        bed = self._bed_resolver.resolve(job)
        vdna_ref = self._dna_bridge.resolve_profile_ref(ctx.coach_id)
        prompt_id = _id("VPE")
        packet = VoicePromptPacket(
            voice_prompt_id=prompt_id, coach_id=ctx.coach_id, user_id=ctx.user_id,
            emotional_job=job, job_selection_reason=ctx.reason, surface=ctx.surface,
            locale=ctx.locale, script_text=script, sonic_bed_profile=bed,
            voice_dna_profile_ref=vdna_ref, duration_target_seconds=bed.duration_ceiling_seconds,
            created_at=_now(),
        )
        if self._receipt:
            self._receipt.log(action="voice-prompt-resolved", metadata={"id": prompt_id, "job": job.value})

        # Render
        if self._synth.is_available():
            attempt = self._synth.synthesize(script=script, voice_dna_ref=vdna_ref, duration_target=bed.duration_ceiling_seconds)
            attempt.voice_prompt_id = prompt_id
            attempt = self._gate.evaluate(attempt)
            if attempt.prestige_gate_passed:
                delivery = self._dispatch.dispatch(packet=packet, attempt=attempt)
                self._telemetry.record(voice_prompt_id=prompt_id)
                return {"packet": packet, "attempt": attempt, "delivery": delivery, "status": PromptStatus.DISPATCHED}
            else:
                # Gate failed — try human fallback
                fallback = self._fallback.find(coach_id=ctx.coach_id, job=job, locale=ctx.locale)
                if fallback:
                    fb_attempt = VoicePromptRenderAttempt(
                        render_attempt_id=_id("VPR"), voice_prompt_id=prompt_id,
                        render_source=RenderSource.PRE_RECORDED_HUMAN,
                        provider_reference=fallback.fallback_pack_id,
                        audio_asset_id=fallback.audio_asset_id, sample_rate_hz=48000,
                        duration_seconds=fallback.duration_seconds, prestige_gate_passed=True,
                        created_at=_now(),
                    )
                    delivery = self._dispatch.dispatch(packet=packet, attempt=fb_attempt)
                    return {"packet": packet, "attempt": fb_attempt, "delivery": delivery, "status": PromptStatus.FALLBACK_RENDERED}
                return {"packet": packet, "attempt": attempt, "status": PromptStatus.FAILED_PRESTIGE_GUARD}

        # ConsciousVoice unavailable
        fallback = self._fallback.find(coach_id=ctx.coach_id, job=job, locale=ctx.locale)
        if fallback:
            fb_attempt = VoicePromptRenderAttempt(
                render_attempt_id=_id("VPR"), voice_prompt_id=prompt_id,
                render_source=RenderSource.PRE_RECORDED_HUMAN,
                provider_reference=fallback.fallback_pack_id,
                audio_asset_id=fallback.audio_asset_id, sample_rate_hz=48000,
                duration_seconds=fallback.duration_seconds, prestige_gate_passed=True,
                created_at=_now(),
            )
            delivery = self._dispatch.dispatch(packet=packet, attempt=fb_attempt)
            return {"packet": packet, "attempt": fb_attempt, "delivery": delivery, "status": PromptStatus.FALLBACK_RENDERED}
        return {"packet": packet, "status": PromptStatus.RETRY_PENDING, "retry_after_seconds": 20, "queue_reason": "conscious_voice_provider_unavailable"}
