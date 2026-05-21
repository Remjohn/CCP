# FR-ERA3-34 Phase-0 Prospect Workspace and Artifact Store Tech Spec

## Pre-Work Log

### Prompt File
- `docs/architecture/april_updates/spec_prompts/P0_S02_FR-ERA3-34_Phase0_Prospect_Workspace_And_Artifact_Store.md`

### Protocol
- `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` — 10-section format, mandatory pre-flight, existing backend integration required.

### Source PRDs

**PRD-09 §1.3A (lines 1216-1222):**
> "Introduce a lightweight `Trial Phase-0` delivery runtime that lets CCP ingest a prospect's existing material inside a shared pre-container workspace and output audits, previews, first-proof assets, and payment links within `24h max`, without requiring full per-coach container provisioning or expensive custom model setup first."

**PRD-01 §5.2 (lines 312-318):**
> "CCP commits to single-tenant repositories and cloud-native, isolated deployment per coach to maintain data privacy and systemic stability... Per-coach PostgreSQL schemas with row-level security (RLS) enforced at the middleware layer."

**Bridge:** PRD-09 §1.3A explicitly defines Phase-0 as a pre-container shared workspace. PRD-01 §5.2 defines the full single-tenant target. This spec defines the workspace and artifact store that sits between intake (FR-ERA3-33) and the full container (PRD-01 §5.2), bridging them via a deterministic migration path.

### Mandatory Phase-0 Source Set — Key Claims

**PRD-09 (line 1219):**
> "The system needs a rapid package-delivery layer before the deeper sovereign container investment."

**PRD-01 (line 43):**
> "AI remains permanently backstage — serving as the refiner, router, benchmarker, memory layer, quality-control layer, and orchestration engine."

**Fladlien Sales Insights (line 11):**
> "Let them DO what they already do (talk/create content) → score them → show them the damage → let the metrics sell."

**Biological Orchestration Model (line 81):**
> "`DNA -> RNA -> force -> delivery -> variation -> phenotype -> evaluation`"

**CCP System Documentation (line 253):**
> "The entire infrastructure demands strict Single-Tenant Architecture (ADR-01). Each coach operates in a completely isolated, containerized cloud environment."

### Existing Backend References

**`src/ccp/core/receipt_chain.py` — ReceiptChain.log():**
```python
def log(self, agent_id: str, action: str, asset_id: Optional[str] = None,
        person_id: Optional[str] = None, input_summary: str = "",
        output_summary: str = "", decision: Optional[str] = None,
        decision_rationale: Optional[str] = None,
        parent_receipt_id: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None) -> ReceiptEntry:
```

**`src/ccp/core/asset_id.py` — AssetIDGenerator.generate():**
```python
def generate(self, asset_type: AssetType, timestamp: Optional[datetime] = None) -> str:
```

**`src/ccp/services/affine_client_workspace.py` — ClientWorkspaceProvisioner:**
```python
async def provision_client_workspace(self, client_id, program_id, coach_theme_file, ...):
```

**`src/ccp/services/payment_eligibility_service.py` — PaymentEligibilityService:**
```python
async def check_eligibility(self, *, telegram_user_id: int, coach_id: str,
                            target_tier: PaymentTier) -> EligibilityCheckResult:
```

### Existing Models Read
- `ReceiptEntry` — Pydantic v2, append-only audit entry with `receipt_id`, `agent_id`, `action`, `asset_id`, `metadata`.
- `AssetID` / `AssetType` — 34 registered types with `AAAA-CCC-MM-YY-XXXX` format.
- `Phase0ProspectPacket` — defined in FR-ERA3-33, the canonical intake handoff model.
- `ConversionSequencePayloadRow` — CPSC conversion routing with receipt chain integration.

### Existing Test Patterns Read

**`tests/integration/test_cpsc_fr53_conversion_sequence.py`:**
- Uses `tmp_path` fixture for isolated receipt chain directories.
- Validates receipt entries via `rc.query(action="...")`.
- Tests boundary conditions, enum integrity, and ADR-01 isolation.

**`tests/integration/test_era3_fr02_payment_eligibility.py`:**
- Skeleton tests for stored value resolution, eligibility gate, and receipt logging.
- Confirms pattern: service → gate → receipt → result.

### Deployment Boundary Confirmation
- **Full containerization assumed by:** `affine_client_workspace.py`, `single_tenant_deployment_service.py`, `affine_workspace_provisioner.py`, `scaffold_coach.py` — all require a bound `coach_acronym` and per-coach PostgreSQL schema.
- **Phase-0 must remain lighter-weight:** No per-prospect PostgreSQL schema. No per-prospect Redis namespace. No custom model fine-tuning. Shared `phase0_` table prefix in the main CCP database. Receipt chain uses a shared `P0W` coach acronym until migration.

### Sibling Spec Relationship
- **FR-ERA3-33** (Intake Console) emits `Phase0ProspectPacket` — this spec receives it.
- **FR-ERA3-35** (Audit Intelligence Engine) consumes artifacts from this workspace.
- **FR-ERA3-36** (Delivery Orchestrator) reads artifact manifests from this store.
- **FR-ERA3-37** (Commercial Bridge) triggers payment-unlocked state transitions.

---

## 1. Files Read

| # | File | Purpose |
|---|---|---|
| 1 | `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md` | Commercial ladder, Phase-0 mandate |
| 2 | `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md` | Sovereign data architecture, single-tenant target |
| 3 | `lab/CCP APRIL Updates/Fladlien_Sales_Insights.md` | Proof-first conversion doctrine |
| 4 | `lab/ccp_biological_orchestration_model_v_1.md` | Runtime organism model |
| 5 | `lab/CCP APRIL Updates/01_Architecture_PRDs/CCP_System_Documentation.md` | System architecture overview |
| 6 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Spec writing protocol |
| 7 | `docs/architecture/april_updates/FR-ERA3-33_Phase0_Prospect_Intake_Console_Tech_Spec.md` | Sibling intake spec |
| 8 | `src/ccp/core/receipt_chain.py` | Receipt chain implementation |
| 9 | `src/ccp/core/asset_id.py` | Universal Asset ID generation |
| 10 | `src/ccp/services/affine_client_workspace.py` | Existing workspace provisioning |
| 11 | `src/ccp/services/payment_eligibility_service.py` | Payment eligibility patterns |
| 12 | `src/ccp/services/conversion_sequence_router.py` | Conversion routing patterns |
| 13 | `src/ccp/scripts/setup_supabase.py` | Database schema patterns |
| 14 | `tests/integration/test_cpsc_fr53_conversion_sequence.py` | Test patterns for state machines |
| 15 | `tests/integration/test_era3_fr02_payment_eligibility.py` | Test patterns for payment flows |

