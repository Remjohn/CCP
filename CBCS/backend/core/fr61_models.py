"""
FR61 — Jim Rohn AI Voice Coach Engine: Data Models
====================================================

Pydantic schemas, enums, error types, and constants for the
7-stage coaching engine defined in FR61_Jim_Rohn_Voice_Coach_Engine_Tech_Spec.md.

Architecture reference: FR61 §4 (Stages 1-7), §5 (Output Schemas), §7 (Tasks).
ADR-01 Coach Isolation: All coach_id fields are mandatory and non-optional.
C-11 Persona Masking: Agent names are orchestration-layer labels only.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime
import uuid


# ═══════════════════════════════════════════════════════════════
# CONSTANTS (FR61 §4, §8)
# ═══════════════════════════════════════════════════════════════

# Gate S1: Provocation Quality (FR61 §4.Stage1, Step 4)
PROVOCATION_MIN_HCD_REFS: int = 1
PROVOCATION_MIN_ANTITHESES: int = 1

# Gate S2: Specificity Ratchet (FR61 §4.Stage2, Step 4)
SPECIFICITY_SENSORY_THRESHOLD: float = 4.0
SPECIFICITY_ENTITY_THRESHOLD: int = 3
MAX_RATCHET_FOLLOWUPS: int = 2

# Gate S5: Session Time (FR61 §4.Stage5, Step 5)
SESSION_WARN_MINUTES: int = 55
SESSION_MAX_MINUTES: int = 60

# Gate S6: Micro-improvement (FR61 §4.Stage6, Step 1)
MICRO_IMPROVEMENT_THRESHOLD_PCT: float = 5.0
MAX_FEEDBACK_DURATION_SECONDS: int = 60

# Rohn Pause detection (FR61 §4.Stage5, Step 3b)
ROHN_PAUSE_MIN_SECONDS: float = 1.5
ROHN_PAUSE_MAX_SECONDS: float = 2.5

# Voice note minimum duration (FR61 §4.Stage2)
VOICE_NOTE_MIN_SECONDS: int = 15

# Redis TTLs (FR61 §4.Stage7)
REDIS_SESSION_TTL_SECONDS: int = 5400       # 90 min
REDIS_PROVOCATION_TTL_SECONDS: int = 43200  # 12 h
REDIS_REMINDER_TTL_SECONDS: int = 259200    # 72 h

# Prohibited AI assistant language (FR61 §4.Stage1 Step 4, §4.Stage6 Step 2)
PROHIBITED_WORDS: List[str] = [
    "I can help with that",
    "as an AI",
    "delve",
    "unlock",
    "game-changing",
]

# 12 Narrative Arcs template (FR61 §4.Stage3, Step 3a)
# Derived from Jim_Rohn_AI_Voice_Coach_Communication_Framework.md v3.0
# Spec names 2 explicitly: "The Epiphany" and "The Warning"
NARRATIVE_ARC_TEMPLATES: dict = {
    "The Epiphany": {
        "trigger_trajectory": "frustration_to_resolution",
        "description": "Coach moves from frustration to sudden clarity",
        "structure": ["setup_frustration", "turning_point", "resolution_insight"],
    },
    "The Warning": {
        "trigger_trajectory": "warning_future_risk",
        "description": "Coach identifies a danger and projects consequences",
        "structure": ["current_state", "risk_identification", "consequence_projection"],
    },
    "The Challenge": {
        "trigger_trajectory": "obstacle_to_confrontation",
        "description": "Coach confronts an obstacle head-on",
        "structure": ["obstacle_description", "confrontation_moment", "outcome_declaration"],
    },
    "The Revelation": {
        "trigger_trajectory": "hidden_truth_uncovered",
        "description": "Something previously unseen becomes visible",
        "structure": ["surface_appearance", "deeper_investigation", "truth_exposed"],
    },
    "The Mirror": {
        "trigger_trajectory": "self_reflection_to_awareness",
        "description": "Coach recognizes something about themselves",
        "structure": ["external_observation", "internal_parallel", "self_awareness_moment"],
    },
    "The Bridge": {
        "trigger_trajectory": "gap_to_connection",
        "description": "Coach connects two seemingly unrelated ideas",
        "structure": ["idea_a", "idea_b", "connection_synthesis"],
    },
    "The Reckoning": {
        "trigger_trajectory": "accountability_consequences",
        "description": "Coach faces accountability for a choice",
        "structure": ["choice_made", "consequences_revealed", "lesson_crystallized"],
    },
    "The Foundation": {
        "trigger_trajectory": "principles_to_practice",
        "description": "Core principle applied to daily reality",
        "structure": ["principle_statement", "real_world_application", "proof_of_practice"],
    },
    "The Contrast": {
        "trigger_trajectory": "opposing_ideas_synthesis",
        "description": "Two opposing viewpoints synthesized into one truth",
        "structure": ["position_a", "position_b", "synthesis_resolution"],
    },
    "The Journey": {
        "trigger_trajectory": "progression_milestones",
        "description": "Coach traces a progression through milestones",
        "structure": ["starting_point", "milestones_traversed", "current_position"],
    },
    "The Stand": {
        "trigger_trajectory": "conviction_declaration",
        "description": "Coach takes a firm position on a contested topic",
        "structure": ["contested_topic", "position_taken", "declaration_with_evidence"],
    },
    "The Legacy": {
        "trigger_trajectory": "past_lessons_future_impact",
        "description": "Past experience informs future direction",
        "structure": ["past_event", "lesson_extracted", "future_application"],
    },
}


# ═══════════════════════════════════════════════════════════════
# ENUMS (FR61 §4)
# ═══════════════════════════════════════════════════════════════

class SessionType(str, Enum):
    """FR61 §4.Stage7 — sessions table session_type CHECK."""
    TRIGGER = "trigger"
    RECORDING = "recording"


class EmotionalTrajectory(str, Enum):
    """FR61 §4.Stage7 — sessions table emotional_trajectory CHECK."""
    ASCENDING = "ascending"
    STABLE = "stable"
    DESCENDING = "descending"


class TemporalPosition(str, Enum):
    """FR61 §4.Stage7 — story_bank table temporal_position CHECK."""
    PAST = "past"
    PRESENT = "present"
    FUTURE = "future"


class ScheduledSessionStatus(str, Enum):
    """FR61 §4.Stage7 — scheduled_sessions table status CHECK."""
    BOOKED = "booked"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    MISSED = "missed"
    RESCHEDULED = "rescheduled"


class ReminderStage(str, Enum):
    """FR61 §4.Stage4 — 3-stage reminder pipeline."""
    T_48H = "T-48h"
    T_24H = "T-24h"
    T_30MIN = "T-30min"


class ProvocationGateVerdict(str, Enum):
    """Gate S1 — Provocation quality verdict."""
    PASS = "PASS"
    FAIL_NO_HCD_REF = "FAIL_NO_HCD_REF"
    FAIL_NO_ANTITHESIS = "FAIL_NO_ANTITHESIS"
    FAIL_NO_CLOSING_QUESTION = "FAIL_NO_CLOSING_QUESTION"
    FAIL_PROHIBITED_WORD = "FAIL_PROHIBITED_WORD"


class SpecificityGateVerdict(str, Enum):
    """Gate S2 — Specificity ratchet verdict."""
    PASS = "PASS"
    FAIL_NEEDS_FOLLOWUP = "FAIL_NEEDS_FOLLOWUP"
    PASS_MAX_RATCHETS_REACHED = "PASS_MAX_RATCHETS_REACHED"


class ScriptGateVerdict(str, Enum):
    """Gate S3 — Script arrangement verdict."""
    PASS = "PASS"
    FAIL_REWRITE_DETECTED = "FAIL_REWRITE_DETECTED"
    FAIL_TOO_LONG = "FAIL_TOO_LONG"
    FAIL_NO_PAUSE_MARKERS = "FAIL_NO_PAUSE_MARKERS"


class FeedbackGateVerdict(str, Enum):
    """Gate S6 — Feedback register verdict."""
    PASS = "PASS"
    FAIL_NO_ANTITHESIS = "FAIL_NO_ANTITHESIS"
    FAIL_NO_HCD_REF = "FAIL_NO_HCD_REF"
    FAIL_NO_PRINCIPLE = "FAIL_NO_PRINCIPLE"
    FAIL_NO_LETS_FRAMING = "FAIL_NO_LETS_FRAMING"
    FAIL_PROHIBITED_WORD = "FAIL_PROHIBITED_WORD"
    FAIL_TOO_LONG = "FAIL_TOO_LONG"


class VideoAvailabilityVerdict(str, Enum):
    """Gate S5B — Video analysis availability."""
    AVAILABLE = "AVAILABLE"
    NO_FACE_TRACK = "NO_FACE_TRACK"


# ═══════════════════════════════════════════════════════════════
# ERROR TYPES (FR61 §4 failure conditions)
# ═══════════════════════════════════════════════════════════════

class FR61Error(Exception):
    """Base error for FR61 Jim Rohn Voice Coach Engine."""
    pass


class ProvocationError(FR61Error):
    """Stage 1 provocation generation failure."""
    pass


class IntakeError(FR61Error):
    """Stage 2 intake processing failure."""
    pass


class ScriptCompositionError(FR61Error):
    """Stage 3 script composition failure."""
    pass


class SchedulingError(FR61Error):
    """Stage 4 scheduling failure."""
    pass


class RecordingSessionError(FR61Error):
    """Stage 5 recording session failure."""
    pass


class FeedbackError(FR61Error):
    """Stage 6 feedback generation failure."""
    pass


class PersistenceError(FR61Error):
    """Stage 7 persistence failure."""
    pass


# ═══════════════════════════════════════════════════════════════
# DATA MODELS — Stage 1: Provocation (FR61 §4.Stage1, §5)
# ═══════════════════════════════════════════════════════════════

class HCDReference(BaseModel):
    """A reference to the coach's Historical Coaching Data.
    FR61 §5 Provocation Question Output — hcd_references array."""
    type: str = Field(..., description="previous_statement | stored_story | unresolved_tension")
    source_session: str = Field(..., description="Session ID where this data originated")
    quote: str = Field(..., description="Exact quote from the coach's HCD")


class EuphonyDevice(BaseModel):
    """Euphonic device detected in provocation question.
    FR61 §4.Stage1 Step 4 — euphony_devices schema array."""
    device_type: str = Field(..., description="alliteration | phonetic_homogeneity | rhyme")
    detected_string: str = Field(..., description="The specific string exhibiting the device")


class TPLMarker(BaseModel):
    """Textual Paralanguage marker in text delivery.
    FR61 §4.Stage1 Step 4 — tpl_markers schema array."""
    marker_type: str = Field(..., description="pause | emphasis | ellipsis")
    marker_text: str = Field(..., description="The TPL marker text (e.g., '*pauses*')")


class TriggerSource(BaseModel):
    """Source data for the provocation trigger.
    FR61 §5 Provocation Question Output — trigger_source."""
    fr15_tension_id: str
    fr5_trigger_id: str
    topic_cluster: str


class GeneratedQuestion(BaseModel):
    """The generated provocation question with quality metadata.
    FR61 §5 Provocation Question Output — generated_question."""
    text: str
    antithesis_count: int = Field(0, ge=0)
    euphony_devices: List[EuphonyDevice] = Field(default_factory=list)
    tpl_markers: List[TPLMarker] = Field(default_factory=list)


class ProvocationQuestionOutput(BaseModel):
    """Complete Stage 1 output schema.
    FR61 §5 Provocation Question Output."""
    provocation_id: str
    coach_tenant_id: str
    trigger_source: TriggerSource
    hcd_references: List[HCDReference] = Field(default_factory=list)
    generated_question: GeneratedQuestion
    voice_note_url: str = ""
    delivered_at: Optional[datetime] = None


# ═══════════════════════════════════════════════════════════════
# DATA MODELS — Stage 2: Intake (FR61 §4.Stage2)
# ═══════════════════════════════════════════════════════════════

class ProsodyMetrics(BaseModel):
    """Raw prosody extraction from OpenSMILE + librosa + Wav2Vec.
    FR61 §4.Stage5 Step 3b — Computed metrics."""
    f0_mean: float = 0.0
    f0_variance: float = 0.0
    jitter: float = 0.0
    shimmer: float = 0.0
    alpha_ratio: float = 0.0
    hnr: float = 0.0
    tempo: float = 0.0
    spm: float = 0.0
    onset_count: int = 0
    arousal: float = 0.0
    valence: float = 0.0


class TranscriptAnalysis(BaseModel):
    """Transcript-level analysis from LIWC-22 + custom extraction.
    FR61 §4.Stage2 Step 3."""
    liwc_authenticity: float = 0.0
    hedging_density: float = 0.0
    pronoun_i_ratio: float = 0.0
    pronoun_we_ratio: float = 0.0
    verb_past_ratio: float = 0.0
    verb_present_ratio: float = 0.0
    verb_future_ratio: float = 0.0
    sensory_detail_score: float = Field(0.0, ge=0.0, le=10.0)
    named_entity_count: int = 0


class ExtractedStory(BaseModel):
    """A narrative passage extracted from the coach's voice note.
    FR61 §4.Stage2 Step 3b."""
    raw_transcript: str
    topic_tags: List[str] = Field(default_factory=list)
    trigger_category_id: str = ""
    emotion_arousal: float = 0.0
    emotion_valence: float = 0.0
    narrative_arc: str = ""
    temporal_position: TemporalPosition = TemporalPosition.PRESENT
    sensory_detail_score: float = Field(0.0, ge=0.0, le=10.0)
    simile_metaphor_density: float = 0.0
    named_entities: List[str] = Field(default_factory=list)


class ContradictionPair(BaseModel):
    """A detected contradiction between two claims.
    FR61 §4.Stage2 Step 3c."""
    claim_a_text: str
    claim_a_session_date: datetime
    claim_b_text: str
    claim_b_session_date: datetime


class SpecificityRatchetResult(BaseModel):
    """Gate S2 output — whether a follow-up is needed.
    FR61 §4.Stage2 Step 4."""
    needs_followup: bool = False
    sensory_score: float = 0.0
    entity_count: int = 0
    ratchet_count: int = 0
    verdict: SpecificityGateVerdict = SpecificityGateVerdict.PASS
    followup_target_claim: str = ""


class IntakeProcessingResult(BaseModel):
    """Complete Stage 2 output."""
    session_id: str
    coach_id: str
    stories_extracted: List[ExtractedStory] = Field(default_factory=list)
    contradictions_detected: List[ContradictionPair] = Field(default_factory=list)
    prosody: ProsodyMetrics = Field(default_factory=ProsodyMetrics)
    transcript_analysis: TranscriptAnalysis = Field(default_factory=TranscriptAnalysis)
    specificity_result: SpecificityRatchetResult = Field(default_factory=SpecificityRatchetResult)
    full_transcript: str = ""
    word_count: int = 0
    duration_seconds: float = 0.0


# ═══════════════════════════════════════════════════════════════
# DATA MODELS — Stage 3: Script (FR61 §4.Stage3)
# ═══════════════════════════════════════════════════════════════

class PinDataPoint(BaseModel):
    """A CRAL evidence data point inserted into the script.
    FR61 §4.Stage3 Step 3c."""
    citation: str = Field(..., description="e.g., 'ICF 2024 study — 62% of coaches set fees below market rate'")
    position_seconds: int = Field(0, description="Position in the script timeline (in seconds)")


class PauseMarker(BaseModel):
    """A pause marker inserted into the script.
    FR61 §4.Stage3 Step 3d."""
    duration_seconds: float = Field(2.0, description="Pause duration calibrated to coach's avg_iss")
    position_after: str = Field("", description="The claim/phrase after which the pause is placed")
    triggered_by_sentiment_peak: bool = True


class ScriptPiece(BaseModel):
    """A single content piece within the script document.
    FR61 §4.Stage3 Step 4."""
    title: str
    narrative_arc: str
    estimated_duration_seconds: int = Field(0, ge=0)
    script_type: str = "ARRANGEMENT"
    arranged_phrases: List[str] = Field(default_factory=list)
    pin_data_points: List[PinDataPoint] = Field(default_factory=list)
    pause_markers: List[PauseMarker] = Field(default_factory=list)
    voice_dna_flagged_lines: List[str] = Field(default_factory=list)


class ScriptDocument(BaseModel):
    """Complete Stage 3 output — the full script document.
    FR61 §4.Stage3 Step 4."""
    script_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    coach_id: str
    content_pieces: List[ScriptPiece] = Field(default_factory=list)
    raw_coach_phrases_used: List[str] = Field(default_factory=list)
    voice_dna_compatibility_score: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ScriptArrangementGateResult(BaseModel):
    """Gate S3 output.
    FR61 §4.Stage3 Failure Condition."""
    verdict: ScriptGateVerdict = ScriptGateVerdict.PASS
    rewrite_violations: List[str] = Field(default_factory=list)
    total_pages: int = 0
    total_pause_markers: int = 0


# ═══════════════════════════════════════════════════════════════
# DATA MODELS — Stage 4: Scheduling (FR61 §4.Stage4)
# ═══════════════════════════════════════════════════════════════

class ReminderEvent(BaseModel):
    """A single reminder in the 3-stage pipeline.
    FR61 §4.Stage4 Step 4."""
    stage: ReminderStage
    scheduled_at: datetime
    content_type: str = Field(..., description="voice_note | script_delivery | voice_note_overview")
    content_text: str
    delivered: bool = False
    delivered_at: Optional[datetime] = None


class ScheduledSessionRecord(BaseModel):
    """Complete Stage 4 output.
    FR61 §4.Stage4."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    coach_id: str
    scheduled_datetime: datetime
    duration_minutes: int = 60
    batch_theme: str = ""
    recordings_planned: int = 0
    reminders: List[ReminderEvent] = Field(default_factory=list)
    status: ScheduledSessionStatus = ScheduledSessionStatus.BOOKED


