"""
CCP FR-ERA3-26 - Subliminal Function Query and Profile Service.

Deterministic runtime lookup and profile assembly service for the
Subliminal Function Layer. Consumes canonical FR-ERA3-25 registry state,
reads primitive and SDA evidence through their dedicated services, and
fails closed on missing or conflicting crosswalk evidence.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.primitive_registry_models import PrimitivePlane, PrimitiveRecord
from src.ccp.models.sda_registry_models import RepresentationGeometryRecord
from src.ccp.models.sfl_query_models import (
    DeliverySurfaceKind,
    FunctionProfileAssemblyRequest,
    FunctionProfileAssemblyResult,
    FunctionProfileEvidenceRecord,
    FunctionSelectionSource,
    ProfileConflictRecord,
    ProfileEvidenceKind,
    ResolvedFamilyRecord,
    ResolvedFunctionRecord,
    SFLAssemblyStatus,
    SFLQueryMode,
    SFLQueryWarning,
    SFLQueryWarningCode,
    SFLVersionStamp,
    SubliminalFunctionProfile,
    SubliminalFunctionQueryRequest,
    SubliminalFunctionQueryResponse,
    SubliminalFunctionStackPacket,
)
from src.ccp.models.sfl_registry_models import (
    ArchetypeToFunctionProfileRecord,
    PrimitiveToFunctionFamilyCrosswalkRecord,
    RepresentationGeometryToFunctionProfileRecord,
    SubliminalFunctionDefinitionRecord,
    SubliminalFunctionFamilyRecord,
    SurfaceConstraintProfileRecord,
)
from src.ccp.services.primitive_registry_service import PrimitiveRegistryQueryService
from src.ccp.services.sda_registry_service import SDARegistryService
from src.ccp.services.sfl_registry_service import SFLRegistryService


STAGE_STARTUP_WARM = "SFL26_STARTUP_WARM"
STAGE_QUERY_LOOKUP = "SFL26_QUERY_LOOKUP"
STAGE_PROFILE_ASSEMBLY = "SFL26_PROFILE_ASSEMBLY"
STAGE_DEGRADED_FALLBACK = "SFL26_DEGRADED_FALLBACK"
STAGE_CONFLICT = "SFL26_CONFLICT"
STAGE_CACHE_REBUILD = "SFL26_CACHE_REBUILD"
STAGE_RELOAD_FAILURE = "SFL26_RELOAD_FAILURE"

MAX_ACTIVE_FUNCTIONS = 4

EVIDENCE_PRECEDENCE = {
    ProfileEvidenceKind.EXPLICIT_FUNCTION: 1,
    ProfileEvidenceKind.SURFACE_CONSTRAINT_PROFILE: 2,
    ProfileEvidenceKind.ARCHETYPE_PROFILE: 3,
    ProfileEvidenceKind.REPRESENTATION_GEOMETRY_PROFILE: 4,
    ProfileEvidenceKind.PRIMITIVE_CROSSWALK: 5,
    ProfileEvidenceKind.FAMILY_DEFAULT: 6,
}


@dataclass(slots=True)
class _CacheSnapshot:
    ready: bool
    version_stamp: SFLVersionStamp
    last_warm_at: str
    index_build_count: int
    family_order: list[str]
    families: dict[str, SubliminalFunctionFamilyRecord]
    functions: dict[str, SubliminalFunctionDefinitionRecord]
    primitive_crosswalks: dict[str, PrimitiveToFunctionFamilyCrosswalkRecord]
    geometry_crosswalks: dict[str, RepresentationGeometryToFunctionProfileRecord]
    archetype_crosswalks: dict[str, ArchetypeToFunctionProfileRecord]
    surface_profiles: dict[str, SurfaceConstraintProfileRecord]
    family_to_function_ids: dict[str, list[str]]
    primitive_to_crosswalk_ids: dict[str, list[str]]
    geometry_to_crosswalk_ids: dict[str, list[str]]
    archetype_to_crosswalk_ids: dict[str, list[str]]
    surface_to_profile_id: dict[DeliverySurfaceKind, str]


@dataclass(slots=True)
class _SelectedFunction:
    function: SubliminalFunctionDefinitionRecord
    source: FunctionSelectionSource
    rationale: str
    evidence_ref: str
    precedence_rank: int


class SFLQueryCacheManager:
    """In-process mirror and deterministic query indexes for FR-ERA3-26."""

    def __init__(self, registry_service: SFLRegistryService) -> None:
        self.registry_service = registry_service
        self.ready = False
        self.version_stamp = SFLVersionStamp(manifest_version="unknown", manifest_hash="0" * 8, registry_hash="0" * 8)
        self.last_warm_at = ""
        self.index_build_count = 0

        self.family_order: list[str] = []
        self.families: dict[str, SubliminalFunctionFamilyRecord] = {}
        self.functions: dict[str, SubliminalFunctionDefinitionRecord] = {}
        self.primitive_crosswalks: dict[str, PrimitiveToFunctionFamilyCrosswalkRecord] = {}
        self.geometry_crosswalks: dict[str, RepresentationGeometryToFunctionProfileRecord] = {}
        self.archetype_crosswalks: dict[str, ArchetypeToFunctionProfileRecord] = {}
        self.surface_profiles: dict[str, SurfaceConstraintProfileRecord] = {}

        self.family_to_function_ids: dict[str, list[str]] = {}
        self.primitive_to_crosswalk_ids: dict[str, list[str]] = {}
        self.geometry_to_crosswalk_ids: dict[str, list[str]] = {}
        self.archetype_to_crosswalk_ids: dict[str, list[str]] = {}
        self.surface_to_profile_id: dict[DeliverySurfaceKind, str] = {}

    def warm_from_registry(self) -> bool:
        report = self.registry_service.health()
        if not report.ready:
            return False

        families = {key: value.model_copy(deep=True) for key, value in self.registry_service.families.items()}
        functions = {key: value.model_copy(deep=True) for key, value in self.registry_service.functions.items()}
        primitive_crosswalks = {
            key: value.model_copy(deep=True) for key, value in self.registry_service.primitive_crosswalks.items()
        }
        geometry_crosswalks = {
            key: value.model_copy(deep=True) for key, value in self.registry_service.geometry_crosswalks.items()
        }
        archetype_crosswalks = {
            key: value.model_copy(deep=True) for key, value in self.registry_service.archetype_crosswalks.items()
        }
        surface_profiles = {
            key: value.model_copy(deep=True) for key, value in self.registry_service.surface_profiles.items()
        }

        family_to_function_ids: dict[str, list[str]] = {family_id: [] for family_id in families}
        for function_id, function in functions.items():
            family_to_function_ids.setdefault(function.family_id, []).append(function_id)
        for family_id in family_to_function_ids:
            family_to_function_ids[family_id] = sorted(family_to_function_ids[family_id])

        primitive_to_crosswalk_ids: dict[str, list[str]] = {}
        for crosswalk_id, crosswalk in primitive_crosswalks.items():
            for link in crosswalk.primitive_links:
                primitive_to_crosswalk_ids.setdefault(link.primitive_id, []).append(crosswalk_id)
        for primitive_id in primitive_to_crosswalk_ids:
            primitive_to_crosswalk_ids[primitive_id] = sorted(primitive_to_crosswalk_ids[primitive_id])

        geometry_to_crosswalk_ids: dict[str, list[str]] = {}
        for crosswalk_id, crosswalk in geometry_crosswalks.items():
            for link in crosswalk.geometry_links:
                geometry_to_crosswalk_ids.setdefault(link.geometry_id, []).append(crosswalk_id)
        for geometry_id in geometry_to_crosswalk_ids:
            geometry_to_crosswalk_ids[geometry_id] = sorted(geometry_to_crosswalk_ids[geometry_id])

        archetype_to_crosswalk_ids: dict[str, list[str]] = {}
        for crosswalk_id, crosswalk in archetype_crosswalks.items():
            for link in crosswalk.archetype_links:
                archetype_key = self._normalize_archetype(link.archetype_name)
                archetype_to_crosswalk_ids.setdefault(archetype_key, []).append(crosswalk_id)
        for archetype_key in archetype_to_crosswalk_ids:
            archetype_to_crosswalk_ids[archetype_key] = sorted(archetype_to_crosswalk_ids[archetype_key])

        surface_to_profile_id: dict[DeliverySurfaceKind, str] = {}
        for profile_id, profile in surface_profiles.items():
            surface_to_profile_id[DeliverySurfaceKind(profile.surface.value)] = profile_id

        manifest = self.registry_service.manifest
        manifest_health = self.registry_service.manifest_health
        manifest_version = manifest.version if manifest is not None else "unknown"
        manifest_hash = manifest_health.manifest_hash if manifest_health is not None else "0" * 8
        registry_hash = self._compute_registry_hash(
            families=families,
            functions=functions,
            primitive_crosswalks=primitive_crosswalks,
            geometry_crosswalks=geometry_crosswalks,
            archetype_crosswalks=archetype_crosswalks,
            surface_profiles=surface_profiles,
        )

        self.family_order = sorted(families.keys())
        self.families = families
        self.functions = functions
        self.primitive_crosswalks = primitive_crosswalks
        self.geometry_crosswalks = geometry_crosswalks
        self.archetype_crosswalks = archetype_crosswalks
        self.surface_profiles = surface_profiles
        self.family_to_function_ids = family_to_function_ids
        self.primitive_to_crosswalk_ids = primitive_to_crosswalk_ids
        self.geometry_to_crosswalk_ids = geometry_to_crosswalk_ids
        self.archetype_to_crosswalk_ids = archetype_to_crosswalk_ids
        self.surface_to_profile_id = surface_to_profile_id
        self.version_stamp = SFLVersionStamp(
            manifest_version=manifest_version,
            manifest_hash=manifest_hash,
            registry_hash=registry_hash,
        )
        self.last_warm_at = report.last_load_at
        self.index_build_count += 1
        self.ready = True
        return True

    def snapshot(self) -> _CacheSnapshot:
        return _CacheSnapshot(
            ready=self.ready,
            version_stamp=self.version_stamp.model_copy(deep=True),
            last_warm_at=self.last_warm_at,
            index_build_count=self.index_build_count,
            family_order=list(self.family_order),
            families=deepcopy(self.families),
            functions=deepcopy(self.functions),
            primitive_crosswalks=deepcopy(self.primitive_crosswalks),
            geometry_crosswalks=deepcopy(self.geometry_crosswalks),
            archetype_crosswalks=deepcopy(self.archetype_crosswalks),
            surface_profiles=deepcopy(self.surface_profiles),
            family_to_function_ids=deepcopy(self.family_to_function_ids),
            primitive_to_crosswalk_ids=deepcopy(self.primitive_to_crosswalk_ids),
            geometry_to_crosswalk_ids=deepcopy(self.geometry_to_crosswalk_ids),
            archetype_to_crosswalk_ids=deepcopy(self.archetype_to_crosswalk_ids),
            surface_to_profile_id=deepcopy(self.surface_to_profile_id),
        )

    def restore(self, snapshot: _CacheSnapshot) -> None:
        self.ready = snapshot.ready
        self.version_stamp = snapshot.version_stamp.model_copy(deep=True)
        self.last_warm_at = snapshot.last_warm_at
        self.index_build_count = snapshot.index_build_count
        self.family_order = list(snapshot.family_order)
        self.families = deepcopy(snapshot.families)
        self.functions = deepcopy(snapshot.functions)
        self.primitive_crosswalks = deepcopy(snapshot.primitive_crosswalks)
        self.geometry_crosswalks = deepcopy(snapshot.geometry_crosswalks)
        self.archetype_crosswalks = deepcopy(snapshot.archetype_crosswalks)
        self.surface_profiles = deepcopy(snapshot.surface_profiles)
        self.family_to_function_ids = deepcopy(snapshot.family_to_function_ids)
        self.primitive_to_crosswalk_ids = deepcopy(snapshot.primitive_to_crosswalk_ids)
        self.geometry_to_crosswalk_ids = deepcopy(snapshot.geometry_to_crosswalk_ids)
        self.archetype_to_crosswalk_ids = deepcopy(snapshot.archetype_to_crosswalk_ids)
        self.surface_to_profile_id = deepcopy(snapshot.surface_to_profile_id)

    def default_function_for_family(self, family_id: str) -> SubliminalFunctionDefinitionRecord | None:
        function_ids = self.family_to_function_ids.get(family_id, [])
        if not function_ids:
            return None
        return self.functions.get(function_ids[0])

    @staticmethod
    def _normalize_archetype(name: str) -> str:
        return " ".join(name.strip().lower().split())

    @staticmethod
    def _compute_registry_hash(
        *,
        families: dict[str, SubliminalFunctionFamilyRecord],
        functions: dict[str, SubliminalFunctionDefinitionRecord],
        primitive_crosswalks: dict[str, PrimitiveToFunctionFamilyCrosswalkRecord],
        geometry_crosswalks: dict[str, RepresentationGeometryToFunctionProfileRecord],
        archetype_crosswalks: dict[str, ArchetypeToFunctionProfileRecord],
        surface_profiles: dict[str, SurfaceConstraintProfileRecord],
    ) -> str:
        bundles = [
            {key: value.model_dump(mode="json") for key, value in sorted(families.items())},
            {key: value.model_dump(mode="json") for key, value in sorted(functions.items())},
            {key: value.model_dump(mode="json") for key, value in sorted(primitive_crosswalks.items())},
            {key: value.model_dump(mode="json") for key, value in sorted(geometry_crosswalks.items())},
            {key: value.model_dump(mode="json") for key, value in sorted(archetype_crosswalks.items())},
            {key: value.model_dump(mode="json") for key, value in sorted(surface_profiles.items())},
        ]
        payload = json.dumps(bundles, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class SubliminalFunctionProfileResolver:
    """Deterministic precedence resolver for FR-ERA3-26 assembly."""

    def __init__(self, cache_manager: SFLQueryCacheManager) -> None:
        self.cache_manager = cache_manager

    def assemble(
        self,
        request: FunctionProfileAssemblyRequest,
        *,
        primitive_registry_service: PrimitiveRegistryQueryService,
        sda_registry_service: SDARegistryService,
    ) -> tuple[
        SFLAssemblyStatus,
        list[ResolvedFamilyRecord],
        list[ResolvedFunctionRecord],
        list[str],
        list[FunctionProfileEvidenceRecord],
        list[ProfileConflictRecord],
        list[SFLQueryWarning],
    ]:
        evidence: list[FunctionProfileEvidenceRecord] = []
        warnings: list[SFLQueryWarning] = []
        conflicts: list[ProfileConflictRecord] = []
        selected_functions: dict[str, _SelectedFunction] = {}
        selected_families: dict[str, ResolvedFamilyRecord] = {}
        suppressed_function_ids: list[str] = []
        fallback_candidate_families: dict[str, tuple[int, str, str, str]] = {}

        surface_profile = self._get_surface_profile(request.delivery_surface)
        surface_discouraged_families = set(surface_profile.discouraged_family_ids if surface_profile else [])
        archetype_discouraged_families: set[str] = set()
        geometry_discouraged_functions: set[str] = set()

        if surface_profile is not None:
            evidence.append(
                self._make_evidence(
                    evidence_kind=ProfileEvidenceKind.SURFACE_CONSTRAINT_PROFILE,
                    source_artifact_id=surface_profile.artifact_id,
                    source_label=surface_profile.surface.value,
                    affected_family_ids=surface_profile.preferred_family_ids + surface_profile.discouraged_family_ids,
                    affected_function_ids=[],
                    rationale=surface_profile.rationale,
                )
            )
            for family_id in surface_profile.preferred_family_ids:
                family = self.cache_manager.families.get(family_id)
                if family is not None:
                    selected_families.setdefault(
                        family_id,
                        ResolvedFamilyRecord(
                            family_id=family_id,
                            canonical_name=family.canonical_name,
                            rationale=f"Preferred by {request.delivery_surface.value} surface profile",
                        ),
                    )
                    fallback_candidate_families.setdefault(
                        family_id,
                        (
                            EVIDENCE_PRECEDENCE[ProfileEvidenceKind.SURFACE_CONSTRAINT_PROFILE],
                            FunctionSelectionSource.PREFERRED_BY_SURFACE.value,
                            f"Preferred by {request.delivery_surface.value} surface profile",
                            surface_profile.artifact_id,
                        ),
                    )

        for function_id in request.explicit_function_ids:
            function = self.cache_manager.functions.get(function_id)
            if function is None:
                continue
            if function.family_id in surface_discouraged_families:
                warning = SFLQueryWarning(
                    code=SFLQueryWarningCode.EXPLICIT_OVERRIDE_DISCOURAGED,
                    message=f"Explicit override {function_id} conflicts with discouraged surface family {function.family_id}",
                    evidence_ref=surface_profile.artifact_id if surface_profile else function_id,
                )
                warnings.append(warning)
                conflicts.append(
                    self._make_conflict(
                        higher_priority_evidence_ref=surface_profile.artifact_id if surface_profile else function_id,
                        lower_priority_evidence_ref=function_id,
                        conflict_scope="surface_rule",
                        affected_function_ids=[function_id],
                        resolution="review_required",
                        rationale="Surface profile discourages the explicit override family.",
                    )
                )
            self._add_function(
                selected_functions,
                selected_families,
                function=function,
                selection_source=FunctionSelectionSource.EXPLICIT_OVERRIDE,
                rationale="Explicit function override supplied in assembly request.",
                evidence_ref=function_id,
                precedence_rank=EVIDENCE_PRECEDENCE[ProfileEvidenceKind.EXPLICIT_FUNCTION],
            )
            evidence.append(
                self._make_evidence(
                    evidence_kind=ProfileEvidenceKind.EXPLICIT_FUNCTION,
                    source_artifact_id=function.artifact_id,
                    source_label=function.canonical_name,
                    affected_family_ids=[function.family_id],
                    affected_function_ids=[function.artifact_id],
                    rationale="Explicit function override supplied in assembly request.",
                )
            )

        for family_id in request.explicit_family_ids:
            family = self.cache_manager.families.get(family_id)
            if family is None:
                continue
            selected_families.setdefault(
                family_id,
                ResolvedFamilyRecord(
                    family_id=family_id,
                    canonical_name=family.canonical_name,
                    rationale="Explicit family override supplied in assembly request.",
                ),
            )
            fallback_candidate_families.setdefault(
                family_id,
                (
                    EVIDENCE_PRECEDENCE[ProfileEvidenceKind.FAMILY_DEFAULT],
                    FunctionSelectionSource.FALLBACK_FROM_FAMILY.value,
                    "Explicit family override supplied in assembly request.",
                    family_id,
                ),
            )

        if request.content_archetype:
            archetype_key = self.cache_manager._normalize_archetype(request.content_archetype)
            archetype_crosswalk_ids = self.cache_manager.archetype_to_crosswalk_ids.get(archetype_key, [])
            if not archetype_crosswalk_ids and request.require_complete_crosswalks:
                warnings.append(
                    SFLQueryWarning(
                        code=SFLQueryWarningCode.PARTIAL_CROSSWALK_EVIDENCE,
                        message=f"No maintained archetype profile found for '{request.content_archetype}'.",
                        evidence_ref=request.content_archetype,
                    )
                )
            for crosswalk_id in archetype_crosswalk_ids:
                crosswalk = self.cache_manager.archetype_crosswalks[crosswalk_id]
                archetype_discouraged_families.update(crosswalk.discouraged_family_ids)
                evidence.append(
                    self._make_evidence(
                        evidence_kind=ProfileEvidenceKind.ARCHETYPE_PROFILE,
                        source_artifact_id=crosswalk.artifact_id,
                        source_label=request.content_archetype,
                        affected_family_ids=crosswalk.required_family_ids + crosswalk.discouraged_family_ids,
                        affected_function_ids=crosswalk.preferred_function_ids,
                        rationale=crosswalk.mapping_rationale,
                    )
                )
                for family_id in crosswalk.required_family_ids:
                    family = self.cache_manager.families.get(family_id)
                    if family is None:
                        continue
                    selected_families.setdefault(
                        family_id,
                        ResolvedFamilyRecord(
                            family_id=family_id,
                            canonical_name=family.canonical_name,
                            rationale=f"Required by archetype profile '{request.content_archetype}'.",
                        ),
                    )
                    fallback_candidate_families.setdefault(
                        family_id,
                        (
                            EVIDENCE_PRECEDENCE[ProfileEvidenceKind.ARCHETYPE_PROFILE],
                            FunctionSelectionSource.REQUIRED_BY_ARCHETYPE.value,
                            f"Required by archetype profile '{request.content_archetype}'.",
                            crosswalk.artifact_id,
                        ),
                    )
                for function_id in crosswalk.preferred_function_ids:
                    function = self.cache_manager.functions.get(function_id)
                    if function is None:
                        continue
                    if function.family_id in surface_discouraged_families:
                        conflicts.append(
                            self._make_conflict(
                                higher_priority_evidence_ref=surface_profile.artifact_id if surface_profile else request.delivery_surface.value,
                                lower_priority_evidence_ref=crosswalk.artifact_id,
                                conflict_scope="surface_rule",
                                affected_function_ids=[function_id],
                                resolution="suppressed_lower_priority",
                                rationale="Surface profile suppresses lower-priority archetype preference.",
                            )
                        )
                        warnings.append(
                            SFLQueryWarning(
                                code=SFLQueryWarningCode.SURFACE_CONSTRAINT_REMOVED_FUNCTION,
                                message=f"Surface profile removed archetype-preferred function {function_id}.",
                                evidence_ref=crosswalk.artifact_id,
                            )
                        )
                        suppressed_function_ids = self._append_unique(suppressed_function_ids, function_id)
                        continue
                    self._add_function(
                        selected_functions,
                        selected_families,
                        function=function,
                        selection_source=FunctionSelectionSource.PREFERRED_BY_ARCHETYPE,
                        rationale=f"Preferred by archetype profile '{request.content_archetype}'.",
                        evidence_ref=crosswalk.artifact_id,
                        precedence_rank=EVIDENCE_PRECEDENCE[ProfileEvidenceKind.ARCHETYPE_PROFILE],
                    )

        if request.representation_geometry_id:
            geometry_record = sda_registry_service.get_representation_geometry(request.representation_geometry_id)
            if geometry_record is None:
                warnings.append(
                    SFLQueryWarning(
                        code=SFLQueryWarningCode.UNKNOWN_GEOMETRY_REFERENCE,
                        message=f"Unknown representation geometry reference: {request.representation_geometry_id}",
                        evidence_ref=request.representation_geometry_id,
                    )
                )
            geometry_crosswalk_ids = self.cache_manager.geometry_to_crosswalk_ids.get(request.representation_geometry_id, [])
            if geometry_record is not None and not geometry_crosswalk_ids and request.require_complete_crosswalks:
                warnings.append(
                    SFLQueryWarning(
                        code=SFLQueryWarningCode.PARTIAL_CROSSWALK_EVIDENCE,
                        message=f"No maintained geometry profile found for {request.representation_geometry_id}.",
                        evidence_ref=request.representation_geometry_id,
                    )
                )
            for crosswalk_id in geometry_crosswalk_ids:
                crosswalk = self.cache_manager.geometry_crosswalks[crosswalk_id]
                geometry_discouraged_functions.update(crosswalk.discouraged_function_ids)
                evidence.append(
                    self._make_evidence(
                        evidence_kind=ProfileEvidenceKind.REPRESENTATION_GEOMETRY_PROFILE,
                        source_artifact_id=crosswalk.artifact_id,
                        source_label=request.representation_geometry_id,
                        affected_family_ids=[],
                        affected_function_ids=crosswalk.preferred_function_ids + crosswalk.discouraged_function_ids,
                        rationale=crosswalk.mapping_rationale,
                    )
                )
                for function_id in crosswalk.preferred_function_ids:
                    function = self.cache_manager.functions.get(function_id)
                    if function is None:
                        continue
                    if function.family_id in surface_discouraged_families:
                        conflicts.append(
                            self._make_conflict(
                                higher_priority_evidence_ref=surface_profile.artifact_id if surface_profile else request.delivery_surface.value,
                                lower_priority_evidence_ref=crosswalk.artifact_id,
                                conflict_scope="surface_rule",
                                affected_function_ids=[function_id],
                                resolution="suppressed_lower_priority",
                                rationale="Surface profile suppresses lower-priority geometry preference.",
                            )
                        )
                        warnings.append(
                            SFLQueryWarning(
                                code=SFLQueryWarningCode.SURFACE_CONSTRAINT_REMOVED_FUNCTION,
                                message=f"Surface profile removed geometry-preferred function {function_id}.",
                                evidence_ref=crosswalk.artifact_id,
                            )
                        )
                        suppressed_function_ids = self._append_unique(suppressed_function_ids, function_id)
                        continue
                    self._add_function(
                        selected_functions,
                        selected_families,
                        function=function,
                        selection_source=FunctionSelectionSource.PREFERRED_BY_GEOMETRY,
                        rationale=f"Preferred by representation geometry {request.representation_geometry_id}.",
                        evidence_ref=crosswalk.artifact_id,
                        precedence_rank=EVIDENCE_PRECEDENCE[ProfileEvidenceKind.REPRESENTATION_GEOMETRY_PROFILE],
                    )

        for primitive_id in request.primitive_ids:
            primitive_record = self._lookup_primitive(primitive_registry_service, primitive_id)
            if primitive_record is None:
                warnings.append(
                    SFLQueryWarning(
                        code=SFLQueryWarningCode.UNKNOWN_PRIMITIVE_REFERENCE,
                        message=f"Unknown primitive reference: {primitive_id}",
                        evidence_ref=primitive_id,
                    )
                )
                continue
            crosswalk_ids = self.cache_manager.primitive_to_crosswalk_ids.get(primitive_id, [])
            if not crosswalk_ids and request.require_complete_crosswalks:
                warnings.append(
                    SFLQueryWarning(
                        code=SFLQueryWarningCode.PARTIAL_CROSSWALK_EVIDENCE,
                        message=f"No maintained primitive crosswalk found for {primitive_id}.",
                        evidence_ref=primitive_id,
                    )
                )
            for crosswalk_id in crosswalk_ids:
                crosswalk = self.cache_manager.primitive_crosswalks[crosswalk_id]
                evidence.append(
                    self._make_evidence(
                        evidence_kind=ProfileEvidenceKind.PRIMITIVE_CROSSWALK,
                        source_artifact_id=crosswalk.artifact_id,
                        source_label=primitive_id,
                        affected_family_ids=crosswalk.target_family_ids,
                        affected_function_ids=[],
                        rationale=crosswalk.mapping_rationale,
                    )
                )
                for family_id in crosswalk.target_family_ids:
                    family = self.cache_manager.families.get(family_id)
                    if family is None:
                        continue
                    selected_families.setdefault(
                        family_id,
                        ResolvedFamilyRecord(
                            family_id=family_id,
                            canonical_name=family.canonical_name,
                            rationale=f"Hinted by primitive crosswalk {primitive_id}.",
                        ),
                    )
                    fallback_candidate_families.setdefault(
                        family_id,
                        (
                            EVIDENCE_PRECEDENCE[ProfileEvidenceKind.PRIMITIVE_CROSSWALK],
                            FunctionSelectionSource.HINTED_BY_PRIMITIVE.value,
                            f"Hinted by primitive crosswalk {primitive_id}.",
                            crosswalk.artifact_id,
                        ),
                    )

        fallback_applied = False
        for family_id in sorted(fallback_candidate_families):
            if len(selected_functions) >= MAX_ACTIVE_FUNCTIONS:
                break
            if any(entry.function.family_id == family_id for entry in selected_functions.values()):
                continue
            if family_id in surface_discouraged_families or family_id in archetype_discouraged_families:
                continue
            default_function = self.cache_manager.default_function_for_family(family_id)
            if default_function is None:
                continue
            if default_function.artifact_id in geometry_discouraged_functions:
                conflicts.append(
                    self._make_conflict(
                        higher_priority_evidence_ref=request.representation_geometry_id or "geometry_rule",
                        lower_priority_evidence_ref=fallback_candidate_families[family_id][3],
                        conflict_scope="geometry_rule",
                        affected_function_ids=[default_function.artifact_id],
                        resolution="downgraded_to_family_only",
                        rationale="Geometry discourages the default family fallback function.",
                    )
                )
                continue

            _, source_value, rationale, evidence_ref = fallback_candidate_families[family_id]
            selection_source = FunctionSelectionSource(source_value)
            if selection_source not in {
                FunctionSelectionSource.PREFERRED_BY_SURFACE,
                FunctionSelectionSource.REQUIRED_BY_ARCHETYPE,
                FunctionSelectionSource.HINTED_BY_PRIMITIVE,
                FunctionSelectionSource.FALLBACK_FROM_FAMILY,
            }:
                selection_source = FunctionSelectionSource.FALLBACK_FROM_FAMILY
            self._add_function(
                selected_functions,
                selected_families,
                function=default_function,
                selection_source=FunctionSelectionSource.FALLBACK_FROM_FAMILY,
                rationale=rationale,
                evidence_ref=evidence_ref,
                precedence_rank=EVIDENCE_PRECEDENCE[ProfileEvidenceKind.FAMILY_DEFAULT],
            )
            fallback_applied = True

        if fallback_applied:
            warnings.append(
                SFLQueryWarning(
                    code=SFLQueryWarningCode.FAMILY_ONLY_FALLBACK,
                    message="Canonical family default fallback was used for one or more active functions.",
                    evidence_ref="family_default",
                )
            )

        ordered_functions = [
            selected_functions[function_id]
            for function_id in sorted(
                selected_functions,
                key=lambda function_id: (
                    selected_functions[function_id].precedence_rank,
                    selected_functions[function_id].function.artifact_id,
                ),
            )
        ][:MAX_ACTIVE_FUNCTIONS]

        if len(ordered_functions) < len(selected_functions):
            overflow_ids = [
                function_id
                for function_id in selected_functions
                if function_id not in {entry.function.artifact_id for entry in ordered_functions}
            ]
            for function_id in overflow_ids:
                suppressed_function_ids = self._append_unique(suppressed_function_ids, function_id)

        resolved_functions = [
            ResolvedFunctionRecord(
                function_id=entry.function.artifact_id,
                canonical_name=entry.function.canonical_name,
                family_id=entry.function.family_id,
                selection_source=entry.source,
                rationale=entry.rationale,
            )
            for entry in ordered_functions
        ]

        selected_family_ids = {record.family_id for record in resolved_functions}
        for family_id in list(selected_families):
            if family_id not in selected_family_ids and family_id not in fallback_candidate_families:
                selected_families.pop(family_id, None)

        resolved_families = [selected_families[family_id] for family_id in sorted(selected_families)]
        ordered_evidence = sorted(
            evidence,
            key=lambda record: (record.precedence_rank, record.source_artifact_id, record.source_label),
        )

        if any(conflict.resolution == "review_required" for conflict in conflicts):
            status = SFLAssemblyStatus.REVIEW_REQUIRED
            warnings.append(
                SFLQueryWarning(
                    code=SFLQueryWarningCode.CONFLICT_REQUIRES_REVIEW,
                    message="One or more higher-priority conflicts require human review.",
                    evidence_ref=conflicts[0].conflict_id,
                )
            )
        elif not resolved_functions and not resolved_families:
            status = SFLAssemblyStatus.UNRESOLVED
        elif resolved_functions and all(
            function.selection_source == FunctionSelectionSource.FALLBACK_FROM_FAMILY for function in resolved_functions
        ):
            status = SFLAssemblyStatus.FAMILY_ONLY
        elif warnings:
            status = SFLAssemblyStatus.PARTIAL
        else:
            status = SFLAssemblyStatus.RESOLVED

        return (
            status,
            resolved_families,
            resolved_functions,
            suppressed_function_ids,
            ordered_evidence,
            conflicts,
            warnings,
        )

    def _get_surface_profile(self, surface: DeliverySurfaceKind) -> SurfaceConstraintProfileRecord | None:
        profile_id = self.cache_manager.surface_to_profile_id.get(surface)
        if profile_id is None:
            return None
        return self.cache_manager.surface_profiles.get(profile_id)

    def _lookup_primitive(
        self,
        primitive_registry_service: PrimitiveRegistryQueryService,
        primitive_id: str,
    ) -> PrimitiveRecord | None:
        plane = PrimitivePlane.EXPERIENCE if primitive_id.startswith("EXP-") else PrimitivePlane.MEANING
        return primitive_registry_service.query_by_id(primitive_id, plane)

    def _add_function(
        self,
        selected_functions: dict[str, _SelectedFunction],
        selected_families: dict[str, ResolvedFamilyRecord],
        *,
        function: SubliminalFunctionDefinitionRecord,
        selection_source: FunctionSelectionSource,
        rationale: str,
        evidence_ref: str,
        precedence_rank: int,
    ) -> None:
        existing = selected_functions.get(function.artifact_id)
        if existing is not None and existing.precedence_rank <= precedence_rank:
            return
        selected_functions[function.artifact_id] = _SelectedFunction(
            function=function,
            source=selection_source,
            rationale=rationale,
            evidence_ref=evidence_ref,
            precedence_rank=precedence_rank,
        )
        family = self.cache_manager.families.get(function.family_id)
        if family is not None:
            selected_families.setdefault(
                function.family_id,
                ResolvedFamilyRecord(
                    family_id=function.family_id,
                    canonical_name=family.canonical_name,
                    rationale=f"Activated by function {function.artifact_id}.",
                ),
            )

    @staticmethod
    def _make_evidence(
        *,
        evidence_kind: ProfileEvidenceKind,
        source_artifact_id: str,
        source_label: str,
        affected_family_ids: list[str],
        affected_function_ids: list[str],
        rationale: str,
    ) -> FunctionProfileEvidenceRecord:
        return FunctionProfileEvidenceRecord(
            evidence_kind=evidence_kind,
            source_artifact_id=source_artifact_id,
            source_label=source_label,
            affected_family_ids=affected_family_ids,
            affected_function_ids=affected_function_ids,
            rationale=rationale,
            precedence_rank=EVIDENCE_PRECEDENCE[evidence_kind],
        )

    @staticmethod
    def _make_conflict(
        *,
        higher_priority_evidence_ref: str,
        lower_priority_evidence_ref: str,
        conflict_scope: str,
        affected_function_ids: list[str],
        resolution: str,
        rationale: str,
    ) -> ProfileConflictRecord:
        conflict_seed = (
            f"{higher_priority_evidence_ref}:{lower_priority_evidence_ref}:{conflict_scope}:{','.join(affected_function_ids)}:{resolution}"
        )
        conflict_id = f"SFL-CF-{hashlib.sha256(conflict_seed.encode('utf-8')).hexdigest()[:10]}"
        return ProfileConflictRecord(
            conflict_id=conflict_id,
            higher_priority_evidence_ref=higher_priority_evidence_ref,
            lower_priority_evidence_ref=lower_priority_evidence_ref,
            conflict_scope=conflict_scope,  # type: ignore[arg-type]
            affected_function_ids=affected_function_ids,
            resolution=resolution,  # type: ignore[arg-type]
            rationale=rationale,
        )

    @staticmethod
    def _append_unique(values: list[str], value: str) -> list[str]:
        if value not in values:
            values.append(value)
        return values


class SubliminalFunctionQueryService:
    """Bounded runtime query and profile assembly service for SFL."""

    def __init__(
        self,
        *,
        sfl_registry_service: SFLRegistryService | None = None,
        primitive_registry_service: PrimitiveRegistryQueryService | None = None,
        sda_registry_service: SDARegistryService | None = None,
        receipt_chain: ReceiptChain | None = None,
    ) -> None:
        coach_acronym = os.getenv("COACH_ACRONYM", "SFL")
        self.receipt_chain = receipt_chain or ReceiptChain(coach_acronym=coach_acronym[:3].upper())
        self.sfl_registry_service = sfl_registry_service or SFLRegistryService(receipt_chain=self.receipt_chain)
        self.primitive_registry_service = primitive_registry_service or PrimitiveRegistryQueryService(
            receipt_chain=self.receipt_chain
        )
        self.sda_registry_service = sda_registry_service or SDARegistryService(receipt_chain=self.receipt_chain)
        self.cache_manager = SFLQueryCacheManager(self.sfl_registry_service)
        self.profile_resolver = SubliminalFunctionProfileResolver(self.cache_manager)

    def warm(self) -> bool:
        if not self.sfl_registry_service.health().ready:
            self.sfl_registry_service.warm(strict=False, allow_degraded_dev_mode=True)
        if self.primitive_registry_service.health().total_cached == 0:
            self.primitive_registry_service.warm_registry()
        if not self.sda_registry_service.health().ready:
            self.sda_registry_service.warm(strict=False, allow_degraded_dev_mode=True)

        ready = self.cache_manager.warm_from_registry()
        self.receipt_chain.log(
            agent_id="sfl_query_service",
            action=STAGE_STARTUP_WARM,
            input_summary="warm_sfl_query_cache",
            output_summary="ready" if ready else "not_ready",
            decision="READY" if ready else "NOT_READY",
            metadata={
                "stage_name": STAGE_STARTUP_WARM,
                "registry_ready": self.sfl_registry_service.health().ready,
                "cache_ready": ready,
                "index_build_count": self.cache_manager.index_build_count,
            },
        )
        return ready

    def query(self, request: SubliminalFunctionQueryRequest) -> SubliminalFunctionQueryResponse:
        start = time.perf_counter()
        ready = self.cache_manager.ready or self.warm()
        if not ready:
            latency_ms = round((time.perf_counter() - start) * 1000, 3)
            return SubliminalFunctionQueryResponse(
                query_id=str(uuid4()),
                query_mode=request.query_mode,
                ready=False,
                version_stamp=self.cache_manager.version_stamp,
                cache_hit=False,
                latency_ms=latency_ms,
            )

        families: list[ResolvedFamilyRecord] = []
        functions: list[ResolvedFunctionRecord] = []
        evidence: list[FunctionProfileEvidenceRecord] = []
        warnings: list[SFLQueryWarning] = []

        if request.query_mode == SFLQueryMode.BY_FAMILY:
            family = self.cache_manager.families.get(request.family_id or "")
            if family is not None:
                families.append(
                    ResolvedFamilyRecord(
                        family_id=family.artifact_id,
                        canonical_name=family.canonical_name,
                        rationale="Canonical family lookup.",
                    )
                )
                evidence.append(
                    FunctionProfileEvidenceRecord(
                        evidence_kind=ProfileEvidenceKind.FAMILY_DEFAULT,
                        source_artifact_id=family.artifact_id,
                        source_label=family.canonical_name,
                        affected_family_ids=[family.artifact_id],
                        affected_function_ids=self.cache_manager.family_to_function_ids.get(family.artifact_id, []),
                        rationale="Canonical family lookup.",
                        precedence_rank=EVIDENCE_PRECEDENCE[ProfileEvidenceKind.FAMILY_DEFAULT],
                    )
                )
                if request.include_functions:
                    for function_id in self.cache_manager.family_to_function_ids.get(family.artifact_id, []):
                        function = self.cache_manager.functions[function_id]
                        functions.append(
                            ResolvedFunctionRecord(
                                function_id=function.artifact_id,
                                canonical_name=function.canonical_name,
                                family_id=function.family_id,
                                selection_source=FunctionSelectionSource.FALLBACK_FROM_FAMILY,
                                rationale="Canonical family-aligned function lookup.",
                            )
                        )

        elif request.query_mode == SFLQueryMode.BY_FUNCTION_ID:
            function = self.cache_manager.functions.get(request.function_id or "")
            if function is not None:
                family = self.cache_manager.families.get(function.family_id)
                if family is not None:
                    families.append(
                        ResolvedFamilyRecord(
                            family_id=family.artifact_id,
                            canonical_name=family.canonical_name,
                            rationale="Parent family of canonical function lookup.",
                        )
                    )
                functions.append(
                    ResolvedFunctionRecord(
                        function_id=function.artifact_id,
                        canonical_name=function.canonical_name,
                        family_id=function.family_id,
                        selection_source=FunctionSelectionSource.EXPLICIT_OVERRIDE,
                        rationale="Canonical function-id lookup.",
                    )
                )
                evidence.append(
                    FunctionProfileEvidenceRecord(
                        evidence_kind=ProfileEvidenceKind.EXPLICIT_FUNCTION,
                        source_artifact_id=function.artifact_id,
                        source_label=function.canonical_name,
                        affected_family_ids=[function.family_id],
                        affected_function_ids=[function.artifact_id],
                        rationale="Canonical function-id lookup.",
                        precedence_rank=EVIDENCE_PRECEDENCE[ProfileEvidenceKind.EXPLICIT_FUNCTION],
                    )
                )

        elif request.query_mode == SFLQueryMode.BY_PRIMITIVE_CROSSWALK:
            primitive_id = request.primitive_id or ""
            primitive_record = self.profile_resolver._lookup_primitive(self.primitive_registry_service, primitive_id)
            if primitive_record is None:
                warnings.append(
                    SFLQueryWarning(
                        code=SFLQueryWarningCode.UNKNOWN_PRIMITIVE_REFERENCE,
                        message=f"Unknown primitive reference: {primitive_id}",
                        evidence_ref=primitive_id,
                    )
                )
            for crosswalk_id in self.cache_manager.primitive_to_crosswalk_ids.get(primitive_id, []):
                crosswalk = self.cache_manager.primitive_crosswalks[crosswalk_id]
                evidence.append(
                    FunctionProfileEvidenceRecord(
                        evidence_kind=ProfileEvidenceKind.PRIMITIVE_CROSSWALK,
                        source_artifact_id=crosswalk.artifact_id,
                        source_label=primitive_id,
                        affected_family_ids=crosswalk.target_family_ids,
                        affected_function_ids=[],
                        rationale=crosswalk.mapping_rationale,
                        precedence_rank=EVIDENCE_PRECEDENCE[ProfileEvidenceKind.PRIMITIVE_CROSSWALK],
                    )
                )
                for family_id in crosswalk.target_family_ids:
                    family = self.cache_manager.families.get(family_id)
                    if family is None:
                        continue
                    families.append(
                        ResolvedFamilyRecord(
                            family_id=family.artifact_id,
                            canonical_name=family.canonical_name,
                            rationale=f"Maintained primitive crosswalk from {primitive_id}.",
                        )
                    )
                    if request.include_functions:
                        for function_id in self.cache_manager.family_to_function_ids.get(family_id, []):
                            function = self.cache_manager.functions[function_id]
                            functions.append(
                                ResolvedFunctionRecord(
                                    function_id=function.artifact_id,
                                    canonical_name=function.canonical_name,
                                    family_id=function.family_id,
                                    selection_source=FunctionSelectionSource.HINTED_BY_PRIMITIVE,
                                    rationale=f"Family-aligned function supported by primitive crosswalk {primitive_id}.",
                                )
                            )

        elif request.query_mode == SFLQueryMode.BY_REPRESENTATION_GEOMETRY:
            geometry_id = request.representation_geometry_id or ""
            geometry_record: RepresentationGeometryRecord | None = self.sda_registry_service.get_representation_geometry(
                geometry_id
            )
            if geometry_record is None:
                warnings.append(
                    SFLQueryWarning(
                        code=SFLQueryWarningCode.UNKNOWN_GEOMETRY_REFERENCE,
                        message=f"Unknown representation geometry reference: {geometry_id}",
                        evidence_ref=geometry_id,
                    )
                )
            for crosswalk_id in self.cache_manager.geometry_to_crosswalk_ids.get(geometry_id, []):
                crosswalk = self.cache_manager.geometry_crosswalks[crosswalk_id]
                evidence.append(
                    FunctionProfileEvidenceRecord(
                        evidence_kind=ProfileEvidenceKind.REPRESENTATION_GEOMETRY_PROFILE,
                        source_artifact_id=crosswalk.artifact_id,
                        source_label=geometry_id,
                        affected_family_ids=[],
                        affected_function_ids=crosswalk.preferred_function_ids,
                        rationale=crosswalk.mapping_rationale,
                        precedence_rank=EVIDENCE_PRECEDENCE[ProfileEvidenceKind.REPRESENTATION_GEOMETRY_PROFILE],
                    )
                )
                for function_id in crosswalk.preferred_function_ids:
                    function = self.cache_manager.functions.get(function_id)
                    if function is None:
                        continue
                    family = self.cache_manager.families.get(function.family_id)
                    if family is not None and family.artifact_id not in {entry.family_id for entry in families}:
                        families.append(
                            ResolvedFamilyRecord(
                                family_id=family.artifact_id,
                                canonical_name=family.canonical_name,
                                rationale=f"Parent family of geometry-preferred function {function_id}.",
                            )
                        )
                    functions.append(
                        ResolvedFunctionRecord(
                            function_id=function.artifact_id,
                            canonical_name=function.canonical_name,
                            family_id=function.family_id,
                            selection_source=FunctionSelectionSource.PREFERRED_BY_GEOMETRY,
                            rationale=f"Maintained geometry profile for {geometry_id}.",
                        )
                    )

        elif request.query_mode == SFLQueryMode.BY_ARCHETYPE_PROFILE:
            archetype_key = self.cache_manager._normalize_archetype(request.archetype_name or "")
            for crosswalk_id in self.cache_manager.archetype_to_crosswalk_ids.get(archetype_key, []):
                crosswalk = self.cache_manager.archetype_crosswalks[crosswalk_id]
                evidence.append(
                    FunctionProfileEvidenceRecord(
                        evidence_kind=ProfileEvidenceKind.ARCHETYPE_PROFILE,
                        source_artifact_id=crosswalk.artifact_id,
                        source_label=request.archetype_name or "",
                        affected_family_ids=crosswalk.required_family_ids,
                        affected_function_ids=crosswalk.preferred_function_ids,
                        rationale=crosswalk.mapping_rationale,
                        precedence_rank=EVIDENCE_PRECEDENCE[ProfileEvidenceKind.ARCHETYPE_PROFILE],
                    )
                )
                for family_id in crosswalk.required_family_ids:
                    family = self.cache_manager.families.get(family_id)
                    if family is not None:
                        families.append(
                            ResolvedFamilyRecord(
                                family_id=family.artifact_id,
                                canonical_name=family.canonical_name,
                                rationale=f"Required by archetype profile '{request.archetype_name}'.",
                            )
                        )
                if request.include_functions:
                    for function_id in crosswalk.preferred_function_ids:
                        function = self.cache_manager.functions.get(function_id)
                        if function is None:
                            continue
                        if function.family_id not in {entry.family_id for entry in families}:
                            family = self.cache_manager.families.get(function.family_id)
                            if family is not None:
                                families.append(
                                    ResolvedFamilyRecord(
                                        family_id=family.artifact_id,
                                        canonical_name=family.canonical_name,
                                        rationale=f"Parent family of archetype-preferred function {function_id}.",
                                    )
                                )
                        functions.append(
                            ResolvedFunctionRecord(
                                function_id=function.artifact_id,
                                canonical_name=function.canonical_name,
                                family_id=function.family_id,
                                selection_source=FunctionSelectionSource.PREFERRED_BY_ARCHETYPE,
                                rationale=f"Maintained archetype profile for '{request.archetype_name}'.",
                            )
                        )

        elif request.query_mode == SFLQueryMode.BY_SURFACE_PROFILE:
            profile_id = self.cache_manager.surface_to_profile_id.get(request.delivery_surface) if request.delivery_surface else None
            if profile_id is not None:
                profile = self.cache_manager.surface_profiles[profile_id]
                evidence.append(
                    FunctionProfileEvidenceRecord(
                        evidence_kind=ProfileEvidenceKind.SURFACE_CONSTRAINT_PROFILE,
                        source_artifact_id=profile.artifact_id,
                        source_label=profile.surface.value,
                        affected_family_ids=profile.preferred_family_ids + profile.discouraged_family_ids,
                        affected_function_ids=[],
                        rationale=profile.rationale,
                        precedence_rank=EVIDENCE_PRECEDENCE[ProfileEvidenceKind.SURFACE_CONSTRAINT_PROFILE],
                    )
                )
                for family_id in profile.preferred_family_ids:
                    family = self.cache_manager.families.get(family_id)
                    if family is None:
                        continue
                    families.append(
                        ResolvedFamilyRecord(
                            family_id=family.artifact_id,
                            canonical_name=family.canonical_name,
                            rationale=f"Preferred by surface profile '{profile.surface.value}'.",
                        )
                    )
                    if request.include_functions:
                        default_function = self.cache_manager.default_function_for_family(family_id)
                        if default_function is not None:
                            functions.append(
                                ResolvedFunctionRecord(
                                    function_id=default_function.artifact_id,
                                    canonical_name=default_function.canonical_name,
                                    family_id=default_function.family_id,
                                    selection_source=FunctionSelectionSource.PREFERRED_BY_SURFACE,
                                    rationale=f"Default family function preferred by surface profile '{profile.surface.value}'.",
                                )
                            )

        latency_ms = round((time.perf_counter() - start) * 1000, 3)
        response = SubliminalFunctionQueryResponse(
            query_id=str(uuid4()),
            query_mode=request.query_mode,
            ready=True,
            resolved_families=self._dedupe_families(families),
            resolved_functions=self._dedupe_functions(functions),
            evidence_trace=evidence if request.include_crosswalk_evidence else [],
            warnings=warnings,
            version_stamp=self.cache_manager.version_stamp.model_copy(deep=True),
            cache_hit=True,
            latency_ms=latency_ms,
        )
        self.receipt_chain.log(
            agent_id="sfl_query_service",
            action=STAGE_QUERY_LOOKUP,
            input_summary=request.model_dump_json(),
            output_summary=(
                f"families={len(response.resolved_families)} functions={len(response.resolved_functions)} "
                f"warnings={len(response.warnings)}"
            ),
            decision="READY" if response.ready else "NOT_READY",
            metadata={
                "stage_name": STAGE_QUERY_LOOKUP,
                "query_mode": request.query_mode.value,
                "cache_hit": response.cache_hit,
                "latency_ms": response.latency_ms,
            },
        )
        return response

    def assemble_profile(self, request: FunctionProfileAssemblyRequest) -> FunctionProfileAssemblyResult:
        start = time.perf_counter()
        ready = self.cache_manager.ready or self.warm()
        if not ready:
            latency_ms = round((time.perf_counter() - start) * 1000, 3)
            profile = SubliminalFunctionProfile(profile_id=str(uuid4()), status=SFLAssemblyStatus.UNRESOLVED)
            return FunctionProfileAssemblyResult(
                request_id=str(uuid4()),
                status=SFLAssemblyStatus.UNRESOLVED,
                profile=profile,
                warnings=[
                    SFLQueryWarning(
                        code=SFLQueryWarningCode.PARTIAL_CROSSWALK_EVIDENCE,
                        message="SFL query cache is not ready.",
                        evidence_ref="registry_not_ready",
                    )
                ],
                version_stamp=self.cache_manager.version_stamp,
                cache_hit=False,
                latency_ms=latency_ms,
            )

        (
            status,
            resolved_families,
            resolved_functions,
            suppressed_function_ids,
            evidence_trace,
            conflicts,
            warnings,
        ) = self.profile_resolver.assemble(
            request,
            primitive_registry_service=self.primitive_registry_service,
            sda_registry_service=self.sda_registry_service,
        )

        profile = SubliminalFunctionProfile(
            profile_id=str(uuid4()),
            status=status,
            resolved_families=resolved_families,
            resolved_functions=resolved_functions,
            suppressed_function_ids=suppressed_function_ids,
            evidence_trace=evidence_trace,
            conflicts=conflicts,
            warnings=warnings,
        )

        stack_packet: SubliminalFunctionStackPacket | None = None
        if status != SFLAssemblyStatus.UNRESOLVED:
            stack_packet = SubliminalFunctionStackPacket(
                packet_id=str(uuid4()),
                coach_id=request.coach_id,
                content_archetype=request.content_archetype,
                representation_geometry_id=request.representation_geometry_id,
                delivery_surface=request.delivery_surface,
                status=status,
                active_family_ids=[family.family_id for family in resolved_families],
                active_function_ids=[function.function_id for function in resolved_functions],
                suppressed_function_ids=suppressed_function_ids,
                evidence_trace=evidence_trace,
                version_stamp=self.cache_manager.version_stamp.model_copy(deep=True),
                lineage={
                    "service": "FR-ERA3-26",
                    "delivery_surface": request.delivery_surface.value,
                    "content_archetype": request.content_archetype or "",
                    "representation_geometry_id": request.representation_geometry_id or "",
                },
                warnings=warnings,
            )

        latency_ms = round((time.perf_counter() - start) * 1000, 3)
        result = FunctionProfileAssemblyResult(
            request_id=str(uuid4()),
            status=status,
            profile=profile,
            stack_packet=stack_packet,
            warnings=warnings,
            conflicts=conflicts,
            version_stamp=self.cache_manager.version_stamp.model_copy(deep=True),
            cache_hit=True,
            latency_ms=latency_ms,
        )

        self.receipt_chain.log(
            agent_id="sfl_query_service",
            action=STAGE_PROFILE_ASSEMBLY,
            input_summary=request.model_dump_json(),
            output_summary=f"status={status.value} functions={len(resolved_functions)} families={len(resolved_families)}",
            decision=status.value,
            metadata={
                "stage_name": STAGE_PROFILE_ASSEMBLY,
                "latency_ms": latency_ms,
                "active_function_ids": [function.function_id for function in resolved_functions],
                "suppressed_function_ids": suppressed_function_ids,
            },
        )

        if status in {SFLAssemblyStatus.FAMILY_ONLY, SFLAssemblyStatus.PARTIAL, SFLAssemblyStatus.UNRESOLVED}:
            self.receipt_chain.log(
                agent_id="sfl_query_service",
                action=STAGE_DEGRADED_FALLBACK,
                input_summary=request.model_dump_json(),
                output_summary=f"status={status.value}",
                decision=status.value,
                metadata={
                    "stage_name": STAGE_DEGRADED_FALLBACK,
                    "warnings": [warning.code.value for warning in warnings],
                },
            )

        for conflict in conflicts:
            self.receipt_chain.log(
                agent_id="sfl_query_service",
                action=STAGE_CONFLICT,
                input_summary=conflict.lower_priority_evidence_ref,
                output_summary=conflict.rationale,
                decision=conflict.resolution,
                metadata={
                    "stage_name": STAGE_CONFLICT,
                    "conflict_id": conflict.conflict_id,
                    "higher_priority_evidence_ref": conflict.higher_priority_evidence_ref,
                    "affected_function_ids": conflict.affected_function_ids,
                },
            )

        return result

    def rebuild_after_registry_reload(self, path: str | Path) -> bool:
        snapshot = self.cache_manager.snapshot()
        reload_result = self.sfl_registry_service.reload_artifact(path)
        if not reload_result.success:
            self.receipt_chain.log(
                agent_id="sfl_query_service",
                action=STAGE_RELOAD_FAILURE,
                input_summary=str(path),
                output_summary=reload_result.message,
                decision="REJECTED",
                decision_rationale=reload_result.error_code,
                metadata={
                    "stage_name": STAGE_RELOAD_FAILURE,
                    "previous_state_restored": True,
                    "error_code": reload_result.error_code,
                },
            )
            return False

        try:
            ready = self.cache_manager.warm_from_registry()
        except Exception as exc:
            self.cache_manager.restore(snapshot)
            self.receipt_chain.log(
                agent_id="sfl_query_service",
                action=STAGE_RELOAD_FAILURE,
                input_summary=str(path),
                output_summary=str(exc),
                decision="REJECTED",
                decision_rationale="CACHE_REBUILD_FAILED",
                metadata={
                    "stage_name": STAGE_RELOAD_FAILURE,
                    "previous_state_restored": True,
                    "error_code": "CACHE_REBUILD_FAILED",
                },
            )
            return False

        self.receipt_chain.log(
            agent_id="sfl_query_service",
            action=STAGE_CACHE_REBUILD,
            input_summary=str(path),
            output_summary="ready" if ready else "not_ready",
            decision="READY" if ready else "NOT_READY",
            metadata={
                "stage_name": STAGE_CACHE_REBUILD,
                "previous_state_restored": not ready,
                "index_build_count": self.cache_manager.index_build_count,
            },
        )
        if not ready:
            self.cache_manager.restore(snapshot)
        return ready

    @staticmethod
    def _dedupe_families(records: list[ResolvedFamilyRecord]) -> list[ResolvedFamilyRecord]:
        deduped: dict[str, ResolvedFamilyRecord] = {}
        for record in records:
            deduped.setdefault(record.family_id, record)
        return [deduped[family_id] for family_id in sorted(deduped)]

    @staticmethod
    def _dedupe_functions(records: list[ResolvedFunctionRecord]) -> list[ResolvedFunctionRecord]:
        deduped: dict[str, ResolvedFunctionRecord] = {}
        for record in records:
            deduped.setdefault(record.function_id, record)
        return [deduped[function_id] for function_id in sorted(deduped)]
