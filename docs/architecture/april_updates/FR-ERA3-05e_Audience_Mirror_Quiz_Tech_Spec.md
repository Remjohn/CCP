# Tech-Spec: FR-ERA3-05e — Audience Mirror Quiz Mini App
**Status:** Ready for Development | **Version:** 1.0 (ERA3 — CBAR-Hardened)

**Created:** 2026-05-11

---

## Pre-Work Log

1. **PROTOCOL LOADED:** `ERA3_Tech_Spec_Writing_Protocol.md` §2.3 confirms `cultural_memory_map` stores 7 CMM layers and `coach_story_archive` stores Hartian 5-element stories; §2.1 confirms model validation is Pydantic v2 under `src/ccp/models/`.
2. **PRD LOADED:** The modular PRD registry names PRD-06 as: `"Conscious Reactions: Solo/Debate/Jury/Tier List modes, topic intelligence, viral thresholds, acquisition-through-reaction, co-created clips"` and the PRD-06 source-of-truth section for this feature defines Audience Mirror Quiz as: `"This format asks the coach questions that reflect the actual concerns, beliefs, or tensions of their own audience."`
3. **EPIC LOADED:** First AC quoted exactly from Story 6.3: `"Given the system reads my CMM (Cultural Memory Map),"` and `"When the quiz generates, it asks me to resolve specific tensions my audience has previously complained about."`
4. **CBAR AUDIT LOADED:** Phase 2 audit confirms `EXP-PER-003` is in scope and the Hallucination Purge bans `EXP-TRB-*`; this spec inherits CORE mandates Phase2-M01 through Phase2-M04 through the shared recording/scoring pipeline.
5. **PRIMITIVES LOADED:** `EXP-PER-003 "Cumulative Investment"`; `EXP-FBK-001 "RIM Feedback Discipline"`; `EXP-FRC-003 "The B=MAP Friction Audit"`. Note: the prompt labels `EXP-PER-003` as Tailoring/Suggestion, but the YAML canonical name is `Cumulative Investment`; the implementation uses the YAML as authoritative and applies the prompt's personalization intent as the behavioral constraint.
6. **BACKEND FILES READ:** `src/ccp/services/signal_source_loader.py` — `"def load(self) -> SignalBundle"`; `src/ccp/services/cmm_extraction.py` — `"async def extract(self, sacred_audio_transcript: str, business_canvas_content: str, tribe_soul_content: str, philosophy_brief_content: str,) -> CulturalMemoryMap"` and `"def confirm_entries(self, cmm: CulturalMemoryMap, approved_entry_ids: list[str], rejected_entry_ids: Optional[list[str]] = None,) -> CulturalMemoryMap"`; `src/ccp/services/trait_scoring_engine.py` — `"def score_all_traits(self) -> list[ScoredTrait]"`.
7. **TEST PATTERN:** Read `tests/integration/test_ca11_fr15_dpa_engine.py` and `tests/integration/test_ca11_fr19_trivianar_engine.py`; both use direct pytest classes/functions, deterministic fixtures, and a local `_run()` helper instead of `pytest-asyncio`.

---

## 1. Files Read

| # | File | Why It Was Read |
|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P2_S09_FR-ERA3-05e_Audience_Mirror_Quiz.md` | Prompt, feature scope, backend relation, output target |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Required spec structure, stack, DB table registry, Mini App mapping |
| 3 | `docs/architecture/april_updates/Phase2_Conscious_Reactions_Epics.md` | Story 6.3 acceptance criteria and primitive quality constraint |
| 4 | `docs/architecture/cbar_audits/CBAR_Audit_Phase2_Conscious_Reactions.md` | Mandate confirmation and primitive hallucination purge |
| 5 | `lab/CCP APRIL Updates/05_Core_Experience/Conscious_Reactions_Source_of_Truth.md` | Source-of-truth section `5.6.4 Audience Mirror Quiz` |
| 6 | `docs/prd/modules/PRD_INDEX.md` | PRD-06 module registry and retained lineage routing |
| 7 | `docs/prd/modules/PRD_06_Conscious_Reactions.md` | Conscious Reactions PRD module and brownfield context |
| 8 | `docs/prd/modules/PRD_02_CCF_Content_Factory.md` | Legacy format inventory line proving Audience Mirror remains an intended format |
| 9 | `primitives/experience/personalization_identity/EXP-PER-003.yaml` | Canonical primitive ID and name verification |
| 10 | `primitives/experience/feedback_scoring/EXP-FBK-001.yaml` | Immediate feedback primitive verification |
| 11 | `primitives/experience/friction_ability/EXP-FRC-003.yaml` | Friction-management primitive verification |
| 12 | `src/ccp/services/signal_source_loader.py` | Existing signal loading path for optional CMM and story archive data |
| 13 | `src/ccp/services/cmm_extraction.py` | CMM lifecycle, operator gate, local JSON persistence, Supabase sync boundary |
| 14 | `src/ccp/services/trait_scoring_engine.py` | Existing downstream consumer of tribe soul, CMM, and story archive data |
| 15 | `src/ccp/models/v5_models.py` | `CulturalMemoryMap` and `CoachStoryArchive` data contracts and query helpers |
| 16 | `src/ccp/scripts/setup_supabase.py` | Actual SQL schema for `cultural_memory_map` and `coach_story_archive` |
| 17 | `src/ccp/api/main.py` | API router registration pattern |
| 18 | `src/ccp/api/sacred_audio.py` | Upload endpoint style and background-safe file ingestion pattern |
| 19 | `src/ccp/core/receipt_chain.py` | Immutable audit logging contract |
| 20 | `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | Inherited CORE mandates, upload, scoring, and export behavior |
| 21 | `tests/integration/test_ca11_fr15_dpa_engine.py` | Integration test class/function style |
| 22 | `tests/integration/test_ca11_fr19_trivianar_engine.py` | Integration test naming and helper style |