# ═══════════════════════════════════════════════════════════════
# DATA MODELS — Stage 5: Recording Analysis (FR61 §4.Stage5, §5)
# ═══════════════════════════════════════════════════════════════

class VocalAnalysis(BaseModel):
    """Per-recording vocal analysis metrics.
    FR61 §5 Recording Session Analysis Output — vocal_analysis."""
    wpm: float = 0.0
    spm: float = 0.0
    pitch_variance_f0: float = 0.0
    rohn_pauses: int = 0
    filler_density: float = 0.0
    sincerity_composite: float = 0.0
    emotional_loading: dict = Field(default_factory=lambda: {"arousal": 0.0, "valence": 0.0})
    pin_iron_ratio: float = 0.0
    liwc_authenticity: float = 0.0
    jitter: float = 0.0
    shimmer: float = 0.0
    avg_iss: float = 0.0


class PostureObservation(BaseModel):
    """A timestamped posture observation.
    FR61 §4.Stage5 Step 3c — posture tracking."""
    timestamp: int = Field(0, description="Seconds into the recording")
    observation: str = Field("", description="forward_lean | backward_lean | neutral")
    content_match: str = Field("", description="What content segment this maps to")


class VideoAnalysis(BaseModel):
    """Per-recording video visual analysis metrics.
    FR61 §5 Recording Session Analysis Output — video_analysis."""
    eye_contact_pct: float = 0.0
    gaze_break_timestamps: List[float] = Field(default_factory=list)
    gesture_congruence: float = Field(0.0, ge=0.0, le=10.0)
    facial_expression_congruence: float = Field(0.0, ge=0.0, le=10.0)
    posture_notes: List[PostureObservation] = Field(default_factory=list)
    video_analysis_available: bool = True


