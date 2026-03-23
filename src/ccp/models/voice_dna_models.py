"""
CCP FR3 Voice DNA Extraction — Data Models (Unit 1)
Pydantic v2 models for all FR3 pipeline objects.

Spec reference: FR3 Tech Spec §Context for Development, §Steps 1-10
Architecture reference: §7 (JIT Skill Compiler), §7.6 (Mandates 4, 7, 8)

Primary outputs:
  - DEP-ENG-004: NegativeSpaceObject (lexical_blacklist, syntactic_impossibilities, structural_exclusions)
  - DEP-ENG-003: PositiveSpaceObject (60-variable stylometry profile + prose descriptions)
  - humor_style_classification: HumorStyleClassification
  - ttt_baseline.json: AdversarialValidationResult
"""

import hashlib
import json
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


# ──────────────────────────────────────────────────────────────
# Constants from spec
# ──────────────────────────────────────────────────────────────

# Spec §Step 1: "Minimum 3,000 unique authenticated words"
MINIMUM_CORPUS_WORDS: int = 3000

# Spec §Step 3: "Minimum 12 invariant markers required"
MINIMUM_INVARIANT_MARKERS: int = 12

# Spec §Step 3: "within ±15% across all 5 clusters"
INVARIANCE_THRESHOLD_PCT: float = 15.0

# Spec §Step 10: quality gate thresholds
TTT_DRIFT_THRESHOLD_PCT: float = 15.0
AI_DETECTION_THRESHOLD_PCT: float = 5.0
BOREDOM_COSINE_THRESHOLD: float = 0.85

# Spec §Step 10: "Maximum 3 rewind cycles"
MAX_ADVERSARIAL_REWIND_CYCLES: int = 3

# Spec §Step 9: "Cycle repeats up to 3 times"
MAX_MANDATE7_CYCLES: int = 3

# Stress test Q1: "≥15 exact contrastive strings"
L3_MINIMUM_DEPTH_THRESHOLD: int = 15


# ──────────────────────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────────────────────

class MarkerInvarianceStatus(str, Enum):
    """Classification of a discourse marker after cross-topic invariance test."""
    INVARIANT = "INVARIANT"
    TOPIC_SPECIFIC = "TOPIC_SPECIFIC"


class PipelineStepStatus(str, Enum):
    """Status of a pipeline step execution."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    HALTED = "HALTED"


class HumorType(str, Enum):
    """Humor style classification per Architecture 6.
    Spec §Step 8: 'affiliative/self_enhancing/aggressive/self_defeating'."""
    AFFILIATIVE = "affiliative"
    SELF_ENHANCING = "self_enhancing"
    AGGRESSIVE = "aggressive"
    SELF_DEFEATING = "self_defeating"


# ──────────────────────────────────────────────────────────────
# Step 1: Corpus Assembly
# ──────────────────────────────────────────────────────────────

class CorpusUnit(BaseModel):
    """A single Thought Unit within the extraction corpus.
    Spec §Step 1: 'Tag each unit with session_id and unit_type.'"""
    unit_id: str
    session_id: str
    text: str
    word_count: int = 0
    unit_type: str = "sacred_audio"

    @field_validator("word_count", mode="before")
    @classmethod
    def auto_word_count(cls, v: int, info) -> int:
        if v == 0 and "text" in info.data:
            return len(info.data["text"].split())
        return v


class ExtractionCorpus(BaseModel):
    """Unified extraction corpus assembled from all FR2 sessions.
    Spec §Step 1: 'extraction_corpus.json — unified array of Thought_Units with metadata'."""
    coach_id: str
    coach_acronym: str
    units: list[CorpusUnit] = Field(default_factory=list)
    total_words: int = 0
    unique_words: int = 0
    session_ids: list[str] = Field(default_factory=list)
    corpus_hash: str = ""

    def compute_stats(self) -> None:
        """Compute total words, unique words, and corpus hash."""
        all_words = []
        for unit in self.units:
            all_words.extend(unit.text.lower().split())
        self.total_words = len(all_words)
        self.unique_words = len(set(all_words))
        self.session_ids = list(set(u.session_id for u in self.units))
        self.corpus_hash = hashlib.sha256(
            json.dumps([u.text for u in self.units]).encode()
        ).hexdigest()

    def passes_word_count_gate(self) -> bool:
        """Spec §Step 1 Gate: 'Minimum 3,000 unique authenticated words'."""
        return self.unique_words >= MINIMUM_CORPUS_WORDS


# ──────────────────────────────────────────────────────────────
# Step 2: Discourse Marker Census
# ──────────────────────────────────────────────────────────────

class MarkerPositionDistribution(BaseModel):
    """Position distribution for a single discourse marker.
    Spec §Step 2: 'position distribution (e.g., "so" appears 73% at
    sentence-opening, 27% mid-sentence)'."""
    marker: str
    total_occurrences: int = 0
    sentence_opening_count: int = 0
    sentence_middle_count: int = 0
    clause_bridging_count: int = 0
    sentence_opening_pct: float = 0.0
    sentence_middle_pct: float = 0.0
    clause_bridging_pct: float = 0.0

    def compute_percentages(self) -> None:
        total = self.total_occurrences
        if total > 0:
            self.sentence_opening_pct = (self.sentence_opening_count / total) * 100.0
            self.sentence_middle_pct = (self.sentence_middle_count / total) * 100.0
            self.clause_bridging_pct = (self.clause_bridging_count / total) * 100.0


