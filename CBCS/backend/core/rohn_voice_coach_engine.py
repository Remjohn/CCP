"""
FR61 — Jim Rohn AI Voice Coach Engine: Core Service
=====================================================
Implements Stages 1-7 of the Jim Rohn AI Voice Coach Engine.
Architecture reference: FR61_Jim_Rohn_Voice_Coach_Engine_Tech_Spec.md §4.
ADR-01: All queries scoped by coach_id. C-11: No agent names in API payloads.
"""

import hashlib
import json
import logging
import re
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Protocol, Tuple

from backend.core.fr61_models import (
    MICRO_IMPROVEMENT_THRESHOLD_PCT, MAX_FEEDBACK_DURATION_SECONDS,
    MAX_RATCHET_FOLLOWUPS, NARRATIVE_ARC_TEMPLATES, PROHIBITED_WORDS,
    PROVOCATION_MIN_ANTITHESES, PROVOCATION_MIN_HCD_REFS,
    REDIS_PROVOCATION_TTL_SECONDS, REDIS_REMINDER_TTL_SECONDS,
    REDIS_SESSION_TTL_SECONDS, ROHN_PAUSE_MAX_SECONDS,
    ROHN_PAUSE_MIN_SECONDS, SESSION_MAX_MINUTES, SESSION_WARN_MINUTES,
    SPECIFICITY_ENTITY_THRESHOLD, SPECIFICITY_SENSORY_THRESHOLD,
    VOICE_NOTE_MIN_SECONDS,
    ContradictionPair, EmotionalTrajectory, ExtractedStory,
    FeedbackElement, FeedbackGateVerdict, FeedbackOutput,
    FeedbackRegisterGateResult, FR5FeedbackSignal, FR61ReceiptBlock,
    GeneratedQuestion, HCDReference, IntakeProcessingResult,
    MicroImprovementDetection, PauseMarker, PinDataPoint,
    PostureObservation, ProsodyMetrics, ProvocationError,
    ProvocationGateResult, ProvocationGateVerdict, ProvocationQuestionOutput,
    RecordingAnalysis, RecordingSessionError, ScheduledSessionRecord,
    ScheduledSessionStatus, SchedulingError, ScriptArrangementGateResult,
    ScriptCompositionError, ScriptDocument, ScriptGateVerdict, ScriptPiece,
    SessionAnalysisOutput, SessionTimeGateResult, SessionType,
    SpecificityGateVerdict, SpecificityRatchetResult, TemporalPosition,
    TranscriptAnalysis, TriggerSource, VideoAnalysis,
    VideoAvailabilityVerdict, VocalAnalysis, EuphonyDevice, TPLMarker,
    FeedbackError, IntakeError, PersistenceError,
)

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# SERVICE PROTOCOLS (Dependency Injection)
# ═══════════════════════════════════════════════════════════════

class SupabaseClientProtocol(Protocol):
    """Protocol for Supabase database operations."""
    async def insert(self, table: str, data: dict) -> dict: ...
    async def select(self, table: str, filters: dict, order_by: str = "", limit: int = 100) -> List[dict]: ...
    async def update(self, table: str, filters: dict, data: dict) -> dict: ...
    async def set_coach_context(self, coach_id: str) -> None: ...


class RedisClientProtocol(Protocol):
    """Protocol for Redis session cache operations."""
    async def set_json(self, key: str, data: dict, ttl: int) -> None: ...
    async def get_json(self, key: str) -> Optional[dict]: ...
    async def delete(self, key: str) -> None: ...


class TTSServiceProtocol(Protocol):
    """Protocol for CosyVoice TTS service."""
    async def synthesize(self, text: str) -> str: ...


class AudioAnalysisProtocol(Protocol):
    """Protocol for audio analysis pipeline (OpenSMILE + librosa + Whisper + Wav2Vec)."""
    async def extract_prosody(self, audio_path: str) -> ProsodyMetrics: ...
    async def transcribe(self, audio_path: str) -> Tuple[str, List[dict]]: ...
    async def analyze_liwc(self, text: str) -> TranscriptAnalysis: ...
    async def extract_emotion(self, audio_path: str) -> List[dict]: ...