class MicroImprovementDetection(BaseModel):
    """A detected micro-improvement between sessions.
    FR61 §4.Stage6 Step 1."""
    metric_name: str
    previous_value: float
    current_value: float
    delta_pct: float
    acknowledged: bool = False


class RecordingAnalysis(BaseModel):
    """Per-recording combined analysis.
    FR61 §5 Recording Session Analysis Output — recordings array."""
    recording_id: str
    script_piece_title: str = ""
    narrative_arc: str = ""
    duration_seconds: int = 0
    vocal_analysis: VocalAnalysis = Field(default_factory=VocalAnalysis)
    video_analysis: VideoAnalysis = Field(default_factory=VideoAnalysis)
    micro_improvements_detected: List[MicroImprovementDetection] = Field(default_factory=list)


class SessionAnalysisOutput(BaseModel):
    """Complete Stage 5 output.
    FR61 §5 Recording Session Analysis Output."""
    session_id: str
    coach_tenant_id: str
    session_type: SessionType = SessionType.RECORDING
    duration_minutes: int = 0
    recordings: List[RecordingAnalysis] = Field(default_factory=list)
    session_emotional_trajectory: EmotionalTrajectory = EmotionalTrajectory.STABLE
    session_depth_rating: int = Field(3, ge=1, le=5)


