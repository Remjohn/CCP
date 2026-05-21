# FR-ERA3-33 Phase-0 Prospect Intake Console Tech Spec

## Pre-Work Log

### Prompt File
- `docs/architecture/april_updates/spec_prompts/P0_S01_FR-ERA3-33_Phase0_Prospect_Intake_Console.md`

### Mandatory Source Set Read
- `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`
- `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md`
- `docs/prd/modules/PRD_04_CVE_Experience_Design.md`
- `lab/CCP APRIL Updates/Fladlien_Sales_Insights.md`
- `lab/ccp_biological_orchestration_model_v_1.md`
- `lab/CCP APRIL Updates/01_Architecture_PRDs/CCP_System_Documentation.md`

### Workspace Reality Check Read
- `src/ccp/api/main.py`
- `src/ccp/api/sacred_audio.py`
- `src/ccp/api/telegram_webhook.py`
- `src/ccp/api/billing_api.py`
- `src/ccp/api/stripe_webhook.py`
- `src/ccp/core/receipt_chain.py`
- `src/ccp/models/billing_models.py`
- `src/ccp/models/ca11_models.py`
- `src/ccp/models/commercial_ladder_models.py`
- `tests/integration/test_fr2_sacred_audio.py`
- `tests/integration/test_era3_fr10_anonymous_onboarding_flow.py`

### Key Commercial Findings Carried Forward
- PRD-09 makes the commercial ladder explicit:
  - `$0 proof`
  - `$29.99 first proof unlock`
  - `$39.99 continuity`
  - `$99.99 Coach OS`
- The intake surface must support the bridge from free proof into paid activation without requiring full coach container provisioning first.
- The audit must sell by diagnosis, prescription, and visible proof rather than by long explanation.

### Key Experience Findings Carried Forward
- PRD-04 requires low-friction, emotionally satisfying flow with one obvious action and one clear next step.
- The intake console is not only a data form. It is the front door into the shared Phase-0 production runtime.

### Key Runtime Findings Carried Forward
- `src/ccp/api/sacred_audio.py` shows a working upload pattern: request data validation, local persistence, receipt logging, and asset ID generation.
- `src/ccp/core/receipt_chain.py` provides append-only receipt logging and provenance querying.
- `src/ccp/api/billing_api.py` and `src/ccp/api/stripe_webhook.py` establish the payment boundary.
- `src/ccp/models/ca11_models.py` contains typed upload request/response patterns that Phase-0 mirrors to maintain API contract shape.

### Biological Orchestration Alignment
- CCP runtime doctrine is: `DNA / truth -> RNA / transcription -> force -> delivery -> variation -> rendered phenotype -> evaluation`.
- Phase-0 intake belongs at the `RNA / transcription` boundary, transforming raw prospect material into a typed, ready-to-run `Phase0ProspectPacket`.

### CBAR Constraints Acknowledged
- Human-First Proof Rule
- No-Full-Container-Before-Payment Rule
- Shared-Workspace-First Rule
- Typed Prospect Packet Rule
- 24h Delivery Readiness Rule
- Payment-Bridge Readiness Rule

---

## 1. Files Read

| # | File | Purpose |
|---|---|---|
| 1 | `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md` | PRD requirements for Phase-0 runtime and commercial bridge |
| 2 | `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md` | Sovereign container rules and architectural target |
| 3 | `docs/prd/modules/PRD_04_CVE_Experience_Design.md` | Intake low-friction experience constraints |
| 4 | `lab/CCP APRIL Updates/Fladlien_Sales_Insights.md` | Sales philosophy for audit and proof delivery |
| 5 | `lab/ccp_biological_orchestration_model_v_1.md` | Orchestration model (DNA/RNA/Force/Delivery/Variation/Phenotype/Evaluation) |
| 6 | `lab/CCP APRIL Updates/01_Architecture_PRDs/CCP_System_Documentation.md` | Base system architecture and tenancy layout |
| 7 | `src/ccp/api/sacred_audio.py` | Existing upload and receipt logging pattern |
| 8 | `src/ccp/core/receipt_chain.py` | ReceiptChain ledger database client |
| 9 | `src/ccp/models/ca11_models.py` | Upload request and response schemas to mirror |
| 10 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Specification writing protocol |

