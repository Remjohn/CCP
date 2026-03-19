# Tech-Spec: FR-VIS-06 — Notion Visual Content Card

**Created:** 2026-03-18
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §Visual Intelligence Pipeline, CVE_Documentation_V2 §12.2
**Skill Implementation:** `skills/visuals/notion_visual_content_card.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` — FR-VIS-06 definition (line 1026)
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V2.md` — §12.2 Notion Visual Content Card Architecture, VPO record structure
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V3.md` — §9 Updated validation gate data included in technical audit
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Tribal Imageability and Cultural Half-Life.md` — Noun decay reporting in technical audit section
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Carousel Physiological State Architecture Research.md` — Arc type rationale for the "Why This Visual" section
- `d:\Work\The Conscious Coaching Factory\docs\architecture\FR50_Sovereign_Image_Rule_Tech_Spec.md` — Reference template

---

## 2. Overview

### Problem Statement
The visual pipeline produces compositions that are technically sophisticated — engineered with PSSL parameters, validated through 6 quality gates, sourced through a 4-tier hierarchy. But the coach sees none of this. Without a structured delivery mechanism, the coach receives raw PNG files via email or file share, with no context about why specific visual choices were made, no suggested posting schedule, no leadership farming context, and no audit trail. The coach cannot understand or trust the visual strategy because it is opaque, and cannot improve their coaching practice through the visuals because the educational context is missing.

### Solution
FR-VIS-06 defines the complete Visual Production Output (VPO) delivery to the coach's Notion workspace via `notion_visual_content_card.py`. Each approved composition delivers a rich Notion page with 6 sections: Card Header (identification and status), Preview Section (visual assets with download links), Content Ready to Copy (hook text, caption, hashtags, posting schedule), Why This Visual Was Built This Way (plain-language rationale), Leadership Farming Note (leadership trait development), and Technical Audit (collapsed, full pipeline traceability).

### Scope
**In scope:**
- VPO Notion page assembly and delivery via `notion_sync.py` (FR45).
- All 6 VPO card sections with specific content requirements.
- Technical audit section with TIAR decay, AGSS scores, authenticity checks, Receipt Chain status, and Fingerprint ID.
- Integration with FR-VIS-05 (triggered by Approve action).

