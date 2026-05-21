# Spec Prompt: FR-ERA3-35 - Audit Intelligence Engine

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-35
SPEC_TITLE:      Audit Intelligence Engine
PHASE:           0 - Trial Phase-0 Commercial Runtime
SOURCE_PRD:      PRD-01, PRD-05, PRD-09
MAPPED_STORIES:  Negative Metrics / Damage Index scoring, proof-of-prescription selling, speaking and reactions prescription logic, continuity upsell diagnosis support
CBAR_MANDATES:   Audit-Sells-By-Diagnosis Rule, Human-First Proof Rule, No-Explanation-First Rule, Damage-Before-Delight Rule, Prescription-With-Proof Rule, Continuity-Bridge Rule
BACKEND_REL:     NEW audit engine - MUST consume existing CCP intelligence, voice, content, and benchmark patterns instead of becoming a detached marketing report generator
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-35_Audit_Intelligence_Engine_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This spec defines the official Audit Intelligence Engine for Phase-0. It is not a shallow report writer. It must diagnose:
> - what is weak
> - what is already strong
> - why the current trajectory compounds damage
> - what the prescription is
> - and show proof of the prescription
>
> The audit engine must emit canonical outputs that can be rendered into:
> - a PDF audit with scoring cards
> - an audit explainer video using scoring cards
> - internal operator review surfaces
> - board-style before/after or multi-card comparisons
>
> The audit must also point naturally toward:
> - speaking improvement
> - native live reactions / live authority
> - accountability / continuity
> - the `$29.99 -> $39.99 -> $99.99` ladder
>
> It must explicitly support multimodal audit targets:
> - single image post + caption
> - multiple images / carousel post + caption
> - reel / short-form video + caption
>
> For video-mode audits, the spec must evaluate whether shot / transition / clip-structure analysis should be integrated using the prior OmniShotCut research note as an architectural reference rather than treating reels as caption-only objects.
>
> This spec is downstream from:
> - `FR-ERA3-35A Eval Registry and Scoring Taxonomy`
> - `FR-ERA3-35B Content Benchmark Profiles and Card Weighting Bundles`
> - `FR-ERA3-35C Eval Card System and Shareable Audit Board`
>
> The audit engine must consume those canonical layers rather than inventing scores, visible labels, or weighting rules locally.

> [!IMPORTANT]
> **MANDATORY PHASE-0 SOURCE SET - READ IN EVERY PHASE-0 SPEC SESSION:**
> - `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`
> - `docs/prd/modules/PRD_05_CBCS_Law28.md`
> - `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md`
> - `lab/CCP APRIL Updates/Fladlien_Sales_Insights.md`
> - `lab/CCP APRIL Updates/05_Core_Experience/Human_First_Brand_Doctrine.md`
> - `lab/CCP APRIL Updates/05_Core_Experience/Conscious_Reactions_Source_of_Truth.md`
> - `lab/ccp_biological_orchestration_model_v_1.md`
> - `lab/phase0_eval_card_scoring_model_v_1.md`
> - `lab/OmniShotCut Holistic Relational Shot Boundary.md`

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-09`, `PRD-05`, `PRD-01`. **PROOF:** Quote the exact lines that establish negative metrics, progress/biometric logic, and human-first positioning.
3. Phase-0 source set: all mandatory docs above. **PROOF:** Quote one concrete structural claim from each file.
4. Existing backend references: read real files related to scoring, benchmarking, reaction or speaking evaluation, and report/artifact generation. **PROOF:** Quote real method signatures.
5. Existing models: read score/report/evaluation model files under `src/ccp/models/`.
6. Existing test patterns: read 2 `tests/integration/` files covering scoring, evaluation, or report patterns.
7. Existing commercial and experience boundaries: confirm how the audit must avoid becoming generic marketing copy or vague “helpful tips.”
8. Video-structure precedent: read the OmniShotCut note and state whether the audit should define a future-ready video segmentation / transition-analysis contract for reels, even if the first implementation uses a lighter-weight fallback.
9. Upstream eval layers: read the completed or target prompt/spec surfaces for `FR-ERA3-35A`, `35B`, and `35C`, and confirm how the audit engine consumes them.

**PRE-WORK LOG - required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 320 LINES

§1 Files Read (>=9) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=3 files) | §3.3 Scores / packets / reports | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=14 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `AuditIntelligenceReport`
  - `DamageIndex`
  - `CompoundingForecast`
  - `StrengthReinforcementBlock`
  - `PrescriptionBlock`
  - `ProofOfPrescriptionBlock`
  - `ContinuityBridgeRecommendation`
  - `AuditTargetDescriptor`
  - `CaptionAuditBlock`
  - `SingleImageAuditBlock`
  - `CarouselAuditBlock`
  - `ReelAuditBlock`
  - `VideoStructureAuditBlock`
  - `PdfAuditPayload`
  - `ExplainerAuditVideoPayload`
- The audit must score for more than generic content quality. It must explicitly account for:
  - authority dilution
  - memorability weakness
  - proof weakness
  - visible humanity weakness
  - genericity / red-ocean blending
  - experiential deficit
  - speaking / live-reaction gap
- The audit must reinforce what is already working if present
- The audit must define modality-specific scoring logic for:
  - image-only visual authority and proof density
  - carousel sequencing, frame-to-frame logic, and caption interaction
  - reel structure, pacing, hook retention, shot / transition coherence, and caption-to-video alignment
- The audit must support both:
  - static PDF audit rendering with scoring cards
  - animated / avatar-led downstream audit video rendering with scoring cards
- The audit must not become a vague “report card” with no clear prescription path

**REJECTION:** generic content-score report | caption-only audit for visual posts | no modality split | no damage model | no reinforcement block | no proof-of-prescription logic | no upgrade bridge | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