---

## 2. Overview

### 2.1 Objective
Define the Phase-0 Prospect Intake Console that captures, validates, normalizes, and routes all prospect materials required to produce a first-proof package inside the shared CCP main environment without provisioning a full coach container.

### 2.2 Problem
CCP’s production architecture assumes per-coach single-tenant containers. But outreach operations require proof generation ($0 free proof and $29.99 activation) before a coach makes a deep infrastructure or financial commitment. Provisioning dedicated PostgreSQL schemas, Supabase projects, and Docker containers for unverified prospects is economically and operationally prohibitive.

### 2.3 Solution
A logical intake surface operating within the shared CCP main runtime. It exposes API endpoints for operators to upload media, transcribe audio, capture target audience details, register Guardian business intelligence, and define audit targets. These inputs are validated, packaged, and persisted as a canonical, receipt-backed `Phase0ProspectPacket` inside shared PostgreSQL tables.

### 2.4 Scope
**In scope:**
- Logical prospect record creation and outreach campaign metadata binding.
- Intake of multimodal input domains (raw audio/video, transcripts, voice DNA, voice clones, avatar references, audience profile, and Guardian BI).
- Auditing content target classification (`single_image_caption`, `carousel_caption`, `reel_caption`).
- Automated packet and delivery readiness calculation.
- Typed missing-input representation to prevent silent failures.
- Handoff packet emission and Supabase persistence.
- Receipt chain logging for all intake actions.

**Out of Scope:**
- Supplying actual audio transcription processing engines (delegated downstream).
- Scoring or evaluating the target post (handled by `FR-ERA3-35`).
- Final video or graphic rendering pipelines (handled by `FR-ERA3-36`).
- Stripe or Telegram payment capture UI (handled by `FR-ERA3-37`).
- Provisioning single-tenant container nodes (handled by `FR-ERA3-34` migration).

---

## 3. Context for Development

### 3.1 Architecture Traceability (DEP-IDs)

| DEP-ID | Object | Type | Status |
|---|---|---|---|
| DEP-P0I-001 | `Phase0AuditTargetContentType` | Enum | NEW |
| DEP-P0I-002 | `Phase0InputState` | Enum | NEW |
| DEP-P0I-003 | `Phase0ProspectStatus` | Enum | NEW |
| DEP-P0I-004 | `Phase0DeliveryReadiness` | Enum | NEW |
| DEP-P0I-005 | `Phase0MediaSourceRef` | Pydantic model | NEW |
| DEP-P0I-006 | `Phase0TranscriptSourceRef` | Pydantic model | NEW |
| DEP-P0I-007 | `Phase0VoiceDnaSourceRef` | Pydantic model | NEW |
| DEP-P0I-008 | `Phase0VoiceCloneSourceRef` | Pydantic model | NEW |
| DEP-P0I-009 | `Phase0AvatarRef` | Pydantic model | NEW |
| DEP-P0I-010 | `Phase0TargetAudienceProfile` | Pydantic model | NEW |
| DEP-P0I-011 | `Phase0GuardianBusinessIntelligenceBundle` | Pydantic model | NEW |
| DEP-P0I-012 | `Phase0CaptionAttachment` | Pydantic model | NEW |
| DEP-P0I-013 | `Phase0AuditTargetDescriptor` | Pydantic model | NEW |
| DEP-P0I-014 | `Phase0MissingInputState` | Pydantic model | NEW |
| DEP-P0I-015 | `Phase0ProspectReadinessState` | Pydantic model | NEW |
| DEP-P0I-016 | `Phase0ProspectPacket` | Pydantic model | NEW |
| DEP-P0I-017 | `Phase0IntakeService` | Python service | NEW |
| DEP-P0I-018 | `phase0_prospect_packets` | Supabase table | NEW |