---

## 2. Overview

### 2.1 Objective
Define the Phase-0 Prospect Workspace and Artifact Store — a shared, pre-container, bounded substrate that manages the full lifecycle of prospect artifacts from intake through audit, preview, production, payment handoff, and upgrade migration. This workspace is the storage and state-management backbone for all Phase-0 commercial operations.

### 2.2 Problem
CCP's production architecture assumes per-coach single-tenant containers (PRD-01 §5.2). But the commercial reality demands proof delivery before payment (PRD-09 §1.3A). There is no intermediate storage substrate that can:
- hold prospect artifacts across the full proof lifecycle
- enforce artifact lineage without per-coach infrastructure
- support 24h delivery SLAs without custom model provisioning
- define a deterministic migration path into full tenancy after conversion

### 2.3 Solution
A shared PostgreSQL-backed workspace with strict logical isolation by `prospect_id`, a canonical artifact state machine, receipt-chain-integrated lineage tracking, and a formal migration protocol that transfers workspace contents into a dedicated coach container upon continuity conversion.

### 2.4 Scope
**In scope:**
- Workspace record lifecycle (create → active → delivered → payment-unlocked → upgraded / archived)
- Artifact record lifecycle (uploaded → normalized → audit-ready → preview-ready → delivered → payment-unlocked → upgraded / handed-off)
- Artifact manifest assembly and lineage preservation
- Readiness state computation
- Upgrade bridge state management
- Migration path definition
- Receipt chain integration for all state transitions

**Out of scope:**
- Intake capture logic (FR-ERA3-33)
- Audit scoring logic (FR-ERA3-35)
- Delivery orchestration (FR-ERA3-36)
- Payment capture (FR-ERA3-37)
- Operator console UI (FR-ERA3-38)

---

## 3. Context for Development

### 3.1 Architecture Traceability (DEP-IDs)

| DEP-ID | Object | Type | Status |
|---|---|---|---|
| DEP-P0W-001 | `Phase0WorkspaceRecord` | Pydantic model | NEW |
| DEP-P0W-002 | `Phase0ArtifactRecord` | Pydantic model | NEW |
| DEP-P0W-003 | `Phase0ArtifactManifest` | Pydantic model | NEW |
| DEP-P0W-004 | `Phase0WorkspaceStatus` | Enum | NEW |
| DEP-P0W-005 | `Phase0ArtifactStatus` | Enum | NEW |
| DEP-P0W-006 | `Phase0ReadinessState` | Pydantic model | NEW |
| DEP-P0W-007 | `Phase0UpgradeBridgeState` | Pydantic model | NEW |
| DEP-P0W-008 | `phase0_workspaces` | PostgreSQL table | NEW |
| DEP-P0W-009 | `phase0_artifacts` | PostgreSQL table | NEW |
| DEP-P0W-010 | `phase0_artifact_manifests` | PostgreSQL table | NEW |
| DEP-P0W-011 | `phase0_upgrade_bridges` | PostgreSQL table | NEW |
| DEP-P0W-012 | `Phase0WorkspaceService` | Python service | NEW |
| DEP-P0W-013 | `Phase0ArtifactStore` | Python service | NEW |
| DEP-P0W-014 | `Phase0MigrationService` | Python service | NEW |

### 3.2 Existing Backend Integration

| File | Integration Point |
|---|---|
| `src/ccp/core/receipt_chain.py` | All workspace and artifact state transitions log receipts via `ReceiptChain.log()` |
| `src/ccp/core/asset_id.py` | Artifact records use `AssetIDGenerator.generate()` with new `AssetType.PHASE0_ARTIFACT = "P0AF"` |
| `src/ccp/services/affine_client_workspace.py` | Migration service reuses provisioning patterns from `ClientWorkspaceProvisioner` |
| `src/ccp/services/payment_eligibility_service.py` | Upgrade bridge reads eligibility verdict before allowing `payment-unlocked` transition |
| `src/ccp/scripts/setup_supabase.py` | New tables added to the shared schema migration script |

### 3.3 Packets, Artifacts, and Stores

**Upstream packet:** `Phase0ProspectPacket` (from FR-ERA3-33) — the typed intake handoff that seeds workspace creation.

**Artifacts stored in this workspace:**
- `intake_source` — raw uploads and references from the intake console
- `normalized_source` — transcoded, checksummed, metadata-enriched versions
- `audit_report` — PDF and video audit outputs from FR-ERA3-35
- `preview_asset` — watermarked or gated preview renderings
- `produced_proof` — final proof-package assets (explainers, cinematics, carousels)
- `payment_bridge` — payment link metadata and commercial bridge artifacts
- `upgrade_metadata` — migration manifests and container handoff records

**Storage backend:** Supabase PostgreSQL (shared main database, `phase0_` table prefix) + Supabase Storage bucket `phase0-artifacts` (private, RLS-enforced).

### 3.4 Governance Constraints (CBAR Mandates)

| Mandate | Enforcement Mechanism |
|---|---|
| **Shared-Workspace-First Rule** | All Phase-0 operations run in shared `phase0_` tables. No per-prospect schema or Redis namespace. Workspace isolation is logical via `prospect_id` column and RLS policies. |
| **No-Full-Container-Before-Payment Rule** | `Phase0WorkspaceStatus` cannot transition to `upgraded` until `Phase0UpgradeBridgeState.payment_confirmed = True`. Migration service hard-rejects container provisioning without payment confirmation. |
| **Artifact-Lineage Rule** | Every `Phase0ArtifactRecord` carries `parent_artifact_ids` and `source_receipt_id`. No artifact may exist without a traceable lineage chain back to an intake source. Orphaned artifacts are rejected at insert. |
| **24h Delivery Readiness Rule** | `Phase0ReadinessState` computes `delivery_window_status` from artifact state machine. Workspace cannot emit `delivered` status if any required artifact family is below `preview-ready`. |
| **Human-Review Recovery Rule** | Any artifact in `rejected` or `quarantined` state blocks workspace progression. Human operator must explicitly acknowledge and resolve via a receipt-logged action before the workspace can advance. |

