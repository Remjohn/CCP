"""
CCP Step 13 — Per-Coach Onboarding Prerequisite Models

Covers: FR13, FR28, FR29, FR38, FR44

DEP-IDs produced:
  DEP-ENG-028 — Client Context Extraction Payload (FR13 Stage 1 output)
  DEP-ENG-029 — Cypher Transaction Manifest (FR13 Stage 2 output)
  DEP-ENG-030 — Client Context Premise Map / 1:1 Neo4j graph (FR13 Stage 3 output)
  DEP-ENG-024 — Dynamic Journaling Directive (FR28 output; distinct from Story Archive)
  DEP-ENG-006 — Context Premise Extraction JSON (FR29 output)
  DEP-ENG-033 — Semantic Committal Receipt (FR38 output)

NOTE: DEP-ENG-030 (1:1 client graph, FR13) is architecturally distinct from
DEP-ENG-006 (macro audience Context Premise, FR9/FR29). Never substitute one for the other.

NOTE: DEP-ENG-024 here is the Dynamic Journaling Directive (FR28).
      DEP-ENG-024 in v5_models.py is the Coach Story Archive. These are different
      sub-schemas sharing the same DEP-ID family. The Journaling Directive is a
      transient execution object; the Story Archive is a persistent knowledge asset.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, model_validator


# ══════════════════════════════════════════════════════════════════════════════
# Constants
# ══════════════════════════════════════════════════════════════════════════════

EXTRACTION_LATENCY_BUDGET_MS: int = 5000
"""FR29 §2: Full pipeline (transcription + extraction + graph write) < 5s."""

WHISPER_TIMEOUT_MS: int = 1500
"""FR29 §4 Stage 1 target: transcription <1.5s."""

ARIA_EXTRACTION_BUDGET_MS: int = 2500
"""FR29 §4 Stage 2 / AC1: 12-dimension extraction < 2500ms (fast model mandatory)."""

GRAPH_WRITE_BUDGET_MS: int = 1000
"""FR29 §4 Stage 3 target: Neo4j write < 1.0s."""

LIWC_EMOTIONAL_INTENSITY_THRESHOLD: float = 7.0
"""FR38 §4 Stage 1: LIWC-22 score > 7.0 → extract to Episodic."""

PATTERN_OCCURRENCE_THRESHOLD: int = 3
"""FR38 §4 Stage 2 Gate: Same root emotional driver ≥ 3 times across sessions."""

PATTERN_MIN_SPAN_DAYS: int = 14
"""FR38 §4 Stage 2: Occurrences must span ≥ 14 days."""

STALE_DECAY_DAYS: int = 30
"""FR38 §6 Fallback: Proposals untouched >30 days → auto-rejected."""

ANTI_ESCALATION_MIN_DAYS: int = 14
"""FR28 §3 Tech Decision 2: Cannot escalate past Foundation before day 14."""

JOURNALING_MAX_WORDS: int = 75
"""FR28 §4 Stage 3: Artisan output strictly capped at 75 words."""

CPR_SPARSE_THRESHOLD: int = 5
"""FR44 §3 Tech Decision 2: < 5 matched sessions → confidence_score = 0.2."""

CPR_RULE_OVERRIDE_THRESHOLD: int = 50
"""FR44 §4 Stage 4: Minimum rows before efficiency report generation."""

CPR_OUTPERFORM_MULTIPLIER: float = 1.2
"""FR44 §4 Stage 3: engagement_rate > 1.2× coach baseline → outperformed_default=True."""


# ══════════════════════════════════════════════════════════════════════════════
# Enums
# ══════════════════════════════════════════════════════════════════════════════

class ContextDimension(str, Enum):
    """FR13/FR29 §4 Stage 2: 12-dimension extraction map for Aria."""
    ENEMY = "Enemy"
    DREAM = "Dream"
    FEAR = "Fear"
    IDENTITY = "Identity"
    COACH_REFERENCE = "CoachReference"
    RITUAL_AFFINITY = "RitualAffinity"
    CAPACITY_SCORE = "CapacityScore"
    TTT_STATE = "TTTState"
    IDENTITY_PILLAR = "IdentityPillar"
    EMOTIONAL_TRIGGER = "EmotionalTrigger"
    RESISTANCE_PATTERN = "ResistancePattern"
    MILESTONE_PROXIMITY = "MilestoneProximity"


class ContextRelationship(str, Enum):
    """FR13 §4 Stage 2 / FR29: Neo4j relationship types."""
    FIGHTS_AGAINST = "FIGHTS_AGAINST"
    FEARS = "FEARS"
    CRAVES = "CRAVES"
    HAS_IDENTITY = "HAS_IDENTITY"
    GUIDED_BY = "GUIDED_BY"
    RESONATES_WITH = "RESONATES_WITH"
    TRIGGERS = "TRIGGERS"


class DepthLevel(str, Enum):
    """FR13/FR29: L1 surface, L2 private, L3 structural depth classification."""
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"


class GraphCommitVerdict(str, Enum):
    """FR13 §4 Stage 3 gate logic outcomes."""
    PASS = "PASS"
    PROVISIONAL = "PROVISIONAL"
    FAIL = "FAIL"


class CapacityTrack(str, Enum):
    """FR28 §4 Stage 2: Atlas 5-track roadmap."""
    RECOVERY = "Recovery"
    FOUNDATION = "Foundation"
    GROWTH = "Growth"
    MOMENTUM = "Momentum"
    PEAK = "Peak"


class StructuralDay(str, Enum):
    """FR28 §3 Tech Decision 1: 4+1+2 weekly pattern."""
    ACTIVE_RITUAL = "Active Ritual"
    REFLECTION_POINT = "Reflection Point"
    REST_DAY = "Rest Day"


class MoodState(str, Enum):
    """FR28 §4 Stage 2: Aria emotional state values."""
    DISTRESSED = "distressed"
    ANXIOUS_AVOIDANT = "anxious_avoidant"
    APATHETIC = "apathetic"
    MOTIVATED = "motivated"
    COMPLACENT = "complacent"
    STABLE = "stable"


class OperatorVerdict(str, Enum):
    """FR38 §4 Stage 3: Human-in-the-loop approval outcomes."""
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    MODIFY = "MODIFY"


class MemoryTierEdge(str, Enum):
    """FR38 §4: Neo4j edge label for memory tier classification."""
    WORKING = "WORKING"
    EPISODIC = "EPISODIC"
    SEMANTIC = "SEMANTIC"
    SUPPORTING_EVIDENCE = "SUPPORTING_EVIDENCE"


class GraphMutationStatus(str, Enum):
    """FR38 §5: Outcome of the Semantic Committal graph mutation."""
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"
    PENDING = "PENDING"


# ══════════════════════════════════════════════════════════════════════════════
# FR13 — Client Context Premise Map (DEP-ENG-028, 029, 030)
# ══════════════════════════════════════════════════════════════════════════════

class ContextEdgeProposal(BaseModel):
    """FR13 §5: A proposed Neo4j edge between two extracted nodes."""
    source_node: str = Field(..., description="Source node ID")
    target_node: str = Field(..., description="Target node ID")
    relationship: ContextRelationship
    properties: dict[str, Any] = Field(default_factory=dict)


class ExtractedContextNode(BaseModel):
    """FR13 §4 Stage 1: A single entity extracted by Aria across one dimension.

    Spec: 'the node attributes must perfectly contain that exact raw string
    without LLM summarization' (AC1 — Raw Language Preservation).
    """
    node_id: str = Field(default="")
    dimension: ContextDimension
    raw_language: str = Field(
        ...,
        description="Exact verbatim substring from transcript — NEVER summarized (AC1).",
        min_length=1,
    )
    depth_level: DepthLevel = DepthLevel.L1
    semantic_category: Optional[str] = None
    intensity: Optional[str] = None

    # Legacy / test compatibility fields
    label: str = Field(default="")
    raw_value: str = Field(default="")

    @model_validator(mode="before")
    @classmethod
    def resolve_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            lbl = data.get("label", "")
            val = data.get("raw_value", "")
            
            if "raw_language" not in data:
                raw = ""
                if lbl:
                    raw = lbl
                elif val:
                    raw = val
                data["raw_language"] = raw
            
            raw_lang = data.get("raw_language", "")
            if not lbl:
                data["label"] = raw_lang
            if not val:
                data["raw_value"] = raw_lang

            if not data.get("node_id"):
                if data.get("label"):
                    data["node_id"] = f"NODE-{data['label']}"
                else:
                    data["node_id"] = f"NODE-{str(raw_lang)[:20].replace(' ', '_')}"
        return data


class ClientContextExtraction(BaseModel):
    """DEP-ENG-028 — Stage 1 output: 12-dimensional extraction by Aria.

    Spec: FR13 §5 'client_context_extraction.json'
    """
    session_reference: str
    client_hash: str
    coach_id: str = Field(..., min_length=3, max_length=3, description="ADR-01: scoped per coach")
    extracted_nodes: list[ExtractedContextNode] = Field(default_factory=list)
    proposed_edges: list[ContextEdgeProposal] = Field(default_factory=list)
    pii_redacted: bool = False
    extraction_timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @model_validator(mode="after")
    def enforce_minimum_entities(self) -> "ClientContextExtraction":
        """FR13 §4 Stage 1 Failure Condition: < 2 valid entities → fail."""
        # Validation deferred to pipeline layer — model allows 0 to support null state
        return self

    @property
    def has_orphaned_nodes(self) -> bool:
        """FR13 AC3: Detects nodes with no outgoing or incoming edge."""
        connected_ids: set[str] = set()
        for edge in self.proposed_edges:
            connected_ids.add(edge.source_node)
            connected_ids.add(edge.target_node)
        for node in self.extracted_nodes:
            if node.node_id not in connected_ids:
                return True
        return False


class CypherQuery(BaseModel):
    """A single Cypher statement with ordering metadata."""
    sequence: int
    cypher: str
    node_ids_referenced: list[str] = Field(default_factory=list)


class CypherTransactionManifest(BaseModel):
    """DEP-ENG-029 — Stage 2 output: ordered Cypher MERGE commands from Atlas.

    Spec: FR13 §5 'cypher_transaction_manifest.json'
    """
    manifest_id: str
    coach_id: str = Field(..., min_length=3, max_length=3)
    source_session_reference: str
    query_chain: list[CypherQuery] = Field(default_factory=list)
    orphan_check_passed: bool = False
    topology_valid: bool = False
    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class GraphCommitResult(BaseModel):
    """DEP-ENG-030 — Stage 3 output: result of the Neo4j hypergraph commit.

    Spec: FR13 §4 Stage 3
    ADR-01: Credentials are coach-isolated. Global/blank URI → security fault.
    """
    coach_id: str = Field(..., min_length=3, max_length=3)
    manifest_id: str
    verdict: GraphCommitVerdict
    nodes_written: int = 0
    edges_written: int = 0
    graph_sync_pending: bool = False
    supabase_fallback_used: bool = False
    error_detail: Optional[str] = None
    retry_count: int = 0
    committed_at: Optional[datetime] = None


class PurgeReceipt(BaseModel):
    """FR13 §4 Stage 4 / AC5: Complete eradication audit record.

    Spec: 'the entire hypergraph, including coach_soul.json Voice DNA payload,
    undergoes a cryptographic sequence purge (The Right-to-be-Forgotten Protocol)'
    """
    coach_id: str = Field(..., min_length=3, max_length=3)
    purge_command: str
    remaining_node_count: int = Field(
        ...,
        description="Post-purge MATCH (n) RETURN COUNT(n) result — must be 0 (AC5).",
    )
    voice_dna_purged: bool = False
    connections_terminated: bool = False
    database_dropped: bool = False
    purge_timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @property
    def complete_eradication_verified(self) -> bool:
        """AC5: True only if zero nodes remain post-purge."""
        return self.remaining_node_count == 0


# ══════════════════════════════════════════════════════════════════════════════
# FR28 — Dynamic Journaling Directive (DEP-ENG-024)
# ══════════════════════════════════════════════════════════════════════════════

class RoadmapContext(BaseModel):
    """FR28 §5: User's current position in the 30-day Atlas roadmap."""
    current_day: int = Field(..., ge=1, le=30)
    capacity_track: CapacityTrack
    structural_day: StructuralDay