class DiscourseMarkerMap(BaseModel):
    """Complete discourse marker census output.
    Spec §Step 2: 'discourse_marker_map.json — each marker with
    occurrence count + position distribution'."""
    markers: dict[str, MarkerPositionDistribution] = Field(default_factory=dict)
    corpus_hash: str = ""

    def get_marker_names(self) -> list[str]:
        return list(self.markers.keys())


# ──────────────────────────────────────────────────────────────
# Step 3: Cross-Topic Invariance
# ──────────────────────────────────────────────────────────────

class TopicCluster(BaseModel):
    """A subject cluster used in the cross-topic invariance test.
    Spec §Step 3: 'identify 5 maximally different subject clusters'."""
    cluster_id: str
    cluster_name: str
    unit_ids: list[str] = Field(default_factory=list)
    word_count: int = 0
    marker_distributions: dict[str, MarkerPositionDistribution] = Field(default_factory=dict)


class MarkerInvarianceResult(BaseModel):
    """Result of cross-topic invariance test for a single marker.
    Spec §Step 3: 'within ±15% across all 5 clusters to qualify as Voice DNA'."""
    marker: str
    status: MarkerInvarianceStatus
    max_variance_pct: float = 0.0
    cluster_values: dict[str, float] = Field(default_factory=dict)
    detail: str = ""


class InvarianceTestResult(BaseModel):
    """Full cross-topic invariance test output.
    Spec §Step 3: minimum 12 invariant markers required."""
    markers: list[MarkerInvarianceResult] = Field(default_factory=list)
    invariant_markers: list[str] = Field(default_factory=list)
    topic_specific_markers: list[str] = Field(default_factory=list)
    clusters_used: int = 5

    def passes_invariance_gate(self) -> bool:
        """Spec §Step 3 Gate: 'Minimum 12 invariant markers'."""
        return len(self.invariant_markers) >= MINIMUM_INVARIANT_MARKERS


# ──────────────────────────────────────────────────────────────
# Step 4: Sentence Skeleton Extraction (Stylometry Profile)
# ──────────────────────────────────────────────────────────────

class LexicalMorphologicalCluster(BaseModel):
    """Spec §Step 4 Cluster 1: Lexical/Morphological.
    'TTR, hapax legomena frequency, vocabulary density'."""
    type_token_ratio: float = 0.0
    hapax_legomena_frequency: float = 0.0
    vocabulary_density: float = 0.0
    unique_word_count: int = 0
    total_word_count: int = 0


