# Tech-Spec: FR-ERA3-35C — Eval Card System UPDATED FOR LIVING COMMENTARY AND SSS
**Created:** 2026-05-19
**Updated:** 2026-05-24
**Status:** Ready for Development
**Version:** 2.0 (ERA3 — Phase 7 Living Commentary & Coach Communication Stack)
**Phase:** 7 — Living Commentary & Coach Communication Stack
**Architecture Reference:** `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`

---

## Pre-Work Log

```text
1. PROTOCOL LOADED:   ERA3_Tech_Spec_Writing_Protocol.md. §2: extend existing backend (201 services, 45 model files). §3: pre-flight with real backend mapping. §4: 10-section format, min 280 lines. §7: CBAR mandates must be loaded from Phase Epic files.
2. PRD-02 LOADED:     docs/prd/modules/PRD_02_CCF_Content_Factory.md. Content compiler chain: "truth → transcription → force → delivery → variation → phenotype → evaluation." §2.4: "keep the archetypes, change the realization grammar." Living Commentary correction: the eval layer must now score delivery presence as a primary dimension.
3. PRD-05 LOADED:     docs/prd/modules/PRD_05_CBCS_Law28.md. §2.1A: Dual-Program Architecture — "CCP Program | Participant: the coach themselves | Purpose: improve the coach's own communication, speaking, delivery, and authority." §5.3: FR61 evidence contract — conviction density, hedge frequency, pause architecture, pitch stability. §5.11: User Cards — collectible identity-bearing card with tier badge, primary stats, weekly delta arrows, streak counter, card color tied to progression tier. Color progression: Foundation → Bronze/earth, Structure → Silver/steel, Nuance → Gold/warm glow, Command → Platinum/white-hot, Sovereign → Prismatic/holographic.
4. HANDOVER LOADED:   docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md. §1.C: "Before final editing, the recorded video's performance is formally scored." §1.B: 4 Vertical Video Realization Formats. §1.C: Complete Editing Session wrapper ensures zero data loss and trigger-first execution.
5. PIVOTS AUDIT:      docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md. §8: "Performance Scoring: The recorded video is formally scored." Absolute ban on synthetic voice. Memetic sound limits: Format 1-3 at 1/30s, Format 4 at 1/10s.
6. LIVING COMMENTARY SOURCE:  lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md. §2.2: "Living Commentary surfaces reintroduce what the AI-saturated market still struggles to fake: delivery, atmosphere, conviction, timing, judgment." §4: Six format families — Quote, Comparison, Screenshot, Atmospheric, Cinematic Story, Animated Explainer.
7. ROADMAP LOADED:    lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md. §4.1 W4: Delivery Module Mastery — "coach practice task → record module → score delivery → feedback → optional content extraction → longitudinal progress." Modules: hook, authority, positioning, testimonial/proof stack, identification, permission to be seen, micro-commitment, commitment escalation, hope, intrigue, objection handling, humor, storytelling, contextual explanation, transitions, close. §4.1 W5A: "module practice → record or go live → review → SSS card update → badge progression → next weakness-targeted drill." §4.4: "Seminar Speaking Score Card Layer — A coach-facing scored progression layer that tracks long-form delivery competence across module families and updates after rehearsal, recorded runs, and live events. This should support visible progression states, including: Elite Seminar Master."
8. EXISTING SPEC:     docs/architecture/april_updates/FR-ERA3-35C_Eval_Card_System_And_Shareable_Audit_Board_Tech_Spec.md (v1.0). §5.1: VisibleCardStatKey enum (humanity, presence, trust, memorability, resonance, signal, ai_slop_risk). §5.2: EvalCardRole enum (audit_primary, audit_secondary, before_snapshot, after_snapshot, marketing_preview, operator_review). §5.3: EvalBoardKind enum (single_card_detail, audit_spread, before_after_comparison, shareable_summary). §5.10: EvalCardFace with validate_visible_stats_keys enforcing exactly 7 stats. §3.4: No-Jargon-On-Card Rule, Canonical-Evals-Underneath Rule, Shareable-Audit Rule, Thumbnail-First Rule, Failure-Closed Law.
9. BACKEND LOADED:    src/ccp/models/phase0_eval_card_models.py (147 lines). VisibleCardStatKey, EvalCardRole, EvalBoardKind, CardScoreBand, BoardDensity enums. EvalCardFace with @model_validator(mode="after") validate_visible_stats_keys(). EvalCard, EvalCardBoard, ShareableAuditBoardRenderRequest models.
10. PROJECTION SVC:   src/ccp/services/eval_card_projection_service.py (267 lines). EvalCardProjectionService.__init__(coach_acronym, log_dir). _determine_score_band(score) → CardScoreBand. async project_card(report, role, brand_hue_override) → EvalCard. DPA theme resolution with fallback. Receipt chain logging.
11. ASSEMBLY SVC:     src/ccp/services/eval_board_assembly_service.py (130 lines). EvalBoardAssemblyService.assemble_board(report_id, board_kind, cards, title, subtitle, density, columns, featured_card_id) → EvalCardBoard. Before/after ordering law. Auto-column resolution. Share caption synthesis.
12. TESTS LOADED:     tests/integration/test_era3_fr35c_eval_card_system.py (162 lines). TestFRERA335CEvalCardSystemIntegration class. Tests: report generation → card projection → direct card projection → board assembly (before/after ordering) → board rendering with watermark. Uses ReceiptChain.query() for audit trail assertion.
13. FR-ERA3-35B v2.0: docs/architecture/april_updates/FR-ERA3-35B_Content_Benchmark_Profiles_Tech_Spec_UPDATED_FOR_LIVING_COMMENTARY.md. §5.7: SSSBridgePacket — packet_id, coach_id, format_family, delivery_dimensions (DeliveryQualityDimensions), composite_delivery_score, presence_weight_applied, anti_slop_passed, content_asset_id, scored_at. This is a one-way feed: 35B produces it, 35C consumes it.
```

---

## 1. Files Read

| # | File | Purpose |
|---|------|---------|
| 1 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory 10-section format, backend mapping, CBAR mandates |
| 2 | `docs/prd/modules/PRD_02_CCF_Content_Factory.md` | Content compiler chain, Living Commentary correction, evaluation layer expectations |
| 3 | `docs/prd/modules/PRD_05_CBCS_Law28.md` | CBCS dual-program architecture, FR61 evidence, User Card tiers, speaking progression |
| 4 | `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` | Performance scoring mandate, 4 Vertical Video formats, Complete Editing Session |
| 5 | `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` | Formal scoring mandate, memetic sound limits, synthetic voice ban |
| 6 | `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md` | 6 format families, delivery-led realization, atmospheric field doctrine |
| 7 | `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md` | W4 Delivery Module Mastery (16 modules), W5A SSS Loop, SSS Card Layer, Elite Seminar Master |
| 8 | `docs/architecture/april_updates/FR-ERA3-35C_Eval_Card_System_And_Shareable_Audit_Board_Tech_Spec.md` | Base spec v1.0 — all existing schemas, governance rules, presentation contracts |
| 9 | `src/ccp/models/phase0_eval_card_models.py` | Existing Pydantic v2 models for eval cards (147 lines) |
| 10 | `src/ccp/services/eval_card_projection_service.py` | Existing card projection service (267 lines) — projection pattern reference |
| 11 | `src/ccp/services/eval_board_assembly_service.py` | Existing board assembly service (130 lines) — assembly pattern reference |
| 12 | `tests/integration/test_era3_fr35c_eval_card_system.py` | Existing integration tests (162 lines) — test pattern reference |
| 13 | `docs/architecture/april_updates/FR-ERA3-35B_Content_Benchmark_Profiles_Tech_Spec_UPDATED_FOR_LIVING_COMMENTARY.md` | SSSBridgePacket schema — upstream feed from 35B into 35C |

---

## 2. Overview

### 2.1 Problem Statement

