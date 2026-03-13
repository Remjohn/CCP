"""
Script Prompt Schema Validator
-------------------------------
Validates that a script prompt's input payload matches the standardized
8-input contract defined in script_prompt_schema.json.

Runs at pipeline init time to catch contract violations BEFORE generation.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)


# ─── Enums ───────────────────────────────────────────────────────────

class DataPhase(str, Enum):
    COLD = "COLD"
    WARM = "WARM"
    HOT = "HOT"


class RegulatoryFocus(str, Enum):
    PROMOTION = "PROMOTION"
    PREVENTION = "PREVENTION"
    DUAL_DOMINANT = "DUAL_DOMINANT"


class CopingPhase(str, Enum):
    PRE_CONTEMPLATION = "PRE_CONTEMPLATION"
    SEARCH_PHASE = "SEARCH_PHASE"
    ACTIVE_COPING = "ACTIVE_COPING"
    MAINTENANCE = "MAINTENANCE"


class Confidence(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ExpressionStyle(str, Enum):
    DIRECT = "DIRECT"
    COMPRESSED = "COMPRESSED"
    EXPANSIVE = "EXPANSIVE"
    CYCLIC = "CYCLIC"


class VisualCategory(str, Enum):
    SINGLE_FRAME = "single_frame"
    COMPARISON = "comparison"
    SEQUENTIAL = "sequential"
    INSTRUCTIONAL = "instructional"


# ─── Input 1: Structural Congruence Point ────────────────────────────

class StructuralCongruencePoint(BaseModel):
    """The seed — where coach and audience maps overlap."""
    trigger_id: str
    trigger_expression_angle: str
    audience_foundation_violated: str
    congruence_description: str
    seed_esk_anchors: list[str] = Field(min_length=1)
    data_phase: DataPhase


# ─── Input 2: Voice DNA SPR (3-Layer) ───────────────────────────────

class VoiceDNALayer1(BaseModel):
    """Construction mechanics — sentence skeletons, discourse markers, rhythm."""
    sentence_skeletons: list[str] = Field(min_length=1)
    discourse_markers: dict[str, str] = Field(default_factory=dict)
    rhythm_patterns: str
    default_sentence_length_range: list[int] = Field(min_length=2, max_length=2)


class VoiceDNALayer2(BaseModel):
    """Emotional path — how the coach travels from activation to expression."""
    activation_to_expression_sequence: list[str] = Field(min_length=1)
    peak_expression_markers: list[str] = Field(default_factory=list)
    recovery_pattern: str


class VoiceDNALayer3(BaseModel):
    """Leadership elevation — peak expression of Attractive Leader Traits."""
    primary_trait: str
    ttt_ceiling: str
    elevation_trigger: str


class VoiceDNASPR(BaseModel):
    """3-layer Sparse Priming Representation of the coach's voice."""
    layer_1_construction: VoiceDNALayer1
    layer_2_emotional_path: VoiceDNALayer2
    layer_3_leadership_elevation: VoiceDNALayer3


# ─── Input 3: Emotional DNA ─────────────────────────────────────────

class EmotionalDNA(BaseModel):
    """10-variable appraisal profile differentiating this coach."""
    appraisal_sequence: list[str] = Field(min_length=1)
    coping_potential_pattern: str
    norm_compatibility_threshold: float = Field(ge=0.0, le=1.0)
    trigger_specificity_threshold: float = Field(ge=0.0, le=1.0)
    emotional_recovery_speed: str  # FAST | MODERATE | SLOW
    dominant_moral_position: str
    activation_intensity: float = Field(ge=0.0, le=1.0)
    expression_style: ExpressionStyle
    vulnerability_window: str
    dual_layer_frequency: float = Field(ge=0.0, le=1.0)


# ─── Input 4: Negative Space ────────────────────────────────────────

class NegativeSpace(BaseModel):
    """What the coach must NOT produce. Loaded FIRST."""
    forbidden_vocabulary: list[str] = Field(default_factory=list)
    forbidden_tones: list[str] = Field(default_factory=list)
    forbidden_rhetorical_moves: list[str] = Field(default_factory=list)
    identity_edges: list[str] = Field(default_factory=list)
    anti_patterns: list[str] = Field(default_factory=list)


