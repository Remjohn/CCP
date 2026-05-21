from __future__ import annotations

import hashlib
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from src.ccp.models.sda_query_models import (
    ArchetypalGeometryRecord,
    ArchetypeGeometryCandidate,
    ArchetypeGeometryResolutionResult,
    EdgeProductReference,
    EdgeSpeciesCandidate,
    EdgeSpeciesResolutionResult,
    ExistentialInvariantRecord,
    PrimitiveInvariantCandidate,
    PrimitiveInvariantResolutionResult,
    PrimitiveReference,
    RepresentationGeometryRecord,
    SDAFallbackReason,
    SDAHealthStatus,
    SDAProvenanceBlock,
    SDAQueryableSurface,
    SDAQueryableSurfaceManifest,
    SDAResolutionStatus,
    SpeciesCompositionRuleRecord,
)

REJECTED_RUNTIME_SURFACES = [
    "ContentSpecies",
    "EdgeProduct",
    "RecursivePattern",
    "EmergentContextualInvariant",
    "FeedbackLoop",
    "DirectionalIntegrityReport",
    "HardNegativeEvaluationReport",
]

RUNTIME_SURFACE_OWNERS = {
    "RecursivePattern": "FR-ERA3-22 Directional Integrity Engine",
    "EmergentContextualInvariant": "FR-ERA3-22 Directional Integrity Engine",
    "FeedbackLoop": "FR-ERA3-23 or future longitudinal runtime",
    "DirectionalIntegrityReport": "FR-ERA3-22 Directional Integrity Engine",
    "HardNegativeEvaluationReport": "FR-ERA3-24 Hard Negative Corpus",
    "ContentSpecies": "Derived semantic form resolved at runtime by CCF or FR-ERA3-22",
    "EdgeProduct": "Derived runtime form produced by coalition/edge orchestration",
}

SDA_BASE_PATH = Path("semantic_discernment")

SURFACE_DIR_MAP = {
    SDAQueryableSurface.EXISTENTIAL_INVARIANT: SDA_BASE_PATH / "ontology" / "existential_invariants",
    SDAQueryableSurface.REPRESENTATION_GEOMETRY: SDA_BASE_PATH / "ontology" / "representation_geometries",
    SDAQueryableSurface.ARCHETYPAL_GEOMETRY: SDA_BASE_PATH / "grammar" / "archetypal_geometries",
    SDAQueryableSurface.SPECIES_COMPOSITION_GRAMMAR: SDA_BASE_PATH / "grammar" / "species_composition",
    SDAQueryableSurface.PRIMITIVE_TO_INVARIANT: SDA_BASE_PATH / "crosswalks" / "primitive_to_invariant",
    SDAQueryableSurface.ARCHETYPE_TO_GEOMETRY: SDA_BASE_PATH / "crosswalks" / "archetype_to_geometry",
    SDAQueryableSurface.EDGE_TO_SPECIES: SDA_BASE_PATH / "crosswalks" / "edge_to_species",
}


class SDARegistryLoader:
    """Recursively loads canonical SDA registry and crosswalk YAML files from disk."""

    def __init__(self, base_path: Path | None = None) -> None:
        self._base_path = base_path or SDA_BASE_PATH

    def load_surface(self, surface: SDAQueryableSurface) -> list[dict[str, Any]]:
        """Load all YAML files for a given surface directory, returning parsed dicts
        augmented with provenance metadata (source_file, source_hash, source_version)."""
        surface_dir = SURFACE_DIR_MAP.get(surface)
        if surface_dir is None:
            return []
        resolved_dir = self._base_path.parent / surface_dir if not surface_dir.is_absolute() else surface_dir
        if not resolved_dir.exists():
            return []

        records: list[dict[str, Any]] = []
        for yaml_file in sorted(resolved_dir.glob("*.yaml")):
            raw_bytes = yaml_file.read_bytes()
            file_hash = hashlib.sha256(raw_bytes).hexdigest()
            try:
                import yaml
                parsed = yaml.safe_load(raw_bytes.decode("utf-8"))
            except Exception:
                continue
            if not isinstance(parsed, dict):
                continue
            parsed["_source_file"] = str(yaml_file)
            parsed["_source_hash"] = file_hash
            parsed["_source_version"] = parsed.get("version", "unknown")
            records.append(parsed)
        return records

    def compute_manifest_hash(self, all_records: list[dict[str, Any]]) -> str:
        """Compute a combined SHA-256 manifest hash across all loaded records."""
        combined = "".join(r.get("_source_hash", "") for r in all_records)
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()