class SyntacticDistributionCluster(BaseModel):
    """Spec §Step 4 Cluster 2: Subconscious Syntactic Distributions.
    'Function word ratios (and/but/so densities), clause connective patterns'."""
    and_density: float = 0.0
    but_density: float = 0.0
    so_density: float = 0.0
    because_density: float = 0.0
    if_density: float = 0.0
    clause_connective_ratio: float = 0.0


class WANMetricsCluster(BaseModel):
    """Spec §Step 4 Cluster 3: Relational WAN Metrics.
    'Preposition-conjunction transition probabilities, adjacency network map'."""
    transition_probabilities: dict[str, dict[str, float]] = Field(default_factory=dict)
    adjacency_pairs: list[tuple[str, str, float]] = Field(default_factory=list)
    network_density: float = 0.0


class GraphicalHabitsCluster(BaseModel):
    """Spec §Step 4 Cluster 4: Graphical Habits.
    'Punctuation density, capitalization anomalies'."""
    em_dash_per_100_words: float = 0.0
    ellipsis_frequency: float = 0.0
    comma_load_per_sentence: float = 0.0
    exclamation_frequency: float = 0.0
    capitalization_anomaly_rate: float = 0.0


class StructuralComplexityCluster(BaseModel):
    """Spec §Step 4 Cluster 5: Structural Complexity.
    'WPS flow pattern, paragraph-to-paragraph length variance'."""
    wps_mean: float = 0.0
    wps_median: float = 0.0
    wps_std_dev: float = 0.0
    wps_flow_pattern: list[int] = Field(default_factory=list)
    paragraph_length_variance: float = 0.0
    short_sentence_ratio: float = 0.0
    long_sentence_ratio: float = 0.0


class StylometryProfile(BaseModel):
    """Complete 60-variable stylometry profile from Step 4.
    Spec §Step 4: 'These 6 cluster groups form the core of the
    Positive Space Object (60-variable profile).'"""
    lexical: LexicalMorphologicalCluster = Field(default_factory=LexicalMorphologicalCluster)
    syntactic: SyntacticDistributionCluster = Field(default_factory=SyntacticDistributionCluster)
    wan_metrics: WANMetricsCluster = Field(default_factory=WANMetricsCluster)
    graphical: GraphicalHabitsCluster = Field(default_factory=GraphicalHabitsCluster)
    structural: StructuralComplexityCluster = Field(default_factory=StructuralComplexityCluster)
    invariant_markers: list[str] = Field(default_factory=list)
    profile_hash: str = ""

    def compute_hash(self) -> str:
        """Hash the profile for receipt chain."""
        data = self.model_dump(exclude={"profile_hash"})
        self.profile_hash = hashlib.sha256(
            json.dumps(data, default=str).encode()
        ).hexdigest()
        return self.profile_hash


# ──────────────────────────────────────────────────────────────
# Step 5: Negative Space Object (DEP-ENG-004)
# ──────────────────────────────────────────────────────────────

class LexicalBlacklist(BaseModel):
    """Spec §Step 5 Component A: Lexical Blacklist.
    'Words never used by the coach in the corpus.'"""
    academic: list[str] = Field(default_factory=list)
    spiritual: list[str] = Field(default_factory=list)
    banned_intensifiers: list[str] = Field(default_factory=list)


class StructuralExclusions(BaseModel):
    """Spec §Step 5 Component C: Structural Exclusions.
    'Macro-level content structures never present.'"""
    forbidden_openings: list[str] = Field(default_factory=list)
    forbidden_closings: list[str] = Field(default_factory=list)