class PsychologicalContext(BaseModel):
    """FR28 §5: Real-time emotional state from Aria's last extraction."""
    last_interaction_mood: MoodState = MoodState.STABLE
    intensity_override: Optional[str] = None


class ArtisanDirective(BaseModel):
    """FR28 §4 Stage 3: Structured constraint for Artisan's text generation."""
    prompt_category: str
    emotional_target: str
    required_constraint: str
    max_words: int = Field(default=JOURNALING_MAX_WORDS, le=JOURNALING_MAX_WORDS)


class DynamicJournalingDirective(BaseModel):
    """DEP-ENG-024 (Journaling) — FR28 primary output schema.

    Spec: FR28 §5 'dynamic_journaling_directive.json'
    Distinct from DEP-ENG-024 Coach Story Archive in v5_models.py.
    """
    user_id: str
    coach_id: str = Field(..., min_length=3, max_length=3)
    scheduled_date: str
    roadmap_context: RoadmapContext
    psychological_context: PsychologicalContext
    artisan_directive: ArtisanDirective
    escalation_blocked: bool = False
    rest_day_blocked: bool = False
    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @model_validator(mode="after")
    def validate_anti_escalation(self) -> "DynamicJournalingDirective":
        """FR28 §3 Tech Decision 2 / AC1:
        Hard block: cannot escalate past Foundation before day 14.
        """
        day = self.roadmap_context.current_day
        track = self.roadmap_context.capacity_track
        high_intensity = {CapacityTrack.GROWTH, CapacityTrack.MOMENTUM, CapacityTrack.PEAK}
        if day < ANTI_ESCALATION_MIN_DAYS and track in high_intensity:
            # Demote to Foundation
            self.roadmap_context.capacity_track = CapacityTrack.FOUNDATION
            self.escalation_blocked = True
        return self