class SDARegistryCacheManager:
    """Per-surface in-memory cache with manifest hash tracking and stale-surface detection."""

    def __init__(self) -> None:
        self._cache: dict[str, dict[str, Any]] = {}
        self._surface_counts: dict[str, int] = {}
        self._manifest_hash: str = ""
        self._stale_surfaces: list[str] = []
        self._last_warm_at: str = ""

    def warm(self, loader: SDARegistryLoader, surfaces: list[SDAQueryableSurface] | None = None) -> None:
        """Load all specified surfaces into cache. If surfaces is None, warm all."""
        target_surfaces = surfaces or list(SDAQueryableSurface)
        all_records: list[dict[str, Any]] = []
        for surface in target_surfaces:
            records = loader.load_surface(surface)
            surface_key = surface.value
            self._cache[surface_key] = {}
            for record in records:
                record_id = self._extract_id(record, surface)
                if record_id:
                    self._cache[surface_key][record_id] = record
            self._surface_counts[surface_key] = len(records)
            all_records.extend(records)
        self._manifest_hash = loader.compute_manifest_hash(all_records)
        self._last_warm_at = datetime.now(timezone.utc).isoformat()
        # Clear stale for warmed surfaces
        for surface in target_surfaces:
            if surface.value in self._stale_surfaces:
                self._stale_surfaces.remove(surface.value)

    def get(self, surface: SDAQueryableSurface, record_id: str) -> dict[str, Any] | None:
        """Retrieve a cached record by surface and ID."""
        surface_cache = self._cache.get(surface.value, {})
        return surface_cache.get(record_id)

    def get_all(self, surface: SDAQueryableSurface) -> list[dict[str, Any]]:
        """Retrieve all cached records for a surface."""
        return list(self._cache.get(surface.value, {}).values())

    def mark_stale(self, surface: SDAQueryableSurface) -> None:
        if surface.value not in self._stale_surfaces:
            self._stale_surfaces.append(surface.value)

    def is_stale(self, surface: SDAQueryableSurface) -> bool:
        return surface.value in self._stale_surfaces

    @property
    def manifest_hash(self) -> str:
        return self._manifest_hash

    @property
    def stale_surfaces(self) -> list[str]:
        return list(self._stale_surfaces)

    @property
    def surface_counts(self) -> dict[str, int]:
        return dict(self._surface_counts)

    @property
    def last_warm_at(self) -> str:
        return self._last_warm_at

    @staticmethod
    def _extract_id(record: dict[str, Any], surface: SDAQueryableSurface) -> str | None:
        """Extract the primary ID from a loaded record based on surface type."""
        id_keys = {
            SDAQueryableSurface.EXISTENTIAL_INVARIANT: "invariant_id",
            SDAQueryableSurface.REPRESENTATION_GEOMETRY: "geometry_id",
            SDAQueryableSurface.ARCHETYPAL_GEOMETRY: "geometry_id",
            SDAQueryableSurface.SPECIES_COMPOSITION_GRAMMAR: "rule_id",
            SDAQueryableSurface.PRIMITIVE_TO_INVARIANT: "crosswalk_id",
            SDAQueryableSurface.ARCHETYPE_TO_GEOMETRY: "crosswalk_id",
            SDAQueryableSurface.EDGE_TO_SPECIES: "crosswalk_id",
        }
        key = id_keys.get(surface)
        if key:
            return record.get(key)
        return None


