# Tech-Spec: FR-ERA3-05j - Ranking Quiz Co-Creation Mini App
**Created:** 2026-05-11
**Status:** Ready for Development
**Version:** 1.0 (ERA3 - CBAR-Hardened)
**Phase:** 2 - Conscious Reactions
**Architecture Reference:** ERA3_Tech_Spec_Writing_Protocol.md Section 7

## Pre-Work Log

```
1. PROTOCOL LOADED:   Section 5.1 classifies Ranking Quiz Co-Creation as a standalone Content Creation Experience
                      with `startapp=react_ranking_quiz`, while Section 2.2 confirms all new routes extend the
                      existing FastAPI app rooted at `src/ccp/api/main.py`.
2. PRD LOADED:        PRD-06 preserves the FR inventory line `FR-06-16 (Ranking Quiz Co-Creation)` and points back
                      to the source-of-truth mode definition: "This format blends ranking logic with co-created reaction."
3. EPIC LOADED:       "Given I publish a completed Tierlist, When a user views it, they can drag-and-drop to propose
                      their own order."
4. CBAR AUDIT LOADED: No direct Phase 2 Ranking Quiz mandate is declared in the audit. This spec inherits only the
                      relevant CORE mandates: Phase2-M01 (Ephemeral Decay), Phase2-M02 (Background Upload Rule),
                      Phase2-M03 (Streaming Audio SLA), and Phase2-M04 (Earned Export Gate). Hallucination purge also
                      confirms `EXP-TRB-*` references must be corrected to `EXP-TRS-*`.
5. PRIMITIVES LOADED: `experience_primitive_id: "EXP-SOC-001"` / `canonical_name: "Social Treasures + Group Quests"`
                      `experience_primitive_id: "EXP-FBK-004"` / `canonical_name: "Bring the Data Forward"`
                      `experience_primitive_id: "EXP-PRG-002"` / `canonical_name: "Discover -> On-board -> Immerse -> Master -> Replay"`
6. BACKEND FILES READ:`src/ccp/services/dpa_engine.py` - `async def resolve(self, coach_id: str, content_archetype: str,
                      audience_mood_state: str = "", brand_hue_analysis: BrandHueAnalysis | None = None,
                      override_mode: OverrideMode = OverrideMode.adaptive, identity_tokens: dict[str, Any] | None = None,) -> DPAResult`
                      `src/ccp/services/trait_scoring_engine.py` - `def score_all_traits(self) -> list[ScoredTrait]`
                      `src/ccp/services/signal_source_loader.py` - `def load(self) -> SignalBundle`
7. TEST PATTERN:      `tests/integration/test_ca11_fr15_dpa_engine.py` and
                      `tests/integration/test_ca11_fr19_trivianar_engine.py` both use a local `_run()` helper,
                      class-per-scenario organization, explicit fixture builders/constants, and direct assertions
                      against typed models and service outputs without `pytest-asyncio`.
```

## 1. Files Read