### 3.5 Technical Decisions

| Decision | Rationale |
|---|---|
| **Shared PostgreSQL tables with RLS** | Phase-0 is pre-container. Per-prospect schemas would violate the lightweight mandate. RLS on `prospect_id` provides isolation without infrastructure cost. |
| **Deterministic artifact state machine** | Seven canonical states with explicit allowed transitions. No implicit state changes. Every transition requires a receipt entry. |
| **Manifest-based artifact grouping** | Artifacts are individually tracked but grouped into manifests for delivery. This allows partial delivery, re-delivery after revision, and selective migration. |
| **Shared `P0W` coach acronym for receipts** | Phase-0 receipts use a system-level acronym `P0W` since no real coach acronym exists yet. Migration remaps receipts to the assigned coach acronym. |
| **Migration as copy-then-archive** | Workspace contents are copied into the new coach container, then the Phase-0 workspace is archived (not deleted). This preserves audit trail and allows rollback. |

---

## 4. Implementation Plan

### Phase 1: Foundation (Tasks 1-4)

**Task 1:** Define all Pydantic v2 models in `src/ccp/models/phase0_workspace_models.py`.
- `Phase0WorkspaceStatus` enum
- `Phase0ArtifactStatus` enum
- `Phase0ArtifactFamily` enum
- `Phase0WorkspaceRecord` model
- `Phase0ArtifactRecord` model
- `Phase0ArtifactManifest` model
- `Phase0ReadinessState` model
- `Phase0UpgradeBridgeState` model

**Task 2:** Add `AssetType.PHASE0_ARTIFACT = "P0AF"` to `src/ccp/core/asset_id.py`.

**Task 3:** Add PostgreSQL table definitions to `src/ccp/scripts/setup_supabase.py`:
- `phase0_workspaces`
- `phase0_artifacts`
- `phase0_artifact_manifests`
- `phase0_upgrade_bridges`

**Task 4:** Add Supabase Storage bucket configuration for `phase0-artifacts`.

### Phase 2: Workspace Service (Tasks 5-8)

**Task 5:** Implement `Phase0WorkspaceService` in `src/ccp/services/phase0_workspace_service.py`.
- `create_workspace(prospect_packet: Phase0ProspectPacket) -> Phase0WorkspaceRecord`
- `get_workspace(workspace_id: str) -> Phase0WorkspaceRecord`
- `transition_workspace(workspace_id: str, target_status: Phase0WorkspaceStatus) -> Phase0WorkspaceRecord`
- `compute_readiness(workspace_id: str) -> Phase0ReadinessState`

**Task 6:** Implement `Phase0ArtifactStore` in `src/ccp/services/phase0_artifact_store.py`.
- `register_artifact(workspace_id, family, source_receipt_id, ...) -> Phase0ArtifactRecord`
- `transition_artifact(artifact_id, target_status) -> Phase0ArtifactRecord`
- `get_artifacts_by_workspace(workspace_id) -> list[Phase0ArtifactRecord]`
- `get_artifacts_by_family(workspace_id, family) -> list[Phase0ArtifactRecord]`

**Task 7:** Implement artifact state machine validation inside `Phase0ArtifactStore`.
- Enforce allowed transitions: `uploaded → normalized → audit-ready → preview-ready → delivered → payment-unlocked → upgraded`
- Reject illegal transitions with `ValueError` and receipt-logged rejection.
- Support `quarantined` state reachable from any state except `upgraded`.

**Task 8:** Implement manifest assembly in `Phase0ArtifactStore`.
- `assemble_manifest(workspace_id) -> Phase0ArtifactManifest`
- Groups artifacts by family, validates completeness, computes readiness.

### Phase 3: Upgrade Bridge and Migration (Tasks 9-11)

**Task 9:** Implement `Phase0UpgradeBridgeState` management.
- `initiate_upgrade_bridge(workspace_id, target_tier) -> Phase0UpgradeBridgeState`
- `confirm_payment(bridge_id, payment_receipt_id) -> Phase0UpgradeBridgeState`
- `abort_upgrade(bridge_id, reason) -> Phase0UpgradeBridgeState`

**Task 10:** Implement `Phase0MigrationService` in `src/ccp/services/phase0_migration_service.py`.
- `migrate_to_container(workspace_id, coach_acronym) -> MigrationResult`
- Copies artifacts to coach-specific storage.
- Remaps asset IDs from `P0AF-P0W-...` to coach-bound IDs.
- Archives the Phase-0 workspace.
- Logs full migration receipt chain.

**Task 11:** Integrate migration service with existing `ClientWorkspaceProvisioner` patterns.
- Reuse theme application and block provisioning from `affine_client_workspace.py`.
- Extend `scaffold_coach.py` to accept Phase-0 migration source.

### Phase 4: API and Integration (Tasks 12-15)

**Task 12:** Create FastAPI router `src/ccp/api/phase0_workspace.py`.
- `POST /phase0/workspaces` — create from prospect packet
- `GET /phase0/workspaces/{workspace_id}` — retrieve workspace state
- `GET /phase0/workspaces/{workspace_id}/artifacts` — list artifacts
- `POST /phase0/workspaces/{workspace_id}/artifacts` — register artifact
- `PATCH /phase0/workspaces/{workspace_id}/artifacts/{artifact_id}/status` — transition
- `GET /phase0/workspaces/{workspace_id}/manifest` — assemble manifest
- `GET /phase0/workspaces/{workspace_id}/readiness` — compute readiness
- `POST /phase0/workspaces/{workspace_id}/upgrade-bridge` — initiate upgrade

**Task 13:** Mount router in `src/ccp/api/main.py`.

**Task 14:** Add receipt chain integration for all state transitions.
- Actions: `PHASE0-WORKSPACE-CREATE`, `PHASE0-ARTIFACT-REGISTER`, `PHASE0-ARTIFACT-TRANSITION`, `PHASE0-MANIFEST-ASSEMBLE`, `PHASE0-READINESS-COMPUTE`, `PHASE0-UPGRADE-INITIATE`, `PHASE0-PAYMENT-CONFIRM`, `PHASE0-MIGRATION-EXECUTE`

**Task 15:** Write integration tests in `tests/integration/test_era3_fr34_phase0_workspace.py`.

---

## 5. Primary Output Schema (Pydantic v2)

### 5.1 Enum: `Phase0WorkspaceStatus`

