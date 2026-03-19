# Tech-Spec: FR-VIS-11 — In-App Image Search Panel

**Created:** 2026-03-18
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §Visual Intelligence Pipeline, CVE_Documentation_V3 §6
**Skill Implementation:** Conscious Canva App — `components/ImageSearchPanel.tsx`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` — FR-VIS-11 definition (line 1036)
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V3.md` — §6 In-App Image Search Panel Architecture
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V2.md` — §8 Canva App Architecture, §12.2 Asset History Table
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Visual Style Psychology in Coaching.md` — Manual override validation against style constraints
- `d:\Work\The Conscious Coaching Factory\docs\architecture\FR50_Sovereign_Image_Rule_Tech_Spec.md` — Reference template

---

## 2. Overview

### Problem Statement
Aurore's automated image sourcing (FR-VIS-09) selects the statistically optimal image per slide based on TIRS alignment, PAD congruence, and relevance scoring. However, operators may disagree with specific selections — a stock photo may be technically optimal but contextually inappropriate for reasons the algorithm cannot detect (e.g., the subject resembles a banned character, the setting evokes a competitor's visual brand, the image was recently used by a viral meme in a negative context). Without an in-app search and replacement mechanism, operators would need to exit the Canva App, search externally, download, re-upload, and re-position — breaking the composition workflow and losing zone alignment.

### Solution
FR-VIS-11 integrates an Image Search Panel directly into the Conscious Canva App. The panel provides a unified search interface across all 5 stock APIs (Unsplash, Pexels, Pixabay, GIPHY, SERPER) and triggers RunningHub AI generation (realistic or Ghibli) — all within the composition environment. Results display as a thumbnail grid with one-click or drag-and-drop placement into any open canvas image slot. Every manual swap is logged in the Asset History Table for provenance tracking and audit.

### Scope
**In scope:**
- Image Search Panel UI component within the Conscious Canva App.
- Unified search across 5 stock APIs + RunningHub generation trigger.
- Thumbnail grid display with one-click slot placement.
- Photo Deck access for branded photography swaps.
- Asset History Table logging for provenance tracking.