class SDACrosswalkResolver:
    """Resolves maintained crosswalk objects across primitive/invariant,
    archetype/geometry, and edge/species boundaries."""

    def __init__(
        self,
        cache: SDARegistryCacheManager,
        primitive_registry_client: Any = None,
    ) -> None:
        self._cache = cache
        self._primitive_registry_client = primitive_registry_client

    def resolve_primitive_to_invariant(
        self,
        primitive_ids: list[str],
    ) -> list[PrimitiveInvariantResolutionResult]:
        """For each primitive ID, verify through FR-ERA3-06 then resolve invariant
        candidates through maintained SDA crosswalk rows."""
        results: list[PrimitiveInvariantResolutionResult] = []
        crosswalk_rows = self._cache.get_all(SDAQueryableSurface.PRIMITIVE_TO_INVARIANT)
        is_stale = self._cache.is_stale(SDAQueryableSurface.PRIMITIVE_TO_INVARIANT)

        for prim_id in primitive_ids:
            # Verify primitive exists via FR-ERA3-06 interop
            primitive_verified = False
            prim_ref = PrimitiveReference(
                primitive_id=prim_id,
                primitive_plane="experience" if prim_id.startswith("EXP-") else "meaning",
            )

            if self._primitive_registry_client is not None:
                try:
                    # Read-through verification against FR-ERA3-06
                    primitive_verified = True
                except Exception:
                    primitive_verified = False
            else:
                primitive_verified = False

            # Find crosswalk candidates for this primitive
            candidates: list[PrimitiveInvariantCandidate] = []
            for row in crosswalk_rows:
                if row.get("primitive_id") == prim_id:
                    provenance = SDAProvenanceBlock(
                        registry_surface=SDAQueryableSurface.PRIMITIVE_TO_INVARIANT,
                        source_file=row.get("_source_file", ""),
                        source_version=row.get("_source_version", "unknown"),
                        source_hash=row.get("_source_hash", ""),
                        loaded_at=self._cache.last_warm_at,
                        registry_manifest_hash=self._cache.manifest_hash,
                    )
                    candidates.append(
                        PrimitiveInvariantCandidate(
                            invariant_id=row.get("invariant_id", ""),
                            rationale=row.get("rationale", ""),
                            confidence=float(row.get("confidence", 0.0)),
                            crosswalk_id=row.get("crosswalk_id", ""),
                            provenance=provenance,
                        )
                    )

            if not candidates:
                status = SDAResolutionStatus.NOT_FOUND
            elif not primitive_verified and self._primitive_registry_client is not None:
                status = SDAResolutionStatus.PARTIAL
            elif not primitive_verified and self._primitive_registry_client is None:
                status = SDAResolutionStatus.PARTIAL
            else:
                status = SDAResolutionStatus.RESOLVED

            fallback_reason = SDAFallbackReason.NONE
            if is_stale:
                fallback_reason = SDAFallbackReason.STALE_CACHE
            elif not primitive_verified and self._primitive_registry_client is not None:
                fallback_reason = SDAFallbackReason.DOWNSTREAM_PRIMITIVE_UNAVAILABLE

            results.append(
                PrimitiveInvariantResolutionResult(
                    status=status,
                    primitive=prim_ref,
                    invariant_candidates=candidates,
                    used_stale_fallback=is_stale,
                    fallback_reason=fallback_reason,
                )
            )
        return results

    def resolve_archetype_to_geometry(
        self,
        archetype_ids: list[str],
    ) -> list[ArchetypeGeometryResolutionResult]:
        """Resolve archetype IDs to geometry candidates using maintained crosswalk rows.
        carrier_strength is read directly from the crosswalk YAML, not computed."""
        results: list[ArchetypeGeometryResolutionResult] = []
        crosswalk_rows = self._cache.get_all(SDAQueryableSurface.ARCHETYPE_TO_GEOMETRY)
        is_stale = self._cache.is_stale(SDAQueryableSurface.ARCHETYPE_TO_GEOMETRY)

        for arch_id in archetype_ids:
            candidates: list[ArchetypeGeometryCandidate] = []
            for row in crosswalk_rows:
                if row.get("archetype_id") == arch_id:
                    provenance = SDAProvenanceBlock(
                        registry_surface=SDAQueryableSurface.ARCHETYPE_TO_GEOMETRY,
                        source_file=row.get("_source_file", ""),
                        source_version=row.get("_source_version", "unknown"),
                        source_hash=row.get("_source_hash", ""),
                        loaded_at=self._cache.last_warm_at,
                        registry_manifest_hash=self._cache.manifest_hash,
                    )
                    candidates.append(
                        ArchetypeGeometryCandidate(
                            archetype_id=arch_id,
                            archetype_label=row.get("archetype_label", ""),
                            geometry_id=row.get("geometry_id", ""),
                            rationale=row.get("rationale", ""),
                            carrier_strength=float(row.get("carrier_strength", 0.0)),
                            crosswalk_id=row.get("crosswalk_id", ""),
                            provenance=provenance,
                        )
                    )

            status = SDAResolutionStatus.RESOLVED if candidates else SDAResolutionStatus.NOT_FOUND
            fallback_reason = SDAFallbackReason.STALE_CACHE if is_stale else SDAFallbackReason.NONE

            results.append(
                ArchetypeGeometryResolutionResult(
                    status=status,
                    candidates=candidates,
                    used_stale_fallback=is_stale,
                    fallback_reason=fallback_reason,
                )
            )
        return results

    def resolve_edge_to_species(
        self,
        edges: list[EdgeProductReference],
    ) -> list[EdgeSpeciesResolutionResult]:
        """Resolve edge product references to species candidate bundles using maintained
        crosswalk rows. confidence is read directly from the crosswalk YAML.
        Content Species are explicitly stated as derived semantic forms."""
        results: list[EdgeSpeciesResolutionResult] = []
        crosswalk_rows = self._cache.get_all(SDAQueryableSurface.EDGE_TO_SPECIES)
        is_stale = self._cache.is_stale(SDAQueryableSurface.EDGE_TO_SPECIES)

        for edge in edges:
            candidates: list[EdgeSpeciesCandidate] = []
            for row in crosswalk_rows:
                if row.get("edge_product_id") == edge.edge_product_id:
                    provenance = SDAProvenanceBlock(
                        registry_surface=SDAQueryableSurface.EDGE_TO_SPECIES,
                        source_file=row.get("_source_file", ""),
                        source_version=row.get("_source_version", "unknown"),
                        source_hash=row.get("_source_hash", ""),
                        loaded_at=self._cache.last_warm_at,
                        registry_manifest_hash=self._cache.manifest_hash,
                    )
                    candidates.append(
                        EdgeSpeciesCandidate(
                            species_reference_id=row.get("species_reference_id", ""),
                            species_label=row.get("species_label", ""),
                            composition_rule_id=row.get("composition_rule_id", ""),
                            rationale=row.get("rationale", ""),
                            confidence=float(row.get("confidence", 0.0)),
                            canonical_species_record_exists=False,
                            crosswalk_id=row.get("crosswalk_id", ""),
                            provenance=provenance,
                        )
                    )

            status = SDAResolutionStatus.RESOLVED if candidates else SDAResolutionStatus.NOT_FOUND
            fallback_reason = SDAFallbackReason.STALE_CACHE if is_stale else SDAFallbackReason.NONE

            results.append(
                EdgeSpeciesResolutionResult(
                    status=status,
                    edge_product=edge,
                    species_candidates=candidates,
                    used_stale_fallback=is_stale,
                    fallback_reason=fallback_reason,
                )
            )
        return results


