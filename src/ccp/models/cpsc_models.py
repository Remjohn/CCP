"""
CPSC Conversion Models
======================
Pydantic models, enums, and constants for Phase 3 CPSC Conversion specs (FR51-FR60).
Models are appended in dependency order as each spec is built.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


# ══════════════════════════════════════════════════════════════════════
# FR55 — Session Booking Intelligence
# ══════════════════════════════════════════════════════════════════════

# ── Enums ──────────────────────────────────────────────────────────────


class RecommendationStatus(str, Enum):
    """Convergence status from 4-signal matrix (§4 Stage 1)."""
    HIGH_CONFIDENCE_READY = "HIGH_CONFIDENCE_READY"
    WATCHLIST_BUILDING = "WATCHLIST_BUILDING"
    NOT_READY = "NOT_READY"


class BookingGateVerdict(str, Enum):
    """Booking Readiness Gate verdict (§4 Stage 2)."""
    PASS = "PASS"
    PROVISIONAL_WATCHLIST = "PROVISIONAL_WATCHLIST"
    FAIL_NURTURE_MODE = "FAIL_NURTURE_MODE"


class SessionBookingError(str, Enum):
    """Error types for Session Booking Intelligence."""
    INVALID_COACH_SCOPE = "INVALID_COACH_SCOPE"
    CONVERGENCE_ERROR = "CONVERGENCE_ERROR"
    GATE_EVALUATION_ERROR = "GATE_EVALUATION_ERROR"
    MISSING_METRICS = "MISSING_METRICS"


# ── Constants ──────────────────────────────────────────────────────────

# HIGH_CONFIDENCE_READY thresholds (§4 Stage 1)
BOOKING_COPING_HIGH: int = 4       # coping_trajectory >= 4
BOOKING_SPT_HIGH: int = 3          # spt_stage >= 3
BOOKING_TII_HIGH: float = 0.4      # composite_tii >= 0.4
# SEARCH phase must be CONFIRMED

# WATCHLIST_BUILDING thresholds (§4 Stage 1)
BOOKING_COPING_WATCH: int = 3      # coping_trajectory >= 3
BOOKING_SPT_WATCH: int = 3         # spt_stage >= 3
BOOKING_TII_WATCH: float = 0.3     # composite_tii >= 0.3
# SEARCH phase NOT strictly required

# Confidence scores
BOOKING_CONFIDENCE_HIGH: float = 1.0
BOOKING_CONFIDENCE_WATCH: float = 0.6
BOOKING_CONFIDENCE_FAIL: float = 0.0

# ── Models ─────────────────────────────────────────────────────────────


class QualifyingMetrics(BaseModel):
    """Snapshot of the 4 CBCS metrics at evaluation time (§5)."""
    tii_snapshot: float = Field(...)
    spt_snapshot: int = Field(...)
    search_confirmed: bool = Field(...)
    coping_tier: int = Field(...)


class OperatorBookingBriefRow(BaseModel):
    """Primary output — operator booking brief (DEP-ENG-076, §5)."""
    briefing_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    recommendation_status: str = Field(...)
    confidence_score_calc: float = Field(..., ge=0.0, le=1.0)
    gate_verdict: str = Field(...)
    qualifying_metrics: QualifyingMetrics = Field(...)
    evaluated_at: str = Field(...)


# ══════════════════════════════════════════════════════════════════════
# FR56 — Campaign Performance Registry
# ══════════════════════════════════════════════════════════════════════

# ── Enums ──────────────────────────────────────────────────────────────


class ConversionOutcome(str, Enum):
    """Commercial conversion result parsed from webhook (§4 Stage 1)."""
    BOOKED_CONVERTED = "BOOKED_CONVERTED"
    DECLINED_OPT_OUT = "DECLINED_OPT_OUT"
    NO_RESPONSE_DORMANT = "NO_RESPONSE_DORMANT"


class RegistryGateVerdict(str, Enum):
    """Registry Completeness Gate verdict (§4 Stage 2)."""
    PASS = "PASS"
    PROVISIONAL_PARTIAL = "PROVISIONAL_PARTIAL"
    FAIL_CORRUPTED = "FAIL_CORRUPTED"


class CampaignRegistryError(str, Enum):
    """Error types for Campaign Performance Registry."""
    MISSING_CLIENT_ID = "MISSING_CLIENT_ID"
    CORRUPTED_PSYCH_SNAPSHOT = "CORRUPTED_PSYCH_SNAPSHOT"
    GATE_EVALUATION_ERROR = "GATE_EVALUATION_ERROR"
    INVALID_COACH_SCOPE = "INVALID_COACH_SCOPE"


# ── Constants ──────────────────────────────────────────────────────────

# Dormancy threshold — hours after offer before NO_RESPONSE_DORMANT applies
CAMPAIGN_DORMANCY_HOURS: float = 72.0

# Webhook outcome resolution keys
BOOKED_WEBHOOK_KEYS: list[str] = [
    "checkout.session.completed",
    "charge.succeeded",
    "invitee.created",
]
DECLINED_WEBHOOK_KEYS: list[str] = ["/stop", "no thanks"]

# ── Models ─────────────────────────────────────────────────────────────


class PsychSnapshotAtLaunch(BaseModel):
    """Psychological state snapshot T-1 before campaign launch (§4 Stage 1)."""
    coping_tier: int | None = Field(default=None)
    spt_stage: int | None = Field(default=None)
    intimacy_score: float | None = Field(default=None)


class CampaignPerformanceRegistryRow(BaseModel):
    """Primary output — campaign performance registry row (DEP-ENG-051, §5)."""
    registry_id: str = Field(...)
    campaign_execution_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    conversion_outcome: str = Field(...)
    psych_snapshot_at_launch: PsychSnapshotAtLaunch = Field(...)
    time_to_conversion_hours: float | None = Field(default=None)
    gate_verdict: str = Field(...)
    log_timestamp: str = Field(...)


# ══════════════════════════════════════════════════════════════════════
# FR57 — Social Proof Intelligence Engine
# ══════════════════════════════════════════════════════════════════════

# ── Enums ──────────────────────────────────────────────────────────────


class MatchTierRating(str, Enum):
    """Tribal segment filter result from Stage 1 (§4 Stage 1)."""
    PERFECT_MATCH = "PERFECT_MATCH"
    ADJACENT_MATCH = "ADJACENT_MATCH"
    BASELINE_DEFAULT = "BASELINE_DEFAULT"


class SocialProofGateVerdict(str, Enum):
    """Relevance Stringency Gate verdict (§4 Stage 2)."""
    PASS = "PASS"
    PROVISIONAL = "PROVISIONAL"
    FAIL_OMIT_REQUIRED = "FAIL_OMIT_REQUIRED"


class SocialProofError(str, Enum):
    """Error types for Social Proof Intelligence Engine."""
    EMPTY_ARCHIVE = "EMPTY_ARCHIVE"
    FILTER_ERROR = "FILTER_ERROR"
    GATE_EVALUATION_ERROR = "GATE_EVALUATION_ERROR"
    INVALID_COACH_SCOPE = "INVALID_COACH_SCOPE"


# ── Models ─────────────────────────────────────────────────────────────


class TestimonialArchiveEntry(BaseModel):
    """A single testimonial in the Coach Story Archive (DEP-ENG-024)."""
    record_id: str = Field(...)
    coach_id: str = Field(...)
    coping_tier: int = Field(...)
    spt_stage: int = Field(...)
    testimonial_text: str = Field(...)


class MatchedTestimonialPayloadRow(BaseModel):
    """Primary output — matched testimonial payload (DEP-ENG-077, §5)."""
    retrieval_id: str = Field(...)
    target_client_id_linked: str = Field(...)
    coach_id: str = Field(...)
    match_tier_rating: str = Field(...)
    gate_verdict: str = Field(...)
    testimonial_text_raw: str | None = Field(default=None)
    matched_historical_record_id: str | None = Field(default=None)
    computation_timestamp: str = Field(...)


# ---------------------------------------------------------------------------
# FR51 — Challenge Funnel Intelligence Builder
# ---------------------------------------------------------------------------

class StructureFocus(str, Enum):
    """Challenge structure focus derived from tribe modal coping position (§4 Stage 1)."""
    FIVE_DAY_MOMENTUM = "5_DAY_MOMENTUM"
    SEVEN_DAY_IDENTITY = "7_DAY_IDENTITY"


class CommitmentGateVerdict(str, Enum):
    """Commitment Device Validation Gate verdicts (§4 Stage 2)."""
    PASS = "PASS"
    PROVISIONAL_FREE_ACCEPTED = "PROVISIONAL_FREE_ACCEPTED"
    FAIL_OVERPRICED = "FAIL_OVERPRICED"


class ChallengeFunnelError(str, Enum):
    """Error codes raised by FR51 services."""
    MISSING_TRIBAL_ANCHOR = "MISSING_TRIBAL_ANCHOR"
    EMPTY_COPING_ARRAY = "EMPTY_COPING_ARRAY"
    FAIL_OVERPRICED = "FAIL_OVERPRICED"
    LEXICON_KEY_MISSING = "LEXICON_KEY_MISSING"


class ChallengeFunnelBriefRow(BaseModel):
    """Primary output — challenge funnel brief (DEP-ENG-072, §5)."""
    funnel_blueprint_id: str = Field(...)
    coach_id: str = Field(...)
    challenge_duration_days: int = Field(...)
    structure_focus: str = Field(...)
    commitment_price: float = Field(...)
    hero_anchor_noun: str = Field(...)
    enemy_contrast_noun: str = Field(...)
    flyer_hook_text: str = Field(...)
    gate_verdict: str = Field(...)
    generated_at: str = Field(...)


# ---------------------------------------------------------------------------
# FR52 — Webinar Brief Generator
# ---------------------------------------------------------------------------

class AlignmentGateVerdict(str, Enum):
    """Structural Coping Alignment Gate verdicts (§4 Stage 2)."""
    PASS = "PASS"
    PROVISIONAL_PARAPHRASED = "PROVISIONAL_PARAPHRASED"
    FAIL_HALLUCINATED = "FAIL_HALLUCINATED"
    PASS_FALLBACK = "PASS_FALLBACK"


class WebinarBriefError(str, Enum):
    """Error codes raised by FR52 services."""
    EMPTY_ARCHIVE_FALLBACK = "EMPTY_ARCHIVE_FALLBACK"
    FAIL_HALLUCINATED = "FAIL_HALLUCINATED"
    EMPTY_COPING_AGGREGATE = "EMPTY_COPING_AGGREGATE"


class WebinarConversionBriefRow(BaseModel):
    """Primary output — webinar conversion brief (DEP-ENG-073, §5)."""
    webinar_brief_id: str = Field(...)
    coach_id: str = Field(...)
    dominant_coping_target: int = Field(...)
    change_talk_injected_quotes: list[str] = Field(...)
    gate_verdict: str = Field(...)
    intro_instruction_string: str = Field(...)
    close_instruction_string: str = Field(...)
    computation_timestamp: str = Field(...)


# ---------------------------------------------------------------------------
# FR53 — Conversion Sequence Generator
# ---------------------------------------------------------------------------

class SequenceVulnerabilityMode(str, Enum):
    """Linguistic depth mode derived from SPT stage (§4 Stage 1)."""
    OBJECTIVE_REFLECTIVE = "OBJECTIVE_REFLECTIVE"
    AFFECTIVE_ATTACHMENT = "AFFECTIVE_ATTACHMENT"


class DormancyGateVerdict(str, Enum):
    """Dormancy Recovery Gate verdicts (§4 Stage 2)."""
    PASS_ACTIVE = "PASS_ACTIVE"
    PROVISIONAL_DORMANT_RECOVERY = "PROVISIONAL_DORMANT_RECOVERY"
    FAIL_DORMANT_ABORT = "FAIL_DORMANT_ABORT"


class SequenceError(str, Enum):
    """Error codes raised by FR53 services."""
    FAIL_DORMANT_ABORT = "FAIL_DORMANT_ABORT"
    MISSING_TIMESTAMP = "MISSING_TIMESTAMP"


class ConversionSequencePayloadRow(BaseModel):
    """Primary output — conversion sequence payload (DEP-ENG-074, §5)."""
    sequence_execution_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    sequence_vulnerability_mode: str = Field(...)
    gate_verdict: str = Field(...)
    current_sequence_step_integer: int = Field(...)
    next_payload_string: str | None = Field(default=None)
    execution_timestamp: str = Field(...)


# ---------------------------------------------------------------------------
# FR54 — Promotional Asset Compiler
# ---------------------------------------------------------------------------

class AssetTypeGenerated(str, Enum):
    """Promotional asset type derived from generator source origin (§4 Stage 1)."""
    Z_PATTERN_FLYER = "Z_PATTERN_FLYER"
    VOICE_SCRIPT = "VOICE_SCRIPT"


class PayloadCompletenessVerdict(str, Enum):
    """Payload Completeness Gate verdicts (§4 Stage 2)."""
    PASS = "PASS"
    PROVISIONAL_MISSING_ASSET = "PROVISIONAL_MISSING_ASSET"
    FAIL_BOUNDARY_VIOLATION = "FAIL_BOUNDARY_VIOLATION"


class AssetCompilerError(str, Enum):
    """Error codes raised by FR54 services."""
    FAIL_BOUNDARY_VIOLATION = "FAIL_BOUNDARY_VIOLATION"
    MISSING_GENERATOR_SOURCE = "MISSING_GENERATOR_SOURCE"


class ZPatternNodes(BaseModel):
    """Z-Pattern flyer node layout (§4 Phase 3)."""
    top_left_hook: str = Field(...)
    bottom_right_cta: str = Field(...)


class StructuredAssetPayloadRow(BaseModel):
    """Primary output — structured asset payload (DEP-ENG-075, §5)."""
    asset_payload_id: str = Field(...)
    generator_source_id: str = Field(...)
    asset_type_generated: str = Field(...)
    gate_verdict: str = Field(...)
    z_pattern_nodes: ZPatternNodes | None = Field(default=None)
    tts_script_body: str | None = Field(default=None)
    compiled_at: str = Field(...)


# ---------------------------------------------------------------------------
# FR58 — Offer Tier Architecture
# ---------------------------------------------------------------------------

class OfferTierCeiling(str, Enum):
    """Maximum eligible offer tier derived from coping position (§4 Stage 1)."""
    TIER_A_PROOF = "TIER_A_PROOF"
    TIER_B_FIRST_PROOF_UNLOCK = "TIER_B_FIRST_PROOF_UNLOCK"
    TIER_C_SPEAKING_LEARNING = "TIER_C_SPEAKING_LEARNING"
    TIER_D_COACH_OS = "TIER_D_COACH_OS"
    TIER_E_OPERATOR = "TIER_E_OPERATOR"



class UpwardRoutingVerdict(str, Enum):
    """Upward-Only Routing Gate verdicts (§4 Stage 2)."""
    PASS_AUTHORIZED = "PASS_AUTHORIZED"
    PROVISIONAL_DOWNSELL_ATTEMPT = "PROVISIONAL_DOWNSELL_ATTEMPT"
    FAIL_CAPACITY_EXCEEDED = "FAIL_CAPACITY_EXCEEDED"


class OfferTierError(str, Enum):
    """Error codes raised by FR58 services."""
    FAIL_CAPACITY_EXCEEDED = "FAIL_CAPACITY_EXCEEDED"


class OfferTierGovernorRow(BaseModel):
    """Primary output — offer tier governor row (DEP-ENG-078, §5)."""
    governor_evaluation_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    computed_coping_position: int = Field(...)
    eligible_tier_ceiling: str = Field(...)
    target_campaign_tier: int = Field(...)
    gate_verdict: str = Field(...)
    timestamp: str = Field(...)


# ---------------------------------------------------------------------------
# FR59 — Campaign Orchestration Agent
# ---------------------------------------------------------------------------

class MasterCampaignState(str, Enum):
    """Timeline state enum governing orchestrator sequence position (§4 Stage 1)."""
    QUEUED_PENDING_LAUNCH = "QUEUED_PENDING_LAUNCH"
    ANCHORING_DAY_1_TO_3 = "ANCHORING_DAY_1_TO_3"
    CONVERSION_WINDOW_ACTIVE = "CONVERSION_WINDOW_ACTIVE"
    COOLDOWN_RESOLVED = "COOLDOWN_RESOLVED"


class CampaignGateVerdict(str, Enum):
    """Verdict from Campaign Initialization Gate (§4 Stage 2)."""
    PASS_AUTHORIZED = "PASS_AUTHORIZED"
    PROVISIONAL_LEGACY_MODE = "PROVISIONAL_LEGACY_MODE"
    FAIL_ABORTED = "FAIL_ABORTED"


class CampaignOrchestrationError(str, Enum):
    """Hard-abort error codes for FR59 Campaign Orchestration Agent."""
    FAIL_ABORTED = "FAIL_ABORTED"


class CampaignExecutionLogRow(BaseModel):
    """Primary output — campaign execution log row (DEP-ENG-079, §5)."""
    execution_run_id: str = Field(...)
    campaign_blueprint_id: str = Field(...)
    coach_id: str = Field(...)
    operator_auth_id: str = Field(...)
    master_campaign_state: str = Field(...)
    gate_verdict: str = Field(...)
    roster_size_at_launch: int = Field(...)
    started_at: str = Field(...)


# ---------------------------------------------------------------------------
# FR60 — Loom Report Generation
# ---------------------------------------------------------------------------

class LoomGateVerdict(str, Enum):
    """Actionable Threshold Gate verdict (§4 Stage 2)."""
    PASS = "PASS"
    PROVISIONAL_VAGUE_SUMMARY = "PROVISIONAL_VAGUE_SUMMARY"
    FAIL_HALLUCINATED_ADVICE = "FAIL_HALLUCINATED_ADVICE"


class LoomReportError(str, Enum):
    """Hard-abort error codes for FR60 Loom Report Generation."""
    FAIL_HALLUCINATED_ADVICE = "FAIL_HALLUCINATED_ADVICE"


class LoomSections(BaseModel):
    """Three narrative sections of the Loom Intelligence Report."""
    summary_block: str = Field(...)
    psychological_signal_block: str = Field(...)
    actionable_recommendation_block: str = Field(...)


class LoomNarrativeReportRow(BaseModel):
    """Primary output — loom narrative report row (DEP-ENG-080, §5)."""
    report_id: str = Field(...)
    campaign_execution_id: str = Field(...)
    coach_id: str = Field(...)
    gate_verdict: str = Field(...)
    loom_sections: LoomSections = Field(...)
    computation_timestamp: str = Field(...)


# ══════════════════════════════════════════════════════════════════════
# FR-ERA3-02 — In-Chat Telegram Payments
# ══════════════════════════════════════════════════════════════════════

# ── Enums ──────────────────────────────────────────────────────────────


class PaymentTier(str, Enum):
    """Pricing tiers from PRD-09 §3."""
    SPEAKING_LEARNING = "SPEAKING_LEARNING"     # $39.99/mo
    COACH_OS = "COACH_OS"                       # $99.99/mo


class PaymentStatus(str, Enum):
    """Payment transaction lifecycle states."""
    INVOICE_SENT = "INVOICE_SENT"
    PRE_CHECKOUT_CONFIRMED = "PRE_CHECKOUT_CONFIRMED"
    REQUIRES_ACTION = "REQUIRES_ACTION"         # SCA/3D Secure
    PAYMENT_SUCCESSFUL = "PAYMENT_SUCCESSFUL"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    REWARD_DISPATCHED = "REWARD_DISPATCHED"
    PROVISIONING_COMPLETE = "PROVISIONING_COMPLETE"


class EligibilityVerdict(str, Enum):
    """Eligibility check outcomes."""
    PASS_STANDARD = "PASS_STANDARD"
    PASS_LOYALTY_UNLOCK = "PASS_LOYALTY_UNLOCK"
    PROVISIONAL_PENDING_PAYMENT = "PROVISIONAL_PENDING_PAYMENT"
    FAIL_ALREADY_SUBSCRIBED = "FAIL_ALREADY_SUBSCRIBED"
    FAIL_TIER_EXCEEDED = "FAIL_TIER_EXCEEDED"
    FAIL_COOLDOWN_ACTIVE = "FAIL_COOLDOWN_ACTIVE"


class PaymentError(str, Enum):
    """Hard-abort error codes for FR-ERA3-02."""
    FAIL_ALREADY_SUBSCRIBED = "FAIL_ALREADY_SUBSCRIBED"
    FAIL_TIER_EXCEEDED = "FAIL_TIER_EXCEEDED"
    FAIL_STRIPE_ERROR = "FAIL_STRIPE_ERROR"
    FAIL_SIGNATURE_INVALID = "FAIL_SIGNATURE_INVALID"


# ── Constants ──────────────────────────────────────────────────────────

LOYALTY_ASSET_THRESHOLD: int = 50        # cumulative_assets_stored >= 50 triggers Loyalty Unlock
TIER_PRICE_MAP: dict[str, int] = {
    "SPEAKING_LEARNING": 3999,           # cents
    "COACH_OS": 9999,                    # cents
}


# ── Models ─────────────────────────────────────────────────────────────


class StoredValueSnapshot(BaseModel):
    """Snapshot of user's cumulative platform investment."""
    cumulative_assets_stored: int = Field(..., ge=0)
    voice_dna_trained: bool = Field(default=False)
    content_archive_count: int = Field(default=0, ge=0)
    reaction_count: int = Field(default=0, ge=0)


