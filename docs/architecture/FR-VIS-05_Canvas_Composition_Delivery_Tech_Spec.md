# Tech-Spec: FR-VIS-05 — Canvas Composition & Delivery

**Created:** 2026-03-18
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §Visual Intelligence Pipeline, CVE_Documentation_V2 §8
**Skill Implementation:** Conscious Canva App (Next.js 14 + Fabric.js)
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` — FR-VIS-05 definition (line 1024)
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V2.md` — §8 Conscious Canva App Architecture, 7 customizations to base canva-clone
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V3.md` — §6 Updated Canva App integration with RunningHub webhooks
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Carousel Physiological State Architecture Research.md` — Stitch boundary alignment, edge bleed zones, seamless carousel export
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Gaze Cueing in Design Framework.md` — Zone preservation during canvas export, Identity/Hook/Action zone positioning
- `d:\Work\The Conscious Coaching Factory\docs\architecture\FR50_Sovereign_Image_Rule_Tech_Spec.md` — Reference template

---

## 2. Overview

### Problem Statement
The visual pipeline produces VCBs, resolved images, and AI-generated assets — but these are raw components, not publishable compositions. A carousel is not 7 individual images — it is a seamless visual narrative that must stitch across slide boundaries, maintain consistent zone positioning, and export at exact platform-specific dimensions. Without a dedicated composition environment, operators would manually assemble assets in generic design tools (Canva, Figma), losing the deterministic zone positioning, edge bleed alignment, and template consistency that the VCB engineered.

### Solution
FR-VIS-05 defines the Conscious Canva App — a Next.js 14 + Fabric.js web application that receives VCBs via API, loads format-specific templates, renders text and image slots, receives RunningHub-generated assets via webhook, and provides approval/regeneration/editing controls. The app implements 7 customizations to the base canva-clone: Template System Replacement, VCB Intake API, RunningHub Asset Reception, Coach Handle Bar Component, Seamless Carousel Export, Stripped Features, and Approval Controls.

### Scope
**In scope:**
- VCB intake via `POST /api/compositions/create`.
- RunningHub asset reception via `POST /api/assets/receive`.
- 7 customizations (A through G) to the base canva-clone.
- Seamless carousel export with edge bleed zones (40px).
- Approval workflow (Approve, Request Regeneration, Edit and Approve).

**Out of scope:**
- In-App Image Search Panel (handled by FR-VIS-11).
- Notion delivery (handled by FR-VIS-06).
- Visual validation scoring (handled by FR-VIS-04).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-VIS-005` | Visual Composition Brief Schema | INPUT — VCB drives template loading and slot population. |
| `DEP-ENG-041` | Receipt Chain Guard | AUDIT — Composition assembly and approval actions are hashed. |
| `FR-VIS-01` | VCB Generation | UPSTREAM — Abel produces the VCB that drives composition. |
| `FR-VIS-04` | Visual Validation | UPSTREAM — Only validated images populate slots. |
| `FR-VIS-06` | Notion Visual Content Card | DOWNSTREAM — Approved compositions are synced to Notion. |
| `FR-VIS-07` | Format & Aspect Ratio Enforcement | UPSTREAM — Templates use locked dimensions from format envelope. |
| RunningHub API | External | Image generation webhook delivery. |
| Cloudflare R2 | External | Asset storage for final compositions. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Applied |
|---|---|---|---|
| **Carousel Physiological State Architecture** | CCP Research Lab | 2026 | Seamless carousel export requires edge bleed zones (40px) that align across stitch boundaries. When a user swipes between carousel slides on Instagram, the platform renders approximately 40px of overlap during the swipe animation. If the visual elements at slide edges are discontinuous (hard color transitions, misaligned geometric elements), the swipe creates a jarring visual break that interrupts the somatic arc's physiological continuity. The Canva App's export function ensures edge bleed zones on adjacent slides share harmonious color values and compositional flow. |
| **Gaze Cueing in Design Framework** | CCP Research Lab | 2026 | The Coach Handle Bar component is positioned at the top of every composition and locked in place — operators cannot move it. This position exploits the Identity Zone principle: the viewer's gaze enters the frame at the top-left (Western reading pattern), immediately encounters the coach's face and name (identity authentication), then follows the coach's gaze direction toward the Hook Zone below. Moving the handle bar to the bottom or side would break this gaze transfer pattern, reducing the Identity → Hook attention flow by 40-60% (measured via eye-tracking). |