# ─── Input 5: Audience Tribal Terms ─────────────────────────────────

class AudienceTribalTerms(BaseModel):
    """In-group vocabulary. Minimum 3 verified terms per content piece."""
    verified_terms: list[str] = Field(min_length=3)
    term_contexts: dict[str, str] = Field(default_factory=dict)
    generation_markers: list[str] = Field(default_factory=list)
    enemy_labels: list[str] = Field(default_factory=list)


# ─── Input 6: Authentication Certificate ────────────────────────────

class PerMarkerScores(BaseModel):
    sentence_compression: float = Field(ge=0.0, le=1.0)
    first_person_singular: float = Field(ge=0.0, le=1.0)
    hedging_absence: float = Field(ge=0.0, le=1.0)
    verb_tense_present: float = Field(ge=0.0, le=1.0)
    exclusive_words: float = Field(ge=0.0, le=1.0)


class AuthenticationCertificate(BaseModel):
    """LIWC-based authentication. Gates generation fidelity."""
    composite_liwc_score: float = Field(ge=0.0, le=1.0)
    per_marker_scores: PerMarkerScores
    dual_layer_activation_detected: bool
    trigger_id: str

    def get_fidelity_level(self) -> str:
        """Determine fidelity gate based on authentication score."""
        if self.composite_liwc_score > 0.7 and self.dual_layer_activation_detected:
            return "HIGH_FIDELITY"
        elif self.composite_liwc_score >= 0.4:
            return "STANDARD_FIDELITY"
        else:
            return "RE_ELICITATION"


# ─── Input 7: Archetype Metadata ────────────────────────────────────

class TTTGravityLayer(BaseModel):
    ttt_level: str
    ttt_name: str
    focus: str


class ResolvedPersuasiveAngle(BaseModel):
    id: str
    name: str
    operational_instruction: str
    construction_constraint: str


class ArchetypeMetadata(BaseModel):
    """Fully resolved archetype metadata from the Archetype Registry Tool."""
    archetype_id: str
    archetype_name: str
    framework_id: str
    framework_name: str
    priority_level: int = Field(ge=1, le=10)
    visual_category: VisualCategory
    persuasive_angles: list[ResolvedPersuasiveAngle] = Field(min_length=1)
    ttt_palette_base_gravity: TTTGravityLayer
    ttt_palette_accent_layer: Optional[TTTGravityLayer] = None
    ttt_palette_intuitive_layer: Optional[TTTGravityLayer] = None
    usage_notes: str = ""
    format_compatibility: list[str] = Field(default_factory=lambda: ["video_note", "carousel", "thread"])


# ─── Input 8: Context Premise Summary ───────────────────────────────

class ContextPremiseSummary(BaseModel):
    """Aggregated audience profile from the Context Premise Engine."""
    dominant_regulatory_focus: RegulatoryFocus
    dominant_moral_foundation: str
    mft_vector: dict[str, float] = Field(default_factory=dict)
    coping_phase: CopingPhase
    hermeneutical_gap_score: float = Field(ge=0.0, le=1.0)
    data_phase: DataPhase
    sample_size: int = Field(ge=0)
    confidence: Confidence


# ─── Optional Enrichment Inputs (HOT phase only) ────────────────────

class EnrichmentInputs(BaseModel):
    """Only populated in HOT data phase (>50 audience texts)."""
    audience_reconsolidation_sensitivity: Optional[float] = Field(
        default=None, ge=0.0, le=1.0
    )
    audience_authenticity_distribution: Optional[dict[str, float]] = None
    intersection_score: Optional[float] = Field(
        default=None, ge=0.0, le=1.0
    )


# ─── Composite: Full Script Prompt Payload ──────────────────────────