class EligibilityCheckResult(BaseModel):
    """Primary output — eligibility evaluation (DEP-PAY-001)."""
    eligibility_id: str = Field(...)
    telegram_user_id: int = Field(...)
    coach_id: str = Field(...)
    target_tier: str = Field(...)
    current_stripe_status: str = Field(...)
    stored_value: StoredValueSnapshot = Field(...)
    verdict: str = Field(...)
    offer_copy_variant: str = Field(...)    # "standard" | "loyalty_unlock"
    evaluated_at: str = Field(...)


class InvoicePayload(BaseModel):
    """Telegram sendInvoice payload (DEP-PAY-002)."""
    invoice_id: str = Field(...)
    chat_id: int = Field(...)
    title: str = Field(...)
    description: str = Field(...)
    payload: str = Field(...)               # internal tracking payload
    provider_token: str = Field(...)
    currency: str = Field(default="USD")
    prices: list[dict[str, int | str]] = Field(...)
    tier: str = Field(...)
    sent_at: str = Field(...)


class PaymentTransactionRow(BaseModel):
    """Payment transaction record (DEP-PAY-003)."""
    transaction_id: str = Field(...)
    telegram_user_id: int = Field(...)
    coach_id: str = Field(...)
    tier: str = Field(...)
    amount_cents: int = Field(..., gt=0)
    status: str = Field(...)
    stripe_charge_id: str = Field(default="")
    eligibility_id: str = Field(...)
    reward_dispatched: bool = Field(default=False)
    provisioning_complete: bool = Field(default=False)
    created_at: str = Field(...)
    updated_at: str = Field(...)


class TierSubscriptionRow(BaseModel):
    """Active subscription tracking record."""
    subscription_id: str = Field(...)
    telegram_user_id: int = Field(...)
    coach_id: str = Field(...)
    tier: str = Field(...)
    stripe_subscription_id: str = Field(default="")
    status: str = Field(default="active")
    started_at: str = Field(...)


class RewardDispatchResult(BaseModel):
    """Result of experiential reward push (DEP-PAY-004)."""
    dispatch_id: str = Field(...)
    chat_id: int = Field(...)
    tier: str = Field(...)
    asset_type: str = Field(...)            # "video" | "audio"
    asset_url: str = Field(...)
    telegram_message_id: int = Field(default=0)
    dispatched_at: str = Field(...)


class CoachOSProvisioningResult(BaseModel):
    """Result of background provisioning (DEP-PAY-005)."""
    provisioning_id: str = Field(...)
    telegram_user_id: int = Field(...)
    tier: str = Field(...)
    vector_namespace_created: bool = Field(...)
    voice_dna_initialized: bool = Field(...)
    completed_at: str = Field(...)