| # | File | Version/Date | Purpose |
|---|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P2_S14_FR-ERA3-05j_Ranking_Quiz_Co_Creation.md` | 2026-05-11 | Assignment prompt, explicit separate-artifact requirement, output path |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Loaded 2026-05-11 | Mandatory protocol, Mini App separation doctrine, backend extension rules |
| 3 | `docs/prd/modules/PRD_06_Conscious_Reactions.md` | v6.0, 2026-05-06 | PRD module, Brownfield FR inventory, source-document linkage |
| 4 | `lab/CCP APRIL Updates/05_Core_Experience/Conscious_Reactions_Source_of_Truth.md` | Loaded 2026-05-11 | Exact mode definition in Section 5.6.10 |
| 5 | `docs/architecture/april_updates/Phase2_Conscious_Reactions_Epics.md` | 2026-05-08 | Story 5.4 acceptance criteria and quality constraint |
| 6 | `docs/architecture/cbar_audits/CBAR_Audit_Phase2_Conscious_Reactions.md` | 2026-05-10 | Mandate inheritance and primitive hallucination corrections |
| 7 | `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | 2026-05-11 | Shared session, scoring, DPA, and share-state contracts |
| 8 | `docs/architecture/april_updates/FR-ERA3-05d_Tierlist_Authority_Tech_Spec.md` | 2026-05-11 | Upstream published Tierlist artifact source for v1 seeding |
| 9 | `primitives/experience/social_referral/EXP-SOC-001.yaml` | Codified registry | Verified co-authorship and group-quest primitive |
| 10 | `primitives/experience/feedback_scoring/EXP-FBK-004.yaml` | Codified registry | Verified immediate comparison-feedback primitive |
| 11 | `primitives/experience/progression_replay/EXP-PRG-002.yaml` | Codified registry | Verified progression/replay scaffold primitive |
| 12 | `src/ccp/services/dpa_engine.py` | Existing service | Branding contract reused for the co-creation surface |
| 13 | `src/ccp/services/trait_scoring_engine.py` | Existing service | Optional defense-audio scoring substrate inherited through CORE |
| 14 | `src/ccp/services/signal_source_loader.py` | Existing service | Existing signal dependency gate for scored defense mode |
| 15 | `src/ccp/api/main.py` | 1.0.0 | FastAPI route registration and `/health` extension point |
| 16 | `src/ccp/core/receipt_chain.py` | Current | Immutable audit logging for proposal/session events |
| 17 | `src/ccp/scripts/setup_supabase.py` | Current | Existing schema bootstrap and migration extension point |
| 18 | `tests/integration/test_ca11_fr15_dpa_engine.py` | Existing | Async `_run()` and class-per-scenario pytest pattern |
| 19 | `tests/integration/test_ca11_fr19_trivianar_engine.py` | Existing | Builder-heavy, direct-assertion integration test pattern |

## 2. Overview

### 2.1 Problem Statement

Without a dedicated Ranking Quiz Co-Creation spec, teams will collapse two distinct artifacts into one mutable board:
- the coach's published original ranking
- the audience member's challenge proposal

That breaks the core mechanic. The social energy comes from visible disagreement and co-authorship, not from silently editing the coach's board in place. If the original ranking is overwritten, the system loses:
- the coach's source-of-truth stance
- the audience member's authored counter-ranking
- the diff object that makes the challenge commentable
- the proof that peer participation, not passive viewing, created the engagement

It also creates an implementation trap where the existing Tierlist board is reused as a generic mutable editor, even though Story 5.4 is not "edit a list"; it is "propose an alternative order to a published authority object."

### 2.2 Solution

This spec creates `react_ranking_quiz` as a standalone Telegram Mini App that opens from a published Tierlist artifact and forks that published ranking into an immutable challenge session. The original coach ranking is stored as a frozen source snapshot. Every audience challenger creates a separate proposal artifact with:
- their reordered list
- a typed diff against the original ranking
- author identity
- optional short defense-audio take captured through the shared CORE recording path

The Mini App is therefore not a replacement for Tierlist. It is a downstream social mode that consumes a published Tierlist artifact, turns disagreement into a structured reorder interaction, and preserves both versions of the ranking as first-class records.

### 2.3 Scope

**In scope:**
- `startapp=react_ranking_quiz` Telegram Mini App launch
- loading only published Tierlist artifacts as v1 seed objects
- freezing the coach's original ranking snapshot inside the ranking-quiz session
- drag-and-drop reorder of the same item set by an audience participant
- distinct persistence for original ranking and audience proposal ranking
- visual comparison view showing slot deltas between original and proposal
- optional 30-60 second defense-audio capture for submitted proposals
- receipt logging, DPA theming, and typed FastAPI contracts