## 2. Overview

### 2.1 Problem Statement

`Audience Mirror Quiz` is not a generic trivia surface. The prompt explicitly requires the system to derive questions from the coach's real audience memory, specifically the approved `cultural_memory_map` record and relevant `coach_story_archive` context. Without a dedicated spec:

- teams will generate generic AI questions that could fit any coach, violating Story 6.3 and the `EXP-PER-003` identity-reflection standard
- teams will read raw `tribe_soul.json` directly and bypass the operator-approved CMM layers that already exist as the system's cultural condensation layer
- teams will over-couple question generation to the scoring engine instead of treating question generation as a separate pre-recording step
- teams will fail open when CMM data is missing, producing fake personalization rather than blocking the mode safely

### 2.2 Solution

Build a standalone Telegram Mini App launched as `startapp=react_mirror_quiz` under `apps/react-mirror-quiz/`. The Mini App consumes the shared CORE reaction session lifecycle for:

- topic/session issuance
- bounded recording
- background upload
- streaming score assembly
- export gating

It adds one new format-specific backend capability: a deterministic `MirrorQuizQuestionService` that reads the latest approved `cultural_memory_map` rows from Supabase, extracts audience tensions from allowed layers, optionally enriches the pack with approved `coach_story_archive` prompts, and emits a personalized `MirrorQuizQuestionPack`. The Mini App renders those questions, lets the coach choose or receive the next question, records the answer through the CORE transport, and receives the same private score / export verdict flow as other reaction modes.

### 2.3 Scope In / Out

**In Scope**

- `react_mirror_quiz` Telegram Mini App shell and question card UI
- question-pack generation from approved `cultural_memory_map` data
- optional answer-support enrichment from `coach_story_archive`
- receipt logging for evidence selection and question generation
- explicit fail-closed behavior when audience-memory readiness is insufficient
- reuse of CORE recording, upload, scoring, and export contracts

**Out of Scope**

- re-implementing transcription, scoring, or CMF export inside this spec
- modifying the CMM extraction protocol itself
- modifying story archive seeding or approval workflows
- building a public audience-facing quiz mode
- generating generic fallback questions from LLM world knowledge

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Component | Source | Purpose |
|---|---|---|---|
| DEP-REA-MRQ-001 | `AudienceMirrorQuizAppShell` | Story 6.3 | Dedicated Telegram Mini App launched with `startapp=react_mirror_quiz` |
| DEP-REA-MRQ-002 | `MirrorQuizQuestionService` | Prompt + Story 6.3 | Builds personalized question packs from approved CMM data |
| DEP-REA-MRQ-003 | `AudienceTensionSelector` | `EXP-PER-003` + source-of-truth §5.6.4 | Ranks candidate tensions from approved audience-memory evidence |
| DEP-REA-MRQ-004 | `StoryArchivePromptLinker` | Prompt + DEP-ENG-024 | Optionally links an approved coach story to a generated question |
| DEP-REA-MRQ-005 | `MirrorQuizQuestionPack` | Prompt | Typed payload returned to the Mini App before recording starts |
| DEP-REA-MRQ-006 | `MirrorQuizReadinessGate` | Prompt + Story 6.3 | Blocks the mode if no approved CMM evidence exists |
| DEP-REA-MRQ-007 | `MirrorQuizReceiptEmitter` | Receipt chain contract | Logs question-evidence selection and generation rationale |
| DEP-REA-MRQ-008 | `MirrorQuizSessionProjection` | CORE inheritance | Combines question pack, recording state, upload state, and score readiness |
| DEP-REA-MRQ-009 | `OverlayRenderer` (Mirror Quiz Camera) | FR-ERA3-25 | Shared AR Overlay Capture Pipeline — composites camera feed with quiz card UI for 9:16 video export |