The v1.0 FR-ERA3-35C spec defines a presentation layer for **Phase-0 content audit cards**: single-image posts, carousels, and reels scored on 7 static visible stats (Humanity, Presence, Trust, Memorability, Resonance, Signal, AI Slop Risk). The existing `EvalCardRole` enum (`audit_primary`, `before_snapshot`, `after_snapshot`, etc.) and the board types (`audit_spread`, `before_after_comparison`, `shareable_summary`) were designed for a prospect-facing audit reveal surface where the coach's own delivery competence is not tracked.

Living Commentary and the Coach Communication Stack break that assumption in three ways:

1. **Living Commentary needs format-specific eval cards.** A Living Commentary piece has unique quality criteria — motion grammar activation, sonic doctrine compliance, atmospheric field presence, delivery presence — that the current 7-stat card face cannot express. The system needs a card type that evaluates the Living Commentary output itself, not just the caption/content text.

2. **Coaches need a Seminar Speaking Score (SSS) progression card.** The W5A loop (Roadmap §4.1) defines: `module practice → record or go live → review → SSS card update → badge progression → next weakness-targeted drill`. The coach must be able to see their long-form delivery competence visually, track module-family mastery, and progress toward `Elite Seminar Master`. No such card type exists in the v1.0 system.

3. **Individual delivery module practice needs eval cards.** The W4 Delivery Module Mastery workflow tracks 16 communication modules (hook, authority, positioning, proof stack, identification, permission to be seen, micro-commitment, commitment escalation, hope, intrigue, objection handling, humor, storytelling, contextual explanation, transitions, close). Each practice run should produce a scored eval card that feeds into the SSS progression.

Without this update, the eval card system:
- Cannot display Living Commentary quality evaluations to operators or coaches.
- Cannot show coaches their speaking progression or badge status.
- Cannot track individual module mastery through scored eval cards.
- Cannot surface SSS progression on the shareable audit board.

### 2.2 Solution

This update **extends** the existing v1.0 eval card presentation substrate with four new card types and one progression system:

1. **`LivingCommentaryEvalCard`** — evaluates Living Commentary output quality across motion grammar, sound discipline, atmospheric field, primitive expression, and delivery presence.
2. **`SeminarSpeakingScoreCard`** — the SSS card tracking overall long-form delivery competence, module-family mastery scores, level title, and badge tier.
3. **`DeliveryModuleEvalCard`** — evaluates individual delivery module practice runs (hook, authority, close, etc.) with module-specific criteria.
4. **`EliteSeminarMasterBadgeProgression`** — defines the badge tier system from Novice through Elite Seminar Master with threshold rules.
5. **`SSSUpdateTrigger`** — the state machine tracking trigger events that update the SSS card.

### 2.3 Scope

**In scope:** New card type enums, Living Commentary eval card schema, SSS card schema, delivery module eval card schema, badge progression model, SSS update trigger engine, new board kinds for SSS progression display, extension of projection and assembly services, new Supabase tables, new test coverage.

**Out of scope:** The delivery quality dimension scoring (FR-ERA3-35B), the benchmark profile resolution (FR-ERA3-35B), the CMF rendering pipeline (FR-ERA3-12), the Persuasive Speaking Program runtime (FR-ERA3-48), the SSS Card and Badge Runtime runtime engine (FR-ERA3-49A).

### 2.4 Relationship to v1.0

This spec is **additive**. All v1.0 schemas (`EvalCard`, `EvalCardFace`, `EvalCardStatLine`, `EvalCardBoard`, `EvalBoardLayout`, `CardThumbnailAsset`, `CardVerdictBlock`, `CardThemeProjection`, `ShareableAuditBoardRenderRequest`) remain unchanged. New card types extend the existing model file. New `EvalCardRole` values extend the enum. Existing board types, projection services, and assembly logic remain valid and active.

---

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Payload / Data Object | Source | Responsibility |
|---|---|---|---|
| DEP-ERA3-35C-001 | `EvalCard` | FR-ERA3-35C v1.0 | Canonical rendered score card object (retained) |
| DEP-ERA3-35C-002 | `EvalCardFace` | FR-ERA3-35C v1.0 | Visible front-face content (retained) |
| DEP-ERA3-35C-004 | `EvalCardBoard` | FR-ERA3-35C v1.0 | Multi-card board payload (retained) |
| DEP-ERA3-35C-010 | `LivingCommentaryEvalCard` | FR-ERA3-35C v2.0 | Living Commentary quality eval card |
| DEP-ERA3-35C-011 | `SeminarSpeakingScoreCard` | FR-ERA3-35C v2.0 | SSS progression card |
| DEP-ERA3-35C-012 | `DeliveryModuleEvalCard` | FR-ERA3-35C v2.0 | Individual module practice eval card |
| DEP-ERA3-35C-013 | `EliteSeminarMasterBadgeProgression` | FR-ERA3-35C v2.0 | Badge tier progression model |
| DEP-ERA3-35C-014 | `SSSUpdateTrigger` | FR-ERA3-35C v2.0 | SSS card update trigger event |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|---|---|---|
| `phase0_eval_card_models.py` | `src/ccp/models/` | **EXTENDS** with new models: `LivingCommentaryEvalCard`, `SeminarSpeakingScoreCard`, `DeliveryModuleEvalCard`, `EliteSeminarMasterBadgeProgression`, extended `EvalCardRole` enum, extended `EvalBoardKind` enum, new `SSSUpdateTriggerType` enum, new `DeliveryModuleFamily` enum, new `BadgeTier` enum, new `SSSLevelTitle` enum |
| `eval_card_projection_service.py` | `src/ccp/services/` | **EXTENDS** with `project_lc_eval_card()`, `project_sss_card()`, `project_module_eval_card()` methods |
| `eval_board_assembly_service.py` | `src/ccp/services/` | **EXTENDS** with `assemble_sss_progression_board()` method for SSS-specific board layout |
| `benchmark_profile_models.py` | `src/ccp/models/` | **READ** — consumes `SSSBridgePacket`, `DeliveryQualityDimensions`, `LivingCommentaryFormatFamily` from FR-ERA3-35B v2.0 |
| `trait_scoring_engine.py` | `src/ccp/services/` | **READ** — scoring pattern reference: evidence-based rubric, `tuple[int, list[TraitEvidence]]` return pattern |
| `test_era3_fr35c_eval_card_system.py` | `tests/integration/` | **EXTENDS** with new test classes for Living Commentary eval cards, SSS cards, and badge progression |

### 3.3 Eval Card Contracts

| Artifact | Layer | What It Governs |
|---|---|---|
| `LivingCommentaryEvalCard` | LC quality substrate | Evaluates Living Commentary output across motion grammar, sound discipline, atmospheric field, delivery presence — separate from the Phase-0 audit card |
| `SeminarSpeakingScoreCard` | SSS progression substrate | Tracks coach-level long-form delivery competence, module mastery scores, level title, badge tier — the coach-facing progression card |
| `DeliveryModuleEvalCard` | Module practice substrate | Evaluates individual module practice runs (hook, authority, close, etc.) with module-specific criteria and rubric scores |
| `EliteSeminarMasterBadgeProgression` | Badge governance | Defines tier thresholds, progression rules, and visible level titles from Novice to Elite Seminar Master |
| `SSSUpdateTrigger` | Trigger governance | Defines the events that cause SSS card updates: module rehearsal, recorded run, live event, scorecard computation, badge evaluation |

### 3.4 Governance Constraints

| Constraint | Origin | Enforcement |
|---|---|---|
| No-Jargon-On-Card Rule | v1.0 §3.4.2 (retained) | New card types MUST NOT expose internal labels like "anti-centroid integrity" or "semantic integrity carry-through" on the visible face |
| Canonical-Evals-Underneath Rule | v1.0 §3.4.3 (retained) | New cards consume canonical evals and bridge packets rather than inventing scores at render time |
| Thumbnail-First Rule | v1.0 §3.4.6 (retained) | Living Commentary eval cards MUST show the content thumbnail or key frame first |
| Failure-Closed Law | v1.0 §3.4 (retained) | If required stats are missing or renamed, card validation MUST crash rather than rendering corrupted surfaces |
| Eval-Card-Preserves-Ownership Rule | Spec prompt CBAR | SSS cards belong to the coach; they display the coach's own progression, not client data |
| SSS-Progression-Visibility Rule | Spec prompt CBAR | The coach MUST be able to see their SSS progression visually with level title, badge tier, and module-family breakdown |
| Honest-Partiality Rule | v1.0 §3.4.10 (retained) | If delivery dimension data is incomplete, the SSS card MUST honestly mark it |
| No-Render-Time-Score-Invention Rule | v1.0 §3.4 (retained) | SSS card scores come from `SSSBridgePacket` aggregation, not from card-layer computation |
| Badge-Progression-Monotonic Rule | Roadmap W5A | Badge tier may advance but MUST NOT regress — once earned, a tier is permanent |
| Delivery-Quality-Dependence Warning | Audit SWOT §7 | System acknowledges that weak delivery degrades output quality regardless of visual sophistication |