**Out of scope:**
- editing the original coach ranking in place
- seeding v1 from arbitrary ranking modes other than published Tierlist artifacts
- live multi-user collaborative dragging on the same board
- anonymous or unverified proposal authorship
- generalized canvas editing or Excalidraw scene management
- replacing the `react_tierlist` recording mode itself

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Component | Source FR | What It Does |
|---|---|---|---|
| DEP-REA-RQC-001 | `RankingQuizAppShell` | FR-06-16 / Story 5.4 | Standalone `react_ranking_quiz` Telegram Mini App |
| DEP-REA-RQC-002 | `PublishedRankingSeedResolver` | Story 5.4 | Resolves a published Tierlist artifact into an immutable original ranking snapshot |
| DEP-REA-RQC-003 | `OriginalRankingSnapshot` | Prompt requirement | Stores the coach's source ranking as a frozen artifact that cannot be mutated by viewers |
| DEP-REA-RQC-004 | `AudienceProposalBoard` | Story 5.4 | Client-side reorder surface for audience drag-and-drop proposals |
| DEP-REA-RQC-005 | `ProposalDiffEngine` | Story 5.4 quality constraint | Computes `original_slot -> proposed_slot` deltas for every item |
| DEP-REA-RQC-006 | `ProposalSubmissionLedger` | Prompt requirement | Persists each audience alternative distinctly from the source ranking |
| DEP-REA-RQC-007 | `ProposalDefenseCapture` | Source-of-truth `rank / defend / challenge / reorder` | Optional short defense-audio session attached to the proposal |
| DEP-REA-RQC-008 | `RankingQuizComparisonReveal` | Story 5.4 | Renders the original ranking beside the proposal after submission |
| DEP-REA-RQC-009 | `CoCreationSessionManager` | FR-06-16 | Governs share token, dedup, expiry, and author identity rules |
| DEP-REA-RQC-010 | `RankingQuizApiBridge` | FR-ERA3-05j | Thin backend bridge between the Mini App, Tierlist seed artifact, and CORE utilities |
| DEP-OVR-001 | `OverlayRenderer` (Ranking Quiz Camera) | FR-ERA3-25 | Shared AR Overlay Capture Pipeline — composites camera feed with ranking comparison for 9:16 video export |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|---|---|---|
| `FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | Upstream contract for session identity, DPA palette continuity, optional defense recording, upload semantics, and scored reaction attachments |
| `FR-ERA3-05d_Tierlist_Authority_Tech_Spec.md` | `docs/architecture/april_updates/FR-ERA3-05d_Tierlist_Authority_Tech_Spec.md` | Upstream seed format. V1 only accepts published `react_tierlist` artifacts as the original ranking source |
| `main.py` | `src/ccp/api/main.py` | Registers the ranking-quiz route module and extends `/health` with seed-artifact and proposal-persistence readiness |
| `dpa_engine.py` | `src/ccp/services/dpa_engine.py` | Reuses `DPAEngine.resolve(...)` so the challenge surface and comparison view remain brand-consistent |
| `trait_scoring_engine.py` | `src/ccp/services/trait_scoring_engine.py` | If a challenger records an optional defense take, the attached scorecard path inherits the existing trait-scoring substrate through CORE |
| `signal_source_loader.py` | `src/ccp/services/signal_source_loader.py` | Preserves the existing dependency gate before any scored defense-audio response is emitted |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | Logs session creation, reorder finalize, proposal submit, dedup suppression, and optional defense attach events |
| `setup_supabase.py` | `src/ccp/scripts/setup_supabase.py` | Appends ranking-quiz tables and indexes to the canonical schema bootstrap |

**Existing database tables consumed:**
- `asset_registry` - source published Tierlist artifact IDs and proposal artifact IDs
- `person_registry` - challenger identity resolution and duplicate-submission guard
- `receipt_chain` - immutable audit trail
- `resolved_palettes` - DPA continuity across source ranking and challenge surface
- `reaction_artifacts` - upstream published Tierlist artifacts and optional defense artifacts from CORE
- `reaction_sessions` - optional defense recording session linkage from CORE

**New ranking-quiz tables introduced by this spec:**
- `reaction_ranking_quiz_sessions` - frozen source snapshot plus share/session metadata
- `reaction_ranking_quiz_proposals` - audience proposals, distinct order payloads, diff summaries, author linkage

**Existing API routes extended or called:**
- `GET /health` - extended with ranking-quiz readiness diagnostics
- inherited CORE upload/finalize endpoints for optional defense audio
- `GET /api/reactions/ranking-quiz/{session_id}` - session/original ranking projection
- `POST /api/reactions/ranking-quiz/{session_id}/proposal` - submit reordered proposal artifact
- `POST /api/reactions/ranking-quiz/{session_id}/proposal/{proposal_id}/defense` - attach optional defense-audio metadata after CORE finalize
- `GET /api/reactions/ranking-quiz/{session_id}/proposal/{proposal_id}` - comparison projection for original vs proposal

### 3.3 ADR-05 Primitives

| Primitive ID | Name | Family | Constraint Applied |
|---|---|---|---|
| `EXP-SOC-001` | Social Treasures + Group Quests | social_referral | The audience must create a distinct human-authored counter-ranking rather than passively liking the coach's list |
| `EXP-FBK-004` | Bring the Data Forward | feedback_scoring | The comparison reveal must surface cumulative dispute data such as proposal counts, changed-item counts, and slot deltas rather than hiding the co-creation investment |
| `EXP-PRG-002` | Discover -> On-board -> Immerse -> Master -> Replay | progression_replay | The challenge is unlocked from a completed public ranking, moving users from passive viewing into a richer co-authored interaction |

### 3.4 CBAR Mandate Enforcement

| Mandate | Phase-M# | Story | Implementation Mechanism |
|---|---|---|---|
| The Background Upload Rule | Phase2-M02 | Inherited from CORE Story 1.2 | If the challenger records an optional defense take, stopping recording returns control to the comparison screen immediately while the audio uploads in the background |
| The Streaming Audio SLA | Phase2-M03 | Inherited from CORE Story 1.3 | Any optional defense take attaches a scorecard only through the streamed CORE chunk path; full-file post-stop scoring is not allowed as the primary mechanism |
| The Earned Export Gate | Phase2-M04 | Inherited from CORE Story 2.1 | Only published Tierlist artifacts that already passed CORE/Tierlist gating may seed `react_ranking_quiz`; private, failed, or redemption-required artifacts cannot become public challenge seeds |

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|---|---|---|---|
| V1 accepts only published `react_tierlist` artifacts as seed rankings | Story 5.4 explicitly says "Given I publish a completed Tierlist" | Accept rankings from any future mode immediately | Cross-mode ranking shapes will drift and create coercion bugs in v1 |
| Store the original ranking snapshot inside the ranking-quiz session | The prompt requires the coach ranking and audience proposal to be stored distinctly | Read the source artifact live on every view | Source artifacts can evolve or be deleted, breaking reproducibility |
| Persist each audience proposal as its own artifact row | The engagement object is the alternative order, not a mutable board edit | Overwrite the session's single board state with the latest viewer action | Destroys co-authorship and makes audit/history impossible |
| Use client-authoritative drag order with server-side validation on submit | Drag interaction must feel immediate and mobile-native | Round-trip every item move to the server | Adds latency and creates brittle mobile reorder UX |
| Make defense audio optional but structurally typed | Source-of-truth says users can rank, defend, challenge, reorder, but Story 5.4 only mandates proposal creation | Require voice recording for every proposal | Over-raises the friction floor for the audience challenge path |
| Compare by explicit slot delta projection instead of generic "changed" flags | The dispute is about order, so the UI must show movement magnitude and direction | Show only the final proposal without a diff object | Hides the argument and weakens the feedback moment |

## 4. Implementation Plan

### Phase 1 - App Scaffold and Seed Loading
- [ ] Create `apps/react-ranking-quiz/package.json`
- [ ] Create `apps/react-ranking-quiz/tsconfig.json`
- [ ] Create `apps/react-ranking-quiz/next.config.mjs`
- [ ] Create `apps/react-ranking-quiz/app/layout.tsx`
- [ ] Create `apps/react-ranking-quiz/app/page.tsx`
- [ ] Create `apps/react-ranking-quiz/app/globals.css`

### Phase 2 - Ranking Quiz Client Contracts
- [ ] Create `apps/react-ranking-quiz/app/lib/types.ts`
- [ ] Create `apps/react-ranking-quiz/app/lib/api.ts`
- [ ] Create `apps/react-ranking-quiz/app/lib/state.ts`
- [ ] Create `apps/react-ranking-quiz/app/lib/reorder-validation.ts`
- [ ] Create `apps/react-ranking-quiz/app/lib/diff-engine.ts`

### Phase 3 - Interactive UI Surface
- [ ] Create `apps/react-ranking-quiz/app/components/original-ranking-card.tsx`
- [ ] Create `apps/react-ranking-quiz/app/components/proposal-board.tsx`
- [ ] Create `apps/react-ranking-quiz/app/components/draggable-ranking-item.tsx`
- [ ] Create `apps/react-ranking-quiz/app/components/proposal-diff-panel.tsx`
- [ ] Create `apps/react-ranking-quiz/app/components/proposal-submit-sheet.tsx`
- [ ] Create `apps/react-ranking-quiz/app/components/optional-defense-recorder.tsx`
- [ ] Create `apps/react-ranking-quiz/app/components/comparison-reveal.tsx`

### Phase 4 - Backend Models and Routes
- [ ] Create `src/ccp/models/reaction_ranking_quiz_models.py`
- [ ] Create `src/ccp/services/reaction_ranking_quiz_projection.py`
- [ ] Create `src/ccp/api/reaction_ranking_quiz_api.py`
- [ ] Register ranking-quiz routes in `src/ccp/api/main.py`
- [ ] Extend `src/ccp/scripts/setup_supabase.py` with ranking-quiz tables and indexes

### Phase 5 - Verification
- [ ] Create `tests/integration/test_era3_fr05j_ranking_quiz_api.py`
- [ ] Create `tests/integration/test_era3_fr05j_ranking_quiz_projection.py`
- [ ] Create `tests/integration/test_era3_fr05j_ranking_quiz_contracts.py`
- [ ] Create `apps/react-ranking-quiz/app/__tests__/proposal-board.test.tsx`
- [ ] Create `apps/react-ranking-quiz/app/__tests__/diff-engine.test.tsx`
- [ ] Create `apps/react-ranking-quiz/app/__tests__/proposal-submit-sheet.test.tsx`

## 5. Primary Output Schema

**Target model file:** `src/ccp/models/reaction_ranking_quiz_models.py`

```python
from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from src.ccp.models.ca11_models import ResolvedPalette
from src.ccp.models.reaction_engine_models import (
    ReactionArtifactRecord,
    ReactionScoreCard,
    ReactionSessionRecord,
)