### 3.2 Existing Backend Integration

| File | Path | How Used |
|---|---|---|
| `SignalSourceLoader` | `src/ccp/services/signal_source_loader.py` | Existing optional enrichment loader already recognizes `config/cultural_memory_map.json` and `config/coach_story_archive.json` through `def load(self) -> SignalBundle`. The Mirror Quiz service must align with this shape instead of inventing a second signal schema. |
| `CMMExtractionProtocol` | `src/ccp/services/cmm_extraction.py` | Existing CMM lifecycle defines operator approval and the gate requirement. `async def extract(...) -> CulturalMemoryMap` and `def confirm_entries(...) -> CulturalMemoryMap` prove CMM is an approved artifact, not raw scraped text. Mirror Quiz must only consume approved entries. |
| `CulturalMemoryMap` / `CoachStoryArchive` | `src/ccp/models/v5_models.py` | `def get_entries_by_layer(self, layer: CMMLayerType) -> list[CMMEntry]` and `def query_by_cral_moment(self, cral_moment: str) -> list[CoachStoryEntry]` establish the correct read semantics for approved layer queries and story retrieval. |
| `setup_supabase.py` | `src/ccp/scripts/setup_supabase.py` | The actual SQL schema proves `cultural_memory_map.entries` is JSONB and `coach_story_archive` is keyed by `story_id`. New query code must target these exact tables/columns. |
| `TraitScoringEngine` | `src/ccp/services/trait_scoring_engine.py` | `def score_all_traits(self) -> list[ScoredTrait]` already consumes `self._cmm` and `self._story_archive`, proving these sources are valid downstream enrichment signals in the current architecture. |
| `ReceiptChain` | `src/ccp/core/receipt_chain.py` | `def log(... ) -> ReceiptEntry` provides the append-only audit trail for question generation, evidence selection, and degraded-mode decisions. |
| `api.main` | `src/ccp/api/main.py` | Shows the correct FastAPI router registration pattern via `app.include_router(...)`; the new Mirror Quiz router must plug in the same way. |
| `sacred_audio.py` | `src/ccp/api/sacred_audio.py` | `@router.post("/sacred-audio/upload")` provides the current upload endpoint and error-handling style that the mode-specific finalize route should mirror where relevant. |

### 3.3 ADR-05 Primitives

| ID | Name | Family | Constraint |
|---|---|---|---|
| `EXP-PER-003` | Cumulative Investment | personalization_identity | Although the prompt describes Tailoring/Suggestion, the canonical YAML name is `Cumulative Investment`. For this mode, the actionable constraint is that the quiz must visibly prove the system has stored real audience knowledge and can reinvest it back into the coach's practice. Generic questions violate the primitive because they reveal no stored value. |
| `EXP-FBK-001` | RIM Feedback Discipline | feedback_scoring | The coach should receive immediate private confirmation that the answer was captured and scored through the CORE path. Post-answer state changes and score readiness cannot feel delayed or ambiguous. |
| `EXP-FRC-003` | The B=MAP Friction Audit | friction_ability | The question-to-record flow must be low-friction. The user should not manually configure prompts, paste evidence, or browse archives before answering. The system pre-builds the question pack so the coach can tap and speak. |

### 3.4 CBAR Mandate Enforcement