```python
class Phase0WorkspaceStatus(str, Enum):
    CREATED = "created"
    INTAKE_RECEIVED = "intake_received"
    ARTIFACTS_COLLECTING = "artifacts_collecting"
    AUDIT_IN_PROGRESS = "audit_in_progress"
    PREVIEW_READY = "preview_ready"
    DELIVERED = "delivered"
    PAYMENT_UNLOCKED = "payment_unlocked"
    UPGRADED = "upgraded"
    ARCHIVED = "archived"
    BLOCKED = "blocked"
```

**Allowed transitions:**
```
created → intake_received
intake_received → artifacts_collecting
artifacts_collecting → audit_in_progress
audit_in_progress → preview_ready
preview_ready → delivered
delivered → payment_unlocked
payment_unlocked → upgraded
upgraded → archived
{any except upgraded, archived} → blocked
blocked → {previous state via human-review recovery}
```

### 5.2 Enum: `Phase0ArtifactStatus`

```python
class Phase0ArtifactStatus(str, Enum):
    UPLOADED = "uploaded"
    NORMALIZED = "normalized"
    AUDIT_READY = "audit_ready"
    PREVIEW_READY = "preview_ready"
    DELIVERED = "delivered"
    PAYMENT_UNLOCKED = "payment_unlocked"
    UPGRADED = "upgraded"
    QUARANTINED = "quarantined"
    REJECTED = "rejected"
```

**Allowed transitions:**
```
uploaded → normalized
normalized → audit_ready
audit_ready → preview_ready
preview_ready → delivered
delivered → payment_unlocked
payment_unlocked → upgraded
{any except upgraded} → quarantined
quarantined → {previous state via human-review}
{any except upgraded} → rejected
```

### 5.3 Enum: `Phase0ArtifactFamily`

```python
class Phase0ArtifactFamily(str, Enum):
    INTAKE_SOURCE = "intake_source"
    NORMALIZED_SOURCE = "normalized_source"
    AUDIT_REPORT = "audit_report"
    PREVIEW_ASSET = "preview_asset"
    PRODUCED_PROOF = "produced_proof"
    PAYMENT_BRIDGE = "payment_bridge"
    UPGRADE_METADATA = "upgrade_metadata"
```

### 5.4 Enum: `Phase0DeliveryWindowStatus`

```python
class Phase0DeliveryWindowStatus(str, Enum):
    NOT_STARTED = "not_started"
    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    BREACHED = "breached"
    DELIVERED = "delivered"
```

### 5.5 Model: `Phase0WorkspaceRecord`

```python
class Phase0WorkspaceRecord(BaseModel):
    workspace_id: str = Field(..., description="UUID v4 workspace identifier")
    prospect_id: str = Field(..., description="Bound prospect from FR-ERA3-33")
    prospect_packet_id: str = Field(..., description="Source Phase0ProspectPacket.packet_id")
    coach_id: Optional[str] = Field(default=None, description="Coach ID if known at intake")
    display_name: str = Field(..., min_length=1, max_length=200)
    status: Phase0WorkspaceStatus = Field(default=Phase0WorkspaceStatus.CREATED)
    artifact_count: int = Field(default=0, ge=0)
    campaign_id: Optional[str] = Field(default=None)
    delivery_sla_deadline_utc: Optional[str] = Field(
        default=None, description="ISO 8601 UTC deadline for 24h delivery SLA"
    )
    created_at: str = Field(..., description="ISO 8601 UTC")
    updated_at: str = Field(..., description="ISO 8601 UTC")
    created_by_receipt_id: str = Field(..., description="Receipt ID of creation action")
    last_transition_receipt_id: Optional[str] = Field(default=None)
```

### 5.6 Model: `Phase0ArtifactRecord`

```python
class Phase0ArtifactRecord(BaseModel):
    artifact_id: str = Field(..., description="Universal Asset ID (P0AF-P0W-MM-YY-XXXX)")
    workspace_id: str = Field(...)
    prospect_id: str = Field(...)
    family: Phase0ArtifactFamily = Field(...)
    status: Phase0ArtifactStatus = Field(default=Phase0ArtifactStatus.UPLOADED)
    display_label: str = Field(..., min_length=1, max_length=300)
    mime_type: Optional[str] = Field(default=None)
    file_size_bytes: Optional[int] = Field(default=None, ge=0)
    storage_uri: Optional[str] = Field(default=None, description="Supabase Storage path")
    checksum_sha256: Optional[str] = Field(default=None)
    parent_artifact_ids: list[str] = Field(
        default_factory=list, description="Lineage: IDs of source artifacts"
    )
    source_receipt_id: str = Field(..., description="Receipt ID that created this artifact")
    metadata: dict[str, str] = Field(default_factory=dict)
    created_at: str = Field(...)
    updated_at: str = Field(...)
    transitioned_at: Optional[str] = Field(default=None)
    transition_receipt_id: Optional[str] = Field(default=None)
```

### 5.7 Model: `Phase0ArtifactManifest`

```python
class Phase0ArtifactManifest(BaseModel):
    manifest_id: str = Field(..., description="UUID v4")
    workspace_id: str = Field(...)
    prospect_id: str = Field(...)
    assembled_at: str = Field(..., description="ISO 8601 UTC")
    assembly_receipt_id: str = Field(...)
    intake_sources: list[str] = Field(default_factory=list, description="Artifact IDs")
    normalized_sources: list[str] = Field(default_factory=list)
    audit_reports: list[str] = Field(default_factory=list)
    preview_assets: list[str] = Field(default_factory=list)
    produced_proofs: list[str] = Field(default_factory=list)
    payment_bridges: list[str] = Field(default_factory=list)
    upgrade_metadata_refs: list[str] = Field(default_factory=list)
    total_artifact_count: int = Field(..., ge=0)
    completeness_summary: dict[str, str] = Field(
        default_factory=dict,
        description="Per-family completeness: 'present' | 'missing' | 'partial'"
    )
    is_delivery_ready: bool = Field(default=False)
    is_payment_bridge_ready: bool = Field(default=False)
```

### 5.8 Model: `Phase0ReadinessState`