class VideoAnalysisProtocol(Protocol):
    """Protocol for video visual analysis pipeline."""
    async def detect_face_track(self, video_path: str) -> bool: ...
    async def analyze_eye_contact(self, video_path: str) -> Tuple[float, List[float]]: ...
    async def analyze_gestures(self, video_path: str, emphasis_timestamps: List[float]) -> float: ...
    async def analyze_facial_expression(self, video_path: str, audio_emotions: List[dict]) -> float: ...
    async def analyze_posture(self, video_path: str) -> List[PostureObservation]: ...


class CalendarServiceProtocol(Protocol):
    """Protocol for Google Calendar / CalDAV integration."""
    async def create_event(self, coach_id: str, title: str, start: datetime,
                           duration_min: int, description: str) -> str: ...


class TelegramDeliveryProtocol(Protocol):
    """Protocol for Telegram Bot API delivery."""
    async def send_voice_note(self, coach_id: str, audio_url: str) -> bool: ...
    async def send_text(self, coach_id: str, text: str) -> bool: ...


class LLMServiceProtocol(Protocol):
    """Protocol for LLM generation (provocation questions, feedback, scripts).
    C-11: No agent persona names may appear in any prompt sent to this service."""
    async def generate(self, system_prompt: str, user_prompt: str) -> str: ...


# ═══════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def _sha256(data: Any) -> str:
    """Compute SHA-256 hash of data serialized as canonical JSON."""
    if isinstance(data, str):
        payload = data
    else:
        payload = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _generate_receipt_id(coach_acronym: str, stage_label: str, date_str: str) -> str:
    """Generate receipt ID per FR61 §4 receipt format: RCP-{COACH}-{STAGE}-{DATE}."""
    return f"RCP-{coach_acronym}-{stage_label}-{date_str}"


def _build_receipt(
    receipt_id: str,
    previous_hash: str,
    input_data: Any,
    output_data: Any,
    stage_name: str,
    agent_name: str,
) -> FR61ReceiptBlock:
    """Build a FR47 DEP-ENG-041 receipt block."""
    return FR61ReceiptBlock(
        receipt_id=receipt_id,
        previous_receipt_hash=previous_hash,
        input_payload_hash=_sha256(input_data),
        output_payload_hash=_sha256(output_data),
        stage_name=stage_name,
        agent_name=agent_name,
    )


def _check_prohibited_words(text: str) -> List[str]:
    """Check text for prohibited AI assistant language.
    FR61 §4.Stage1 Step 4, §4.Stage6 Step 2."""
    found = []
    text_lower = text.lower()
    for word in PROHIBITED_WORDS:
        if word.lower() in text_lower:
            found.append(word)
    return found


def _count_antitheses(text: str) -> int:
    """Count antithetical constructions in text.
    Pattern: 'not X — Y', 'not X, but Y', 'not because X, but because Y'."""
    patterns = [
        r'\bnot\b[^.!?]{1,80}[—–-]\s',
        r'\bnot\b[^.!?]{1,80}\bbut\b',
        r'\bnot\s+because\b[^.!?]{1,80}\bbut\s+because\b',
    ]
    count = 0
    for pattern in patterns:
        count += len(re.findall(pattern, text, re.IGNORECASE))
    return max(count, 0)


def _has_closing_question(text: str) -> bool:
    """Check if text ends with a direct question demanding a position."""
    stripped = text.strip()
    if not stripped:
        return False
    sentences = re.split(r'[.!]', stripped)
    last_part = stripped.split('?')
    return len(last_part) >= 2 and len(last_part[-2].strip()) > 0


def _detect_alliteration(text: str) -> List[EuphonyDevice]:
    """Detect alliterative patterns (FR61 §4.Stage1 Step 4 — euphonic devices)."""
    devices = []
    words = text.lower().split()
    for i in range(len(words) - 2):
        w1, w2, w3 = words[i], words[i + 1], words[i + 2]
        if len(w1) > 2 and len(w2) > 2 and w1[0] == w2[0] == w3[0]:
            detected = f"{words[i]} {words[i+1]} {words[i+2]}"
            devices.append(EuphonyDevice(
                device_type="alliteration",
                detected_string=f"alliteration: '{detected}'",
            ))
    return devices