**Out of scope:**
- API skill implementations (defined by FR-VIS-10).
- Image sourcing hierarchy logic (defined by FR-VIS-09).
- Visual validation of manually selected images (operator assumes validation responsibility for manual overrides).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-041` | Receipt Chain Guard | AUDIT — All manual swaps logged and hashed. |
| `FR-VIS-10` | Multi-API Image Search | BACKEND — The panel calls `multi_api_image_search.py` for all search operations. |
| `FR-VIS-05` | Canvas Composition & Delivery | HOST — The panel is embedded in the Canva App. |
| `FR-VIS-09` | Image Sourcing Hierarchy | REFERENCE — Panel displays Aurore's original selections as the default. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Applied |
|---|---|---|---|
| **Visual Style Psychology in Coaching** | CCP Research Lab | 2026 | Manual overrides must still respect the style directive (FR-VIS-08). If an operator searches for a Ghibli image for a carousel slot, the panel displays a warning: "This format restricts Ghibli/illustrated styles. Results filtered to permitted styles only." The panel enforces style constraints on search results — it does not show prohibited image types for the current format, preventing operators from accidentally overriding pipeline constraints. |

### Technical Decisions
1. **Panel as Extension, Not Separate App:** The Image Search Panel is a sidebar component within the Canva App, not a separate application. This allows direct canvas manipulation — clicking "Place" on a search result immediately populates the target slot without file export/import.
2. **Asset History Logging:** Every manual swap records: `original_image_url`, `replacement_image_url`, `operator_id`, `swap_reason` (optional text field), `swap_timestamp`, `slide_index`. This creates a full audit trail for compliance and quality retrospectives.
3. **Style-Filtered Results:** Search results are pre-filtered by the current composition's style directive. If the composition permits only `cinematic_color_graded` and `semi_realistic_digital`, GIPHY results (animated) and Ghibli-generation options are hidden.

---

## 4. Implementation Plan

### Stage 1: Search Panel UI
*Agent:* `ImageSearchPanel.tsx` (React component)
*Inputs:* Operator search query, current composition's style directive, current slide's image slot.
*Outputs:* Thumbnail grid of search results.
*Failure Condition:* All API calls fail; panel displays "No results. Check API connectivity." with retry button.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**UI Components:**
1. **Search Bar:** Text input with search icon. Auto-dispatches to `multi_api_image_search.py` on Enter or after 500ms debounce.
2. **Source Tabs:** Tabs for "All", "Stock Photos", "GIFs", "AI Generate", "Photo Deck". Filters results by source type.
3. **Thumbnail Grid:** 3-column grid of image thumbnails. Each thumbnail shows: image preview, source API icon (Unsplash/Pexels/Pixabay/GIPHY/SERPER), resolution badge (if below 1080px: red warning badge), licensing icon.
4. **Placement Controls:** Each thumbnail has "Place in Slot" button. Clicking it places the image in the currently selected (highlighted) canvas slot. Alternative: drag-and-drop from thumbnail to slot.
5. **AI Generation Section:** Under the "AI Generate" tab: text prompt input, style selector (filtered by permitted styles), "Generate" button. Triggers SKILL-IMG-007 or SKILL-IMG-008 and displays a "Generating..." spinner until RunningHub completes.
6. **Photo Deck Section:** Displays the coach's Photo Deck (SKILL-IMG-009 results) with mood/format filters.

### Stage 2: Result Filtering & Placement
*Agent:* `ImageSearchPanel.tsx` + `multi_api_image_search.py`
*Inputs:* Raw API results, style directive constraints.
*Outputs:* Filtered, ranked thumbnail display; selected image placed in canvas slot.
*Failure Condition:* Selected image resolution below 1080px; panel displays warning "Low resolution — may appear pixelated at export" but does not block placement (operator override).
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. API results are filtered by the composition's style directive: images from Ghibli generation are hidden for carousel compositions; animated GIFs are hidden for formats that don't support animation.
2. Results with resolution < 1080px shortest edge receive a red warning badge but are not hidden — operator may choose low-res with informed consent.
3. When the operator clicks "Place in Slot" or drags a thumbnail to a slot:
   a. The original image URL for that slot is stored in the `asset_history` table.
   b. The new image is downloaded to Cloudflare R2 and placed in the canvas slot.
   c. The composition's `image_resolution_map` entry for that slide is updated with `source_type: "manual_override"`.

### Stage 3: Asset History Logging
*Agent:* Conscious Canva App backend
*Inputs:* Manual swap event.
*Outputs:* Asset History Table entry.
*Failure Condition:* History write failure; logged to error queue. Swap proceeds — audit logging failure is non-blocking.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Asset History Entry:**
```json
{
  "swap_id": "SWAP-JP-20260318-001",
  "composition_id": "COMP-JP-20260318-012",
  "slide_index": 3,
  "original_image": {
    "url": "https://r2.ccf-assets.com/stock/unsplash-abc123.jpg",
    "source_type": "tier_2_stock",
    "source_api": "unsplash"
  },
  "replacement_image": {
    "url": "https://r2.ccf-assets.com/stock/pexels-def456.jpg",
    "source_type": "manual_override_stock",
    "source_api": "pexels"
  },
  "operator_id": "operator_maria",
  "swap_reason": "Original image too similar to competitor's recent post",
  "swap_timestamp_utc": "2026-03-18T01:42:00Z",
  "receipt_chain_block": "RCB-SWAP-20260318-001"
}
```

---

## 5. Primary Output Schema

### Schema Name: `Image_Search_Panel_State.json`

```json
{
  "panel_session_id": "ISP-JP-20260318-001",
  "composition_id": "COMP-JP-20260318-012",
  "current_search_query": "person at stagnant desk looking frustrated",
  "active_tab": "Stock Photos",
  "style_directive_filter": {
    "permitted_styles": ["cinematic_color_graded", "semi_realistic_digital"],
    "hidden_sources": ["giphy_animated", "runninghub_ghibli"]
  },
  "results_displayed": 12,
  "results_filtered_out": 3,
  "total_swaps_this_session": 1,
  "resolution_warnings_shown": 2
}
```

---

## 6. Backward Compatibility Fallback

If `multi_api_image_search.py` is unavailable:
1. The panel displays "Search functionality temporarily unavailable."
2. The Photo Deck tab remains functional (direct Notion API query, no dependency on the multi-API search tool).
3. Operators can manually upload images via a file picker fallback — uploads are stored in R2 and logged in Asset History with `source_type: "manual_upload"`.

---

## 7. Tasks

- [ ] **Task 1:** Build `ImageSearchPanel.tsx` React component — search bar, source tabs, thumbnail grid, placement controls.
- [ ] **Task 2:** Integrate the search panel with `multi_api_image_search.py` — dispatch search queries via the Canva App's API layer.
- [ ] **Task 3:** Implement style directive filtering — hide results from sources incompatible with the current composition's style constraints.
- [ ] **Task 4:** Implement the one-click "Place in Slot" and drag-and-drop placement interactions — download to R2, populate canvas slot, update resolution map.
- [ ] **Task 5:** Build the AI Generation section — prompt input, style selector, RunningHub trigger, polling spinner, result display.
- [ ] **Task 6:** Implement the Asset History Table — log every manual swap with full provenance data.
- [ ] **Task 7:** Integrate with Receipt Chain Guard (DEP-ENG-041).

---

## 8. Acceptance Criteria

- [ ] **AC1 (Multi-API Search):** Enter "person at desk" in the search panel. Assert results appear from at least 3 different stock APIs in the thumbnail grid. Assert each thumbnail shows the source API icon. *Failure Example:* Only Unsplash results appear because the panel hardcoded a single API.
- [ ] **AC2 (Style Filtering):** Open the panel for a `carousel_dopamine_cliff` composition. Assert the "AI Generate" tab does not offer Ghibli generation options. Assert animated GIF results from GIPHY are hidden. *Failure Example:* The operator generates a Ghibli image and places it in a carousel slot, violating the style directive.
- [ ] **AC3 (One-Click Placement):** Click "Place in Slot" on a Pexels thumbnail for slide 3. Assert the image appears in slide 3's canvas slot immediately. Assert the previous image is stored in Asset History. *Failure Example:* The image is placed in slide 0 (wrong slot) because the panel didn't track which slot was selected.
- [ ] **AC4 (Asset History Logging):** Perform 2 manual swaps on different slides. Assert the Asset History Table contains 2 entries with correct original and replacement URLs, operator ID, and timestamps. *Failure Example:* The history table is empty because logging silently failed.
- [ ] **AC5 (Resolution Warning):** Place a 640×480 image into a slot for a 1080×1350 composition. Assert a yellow warning appears: "Low resolution — may appear pixelated at export." Assert the placement is not blocked. *Failure Example:* No warning appears, and the operator exports a pixelated slide.
- [ ] **AC6 (Photo Deck Access):** Open the "Photo Deck" tab. Assert the coach's branded photos appear with mood and format filter dropdowns. Select a photo and place it. Assert provenance logged as `source_type: "manual_override_photo_deck"`. *Failure Example:* The Photo Deck tab is empty because the Notion query does not match the operator's coach_id.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR-VIS-10 (Multi-API Image Search) | Internal | BACKEND — all search queries route through this tool. |
| FR-VIS-05 (Canvas Composition) | Internal | HOST — panel is embedded in the Canva App. |
| FR-VIS-08 (Style Scoping) | Internal | CONSTRAINT — panel filters results by style directive. |
| DEP-ENG-041 (Receipt Chain Guard) | Internal | AUDIT — all swaps hashed. |
| Cloudflare R2 | External | Asset storage for manually placed images. |
| Notion API | External | Photo Deck queries. |

---

## 10. Testing Strategy

### Unit Tests
- **Style Filtering Logic:** Provide a style directive with `prohibited_styles: ["ghibli_illustration"]`. Assert Ghibli generation options and Ghibli-tagged results are hidden from the panel.
- **History Entry Assembly:** Trigger a swap event. Assert the history entry contains all required fields.

### Integration Tests
- **Full Search-to-Placement:** Search for "mountain landscape sunset", select a result, place it in slide 2, export the carousel. Assert slide 2's exported PNG contains the placed image at correct dimensions.
- **AI Generation Within Panel:** Enter a custom prompt in the AI Generate section. Assert RunningHub task is created, polling completes, and the generated image appears as a result in the panel.

### Safety Tests (ADR-01 Quarantine Security)
- **XSS in Search Query:** Enter `<img src=x onerror=alert(1)>` as the search query. Assert the panel sanitizes the input and displays it as escaped text in results — no JavaScript execution.
- **Unauthorized Photo Deck Access:** Attempt to query another coach's Photo Deck by manipulating the `coach_id` parameter. Assert the API returns 403 and no images from the other coach.