```python
class Phase0ReadinessState(BaseModel):
    workspace_id: str = Field(...)
    prospect_id: str = Field(...)
    workspace_status: Phase0WorkspaceStatus = Field(...)
    delivery_window_status: Phase0DeliveryWindowStatus = Field(...)
    sla_deadline_utc: Optional[str] = Field(default=None)
    hours_remaining: Optional[float] = Field(default=None, ge=0.0)
    blocking_families: list[str] = Field(
        default_factory=list,
        description="Artifact families that block delivery"
    )
    warning_families: list[str] = Field(default_factory=list)
    quarantined_artifact_ids: list[str] = Field(default_factory=list)
    rejected_artifact_ids: list[str] = Field(default_factory=list)
    human_review_required: bool = Field(default=False)
    readiness_summary: str = Field(default="")
    computed_at: str = Field(...)
    computation_receipt_id: str = Field(...)
```

### 5.9 Model: `Phase0UpgradeBridgeState`

```python
class Phase0UpgradeBridgeState(BaseModel):
    bridge_id: str = Field(..., description="UUID v4")
    workspace_id: str = Field(...)
    prospect_id: str = Field(...)
    target_tier: str = Field(..., description="speaking_learning | coach_os | operator")
    payment_confirmed: bool = Field(default=False)
    payment_receipt_id: Optional[str] = Field(default=None)
    payment_amount_cents: Optional[int] = Field(default=None, ge=0)
    credit_applied_cents: Optional[int] = Field(
        default=None, ge=0,
        description="$29.99 credit applied toward upgrade per PRD-09 §V"
    )
    migration_status: str = Field(
        default="pending",
        description="pending | in_progress | completed | failed | aborted"
    )
    target_coach_acronym: Optional[str] = Field(
        default=None, min_length=3, max_length=3
    )
    migration_receipt_id: Optional[str] = Field(default=None)
    initiated_at: str = Field(...)
    confirmed_at: Optional[str] = Field(default=None)
    completed_at: Optional[str] = Field(default=None)
    abort_reason: Optional[str] = Field(default=None)
```

---

## 6. Backward Compatibility Fallback

### 6.1 Workspace Creation Fallback
If `Phase0ProspectPacket` is malformed or missing required fields, `Phase0WorkspaceService.create_workspace()` must:
1. Log a `PHASE0-WORKSPACE-CREATE-FAIL` receipt with the rejection reason.
2. Return HTTP 422 with body `{ "error": "WORKSPACE_CREATE_REJECTED", "reason": "<detail>" }`.
3. Never persist a partial workspace record.

**Failure example:** Intake packet arrives with `prospect_id = ""`. Service logs receipt `decision = "rejected"`, `decision_rationale = "prospect_id is empty"`. No row written to `phase0_workspaces`.

### 6.2 Artifact State Machine Fallback
If an illegal transition is attempted (e.g., `uploaded → delivered`):
1. Raise `ValueError("ILLEGAL_ARTIFACT_TRANSITION: uploaded → delivered. Required path: uploaded → normalized → audit_ready → preview_ready → delivered")`.
2. Log receipt `action = "PHASE0-ARTIFACT-TRANSITION-FAIL"`, `decision = "rejected"`.
3. Leave artifact in its current state — never write a partial update.

**Failure example:** FR-ERA3-35 attempts to mark an `intake_source` artifact as `delivered` without normalizing. Store rejects. Artifact remains `uploaded`.

### 6.3 Migration Guard Fallback
If `migrate_to_container()` is called without `payment_confirmed = True`:
1. Raise `PermissionError("MIGRATION_BLOCKED: No-Full-Container-Before-Payment Rule violated. payment_confirmed=False for bridge_id={bridge_id}")`.
2. Log receipt `action = "PHASE0-MIGRATION-BLOCKED"`, `decision = "rejected"`.
3. Do NOT touch any container provisioning code.

**Failure example:** Operator triggers migration before payment webhook fires. `bridge.payment_confirmed = False`. Hard rejection. Zero infra resources touched.

### 6.4 SLA Breach Fallback
If `compute_readiness()` detects `hours_remaining <= 0` and workspace is not `delivered`:
1. Set `delivery_window_status = BREACHED`.
2. Set `human_review_required = True`.
3. Log receipt `action = "PHASE0-SLA-BREACH"`.
4. Do NOT auto-archive. Human must explicitly resolve.

### 6.5 Quarantine Recovery Protocol
When operator resolves a `quarantined` artifact:
1. Call `PATCH /phase0/workspaces/{id}/artifacts/{artifact_id}/status` with `{ "target_status": "normalized", "human_review_note": "<non-empty reason>" }`.
2. Service validates `human_review_note` is non-empty — rejects if blank.
3. Logs receipt `action = "PHASE0-ARTIFACT-HUMAN-RECOVERY"`, `decision = "approved"`.
4. Re-evaluates workspace readiness.

---

## 7. Tasks

| # | Task | File | Priority |
|---|---|---|---|
| T-01 | Define all enums + Pydantic v2 models | `src/ccp/models/phase0_workspace_models.py` | P0 |
| T-02 | Add `AssetType.PHASE0_ARTIFACT = "P0AF"` | `src/ccp/core/asset_id.py` | P0 |
| T-03 | Add `phase0_workspaces` SQL to setup_supabase.py | `src/ccp/scripts/setup_supabase.py` | P0 |
| T-04 | Add `phase0_artifacts` SQL | `src/ccp/scripts/setup_supabase.py` | P0 |
| T-05 | Add `phase0_artifact_manifests` SQL | `src/ccp/scripts/setup_supabase.py` | P0 |
| T-06 | Add `phase0_upgrade_bridges` SQL | `src/ccp/scripts/setup_supabase.py` | P0 |
| T-07 | Implement `Phase0WorkspaceService.create_workspace()` | `src/ccp/services/phase0_workspace_service.py` | P1 |
| T-08 | Implement `transition_workspace()` with allowed-transition guard | `src/ccp/services/phase0_workspace_service.py` | P1 |
| T-09 | Implement `compute_readiness()` with SLA clock | `src/ccp/services/phase0_workspace_service.py` | P1 |
| T-10 | Implement `Phase0ArtifactStore.register_artifact()` with lineage guard | `src/ccp/services/phase0_artifact_store.py` | P1 |
| T-11 | Implement `transition_artifact()` with state machine | `src/ccp/services/phase0_artifact_store.py` | P1 |
| T-12 | Implement `assemble_manifest()` | `src/ccp/services/phase0_artifact_store.py` | P1 |
| T-13 | Implement `Phase0MigrationService.migrate_to_container()` with payment guard | `src/ccp/services/phase0_migration_service.py` | P2 |
| T-14 | Implement upgrade bridge initiation and payment confirmation | `src/ccp/services/phase0_migration_service.py` | P2 |
| T-15 | Create FastAPI router with all 8 endpoints | `src/ccp/api/phase0_workspace.py` | P2 |
| T-16 | Mount router in `main.py` | `src/ccp/api/main.py` | P2 |
| T-17 | Write integration tests | `tests/integration/test_era3_fr34_phase0_workspace.py` | P2 |
| T-18 | Write model unit tests | `tests/models/test_phase0_workspace_models.py` | P3 |