class SessionTimeGateResult(BaseModel):
    """Gate S5A output."""
    elapsed_minutes: int = 0
    warn_triggered: bool = False
    hard_stop_triggered: bool = False
    recordings_remaining: int = 0


# ═══════════════════════════════════════════════════════════════
# DATA MODELS — Stage 6: Feedback (FR61 §4.Stage6)
# ═══════════════════════════════════════════════════════════════

class FeedbackElement(BaseModel):
    """One of the 4 required feedback elements.
    FR61 §4.Stage6 Step 2 — 4-element structure."""
    element_type: str = Field(..., description="micro_improvement | strongest_moment | growth_area | forward_reference")
    content: str
    timestamp_reference: Optional[float] = None
    metric_reference: Optional[str] = None
    rohn_principle: str = ""


class FeedbackOutput(BaseModel):
    """Complete Stage 6 output for one recording take.
    FR61 §4.Stage6."""
    feedback_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    recording_id: str
    coach_id: str
    elements: List[FeedbackElement] = Field(default_factory=list)
    full_text: str = ""
    voice_note_url: str = ""
    estimated_duration_seconds: int = 0
    contains_antithesis: bool = False
    contains_hcd_reference: bool = False
    contains_rohn_principle: bool = False
    uses_lets_framing: bool = False
    prohibited_words_found: List[str] = Field(default_factory=list)