### 3.2 Existing Backend Integration

| File | Integration Point |
|---|---|
| `src/ccp/api/main.py` | Mounts the new `src/ccp/api/phase0_intake.py` router on the FastAPI core gateway. |
| `src/ccp/api/sacred_audio.py` | Reuse pattern for validating local path writes, saving uploads to storage buckets, and calling `ReceiptChain`. |
| `src/ccp/core/receipt_chain.py` | Logs structural validation audits and handoff transactions via `ReceiptChain.log()`. |
| `src/ccp/scripts/setup_supabase.py` | Supplying the `phase0_prospect_packets` table schema definitions for setup. |
| `src/ccp/models/ca11_models.py` | Mirrors standard patterns for payload structures to ensure consistency across upload payloads. |

### 3.3 ADR-05 Primitives
While this console is primarily logical intake, it prepares the contextual DNA/RNA payload that downstream experience apps require. The input forms and operator UI states are governed by:
- `EXP-FRC-002` (Zero-Thought Onboarding): Capturing files and text inputs with minimal operator steps.
- `EXP-TRS-003` (Visceral Hooking): Immediate validation and feedback showing that the system has successfully registered their voice, avatar, and context.
- `EXP-FBK-001` (RIM Feedback): Structured status returns that reveal exactly what inputs are missing or warning-flagged.

### 3.4 CBAR Mandate Enforcement

| Mandate | Enforcement Mechanism |
|---|---|
| **Human-First Proof Rule** | Intake enforces minimum human source content (voice and audience profiles) and rejects packets that contain purely automated dummy variables. |
| **No-Full-Container-Before-Payment Rule** | The intake router operates directly out of the shared gateway, saving records to a common table prefix. No docker runtime or Supabase schemas are provisioned. |
| **Shared-Workspace-First Rule** | All ingested records are logically isolated in the `phase0_prospect_packets` table using a `prospect_id` field. No per-prospect tenant namespace is generated. |
| **Typed Prospect Packet Rule** | The final step of the intake console service transforms the logical records into a strictly-typed `Phase0ProspectPacket` with exact validation constraints. |
| **24h Delivery Readiness Rule** | The intake service calculates a strict `delivery_readiness` state flag, returning specific missing-input descriptors that block operator handoff until SLA criteria are met. |
| **Payment-Bridge Readiness Rule** | Enforces the presence of target audience profile and Guardian BI context, which downstream payment sheets use to calculate pricing upgrades. |

### 3.5 Technical Decisions
- **Decision: Standardize Dates as ISO 8601 Strings:** In order to prevent timezone conversion discrepancies and Pydantic serialization errors when moving packets between Supabase and the FastAPI layer, all date fields are defined as `str` containing ISO 8601 UTC timestamps (e.g., `2026-05-20T10:57:22Z`).
- **Decision: Explicit Missing-Input States:** Instead of using optional fields or null returns, missing input states are returned as a list of typed `Phase0MissingInputState` objects. This makes it impossible for downstream engines to silently fail due to absent voice DNA or avatar files.
- **Decision: Readiness Classification Rules:** Formally define mathematical-logical thresholds for `Phase0DeliveryReadiness` enum calculations.

---

## 4. Implementation Plan

### Stage 1: Models & Setup (Tasks T-01 - T-03)
- Define enums and Pydantic v2 schemas in `src/ccp/models/phase0_intake_models.py`.
- Add the `phase0_prospect_packets` Supabase table migration logic to `src/ccp/scripts/setup_supabase.py`.
- Register the `P0I` acronym and asset generation rules in `src/ccp/core/asset_id.py`.

### Stage 2: Service Layer (Tasks T-04 - T-06)
- Create `Phase0IntakeService` in `src/ccp/services/phase0_intake_service.py`.
- Implement `create_prospect_record()`, `save_intake_media()`, and context attachments.
- Implement the `compute_readiness_state()` function using formalized thresholds.