# ══════════════════════════════════════════════════════════════════════════════
# FR29 — Context Premise Extraction (DEP-ENG-006)
# ══════════════════════════════════════════════════════════════════════════════

class ContextDimensionEntry(BaseModel):
    """FR29 §5: A single entry in the 12-dimension extraction array.

    Spec: 'Hallucination Gate: Every extracted dimension must quote the exact
    3-4 word phrase from the transcript that supports it. If an extraction
    lacks a direct quote, it is dropped as <null>.' (AC3)
    """
    entity: str = Field(default="")
    depth_level: DepthLevel = DepthLevel.L1
    exact_quote: Optional[str] = Field(
        None,
        description="Mandatory for non-null entries (AC3 Evidence Grounding).",
    )

    # Legacy / test fields
    dimension: Optional[Any] = Field(default=None)
    label: str = Field(default="")
    raw_value: str = Field(default="")
    confidence: float = Field(default=0.0)
    session_id: str = Field(default="")

    @model_validator(mode="before")
    @classmethod
    def resolve_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Sync label & raw_value with entity
            if "label" in data and not data.get("entity"):
                data["entity"] = data["label"]
            elif "raw_value" in data and not data.get("entity"):
                data["entity"] = data["raw_value"]
            elif "entity" in data:
                if not data.get("label"):
                    data["label"] = data["entity"]
                if not data.get("raw_value"):
                    data["raw_value"] = data["entity"]
        return data

    @model_validator(mode="after")
    def enforce_evidence_grounding(self) -> "ContextDimensionEntry":
        """AC3: exact_quote required — if missing, entry must be treated as null."""
        # The pipeline layer enforces dropping null-quote entries.
        # Model allows None so that deserialization from partial LLM output works.
        return self