class RankingQuizSourceItem(BaseModel):
    item_id: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    original_slot_index: int = Field(..., ge=0)
    asset_url: str | None = None


class RankingQuizOriginalRanking(BaseModel):
    source_artifact_id: str = Field(..., min_length=1)
    source_mode: Literal["react_tierlist"] = Field(default="react_tierlist")
    published_by_person_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    frozen_at: datetime = Field(...)
    items: list[RankingQuizSourceItem] = Field(..., min_length=1)


class RankingQuizProposalItem(BaseModel):
    item_id: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    proposed_slot_index: int = Field(..., ge=0)


class RankingQuizDiffEntry(BaseModel):
    item_id: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    original_slot_index: int = Field(..., ge=0)
    proposed_slot_index: int = Field(..., ge=0)
    slot_delta: int = Field(...)


class RankingQuizProposalArtifact(BaseModel):
    proposal_id: str = Field(..., min_length=1)
    session_id: str = Field(..., min_length=1)
    proposer_person_id: str = Field(..., min_length=1)
    status: Literal["submitted", "duplicate_suppressed"] = Field(default="submitted")
    proposal_items: list[RankingQuizProposalItem] = Field(..., min_length=1)
    diff_entries: list[RankingQuizDiffEntry] = Field(default_factory=list)
    changed_item_count: int = Field(..., ge=0)
    proposal_caption: str | None = Field(default=None, max_length=280)
    defense_session: ReactionSessionRecord | None = None
    defense_artifact: ReactionArtifactRecord | None = None
    defense_scorecard: ReactionScoreCard | None = None
    submitted_at: datetime = Field(...)