def _select_narrative_arc(emotional_trajectory: str) -> str:
    """Select the narrative arc from the 12-arc template based on emotional trajectory.
    FR61 §4.Stage3 Step 3a."""
    trajectory_map = {
        "frustration_to_resolution": "The Epiphany",
        "warning_future_risk": "The Warning",
        "obstacle_to_confrontation": "The Challenge",
        "hidden_truth_uncovered": "The Revelation",
        "self_reflection_to_awareness": "The Mirror",
        "gap_to_connection": "The Bridge",
        "accountability_consequences": "The Reckoning",
        "principles_to_practice": "The Foundation",
        "opposing_ideas_synthesis": "The Contrast",
        "progression_milestones": "The Journey",
        "conviction_declaration": "The Stand",
        "past_lessons_future_impact": "The Legacy",
    }
    return trajectory_map.get(emotional_trajectory, "The Foundation")


def _compute_sincerity_composite(liwc_auth: float, jitter: float, shimmer: float) -> float:
    """Compute sincerity composite metric.
    FR61 §4.Stage5 Step 3b — sincerity composite = f(LIWC_authenticity, jitter_stability, shimmer_stability).
    Higher LIWC authenticity + lower jitter/shimmer variance = higher sincerity."""
    jitter_stability = max(0.0, 1.0 - abs(jitter) * 10)
    shimmer_stability = max(0.0, 1.0 - abs(shimmer) * 5)
    return round((liwc_auth * 0.5 + jitter_stability * 0.25 + shimmer_stability * 0.25) * 10, 1)


def _compute_wpm(word_count: int, duration_seconds: float) -> float:
    """Compute words per minute. FR61 §4.Stage5 Step 3b."""
    if duration_seconds <= 0:
        return 0.0
    return round(word_count / (duration_seconds / 60.0), 1)


def _compute_filler_density(filler_count: int, total_words: int) -> float:
    """Compute filler density. FR61 §4.Stage5 Step 3b."""
    if total_words <= 0:
        return 0.0
    return round(filler_count / total_words, 4)


def _count_rohn_pauses(iss_events: List[dict]) -> int:
    """Count Rohn Pauses: ISS events between 1.5-2.5s following key statements.
    FR61 §4.Stage5 Step 3b."""
    count = 0
    for event in iss_events:
        duration = event.get("duration", 0.0)
        if ROHN_PAUSE_MIN_SECONDS <= duration <= ROHN_PAUSE_MAX_SECONDS:
            if event.get("follows_key_statement", False):
                count += 1
    return count


def _compute_pin_iron_ratio(entity_count: int, citation_count: int,
                            emotional_loading: float) -> float:
    """Compute Pin-Iron-Bar ratio. FR61 §4.Stage5 Step 3b."""
    if emotional_loading <= 0:
        return 0.0
    return round((entity_count + citation_count) / emotional_loading, 2)


def _compute_micro_improvements(
    current_metrics: Dict[str, float],
    previous_metrics: Dict[str, float],
) -> List[MicroImprovementDetection]:
    """Detect micro-improvements with ≥5% delta between sessions.
    FR61 §4.Stage6 Step 1."""
    improvements = []
    for metric_name, current_val in current_metrics.items():
        prev_val = previous_metrics.get(metric_name)
        if prev_val is None or prev_val == 0:
            continue
        delta_pct = round((current_val - prev_val) / abs(prev_val) * 100, 1)
        improved = False
        if metric_name in ("filler_density",):
            improved = delta_pct <= -MICRO_IMPROVEMENT_THRESHOLD_PCT
        else:
            improved = delta_pct >= MICRO_IMPROVEMENT_THRESHOLD_PCT
        if improved:
            improvements.append(MicroImprovementDetection(
                metric_name=metric_name,
                previous_value=prev_val,
                current_value=current_val,
                delta_pct=delta_pct,
            ))
    improvements.sort(key=lambda x: abs(x.delta_pct), reverse=True)
    return improvements


# ═══════════════════════════════════════════════════════════════
# QUALITY GATES
# ═══════════════════════════════════════════════════════════════