| Mandate | Phase-M# | Story | Implementation Mechanism |
|---|---|---|---|
| The Ephemeral Decay Mandate | Phase2-M01 | Inherited via CORE topic/session issuance | `MirrorQuizQuestionPack` carries `issued_at`, `expires_at`, and `ttl_seconds`. Expired quiz packs are rejected with `TOPIC_EXPIRED`; the app must request a fresh pack instead of replaying stale audience tensions. |
| The Background Upload Rule | Phase2-M02 | Inherited via CORE finalize flow | The Mini App releases the user immediately after stop and uses the shared background upload ticket flow. Mirror Quiz must never block on full file upload before revealing the captured-answer state. |
| The Streaming Audio SLA | Phase2-M03 | Inherited via CORE scoring flow | The mode does not implement its own end-of-recording batch transcription. It relies on CORE chunk streaming so the personalized answer can be scored and surfaced within the existing 3-second SLA. |
| The Earned Export Gate | Phase2-M04 | Inherited via CORE artifact gate | A Mirror Quiz answer can only route to CMF/export if the shared biometric and semantic gates pass. Personalized questions do not exempt the answer from anti-slop enforcement. |

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|---|---|---|---|
| Query `cultural_memory_map` first and treat it as the primary audience-memory source | The prompt explicitly says CMM exists and must drive personalization | Generate directly from `tribe_soul.json` | Bypasses approved CMM condensation and loses the operator-reviewed cultural layer |
| Fail closed when approved CMM evidence is insufficient | Story 6.3 forbids generic questions; false personalization is worse than no session | Fall back to generic LLM questions | Violates the feature's core promise and breaks `EXP-PER-003` |
| Treat `coach_story_archive` as optional enrichment, not primary question source | Questions must reflect audience tensions; stories help answer them but should not replace them | Build questions from story archive only | Produces coach-centric prompts instead of audience-centric prompts |
| Build a dedicated `MirrorQuizQuestionService` instead of modifying `TraitScoringEngine` | Question generation is a pre-recording problem; scoring is a post-recording problem | Cram question synthesis into the scoring engine | Blurs responsibilities and risks breaking FR61 trait scoring |
| Persist question-evidence rationale in the receipt chain | Developers and operators need proof that each question came from approved data | Return only final question text | No auditability, no debugging path, no trust check |
| Use a dedicated Mini App under `apps/react-mirror-quiz/` | The mode has question-card interactions and pack refresh behavior distinct from Solo/Debate/Tierlist | Reuse another format's frontend shell without a dedicated boundary | Increases coupling and makes future mode-specific changes harder |

## 4. Implementation Plan

### Phase 1 — Data Contracts and Readiness Gates

- [ ] Create `src/ccp/models/reaction_mirror_quiz_models.py`
- [ ] Define `MirrorQuizEvidenceQuote`, `StoryArchiveHint`, `AudienceMirrorQuestion`, and `MirrorQuizQuestionPack`
- [ ] Add `MirrorQuizGenerationStatus` and `MirrorQuizReadinessStatus` enums in `src/ccp/models/reaction_mirror_quiz_models.py`
- [ ] Add `MirrorQuizSessionProjection` in `src/ccp/models/reaction_mirror_quiz_models.py`

### Phase 2 — Backend Personalization Service

- [ ] Create `src/ccp/services/mirror_quiz_question_service.py`
- [ ] Implement Supabase-backed `load_latest_cmm(coach_id: str) -> CulturalMemoryMap`
- [ ] Implement approved-layer filtering against `collective_wound`, `industry_mythology`, `linguistic_templates`, and `shared_enemy`
- [ ] Implement `load_story_archive(coach_id: str) -> CoachStoryArchive | None` in `src/ccp/services/mirror_quiz_question_service.py`
- [ ] Implement `build_question_pack(...) -> MirrorQuizQuestionPack` in `src/ccp/services/mirror_quiz_question_service.py`
- [ ] Implement receipt logging for evidence selection in `src/ccp/services/mirror_quiz_question_service.py`

### Phase 3 — API and CORE Integration

- [ ] Create `src/ccp/api/reaction_mirror_quiz_api.py`
- [ ] Add `POST /api/reactions/mirror-quiz/question-pack` in `src/ccp/api/reaction_mirror_quiz_api.py`
- [ ] Add `POST /api/reactions/mirror-quiz/finalize` in `src/ccp/api/reaction_mirror_quiz_api.py` as a thin adapter to CORE finalize behavior plus question metadata
- [ ] Register the router in `src/ccp/api/main.py`
- [ ] Add readiness error mapping and circuit-breaker codes in `src/ccp/core/circuit_breaker.py`

### Phase 4 — Telegram Mini App Surface

- [ ] Create `apps/react-mirror-quiz/package.json`
- [ ] Create `apps/react-mirror-quiz/src/main.jsx`
- [ ] Create `apps/react-mirror-quiz/src/App.jsx`
- [ ] Create `apps/react-mirror-quiz/src/components/MirrorQuestionCard.jsx`
- [ ] Create `apps/react-mirror-quiz/src/components/AudienceEvidenceDrawer.jsx`
- [ ] Create `apps/react-mirror-quiz/src/components/RecordAnswerPanel.jsx`
- [ ] Create `apps/react-mirror-quiz/src/styles.css`

### Phase 5 — Verification and Coverage