class FeedbackRegisterGateResult(BaseModel):
    """Gate S6 output.
    FR61 §4.Stage6 Step 2 — Delivery Register constraints."""
    verdict: FeedbackGateVerdict = FeedbackGateVerdict.PASS
    antithesis_found: bool = False
    hcd_ref_found: bool = False
    rohn_principle_found: bool = False
    lets_framing_found: bool = False
    prohibited_words_found: List[str] = Field(default_factory=list)
    estimated_duration_seconds: int = 0


# ═══════════════════════════════════════════════════════════════
# DATA MODELS — Receipt Chain (FR61 §4 all stages, FR47 DEP-ENG-041)
# ═══════════════════════════════════════════════════════════════

class FR61ReceiptBlock(BaseModel):
    """Receipt conforming to FR47 DEP-ENG-041 schema.
    FR61 §4 Stages 1-6 — Receipt Write sections."""
    receipt_id: str
    previous_receipt_hash: str
    input_payload_hash: str
    output_payload_hash: str
    stage_name: str
    agent_name: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


# ═══════════════════════════════════════════════════════════════
# DATA MODELS — FR5 Feedback Signal (FR61 §4.Stage7)
# ═══════════════════════════════════════════════════════════════

class FR5FeedbackSignal(BaseModel):
    """Webhook payload to FR5 Weekly Pipeline Stage 5.
    FR61 §4.Stage7 — FR5 Feedback Signal."""
    trigger_id: str
    liwc_authenticity_score: float
    sincerity_composite: float
    coach_id: str
    session_id: str


# ═══════════════════════════════════════════════════════════════
# DATA MODELS — Provocation Gate (FR61 §4.Stage1 Step 4)
# ═══════════════════════════════════════════════════════════════

class ProvocationGateResult(BaseModel):
    """Gate S1 output."""
    verdict: ProvocationGateVerdict = ProvocationGateVerdict.PASS
    hcd_ref_count: int = 0
    antithesis_count: int = 0
    has_closing_question: bool = False
    prohibited_words_found: List[str] = Field(default_factory=list)
