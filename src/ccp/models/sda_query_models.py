from __future__ import annotations

from enum import Enum
from typing import Literal
from pydantic import BaseModel, Field


SDA_QUERY_AUDIT_SQL = """
CREATE TABLE IF NOT EXISTS sda_query_audit (
    audit_id              TEXT PRIMARY KEY,
    action_type           TEXT NOT NULL,
    queryable_surface     TEXT NOT NULL,
    request_payload       JSONB NOT NULL,
    response_summary      JSONB NOT NULL,
    provenance_bundle     JSONB NOT NULL,
    used_stale_fallback   BOOLEAN NOT NULL DEFAULT FALSE,
    fallback_reason       TEXT,
    latency_ms            REAL NOT NULL,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""

# Cache key constants
SDA_CACHE_KEY_INV = "sda:inv:{id}"
SDA_CACHE_KEY_RPG = "sda:rpg:{id}"
SDA_CACHE_KEY_ARG = "sda:arg:{id}"
SDA_CACHE_KEY_SCG = "sda:scg:{id}"
SDA_CACHE_KEY_XW_PRI = "sda:xw:pri:{id}"
SDA_CACHE_KEY_XW_ATG = "sda:xw:atg:{id}"
SDA_CACHE_KEY_XW_ETS = "sda:xw:ets:{id}"


class SDAQueryableSurface(str, Enum):
    EXISTENTIAL_INVARIANT = "existential_invariant"
    REPRESENTATION_GEOMETRY = "representation_geometry"
    ARCHETYPAL_GEOMETRY = "archetypal_geometry"
    SPECIES_COMPOSITION_GRAMMAR = "species_composition_grammar"
    PRIMITIVE_TO_INVARIANT = "primitive_to_invariant_crosswalk"
    ARCHETYPE_TO_GEOMETRY = "archetype_to_geometry_crosswalk"
    EDGE_TO_SPECIES = "edge_to_species_crosswalk"


class SDAResolutionStatus(str, Enum):
    RESOLVED = "resolved"
    PARTIAL = "partial"
    NOT_FOUND = "not_found"
    REJECTED_NON_CANONICAL = "rejected_non_canonical"


class SDAFallbackReason(str, Enum):
    NONE = "none"
    STALE_CACHE = "stale_cache"
    DOWNSTREAM_PRIMITIVE_UNAVAILABLE = "downstream_primitive_unavailable"
    MANIFEST_MISMATCH = "manifest_mismatch"


class SDAProvenanceBlock(BaseModel):
    registry_surface: SDAQueryableSurface
    source_file: str
    source_version: str
    source_hash: str
    loaded_at: str
    registry_manifest_hash: str
    supporting_refs: list[str] = Field(default_factory=list)


class ExistentialInvariantRecord(BaseModel):
    invariant_id: str
    canonical_name: str
    definition: str
    invariant_gravity: float = Field(ge=0.0, le=1.0)
    tension_poles: list[str] = Field(default_factory=list)
    distortion_modes: list[str] = Field(default_factory=list)
    provenance: SDAProvenanceBlock


class RepresentationGeometryRecord(BaseModel):
    geometry_id: str
    canonical_name: str
    authority_structure: str
    identity_framing: str
    fear_weighting: float = Field(ge=0.0, le=1.0)
    drift_risks: list[str] = Field(default_factory=list)
    provenance: SDAProvenanceBlock


class ArchetypalGeometryRecord(BaseModel):
    geometry_id: str
    canonical_name: str
    definition: str
    authority_flow: str
    agency_distribution: str
    transformation_pattern: str
    provenance: SDAProvenanceBlock


class SpeciesCompositionRuleRecord(BaseModel):
    rule_id: str
    canonical_name: str
    admissible_bindings: list[str] = Field(default_factory=list)
    forbidden_pairings: list[str] = Field(default_factory=list)
    instability_triggers: list[str] = Field(default_factory=list)
    provenance: SDAProvenanceBlock


class PrimitiveReference(BaseModel):
    primitive_id: str
    primitive_plane: Literal["experience", "meaning"]
    canonical_name: str | None = None
    family: str | None = None


class PrimitiveInvariantCandidate(BaseModel):
    invariant_id: str
    rationale: str
    confidence: float = Field(ge=0.0, le=1.0)
    crosswalk_id: str
    provenance: SDAProvenanceBlock


class PrimitiveInvariantResolutionResult(BaseModel):
    status: SDAResolutionStatus
    primitive: PrimitiveReference
    invariant_candidates: list[PrimitiveInvariantCandidate] = Field(default_factory=list)
    used_stale_fallback: bool = False
    fallback_reason: SDAFallbackReason = SDAFallbackReason.NONE


class ArchetypeGeometryCandidate(BaseModel):
    archetype_id: str
    archetype_label: str
    geometry_id: str
    rationale: str
    carrier_strength: float = Field(ge=0.0, le=1.0)
    crosswalk_id: str
    provenance: SDAProvenanceBlock


class ArchetypeGeometryResolutionResult(BaseModel):
    status: SDAResolutionStatus
    candidates: list[ArchetypeGeometryCandidate] = Field(default_factory=list)
    used_stale_fallback: bool = False
    fallback_reason: SDAFallbackReason = SDAFallbackReason.NONE


class EdgeProductReference(BaseModel):
    edge_product_id: str
    edge_label: str
    coalition_signature_id: str | None = None
    invariant_field_id: str | None = None


class EdgeSpeciesCandidate(BaseModel):
    species_reference_id: str
    species_label: str
    composition_rule_id: str
    rationale: str
    confidence: float = Field(ge=0.0, le=1.0)
    canonical_species_record_exists: bool = False
    crosswalk_id: str
    provenance: SDAProvenanceBlock


class EdgeSpeciesResolutionResult(BaseModel):
    status: SDAResolutionStatus
    edge_product: EdgeProductReference
    species_candidates: list[EdgeSpeciesCandidate] = Field(default_factory=list)
    note: str = Field(
        default="Content Species are derived semantic forms. This service returns maintained candidate references, not canonical species rows."
    )
    used_stale_fallback: bool = False
    fallback_reason: SDAFallbackReason = SDAFallbackReason.NONE


class SDAQueryableSurfaceManifest(BaseModel):
    canonical_surfaces: list[SDAQueryableSurface]
    maintained_crosswalk_surfaces: list[SDAQueryableSurface]
    rejected_runtime_surfaces: list[str]
    sibling_service_dependencies: list[str]
    manifest_hash: str


class SDAHealthStatus(BaseModel):
    cached_surfaces: dict[str, int]
    registry_manifest_hash: str
    stale_surfaces: list[str] = Field(default_factory=list)
    primitive_service_reachable: bool
    last_warm_at: str