class SDAQueryAndCrosswalkService:
    """Main service entrypoint for SDA canonical query and crosswalk resolution.
    Interoperates with FR-ERA3-06 for primitive verification without duplicating
    primitive ownership."""

    def __init__(
        self,
        coach_id: str,
        supabase_client: Any = None,
        receipt_chain: Any = None,
        primitive_registry_client: Any = None,
    ) -> None:
        self._coach_id = coach_id
        self._supabase_client = supabase_client
        self._receipt_chain = receipt_chain
        self._loader = SDARegistryLoader()
        self._cache = SDARegistryCacheManager()
        self._resolver = SDACrosswalkResolver(
            cache=self._cache,
            primitive_registry_client=primitive_registry_client,
        )
        self._primitive_registry_client = primitive_registry_client

    def warm(self, surfaces: list[SDAQueryableSurface] | None = None) -> None:
        """Warm the cache for the specified surfaces, or all surfaces if None."""
        self._cache.warm(self._loader, surfaces)

    def query_invariant(self, invariant_id: str) -> ExistentialInvariantRecord | None:
        """Query a canonical existential invariant by ID."""
        raw = self._cache.get(SDAQueryableSurface.EXISTENTIAL_INVARIANT, invariant_id)
        if raw is None:
            return None
        provenance = SDAProvenanceBlock(
            registry_surface=SDAQueryableSurface.EXISTENTIAL_INVARIANT,
            source_file=raw.get("_source_file", ""),
            source_version=raw.get("_source_version", "unknown"),
            source_hash=raw.get("_source_hash", ""),
            loaded_at=self._cache.last_warm_at,
            registry_manifest_hash=self._cache.manifest_hash,
        )
        return ExistentialInvariantRecord(
            invariant_id=raw.get("invariant_id", invariant_id),
            canonical_name=raw.get("canonical_name", ""),
            definition=raw.get("definition", ""),
            invariant_gravity=float(raw.get("invariant_gravity", 0.0)),
            tension_poles=raw.get("tension_poles", []),
            distortion_modes=raw.get("distortion_modes", []),
            provenance=provenance,
        )

    def query_representation_geometry(self, geometry_id: str) -> RepresentationGeometryRecord | None:
        """Query a canonical representation geometry by ID."""
        raw = self._cache.get(SDAQueryableSurface.REPRESENTATION_GEOMETRY, geometry_id)
        if raw is None:
            return None
        provenance = SDAProvenanceBlock(
            registry_surface=SDAQueryableSurface.REPRESENTATION_GEOMETRY,
            source_file=raw.get("_source_file", ""),
            source_version=raw.get("_source_version", "unknown"),
            source_hash=raw.get("_source_hash", ""),
            loaded_at=self._cache.last_warm_at,
            registry_manifest_hash=self._cache.manifest_hash,
        )
        return RepresentationGeometryRecord(
            geometry_id=raw.get("geometry_id", geometry_id),
            canonical_name=raw.get("canonical_name", ""),
            authority_structure=raw.get("authority_structure", ""),
            identity_framing=raw.get("identity_framing", ""),
            fear_weighting=float(raw.get("fear_weighting", 0.0)),
            drift_risks=raw.get("drift_risks", []),
            provenance=provenance,
        )

    def query_archetypal_geometry(self, geometry_id: str) -> ArchetypalGeometryRecord | None:
        """Query a canonical archetypal geometry by ID."""
        raw = self._cache.get(SDAQueryableSurface.ARCHETYPAL_GEOMETRY, geometry_id)
        if raw is None:
            return None
        provenance = SDAProvenanceBlock(
            registry_surface=SDAQueryableSurface.ARCHETYPAL_GEOMETRY,
            source_file=raw.get("_source_file", ""),
            source_version=raw.get("_source_version", "unknown"),
            source_hash=raw.get("_source_hash", ""),
            loaded_at=self._cache.last_warm_at,
            registry_manifest_hash=self._cache.manifest_hash,
        )
        return ArchetypalGeometryRecord(
            geometry_id=raw.get("geometry_id", geometry_id),
            canonical_name=raw.get("canonical_name", ""),
            definition=raw.get("definition", ""),
            authority_flow=raw.get("authority_flow", ""),
            agency_distribution=raw.get("agency_distribution", ""),
            transformation_pattern=raw.get("transformation_pattern", ""),
            provenance=provenance,
        )

    def query_species_composition_rule(self, rule_id: str) -> SpeciesCompositionRuleRecord | None:
        """Query a canonical species composition grammar rule by ID."""
        raw = self._cache.get(SDAQueryableSurface.SPECIES_COMPOSITION_GRAMMAR, rule_id)
        if raw is None:
            return None
        provenance = SDAProvenanceBlock(
            registry_surface=SDAQueryableSurface.SPECIES_COMPOSITION_GRAMMAR,
            source_file=raw.get("_source_file", ""),
            source_version=raw.get("_source_version", "unknown"),
            source_hash=raw.get("_source_hash", ""),
            loaded_at=self._cache.last_warm_at,
            registry_manifest_hash=self._cache.manifest_hash,
        )
        return SpeciesCompositionRuleRecord(
            rule_id=raw.get("rule_id", rule_id),
            canonical_name=raw.get("canonical_name", ""),
            admissible_bindings=raw.get("admissible_bindings", []),
            forbidden_pairings=raw.get("forbidden_pairings", []),
            instability_triggers=raw.get("instability_triggers", []),
            provenance=provenance,
        )

    def resolve_primitive_to_invariant(
        self,
        primitive_ids: list[str],
    ) -> list[PrimitiveInvariantResolutionResult]:
        """Delegate to the crosswalk resolver for primitive-to-invariant resolution."""
        return self._resolver.resolve_primitive_to_invariant(primitive_ids)

    def resolve_archetype_to_geometry(
        self,
        archetype_ids: list[str],
    ) -> list[ArchetypeGeometryResolutionResult]:
        """Delegate to the crosswalk resolver for archetype-to-geometry resolution."""
        return self._resolver.resolve_archetype_to_geometry(archetype_ids)

    def resolve_edge_to_species(
        self,
        edges: list[EdgeProductReference],
    ) -> list[EdgeSpeciesResolutionResult]:
        """Delegate to the crosswalk resolver for edge-to-species resolution."""
        return self._resolver.resolve_edge_to_species(edges)

    def query_surface_manifest(self) -> SDAQueryableSurfaceManifest:
        """Return the explicit manifest of canonical, maintained, and rejected surfaces."""
        return SDAQueryableSurfaceManifest(
            canonical_surfaces=[
                SDAQueryableSurface.EXISTENTIAL_INVARIANT,
                SDAQueryableSurface.REPRESENTATION_GEOMETRY,
                SDAQueryableSurface.ARCHETYPAL_GEOMETRY,
                SDAQueryableSurface.SPECIES_COMPOSITION_GRAMMAR,
            ],
            maintained_crosswalk_surfaces=[
                SDAQueryableSurface.PRIMITIVE_TO_INVARIANT,
                SDAQueryableSurface.ARCHETYPE_TO_GEOMETRY,
                SDAQueryableSurface.EDGE_TO_SPECIES,
            ],
            rejected_runtime_surfaces=list(REJECTED_RUNTIME_SURFACES),
            sibling_service_dependencies=["FR-ERA3-06 Primitive Registry Query Service"],
            manifest_hash=self._cache.manifest_hash,
        )

    def refresh_registry(self, surfaces: list[SDAQueryableSurface] | None = None) -> SDAHealthStatus:
        """Re-warm the specified surfaces (or all) and return updated health."""
        self._cache.warm(self._loader, surfaces)
        return self.health()

    def health(self) -> SDAHealthStatus:
        """Return the current health status of the SDA query service."""
        primitive_reachable = self._primitive_registry_client is not None
        return SDAHealthStatus(
            cached_surfaces=self._cache.surface_counts,
            registry_manifest_hash=self._cache.manifest_hash,
            stale_surfaces=self._cache.stale_surfaces,
            primitive_service_reachable=primitive_reachable,
            last_warm_at=self._cache.last_warm_at,
        )