### Stage 3: API Gateway (Tasks T-07 - T-09)
- Define FastAPI routes in `src/ccp/api/phase0_intake.py`.
- Mount the router on the FastAPI core app in `src/ccp/api/main.py`.
- Implement `ReceiptChain.log()` calls for all state mutations.

### Stage 4: Testing & Verification (Tasks T-10 - T-12)
- Write unit tests for schemas in `tests/models/test_phase0_intake_models.py`.
- Write service tests in `tests/services/test_phase0_intake_service.py`.
- Write API integration tests in `tests/integration/test_era3_fr33_phase0_intake_console.py`.

---

## 5. Primary Output Schema

### 5.1 Enum: `Phase0AuditTargetContentType`
```python
class Phase0AuditTargetContentType(str, Enum):
    SINGLE_IMAGE_CAPTION = "single_image_caption"
    CAROUSEL_CAPTION = "carousel_caption"
    REEL_CAPTION = "reel_caption"
```

### 5.2 Enum: `Phase0InputState`
```python
class Phase0InputState(str, Enum):
    MISSING = "missing"
    ATTACHED = "attached"
    VALIDATED = "validated"
    REJECTED = "rejected"
    DERIVED = "derived"
    OPTIONAL_MISSING = "optional_missing"
```

### 5.3 Enum: `Phase0ProspectStatus`
```python
class Phase0ProspectStatus(str, Enum):
    DRAFT = "draft"
    COLLECTING_INPUTS = "collecting_inputs"
    AWAITING_VALIDATION = "awaiting_validation"
    READY_FOR_PHASE0 = "ready_for_phase0"
    BLOCKED_MISSING_INPUTS = "blocked_missing_inputs"
    HANDED_OFF = "handed_off"
    ARCHIVED = "archived"
```

### 5.4 Enum: `Phase0DeliveryReadiness`
```python
class Phase0DeliveryReadiness(str, Enum):
    NOT_READY = "not_ready"
    CONDITIONALLY_READY = "conditionally_ready"
    READY = "ready"
    READY_HIGH_CONFIDENCE = "ready_high_confidence"
```

**Readiness Calculation Logic and Criteria:**
- **`not_ready`:** Assigned if `media_sources` is empty OR if `audit_targets` is empty. The package cannot be produced at all.
- **`conditionally_ready`:** Assigned if `media_sources` contains at least one audio/video file AND `voice_dna_sources` contains at least one record, but either `target_audience_profile` is missing or `avatar_refs` is empty. (Allows a manual bypass for $0 outreach trials).
- **`ready`:** Assigned if `media_sources` has transcribable audio/video, `transcript_sources` has at least one valid transcript, `voice_dna_sources` has at least one record, `avatar_refs` has at least one reference, `target_audience_profile` is attached, and `audit_targets` has at least one target content descriptor.
- **`ready_high_confidence`:** Assigned if all criteria for `ready` are met, PLUS `guardian_business_intelligence_bundle` is attached and every audit target has a valid linked `caption_id` (no warnings).

### 5.5 Pydantic Models

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class Phase0MediaSourceRef(BaseModel):
    source_id: str = Field(..., description="UUID v4 source file identifier")
    prospect_id: str = Field(..., description="Bound prospect ID")
    coach_id: Optional[str] = Field(default=None, description="Bound coach ID if known")
    media_kind: str = Field(..., description="interview_video | interview_audio | audit_target_image | audit_target_video | supporting_reference")
    storage_uri: str = Field(..., description="Supabase storage path (sacred-audio/...)")
    original_filename: str = Field(..., description="Name of file at upload")
    mime_type: str = Field(..., description="File MIME type")
    file_size_bytes: int = Field(..., ge=0, description="Size of file in bytes")
    duration_seconds: Optional[float] = Field(default=None, description="Duration in seconds if audio/video")
    image_width: Optional[int] = Field(default=None, description="Width in pixels if image")
    image_height: Optional[int] = Field(default=None, description="Height in pixels if image")
    checksum_sha256: str = Field(..., description="SHA-256 checksum of file content")
    upload_receipt_id: str = Field(..., description="Audit receipt ID for upload action")
    created_at: str = Field(..., description="ISO 8601 UTC timestamp")