### 3.5 Technical Decisions

| Decision | Rationale | Consequence |
|---|---|---|
| New card types are sibling models, not subclasses of `EvalCard` | Living Commentary eval cards and SSS cards have fundamentally different face structures than Phase-0 audit cards; forcing them into the 7-stat face would violate the Format-Specific-Card Rule | Each new card type has its own face model and validation logic |
| `DeliveryModuleFamily` enum covers 16 modules | Roadmap §4.1 W4 lists exactly 16 delivery modules; the enum is exhaustive | New modules require formal enum extension |
| `BadgeTier` enum mirrors PRD-05 §5.11 color progression | Foundation→Bronze, Structure→Silver, Nuance→Gold, Command→Platinum, Sovereign→Prismatic aligns with existing User Card color tiers | Consistent visual identity across challenge cards and SSS cards |
| SSS card consumes `SSSBridgePacket` from FR-ERA3-35B | One-way feed prevents circular dependency between 35B and 35C | SSS card never calls back into 35B benchmark resolution |
| Anti-slop gate verdict is displayed on LC eval cards | Coaches and operators need to see when content fails the anti-slop gate | LC eval card carries `anti_slop_verdict` with pass/fail and rejection reasons |
| SSS update triggers are typed events, not ad-hoc strings | Prevents trigger drift and enables typed state machine transitions | `SSSUpdateTriggerType` enum enforces valid trigger types |
| Badge progression is monotonic (no regression) | Earned mastery should never be taken away; this prevents punitive UX | Once a `BadgeTier` is earned, the system only tracks forward movement |
| New board kinds for SSS display | SSS progression needs dedicated board layouts that show module-family breakdown and badge timeline | New `EvalBoardKind` values: `sss_progression_detail`, `sss_module_mastery_spread` |
| New `EvalCardRole` values for new card types | Existing roles (`audit_primary`, `before_snapshot`) do not semantically cover SSS or LC eval cards | New roles: `lc_eval`, `sss_progression`, `module_eval` |

---

## 4. Implementation Plan

### Phase 1 — New Enums and Core Types (Tasks 1–5)

1. Add `DeliveryModuleFamily` enum to `phase0_eval_card_models.py` with 16 values matching Roadmap W4 module list.
2. Add `BadgeTier` enum with 6 tiers: `NOVICE`, `BRONZE`, `SILVER`, `GOLD`, `PLATINUM`, `PRISMATIC`.
3. Add `SSSLevelTitle` enum with visible progression titles: `BEGINNER`, `DEVELOPING_SPEAKER`, `COMPETENT_SPEAKER`, `ADVANCED_SPEAKER`, `EXPERT_SPEAKER`, `ELITE_SEMINAR_MASTER`.
4. Add `SSSUpdateTriggerType` enum with 5 values: `MODULE_REHEARSAL`, `RECORDED_RUN`, `LIVE_EVENT`, `SCORECARD_COMPUTATION`, `BADGE_EVALUATION`.
5. Extend `EvalCardRole` enum with 3 new values: `lc_eval`, `sss_progression`, `module_eval`. Extend `EvalBoardKind` enum with 2 new values: `sss_progression_detail`, `sss_module_mastery_spread`.

### Phase 2 — Living Commentary Eval Card Models (Tasks 6–9)

6. Define `LCEvalCriterion` model for individual Living Commentary evaluation criteria (motion grammar, sound discipline, atmospheric field, delivery presence, primitive expression).
7. Define `LCEvalCardFace` model with format family, content type, LC-specific criteria list, anti-slop verdict, delivery composite score, presence weight applied, and verdict block.
8. Define `LivingCommentaryEvalCard` model wrapping `LCEvalCardFace` with card metadata, theme projection, and content asset reference.
9. Add `LCEvalCardFace` validator enforcing minimum 4 criteria and format-family-specific criterion presence.

### Phase 3 — SSS Card and Badge Models (Tasks 10–16)

10. Define `ModuleMasteryScore` model keyed by `DeliveryModuleFamily`, containing score (0–100), practice count, last practiced timestamp, and trend direction.
11. Define `SSSCardFace` model containing overall SSS score (0–100), module mastery scores map, level title, badge tier, total practice sessions, total recorded runs, total live events, strongest module, weakest module, and last update timestamp.
12. Define `SeminarSpeakingScoreCard` model wrapping `SSSCardFace` with card metadata, coach ID, theme projection, and confidence note.
13. Define `SSSUpdateTrigger` model containing trigger type, coach ID, module family, source asset ID, delivery dimensions snapshot, composite score, timestamp.
14. Define `SSSUpdateResult` model containing previous SSS score, new SSS score, previous level, new level, previous badge, new badge, modules updated, trigger ID.
15. Define `BadgeThreshold` model mapping `BadgeTier` to minimum SSS score, minimum modules mastered, minimum practice sessions, minimum live events.
16. Define `EliteSeminarMasterBadgeProgression` model containing the full threshold table, current tier, earned tiers history, and next tier requirements.

### Phase 4 — Delivery Module Eval Card Models (Tasks 17–19)

17. Define `ModuleEvalCriterion` model for module-specific evaluation criteria (module-level rubric scores, evidence citations).
18. Define `ModuleEvalCardFace` model containing module family, module score (0–100), practice type (rehearsal / recorded / live), criteria list, delivery dimension snapshot, and verdict block.
19. Define `DeliveryModuleEvalCard` model wrapping `ModuleEvalCardFace` with card metadata, coach ID, theme projection, and SSS contribution flag.

### Phase 5 — Projection and Assembly Services (Tasks 20–25)

20. Add `project_lc_eval_card(lc_benchmark_result, format_family, anti_slop_verdict)` method to `EvalCardProjectionService`.
21. Add `project_sss_card(coach_id, sss_state, badge_progression)` method to `EvalCardProjectionService`.
22. Add `project_module_eval_card(coach_id, module_family, module_score, practice_type, delivery_dimensions)` method to `EvalCardProjectionService`.
23. Add `assemble_sss_progression_board(coach_id, sss_card, module_cards, badge_progression)` method to `EvalBoardAssemblyService`.
24. Add `assemble_sss_module_mastery_spread(coach_id, module_cards)` method to `EvalBoardAssemblyService` for module-family breakdown layout.
25. Create `SSSUpdateProcessor` service with `process_trigger(trigger: SSSUpdateTrigger) → SSSUpdateResult` method that consumes `SSSBridgePacket` data and updates the SSS card state.

### Phase 6 — Persistence (Tasks 26–29)

26. Create `living_commentary_eval_cards` Supabase table.
27. Create `seminar_speaking_score_cards` Supabase table.
28. Create `delivery_module_eval_cards` Supabase table.
29. Create `sss_update_triggers` Supabase table.

### Phase 7 — Testing (Tasks 30–36)

30. Unit tests for `LCEvalCardFace` validator (minimum criteria, format-family-specific criterion presence).
31. Unit tests for `SSSCardFace` score range validation and level/badge assignment.
32. Unit tests for `EliteSeminarMasterBadgeProgression` monotonic tier advancement.
33. Unit tests for `SSSUpdateTrigger` type validation and state transitions.
34. Integration tests for Living Commentary eval card projection chain.
35. Integration tests for SSS card projection and update chain.
36. Non-regression tests confirming v1.0 Phase-0 audit cards remain unchanged.

---

## 5. Schema

### 5.1 New Enums