- [ ] Add `tests/unit/test_mirror_quiz_question_service.py`
- [ ] Add `tests/integration/test_era3_fr05e_mirror_quiz_api.py`
- [ ] Add `tests/integration/test_era3_fr05e_mirror_quiz_personalization.py`
- [ ] Add manual QA checklist updates in `docs/architecture/april_updates/FR-ERA3-05e_Audience_Mirror_Quiz_Tech_Spec.md`

## 5. Primary Output Schema

The models below are new mode-specific contracts that sit beside the shared CORE reaction session contracts. They do not replace the CORE envelopes; they specialize the question-generation payload and the format-specific session projection.

```python
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class MirrorQuizGenerationStatus(str, Enum):
    READY = "ready"
    DEGRADED_STORYLESS = "degraded_storyless"
    BLOCKED_CMM_NOT_READY = "blocked_cmm_not_ready"
    BLOCKED_NO_APPROVED_TENSIONS = "blocked_no_approved_tensions"


class MirrorQuizReadinessStatus(str, Enum):
    READY = "ready"
    CMM_NOT_READY = "cmm_not_ready"
    CMM_TOO_THIN = "cmm_too_thin"
    STORY_ARCHIVE_MISSING = "story_archive_missing"


class MirrorQuizEvidenceQuote(BaseModel):
    evidence_id: str = Field(..., description="Deterministic ID for the selected CMM evidence row")
    cmm_id: str = Field(..., description="Source CulturalMemoryMap identifier")
    layer_type: Literal[
        "collective_wound",
        "industry_mythology",
        "linguistic_templates",
        "shared_enemy",
        "aspirational_archetype",
    ] = Field(...)
    source_material: Literal[
        "sacred_audio_transcript",
        "business_canvas",
        "tribe_soul",
        "philosophy_brief",
        "unknown",
    ] = Field(...)
    quoted_text: str = Field(..., min_length=8, description="Exact approved audience-memory phrasing")
    normalized_tension: str = Field(..., min_length=8, description="System-normalized tension label")
    selection_reason: str = Field(..., min_length=8, description="Why this quote was chosen for the question")


class StoryArchiveHint(BaseModel):
    story_id: str = Field(..., description="Approved coach story identifier")
    story_type: str = Field(..., min_length=2)
    cral_moment_fit: str = Field(default="")
    mechanism_tag: str = Field(default="")
    hook_line: str = Field(..., min_length=8, description="Short private reminder for the coach")
    why_relevant: str = Field(..., min_length=8)


class AudienceMirrorQuestion(BaseModel):
    question_id: str = Field(..., description="Deterministic question identifier")
    ordinal: int = Field(..., ge=1, le=5)
    surface_text: str = Field(..., min_length=12, description="Coach-facing prompt text")
    audience_verbatim: str = Field(..., min_length=8, description="Exact audience wording shown in the UI")
    primary_tension: str = Field(..., min_length=8)
    coaching_intent: Literal[
        "resolve_belief_conflict",
        "answer_hidden_objection",
        "name_shared_enemy",
        "reframe_failed_assumption",
        "validate_audience_identity",
    ] = Field(...)
    answer_time_limit_seconds: int = Field(default=90, ge=30, le=180)
    evidence_quotes: list[MirrorQuizEvidenceQuote] = Field(
        default_factory=list,
        min_length=1,
        max_length=3,
        description="Approved CMM evidence proving personalization"
    )
    story_hint: StoryArchiveHint | None = Field(
        default=None,
        description="Optional private answer prompt from approved story archive"
    )


class MirrorQuizQuestionPack(BaseModel):
    pack_id: str = Field(..., description="Primary identifier for this generated pack")
    coach_id: str = Field(..., description="Single-tenant coach scope")
    startapp: Literal["react_mirror_quiz"] = Field(default="react_mirror_quiz")
    source_mode: Literal["audience_mirror_quiz"] = Field(default="audience_mirror_quiz")
    cmm_id: str = Field(..., description="Approved CMM record used to build the pack")
    question_pack_version: str = Field(default="1.0")
    generation_status: MirrorQuizGenerationStatus = Field(...)
    readiness_status: MirrorQuizReadinessStatus = Field(...)
    questions: list[AudienceMirrorQuestion] = Field(default_factory=list, min_length=1, max_length=5)
    story_archive_used: bool = Field(default=False)
    receipt_id: str = Field(..., description="Receipt chain entry for generation traceability")
    issued_at: datetime = Field(...)
    expires_at: datetime = Field(...)
    ttl_seconds: int = Field(..., ge=60, le=86400)


class MirrorQuizSessionProjection(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    question_pack: MirrorQuizQuestionPack = Field(...)
    selected_question_id: str = Field(...)
    upload_status: Literal[
        "pending_background",
        "uploading",
        "uploaded",
        "failed_retryable",
    ] = Field(...)
    scoring_status: Literal[
        "recording",
        "processing",
        "scored",
        "redemption_required",
    ] = Field(...)
    export_eligible: bool = Field(default=False)
    score_ready: bool = Field(default=False)
    score_receipt_id: str | None = Field(default=None)
```