**SQL Schemas (for T-03 through T-06):**

```sql
-- Phase-0 Workspaces
CREATE TABLE IF NOT EXISTS phase0_workspaces (
    workspace_id              TEXT PRIMARY KEY,
    prospect_id               TEXT NOT NULL,
    prospect_packet_id        TEXT NOT NULL,
    coach_id                  TEXT,
    display_name              TEXT NOT NULL,
    status                    TEXT NOT NULL DEFAULT 'created'
        CHECK (status IN ('created','intake_received','artifacts_collecting',
            'audit_in_progress','preview_ready','delivered',
            'payment_unlocked','upgraded','archived','blocked')),
    artifact_count            INTEGER NOT NULL DEFAULT 0,
    campaign_id               TEXT,
    delivery_sla_deadline_utc TIMESTAMPTZ,
    created_at                TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at                TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by_receipt_id     TEXT NOT NULL,
    last_transition_receipt_id TEXT
);
CREATE INDEX IF NOT EXISTS idx_p0w_prospect ON phase0_workspaces(prospect_id);
CREATE INDEX IF NOT EXISTS idx_p0w_status ON phase0_workspaces(status);
ALTER TABLE phase0_workspaces ENABLE ROW LEVEL SECURITY;

-- Phase-0 Artifacts
CREATE TABLE IF NOT EXISTS phase0_artifacts (
    artifact_id             TEXT PRIMARY KEY,
    workspace_id            TEXT NOT NULL REFERENCES phase0_workspaces(workspace_id),
    prospect_id             TEXT NOT NULL,
    family                  TEXT NOT NULL CHECK (family IN (
        'intake_source','normalized_source','audit_report',
        'preview_asset','produced_proof','payment_bridge','upgrade_metadata')),
    status                  TEXT NOT NULL DEFAULT 'uploaded' CHECK (status IN (
        'uploaded','normalized','audit_ready','preview_ready',
        'delivered','payment_unlocked','upgraded','quarantined','rejected')),
    display_label           TEXT NOT NULL,
    mime_type               TEXT,
    file_size_bytes         BIGINT,
    storage_uri             TEXT,
    checksum_sha256         TEXT,
    parent_artifact_ids     JSONB NOT NULL DEFAULT '[]',
    source_receipt_id       TEXT NOT NULL,
    metadata                JSONB NOT NULL DEFAULT '{}',
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    transitioned_at         TIMESTAMPTZ,
    transition_receipt_id   TEXT
);
CREATE INDEX IF NOT EXISTS idx_p0a_workspace ON phase0_artifacts(workspace_id);
CREATE INDEX IF NOT EXISTS idx_p0a_family ON phase0_artifacts(family);
CREATE INDEX IF NOT EXISTS idx_p0a_status ON phase0_artifacts(status);
ALTER TABLE phase0_artifacts ENABLE ROW LEVEL SECURITY;

-- Phase-0 Artifact Manifests
CREATE TABLE IF NOT EXISTS phase0_artifact_manifests (
    manifest_id             TEXT PRIMARY KEY,
    workspace_id            TEXT NOT NULL REFERENCES phase0_workspaces(workspace_id),
    prospect_id             TEXT NOT NULL,
    assembled_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
    assembly_receipt_id     TEXT NOT NULL,
    intake_sources          JSONB NOT NULL DEFAULT '[]',
    normalized_sources      JSONB NOT NULL DEFAULT '[]',
    audit_reports           JSONB NOT NULL DEFAULT '[]',
    preview_assets          JSONB NOT NULL DEFAULT '[]',
    produced_proofs         JSONB NOT NULL DEFAULT '[]',
    payment_bridges         JSONB NOT NULL DEFAULT '[]',
    upgrade_metadata_refs   JSONB NOT NULL DEFAULT '[]',
    total_artifact_count    INTEGER NOT NULL DEFAULT 0,
    completeness_summary    JSONB NOT NULL DEFAULT '{}',
    is_delivery_ready       BOOLEAN NOT NULL DEFAULT FALSE,
    is_payment_bridge_ready BOOLEAN NOT NULL DEFAULT FALSE
);
CREATE INDEX IF NOT EXISTS idx_p0am_workspace ON phase0_artifact_manifests(workspace_id);
ALTER TABLE phase0_artifact_manifests ENABLE ROW LEVEL SECURITY;

-- Phase-0 Upgrade Bridges
CREATE TABLE IF NOT EXISTS phase0_upgrade_bridges (
    bridge_id               TEXT PRIMARY KEY,
    workspace_id            TEXT NOT NULL REFERENCES phase0_workspaces(workspace_id),
    prospect_id             TEXT NOT NULL,
    target_tier             TEXT NOT NULL CHECK (target_tier IN (
        'speaking_learning','coach_os','operator')),
    payment_confirmed       BOOLEAN NOT NULL DEFAULT FALSE,
    payment_receipt_id      TEXT,
    payment_amount_cents    INTEGER CHECK (payment_amount_cents >= 0),
    credit_applied_cents    INTEGER CHECK (credit_applied_cents >= 0),
    migration_status        TEXT NOT NULL DEFAULT 'pending' CHECK (migration_status IN (
        'pending','in_progress','completed','failed','aborted')),
    target_coach_acronym    CHAR(3),
    migration_receipt_id    TEXT,
    initiated_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
    confirmed_at            TIMESTAMPTZ,
    completed_at            TIMESTAMPTZ,
    abort_reason            TEXT
);
CREATE INDEX IF NOT EXISTS idx_p0ub_workspace ON phase0_upgrade_bridges(workspace_id);
CREATE INDEX IF NOT EXISTS idx_p0ub_migration ON phase0_upgrade_bridges(migration_status);
ALTER TABLE phase0_upgrade_bridges ENABLE ROW LEVEL SECURITY;
```