class RankingQuizSessionProjection(BaseModel):
    startapp: Literal["react_ranking_quiz"] = Field(default="react_ranking_quiz")
    session_id: str = Field(..., min_length=1)
    palette: ResolvedPalette = Field(...)
    original_ranking: RankingQuizOriginalRanking = Field(...)
    working_order: list[RankingQuizProposalItem] = Field(..., min_length=1)
    share_token: str = Field(..., min_length=1)
    proposal_count: int = Field(default=0, ge=0)
    proposal_submission_open: bool = Field(default=True)


class RankingQuizComparisonProjection(BaseModel):
    session: RankingQuizSessionProjection = Field(...)
    proposal: RankingQuizProposalArtifact = Field(...)
```

**Schema notes:**
- `RankingQuizOriginalRanking` is immutable once the session is created
- `RankingQuizProposalArtifact` is a separate object, never an in-place mutation of `original_ranking`
- `ReactionSessionRecord`, `ReactionArtifactRecord`, and `ReactionScoreCard` are only populated when optional defense audio is recorded
- v1 intentionally normalizes the seed source to `react_tierlist` only

## 6. Backward Compatibility Fallback

This spec follows the fail-closed posture used by `circuit_breaker.py`.

| Failure Mode | Graceful Degradation |
|---|---|
| Source artifact is not `published` or is not from `react_tierlist` | Session creation is rejected with a typed `UNSUPPORTED_RANKING_SOURCE` error; the app never guesses how to coerce the artifact |
| Submitted proposal omits an item, duplicates an item, or changes the item set | The proposal is rejected and the client is returned to the last valid working order with explicit validation errors |
| Same viewer submits the exact same order repeatedly | The system preserves the first submitted proposal and marks later identical submissions as `duplicate_suppressed` instead of creating noisy clones |
| Optional defense-audio upload fails after reorder submit | The proposal remains submitted as a non-audio artifact, and the defense attachment stays retryable under the same CORE upload ticket |
| DPA resolution degrades | The comparison surface falls back to the safe default palette while preserving the distinct original/proposal data model |

## 7. Tasks

### Frontend
- [ ] Build the standalone Ranking Quiz Mini App in `apps/react-ranking-quiz/`
- [ ] Add typed session, proposal, and diff contracts in `apps/react-ranking-quiz/app/lib/types.ts`
- [ ] Implement seed-load, submit, and comparison API calls in `apps/react-ranking-quiz/app/lib/api.ts`
- [ ] Implement local reorder state and dedup guards in `apps/react-ranking-quiz/app/lib/state.ts`
- [ ] Implement final-order validation in `apps/react-ranking-quiz/app/lib/reorder-validation.ts`
- [ ] Implement slot-delta comparison logic in `apps/react-ranking-quiz/app/lib/diff-engine.ts`
- [ ] Build the immutable original-ranking card in `apps/react-ranking-quiz/app/components/original-ranking-card.tsx`
- [ ] Build the drag-and-drop proposal board in `apps/react-ranking-quiz/app/components/proposal-board.tsx`
- [ ] Build individual draggable list items in `apps/react-ranking-quiz/app/components/draggable-ranking-item.tsx`
- [ ] Build the diff reveal panel in `apps/react-ranking-quiz/app/components/proposal-diff-panel.tsx`
- [ ] Build the proposal submission surface in `apps/react-ranking-quiz/app/components/proposal-submit-sheet.tsx`
- [ ] Build optional defense capture in `apps/react-ranking-quiz/app/components/optional-defense-recorder.tsx`
- [ ] Build the original-vs-proposal comparison view in `apps/react-ranking-quiz/app/components/comparison-reveal.tsx`

### Backend
- [ ] Create `src/ccp/models/reaction_ranking_quiz_models.py`
- [ ] Create `src/ccp/services/reaction_ranking_quiz_projection.py`
- [ ] Create `src/ccp/api/reaction_ranking_quiz_api.py`
- [ ] Register ranking-quiz routes in `src/ccp/api/main.py`
- [ ] Extend `src/ccp/scripts/setup_supabase.py` with `reaction_ranking_quiz_sessions` and `reaction_ranking_quiz_proposals`
- [ ] Write receipt events for session create, proposal submit, defense attach, and duplicate suppression in `src/ccp/core/receipt_chain.py` consumers

### Verification
- [ ] Create `tests/integration/test_era3_fr05j_ranking_quiz_api.py`
- [ ] Create `tests/integration/test_era3_fr05j_ranking_quiz_projection.py`
- [ ] Create `tests/integration/test_era3_fr05j_ranking_quiz_contracts.py`
- [ ] Create `apps/react-ranking-quiz/app/__tests__/proposal-board.test.tsx`
- [ ] Create `apps/react-ranking-quiz/app/__tests__/diff-engine.test.tsx`
- [ ] Create `apps/react-ranking-quiz/app/__tests__/proposal-submit-sheet.test.tsx`

## 8. Acceptance Criteria

### AC-5.4A - Viewing a Published Tierlist Creates a Reorderable Audience Proposal Surface

**CBAR Mandate enforced:** Phase2-M04 (transitive seed gate)

**Given** I publish a completed Tierlist,
**When** a user opens the Ranking Quiz Co-Creation Mini App from that published artifact,
**Then** the app loads the coach's ranking as an immutable source snapshot,
**And** the viewer can drag-and-drop the same item set into a new proposed order,
**And** the original ranking is not edited in place.

**FAILURE EXAMPLE:** The viewer drags one item and the coach's original published board changes for everyone because the system reused the source ranking as the working state. The challenge no longer has an original stance to disagree with. This is a spec violation.

**Measurable pass condition:** the session projection contains one `RankingQuizOriginalRanking` and one separate working proposal order before submission, with different object identities and independent persistence paths.

### AC-5.4B - Audience-Proposed Alternatives Are Stored Distinctly From the Coach's Ranking

**CBAR Mandate enforced:** None directly

**Given** a viewer finishes reordering the ranking,
**When** they submit the proposal,
**Then** the backend stores a distinct `RankingQuizProposalArtifact`,
**And** it links back to the immutable source ranking by `session_id` and `source_artifact_id`,
**And** the proposal record contains its own order payload and diff summary.

**FAILURE EXAMPLE:** The backend stores only the latest board JSON and overwrites the coach's source order, making it impossible to know what the original ranking was or who proposed the alternative. This is a spec violation.

**Measurable pass condition:** one submitted challenge creates exactly one new row in `reaction_ranking_quiz_proposals` while leaving the `original_ranking` snapshot unchanged.

### AC-5.4C - The Comparison Reveal Shows Exactly How the Proposal Challenges the Original Order

**CBAR Mandate enforced:** None directly

**Given** a proposal has been submitted,
**When** the comparison view renders,
**Then** the app shows the original ranking beside the proposal,
**And** every moved item displays `original_slot_index`, `proposed_slot_index`, and `slot_delta`,
**And** unchanged items are not misreported as changed.

**FAILURE EXAMPLE:** The reveal view shows only the proposal list with no original comparison or slot movement explanation. The audience cannot see what the challenger actually disputed. This is a spec violation.

**Measurable pass condition:** `len(diff_entries)` equals the count of items where `original_slot_index != proposed_slot_index`, and every diff entry contains exact original/proposed positions.

### AC-5.4D - Optional Defense Audio Does Not Block Proposal Submission

**CBAR Mandate enforced:** Phase2-M02 and Phase2-M03 (inherited through optional defense mode)

**Given** a challenger chooses to defend their reordered list with audio,
**When** they stop the defense recording,
**Then** the proposal remains visible immediately,
**And** defense audio uploads in the background through the CORE contract,
**And** any defense scorecard is attached only through the streamed chunk-scoring path.

**FAILURE EXAMPLE:** The user submits a proposal, records a defense take, and then waits on a blocking upload spinner before seeing their comparison result. On a weak mobile connection the defense upload stalls and the whole challenge appears lost. This is a spec violation.

**Measurable pass condition:** proposal submit completes independently of defense upload completion, and any defense scorecard arrival references a streamed CORE session rather than a post-stop full-file-only scoring path.

## 9. Dependencies

### Internal

| Service/Spec | Dependency Type | What This Spec Needs From It |
|---|---|---|
| `FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | Upstream spec dependency | Optional defense-session lifecycle, DPA continuity, shared identity/session assumptions |
| `FR-ERA3-25_AR_Overlay_Capture_Pipeline_Tech_Spec.md` | Shared spec dependency | Camera feed, PixiJS overlay rendering, composite video capture, sound engine, interaction journal |
| `FR-ERA3-05d_Tierlist_Authority_Tech_Spec.md` | Upstream artifact dependency | Published Tierlist artifact shape and publish-state semantics |
| `src/ccp/api/main.py` | Code extension | Route registration and readiness diagnostics |
| `src/ccp/services/dpa_engine.py` | Runtime dependency | `DPAEngine.resolve(...)` branding continuity |
| `src/ccp/services/trait_scoring_engine.py` | Runtime dependency | Trait-based scoring substrate for optional defense audio |
| `src/ccp/services/signal_source_loader.py` | Runtime dependency | Dependency gate before emitting scored defense results |
| `src/ccp/core/receipt_chain.py` | Runtime dependency | Immutable session/proposal audit logging |
| `src/ccp/scripts/setup_supabase.py` | Migration dependency | Canonical place to extend PostgreSQL schema |
| `src/ccp/models/ca11_models.py` | Model dependency | `ResolvedPalette` reuse |