```python
class DeliveryModuleFamily(str, Enum):
    """The 16 delivery module families from Roadmap §4.1 W4."""
    HOOK = "hook"
    AUTHORITY = "authority"
    POSITIONING = "positioning"
    PROOF_STACK = "proof_stack"
    IDENTIFICATION = "identification"
    PERMISSION_TO_BE_SEEN = "permission_to_be_seen"
    MICRO_COMMITMENT = "micro_commitment"
    COMMITMENT_ESCALATION = "commitment_escalation"
    HOPE = "hope"
    INTRIGUE = "intrigue"
    OBJECTION_HANDLING = "objection_handling"
    HUMOR = "humor"
    STORYTELLING = "storytelling"
    CONTEXTUAL_EXPLANATION = "contextual_explanation"
    TRANSITIONS = "transitions"
    CLOSE = "close"


class BadgeTier(str, Enum):
    """Badge tiers aligned with PRD-05 §5.11 User Card color progression.

    Foundation → Bronze/earth
    Structure → Silver/steel
    Nuance → Gold/warm glow
    Command → Platinum/white-hot
    Sovereign → Prismatic/holographic
    """
    NOVICE = "novice"
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    PRISMATIC = "prismatic"


class SSSLevelTitle(str, Enum):
    """Coach-visible level titles for the Seminar Speaking Score progression."""
    BEGINNER = "Beginner"
    DEVELOPING_SPEAKER = "Developing Speaker"
    COMPETENT_SPEAKER = "Competent Speaker"
    ADVANCED_SPEAKER = "Advanced Speaker"
    EXPERT_SPEAKER = "Expert Speaker"
    ELITE_SEMINAR_MASTER = "Elite Seminar Master"


class SSSUpdateTriggerType(str, Enum):
    """Typed trigger events that cause SSS card updates.

    Flow: module_rehearsal → recorded_run → live_event
          → scorecard_computation → badge_evaluation
    """
    MODULE_REHEARSAL = "module_rehearsal"
    RECORDED_RUN = "recorded_run"
    LIVE_EVENT = "live_event"
    SCORECARD_COMPUTATION = "scorecard_computation"
    BADGE_EVALUATION = "badge_evaluation"


class TrendDirection(str, Enum):
    """Trend direction for module mastery tracking."""
    IMPROVING = "improving"
    FLAT = "flat"
    DECLINING = "declining"


class PracticeType(str, Enum):
    """Type of delivery module practice session."""
    REHEARSAL = "rehearsal"
    RECORDED = "recorded"
    LIVE = "live"
```

### 5.2 Extended EvalCardRole Enum

```python
class EvalCardRole(str, Enum):
    # --- v1.0 retained ---
    audit_primary = "audit_primary"
    audit_secondary = "audit_secondary"
    before_snapshot = "before_snapshot"
    after_snapshot = "after_snapshot"
    marketing_preview = "marketing_preview"
    operator_review = "operator_review"
    # --- v2.0 Living Commentary & SSS additions ---
    lc_eval = "lc_eval"
    sss_progression = "sss_progression"
    module_eval = "module_eval"
```

### 5.3 Extended EvalBoardKind Enum

```python
class EvalBoardKind(str, Enum):
    # --- v1.0 retained ---
    single_card_detail = "single_card_detail"
    audit_spread = "audit_spread"
    before_after_comparison = "before_after_comparison"
    shareable_summary = "shareable_summary"
    # --- v2.0 SSS additions ---
    sss_progression_detail = "sss_progression_detail"
    sss_module_mastery_spread = "sss_module_mastery_spread"
```

### 5.4 Living Commentary Eval Card

```python
class LCEvalCriterion(BaseModel):
    """A single evaluation criterion for Living Commentary output quality."""
    criterion_id: str = Field(min_length=1)
    criterion_name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    score: float = Field(ge=0.0, le=100.0)
    weight: float = Field(ge=0.0, le=1.0)
    evidence_summary: str = Field(min_length=1)


class LCEvalCardFace(BaseModel):
    """Face content for a Living Commentary evaluation card.

    Unlike v1.0 EvalCardFace which uses 7 fixed visible stats,
    this face evaluates Living Commentary-specific quality criteria:
    motion grammar activation, sound discipline, atmospheric field,
    delivery presence, and primitive expression.
    """
    title: str = Field(min_length=1)
    subtitle: str | None = Field(default=None)
    thumbnail: CardThumbnailAsset = Field(...)
    format_family: str = Field(min_length=1,
        description="LivingCommentaryFormatFamily value from FR-ERA3-35B")
    content_type: str = Field(min_length=1,
        description="Extended ContentType value from FR-ERA3-35B")
    overall_lc_score: float = Field(ge=0.0, le=100.0)
    delivery_composite_score: float = Field(ge=0.0, le=100.0)
    presence_weight_applied: float = Field(ge=0.0, le=1.0)
    anti_slop_passed: bool
    anti_slop_failures: list[str] = Field(default_factory=list,
        description="List of anti-slop floor criteria that failed")
    criteria: list[LCEvalCriterion] = Field(min_length=4,
        description="At least 4 format-specific evaluation criteria")
    verdict: CardVerdictBlock = Field(...)
    role: EvalCardRole = Field(default=EvalCardRole.lc_eval)

    @model_validator(mode="after")
    def validate_lc_criteria(self) -> "LCEvalCardFace":
        criterion_names = [c.criterion_name for c in self.criteria]
        if len(set(criterion_names)) != len(criterion_names):
            raise ValueError("LC eval criteria must not contain duplicates")
        total_weight = sum(c.weight for c in self.criteria)
        if not (0.99 <= total_weight <= 1.01):
            raise ValueError(
                f"LC eval criteria weights must sum to 1.0, got {total_weight:.4f}"
            )
        return self


class LivingCommentaryEvalCard(BaseModel):
    """Eval card for judging Living Commentary output quality.

    Evaluates motion grammar adherence, sound discipline,
    atmospheric field activation, primitive expression, and delivery presence.
    Separate from the Phase-0 audit card which evaluates caption/content text.
    """
    card_id: str = Field(min_length=1)
    content_asset_id: str = Field(min_length=1)
    coach_id: str = Field(min_length=1)
    face: LCEvalCardFace = Field(...)
    theme: CardThemeProjection = Field(...)
    generated_at: str = Field(min_length=1)
    sss_bridge_packet_id: str | None = Field(default=None,
        description="If this LC eval produced an SSSBridgePacket, reference it here")
```

### 5.5 Seminar Speaking Score Card

```python
class ModuleMasteryScore(BaseModel):
    """Mastery score for a single delivery module family."""
    module_family: DeliveryModuleFamily
    score: float = Field(ge=0.0, le=100.0)
    practice_count: int = Field(ge=0)
    last_practiced_at: str | None = Field(default=None,
        description="ISO 8601 timestamp of last practice")
    trend: TrendDirection = Field(default=TrendDirection.FLAT)
    mastered: bool = Field(default=False,
        description="True when score >= 70 and practice_count >= 5")


class SSSCardFace(BaseModel):
    """Face content for the Seminar Speaking Score progression card.

    This is the coach-facing scored progression card that tracks
    long-form delivery competence across module families.
    """
    title: str = Field(min_length=1)
    subtitle: str | None = Field(default=None)
    thumbnail: CardThumbnailAsset = Field(...)
    overall_sss_score: float = Field(ge=0.0, le=100.0,
        description="Aggregate SSS score across all module families")
    level_title: SSSLevelTitle = Field(...)
    badge_tier: BadgeTier = Field(...)
    module_mastery_scores: list[ModuleMasteryScore] = Field(
        min_length=1,
        description="Mastery scores per module family")
    total_practice_sessions: int = Field(ge=0)
    total_recorded_runs: int = Field(ge=0)
    total_live_events: int = Field(ge=0)
    strongest_module: DeliveryModuleFamily | None = Field(default=None)
    weakest_module: DeliveryModuleFamily | None = Field(default=None)
    modules_mastered_count: int = Field(ge=0,
        description="Number of modules with mastered=True")
    last_updated_at: str = Field(min_length=1,
        description="ISO 8601 timestamp of last SSS update")
    verdict: CardVerdictBlock = Field(...)
    role: EvalCardRole = Field(default=EvalCardRole.sss_progression)


class SeminarSpeakingScoreCard(BaseModel):
    """The SSS card — tracks a coach's long-form delivery competence
    across module families and updates after rehearsal, recorded runs,
    and live events.

    Consumes SSSBridgePacket from FR-ERA3-35B.
    Progression includes visible level states up to Elite Seminar Master.
    """
    card_id: str = Field(min_length=1)
    coach_id: str = Field(min_length=1)
    face: SSSCardFace = Field(...)
    theme: CardThemeProjection = Field(...)
    badge_progression: "EliteSeminarMasterBadgeProgression" = Field(...)
    generated_at: str = Field(min_length=1)
    confidence_note: str | None = Field(default=None,
        description="Honest partiality note if module data is incomplete")
```