---

## 8. Acceptance Criteria

### AC-1 — Workspace Creation from Prospect Packet
**Mandate:** Shared-Workspace-First Rule

**Pass:** Given a valid `Phase0ProspectPacket` with non-empty `prospect_id` and `packet_id`, `create_workspace()` returns `Phase0WorkspaceRecord` with `status = intake_received`, populated `created_by_receipt_id`, and `delivery_sla_deadline_utc = now() + 24h`.

**Failure example:** `prospect_packet_id = ""` → workspace NOT created. Receipt logged `decision = "rejected"`. HTTP 422 returned. A workspace with an empty packet reference must never persist.

---

### AC-2 — Artifact Lineage Enforcement
**Mandate:** Artifact-Lineage Rule

**Pass:** Every artifact registered via `register_artifact()` includes a non-empty `source_receipt_id`. For `family != intake_source`, `parent_artifact_ids` must contain ≥ 1 valid artifact ID from the same workspace.

**Failure example:** An `audit_report` artifact submitted with `parent_artifact_ids = []`. Store rejects: `LINEAGE_VIOLATION: audit_report requires at least one parent artifact ID`. Not written to the database.

---

### AC-3 — Artifact State Machine Integrity
**Mandate:** Deterministic state transitions

**Pass:** `transition_artifact(id, AUDIT_READY)` from `normalized` succeeds. `transition_artifact(id, DELIVERED)` from `normalized` raises `ValueError("ILLEGAL_ARTIFACT_TRANSITION: normalized → delivered")`.

**Failure example:** Caller attempts `normalized → payment_unlocked`. Rejected. Artifact stays `normalized`. Receipt logged `decision = "rejected"`.

---

### AC-4 — No-Full-Container-Before-Payment
**Mandate:** No-Full-Container-Before-Payment Rule

**Pass:** `migrate_to_container()` succeeds only when `bridge.payment_confirmed = True` and `bridge.migration_status = "pending"`.

**Failure example:** `migrate_to_container(workspace_id="ws-001", coach_acronym="NDL")` called while `bridge.payment_confirmed = False`. Raises `PermissionError("MIGRATION_BLOCKED: payment_confirmed=False")`. Zero container resources provisioned. Receipt logged `action = "PHASE0-MIGRATION-BLOCKED"`.

---

### AC-5 — 24h SLA Tracking
**Mandate:** 24h Delivery Readiness Rule

**Pass:** `compute_readiness()` returns `ON_TRACK` when `hours_remaining > 6`, `AT_RISK` when `0 < hours_remaining <= 6`, `BREACHED` when `hours_remaining <= 0` and workspace not `delivered`.

**Failure example:** Workspace 26h old, still not `delivered`. Returns `BREACHED`, `human_review_required = True`, logs `PHASE0-SLA-BREACH`. Workspace NOT auto-archived.

---

### AC-6 — Human-Review Recovery
**Mandate:** Human-Review Recovery Rule

**Pass:** `quarantined` artifact blocks readiness from returning `ON_TRACK`. Recovery via `PATCH` with non-empty `human_review_note` transitions artifact back and re-enables readiness computation.

**Failure example:** Recovery submitted with `human_review_note = ""`. Rejected: `RECOVERY_NOTE_REQUIRED`. Artifact stays `quarantined`.

---

### AC-7 — Manifest Completeness Accuracy
**Mandate:** Artifact-Lineage Rule

**Pass:** `assemble_manifest()` sets `completeness_summary["audit_report"] = "present"` only when ≥ 1 audit_report artifact is `preview_ready` or beyond. `is_delivery_ready = True` only when both `audit_report` and `preview_asset` families are `"present"`.

**Failure example:** All `audit_report` artifacts are `audit_ready` (not yet `preview_ready`). `completeness_summary["audit_report"] = "partial"`. `is_delivery_ready = False`.

---

### AC-8 — Receipt Chain Completeness
**Mandate:** Era 3 audit trail mandate

**Pass:** Every call to `create_workspace()`, `transition_workspace()`, `register_artifact()`, `transition_artifact()`, `assemble_manifest()`, `compute_readiness()`, `initiate_upgrade_bridge()`, `confirm_payment()`, and `migrate_to_container()` produces ≥ 1 `ReceiptEntry` with non-empty `receipt_id`.

**Failure example:** `assemble_manifest()` completes but `rc.query(action="PHASE0-MANIFEST-ASSEMBLE")` returns empty list. Hard test failure — manifests without receipts are non-compliant.

---

### AC-9 — Shared Workspace Isolation
**Mandate:** Shared-Workspace-First Rule + ADR-01

**Pass:** Workspaces for `prospect_id = "P1"` and `prospect_id = "P2"` never return each other's artifacts in `get_artifacts_by_workspace()`.

**Failure example:** `get_artifacts_by_workspace("ws-P1")` returns an artifact with `prospect_id = "P2"`. Critical isolation violation.

---

### AC-10 — Migration Archive Preservation
**Mandate:** Copy-then-archive migration law

**Pass:** After `migrate_to_container()` completes: source workspace `status = archived`. All artifact records remain in `phase0_artifacts` with `status = upgraded`. Full migration receipt chain is present and traceable.

**Failure example:** After migration, `phase0_artifacts` is empty for the workspace. Artifacts were deleted instead of archived. Violates audit trail mandate. Test must fail.

---

## 9. Dependencies

### 9.1 Internal

| Dependency | Type | Reason |
|---|---|---|
| `src/ccp/core/receipt_chain.py` | Runtime | All state transitions require `ReceiptChain.log()` |
| `src/ccp/core/asset_id.py` | Runtime | Artifact IDs via `AssetIDGenerator.generate(AssetType.PHASE0_ARTIFACT)` |
| `src/ccp/models/phase0_intake_models.py` (FR-ERA3-33) | Data contract | `Phase0ProspectPacket` seeds workspace creation |
| `src/ccp/services/payment_eligibility_service.py` | Runtime | Eligibility gate consulted before upgrade bridge confirmation |
| `src/ccp/services/affine_client_workspace.py` | Runtime | Migration delegates container provisioning patterns |
| `src/ccp/scripts/setup_supabase.py` | Schema | New `phase0_` tables registered here |

### 9.2 Downstream Consumers