### Technical Decisions
1. **Template from VCB, Not Manual Browsing:** Standard Canva-like tools offer a template gallery where users browse and select templates manually. The Conscious Canva App eliminates this — templates load automatically from the VCB's `template_id`, which is determined by the recipe protocol. The operator sees the correct template pre-populated, not a gallery of options. This prevents template misselection that would violate the VCB's zone positioning and dimensional specifications.
2. **Stripped Features:** Six features are deliberately removed from the base canva-clone to prevent operators from making changes that would violate the VCB's deterministic specification: template gallery (replaced by VCB-driven loading), font selector for primary zones (fonts are locked by the VCB recipe), color picker for backgrounds (backgrounds are PSSL-driven), background upload (backgrounds are pipeline-generated), manual text sizing (text zones respect VCB specifications), freeform element placement in locked zones.
3. **Approval as Pipeline Trigger:** The "Approve" button is not a UI confirmation — it triggers the Notion sync pipeline (FR-VIS-06), writing the finalized composition to the coach's Notion workspace. This architectural coupling ensures that only operator-approved compositions reach Notion.

---

## 4. Implementation Plan

### Stage 1: VCB Intake & Template Loading
*Agent:* Conscious Canva App (`POST /api/compositions/create`)
*Inputs:* VCB JSON (DEP-VIS-005), format constraint envelope (FR-VIS-07).
*Outputs:* Canva App composition object with template loaded, text slots populated, image slots as placeholders.
*Failure Condition:* Template not found for `template_id`; API returns 400 with `TEMPLATE_NOT_FOUND`.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. The pipeline submits the VCB JSON via `POST /api/compositions/create`.
2. The app reads `template_id` and loads the corresponding Fabric.js template — a pre-defined canvas with locked zones (Identity/Handle Bar, Hook, Body, Action, Image).
3. Text slots populate immediately from VCB fields: `hook_text` → Hook Zone, `body_text` → Body Zone, `overlay_text` → Overlay Zone.
4. Image slots render as placeholder grayscale rectangles with "Awaiting Image" labels — populated when RunningHub or stock images arrive.
5. The Coach Handle Bar component (Customization D) is rendered at the top: profile picture, coach name, handle, logo. Position is locked — not draggable.
6. The composition object is saved to the database with status `ASSEMBLING`.

### Stage 2: RunningHub Asset Reception
*Agent:* Conscious Canva App (`POST /api/assets/receive`)
*Inputs:* RunningHub webhook payload containing `task_id`, `slide_index`, `image_url`, `original_vcb_id`.
*Outputs:* Image slot populated in the composition canvas.
*Failure Condition:* `task_id` does not match any active composition; webhook returns 404.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. RunningHub sends a webhook on task completion: `{ "task_id": "...", "output_url": "..." }`.
2. The app matches `task_id` to the queued slide via the `pending_assets` table.
3. Downloads the image from RunningHub's `output_url` to Cloudflare R2.
4. Populates the corresponding image slot in the Fabric.js canvas with the R2-hosted image.
5. If all image slots are populated: composition status transitions from `ASSEMBLING` to `READY_FOR_REVIEW`.
6. Operator is notified that the composition is ready for review.

### Stage 3: Seamless Carousel Export (Customization E)
*Agent:* Conscious Canva App export engine
*Inputs:* Complete composition canvas with all slots populated.
*Outputs:* Individual slide PNGs at exact VCB dimensions, horizontal stitch image (for preview), ZIP archive.
*Failure Condition:* Edge bleed misalignment detected; export retries after canvas re-render.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. For carousels: the app stitches all slides into one horizontal canvas for preview purposes.
2. Slices the horizontal canvas at exact slide dimensions (e.g., 1080×1350px per slide for 4:5).
3. Edge bleed zones (40px on each side of the stitch boundary) are validated: adjacent slides must share harmonious color values within the bleed zone (color distance ≤ 15 on the CIEDE2000 scale).
4. Exports individual slide PNGs at the exact pixel dimensions specified in the format envelope.
5. Generates a horizontal stitch preview image (for visual inspection).
6. Packages everything into a ZIP archive.