class ProvocationQualityGate:
    """Gate S1: Validates Rohn-style provocation question quality.
    FR61 §4.Stage1 Step 4 — MUST constraints."""

    @staticmethod
    def evaluate(question_text: str, hcd_refs: List[HCDReference]) -> ProvocationGateResult:
        prohibited = _check_prohibited_words(question_text)
        if prohibited:
            return ProvocationGateResult(
                verdict=ProvocationGateVerdict.FAIL_PROHIBITED_WORD,
                hcd_ref_count=len(hcd_refs),
                antithesis_count=_count_antitheses(question_text),
                has_closing_question=_has_closing_question(question_text),
                prohibited_words_found=prohibited,
            )
        hcd_count = len(hcd_refs)
        if hcd_count < PROVOCATION_MIN_HCD_REFS:
            return ProvocationGateResult(
                verdict=ProvocationGateVerdict.FAIL_NO_HCD_REF,
                hcd_ref_count=hcd_count,
                antithesis_count=_count_antitheses(question_text),
                has_closing_question=_has_closing_question(question_text),
            )
        antithesis_count = _count_antitheses(question_text)
        if antithesis_count < PROVOCATION_MIN_ANTITHESES:
            return ProvocationGateResult(
                verdict=ProvocationGateVerdict.FAIL_NO_ANTITHESIS,
                hcd_ref_count=hcd_count,
                antithesis_count=antithesis_count,
                has_closing_question=_has_closing_question(question_text),
            )
        has_question = _has_closing_question(question_text)
        if not has_question:
            return ProvocationGateResult(
                verdict=ProvocationGateVerdict.FAIL_NO_CLOSING_QUESTION,
                hcd_ref_count=hcd_count,
                antithesis_count=antithesis_count,
                has_closing_question=False,
            )
        return ProvocationGateResult(
            verdict=ProvocationGateVerdict.PASS,
            hcd_ref_count=hcd_count,
            antithesis_count=antithesis_count,
            has_closing_question=True,
        )


class SpecificityRatchetGate:
    """Gate S2: Validates response specificity.
    FR61 §4.Stage2 Step 4."""

    @staticmethod
    def evaluate(sensory_score: float, entity_count: int,
                 ratchet_count: int, vaguest_claim: str = "") -> SpecificityRatchetResult:
        if ratchet_count >= MAX_RATCHET_FOLLOWUPS:
            return SpecificityRatchetResult(
                needs_followup=False,
                sensory_score=sensory_score,
                entity_count=entity_count,
                ratchet_count=ratchet_count,
                verdict=SpecificityGateVerdict.PASS_MAX_RATCHETS_REACHED,
            )
        if sensory_score < SPECIFICITY_SENSORY_THRESHOLD and entity_count < SPECIFICITY_ENTITY_THRESHOLD:
            return SpecificityRatchetResult(
                needs_followup=True,
                sensory_score=sensory_score,
                entity_count=entity_count,
                ratchet_count=ratchet_count,
                verdict=SpecificityGateVerdict.FAIL_NEEDS_FOLLOWUP,
                followup_target_claim=vaguest_claim,
            )
        return SpecificityRatchetResult(
            needs_followup=False,
            sensory_score=sensory_score,
            entity_count=entity_count,
            ratchet_count=ratchet_count,
            verdict=SpecificityGateVerdict.PASS,
        )


class ScriptArrangementGate:
    """Gate S3: Validates script arrangement (not rewrite).
    FR61 §4.Stage3 Failure Condition."""

    @staticmethod
    def evaluate(
        script: ScriptDocument,
        original_phrases: List[str],
        max_pages: int = 3,
    ) -> ScriptArrangementGateResult:
        rewrite_violations = []
        for piece in script.content_pieces:
            for phrase in piece.arranged_phrases:
                found_match = False
                for orig in original_phrases:
                    if orig.strip().lower() in phrase.strip().lower() or phrase.strip().lower() in orig.strip().lower():
                        found_match = True
                        break
                if not found_match and len(phrase.split()) > 5:
                    rewrite_violations.append(phrase[:80])

        total_pause_markers = sum(len(p.pause_markers) for p in script.content_pieces)
        total_pages = len(script.content_pieces)

        if rewrite_violations:
            return ScriptArrangementGateResult(
                verdict=ScriptGateVerdict.FAIL_REWRITE_DETECTED,
                rewrite_violations=rewrite_violations[:5],
                total_pages=total_pages,
                total_pause_markers=total_pause_markers,
            )
        if total_pages > max_pages:
            return ScriptArrangementGateResult(
                verdict=ScriptGateVerdict.FAIL_TOO_LONG,
                total_pages=total_pages,
                total_pause_markers=total_pause_markers,
            )
        if total_pause_markers < 1:
            return ScriptArrangementGateResult(
                verdict=ScriptGateVerdict.FAIL_NO_PAUSE_MARKERS,
                total_pages=total_pages,
                total_pause_markers=0,
            )
        return ScriptArrangementGateResult(
            verdict=ScriptGateVerdict.PASS,
            total_pages=total_pages,
            total_pause_markers=total_pause_markers,
        )