class NegativeSpaceObject(BaseModel):
    """DEP-ENG-004 — Negative Space Object.
    Spec §Step 5: exact JSON structure specified.
    Stress test Q1: Gate PC-03 enforces ≥15 contrastive strings."""
    lexical_blacklist: LexicalBlacklist = Field(default_factory=LexicalBlacklist)
    syntactic_impossibilities: list[str] = Field(default_factory=list)
    structural_exclusions: StructuralExclusions = Field(default_factory=StructuralExclusions)
    dep_id: str = "DEP-ENG-004"
    extraction_timestamp: str = ""
    object_hash: str = ""

    def total_contrastive_strings(self) -> int:
        """Count all contrastive strings for Gate PC-03 validation.
        Stress test Q1: 'count is mathematically less than 15 validated
        contrastive strings → L3_INSUFFICIENT_DEPTH halt'."""
        count = 0
        count += len(self.lexical_blacklist.academic)
        count += len(self.lexical_blacklist.spiritual)
        count += len(self.lexical_blacklist.banned_intensifiers)
        count += len(self.syntactic_impossibilities)
        count += len(self.structural_exclusions.forbidden_openings)
        count += len(self.structural_exclusions.forbidden_closings)
        return count

    def passes_depth_gate(self) -> bool:
        """Gate PC-03: L3 Minimum Depth Threshold.
        Spec + Stress test Q1: ≥15 exact contrastive strings."""
        return self.total_contrastive_strings() >= L3_MINIMUM_DEPTH_THRESHOLD

    def compute_hash(self) -> str:
        data = self.model_dump(exclude={"object_hash"})
        self.object_hash = hashlib.sha256(
            json.dumps(data, default=str).encode()
        ).hexdigest()
        return self.object_hash


# ──────────────────────────────────────────────────────────────
# Steps 6-8: Positive Space Object (DEP-ENG-003)
# ──────────────────────────────────────────────────────────────

class ClusterProseDescription(BaseModel):
    """Numerical profile + prose description for a single cluster.
    Spec §Steps 6-8: 'generate the numerical profile AND a prose
    description suitable for inclusion in Block A of compiled SKILL.md files.'"""
    cluster_name: str
    numerical_profile: dict[str, Any] = Field(default_factory=dict)
    prose_description: str = ""


class PositiveSpaceObject(BaseModel):
    """DEP-ENG-003 — Positive Space (60-Variable Stylometry Profile).
    Spec §Steps 6-8: 5 cluster groups → numerical + prose."""
    clusters: list[ClusterProseDescription] = Field(default_factory=list)
    stylometry_profile: Optional[StylometryProfile] = None
    total_variables: int = 0
    dep_id: str = "DEP-ENG-003"
    extraction_timestamp: str = ""
    object_hash: str = ""

    def is_complete(self) -> bool:
        """Stress test Q2: 'An incomplete matrix evaluates as status: PARTIAL.'
        All 5 clusters must be present with prose descriptions."""
        if len(self.clusters) < 5:
            return False
        return all(c.prose_description != "" for c in self.clusters)

    def compute_hash(self) -> str:
        data = self.model_dump(exclude={"object_hash"})
        self.object_hash = hashlib.sha256(
            json.dumps(data, default=str).encode()
        ).hexdigest()
        return self.object_hash


# ──────────────────────────────────────────────────────────────
# Step 8: Humor Style Classification (Mandate 8)
# ──────────────────────────────────────────────────────────────

class HumorStyleClassification(BaseModel):
    """Humor style classification per Architecture 6.
    Spec §Step 8: 'affiliative/self_enhancing/aggressive/self_defeating'."""
    primary_style: HumorType = HumorType.AFFILIATIVE
    secondary_style: Optional[HumorType] = None
    self_referential_frequency: float = 0.0
    observational_irony_frequency: float = 0.0
    self_deprecation_frequency: float = 0.0
    absurdist_frequency: float = 0.0
    aggressive_targeting_present: bool = False
    detail: str = ""


# ──────────────────────────────────────────────────────────────
# Step 9: Emotional DNA Integration Test (Mandate 7)
# ──────────────────────────────────────────────────────────────