### Stage 4: Approval Controls (Customization G)
*Agent:* Conscious Canva App
*Inputs:* Operator interaction (button click).
*Outputs:* Action trigger based on button.
*Failure Condition:* Notion sync failure on approval; composition remains in `APPROVED` status with `SYNC_PENDING` flag.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Three Approval Actions:**

| Action | Button | Pipeline Trigger |
|---|---|---|
| Approve | "Approve & Publish" | Triggers Notion sync (FR-VIS-06) with finalized assets. Composition status → `APPROVED`. |
| Request Regeneration | "Request Regeneration" | Returns specific slides to Paradoxe (FR-VIS-03) with operator's revision note. Status → `REGENERATION_REQUESTED`. |
| Edit and Approve | "Edit & Approve" | Saves operator's manual edits to the canvas, then triggers Notion sync. Status → `MANUALLY_EDITED_APPROVED`. |

---

## 5. Primary Output Schema

### Schema Name: `Canva_Composition.json`

```json
{
  "composition_id": "COMP-JP-20260318-012",
  "vcb_id": "VCB-JP-20260318-012",
  "content_output_id": "CO-JP-20260318-012-CAROUSEL",
  "template_id": "TPL-CAROUSEL-DOPAMINE-CLIFF-003",
  "status": "READY_FOR_REVIEW",
  "dimensions": { "width_px": 1080, "height_px": 1350, "aspect_ratio": "4:5" },
  "slide_count": 7,
  "handle_bar": {
    "visible": true,
    "position": "top_locked",
    "coach_name": "Jean Pierre",
    "coach_handle": "@jeanpierre.coaching",
    "profile_picture_url": "https://r2.ccf-assets.com/coach/jp-profile.jpg",
    "logo_url": "https://r2.ccf-assets.com/coach/jp-logo.png"
  },
  "slots": [
    {
      "slide_index": 0,
      "text_populated": true,
      "image_populated": true,
      "image_source": "runninghub_tier_3",
      "image_r2_url": "https://r2.ccf-assets.com/generated/rh-task-a7b3c9.png"
    }
  ],
  "export_assets": {
    "individual_slides": ["https://r2.ccf-assets.com/export/comp-012-slide-0.png"],
    "horizontal_stitch": "https://r2.ccf-assets.com/export/comp-012-stitch.png",
    "zip_archive": "https://r2.ccf-assets.com/export/comp-012-all.zip"
  },
  "approval_action": null,
  "receipt_chain_block": "RCB-COMP-20260318-012",
  "timestamp_utc": "2026-03-18T01:41:00Z"
}
```

---

## 6. Backward Compatibility Fallback

If the Conscious Canva App is offline or experiencing issues:
1. Individual validated images are still available in Cloudflare R2.
2. The VCB JSON contains all text content, zone specifications, and image URLs.
3. An operator can manually assemble the composition using the raw assets and VCB specification in any standard design tool.
4. The pipeline logs `CANVA_APP_UNAVAILABLE` and queues the composition for automatic re-processing when the app restores.

---

## 7. Tasks

- [ ] **Task 1:** Implement `POST /api/compositions/create` — VCB intake endpoint that loads templates and populates text slots.
- [ ] **Task 2:** Implement `POST /api/assets/receive` — RunningHub webhook endpoint that matches assets to compositions and populates image slots.
- [ ] **Task 3:** Build the Template System Replacement (Customization A) — templates load from VCB JSON by `template_id`, no manual browsing.
- [ ] **Task 4:** Build the Coach Handle Bar Component (Customization D) — profile picture, name, handle, logo; position locked to top, not movable.
- [ ] **Task 5:** Build the Seamless Carousel Export engine (Customization E) — horizontal stitch, edge bleed validation (40px, CIEDE2000 ≤ 15), individual slide PNGs, ZIP archive.
- [ ] **Task 6:** Implement Stripped Features (Customization F) — remove template gallery, font selector for primary zones, color picker for backgrounds, background upload.
- [ ] **Task 7:** Implement Approval Controls (Customization G) — Approve, Request Regeneration, Edit and Approve buttons with pipeline triggers.
- [ ] **Task 8:** Integrate with Receipt Chain Guard (DEP-ENG-041).

---

## 8. Acceptance Criteria