**Schema Notes**

- `quoted_text` must preserve the approved audience phrasing that justified the question.
- `questions` must never be empty on a `READY` pack.
- `startapp` is hard-coded to `react_mirror_quiz`.
- `story_hint` is enrichment only; the pack remains valid without it.
- `generation_status` and `readiness_status` separate hard-blocks from soft degradation.

## 6. Backward Compatibility Fallback

This feature must follow the `circuit_breaker.py` pattern and fail safely.

| Failure Condition | Fallback Behavior |
|---|---|
| No approved `cultural_memory_map` row for the coach | Return `generation_status="blocked_cmm_not_ready"` and `readiness_status="cmm_not_ready"` with error code `MIRROR_QUIZ_CMM_NOT_READY`. Do not generate generic questions. |
| Approved CMM exists but contains no usable audience-tension entries in allowed layers | Return `generation_status="blocked_no_approved_tensions"` and `readiness_status="cmm_too_thin"` with error code `MIRROR_QUIZ_NO_APPROVED_TENSIONS`. Do not synthesize from world knowledge. |
| `coach_story_archive` absent or below gate | Continue with `generation_status="degraded_storyless"`, `readiness_status="story_archive_missing"`, and `story_archive_used=false`; questions are still valid if the CMM evidence is sufficient. |
| Quiz pack expired | Reject the pack with `TOPIC_EXPIRED` and force regeneration under Phase2-M01. |
| CORE upload/scoring path fails | Preserve the selected question metadata, emit a receipt entry, and let the shared CORE fallback rules govern retry, score delay, or redemption routing. |

**Non-Negotiable Rule**

If the CMM evidence is not real, approved, and coach-specific, the system must block the Mirror Quiz mode. It must never degrade into a generic "What does your audience struggle with?" style prompt.

## 7. Tasks

### Backend

- [ ] Add `src/ccp/models/reaction_mirror_quiz_models.py` with the typed payloads from Section 5
- [ ] Add `src/ccp/services/mirror_quiz_question_service.py`
- [ ] Read `cultural_memory_map` from Supabase using the exact `cmm_id`, `coach_id`, `entries`, `operator_confirmed`, `updated_at` columns defined in `src/ccp/scripts/setup_supabase.py`
- [ ] Rehydrate `CulturalMemoryMap` and `CoachStoryArchive` using `src/ccp/models/v5_models.py`
- [ ] Filter CMM entries to approved entries only; reject unapproved rows at service level
- [ ] Build deterministic question IDs from `coach_id + cmm_id + normalized_tension`
- [ ] Generate `pack_id` as a UUID v4 or deterministic hash of `coach_id` and timestamp
- [ ] Set `issued_at` to the current UTC timestamp and `expires_at` to `issued_at + 24 hours` (enforcing the 86400 TTL)
- [ ] Emit receipt chain records through `src/ccp/core/receipt_chain.py` for pack generation and degraded-mode decisions
- [ ] Add `src/ccp/api/reaction_mirror_quiz_api.py` and register it in `src/ccp/api/main.py`

### Frontend

- [ ] Create `apps/react-mirror-quiz/src/App.jsx` with dedicated `react_mirror_quiz` flow
- [ ] Create `apps/react-mirror-quiz/src/components/MirrorQuestionCard.jsx` to show prompt, verbatim evidence, and answer CTA
- [ ] Create `apps/react-mirror-quiz/src/components/AudienceEvidenceDrawer.jsx` to expose the audience quote without cluttering the main card
- [ ] Create `apps/react-mirror-quiz/src/components/RecordAnswerPanel.jsx` to hand off recording to the shared CORE transport
- [ ] Add `apps/react-mirror-quiz/src/styles.css` with a distinct premium quiz surface aligned to the existing Conscious Reactions visual language

### Testing

- [ ] Add unit coverage for evidence selection, blocked mode behavior, and story-archive degradation
- [ ] Add integration coverage for question-pack generation and finalize flow
- [ ] Add manual QA to verify that the rendered audience quote is copied from real approved CMM data and not paraphrased into a bland generic prompt

