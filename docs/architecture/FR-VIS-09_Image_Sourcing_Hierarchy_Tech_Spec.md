# Tech-Spec: FR-VIS-09 — Image Sourcing Hierarchy

**Created:** 2026-03-18
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §Visual Intelligence Pipeline, CVE_Documentation_V3 §2
**Skill Implementation:** `skills/visuals/aurore_image_sourcing.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` — FR-VIS-09 definition (line 1032)
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V3.md` — §2 Four-Tier Image Sourcing Hierarchy, §3 Aurore Agent Upgrade, SKILL-IMG specifications
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V2.md` — §4 Character Image Resolution, §9 RunningHub Integration
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Visual Style Psychology in Coaching.md` — Realism-authentication link, TII-indexed style selection
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Tribal Imageability and Cultural Half-Life.md` — Noun-visual congruence, TIRS-driven search terms
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Cinematographic Emotional Grammar Framework Research.md` — Environmental imagery requirements for mood state congruence
- `d:\Work\The Conscious Coaching Factory\docs\architecture\FR50_Sovereign_Image_Rule_Tech_Spec.md` — Reference template

---

## 2. Overview

### Problem Statement
Every visual the CCP produces requires imagery — photographs, illustrations, AI-generated characters, or brand assets. Using a single source type for all slides creates a visual monoculture: all-stock looks generic, all-AI looks synthetic, all-photo looks like a corporate brochure. More critically, different slide purposes demand different image types: a named hero figure requires an authentic photograph; a metaphorical concept benefits from curated illustration; a character-driven narrative slide needs AI-generated consistency. Without a deterministic sourcing hierarchy, the pipeline makes ad-hoc sourcing decisions that produce inconsistent visual quality, licensing violations, and identity-incoherent character representations.

### Solution
FR-VIS-09 establishes a strict 4-tier sourcing cascade operated by Aurore (Image Research Planner). For each slide in the VCB, Aurore evaluates the slide's `image_type` (validated by Gate V-00 in FR-VIS-13) and routes to the appropriate tier:

- **Tier 1 (Real Person Photo):** Named real individuals → Photo Deck + Known Persons Registry (DEP-VIS-006) + SERPER.
- **Tier 2 (Real Stock Image):** Environmental, contextual, or abstract imagery → Unsplash, Pexels, Pixabay, GIPHY, SERPER.
- **Tier 3 (Realistic AI Character):** When Tiers 1-2 produce no adequate match → RunningHub semi-realistic workflows with identity-preserving reference images (DEP-VIS-004).
- **Tier 4 (Ghibli AI Illustration):** Exclusively for Conceptual Contrast and Supervisual formats → RunningHub Ghibli LoRA workflows (DEP-VIS-007).

Aurore processes all slides in parallel and outputs an `image_resolution_map` specifying the resolved tier per slide. Only slides that fail stock search proceed to AI generation. The hierarchy is a cascade, not a menu — lower tiers are fallbacks, not alternatives.

### Scope
**In scope:**
- The 4-tier cascade logic and per-slide tier resolution.
- Aurore's parallel slide processing architecture.
- The `image_resolution_map` output schema.
- Fallback cascade: primary API fails → next tier.
- Integration with FR-VIS-12 (Known Persons Registry) for Tier 1 and FR-VIS-10 (Multi-API Search) for Tier 2.

**Out of scope:**
- Individual API skill implementations (covered by FR-VIS-10).
- PSSL prompt compilation for AI generation (covered by FR-VIS-03).
- Visual validation post-generation (covered by FR-VIS-04).
- Sovereign Image Rule (covered by FR50 — coach personal photos are separate from this hierarchy).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-VIS-004` | Brand Character Reference Archive | REFERENCE — Canonical character reference images for Tier 3 identity-preserving AI generation. |
| `DEP-VIS-005` | Visual Composition Brief Schema | INPUT — VCB with per-slide `image_type` assignments. |
| `DEP-VIS-006` | Known Persons Registry | TIER 1 SOURCE — Named person canonical images. |
| `DEP-VIS-007` | Ghibli LoRA Registry | TIER 4 SOURCE — LoRA model paths for Ghibli-style generation. |
| `DEP-ENG-044` | Sovereign Image Router | UPSTREAM CONSTRAINT — Coach personal images bypass this hierarchy entirely. |
| `DEP-ENG-041` | Receipt Chain Guard | AUDIT — Tier resolution per slide is hashed and recorded. |
| `FR-VIS-10` | Multi-API Image Search | TIER 2 TOOL — Provides the unified search interface across 5 stock APIs. |
| `FR-VIS-12` | Known Persons Registry | TIER 1 TOOL — Provides named person resolution and context validation. |
| `FR-VIS-03` | PSSL Prompt Compilation | DOWNSTREAM — Paradoxe compiles prompts only for slides resolved to Tier 3 or Tier 4. |
| `FR-VIS-13` | Image Type Validity Gate | UPSTREAM — Gate V-00 has already validated that each slide's `image_type` is compatible with format/style rules. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Applied |
|---|---|---|---|
| **Visual Style Psychology in Coaching** | CCP Research Lab | 2026 | The realism-authentication link establishes that audiences process photographic images as evidence and illustrated images as narrative. The sourcing hierarchy leverages this: Tier 1-2 (real photos) are deployed for slides that need to authenticate claims (hero figures, environmental contexts, documentary moments). Tier 3-4 (AI) are deployed for slides that need to narrate transformation (character-driven metaphors, symbolic contrasts). Mixing sourcing tiers within a single composition follows a deliberate psychological strategy — the shift from photo to AI signals a shift from "this is real" to "this could be you." |
| **Tribal Imageability and Cultural Half-Life** | CCP Research Lab | 2026 | TIAR nouns in text slides must be paired with visually congruent images. The sourcing hierarchy's search terms are derived from the VCB's `tribal_noun_assignments` — Aurore searches for images that visually represent the tribal noun's concrete referent, not generic category images. A search for "the 5am alarm defeat" produces results for "person reaching for alarm clock in dark bedroom," not "morning routine" or "wake up early." The TIRS score of the noun influences search specificity: higher TIRS → more specific search terms → narrower stock results → higher Tier 3 fallback probability (acceptable tradeoff for visual precision). |
| **Cinematographic Emotional Grammar Framework** | CCP Research Lab | 2026 | Environmental imagery (Tier 2) must match the CEGF mood state specified in the VCB's PSSL parameters. A slide with PAD `{P: -0.2, A: 0.7, D: 0.2}` (tense, alert, low-control) requires environmental imagery with tight framing, high contrast lighting, and desaturated warm tones — not a bright, open landscape. Aurore encodes the PAD vector into search modifiers that filter stock results by color temperature, composition type, and spatial geometry. |