class Phase0TranscriptSourceRef(BaseModel):
    transcript_id: str = Field(..., description="UUID v4 transcript identifier")
    prospect_id: str = Field(...)
    source_kind: str = Field(..., description="uploaded_file | inline_text | derived_from_media")
    linked_media_source_id: Optional[str] = Field(default=None, description="Linked media file ID if derived")
    storage_uri: Optional[str] = Field(default=None)
    raw_text: Optional[str] = Field(default=None)
    language_hint: Optional[str] = Field(default="en")
    word_count: Optional[int] = Field(default=None, ge=0)
    created_at: str = Field(..., description="ISO 8601 UTC timestamp")

class Phase0VoiceDnaSourceRef(BaseModel):
    voice_dna_source_id: str = Field(..., description="UUID v4 Voice DNA ref ID")
    prospect_id: str = Field(...)
    linked_media_source_ids: List[str] = Field(default_factory=list)
    notes: str = Field(default="")
    quality_confidence: float = Field(..., ge=0.0, le=1.0)
    created_at: str = Field(..., description="ISO 8601 UTC timestamp")

class Phase0VoiceCloneSourceRef(BaseModel):
    voice_clone_source_id: str = Field(..., description="UUID v4 Voice Clone ref ID")
    prospect_id: str = Field(...)
    linked_media_source_ids: List[str] = Field(default_factory=list)
    duration_seconds_total: float = Field(..., ge=0.0)
    quality_confidence: float = Field(..., ge=0.0, le=1.0)
    consent_status: Optional[str] = Field(default="given")
    created_at: str = Field(..., description="ISO 8601 UTC timestamp")

class Phase0AvatarRef(BaseModel):
    avatar_ref_id: str = Field(..., description="UUID v4 Avatar ref ID")
    prospect_id: str = Field(...)
    image_source_ids: List[str] = Field(default_factory=list)
    style_notes: str = Field(default="")
    pose_notes: str = Field(default="")
    quality_confidence: float = Field(..., ge=0.0, le=1.0)
    created_at: str = Field(..., description="ISO 8601 UTC timestamp")

class Phase0TargetAudienceProfile(BaseModel):
    prospect_id: str = Field(...)
    primary_audience_label: str = Field(..., min_length=1)
    pain_points: List[str] = Field(default_factory=list)
    desires: List[str] = Field(default_factory=list)
    market_context: str = Field(default="")
    offer_context: str = Field(default="")
    tone_notes: str = Field(default="")
    language_notes: str = Field(default="")
    created_at: str = Field(..., description="ISO 8601 UTC timestamp")

class Phase0GuardianBusinessIntelligenceBundle(BaseModel):
    guardian_bundle_id: str = Field(..., description="UUID v4 Guardian bundle ID")
    prospect_id: str = Field(...)
    market_summary: str = Field(...)
    offer_summary: str = Field(...)
    positioning_notes: str = Field(default="")
    objections: List[str] = Field(default_factory=list)
    differentiation_notes: str = Field(default="")
    proof_notes: str = Field(default="")
    raw_artifact_refs: List[str] = Field(default_factory=list)
    created_at: str = Field(..., description="ISO 8601 UTC timestamp")

class Phase0CaptionAttachment(BaseModel):
    caption_id: str = Field(..., description="UUID v4 caption ID")
    prospect_id: str = Field(...)
    audit_target_id: str = Field(..., description="Bound audit target")
    caption_text: str = Field(..., min_length=1)
    language_hint: str = Field(default="en")
    source_kind: str = Field(..., description="manual_entry | uploaded_file | imported_reference")
    created_at: str = Field(..., description="ISO 8601 UTC timestamp")