### External

| API/Library | Version | Purpose |
|---|---|---|
| Next.js | workspace-pinned | Ranking Quiz Mini App runtime |
| React | workspace-pinned | Drag-and-drop UI, comparison reveal, defense sheet |
| TypeScript | workspace-pinned | Typed client contracts |
| FastAPI | existing backend dependency | Ranking Quiz API routes |
| Pydantic v2 | existing backend dependency | Typed ranking-quiz models |
| Telegram Web App API | current platform | Mini App launch and identity context |
| Browser drag-and-drop / pointer events | modern mobile browser capability | Reordering interaction |
| Browser `MediaRecorder` | modern mobile browser capability | Optional defense-audio capture |

## 10. Testing Strategy

### Unit Tests

**File:** `apps/react-ranking-quiz/app/__tests__/proposal-board.test.tsx`
- `describe("ProposalBoard")`
- `it("renders the immutable source ranking and the mutable working proposal separately")`
- `it("reorders items without changing the original ranking snapshot")`

**File:** `apps/react-ranking-quiz/app/__tests__/diff-engine.test.tsx`
- `describe("diff-engine")`
- `it("computes slot deltas only for items whose positions changed")`
- `it("rejects proposals that contain missing or duplicated item ids")`

**File:** `apps/react-ranking-quiz/app/__tests__/proposal-submit-sheet.test.tsx`
- `describe("ProposalSubmitSheet")`
- `it("submits a proposal artifact with caption and diff summary")`
- `it("keeps proposal submission complete when optional defense upload is still pending")`