### Technical Decisions
1. **Cascade, Not Menu:** The tiers are a strict cascade — Aurore does not "choose" between stock and AI. It always attempts Tier 1 (if named person) or Tier 2 (if not) first. Only when stock search fails to produce adequate results (relevance score < 0.7, resolution < 1080px on shortest edge, licensing incompatible) does Aurore fall through to Tier 3. Tier 4 is never a fallback — it is only available for explicitly permitted formats (Conceptual Contrast, Supervisual) via the style directive.
2. **Parallel Slide Processing:** Aurore processes all slides concurrently, not sequentially. Each slide's tier resolution is independent — slide 3 may resolve at Tier 2 (stock) while slide 5 resolves at Tier 3 (AI) simultaneously. This maximizes throughput: a 7-slide carousel's image sourcing takes ~15 seconds (one parallel batch of API calls) rather than ~105 seconds (7 sequential batches).
3. **Adequacy Threshold:** A stock image is "adequate" when it scores ≥0.7 on Aurore's relevance assessment (semantic similarity to the VCB slide description + PSSL mood congruence + noun-visual alignment), has resolution ≥1080px on its shortest edge, and has a compatible license (Creative Commons, Editorial, or Licensed Stock). Images below any threshold trigger the Tier 3 cascade.

---

## 4. Implementation Plan

### Stage 1: Per-Slide Tier Routing
*Agent:* Aurore (Image Research Planner)
*Inputs:* VCB (DEP-VIS-005) with per-slide `image_type`, `named_person_reference`, `tribal_noun_assignments`, `pssl` parameters, format envelope (FR-VIS-07), style directive (FR-VIS-08).
*Outputs:* Per-slide `tier_assignment` array — which tier each slide should attempt first.
*Failure Condition:* VCB missing `image_type` on any slide; Aurore rejects with `INCOMPLETE_VCB` (should not occur if Gate V-00 passed).
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Routing Logic:**