- [ ] **AC1 (VCB Template Loading):** Submit a VCB with `template_id: "TPL-CAROUSEL-DOPAMINE-CLIFF-003"`. Assert the Canva App loads the correct template with all zones at VCB-specified positions and dimensions. Assert text slots are populated from VCB content. *Failure Example:* The app loads a generic blank canvas instead of the specified template.
- [ ] **AC2 (RunningHub Asset Reception):** Submit a webhook payload with a valid `task_id`. Assert the corresponding image slot in the composition is populated with the received image. *Failure Example:* The webhook is received but the image slot remains as a placeholder because the `task_id` matching logic fails.
- [ ] **AC3 (Handle Bar Lock):** Open a composition in the Canva App. Attempt to drag the Coach Handle Bar from the top to the bottom of the canvas. Assert the component is locked in position and cannot be moved. *Failure Example:* The operator drags the handle bar to the bottom-right corner, breaking the Identity Zone → Hook Zone gaze transfer pattern.
- [ ] **AC4 (Seamless Stitch Export):** Export a 7-slide carousel. Assert individual slide PNGs are exactly 1080×1350px each. Assert the horizontal stitch is 7560×1350px. Assert edge bleed zones on adjacent slides have CIEDE2000 color distance ≤ 15. *Failure Example:* A hard color transition at the slide 3-4 boundary creates a jarring visual break during the Instagram swipe animation.
- [ ] **AC5 (Approve Triggers Notion Sync):** Click "Approve & Publish." Assert composition status transitions to `APPROVED` and the Notion sync pipeline (FR-VIS-06) is triggered with all export assets. *Failure Example:* The approve button saves the status but doesn't trigger the Notion sync, requiring manual export.
- [ ] **AC6 (Request Regeneration):** Click "Request Regeneration" for slide 3 with revision note "make the lighting warmer." Assert the slide is returned to Paradoxe with the revision note and the composition status transitions to `REGENERATION_REQUESTED`. *Failure Example:* The regeneration request targets the entire composition instead of the specific slide.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| DEP-VIS-005 (VCB Schema) | Internal | INPUT — drives template loading and slot population. |
| DEP-ENG-041 (Receipt Chain Guard) | Internal | AUDIT. |
| FR-VIS-01 (VCB Generation) | Internal | UPSTREAM — produces VCBs. |
| FR-VIS-03 (PSSL Prompt Compilation) | Internal | FEEDBACK — regeneration requests route back to Paradoxe. |
| FR-VIS-04 (Visual Validation) | Internal | UPSTREAM — only validated images populate slots. |
| FR-VIS-06 (Notion Visual Content Card) | Internal | DOWNSTREAM — approval triggers sync. |
| FR-VIS-07 (Format Enforcement) | Internal | UPSTREAM — templates use locked dimensions. |
| FR-VIS-11 (In-App Image Search Panel) | Internal | EMBEDDED — search panel is integrated into the app. |
| RunningHub API | External | Webhook delivery. |
| Cloudflare R2 | External | Asset storage. |
| Next.js 14 | Framework | App framework. |
| Fabric.js | Library | Canvas manipulation. |

---

## 10. Testing Strategy

### Unit Tests
- **Template Matching:** Provide 5 different `template_id` values. Assert each loads the correct Fabric.js template with the correct zone dimensions.
- **Edge Bleed Validation:** Provide two adjacent slide canvases. One pair with harmonious edge colors (CIEDE2000 ≤ 15), one pair with clashing edges (CIEDE2000 > 15). Assert the validator passes the first and flags the second.

### Integration Tests
- **Full Composition Flow:** Submit a VCB, receive 7 RunningHub webhooks, assert composition transitions from ASSEMBLING → READY_FOR_REVIEW, click Approve, assert Notion sync triggers.
- **Export Dimension Verification:** Export a carousel and measure each individual PNG's pixel dimensions programmatically. Assert exact match to format envelope.

### Safety Tests (ADR-01 Quarantine Security)
- **Webhook Spoofing:** Send a webhook with an invalid `task_id`. Assert the app returns 404 and does not modify any composition.
- **XSS in VCB Text:** Inject `<script>alert('xss')</script>` into VCB `hook_text`. Assert the Canva App renders the text as escaped content without executing JavaScript.