### 5.6 Delivery Module Eval Card

```python
class ModuleEvalCriterion(BaseModel):
    """A single evaluation criterion for a delivery module practice run."""
    criterion_id: str = Field(min_length=1)
    criterion_name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    score: float = Field(ge=0.0, le=100.0)
    scoring_rubric: str = Field(min_length=1)
    evidence_citations: list[str] = Field(default_factory=list)


class DeliveryDimensionSnapshot(BaseModel):
    """Lightweight snapshot of delivery quality dimensions for a module eval.

    Contains the 8 delivery quality dimension scores from FR-ERA3-35B.
    """
    pause_quality: float = Field(ge=0.0, le=100.0)
    transition_strength: float = Field(ge=0.0, le=100.0)
    emotional_modulation: float = Field(ge=0.0, le=100.0)
    story_retention: float = Field(ge=0.0, le=100.0)
    humor_landing: float = Field(ge=0.0, le=100.0)
    objection_clarity: float = Field(ge=0.0, le=100.0)
    close_integrity: float = Field(ge=0.0, le=100.0)
    replay_usefulness: float = Field(ge=0.0, le=100.0)


class ModuleEvalCardFace(BaseModel):
    """Face content for a delivery module evaluation card.

    Evaluates a single module practice run with module-specific
    criteria, delivery dimension snapshot, and verdict.
    """
    title: str = Field(min_length=1)
    subtitle: str | None = Field(default=None)
    thumbnail: CardThumbnailAsset = Field(...)
    module_family: DeliveryModuleFamily = Field(...)
    module_score: float = Field(ge=0.0, le=100.0)
    practice_type: PracticeType = Field(...)
    criteria: list[ModuleEvalCriterion] = Field(min_length=2,
        description="At least 2 module-specific evaluation criteria")
    delivery_snapshot: DeliveryDimensionSnapshot = Field(...)
    composite_delivery_score: float = Field(ge=0.0, le=100.0)
    verdict: CardVerdictBlock = Field(...)
    role: EvalCardRole = Field(default=EvalCardRole.module_eval)

    @model_validator(mode="after")
    def validate_module_criteria(self) -> "ModuleEvalCardFace":
        criterion_names = [c.criterion_name for c in self.criteria]
        if len(set(criterion_names)) != len(criterion_names):
            raise ValueError("Module eval criteria must not contain duplicates")
        return self


class DeliveryModuleEvalCard(BaseModel):
    """Eval card for an individual delivery module practice run.

    Evaluates module-specific performance (hook, authority, close, etc.)
    and feeds into the SSS progression system.
    """
    card_id: str = Field(min_length=1)
    coach_id: str = Field(min_length=1)
    content_asset_id: str = Field(min_length=1,
        description="Recording or live-event asset ID for this practice run")
    face: ModuleEvalCardFace = Field(...)
    theme: CardThemeProjection = Field(...)
    generated_at: str = Field(min_length=1)
    contributes_to_sss: bool = Field(default=True,
        description="Whether this module eval feeds into the SSS card update")
```

### 5.7 Badge Progression

```python
class BadgeThreshold(BaseModel):
    """Threshold requirements for earning a badge tier."""
    tier: BadgeTier
    min_sss_score: float = Field(ge=0.0, le=100.0)
    min_modules_mastered: int = Field(ge=0)
    min_practice_sessions: int = Field(ge=0)
    min_live_events: int = Field(ge=0)
    display_color: str = Field(min_length=1,
        description="Hex color for badge display aligned with PRD-05 §5.11")


class EliteSeminarMasterBadgeProgression(BaseModel):
    """Badge tier progression system from Novice to Elite Seminar Master.

    Badge advancement is monotonic — once earned, a tier is permanent.
    Regression is not permitted.
    """
    coach_id: str = Field(min_length=1)
    current_tier: BadgeTier = Field(default=BadgeTier.NOVICE)
    current_level: SSSLevelTitle = Field(default=SSSLevelTitle.BEGINNER)
    earned_tiers: list[BadgeTier] = Field(default_factory=lambda: [BadgeTier.NOVICE])
    thresholds: list[BadgeThreshold] = Field(min_length=6, max_length=6)
    next_tier_requirements: BadgeThreshold | None = Field(default=None)
    progression_history: list[str] = Field(default_factory=list,
        description="ISO 8601 timestamps of tier advancement events")

    @model_validator(mode="after")
    def validate_monotonic_progression(self) -> "EliteSeminarMasterBadgeProgression":
        tier_order = list(BadgeTier)
        current_idx = tier_order.index(self.current_tier)
        for earned in self.earned_tiers:
            earned_idx = tier_order.index(earned)
            if earned_idx > current_idx:
                raise ValueError(
                    f"Badge progression violation: earned tier {earned} "
                    f"is higher than current tier {self.current_tier}"
                )
        return self
```

### 5.8 SSS Update Trigger and Result

```python
class SSSUpdateTrigger(BaseModel):
    """An event that triggers an SSS card update.

    Flow: module_rehearsal → recorded_run → live_event
          → scorecard_computation → badge_evaluation
    """
    trigger_id: str = Field(min_length=1)
    trigger_type: SSSUpdateTriggerType = Field(...)
    coach_id: str = Field(min_length=1)
    module_family: DeliveryModuleFamily | None = Field(default=None,
        description="Which module was practiced (None for scorecard/badge triggers)")
    source_asset_id: str | None = Field(default=None,
        description="Recording or live-event asset ID")
    composite_delivery_score: float | None = Field(default=None, ge=0.0, le=100.0)
    delivery_snapshot: DeliveryDimensionSnapshot | None = Field(default=None)
    triggered_at: str = Field(min_length=1,
        description="ISO 8601 timestamp")


class SSSUpdateResult(BaseModel):
    """Result of processing an SSS update trigger."""
    trigger_id: str = Field(min_length=1)
    coach_id: str = Field(min_length=1)
    previous_sss_score: float = Field(ge=0.0, le=100.0)
    new_sss_score: float = Field(ge=0.0, le=100.0)
    previous_level: SSSLevelTitle
    new_level: SSSLevelTitle
    previous_badge: BadgeTier
    new_badge: BadgeTier
    level_advanced: bool = Field(default=False)
    badge_advanced: bool = Field(default=False)
    modules_updated: list[DeliveryModuleFamily] = Field(default_factory=list)
    processed_at: str = Field(min_length=1,
        description="ISO 8601 timestamp")
```

### 5.9 Canonical Badge Thresholds