| Condition | Initial Tier | Fallback Cascade |
|---|---|---|
| `named_person_reference` is non-null | Tier 1 → Known Persons Registry (FR-VIS-12) | Tier 1 SERPER fallback → PENDING_OPERATOR_REVIEW (never to Tier 3/4) |
| `image_type: tier_2_stock_*` | Tier 2 → Multi-API Search (FR-VIS-10) | Tier 3 (if stock search fails adequacy threshold) |
| `image_type: tier_3_ai_realistic` | Tier 3 → RunningHub semi-realistic | No further fallback — Tier 3 failure triggers PENDING_HUMAN_REVIEW |
| `image_type: tier_4_ai_ghibli` | Tier 4 → RunningHub Ghibli LoRA | No further fallback — Tier 4 failure triggers PENDING_HUMAN_REVIEW |
| `image_type: graphic_vector` | Tier 2 → Stock search with `image_type=vector` filter | Tier 3 with vector-style prompt |
| `image_type: animated_gif` | Tier 2 → GIPHY search | No fallback — GIPHY failure triggers PENDING_HUMAN_REVIEW |

### Stage 2: Parallel Source Resolution
*Agent:* Aurore (Image Research Planner)
*Inputs:* Per-slide `tier_assignment`, search parameters derived from VCB (tribal nouns, PAD vector, slide description).
*Outputs:* Per-slide `source_resolution` — resolved image URL (or PENDING_HUMAN_REVIEW) with provenance metadata.
*Failure Condition:* Individual slide source failure — slide flagged PENDING_HUMAN_REVIEW; remaining slides proceed. Never halt batch for individual slide failure.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Aurore launches parallel resolution tasks for all slides simultaneously.
2. For each slide:
   a. **Tier 1 slides:** Invoke FR-VIS-12's `known_persons_registry_adapter`. If match found: resolve immediately. If no match: invoke SKILL-IMG-006 SERPER fallback. If SERPER fails: flag PENDING_OPERATOR_REVIEW.
   b. **Tier 2 slides:** Invoke FR-VIS-10's `multi_api_image_search` with search parameters derived from the VCB:
      - Primary search terms: tribal nouns from `tribal_noun_assignments` converted to visual descriptors.
      - Mood modifiers: PAD vector translated to color/lighting/composition keywords.
      - Resolution filter: ≥1080px shortest edge.
      - License filter: Creative Commons, Editorial, or Licensed Stock.
      - If results adequacy ≥ 0.7: select top result. If < 0.7: cascade to Tier 3.
   c. **Tier 3 slides:** Queue prompt for Paradoxe (FR-VIS-03) compilation and RunningHub submission.
   d. **Tier 4 slides:** Queue prompt for Paradoxe (FR-VIS-03) with Ghibli LoRA specification and RunningHub submission.
3. Collect all resolved images into the `image_resolution_map`.

### Stage 3: Image Resolution Map Assembly
*Agent:* Aurore (Image Research Planner)
*Inputs:* All per-slide resolution results from Stage 2.
*Outputs:* Complete `image_resolution_map` — per-slide image URLs, sourcing tiers, provenance, and status.
*Failure Condition:* More than 50% of slides flagged PENDING_HUMAN_REVIEW; Aurore escalates the entire composition to operator review.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Aggregate all resolved images into the `image_resolution_map`.
2. For each slide, record: `resolved_tier`, `image_url` (or null if pending), `source_api`, `relevance_score`, `resolution_px`, `licensing_type`, `status`.
3. Count slides by status: `RESOLVED`, `PENDING_AI_GENERATION`, `PENDING_HUMAN_REVIEW`.
4. If more than 50% of slides are `PENDING_HUMAN_REVIEW`: flag the entire composition for operator intervention.
5. Forward `PENDING_AI_GENERATION` slides to Paradoxe (FR-VIS-03) for prompt compilation.
6. Forward `RESOLVED` slides directly to the Conscious Canva App (FR-VIS-05).

---

## 5. Primary Output Schema

### Schema Name: `Image_Resolution_Map.json`