## 8. Acceptance Criteria

### AC-6.3A — Questions Must Be Derived From Real Audience Data

**CBAR / Primitive Reference:** Story 6.3, `EXP-PER-003`

**Given** the active coach has an operator-approved `cultural_memory_map` row with approved entries in `collective_wound`, `industry_mythology`, or `shared_enemy`,  
**When** `POST /api/reactions/mirror-quiz/question-pack` generates a pack,  
**Then** each returned question includes at least one `evidence_quotes` entry copied from an approved CMM entry,  
**And** the `audience_verbatim` shown in the question card reflects real stored phrasing rather than a generic paraphrase,  
**And** the receipt metadata records which `cmm_id`, layer, and quote were used.

**FAILURE EXAMPLE:** The coach has approved CMM entries like `"I'm tired of sounding smart but still not converting"` and `"Every mastermind tells me to post more, but none of it lands"`. The generated question says only `"What challenge does your audience have with marketing?"` and exposes no evidence quote. This is a spec violation.

### AC-6.3B — Missing CMM Data Must Block the Mode, Not Trigger Generic Questions

**CBAR / Primitive Reference:** Story 6.3, `EXP-PER-003`, Section 6 fail-closed rule

**Given** the coach has no approved `cultural_memory_map` row or no approved tension entries in the allowed layers,  
**When** the Mirror Quiz pack endpoint is called,  
**Then** the service returns a blocked readiness state (`MIRROR_QUIZ_CMM_NOT_READY` or `MIRROR_QUIZ_NO_APPROVED_TENSIONS`),  
**And** no question pack is generated,  
**And** the system does not synthesize placeholder questions from broad industry assumptions.

**FAILURE EXAMPLE:** A newly onboarded coach with no approved CMM data taps Mirror Quiz. The backend responds with `"What do your clients fear most?"`, `"What myth do you challenge?"`, and `"What belief holds them back?"` based only on general coaching tropes. This is a spec violation.

### AC-6.3C — Story Archive Enrichment Must Remain Secondary

**CBAR / Primitive Reference:** Prompt backend relation, DEP-ENG-024

**Given** the coach has an approved `coach_story_archive` entry relevant to the same audience tension,  
**When** the question pack is built,  
**Then** the matching question may include a private `story_hint`,  
**And** the question still remains anchored to CMM evidence as its primary source,  
**And** if no approved story exists the pack remains valid in degraded storyless mode.

**FAILURE EXAMPLE:** The service skips CMM lookup entirely, reads only coach stories, and generates questions like `"Tell the story about your burnout client"` with no audience-memory quote attached. This is a spec violation.

### AC-6.3D — The Recording Flow Must Inherit CORE Upload and Scoring Guarantees

**CBAR / Primitive Reference:** Phase2-M02, Phase2-M03, `EXP-FBK-001`

**Given** the coach is answering a personalized Mirror Quiz question,  
**When** they stop recording,  
**Then** the session immediately transitions to the shared background-upload state,  
**And** the selected question metadata remains attached to the session projection,  
**And** scoring readiness is delivered through the CORE 3-second streaming path rather than waiting for the full file upload.

**FAILURE EXAMPLE:** The app keeps a blocking spinner labeled `"Uploading before scoring..."` for 20 seconds after the coach stops speaking because the full audio file must finish uploading before the backend starts processing. This is a spec violation.

### AC-6.3E — Personalized Questions Still Obey the Shared Export Gate

**CBAR / Primitive Reference:** Phase2-M04

**Given** a coach answers an Audience Mirror question with low conviction, poor transcript quality, or centroid hedging,  
**When** CORE final scoring completes,  
**Then** the result is marked `redemption_required` or otherwise non-exportable according to the shared gate,  
**And** the personalized nature of the prompt does not auto-authorize CMF publication.

**FAILURE EXAMPLE:** The system sees that the question came from real audience data and publishes the answer automatically even though the transcript is mostly filler and fails the anti-centroid threshold. This is a spec violation.

## 9. Dependencies

### Internal