```python
# --- Canonical Badge Threshold Table ---

CANONICAL_BADGE_THRESHOLDS = [
    BadgeThreshold(
        tier=BadgeTier.NOVICE,
        min_sss_score=0.0,
        min_modules_mastered=0,
        min_practice_sessions=0,
        min_live_events=0,
        display_color="#8B7355",  # earth/brown
    ),
    BadgeThreshold(
        tier=BadgeTier.BRONZE,
        min_sss_score=25.0,
        min_modules_mastered=3,
        min_practice_sessions=15,
        min_live_events=0,
        display_color="#CD7F32",  # bronze
    ),
    BadgeThreshold(
        tier=BadgeTier.SILVER,
        min_sss_score=40.0,
        min_modules_mastered=6,
        min_practice_sessions=40,
        min_live_events=2,
        display_color="#C0C0C0",  # silver/steel
    ),
    BadgeThreshold(
        tier=BadgeTier.GOLD,
        min_sss_score=60.0,
        min_modules_mastered=10,
        min_practice_sessions=80,
        min_live_events=5,
        display_color="#FFD700",  # gold/warm glow
    ),
    BadgeThreshold(
        tier=BadgeTier.PLATINUM,
        min_sss_score=80.0,
        min_modules_mastered=14,
        min_practice_sessions=150,
        min_live_events=12,
        display_color="#E5E4E2",  # platinum/white-hot
    ),
    BadgeThreshold(
        tier=BadgeTier.PRISMATIC,
        min_sss_score=90.0,
        min_modules_mastered=16,
        min_practice_sessions=250,
        min_live_events=24,
        display_color="#E0B0FF",  # prismatic/holographic
    ),
]


# --- SSS Level Title Resolution ---

def resolve_sss_level(sss_score: float) -> SSSLevelTitle:
    """Resolves the coach-visible level title from the overall SSS score."""
    if sss_score >= 90.0:
        return SSSLevelTitle.ELITE_SEMINAR_MASTER
    elif sss_score >= 75.0:
        return SSSLevelTitle.EXPERT_SPEAKER
    elif sss_score >= 60.0:
        return SSSLevelTitle.ADVANCED_SPEAKER
    elif sss_score >= 45.0:
        return SSSLevelTitle.COMPETENT_SPEAKER
    elif sss_score >= 25.0:
        return SSSLevelTitle.DEVELOPING_SPEAKER
    else:
        return SSSLevelTitle.BEGINNER
```

### 5.10 Supabase DDL (New Tables)

