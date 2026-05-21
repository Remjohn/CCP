from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.ccp.models.sda_query_models import (
    ArchetypalGeometryRecord,
    ArchetypeGeometryResolutionResult,
    EdgeProductReference,
    EdgeSpeciesResolutionResult,
    ExistentialInvariantRecord,
    PrimitiveInvariantResolutionResult,
    RepresentationGeometryRecord,
    SDAHealthStatus,
    SDAQueryableSurface,
    SDAQueryableSurfaceManifest,
    SDAResolutionStatus,
    SpeciesCompositionRuleRecord,
)
from src.ccp.services.sda_query_service import (
    RUNTIME_SURFACE_OWNERS,
    SDAQueryAndCrosswalkService,
)

router = APIRouter()


# --- Request bodies ---

class PrimitiveToInvariantRequest(BaseModel):
    primitive_ids: list[str] = Field(..., min_length=1)


class ArchetypeToGeometryRequest(BaseModel):
    archetype_ids: list[str] = Field(..., min_length=1)


class EdgeToSpeciesRequest(BaseModel):
    edges: list[EdgeProductReference] = Field(..., min_length=1)


class RefreshRequest(BaseModel):
    surfaces: list[SDAQueryableSurface] | None = None


# --- Canonical query routes ---

@router.get("/sda/invariants/{invariant_id}", response_model=ExistentialInvariantRecord)
async def get_invariant(invariant_id: str):
    """Query a canonical existential invariant by ID."""
    pass


@router.get("/sda/representation-geometries/{geometry_id}", response_model=RepresentationGeometryRecord)
async def get_representation_geometry(geometry_id: str):
    """Query a canonical representation geometry by ID."""
    pass


@router.get("/sda/archetypal-geometries/{geometry_id}", response_model=ArchetypalGeometryRecord)
async def get_archetypal_geometry(geometry_id: str):
    """Query a canonical archetypal geometry by ID."""
    pass


@router.get("/sda/species-composition-rules/{rule_id}", response_model=SpeciesCompositionRuleRecord)
async def get_species_composition_rule(rule_id: str):
    """Query a canonical species composition grammar rule by ID."""
    pass


# --- Crosswalk resolution routes ---

@router.post(
    "/sda/crosswalks/primitive-to-invariant/resolve",
    response_model=list[PrimitiveInvariantResolutionResult],
)
async def resolve_primitive_to_invariant(request: PrimitiveToInvariantRequest):
    """Resolve primitive IDs to invariant candidates through maintained crosswalk rows.
    Verifies primitives through FR-ERA3-06 before yielding candidates."""
    pass


@router.post(
    "/sda/crosswalks/archetype-to-geometry/resolve",
    response_model=list[ArchetypeGeometryResolutionResult],
)
async def resolve_archetype_to_geometry(request: ArchetypeToGeometryRequest):
    """Resolve archetype IDs to geometry candidates using maintained carrier mappings.
    carrier_strength is read from crosswalk YAML, not computed dynamically."""
    pass


@router.post(
    "/sda/crosswalks/edge-to-species/resolve",
    response_model=list[EdgeSpeciesResolutionResult],
)
async def resolve_edge_to_species(request: EdgeToSpeciesRequest):
    """Resolve edge product references to species candidate bundles.
    Content Species are explicitly derived semantic forms, not canonical registry rows."""
    pass


# --- Surface manifest, health, and refresh routes ---

@router.get("/sda/queryable-surfaces", response_model=SDAQueryableSurfaceManifest)
async def get_queryable_surfaces():
    """Return the explicit manifest of canonical, maintained, and rejected surfaces."""
    pass


@router.get("/sda/health", response_model=SDAHealthStatus)
async def get_health():
    """Return the current health status of the SDA query service."""
    pass


@router.post("/sda/refresh", response_model=SDAHealthStatus)
async def refresh_registry(request: RefreshRequest):
    """Re-warm specified SDA surfaces. Internal maintenance endpoint."""
    pass