class Mandate7TestResult(BaseModel):
    """Result of Mandate 7 emotional DNA integration test.
    Spec §Step 9: 'Would someone who shares this coach's specific wound
    architecture recognize their own experience in the first 30 words?'"""
    passed: bool = False
    cycles_used: int = 0
    samples: list[str] = Field(default_factory=list)
    evaluation_details: list[str] = Field(default_factory=list)
    skipped: bool = False
    skip_reason: str = ""


# ──────────────────────────────────────────────────────────────
# Step 10: Adversarial Validation
# ──────────────────────────────────────────────────────────────

class AdversarialSampleResult(BaseModel):
    """Result of adversarial evaluation for a single sample."""
    sample_index: int
    sample_text: str = ""
    ttt_drift_pct: float = 0.0
    ai_detection_pct: float = 0.0
    boredom_cosine: float = 0.0
    adversary_flagged: bool = False
    adversary_flagged_structure: str = ""
    adversary_flagged_reason: str = ""


class AdversarialValidationResult(BaseModel):
    """Full adversarial validation output for Step 10.
    Spec §Step 10: 'TTT drift < 15%, AI detection < 5%,
    Boredom ≤0.85 cosine similarity'."""
    passed: bool = False
    rewind_cycles_used: int = 0
    samples: list[AdversarialSampleResult] = Field(default_factory=list)
    max_ttt_drift_pct: float = 0.0
    max_ai_detection_pct: float = 0.0
    max_boredom_cosine: float = 0.0
    structures_added_to_negative_space: list[str] = Field(default_factory=list)
    ttt_baseline_hash: str = ""
    detail: str = ""

    def passes_all_gates(self) -> bool:
        """Check all 3 quality gates."""
        if not self.samples:
            return False
        return (
            self.max_ttt_drift_pct < TTT_DRIFT_THRESHOLD_PCT
            and self.max_ai_detection_pct < AI_DETECTION_THRESHOLD_PCT
            and self.max_boredom_cosine <= BOREDOM_COSINE_THRESHOLD
            and not any(s.adversary_flagged for s in self.samples)
        )


# ──────────────────────────────────────────────────────────────
# V5.0 Extension Triggers
# ──────────────────────────────────────────────────────────────

class V50ExtensionStatus(BaseModel):
    """V5.0 post-Step-10 onboarding chain status.
    Spec §V5.0 Extension: Steps 0-A through 0-D."""
    step_0a_cmm_triggered: bool = False
    step_0b_story_archive_triggered: bool = False
    step_0c_humor_registry_created: bool = False
    step_0d_context_performance_created: bool = False


# ──────────────────────────────────────────────────────────────
# Pipeline Session (top-level container)
# ──────────────────────────────────────────────────────────────

class VoiceDNAPipelineSession(BaseModel):
    """Top-level session object tracking the full FR3 pipeline execution."""
    session_id: str
    coach_id: str
    coach_acronym: str
    date: str = Field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    # Step outputs
    corpus: Optional[ExtractionCorpus] = None
    discourse_marker_map: Optional[DiscourseMarkerMap] = None
    invariance_result: Optional[InvarianceTestResult] = None
    stylometry_profile: Optional[StylometryProfile] = None
    negative_space: Optional[NegativeSpaceObject] = None
    positive_space: Optional[PositiveSpaceObject] = None
    humor_classification: Optional[HumorStyleClassification] = None
    mandate7_result: Optional[Mandate7TestResult] = None
    adversarial_result: Optional[AdversarialValidationResult] = None
    v50_status: V50ExtensionStatus = Field(default_factory=V50ExtensionStatus)

    # Step statuses
    step_statuses: dict[str, PipelineStepStatus] = Field(default_factory=dict)

    # Receipt tracking
    receipt_ids: dict[str, str] = Field(default_factory=dict)

    # Final output
    dep_eng_003_written: bool = False
    dep_eng_004_written: bool = False
    ttt_baseline_written: bool = False

    def is_complete(self) -> bool:
        """Pipeline is complete when both DEP objects and ttt_baseline are written."""
        return self.dep_eng_003_written and self.dep_eng_004_written and self.ttt_baseline_written