class Phase0AuditTargetDescriptor(BaseModel):
    audit_target_id: str = Field(..., description="UUID v4 target ID")
    prospect_id: str = Field(...)
    content_type: Phase0AuditTargetContentType = Field(...)
    primary_media_source_ids: List[str] = Field(default_factory=list)
    caption_id: Optional[str] = Field(default=None)
    platform_hint: Optional[str] = Field(default=None)
    content_url: Optional[str] = Field(default=None)
    archetype_hint: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)
    created_at: str = Field(..., description="ISO 8601 UTC timestamp")

class Phase0MissingInputState(BaseModel):
    prospect_id: str = Field(...)
    missing_code: str = Field(..., description="e.g. missing_voice_source")
    severity: str = Field(..., description="blocking | warning | optional")
    message: str = Field(...)
    resolution_hint: str = Field(...)

class Phase0ProspectReadinessState(BaseModel):
    prospect_id: str = Field(...)
    packet_status: Phase0ProspectStatus = Field(...)
    delivery_readiness: Phase0DeliveryReadiness = Field(...)
    blocking_missing_inputs: List[Phase0MissingInputState] = Field(default_factory=list)
    warning_missing_inputs: List[Phase0MissingInputState] = Field(default_factory=list)
    readiness_summary: str = Field(default="")
    validated_at: str = Field(..., description="ISO 8601 UTC timestamp")
    validation_receipt_id: str = Field(...)

class Phase0ProspectPacket(BaseModel):
    packet_id: str = Field(..., description="UUID v4 packet ID")
    prospect_id: str = Field(..., description="Unique prospect ID")
    coach_id: Optional[str] = Field(default=None, description="Bound coach acronym when known")
    display_name: str = Field(..., min_length=1)
    status: Phase0ProspectStatus = Field(...)
    created_at: str = Field(..., description="ISO 8601 UTC timestamp")
    updated_at: str = Field(..., description="ISO 8601 UTC timestamp")
    media_sources: List[Phase0MediaSourceRef] = Field(default_factory=list)
    transcript_sources: List[Phase0TranscriptSourceRef] = Field(default_factory=list)
    voice_dna_sources: List[Phase0VoiceDnaSourceRef] = Field(default_factory=list)
    voice_clone_sources: List[Phase0VoiceCloneSourceRef] = Field(default_factory=list)
    avatar_refs: List[Phase0AvatarRef] = Field(default_factory=list)
    target_audience_profile: Optional[Phase0TargetAudienceProfile] = Field(default=None)
    guardian_business_intelligence_bundle: Optional[Phase0GuardianBusinessIntelligenceBundle] = Field(default=None)
    audit_targets: List[Phase0AuditTargetDescriptor] = Field(default_factory=list)
    missing_input_states: List[Phase0MissingInputState] = Field(default_factory=list)
    readiness_state: Phase0ProspectReadinessState = Field(...)
    campaign_metadata: dict[str, str] = Field(default_factory=dict)
    handoff_notes: Optional[str] = Field(default=None)
    receipt_chain_refs: List[str] = Field(default_factory=list)