class SessionTimeGate:
    """Gate S5A: Enforces session time limits.
    FR61 §4.Stage5 Step 5 — 55-min warn, 60-min hard stop."""

    @staticmethod
    def evaluate(elapsed_minutes: int, recordings_remaining: int) -> SessionTimeGateResult:
        return SessionTimeGateResult(
            elapsed_minutes=elapsed_minutes,
            warn_triggered=elapsed_minutes >= SESSION_WARN_MINUTES,
            hard_stop_triggered=elapsed_minutes >= SESSION_MAX_MINUTES,
            recordings_remaining=recordings_remaining,
        )


class FeedbackRegisterGate:
    """Gate S6: Validates feedback against Rohn delivery register.
    FR61 §4.Stage6 Step 2 — Delivery Register constraints."""

    @staticmethod
    def evaluate(feedback_text: str, estimated_seconds: int) -> FeedbackRegisterGateResult:
        prohibited = _check_prohibited_words(feedback_text)
        if prohibited:
            return FeedbackRegisterGateResult(
                verdict=FeedbackGateVerdict.FAIL_PROHIBITED_WORD,
                prohibited_words_found=prohibited,
            )
        antithesis = _count_antitheses(feedback_text) > 0
        if not antithesis:
            return FeedbackRegisterGateResult(
                verdict=FeedbackGateVerdict.FAIL_NO_ANTITHESIS,
                antithesis_found=False,
            )
        hcd_keywords = ["last session", "previous", "weeks ago", "since", "your", "you said", "you mentioned"]
        hcd_found = any(kw in feedback_text.lower() for kw in hcd_keywords)
        if not hcd_found:
            return FeedbackRegisterGateResult(
                verdict=FeedbackGateVerdict.FAIL_NO_HCD_REF,
                antithesis_found=True,
                hcd_ref_found=False,
            )
        rohn_indicators = ["Jim Rohn", "Rohn", "discipline", "master", "philosophy", "principle"]
        principle_found = any(ind in feedback_text for ind in rohn_indicators)
        if not principle_found:
            return FeedbackRegisterGateResult(
                verdict=FeedbackGateVerdict.FAIL_NO_PRINCIPLE,
                antithesis_found=True,
                hcd_ref_found=True,
                rohn_principle_found=False,
            )
        lets_found = "let's" in feedback_text.lower() or "let us" in feedback_text.lower()
        if not lets_found:
            return FeedbackRegisterGateResult(
                verdict=FeedbackGateVerdict.FAIL_NO_LETS_FRAMING,
                antithesis_found=True,
                hcd_ref_found=True,
                rohn_principle_found=True,
                lets_framing_found=False,
            )
        if estimated_seconds > MAX_FEEDBACK_DURATION_SECONDS:
            return FeedbackRegisterGateResult(
                verdict=FeedbackGateVerdict.FAIL_TOO_LONG,
                antithesis_found=True, hcd_ref_found=True,
                rohn_principle_found=True, lets_framing_found=True,
                estimated_duration_seconds=estimated_seconds,
            )
        return FeedbackRegisterGateResult(
            verdict=FeedbackGateVerdict.PASS,
            antithesis_found=True, hcd_ref_found=True,
            rohn_principle_found=True, lets_framing_found=True,
            estimated_duration_seconds=estimated_seconds,
        )


class VideoAnalysisGate:
    """Gate S5B: Checks if video has detectable face track.
    FR61 §8 AC8."""

    @staticmethod
    def evaluate(face_detected: bool) -> VideoAvailabilityVerdict:
        if face_detected:
            return VideoAvailabilityVerdict.AVAILABLE
        return VideoAvailabilityVerdict.NO_FACE_TRACK