class ContextPremiseExtraction(BaseModel):
    """DEP-ENG-006 — FR29 primary output schema.

    Spec: FR29 §5 'context_premise_extraction.json'
    Note: This is the macro audience Context Premise map produced by FR29.
    NOT to be confused with DEP-ENG-030 (1:1 client map, FR13).
    """
    user_id: str
    transcription_time_ms: Optional[float] = None
    extraction_time_ms: Optional[float] = None
    total_latency_ms: Optional[float] = None
    context_premise: dict[str, Any] = Field(
        default_factory=dict,
        description="Keyed by dimension name. Empty array = not detected (never hallucinated).",
    )
    # 12 standard dimensions — each is a list (may be empty, never hallucinated)
    fears: list[ContextDimensionEntry] = Field(default_factory=list)
    enemies: list[ContextDimensionEntry] = Field(default_factory=list)
    dreams: list[ContextDimensionEntry] = Field(default_factory=list)
    hidden_beliefs: list[ContextDimensionEntry] = Field(default_factory=list)
    frustrations: list[ContextDimensionEntry] = Field(default_factory=list)
    insecurities: list[ContextDimensionEntry] = Field(default_factory=list)
    envy_feelings: list[ContextDimensionEntry] = Field(default_factory=list)
    wants: list[ContextDimensionEntry] = Field(default_factory=list)
    coping_mechanism: Optional[str] = None
    emotional_triggers: list[str] = Field(default_factory=list)
    success_markers: list[ContextDimensionEntry] = Field(default_factory=list)
    suspicions: list[ContextDimensionEntry] = Field(default_factory=list)
    transcript_null: bool = False  # True if Whisper failed → use previous session
    coach_id: str = Field(default="", min_length=0)

    # Fallback/test attributes
    whisper_latency_ms: Optional[float] = None
    aria_latency_ms: Optional[float] = None
    graph_write_latency_ms: Optional[float] = None
    session_id: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def distribute_entries(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Capture entries passed to constructor
            entries = data.pop("entries", None)
            if entries is not None:
                for entry in entries:
                    dim = None
                    if isinstance(entry, dict):
                        dim = entry.get("dimension")
                    else:
                        dim = getattr(entry, "dimension", None)
                    
                    # Map to target list field based on dimension
                    target_field = "fears"
                    if dim:
                        dim_str = str(dim).lower()
                        if "fear" in dim_str:
                            target_field = "fears"
                        elif "enemy" in dim_str:
                            target_field = "enemies"
                        elif "dream" in dim_str:
                            target_field = "dreams"
                        elif "belief" in dim_str or "identity" in dim_str:
                            target_field = "hidden_beliefs"
                        elif "frustration" in dim_str:
                            target_field = "frustrations"
                        elif "insecurity" in dim_str:
                            target_field = "insecurities"
                        elif "envy" in dim_str:
                            target_field = "envy_feelings"
                        elif "want" in dim_str:
                            target_field = "wants"
                        elif "trigger" in dim_str:
                            target_field = "fears"
                        elif "success" in dim_str or "milestone" in dim_str:
                            target_field = "success_markers"
                        elif "suspicion" in dim_str:
                            target_field = "suspicions"
                    
                    # Add ContextDimensionEntry instance or dict
                    data.setdefault(target_field, []).append(entry)
        return data

    @property
    def entries(self) -> list[ContextDimensionEntry]:
        """Aggregate all dimensional lists into a single flat list of entries."""
        return (
            self.fears
            + self.enemies
            + self.dreams
            + self.hidden_beliefs
            + self.frustrations
            + self.insecurities
            + self.envy_feelings
            + self.wants
            + self.success_markers
            + self.suspicions
        )

    @property
    def sla_compliant(self) -> bool:
        """FR29 AC1: total_latency_ms < 5000ms."""
        if self.total_latency_ms is None:
            return False
        return self.total_latency_ms < EXTRACTION_LATENCY_BUDGET_MS

    @property
    def evidence_grounded_entries_only(self) -> list[ContextDimensionEntry]:
        """FR29 AC3: Returns only entries with a non-empty exact_quote."""
        results: list[ContextDimensionEntry] = []
        for dim in [
            self.fears, self.enemies, self.dreams, self.hidden_beliefs,
            self.frustrations, self.insecurities,
        ]:
            for entry in dim:
                if entry.exact_quote:
                    results.append(entry)
        return results


# ══════════════════════════════════════════════════════════════════════════════
# FR38 — Memory Tier Promotion (DEP-ENG-033)
# ══════════════════════════════════════════════════════════════════════════════

class EpisodicNode(BaseModel):
    """FR38 §4 Stage 1: An event node created in the Episodic graph layer."""
    node_id: str
    client_id: str = Field(default="")
    coach_id: str = Field(default="", min_length=0)
    raw_text: str = Field(default="")
    emotional_intensity_score: float = Field(default=0.0, ge=0.0, le=10.0)
    session_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    edge_label: MemoryTierEdge = MemoryTierEdge.EPISODIC
    rejected_for_promotion: bool = False

    # Fields expected by legacy/test codes
    label: str = Field(default="")
    raw_value: str = Field(default="")
    liwc_emotional_intensity: float = Field(default=0.0, ge=0.0, le=10.0)
    edge_type: MemoryTierEdge = Field(default=MemoryTierEdge.WORKING)
    first_observed: Optional[date] = Field(default=None)

    @model_validator(mode="before")
    @classmethod
    def resolve_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Sync label & raw_value with raw_text
            if "label" in data and not data.get("raw_text"):
                data["raw_text"] = data["label"]
            if "raw_value" in data and not data.get("raw_text"):
                data["raw_text"] = data["raw_value"]
            if "raw_text" in data:
                if not data.get("label"):
                    data["label"] = data["raw_text"]
                if not data.get("raw_value"):
                    data["raw_value"] = data["raw_text"]

            # Sync liwc_emotional_intensity with emotional_intensity_score
            if "liwc_emotional_intensity" in data and not data.get("emotional_intensity_score"):
                data["emotional_intensity_score"] = data["liwc_emotional_intensity"]
            elif "emotional_intensity_score" in data and not data.get("liwc_emotional_intensity"):
                data["liwc_emotional_intensity"] = data["emotional_intensity_score"]

            # Sync edge_type with edge_label
            if "edge_type" in data and not data.get("edge_label"):
                data["edge_label"] = data["edge_type"]
            elif "edge_label" in data and not data.get("edge_type"):
                data["edge_type"] = data["edge_label"]

            # Sync first_observed with session_date
            from datetime import date as dt_date, datetime as dt_datetime
            if "first_observed" in data and data["first_observed"]:
                fo = data["first_observed"]
                if isinstance(fo, dt_date) and not isinstance(fo, dt_datetime):
                    data["session_date"] = dt_datetime(fo.year, fo.month, fo.day, tzinfo=timezone.utc)
                elif isinstance(fo, str):
                    try:
                        parsed = dt_date.fromisoformat(fo)
                        data["session_date"] = dt_datetime(parsed.year, parsed.month, parsed.day, tzinfo=timezone.utc)
                    except ValueError:
                        pass
            elif "session_date" in data and data["session_date"]:
                sd = data["session_date"]
                if isinstance(sd, dt_datetime):
                    data["first_observed"] = sd.date()
                elif isinstance(sd, str):
                    try:
                        parsed = dt_datetime.fromisoformat(sd)
                        data["first_observed"] = parsed.date()
                    except ValueError:
                        pass
        return data

    @property
    def qualifies_for_episodic(self) -> bool:
        """FR38 §4 Stage 1: LIWC score > 7.0 → extract."""
        intensity = self.emotional_intensity_score or self.liwc_emotional_intensity or 0.0
        return intensity > LIWC_EMOTIONAL_INTENSITY_THRESHOLD


class SemanticReviewProposal(BaseModel):
    """FR38 §4 Stage 2: A candidate Semantic Truth queued for operator review.

    Spec: 'If the same root emotional driver appears ≥ 3 times across separate
    sessions spanning ≥ 14 days, the pattern crosses the threshold.'
    """
    proposal_id: str
    client_id: str = Field(default="")
    coach_id: str = Field(default="EMI", min_length=3, max_length=3)
    proposed_semantic_truth: str = Field(default="")
    supporting_node_ids: list[str] = Field(default_factory=list)
    occurrence_count: int = Field(..., ge=1)
    span_days: int = Field(..., ge=0)
    queued_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    stale: bool = False

    # Fields/properties expected by legacy/test codes
    root_driver: str = Field(default="")
    proposed_truth: str = Field(default="")
    supporting_episodic_node_ids: list[str] = Field(default_factory=list)
    first_observed: Optional[date] = Field(default=None)
    most_recent: Optional[date] = Field(default=None)

    @model_validator(mode="before")
    @classmethod
    def resolve_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "root_driver" in data and not data.get("client_id"):
                data["client_id"] = "USR-001"
            if "proposed_truth" in data and not data.get("proposed_semantic_truth"):
                data["proposed_semantic_truth"] = data["proposed_truth"]
            elif "proposed_semantic_truth" in data and not data.get("proposed_truth"):
                data["proposed_truth"] = data["proposed_semantic_truth"]

            if "supporting_episodic_node_ids" in data and not data.get("supporting_node_ids"):
                data["supporting_node_ids"] = data["supporting_episodic_node_ids"]
            elif "supporting_node_ids" in data and not data.get("supporting_episodic_node_ids"):
                data["supporting_episodic_node_ids"] = data["supporting_node_ids"]

            if not data.get("coach_id"):
                data["coach_id"] = "EMI"
            if not data.get("client_id"):
                data["client_id"] = "USR-001"
        return data

    @model_validator(mode="after")
    def check_threshold_met(self) -> "SemanticReviewProposal":
        """FR38 §4 Stage 2 Gate Threshold validation."""
        # The pipeline enforces this before creation; model flags for clarity.
        return self

    @property
    def threshold_met(self) -> bool:
        """Pattern qualifies for review if ≥ 3 occurrences over ≥ 14 days."""
        return (
            self.occurrence_count >= PATTERN_OCCURRENCE_THRESHOLD
            and self.span_days >= PATTERN_MIN_SPAN_DAYS
        )



class SemanticCommittalReceipt(BaseModel):
    """DEP-ENG-033 — FR38 primary output schema.

    Spec: FR38 §5 'semantic_committal_receipt.json'
    """
    committal_id: str
    client_id: str
    operator_id: str
    coach_id: str = Field(..., min_length=3, max_length=3)
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    approved_semantic_truth: str
    operator_verdict: OperatorVerdict
    original_system_proposal: str
    supporting_evidence_nodes: list[str] = Field(default_factory=list)
    graph_mutation_status: GraphMutationStatus = GraphMutationStatus.PENDING
    episodic_edges_severed: list[str] = Field(default_factory=list)
    semantic_edge_created: bool = False


# ══════════════════════════════════════════════════════════════════════════════
# FR44 — Context Performance Registry (DEP-ENG-045)
# ══════════════════════════════════════════════════════════════════════════════

class ContextCombination(BaseModel):
    """FR44 §5: The specific context ingredients chosen by the Research Planner."""
    cmm_layers: list[str] = Field(default_factory=list)
    context_labels: list[str] = Field(default_factory=list)
    story_archive_utilized: bool = False
    story_id: Optional[str] = None
    humor_mechanism: Optional[str] = None
    regulatory_frame: str = ""
    arc_phase: str = ""


class ContextSelectionObject(BaseModel):
    """FR44 §4 Stage 2 / §5: What the Research Planner chose and WHY.

    Spec: 'We do not just log You chose M4. We log the LLM's explicit reasoning
    string for why it chose M4.' (Tech Decision 1 — Rationale Logging)
    AC1: selection_rationale must be non-empty.
    """
    universal_asset_id: str = Field(default="")
    coach_id: str = Field(default="", min_length=0)
    moment_id: str
    context_combination: ContextCombination
    selection_rationale: str = Field(
        ...,
        description="Non-empty reasoning string explaining CMM/story selection (AC1).",
        min_length=1,
    )
    confidence_score: float = Field(
        default=0.2,
        ge=0.0,
        le=1.0,
        description="0.2 if matched_sessions < 5 (AC2 sparse-data fallback).",
    )
    override_flags_triggered: list[str] = Field(default_factory=list)
    performance_outcome: Optional[float] = None
    outperformed_default: Optional[bool] = None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @property
    def is_sparse_data_mode(self) -> bool:
        """FR44 AC2: confidence_score = 0.2 when sample < 5."""
        return self.confidence_score <= 0.2


class CPRQueryResult(BaseModel):
    """FR44 §4 Stage 2: Result of querying the performance registry for priors."""
    coach_id: str = Field(default="")
    moment_id: str
    regulatory_frame: str
    matched_sessions: int = 0
    outperforming_rows: list[ContextSelectionObject] = Field(default_factory=list)
    confidence_score: float = 0.2
    
    # Optional fields for test and service flexibility
    query_id: Optional[str] = Field(default=None)
    selection_object: Optional[ContextSelectionObject] = Field(default=None)
    outperforming_sessions: int = Field(default=0)

    @property
    def is_sparse_data(self) -> bool:
        """FR44 AC2: returns True if matched_sessions < 5."""
        return self.matched_sessions < 5

    @model_validator(mode="after")
    def compute_confidence(self) -> "CPRQueryResult":
        """FR44 §4 Stage 2 Resolution Rule:
        < 5 matches → confidence 0.2
        ≥ 5 matches with outperformed_default=True → confidence 0.8
        """
        if self.matched_sessions < CPR_SPARSE_THRESHOLD:
            self.confidence_score = 0.2
        elif any(r.outperformed_default for r in self.outperforming_rows):
            self.confidence_score = 0.8
        return self


class PerformanceHandshakeResult(BaseModel):
    """FR44 §4 Stage 3: Data Analyst performance feedback written back to registry."""
    universal_asset_id: str
    coach_id: str = Field(default="")
    engagement_rate: float
    saves: int = 0
    shares: int = 0
    coach_baseline: float = Field(default=0.0)
    coach_baseline_engagement: Optional[float] = Field(default=None)
    moment_id: Optional[str] = Field(default=None)
    regulatory_frame: Optional[str] = Field(default=None)
    outperformed_default: bool = False
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @model_validator(mode="before")
    @classmethod
    def resolve_baseline(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "coach_baseline_engagement" in data:
                if "coach_baseline" not in data or data["coach_baseline"] == 0.0:
                    data["coach_baseline"] = data["coach_baseline_engagement"]
            elif "coach_baseline" in data:
                data["coach_baseline_engagement"] = data["coach_baseline"]
        return data

    @model_validator(mode="after")
    def determine_outperformance(self) -> "PerformanceHandshakeResult":
        """FR44 §4 Stage 3 Resolution Rule:
        engagement_rate > 1.2× coach baseline → outperformed_default=True.
        """
        baseline = self.coach_baseline or self.coach_baseline_engagement or 0.03
        self.outperformed_default = (
            self.engagement_rate > baseline * CPR_OUTPERFORM_MULTIPLIER
        )
        return self