```

### 5.6 Packet Invariant Rules
- Every packet must belong to exactly one `prospect_id`.
- Every audit target must have exactly one valid `content_type`.
- Every audit target must have an attached caption, unless the operator explicitly waives it and receives a warning flag.
- Every packet must preserve the raw upload history inside the receipt chain.

---

## 6. Backward Compatibility Fallback

### 6.1 Packet Schema Fallback
If an upstream ingest payload contains raw datetimes or bare dictionaries instead of proper ISO 8601 strings:
- The parser within `Phase0IntakeService` must parse the string or datetime object, coerce it to ISO 8601 format (`YYYY-MM-DDTHH:MM:SSZ`), and save the coerced string.
- If coercion fails, raise a `ValidationError` and log a `PHASE0-INGEST-PARSE-FAIL` receipt.

### 6.2 Error Responses
- **ValidationError (Unprocessable Entity):** Returns HTTP 422 with JSON:
  ```json
  {
    "detail": "VALIDATION_FAILED",
    "fields": ["prospect_id"],
    "message": "Prospect ID cannot be empty or null."
  }
  ```
- **Lineage Breach:** Returns HTTP 400 with JSON:
  ```json
  {
    "detail": "LINEAGE_VIOLATION",
    "message": "Audit target must have at least one valid source media reference."
  }
  ```

### 6.3 Handoff Failure Protocol
If `handoff()` is triggered on a packet with `delivery_readiness == not_ready`:
- Immediately reject the request with HTTP 409 (Conflict).
- Do NOT advance the state of the packet to `handed_off`.
- Log a `PHASE0-HANDOFF-BLOCKED` receipt in the database.

---

## 7. Tasks

| Task ID | Task Description | Target File | Priority |
|---|---|---|---|
| T-01 | Create and define all Pydantic v2 schemas. | `src/ccp/models/phase0_intake_models.py` | P0 |
| T-02 | Add Supabase `phase0_prospect_packets` table scheme. | `src/ccp/scripts/setup_supabase.py` | P0 |
| T-03 | Add asset type `P0I` mappings to asset generator. | `src/ccp/core/asset_id.py` | P0 |
| T-04 | Implement core CRUD database helpers in `IntakeService`. | `src/ccp/services/phase0_intake_service.py` | P1 |
| T-05 | Implement mathematical-logical validation rules for readiness. | `src/ccp/services/phase0_intake_service.py` | P1 |
| T-06 | Implement receipt logging operations for intake mutations. | `src/ccp/services/phase0_intake_service.py` | P1 |
| T-07 | Create router endpoints for media upload and context setup. | `src/ccp/api/phase0_intake.py` | P2 |
| T-08 | Mount `phase0_intake` router on the core gateway application. | `src/ccp/api/main.py` | P2 |
| T-09 | Write intake schema unit tests. | `tests/models/test_phase0_intake_models.py` | P2 |
| T-10 | Write intake service business logic tests. | `tests/services/test_phase0_intake_service.py` | P2 |
| T-11 | Write endpoint integration tests using `pytest` async client. | `tests/integration/test_era3_fr33_phase0_intake_console.py` | P3 |

---

## 8. Acceptance Criteria

### AC-1 — Draft Packet Shell Initialization
- **CBAR Mandate Reference:** Typed Prospect Packet Rule, Shared-Workspace-First Rule
- **Pass Verdict:** The service successfully creates a prospect packet shell with a status of `draft`, generating a valid `prospect_id` and logging a `PHASE0-PROSPECT-CREATE` receipt.
- **Failure Example:** An attempt to create a packet with an empty display name is rejected with HTTP 422, logging a `PHASE0-PROSPECT-CREATE-FAIL` receipt. No table row is persisted.

### AC-2 — Multimedia Ingest Lineage Preservation
- **CBAR Mandate Reference:** Human-First Proof Rule, Typed Prospect Packet Rule
- **Pass Verdict:** A payload containing source media file size, checksum, and storage URIs is successfully validated and stored, referencing the creator's upload receipt ID.
- **Failure Example:** An upload reference is registered with a missing or invalid SHA-256 checksum pattern. The request fails with HTTP 422 and does not modify the packet.

### AC-3 — Explicit Missing-Input Resolution
- **CBAR Mandate Reference:** Typed Prospect Packet Rule, 24h Delivery Readiness Rule
- **Pass Verdict:** A packet missing its voice DNA yields an explicit `Phase0MissingInputState` entry with code `missing_voice_source` and severity `blocking`.
- **Failure Example:** An operator calls the validation endpoint on a packet without voice files, but the system returns `delivery_readiness = ready` and hides the missing input. The test fails.

### AC-4 — Readiness State Thresholding
- **CBAR Mandate Reference:** 24h Delivery Readiness Rule
- **Pass Verdict:** A prospect packet with media sources, voice DNA, transcript, and target post details evaluates to `ready` or `ready_high_confidence`.
- **Failure Example:** A packet containing only a single raw image file with no voice DNA or target audience evaluates to `ready` or `conditionally_ready`. The test fails because it violates the minimum proof generation data envelope.

### AC-5 — Caption Validation and Platform Constraints
- **CBAR Mandate Reference:** Human-First Proof Rule
- **Pass Verdict:** A carousel target content is registered containing multiple image assets and an attached caption, yielding `is_delivery_ready = True`.
- **Failure Example:** A carousel target content is registered without any image references. The API throws HTTP 400 (Lineage Breach), block-rejecting the registration.

### AC-6 — Shared Database Isolation Verification
- **CBAR Mandate Reference:** Shared-Workspace-First Rule
- **Pass Verdict:** Retrieving packet records for `prospect_id = "P1"` yields only records matching `"P1"` and never leaks objects belonging to `"P2"`.
- **Failure Example:** A query to `/phase0/prospects/P1` returns a JSON object containing target posts or voice DNA belonging to `prospect_id = "P2"`. This critical tenant leakage fails validation.

### AC-7 — Handoff Gate Blockers
- **CBAR Mandate Reference:** No-Full-Container-Before-Payment Rule, 24h Delivery Readiness Rule
- **Pass Verdict:** Handoff is rejected with HTTP 409 if the calculated readiness is `not_ready`.
- **Failure Example:** Handoff succeeds on a packet with no assets attached. The status changes to `handed_off`. The test fails.

### AC-8 — Receipt Chain Audit Verification
- **CBAR Mandate Reference:** Receipt Integrity
- **Pass Verdict:** Every call to the intake routes creates exactly one `ReceiptEntry` in the shared Supabase ledger table.
- **Failure Example:** Creating a prospect succeeds, but querying the receipt database client yields no matching receipt record. The audit trail is broken; test fails.

### AC-9 — Invariant Handoff Determinism
- **CBAR Mandate Reference:** Typed Prospect Packet Rule
- **Pass Verdict:** Running `validate` twice on unchanged input yields identical readiness state values and identical checksum digests.
- **Failure Example:** The readiness validation service uses system timestamps inside internal state calculations, causing consecutive validations of identical data to produce different validation receipts or hashes. The test fails.

### AC-10 — Continuity Bridge Preparation
- **CBAR Mandate Reference:** Payment-Bridge Readiness Rule
- **Pass Verdict:** The emitted packet contains all target audience profiles and Guardian BI context fields populated, enabling the billing service to verify continuity tier eligibility.
- **Failure Example:** The handoff packet has a null `target_audience_profile` field, blocking the payment sheet from resolving pricing tiers. The test fails.

---

## 9. Dependencies

### 9.1 Internal
- `src/ccp/core/receipt_chain.py`: Required to log structural validation transactions.
- `src/ccp/core/asset_id.py`: Required to generate unique logical IDs.
- `src/ccp/scripts/setup_supabase.py`: Schema setup configuration script.
- `src/ccp/models/ca11_models.py`: Model schema patterns.

### 9.2 Sibling Integration
- `FR-ERA3-34` (Workspace and Artifact Store): Consumes the `Phase0ProspectPacket` returned by `/phase0/prospects/{id}/handoff` to build the pre-container workspace.

### 9.3 External
- Supabase PostgreSQL and private buckets (`sacred-audio` and `prospect-intake`).

---

## 10. Testing Strategy

### 10.1 Unit Tests
- Create `tests/models/test_phase0_intake_models.py`.
- Test Pydantic validation rules, date string parsing, and enum validation.

### 10.2 Service Tests
- Create `tests/services/test_phase0_intake_service.py`.
- Test `compute_readiness_state()` against various input mock combinations (empty, missing voice, conditionally ready, fully ready).

### 10.3 Integration Tests
- Create `tests/integration/test_era3_fr33_phase0_intake_console.py` using `pytest-asyncio`.
- Setup a test Supabase client pointing to a local docker or mock database container.
- Perform HTTP operations (POST to create, register uploads, validate, handoff) and verify response payloads and receipt chain ledger writes.
- Enforce cleanup by deleting test prospect rows from Supabase at test teardown.