class ScriptPromptPayload(BaseModel):
    """
    The complete input payload for a Script Prompt SKILL.md.
    Replaces the legacy {content_idea} + {Conscious_Soul_Values} contract.
    """
    # Mandatory inputs (8)
    structural_congruence_point: StructuralCongruencePoint
    voice_dna_spr: VoiceDNASPR
    emotional_dna: EmotionalDNA
    negative_space: NegativeSpace
    audience_tribal_terms: AudienceTribalTerms
    authentication_certificate: AuthenticationCertificate
    archetype_metadata: ArchetypeMetadata
    context_premise_summary: ContextPremiseSummary

    # Optional enrichment (HOT phase only)
    enrichment: Optional[EnrichmentInputs] = None

    @field_validator("enrichment", mode="before")
    @classmethod
    def gate_enrichment_by_phase(cls, v, info):
        """Enrichment inputs are only valid in HOT data phase."""
        scp = info.data.get("structural_congruence_point")
        if scp and hasattr(scp, "data_phase"):
            if scp.data_phase != DataPhase.HOT and v is not None:
                logger.warning(
                    f"Enrichment inputs provided but data_phase is {scp.data_phase}, "
                    f"not HOT. Clearing enrichment."
                )
                return None
        return v

    def get_loading_sequence(self) -> list[tuple[str, object]]:
        """Returns inputs in the mandated loading order."""
        return [
            ("negative_space", self.negative_space),
            ("authentication_certificate", self.authentication_certificate),
            ("structural_congruence_point", self.structural_congruence_point),
            ("voice_dna_spr", self.voice_dna_spr),
            ("emotional_dna", self.emotional_dna),
            ("audience_tribal_terms", self.audience_tribal_terms),
            ("archetype_metadata", self.archetype_metadata),
            ("context_premise_summary", self.context_premise_summary),
        ]

    def get_fidelity_level(self) -> str:
        """Returns the fidelity gate for this payload."""
        return self.authentication_certificate.get_fidelity_level()

    def get_priming_layers(self) -> dict:
        """Extracts the 3-layer priming config from voice DNA + archetype palette."""
        return {
            "layer_1_universal_emotion": self.archetype_metadata.ttt_palette_base_gravity,
            "layer_2_coach_emotional_path": self.voice_dna_spr.layer_2_emotional_path,
            "layer_3_leadership_elevation": self.archetype_metadata.ttt_palette_intuitive_layer,
        }


# ─── Validation Functions ───────────────────────────────────────────

def validate_payload(payload_dict: dict) -> tuple[bool, ScriptPromptPayload | None, list[str]]:
    """
    Validates a script prompt payload dict against the schema.
    Returns (is_valid, payload_or_none, list_of_errors).
    """
    errors = []
    try:
        payload = ScriptPromptPayload(**payload_dict)
        return True, payload, []
    except Exception as e:
        for error in getattr(e, "errors", lambda: [{"msg": str(e)}])():
            loc = " → ".join(str(l) for l in error.get("loc", []))
            errors.append(f"[{loc}] {error.get('msg', 'Unknown error')}")
        return False, None, errors


def validate_payload_from_file(filepath: str) -> tuple[bool, ScriptPromptPayload | None, list[str]]:
    """Validates a JSON file containing a script prompt payload."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return validate_payload(data)
    except json.JSONDecodeError as e:
        return False, None, [f"JSON parse error: {e}"]
    except FileNotFoundError:
        return False, None, [f"File not found: {filepath}"]


def check_deprecated_inputs(payload_dict: dict) -> list[str]:
    """
    Checks if a payload contains any deprecated input names.
    Returns warnings for any found.
    """
    deprecated = {
        "content_idea": "structural_congruence_point.trigger_expression_angle",
        "Conscious_Soul_Values": "voice_dna_spr + emotional_dna + negative_space",
        "character_lexicon": "Only used by Art Director, not Script Prompts",
        "content_archetype": "archetype_metadata (fully resolved)",
    }
    warnings = []
    for old_key, replacement in deprecated.items():
        if old_key in payload_dict:
            warnings.append(
                f"DEPRECATED: '{old_key}' found in payload. "
                f"Replace with: {replacement}"
            )
    return warnings