```json
{
  "resolution_map_id": "IRM-JP-20260318-012",
  "vcb_id": "VCB-JP-20260318-012",
  "content_output_id": "CO-JP-20260318-012-CAROUSEL",
  "total_slides": 7,
  "resolution_summary": {
    "tier_1_resolved": 0,
    "tier_2_resolved": 3,
    "tier_3_pending_generation": 3,
    "tier_4_pending_generation": 0,
    "pending_human_review": 1
  },
  "per_slide_resolution": [
    {
      "slide_index": 0,
      "image_type": "tier_3_ai_realistic",
      "resolved_tier": 3,
      "status": "PENDING_AI_GENERATION",
      "image_url": null,
      "source_api": null,
      "search_terms_used": ["person reaching for alarm in dark bedroom", "dimly lit bedroom morning dread"],
      "stock_search_result": { "attempted": true, "best_relevance_score": 0.52, "reason_rejected": "relevance below 0.7 threshold" },
      "ai_generation_queued": true,
      "provenance": { "pssl_mood": { "P": 0.3, "A": 0.7, "D": 0.4 }, "tribal_nouns": ["the 5am alarm defeat"] }
    },
    {
      "slide_index": 1,
      "image_type": "tier_2_stock_contextual",
      "resolved_tier": 2,
      "status": "RESOLVED",
      "image_url": "https://r2.ccf-assets.com/stock/unsplash-abc123.jpg",
      "source_api": "unsplash",
      "relevance_score": 0.84,
      "resolution_px": "2400x3200",
      "licensing_type": "Unsplash License",
      "search_terms_used": ["flat revenue graph stagnant office desk"],
      "stock_search_result": { "attempted": true, "best_relevance_score": 0.84, "reason_accepted": "relevance ≥0.7, resolution ≥1080px, license compatible" },
      "ai_generation_queued": false,
      "provenance": { "pssl_mood": { "P": -0.2, "A": 0.5, "D": 0.2 }, "tribal_nouns": ["revenue plateau confession"] }
    },
    {
      "slide_index": 4,
      "image_type": "tier_3_ai_realistic",
      "resolved_tier": 3,
      "status": "PENDING_AI_GENERATION",
      "image_url": null,
      "source_api": null,
      "search_terms_used": ["person standing at crossroads dramatic lighting"],
      "stock_search_result": { "attempted": true, "best_relevance_score": 0.61, "reason_rejected": "relevance below 0.7 threshold" },
      "ai_generation_queued": true,
      "provenance": { "pssl_mood": { "P": 0.6, "A": 0.4, "D": 0.7 }, "tribal_nouns": ["launch anxiety loop"] }
    }
  ],
  "receipt_chain_block": "RCB-IRM-20260318-012",
  "timestamp_utc": "2026-03-18T01:38:00Z"
}
```

---

## 6. Backward Compatibility Fallback

If the VCB was generated by an older pipeline version that does not include per-slide `image_type` fields:
1. Aurore defaults all slides to Tier 2 (stock search).
2. If stock search fails the adequacy threshold: Aurore cascades to Tier 3 (AI realistic).
3. Named person references are still detected from text content analysis and routed to Tier 1.
4. Tier 4 (Ghibli) is never auto-assigned — it requires an explicit `image_type: tier_4_ai_ghibli` from the VCB.
5. A `LEGACY_SOURCING_DEFAULT` warning is logged in the resolution map.

---

## 7. Tasks