| Dependency | Type | Why Required |
|---|---|---|
| `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | Shared spec dependency | Provides the authoritative recording, upload, scoring, and export lifecycle |
| `docs/architecture/april_updates/FR-ERA3-25_AR_Overlay_Capture_Pipeline_Tech_Spec.md` | Shared spec dependency | Camera feed, PixiJS overlay rendering, composite video capture, sound engine, interaction journal |
| `src/ccp/services/signal_source_loader.py` | Existing service contract | Existing optional signal shape for CMM and story archive |
| `src/ccp/services/cmm_extraction.py` | Existing service contract | Defines how approved CMM data is produced and confirmed |
| `src/ccp/models/v5_models.py` | Existing model dependency | Canonical contracts for `CulturalMemoryMap` and `CoachStoryArchive` |
| `src/ccp/scripts/setup_supabase.py` | Existing schema dependency | Defines actual table columns and RLS-enabled tables |
| `src/ccp/core/receipt_chain.py` | Existing infrastructure | Required provenance logging |
| `src/ccp/api/main.py` | Existing API composition | Router registration point |
| `src/ccp/api/sacred_audio.py` | Existing API pattern | Upload route style reference |

### External

| Dependency | Type | Why Required |
|---|---|---|
| Supabase | Managed database | Stores `cultural_memory_map` and `coach_story_archive` |
| Telegram Mini App runtime | Client platform | Required launch surface for `react_mirror_quiz` |
| Browser `MediaRecorder` + local cache | Client browser capability | Needed through CORE for answer recording and background upload |
| Sovereign NIM transcription / reasoning stack | Deployment dependency | Needed through CORE for streaming scoring and post-answer analysis |

## 10. Testing Strategy

### Unit Tests

- `tests/unit/test_mirror_quiz_question_service.py::test_build_question_pack_uses_only_approved_cmm_entries`
- `tests/unit/test_mirror_quiz_question_service.py::test_generation_blocks_when_cmm_missing_or_unapproved`
- `tests/unit/test_mirror_quiz_question_service.py::test_story_archive_hint_is_optional_and_never_replaces_cmm_evidence`
- `tests/unit/test_mirror_quiz_question_service.py::test_question_ids_are_deterministic_for_same_cmm_input`

### Integration Tests

- `tests/integration/test_era3_fr05e_mirror_quiz_api.py::test_question_pack_endpoint_returns_react_mirror_quiz_payload`
- `tests/integration/test_era3_fr05e_mirror_quiz_api.py::test_finalize_preserves_selected_question_and_enters_pending_background`
- `tests/integration/test_era3_fr05e_mirror_quiz_personalization.py::test_real_cmm_verbatim_appears_in_question_pack`
- `tests/integration/test_era3_fr05e_mirror_quiz_personalization.py::test_missing_cmm_returns_blocked_status_without_generic_questions`

### Test Pattern Notes

- Follow the existing integration style from `test_ca11_fr15_dpa_engine.py` and `test_ca11_fr19_trivianar_engine.py`
- Prefer deterministic factory helpers and explicit assertion names
- Use a local `_run()` helper for async calls if async behavior is exercised
- Avoid hidden fixture magic; build the CMM and story archive payloads inline in the test where possible

### Manual QA Checklist

1. Launch the mode with `startapp=react_mirror_quiz` and verify the app loads a dedicated question card surface.
2. Seed a coach with approved CMM entries containing distinctive audience language and verify the same phrases appear in `audience_verbatim`.
3. Remove approved CMM entries and verify the pack endpoint returns a blocked readiness state rather than generic prompts.
4. Keep CMM approved but remove `coach_story_archive`; verify the pack still generates and marks `story_archive_used=false`.
5. Record an answer and verify the UI leaves recording state immediately after stop while upload continues in the background.
6. Force a low-quality answer and verify the result remains private / non-exportable through the inherited CORE gate.
7. Inspect receipt logs and verify the selected `cmm_id`, evidence layer, and question ID were recorded.

---

## Appendix — Personalization Selection Rules

The question service must use deterministic filtering rules before any model-assisted phrasing step:

1. Load the latest operator-confirmed `cultural_memory_map` for the coach.
2. Keep approved entries only.
3. Limit candidate layers to those that best express audience pain or worldview tension:
   - `collective_wound`
   - `industry_mythology`
   - `linguistic_templates`
   - `shared_enemy`
   - `aspirational_archetype` only when paired with a tension-bearing layer
4. Normalize duplicate complaints into a single tension label while preserving verbatim source quotes.
   - Deterministically map the resulting `normalized_tension` to one of the five `coaching_intent` literals (e.g., if the tension involves a false belief, assign `resolve_belief_conflict`).
5. Prefer tensions backed by at least two approved entries when available.
6. Optionally attach one approved story hint from `coach_story_archive` if a story strengthens the coach's likely answer path.
7. Emit 3-5 questions maximum; more than 5 dilutes choice and slows the coach down.

These rules are intentionally stricter than a generic "ask the LLM for good questions" approach. The point of this mode is proof of audience understanding, not quiz abundance.