**Out of scope:**
- The `notion_sync.py` infrastructure itself (maintained by FR45).
- Notion workspace setup and permissions (coach's responsibility).
- Post-delivery analytics (handled by FR42/FR43).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-VIS-005` | Visual Composition Brief Schema | INPUT — VCB provides recipe name, arc type, style, and tribal noun data. |
| `DEP-ENG-039` | Notion Export Pipeline (FR45) | TOOL — The Notion sync infrastructure that creates and updates pages. |
| `DEP-ENG-041` | Receipt Chain Guard | INPUT — Receipt Chain status is reported in the Technical Audit section. |
| `FR-VIS-04` | Visual Validation | INPUT — AGSS scores and authenticity results are reported. |
| `FR-VIS-05` | Canvas Composition & Delivery | UPSTREAM — Approve action triggers VPO delivery. |
| `FR-VIS-02` | TIAR Integration | INPUT — Noun decay audit included in Technical Audit. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Applied |
|---|---|---|---|
| **Tribal Imageability and Cultural Half-Life** | CCP Research Lab | 2026 | The Technical Audit section includes per-noun TIAR decay status so the operator and coach can monitor which tribal nouns are approaching expiration. This longitudinal visibility enables proactive vocabulary refresh — the coach sees "the 5am alarm defeat (TIRS 8.7, active)" alongside "revenue plateau confession (TIRS 6.8, decay approaching)" and can prepare replacement nouns before the quarterly TIAR refresh cycle. Without this visibility, noun decay remains invisible until engagement metrics drop. |
| **Carousel Physiological State Architecture** | CCP Research Lab | 2026 | The "Why This Visual Was Built This Way" section translates the somatic arc type into plain language the coach can understand: "This carousel follows a Tension-Release arc — the first 4 slides build a feeling of frustrated stagnation (using progressively tighter framing and cooler colors), then slide 5 releases the tension with a warm, expansive composition. This arc type produces a 340% higher initial engagement spike than linear information sequences." This educational context helps the coach understand and internalize the visual strategy, building their coaching intuition over time. |

### Technical Decisions
1. **Plain Language Rationale:** The "Why This Visual" section is written by the Content Orchestrator using the VCB's metadata, NOT by the coach. It translates technical decisions into plain-language explanations: "We used Ghibli illustration for this Supervisual because illustrated styles trigger identity play — your audience sees themselves in the character, not as an observer of a photograph." This rationale is not a prompt response — it is assembled from a template library keyed to recipe types and style selections.
2. **Technical Audit Collapsed by Default:** The audit section contains TIAR decay status, AGSS scores, authenticity check results, Receipt Chain status, and Fingerprint ID. This data is valuable for operators and advanced coaches but overwhelming for most users. Collapsing it by default (using Notion's toggle block) ensures the card is clean and readable while maintaining full traceability when expanded.
3. **Universal Asset ID as Card Anchor:** Every VPO card is anchored by a Universal Asset ID (FR46) — a globally unique identifier that links the Notion page to the source content output, VCB, compositions, and Receipt Chain. This enables bidirectional traceability: given a published Instagram post, the coach or operator can trace back to the exact VCB, PSSL parameters, and validation scores that produced it.

---

## 4. Implementation Plan

### Stage 1: VPO Data Assembly
*Agent:* `notion_visual_content_card.py`
*Inputs:* Approved composition from FR-VIS-05, VCB (DEP-VIS-005), validation results (FR-VIS-04), TIAR audit (FR-VIS-02), Receipt Chain status (DEP-ENG-041), content output (DEP-ENG-011).
*Outputs:* `VPO_Data_Package` — structured data for Notion page creation.
*Failure Condition:* Missing upstream data fields; assembler uses `DATA_UNAVAILABLE` placeholder with explicit warning (never silently omits a section).
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Collects all upstream data into a unified `VPO_Data_Package`:
   - From FR-VIS-05: export asset URLs (individual PNGs, horizontal stitch, ZIP), composition ID.
   - From DEP-VIS-005 (VCB): recipe name, arc type, visual style, TIAR nouns, PSSL summaries.
   - From FR-VIS-04: per-slide AGSS scores, authenticity check results, drift scores.
   - From FR-VIS-02: noun decay audit.
   - From DEP-ENG-041: Receipt Chain block IDs, integrity status.
   - From DEP-ENG-011: content output ID, hook text, full caption, hashtag recommendations, posting schedule.
2. Generates the Universal Asset ID (FR46) for this VPO.
3. Generates the plain-language rationale from the template library keyed to the VCB's recipe type and visual style.
4. Identifies the Leadership Farming trait for this visual.

### Stage 2: Notion Page Assembly & Sync
*Agent:* `notion_visual_content_card.py` → `notion_sync.py` (FR45)
*Inputs:* `VPO_Data_Package`.
*Outputs:* Created Notion page in the coach's Visual Content database.
*Failure Condition:* Notion API failure; VPO queued for retry. Never lost.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Notion Page Structure (6 Sections):**

**Section 1 — Card Header:**
- Universal Asset ID (e.g., `JP-VIS-20260318-012`)
- Recipe Name in plain language (e.g., "Dopamine Cliff Carousel — Tension-Release Arc")
- Production Status: `APPROVED` / `MANUALLY_EDITED_APPROVED`
- Date: "March 18, 2026"
- Visual Style: "Cinematic Color Graded"

**Section 2 — Preview:**
- Carousel: horizontal stitch image embedded + individual numbered slide previews + ZIP download link
- Single Image: full-size preview + PNG download link
- All images embedded as Notion media blocks with R2 URLs

**Section 3 — Content Ready to Copy:**
- Hook Text (formatted as quote block for easy copying)
- Full Caption (formatted as collapsible text block)
- Hashtag Recommendations (comma-separated, formatted as code block)
- Posting Day & Time Recommendation (e.g., "Thursday 9:30am — peak engagement window for your tribe")

**Section 4 — Why This Visual Was Built This Way:**
- Arc Type explanation: "This carousel follows a Tension-Release arc..."
- Emotional Arc Mapping: "Slides 1-4 build frustrated stagnation → Slide 5 releases tension with warmth"
- TIAR Noun Selection rationale: "We chose 'the 5am alarm defeat' (TIRS 8.7) because this phrase triggers immediate identity recognition in your audience..."
- Style Choice rationale: "Cinematic color grading was selected because your audience's interaction depth (CBCS 6) is at the trust-authentication stage..."
- Tribal Function: "This visual exercises the 'Observer' leadership trait — you're naming a shared experience without prescribing a solution"

**Section 5 — Leadership Farming Note:**
- Which leadership trait this visual exercises (e.g., "Observer," "Provocateur," "Shepherd")
- How publishing this visual advances the coach's leadership development

**Section 6 — Technical Audit (collapsed toggle block):**
- TIAR Decay Status per noun: table of `noun | TIRS score | decay stage | last measured`
- AGSS Scores per slide: table of `slide | AGSS | lighting | texture | composition | emotion`
- Authenticity Check Results per slide: table of `slide | expression | proportion | skin texture`
- Character Drift Scores (if applicable): table of `slide | drift score | threshold | result`
- Receipt Chain Status: linked block IDs, integrity VALID/INVALID
- Fingerprint ID: cryptographic hash of the complete VPO record
- Asset History: table of any manual swaps performed in the Canva App

---

## 5. Primary Output Schema

### Schema Name: `VPO_Notion_Card.json`

```json
{
  "vpo_id": "VPO-JP-20260318-012",
  "universal_asset_id": "JP-VIS-20260318-012",
  "notion_page_id": "abc-123-def-456",
  "coach_id": "coach_jean_pierre",
  "card_header": {
    "recipe_name": "Dopamine Cliff Carousel — Tension-Release Arc",
    "production_status": "APPROVED",
    "date": "2026-03-18",
    "visual_style": "Cinematic Color Graded"
  },
  "preview_assets": {
    "type": "carousel",
    "horizontal_stitch_url": "https://r2.ccf-assets.com/export/comp-012-stitch.png",
    "slide_previews": [
      { "slide_index": 0, "url": "https://r2.ccf-assets.com/export/comp-012-slide-0.png" },
      { "slide_index": 1, "url": "https://r2.ccf-assets.com/export/comp-012-slide-1.png" }
    ],
    "zip_download_url": "https://r2.ccf-assets.com/export/comp-012-all.zip"
  },
  "content_ready_to_copy": {
    "hook_text": "The 5am alarm goes off. You don't hit snooze — you just lie there, reverse-engineering how many meetings you can cancel before anyone notices.",
    "full_caption": "The Sunday night dread spiral isn't about Monday...",
    "hashtags": "#consciouscoaching, #leadershipdevelopment, #coachlife, #sundayscaries",
    "posting_recommendation": {
      "day": "Thursday",
      "time": "09:30",
      "rationale": "Peak engagement window for your tribe — Thursday morning pre-meeting scroll behavior"
    }
  },
  "why_this_visual": {
    "arc_type_explanation": "This carousel follows a Tension-Release arc — the first 4 slides build frustrated stagnation using progressively tighter framing and cooler colors, then slide 5 releases with warm, expansive composition. This arc type produces a 340% higher initial engagement spike than linear information sequences.",
    "tiar_noun_rationale": "We used 'the 5am alarm defeat' (TIRS 8.7, active) because this phrase triggers immediate identity recognition — your audience has lived this exact moment and the recognition flash drives the initial swipe.",
    "style_rationale": "Cinematic color grading was selected because your audience's CBCS (6) is at the trust-authentication stage — they need visual evidence, not illustration, to deepen their parasocial bond.",
    "tribal_function": "This visual exercises the 'Observer' leadership trait — naming a shared pain without prescribing a premature solution."
  },
  "leadership_farming_note": {
    "trait": "Observer",
    "development_context": "Publishing this visual positions you as someone who notices what others suppress. Your audience will recognize themselves in the observation, building the 'I'm not the only one' resonance that precedes trust."
  },
  "technical_audit": {
    "collapsed": true,
    "tiar_decay_status": [
      { "noun": "the 5am alarm defeat", "tirs_score": 8.7, "decay_stage": "in_distribution", "last_measured": "2026-03-17" },
      { "noun": "Sunday night dread spiral", "tirs_score": 9.1, "decay_stage": "in_distribution", "last_measured": "2026-03-17" },
      { "noun": "revenue plateau confession", "tirs_score": 6.8, "decay_stage": "decay_approaching", "last_measured": "2026-03-17" }
    ],
    "agss_scores": [
      { "slide_index": 0, "composite": 7.8, "lighting": 8.2, "texture": 7.5, "composition": 7.9, "emotion": 7.6 }
    ],
    "authenticity_checks": [
      { "slide_index": 0, "expression": "PASS", "proportion": "PASS", "skin_texture": "PASS" }
    ],
    "receipt_chain_status": "VALID",
    "receipt_chain_blocks": ["RCB-VIS07-20260318-001", "RCB-VIS08-20260318-001", "RCB-VCB-20260318-012", "RCB-VVR-20260318-012-S00"],
    "fingerprint_id": "SHA256:e7a3b9c1d2f4a5b8c3d6e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1",
    "asset_history": []
  },
  "receipt_chain_block": "RCB-VPO-20260318-012",
  "timestamp_utc": "2026-03-18T01:43:00Z"
}
```

---

## 6. Backward Compatibility Fallback

If `notion_sync.py` (FR45) is unavailable or the Notion API fails:
1. The VPO data package is serialized to JSON and stored in Cloudflare R2 at a permanent URL.
2. The operator receives the R2 URL via the System Operator notification channel.
3. The VPO is queued for automatic Notion sync retry with exponential backoff.
4. On successful retry, the Notion page is created with a `DELAYED_SYNC` tag and the original production timestamp (not the sync timestamp).
5. No VPO data is lost — the R2 JSON serves as the permanent source of truth, and the Notion page is a derived delivery view.

---

## 7. Tasks

- [ ] **Task 1:** Write `notion_visual_content_card.py` — the VPO data assembler that collects all upstream data into the structured VPO_Data_Package.
- [ ] **Task 2:** Build the Notion page assembly template — 6 sections with proper Notion block types (heading, quote, toggle, table, media, code).
- [ ] **Task 3:** Implement the plain-language rationale generation from the template library — map recipe types and style selections to pre-written explanation templates.
- [ ] **Task 4:** Implement the Leadership Farming Note generation — map recipe types and content themes to leadership traits.
- [ ] **Task 5:** Build the Technical Audit section as a Notion toggle block (collapsed by default) — embed TIAR decay table, AGSS scores table, authenticity results table, Receipt Chain status, Fingerprint ID.
- [ ] **Task 6:** Integrate with `notion_sync.py` (FR45) for Notion API page creation and media embedding.
- [ ] **Task 7:** Implement the Cloudflare R2 fallback for failed Notion syncs — JSON serialization, permanent URL generation, retry queue.
- [ ] **Task 8:** Integrate with Receipt Chain Guard (DEP-ENG-041) for the final VPO hash.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Complete VPO Card):** Approve a 7-slide carousel composition. Assert the Notion page contains all 6 sections: Card Header with Universal Asset ID, Preview with stitch + numbered slides + ZIP, Content Ready to Copy with hook + caption + hashtags + schedule, Why This Visual rationale, Leadership Farming Note, Technical Audit (collapsed). *Failure Example:* The Notion page is created with only the preview images and no textual content — the coach sees pictures but has no context.
- [ ] **AC2 (Rationale Content):** Assert the "Why This Visual" section contains specific references to the arc type (not generic), the TIAR nouns used (with TIRS scores), the style choice rationale (referencing CBCS score), and the tribal function. *Failure Example:* The rationale says "This visual was created to engage your audience" — generic filler that provides zero coaching value.
- [ ] **AC3 (Technical Audit Collapsed):** Open the Notion page. Assert the Technical Audit section renders as a collapsed toggle. Expand it. Assert TIAR decay table, AGSS scores table, authenticity checks, Receipt Chain status, and Fingerprint ID are all present. *Failure Example:* Technical Audit is expanded by default, overwhelming the coach with AGSS scores before they see the preview.
- [ ] **AC4 (TIAR Decay Visibility):** Assert the Technical Audit's TIAR table contains all nouns used in the composition with their current TIRS scores and decay stages. Assert a `decay_approaching` noun is visually differentiated (bold or colored). *Failure Example:* TIAR data is missing — the coach cannot see which tribal vocabulary is aging.
- [ ] **AC5 (Content Ready to Copy):** Assert the hook text is formatted as a Notion quote block that the coach can copy in one click. Assert hashtags are formatted as a code block (monospace, easy to copy). *Failure Example:* The hook text is embedded inside a paragraph with formatting that breaks on copy-paste.
- [ ] **AC6 (Sync Failure Fallback):** Simulate Notion API failure. Assert the VPO JSON is stored in R2 with a permanent URL. Assert the operator is notified. Restore the API. Assert automatic retry creates the Notion page with `DELAYED_SYNC` tag. *Failure Example:* The VPO data is lost because the sync failure was not caught, and the operator has no way to recover it.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| DEP-VIS-005 (VCB Schema) | Internal | INPUT — recipe, arc type, style, TIAR data. |
| DEP-ENG-039 (Notion Export Pipeline / FR45) | Internal | TOOL — Notion page creation and sync. |
| DEP-ENG-041 (Receipt Chain Guard) | Internal | INPUT — Receipt Chain status. AUDIT — VPO hash. |
| FR-VIS-02 (TIAR Integration) | Internal | INPUT — noun decay audit. |
| FR-VIS-04 (Visual Validation) | Internal | INPUT — AGSS scores, authenticity results. |
| FR-VIS-05 (Canvas Composition) | Internal | UPSTREAM — Approve action triggers delivery. Export assets. |
| FR46 (Universal Asset ID) | Internal | ID — Universal Asset ID anchors the VPO card. |
| Notion API | External | Page creation, block assembly, media embedding. |
| Cloudflare R2 | External | Fallback storage, export asset hosting. |

---

## 10. Testing Strategy

### Unit Tests
- **Rationale Template Matching:** For each recipe type (dopamine cliff, listicle, timeline, comparison, etc.), assert the template library produces a specific, non-generic rationale string containing the recipe name, arc type, and at least one TIAR noun reference.
- **Card Section Completeness:** Provide a complete VPO_Data_Package. Assert all 6 sections are assembled with non-null content. Remove one upstream input at a time and assert `DATA_UNAVAILABLE` placeholder appears (never silent omission).

### Integration Tests
- **Full VPO Delivery:** Approve a composition in the Canva App. Assert the Notion page is created within 30 seconds. Assert all 6 sections are present and correctly populated. Assert the Fingerprint ID matches the SHA-256 hash of the VPO record.
- **Round Trip Traceability:** Given the Universal Asset ID, trace backward through the Notion page's Technical Audit to the Receipt Chain blocks, the VCB, and the original content output. Assert all IDs chain correctly.

### Safety Tests (ADR-01 Quarantine Security)
- **Notion Block Injection:** Inject malicious Notion API block constructs into the VCB's `hook_text`. Assert the page assembler sanitizes all text content before creating Notion blocks — no unexpected block types are created.
- **R2 URL Exposure:** Assert that R2 fallback URLs use signed URLs with time-limited access tokens, not permanent public URLs.