```sql
-- Living Commentary Eval Cards
CREATE TABLE IF NOT EXISTS living_commentary_eval_cards (
    card_id              TEXT PRIMARY KEY,
    content_asset_id     TEXT NOT NULL,
    coach_id             TEXT NOT NULL,
    format_family        TEXT NOT NULL,
    content_type         TEXT NOT NULL,
    overall_lc_score     FLOAT NOT NULL,
    anti_slop_passed     BOOLEAN NOT NULL,
    card_json            JSONB NOT NULL,
    generated_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Seminar Speaking Score Cards
CREATE TABLE IF NOT EXISTS seminar_speaking_score_cards (
    card_id              TEXT PRIMARY KEY,
    coach_id             TEXT NOT NULL UNIQUE,
    overall_sss_score    FLOAT NOT NULL,
    level_title          TEXT NOT NULL,
    badge_tier           TEXT NOT NULL,
    modules_mastered     INT NOT NULL DEFAULT 0,
    card_json            JSONB NOT NULL,
    last_updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Delivery Module Eval Cards
CREATE TABLE IF NOT EXISTS delivery_module_eval_cards (
    card_id              TEXT PRIMARY KEY,
    coach_id             TEXT NOT NULL,
    content_asset_id     TEXT NOT NULL,
    module_family        TEXT NOT NULL,
    module_score         FLOAT NOT NULL,
    practice_type        TEXT NOT NULL,
    contributes_to_sss   BOOLEAN NOT NULL DEFAULT TRUE,
    card_json            JSONB NOT NULL,
    generated_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- SSS Update Triggers (audit trail)
CREATE TABLE IF NOT EXISTS sss_update_triggers (
    trigger_id           TEXT PRIMARY KEY,
    trigger_type         TEXT NOT NULL,
    coach_id             TEXT NOT NULL,
    module_family        TEXT,
    source_asset_id      TEXT,
    composite_score      FLOAT,
    previous_sss_score   FLOAT,
    new_sss_score        FLOAT,
    level_advanced       BOOLEAN NOT NULL DEFAULT FALSE,
    badge_advanced       BOOLEAN NOT NULL DEFAULT FALSE,
    triggered_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

---

## 6. Backward Compatibility and Fallback

### 6.1 v1.0 Eval Cards Unchanged

All v1.0 models, projection services, assembly services, and API endpoints remain active and unchanged. Phase-0 audit cards (`audit_primary`, `before_snapshot`, `after_snapshot`, etc.) continue to use the 7-stat `EvalCardFace` and the existing `EvalCardProjectionService.project_card()` method.

### 6.2 SSS Card Not Yet Populated

If a coach has no SSS card data (no practice sessions, no module scores):

- Create a default `SeminarSpeakingScoreCard` with `overall_sss_score=0`, `level_title=BEGINNER`, `badge_tier=NOVICE`, empty module mastery scores.
- Set `confidence_note = "No practice sessions recorded yet. Begin module practice to start building your Seminar Speaking Score."`.
- Log `sss_card_cold_start` to receipt chain.

### 6.3 Delivery Dimensions Not Available for Module Eval

If delivery dimension data is unavailable during a module practice eval:

- All 8 dimensions in `DeliveryDimensionSnapshot` default to `50.0` (neutral).
- Set `confidence_note` on the verdict block explaining partial data.
- Log `module_eval_delivery_fallback` to receipt chain.

### 6.4 SSSBridgePacket Not Available

If `SSSBridgePacket` from FR-ERA3-35B is not yet implemented:

- The `SSSUpdateProcessor` accepts delivery dimension snapshots directly from module eval cards instead of bridge packets.
- Set `provisional_upstream_contract = true` on the SSS card.
- Log `sss_bridge_fallback` to receipt chain.

### 6.5 Living Commentary Eval Card Without Anti-Slop Data

If anti-slop gate data is not available for a Living Commentary piece:

- Set `anti_slop_passed = True` (assume pass) and `anti_slop_failures = []`.
- Set `confidence_note = "Anti-slop gate data unavailable. Score assumes compliance."`.
- Log `lc_eval_anti_slop_fallback` to receipt chain.

### 6.6 Badge Tier Regression Prevention

If a scoring update would result in a lower badge tier than the current earned tier:

- Reject the regression silently — keep the current tier.
- Log `badge_regression_prevented` with the would-be tier and the retained tier.
- The SSS score itself may fluctuate, but the badge tier only advances.

### 6.7 Unknown Module Family

If an unknown `DeliveryModuleFamily` value is encountered:

- Reject with validation error — no fallback for unrecognized module families.

---

## 7. Tasks

### New Enums and Types

- [ ] Add `DeliveryModuleFamily` enum with 16 values
- [ ] Add `BadgeTier` enum with 6 tiers
- [ ] Add `SSSLevelTitle` enum with 6 level titles
- [ ] Add `SSSUpdateTriggerType` enum with 5 trigger types
- [ ] Add `TrendDirection` enum
- [ ] Add `PracticeType` enum
- [ ] Extend `EvalCardRole` with `lc_eval`, `sss_progression`, `module_eval`
- [ ] Extend `EvalBoardKind` with `sss_progression_detail`, `sss_module_mastery_spread`

### Living Commentary Eval Card

- [ ] Add `LCEvalCriterion` model
- [ ] Add `LCEvalCardFace` model with criteria weight validator
- [ ] Add `LivingCommentaryEvalCard` model

### SSS Card and Badge Progression

- [ ] Add `ModuleMasteryScore` model
- [ ] Add `SSSCardFace` model
- [ ] Add `SeminarSpeakingScoreCard` model
- [ ] Add `BadgeThreshold` model
- [ ] Add `EliteSeminarMasterBadgeProgression` model with monotonic validator
- [ ] Register `CANONICAL_BADGE_THRESHOLDS` constants
- [ ] Implement `resolve_sss_level()` function

### Delivery Module Eval Card

- [ ] Add `ModuleEvalCriterion` model
- [ ] Add `DeliveryDimensionSnapshot` model
- [ ] Add `ModuleEvalCardFace` model with criteria validator
- [ ] Add `DeliveryModuleEvalCard` model

### SSS Update Engine

- [ ] Add `SSSUpdateTrigger` model
- [ ] Add `SSSUpdateResult` model
- [ ] Create `SSSUpdateProcessor` service with `process_trigger()` method

### Projection Services

- [ ] Add `project_lc_eval_card()` to `EvalCardProjectionService`
- [ ] Add `project_sss_card()` to `EvalCardProjectionService`
- [ ] Add `project_module_eval_card()` to `EvalCardProjectionService`

### Assembly Services

- [ ] Add `assemble_sss_progression_board()` to `EvalBoardAssemblyService`
- [ ] Add `assemble_sss_module_mastery_spread()` to `EvalBoardAssemblyService`

### Persistence

- [ ] Create `living_commentary_eval_cards` table
- [ ] Create `seminar_speaking_score_cards` table
- [ ] Create `delivery_module_eval_cards` table
- [ ] Create `sss_update_triggers` table

### Receipt Chain

- [ ] Add receipt entries for `lc_eval_card_projected`, `sss_card_projected`, `module_eval_card_projected`, `sss_update_processed`, `badge_advanced`, `level_advanced`, `sss_card_cold_start`, `badge_regression_prevented`, `lc_eval_anti_slop_fallback`, `module_eval_delivery_fallback`, `sss_bridge_fallback`

### Testing

- [ ] Unit tests for `LCEvalCardFace` criteria weight validation
- [ ] Unit tests for `SSSCardFace` score range and level/badge assignment
- [ ] Unit tests for `EliteSeminarMasterBadgeProgression` monotonic advancement
- [ ] Unit tests for `SSSUpdateTrigger` type validation
- [ ] Integration tests for LC eval card projection chain
- [ ] Integration tests for SSS card projection and update chain
- [ ] Integration tests for SSS progression board assembly
- [ ] Non-regression tests confirming v1.0 Phase-0 audit cards remain unchanged

---

## 8. Acceptance Criteria

### AC-SSS-1 — SSS card displays visible level title and badge tier

**Given** a coach with `overall_sss_score=62`, `modules_mastered_count=10`, `total_practice_sessions=85`, `total_live_events=6`,
**When** the `EvalCardProjectionService.project_sss_card()` projects the SSS card,
**Then** the card face displays `level_title=ADVANCED_SPEAKER`,
**And** the card face displays `badge_tier=GOLD`,
**And** the card face shows `modules_mastered_count=10` out of 16,
**And** the card face shows `strongest_module` and `weakest_module`,
**And** the card face includes a verdict block with interpretive coaching commentary.

**FAILURE EXAMPLE:** The SSS card displays `level_title=ADVANCED_SPEAKER` and `badge_tier=PLATINUM`. Platinum requires `min_sss_score=80` and `min_modules_mastered=14`, but the coach only has score 62 and 10 modules mastered. The system over-awarded the badge by ignoring threshold requirements, creating false progression that destroys trust in the scoring system.

**Constraint:** SSS-Progression-Visibility Rule, Canonical-Evals-Underneath Rule.

### AC-SSS-2 — Badge progression is monotonic (no regression)

**Given** a coach at `badge_tier=GOLD` whose `overall_sss_score` drops from 62 to 55 after a poor live event,
**When** the `SSSUpdateProcessor.process_trigger()` processes the update,
**Then** the `new_sss_score` is updated to 55,
**And** the `new_badge` remains `GOLD` (not regressed to SILVER),
**And** the `badge_advanced` flag is `False`,
**And** a `badge_regression_prevented` receipt is logged.

**FAILURE EXAMPLE:** The system demotes the coach from Gold to Silver because their SSS score dropped below 60. This punishes the coach for practicing and creates fear of attempting difficult live events. The Roadmap §W5A says the coach should "visibly progress toward Elite Seminar Master" — regression contradicts visible progress.

**Constraint:** Badge-Progression-Monotonic Rule.

### AC-SSS-3 — SSS card updates after module rehearsal trigger

**Given** a coach with `overall_sss_score=40` who completes a `HOOK` module rehearsal with `composite_delivery_score=75`,
**When** the `SSSUpdateProcessor.process_trigger()` processes an `SSSUpdateTrigger(trigger_type=MODULE_REHEARSAL, module_family=HOOK)`,
**Then** the `ModuleMasteryScore` for HOOK is updated with the new score,
**And** the `practice_count` for HOOK increments by 1,
**And** the `overall_sss_score` is recomputed from the weighted average of all module scores,
**And** the `SSSUpdateResult` includes `modules_updated=[HOOK]`,
**And** a `sss_update_processed` receipt is logged.

**FAILURE EXAMPLE:** The system updates the overall SSS score but does not update the individual module mastery score for HOOK. This makes the module-family breakdown stale while the aggregate moves, preventing the coach from seeing which specific module they just improved. The SSS card becomes a generic number instead of a diagnostic progression tool.

**Constraint:** SSS-Progression-Visibility Rule.

### AC-SSS-4 — Living Commentary eval card evaluates format-specific criteria

**Given** a Living Commentary Quote piece with `motion_grammar_active=True`, `sonic_doctrine_compliant=True`, `atmospheric_field_present=True`, `composite_delivery_score=72`,
**When** the `EvalCardProjectionService.project_lc_eval_card()` projects the card,
**Then** the card face contains at least 4 format-specific criteria,
**And** at least one criterion is specific to Quote format (e.g., `interpretive_stance_clarity`),
**And** the `anti_slop_passed` flag is `True`,
**And** the `format_family` is `"quote"`,
**And** the card includes a verdict block with coaching commentary.

**FAILURE EXAMPLE:** All 6 Living Commentary format families produce identical eval cards with the same 4 generic criteria ("visual quality", "audio quality", "engagement", "relevance"). A Quote commentary should be evaluated on interpretive stance clarity, while an Atmospheric commentary should be evaluated on emotional field immersion. Generic criteria make format-specific evaluation meaningless.

**Constraint:** Eval-Card-Preserves-Ownership Rule, No-Jargon-On-Card Rule.

### AC-SSS-5 — Delivery module eval card feeds into SSS progression

**Given** a coach with `overall_sss_score=40` who records a CLOSE module practice with `module_score=82` and `practice_type=RECORDED`,
**When** the `DeliveryModuleEvalCard` is projected and the system processes the SSS update trigger,
**Then** the CLOSE module's `ModuleMasteryScore.score` is updated,
**And** the CLOSE module's `practice_count` increments,
**And** if `score >= 70` and `practice_count >= 5`, the module's `mastered` flag is set to `True`,
**And** the `contributes_to_sss` flag on the eval card is `True`,
**And** the SSS card's `overall_sss_score` is recomputed.

**FAILURE EXAMPLE:** The delivery module eval card is projected with `contributes_to_sss=True`, but the SSS card is never updated. The module eval becomes a dead-end presentation artifact that does not feed back into the progression system, breaking the W5A loop: "module practice → record or go live → review → SSS card update → badge progression."

**Constraint:** SSS-Progression-Visibility Rule.

### AC-SSS-6 — SSS progression board displays module mastery breakdown

**Given** a coach with an SSS card containing mastery scores for 16 modules,
**When** the `EvalBoardAssemblyService.assemble_sss_progression_board()` assembles the board,
**Then** the board has `board_kind=sss_progression_detail`,
**And** the board includes the SSS card as the featured card,
**And** the board includes the top 5 most recent module eval cards,
**And** the layout is screenshot-safe with appropriate column count,
**And** the summary line includes the overall SSS score, level title, and badge tier.

**FAILURE EXAMPLE:** The SSS progression board displays only the aggregate SSS score with no module-family breakdown. The coach sees "62/100 — Advanced Speaker" but cannot tell whether their Hook module is at 85 and their Close module is at 35. This makes the progression board a vanity metric display instead of a diagnostic coaching surface.

**Constraint:** SSS-Progression-Visibility Rule, Thumbnail-First Rule.

### AC-SSS-7 — Anti-slop failure is visible on Living Commentary eval card

**Given** a Living Commentary piece that fails the anti-slop gate with `anti_slop_passed=False` and `anti_slop_failures=["motion_grammar_inactive", "atmospheric_field_absent"]`,
**When** the `EvalCardProjectionService.project_lc_eval_card()` projects the card,
**Then** the card face displays `anti_slop_passed=False`,
**And** the `anti_slop_failures` list is populated with the specific failure reasons,
**And** the verdict block explains that the content degrades to "talking head with captions",
**And** the overall LC score is capped or penalized to reflect anti-slop failure.

**FAILURE EXAMPLE:** The Living Commentary eval card shows `overall_lc_score=78` with no indication that the content failed the anti-slop gate. The operator reviews the card, sees a high score, and approves content that is nothing more than a static camera on the coach with subtitle text — exactly the commodity format Living Commentary was designed to replace.

**Constraint:** Anti-Slop visibility, Honest-Partiality Rule.

### AC-SSS-8 — v1.0 Phase-0 audit cards remain unchanged

**Given** the 3 existing v1.0 card roles (`audit_primary`, `before_snapshot`, `after_snapshot`) and 4 board types (`single_card_detail`, `audit_spread`, `before_after_comparison`, `shareable_summary`),
**When** projecting and assembling Phase-0 audit cards using v1.0 methods,
**Then** the `EvalCardFace` still requires exactly 7 visible stats matching `VisibleCardStatKey`,
**And** the `validate_visible_stats_keys` validator still enforces the 7-stat lock,
**And** the `EvalBoardAssemblyService.assemble_board()` still applies before/after ordering law,
**And** no new card roles or board kinds appear in v1.0 resolution paths.

**FAILURE EXAMPLE:** Adding the new `lc_eval` role to the `EvalCardRole` enum causes the existing `EvalCardProjectionService.project_card()` method to accidentally accept LC eval cards and attempt to validate them against the 7-stat `VisibleCardStatKey` lock, crashing with a validation error. The v1.0 path must remain isolated from v2.0 card types.

**Constraint:** Failure-Closed Law, No-New-Score Rule (retained for v1.0 path).

---

## 9. Dependencies

### Internal Services

| Dependency | Type | Use |
|---|---|---|
| `FR-ERA3-35B Content Benchmark Profiles v2.0` | Upstream | Produces `SSSBridgePacket` consumed by SSS card update processor |
| `FR-ERA3-35A Eval Registry` | Upstream | Provides canonical eval taxonomy (retained from v1.0) |
| `FR-ERA3-35 Audit Intelligence Engine` | Upstream | Produces `AuditIntelligenceReport` consumed by Phase-0 card projection (retained) |
| `FR-ERA3-48 Persuasive Speaking Program` | Upstream | Produces module practice events that become `SSSUpdateTrigger` events |
| `FR-ERA3-49A SSS Card And Badge Runtime` | Downstream partner | Runtime engine that operationalizes the SSS progression; this spec defines the card/schema contracts that 49A executes |
| `FR-ERA3-16 Archetype Container Runtime` | Read dependency | `ArchetypeChoice` enum for archetype hint on LC eval cards |
| `FR-ERA3-12 CMF Arc-Governed Rendering` | Read dependency | Motion grammar activation, sonic doctrine compliance, atmospheric field presence status |
| `ReceiptChain` | Existing core | Extended with Living Commentary and SSS-specific receipt entries |

### Internal Models

| Dependency | Type | Use |
|---|---|---|
| `phase0_eval_card_models.py` | Extended | New enums, new card type models, extended `EvalCardRole` and `EvalBoardKind` |
| `benchmark_profile_models.py` | Read-only | `SSSBridgePacket`, `DeliveryQualityDimensions`, `LivingCommentaryFormatFamily` |
| `phase0_audit_models.py` | Read-only | `AuditIntelligenceReport` for v1.0 card projection (retained) |
| Supabase | Existing infra | 4 new tables |

### External

| Library | Version | Purpose |
|---|---|---|
| `pydantic` | v2.x | Typed model definitions with validators |

---

## 10. Testing Strategy

### 10.1 Unit Tests

#### `test_frera35c_v2_lc_eval_card.py`

- `test_lc_eval_face_minimum_4_criteria_passes`
- `test_lc_eval_face_fewer_than_4_criteria_fails`
- `test_lc_eval_face_duplicate_criteria_fails`
- `test_lc_eval_face_criteria_weights_sum_to_one_passes`
- `test_lc_eval_face_criteria_weights_not_summing_fails`
- `test_lc_eval_card_anti_slop_passed_true`
- `test_lc_eval_card_anti_slop_passed_false_with_failures`

#### `test_frera35c_v2_sss_card.py`

- `test_sss_card_face_score_range_validation`
- `test_sss_card_face_level_title_assignment`
- `test_sss_card_face_badge_tier_assignment`
- `test_resolve_sss_level_beginner`
- `test_resolve_sss_level_elite_seminar_master`
- `test_sss_card_cold_start_defaults`
- `test_module_mastery_score_mastered_flag`

#### `test_frera35c_v2_badge_progression.py`

- `test_badge_progression_monotonic_passes`
- `test_badge_progression_regression_fails`
- `test_badge_thresholds_exactly_6`
- `test_canonical_thresholds_ordered_correctly`
- `test_novice_threshold_zero_requirements`
- `test_prismatic_requires_all_16_modules`

#### `test_frera35c_v2_module_eval_card.py`

- `test_module_eval_face_minimum_2_criteria`
- `test_module_eval_face_duplicate_criteria_fails`
- `test_delivery_dimension_snapshot_all_within_range`
- `test_module_eval_contributes_to_sss_default_true`
- `test_all_16_module_families_valid`

#### `test_frera35c_v2_sss_update_trigger.py`

- `test_trigger_module_rehearsal_valid`
- `test_trigger_recorded_run_valid`
- `test_trigger_live_event_valid`
- `test_trigger_scorecard_computation_valid`
- `test_trigger_badge_evaluation_valid`
- `test_update_result_level_advanced_flag`
- `test_update_result_badge_advanced_flag`

### 10.2 Integration Tests

#### `tests/integration/test_frera35c_v2_lc_eval_projection.py`

Scenario class: `TestACSSS4LCEvalCardProjection`

- Project an LC eval card for a Quote Living Commentary piece.
- Assert at least 4 criteria with Quote-specific criterion present.
- Assert `anti_slop_passed` reflects input.
- Assert format_family is correct.
- Assert receipt chain logged `lc_eval_card_projected`.

#### `tests/integration/test_frera35c_v2_sss_progression.py`

Scenario class: `TestACSSS1SSSCardProjection`

- Project SSS card for coach with known scores.
- Assert level title and badge tier match threshold table.
- Assert module mastery breakdown is present.
- Assert strongest/weakest modules are identified.

Scenario class: `TestACSSS2BadgeMonotonicity`

- Create coach at GOLD badge with SSS score that drops.
- Process update trigger.
- Assert badge remains GOLD.
- Assert `badge_regression_prevented` receipt logged.

Scenario class: `TestACSSS3ModuleRehearsalUpdate`

- Process MODULE_REHEARSAL trigger with known score.
- Assert module mastery score updated.
- Assert practice count incremented.
- Assert overall SSS score recomputed.

#### `tests/integration/test_frera35c_v2_sss_board.py`

Scenario class: `TestACSSS6SSSProgressionBoard`

- Assemble SSS progression board with SSS card and 5 module eval cards.
- Assert board_kind is `sss_progression_detail`.
- Assert SSS card is featured.
- Assert layout is screenshot-safe.
- Assert summary includes level title and badge tier.

#### `tests/integration/test_frera35c_v2_nonregression.py`

Scenario class: `TestACSSS8V1NonRegression`

- Project Phase-0 audit card using v1.0 path.
- Assert 7 visible stats with exact `VisibleCardStatKey` values.
- Assert before/after ordering law still works.
- Assert new roles do not leak into v1.0 resolution.

### 10.3 Non-Regression Expectations

- No test may accept a badge tier regression (earned tier must never decrease).
- No test may accept an SSS card without `level_title` and `badge_tier` fields.
- No test may accept a Living Commentary eval card with fewer than 4 criteria.
- No test may accept an LC eval card with criteria weights not summing to 1.0.
- No test may accept a delivery module eval card with a `DeliveryModuleFamily` value not in the 16-member enum.
- No test may accept an SSS update result where `badge_advanced=True` but the badge tier did not actually change.
- No test may allow v1.0 Phase-0 audit cards to be affected by v2.0 card types.
- No test may accept a `SeminarSpeakingScoreCard` without a `BadgeProgression` reference.
- No test may accept identical criteria lists across all 6 Living Commentary format families in LC eval cards.
