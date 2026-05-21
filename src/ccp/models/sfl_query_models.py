"""
CCP FR-ERA3-26 - Subliminal Function Query and Profile Service models.

Typed contracts for bounded SFL lookup, deterministic profile assembly,
warnings, conflict reporting, and runtime stack packets.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


SFL_QUERY_AUDIT_SQL = """
CREATE TABLE IF NOT EXISTS sfl_query_audit (
    audit_id             TEXT PRIMARY KEY,
    action_type          TEXT NOT NULL,
    query_mode           TEXT NOT NULL,
    request_payload      JSONB NOT NULL,
    response_summary     JSONB NOT NULL,
    evidence_trace       JSONB NOT NULL DEFAULT '[]',
    warning_payload      JSONB NOT NULL DEFAULT '[]',
    conflict_payload     JSONB NOT NULL DEFAULT '[]',
    cache_hit            BOOLEAN NOT NULL DEFAULT TRUE,
    latency_ms           REAL NOT NULL,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_sfl_query_audit_mode
    ON sfl_query_audit(query_mode);
CREATE INDEX IF NOT EXISTS idx_sfl_query_audit_created_at
    ON sfl_query_audit(created_at DESC);
"""


SFL_FAMILY_ID_PATTERN = r"^SFL-FAM-\d{3}$"
SFL_FUNCTION_ID_PATTERN = r"^SFL-FN-\d{3}$"
PRIMITIVE_ID_PATTERN = r"^(EXP|PRM)-[A-Z]{3}-\d{3}$"
REP_GEOMETRY_ID_PATTERN = r"^SDA-RPG-\d{3}$"


class SFLQueryMode(str, Enum):
    BY_FAMILY = "by_family"
    BY_FUNCTION_ID = "by_function_id"
    BY_PRIMITIVE_CROSSWALK = "by_primitive_crosswalk"
    BY_REPRESENTATION_GEOMETRY = "by_representation_geometry"
    BY_ARCHETYPE_PROFILE = "by_archetype_profile"
    BY_SURFACE_PROFILE = "by_surface_profile"


class SFLAssemblyStatus(str, Enum):
    RESOLVED = "resolved"
    FAMILY_ONLY = "family_only"
    PARTIAL = "partial"
    REVIEW_REQUIRED = "review_required"
    UNRESOLVED = "unresolved"


class ProfileEvidenceKind(str, Enum):
    EXPLICIT_FUNCTION = "explicit_function"
    SURFACE_CONSTRAINT_PROFILE = "surface_constraint_profile"
    ARCHETYPE_PROFILE = "archetype_profile"
    REPRESENTATION_GEOMETRY_PROFILE = "representation_geometry_profile"
    PRIMITIVE_CROSSWALK = "primitive_crosswalk"
    FAMILY_DEFAULT = "family_default"


class FunctionSelectionSource(str, Enum):
    EXPLICIT_OVERRIDE = "explicit_override"
    REQUIRED_BY_SURFACE = "required_by_surface"
    PREFERRED_BY_SURFACE = "preferred_by_surface"
    PREFERRED_BY_ARCHETYPE = "preferred_by_archetype"
    REQUIRED_BY_ARCHETYPE = "required_by_archetype"
    PREFERRED_BY_GEOMETRY = "preferred_by_geometry"
    HINTED_BY_PRIMITIVE = "hinted_by_primitive"
    FALLBACK_FROM_FAMILY = "fallback_from_family"


class SFLQueryWarningCode(str, Enum):
    FAMILY_ONLY_FALLBACK = "family_only_fallback"
    PARTIAL_CROSSWALK_EVIDENCE = "partial_crosswalk_evidence"
    CONFLICT_REQUIRES_REVIEW = "conflict_requires_review"
    UNKNOWN_PRIMITIVE_REFERENCE = "unknown_primitive_reference"
    UNKNOWN_GEOMETRY_REFERENCE = "unknown_geometry_reference"
    SURFACE_CONSTRAINT_REMOVED_FUNCTION = "surface_constraint_removed_function"
    EXPLICIT_OVERRIDE_DISCOURAGED = "explicit_override_discouraged"


class DeliverySurfaceKind(str, Enum):
    TELEGRAM = "telegram"
    CAROUSEL = "carousel"
    SHORT_FORM_VIDEO = "short_form_video"
    LONG_FORM_VIDEO = "long_form_video"
    WEBINAR = "webinar"
    COMMERCIAL = "commercial"
    AUDIT = "audit"


class SFLVersionStamp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    manifest_version: str = Field(min_length=1)
    manifest_hash: str = Field(min_length=8)
    registry_hash: str | None = Field(default=None, min_length=8)


class SFLQueryWarning(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: SFLQueryWarningCode
    message: str = Field(min_length=3)
    evidence_ref: str | None = None


class FunctionProfileEvidenceRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    evidence_kind: ProfileEvidenceKind
    source_artifact_id: str = Field(min_length=3)
    source_label: str = Field(min_length=3)
    affected_family_ids: list[str] = Field(default_factory=list)
    affected_function_ids: list[str] = Field(default_factory=list)
    rationale: str = Field(min_length=3)
    precedence_rank: int = Field(ge=1, le=6)

    @field_validator("affected_family_ids", mode="before")
    @classmethod
    def normalize_family_ids(cls, value: Any) -> list[str]:
        return _normalize_unique_str_list(value)

    @field_validator("affected_function_ids", mode="before")
    @classmethod
    def normalize_function_ids(cls, value: Any) -> list[str]:
        return _normalize_unique_str_list(value)

    @model_validator(mode="after")
    def validate_references(self) -> "FunctionProfileEvidenceRecord":
        for family_id in self.affected_family_ids:
            if not _matches_pattern(family_id, SFL_FAMILY_ID_PATTERN):
                raise ValueError(f"Invalid family reference: {family_id}")
        for function_id in self.affected_function_ids:
            if not _matches_pattern(function_id, SFL_FUNCTION_ID_PATTERN):
                raise ValueError(f"Invalid function reference: {function_id}")
        return self


class ResolvedFunctionRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    function_id: str = Field(pattern=SFL_FUNCTION_ID_PATTERN)
    canonical_name: str = Field(min_length=3)
    family_id: str = Field(pattern=SFL_FAMILY_ID_PATTERN)
    selection_source: FunctionSelectionSource
    rationale: str = Field(min_length=3)


class ResolvedFamilyRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    family_id: str = Field(pattern=SFL_FAMILY_ID_PATTERN)
    canonical_name: str = Field(min_length=3)
    rationale: str = Field(min_length=3)


class ProfileConflictRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    conflict_id: str = Field(min_length=3)
    higher_priority_evidence_ref: str = Field(min_length=3)
    lower_priority_evidence_ref: str = Field(min_length=3)
    conflict_scope: Literal["family", "function", "surface_rule", "archetype_rule", "geometry_rule"]
    affected_function_ids: list[str] = Field(default_factory=list)
    resolution: Literal["suppressed_lower_priority", "downgraded_to_family_only", "review_required"]
    rationale: str = Field(min_length=3)

    @field_validator("affected_function_ids", mode="before")
    @classmethod
    def normalize_function_ids(cls, value: Any) -> list[str]:
        return _normalize_unique_str_list(value)

    @model_validator(mode="after")
    def validate_function_ids(self) -> "ProfileConflictRecord":
        for function_id in self.affected_function_ids:
            if not _matches_pattern(function_id, SFL_FUNCTION_ID_PATTERN):
                raise ValueError(f"Invalid function reference: {function_id}")
        return self


class SubliminalFunctionProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profile_id: str = Field(min_length=3)
    status: SFLAssemblyStatus
    resolved_families: list[ResolvedFamilyRecord] = Field(default_factory=list)
    resolved_functions: list[ResolvedFunctionRecord] = Field(default_factory=list)
    suppressed_function_ids: list[str] = Field(default_factory=list)
    evidence_trace: list[FunctionProfileEvidenceRecord] = Field(default_factory=list)
    conflicts: list[ProfileConflictRecord] = Field(default_factory=list)
    warnings: list[SFLQueryWarning] = Field(default_factory=list)

    @field_validator("suppressed_function_ids", mode="before")
    @classmethod
    def normalize_suppressed_function_ids(cls, value: Any) -> list[str]:
        return _normalize_unique_str_list(value)

    @model_validator(mode="after")
    def validate_suppressed_ids(self) -> "SubliminalFunctionProfile":
        for function_id in self.suppressed_function_ids:
            if not _matches_pattern(function_id, SFL_FUNCTION_ID_PATTERN):
                raise ValueError(f"Invalid suppressed function reference: {function_id}")
        return self


class SubliminalFunctionStackPacket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    packet_id: str = Field(min_length=3)
    coach_id: str | None = None
    content_archetype: str | None = None
    representation_geometry_id: str | None = Field(default=None, pattern=REP_GEOMETRY_ID_PATTERN)
    delivery_surface: DeliverySurfaceKind
    status: SFLAssemblyStatus
    active_family_ids: list[str] = Field(default_factory=list)
    active_function_ids: list[str] = Field(default_factory=list)
    suppressed_function_ids: list[str] = Field(default_factory=list)
    evidence_trace: list[FunctionProfileEvidenceRecord] = Field(default_factory=list)
    version_stamp: SFLVersionStamp
    lineage: dict[str, str] = Field(default_factory=dict)
    warnings: list[SFLQueryWarning] = Field(default_factory=list)

    @field_validator("active_family_ids", "active_function_ids", "suppressed_function_ids", mode="before")
    @classmethod
    def normalize_id_lists(cls, value: Any) -> list[str]:
        return _normalize_unique_str_list(value)

    @model_validator(mode="after")
    def validate_ids(self) -> "SubliminalFunctionStackPacket":
        for family_id in self.active_family_ids:
            if not _matches_pattern(family_id, SFL_FAMILY_ID_PATTERN):
                raise ValueError(f"Invalid active family reference: {family_id}")
        for function_id in self.active_function_ids + self.suppressed_function_ids:
            if not _matches_pattern(function_id, SFL_FUNCTION_ID_PATTERN):
                raise ValueError(f"Invalid function reference: {function_id}")
        return self


class SubliminalFunctionQueryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query_mode: SFLQueryMode
    family_id: str | None = Field(default=None, pattern=SFL_FAMILY_ID_PATTERN)
    function_id: str | None = Field(default=None, pattern=SFL_FUNCTION_ID_PATTERN)
    primitive_id: str | None = Field(default=None, pattern=PRIMITIVE_ID_PATTERN)
    representation_geometry_id: str | None = Field(default=None, pattern=REP_GEOMETRY_ID_PATTERN)
    archetype_name: str | None = None
    delivery_surface: DeliverySurfaceKind | None = None
    include_functions: bool = True
    include_crosswalk_evidence: bool = True

    @model_validator(mode="after")
    def validate_target(self) -> "SubliminalFunctionQueryRequest":
        required_by_mode = {
            SFLQueryMode.BY_FAMILY: self.family_id,
            SFLQueryMode.BY_FUNCTION_ID: self.function_id,
            SFLQueryMode.BY_PRIMITIVE_CROSSWALK: self.primitive_id,
            SFLQueryMode.BY_REPRESENTATION_GEOMETRY: self.representation_geometry_id,
            SFLQueryMode.BY_ARCHETYPE_PROFILE: self.archetype_name,
            SFLQueryMode.BY_SURFACE_PROFILE: self.delivery_surface,
        }
        if not required_by_mode[self.query_mode]:
            raise ValueError(f"Missing required target for query_mode={self.query_mode.value}")
        return self


class SubliminalFunctionQueryResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query_id: str = Field(min_length=3)
    query_mode: SFLQueryMode
    ready: bool
    resolved_families: list[ResolvedFamilyRecord] = Field(default_factory=list)
    resolved_functions: list[ResolvedFunctionRecord] = Field(default_factory=list)
    evidence_trace: list[FunctionProfileEvidenceRecord] = Field(default_factory=list)
    warnings: list[SFLQueryWarning] = Field(default_factory=list)
    version_stamp: SFLVersionStamp
    cache_hit: bool
    latency_ms: float = Field(ge=0.0)


class FunctionProfileAssemblyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    coach_id: str | None = None
    content_archetype: str | None = None
    delivery_surface: DeliverySurfaceKind
    representation_geometry_id: str | None = Field(default=None, pattern=REP_GEOMETRY_ID_PATTERN)
    primitive_ids: list[str] = Field(default_factory=list)
    explicit_function_ids: list[str] = Field(default_factory=list)
    explicit_family_ids: list[str] = Field(default_factory=list)
    allow_family_only_fallback: bool = True
    require_complete_crosswalks: bool = False

    @field_validator("primitive_ids", "explicit_function_ids", "explicit_family_ids", mode="before")
    @classmethod
    def normalize_lists(cls, value: Any) -> list[str]:
        return _normalize_unique_str_list(value)

    @model_validator(mode="after")
    def validate_ids(self) -> "FunctionProfileAssemblyRequest":
        for primitive_id in self.primitive_ids:
            if not _matches_pattern(primitive_id, PRIMITIVE_ID_PATTERN):
                raise ValueError(f"Invalid primitive id: {primitive_id}")
        for function_id in self.explicit_function_ids:
            if not _matches_pattern(function_id, SFL_FUNCTION_ID_PATTERN):
                raise ValueError(f"Invalid explicit function id: {function_id}")
        for family_id in self.explicit_family_ids:
            if not _matches_pattern(family_id, SFL_FAMILY_ID_PATTERN):
                raise ValueError(f"Invalid explicit family id: {family_id}")
        return self


class FunctionProfileAssemblyResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str = Field(min_length=3)
    status: SFLAssemblyStatus
    profile: SubliminalFunctionProfile
    stack_packet: SubliminalFunctionStackPacket | None = None
    warnings: list[SFLQueryWarning] = Field(default_factory=list)
    conflicts: list[ProfileConflictRecord] = Field(default_factory=list)
    version_stamp: SFLVersionStamp
    cache_hit: bool
    latency_ms: float = Field(ge=0.0)

    @model_validator(mode="after")
    def validate_packet_status(self) -> "FunctionProfileAssemblyResult":
        if self.stack_packet is not None and self.stack_packet.status != self.status:
            raise ValueError("stack_packet.status must match assembly result status")
        if self.profile.status != self.status:
            raise ValueError("profile.status must match assembly result status")
        return self


def _normalize_unique_str_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        value = [value]
    normalized: list[str] = []
    seen: set[str] = set()
    for item in value:
        item_str = str(item).strip()
        if not item_str or item_str in seen:
            continue
        seen.add(item_str)
        normalized.append(item_str)
    return normalized


def _matches_pattern(value: str, pattern: str) -> bool:
    import re

    return re.match(pattern, value) is not None