| Spec | What It Reads |
|---|---|
| FR-ERA3-35 Audit Intelligence Engine | `phase0_artifacts` (intake_source, normalized_source families) |
| FR-ERA3-36 Delivery Orchestrator | `Phase0ArtifactManifest`, workspace `delivered` status |
| FR-ERA3-37 Commercial Bridge | `Phase0UpgradeBridgeState`, writes `payment_confirmed = True` |
| FR-ERA3-38 Operator Console | `Phase0ReadinessState`, all workspace + artifact statuses |

### 9.3 External

| Dependency | Type | Reason |
|---|---|---|
| Supabase PostgreSQL | Storage | Primary persistence layer |
| Supabase Storage `phase0-artifacts` | Object store | Binary artifact storage (private, RLS) |
| Stripe webhook (via FR-ERA3-37) | Event | Fires `confirm_payment()` on successful charge |

---

## 10. Testing Strategy

### 10.1 Integration Test File
`tests/integration/test_era3_fr34_phase0_workspace.py`

Mirror patterns from `test_cpsc_fr53_conversion_sequence.py`:
- `tmp_path` fixture for isolated receipt chain log directories.
- Inject mock Supabase via constructor — all service classes accept `supabase_client: Optional[Any]`.
- In-memory dict stores for DB simulation in unit/integration layers.

### 10.2 Test Class Structure

```python
class TestPhase0WorkspaceCreation:
    def test_valid_packet_creates_workspace(self): ...
    def test_status_is_intake_received(self): ...
    def test_sla_deadline_is_24h_from_now(self): ...
    def test_empty_prospect_id_rejected(self): ...
    def test_empty_packet_id_rejected(self): ...
    def test_receipt_logged_on_create(self): ...

class TestPhase0WorkspaceTransition:
    def test_valid_transition_succeeds(self): ...
    def test_illegal_transition_raises_value_error(self): ...
    def test_illegal_transition_leaves_status_unchanged(self): ...
    def test_transition_logs_receipt(self): ...
    def test_blocked_requires_human_recovery(self): ...

class TestPhase0ArtifactRegistration:
    def test_intake_source_registered_without_parent(self): ...
    def test_audit_report_requires_parent_artifact(self): ...
    def test_empty_source_receipt_id_rejected(self): ...
    def test_artifact_id_follows_p0af_format(self): ...
    def test_receipt_logged_on_register(self): ...

class TestPhase0ArtifactStateMachine:
    def test_uploaded_to_normalized_allowed(self): ...
    def test_uploaded_to_delivered_raises(self): ...
    def test_normalized_to_audit_ready_allowed(self): ...
    def test_any_state_to_quarantined_allowed(self): ...
    def test_quarantine_recovery_requires_human_note(self): ...
    def test_upgraded_is_terminal_state(self): ...
    def test_transition_logs_receipt(self): ...

class TestPhase0ManifestAssembly:
    def test_empty_workspace_all_families_missing(self): ...
    def test_intake_source_present_marks_family_partial(self): ...
    def test_preview_ready_artifact_marks_family_present(self): ...
    def test_delivery_ready_requires_audit_and_preview(self): ...
    def test_manifest_receipt_logged(self): ...

class TestPhase0ReadinessComputation:
    def test_on_track_when_hours_remaining_gt_6(self): ...
    def test_at_risk_when_hours_remaining_lte_6(self): ...
    def test_breached_when_hours_remaining_lte_0(self): ...
    def test_quarantined_artifact_sets_human_review_required(self): ...
    def test_readiness_receipt_logged(self): ...

class TestPhase0UpgradeBridge:
    def test_initiate_bridge_creates_pending_record(self): ...
    def test_payment_confirmed_sets_flag(self): ...
    def test_migration_blocked_without_payment(self): ...
    def test_migration_blocked_logs_receipt(self): ...
    def test_abort_sets_abort_reason(self): ...

class TestPhase0Migration:
    def test_migration_archives_workspace(self): ...
    def test_migration_marks_artifacts_upgraded(self): ...
    def test_migration_receipt_chain_complete(self): ...
    def test_migration_preserves_artifact_lineage(self): ...

class TestPhase0Isolation:
    def test_two_prospects_artifacts_never_cross(self): ...
    def test_workspace_ids_unique_across_prospects(self): ...
```

### 10.3 Model Unit Tests
`tests/models/test_phase0_workspace_models.py`

```python
class TestPhase0WorkspaceRecord:
    def test_status_default_is_created(self): ...
    def test_artifact_count_cannot_be_negative(self): ...
    def test_created_by_receipt_id_required(self): ...

class TestPhase0ArtifactRecord:
    def test_parent_artifact_ids_defaults_empty(self): ...
    def test_metadata_values_must_be_strings(self): ...
    def test_file_size_bytes_cannot_be_negative(self): ...

class TestPhase0UpgradeBridgeState:
    def test_payment_confirmed_defaults_false(self): ...
    def test_target_coach_acronym_enforces_3_char(self): ...
    def test_credit_applied_cannot_be_negative(self): ...
```

### 10.4 Key Invariants

| Invariant | Assertion |
|---|---|
| Every `Phase0ArtifactRecord` has a `source_receipt_id` | `assert artifact.source_receipt_id != ""` |
| No artifact in terminal state can transition | `pytest.raises(ValueError)` on `upgraded → normalized` |
| Migration without payment raises | `pytest.raises(PermissionError)` |
| Manifest assembly always logs receipt | `len(rc.query(action="PHASE0-MANIFEST-ASSEMBLE")) >= 1` |
| SLA breach sets `human_review_required = True` | `assert readiness.human_review_required is True` |

### 10.5 Existing Patterns Referenced
- Receipt chain isolation via `tmp_path` — mirrors `test_cpsc_fr53_conversion_sequence.py` lines 155–160.
- State machine boundary testing — mirrors dormancy gate threshold tests (FR53 lines 104–146).
- Payment gate pattern — mirrors `TestEligibilityGate` from `test_era3_fr02_payment_eligibility.py`.

---

*Spec complete. §1–§5: 511 lines. §6–§10: appended. All 6 canonical schemas defined (Phase0WorkspaceRecord, Phase0ArtifactRecord, Phase0ArtifactManifest, Phase0WorkspaceStatus, Phase0ReadinessState, Phase0UpgradeBridgeState). Artifact state machine formally specified with 7 forward states + quarantine + rejected. Migration law explicit. 10 ACs each with failure example. No vague storage story. No assumed full tenancy. Receipt chain and lineage enforced throughout.*