- [ ] **Task 1:** Write `aurore_image_sourcing.py` — the parallel image resolution orchestrator that processes all VCB slides concurrently.
- [ ] **Task 2:** Implement the per-slide tier routing logic — map each `image_type` to its initial tier and fallback cascade path.
- [ ] **Task 3:** Implement the stock search adequacy threshold — relevance scoring (≥0.7), resolution check (≥1080px shortest edge), licensing compatibility check.
- [ ] **Task 4:** Implement the parallel resolution engine — launch concurrent API calls for all slides, collect results, handle per-slide failures without halting the batch.
- [ ] **Task 5:** Build the `image_resolution_map` assembly — aggregate all per-slide results, compute resolution summary, determine batch-level escalation (>50% PENDING_HUMAN_REVIEW → operator intervention).
- [ ] **Task 6:** Implement the Tier 2 → Tier 3 cascade — when stock search fails the adequacy threshold, automatically queue the slide for AI generation via Paradoxe.
- [ ] **Task 7:** Implement the search term derivation engine — translate VCB `tribal_noun_assignments` and PSSL `pad_environmental_grammar` into specific, non-generic search terms.
- [ ] **Task 8:** Integrate with Receipt Chain Guard (DEP-ENG-041) at every stage.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Tier 1 — Named Person Resolution):** Submit a VCB with `named_person_reference: "Brené Brown"` on slide 2. Assert Aurore routes to FR-VIS-12, resolves a canonical photograph, and the `image_resolution_map` shows `resolved_tier: 1` for slide 2. *Failure Example:* Aurore skips the Known Persons Registry and routes directly to SERPER, potentially retrieving an unlicensed image.
- [ ] **AC2 (Tier 2 → Tier 3 Cascade):** Submit a VCB with `image_type: tier_2_stock_contextual` for slide 4. Configure the stock APIs to return results with relevance < 0.7 for this slide. Assert slide 4 cascades to Tier 3 (`PENDING_AI_GENERATION`) while other Tier 2 slides that scored ≥0.7 remain `RESOLVED`. *Failure Example:* Aurore accepts a low-relevance stock image (0.48) because the cascade logic is not implemented, producing a visually incoherent slide.
- [ ] **AC3 (Parallel Processing):** Submit a 7-slide carousel. Assert all 7 slides are processed concurrently — the total resolution time is approximately equal to the slowest single-slide resolution, not the sum of all slides. *Failure Example:* Slides are processed sequentially, taking 7x longer than necessary.
- [ ] **AC4 (Named Person Never Routes to AI):** Submit a VCB with `named_person_reference: "Simon Sinek"` and remove all registry entries and SERPER results. Assert the slide is flagged `PENDING_OPERATOR_REVIEW` — it does NOT cascade to Tier 3 or 4. *Failure Example:* RunningHub generates a semi-realistic AI image of Simon Sinek.
- [ ] **AC5 (Tier 4 Format Restriction):** Submit a VCB for `carousel_dopamine_cliff` with `image_type: tier_4_ai_ghibli` on slide 3 (which should have been caught by Gate V-00). Assert Aurore explicitly verifies the format permits Tier 4 and rejects if not. *Failure Example:* Aurore blindly executes a Ghibli generation for a carousel slide because the image_type was set without Gate V-00 validation.
- [ ] **AC6 (Batch Escalation):** Submit a 6-slide VCB where 4 slides fail all sourcing attempts (stock fails, AI fails). Assert the composition is escalated to operator review because >50% of slides are PENDING_HUMAN_REVIEW. *Failure Example:* The composition is delivered with 4 placeholder slots, producing an unpublishable visual.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| DEP-VIS-004 (Brand Character Reference Archive) | Internal | Tier 3 — reference images for identity-preserving AI generation. |
| DEP-VIS-005 (VCB Schema) | Internal | INPUT — per-slide image types and search parameters. |
| DEP-VIS-006 (Known Persons Registry) | Internal | Tier 1 — named person canonical images. |
| DEP-VIS-007 (Ghibli LoRA Registry) | Internal | Tier 4 — LoRA model paths for Ghibli generation. |
| DEP-ENG-041 (Receipt Chain Guard) | Internal | AUDIT — all tier resolutions are hashed and recorded. |
| DEP-ENG-044 (Sovereign Image Router) | Internal | UPSTREAM — coach personal images bypass this hierarchy. |
| FR-VIS-10 (Multi-API Image Search) | Internal | Tier 2 — unified stock search interface. |
| FR-VIS-12 (Known Persons Registry) | Internal | Tier 1 — named person resolution and context validation. |
| FR-VIS-03 (PSSL Prompt Compilation) | Internal | DOWNSTREAM — Paradoxe compiles prompts for Tier 3/4 slides. |
| FR-VIS-13 (Image Type Validity Gate) | Internal | UPSTREAM — Gate V-00 has validated all image types. |
| Unsplash, Pexels, Pixabay, GIPHY, SERPER APIs | External | Tier 2 stock image sources. |
| RunningHub API | External | Tier 3/4 AI image generation. |

---

## 10. Testing Strategy

### Unit Tests
- **Tier Routing:** For each valid `image_type`, assert the routing logic assigns the correct initial tier and defines the correct fallback cascade.
- **Search Term Derivation:** Provide a VCB slide with `tribal_noun_assignments: ["the 5am alarm defeat"]` and PAD `{P: 0.3, A: 0.7, D: 0.4}`. Assert the derived search terms include "person reaching for alarm clock dark bedroom" and NOT generic terms like "morning" or "wake up."
- **Adequacy Threshold:** Provide stock search results with relevance scores [0.65, 0.71, 0.88]. Assert 0.65 cascades to Tier 3, while 0.71 and 0.88 resolve at Tier 2.

### Integration Tests
- **Full Cascade:** Submit a VCB with 1 Tier 1 slide, 3 Tier 2 slides (1 with inadequate stock results), 2 Tier 3 slides, 1 Tier 4 slide. Assert the resolution map shows correct tier resolution for all 7 slides, with the inadequate Tier 2 slide correctly cascading to Tier 3.
- **Parallel Performance:** Submit a 10-slide VCB and measure total resolution time. Assert it is <20 seconds (parallel) rather than >100 seconds (sequential).

### Safety Tests (ADR-01 Quarantine Security)
- **Search Term Injection:** Inject search terms with embedded API query parameters: `"alarm clock" site:malicious.com`. Assert the search APIs receive sanitized queries without injected parameters.
- **Named Person AI Prohibition:** Force all Tier 1 and SERPER sources to fail for a named person. Assert the pipeline flags PENDING_OPERATOR_REVIEW and does NOT route to RunningHub.