### Integration Tests

Modeled on `tests/integration/test_ca11_fr15_dpa_engine.py` and `tests/integration/test_ca11_fr19_trivianar_engine.py`:
- use a local `_run()` helper for async code paths
- organize tests by scenario class
- create small builders for source rankings, proposal payloads, and duplicate submissions
- assert exact typed fields and state transitions directly

**File:** `tests/integration/test_era3_fr05j_ranking_quiz_projection.py`

```python
def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


class TestRankingQuizProjection:
    def test_session_freezes_original_tierlist_snapshot(self): ...
    def test_proposal_diff_entries_match_actual_slot_changes(self): ...
    def test_duplicate_item_submission_is_rejected(self): ...
```

**File:** `tests/integration/test_era3_fr05j_ranking_quiz_api.py`

```python
class TestRankingQuizApi:
    def test_only_published_tierlist_artifacts_can_seed_sessions(self): ...
    def test_submitted_proposal_creates_distinct_proposal_row(self): ...
    def test_optional_defense_attach_does_not_block_proposal_submit(self): ...
```

**File:** `tests/integration/test_era3_fr05j_ranking_quiz_contracts.py`

```python
class TestRankingQuizContracts:
    def test_original_ranking_and_proposal_use_distinct_models(self): ...
    def test_duplicate_submission_returns_duplicate_suppressed_status(self): ...
    def test_comparison_projection_embeds_slot_delta_entries(self): ...
```

### Manual Verification

1. Launch the Mini App with `startapp=react_ranking_quiz` from a published Tierlist artifact.
2. Confirm the original coach ranking renders as a frozen source view and cannot be edited directly.
3. Drag items into a new order and confirm only the working proposal board changes.
4. Submit the proposal and verify a distinct proposal artifact is created without mutating the source ranking.
5. Open the comparison reveal and confirm the app shows original vs proposal plus exact moved-slot deltas.
6. Submit an invalid reorder payload with a duplicate or missing item and confirm the backend rejects it cleanly.
7. Submit the same final order twice from the same viewer and confirm the second attempt is deduplicated rather than cloned.
8. Record an optional defense take and confirm the comparison result stays visible immediately while upload continues in the background.
9. Verify any attached defense scorecard references the shared CORE scoring path rather than a separate ranking-quiz scoring engine.
10. Inspect receipts and confirm session create, proposal submit, and optional defense attach events are logged independently.
