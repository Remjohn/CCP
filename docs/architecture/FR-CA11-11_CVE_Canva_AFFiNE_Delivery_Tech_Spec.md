# Tech-Spec: FR-CA11-11 — CVE Canva Clone → AFFiNE Delivery

**Created:** 2026-03-24
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / PRD Update v2.0 — Capability Area 11)
**Architecture Reference:** PRD-Update-CA11 §4.4, Parent PRD FR-VIS-05/FR-VIS-06
**Skill Implementation:** Modification to `conscious-canva-app/api/compositions/approve.ts`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` (FR-VIS-05 Canvas Composition, FR-VIS-06 Notion Visual Content Card)
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd-update-CA11-quad-platform.md`

---

## 2. Overview

### Problem Statement
The Conscious Canva App (FR-VIS-05) currently delivers approved visual compositions to the coach's **Notion** workspace via `notion_sync.py`. With Notion being retired (ADR-05), the visual production output needs to be redirected to AFFiNE. The Canva App's internal mechanics (Fabric.js canvas, VCB intake, RunningHub webhooks, approval controls) remain unchanged — only the delivery target changes.

### Solution
FR-CA11-11 rewires the Conscious Canva App's `POST /api/compositions/approve` endpoint to call `affine_sync.py` instead of `notion_sync.py`. The VPO (Visual Production Output) — individual slide PNGs, horizontal stitch image, ZIP download, metadata (TIAR, AGSS, Receipt Chain, Fingerprint ID), and "Why This Visual Was Built This Way" rationale — is pushed to the coach's AFFiNE Visual Production Console. The Canva App's Approval Controls and internal workflow are completely unmodified.

### Scope
**In scope:**
- Rewiring `POST /api/compositions/approve` to call `affine_sync.py`.
- AFFiNE Visual Production Console database entry format.
- VPO metadata delivery (TIAR audit, AGSS scores, Receipt Chain status).

**Out of scope:**
- Canva App internals (no changes to Fabric.js canvas, VCB intake, template system).
- RunningHub asset reception (webhook unchanged).
- Approval UI controls (unchanged).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| FR-VIS-05 (Canvas Composition) | Conscious Canva App | SOURCE — Generates approved visual compositions. |
| FR-VIS-06 (Notion Visual Content Card) | Notion Delivery | SUPERSEDED — Replaced by AFFiNE delivery. |
| `affine_sync.py` (FR-CA11-02) | AFFiNE Sync Service | TARGET — Receives VPO and pushes to AFFiNE. |
| `DEP-ENG-020` | Fingerprint Archive | METADATA — Linked to each VPO. |

### Technical Decisions
1. **Endpoint Rewire, Not Rebuild:** The Canva App's approval endpoint sends a webhook payload. Currently it targets `notion_sync.py`. The change is a URL swap — now targeting `affine_sync.py`'s `POST /webhook/canva-approve` endpoint. The payload schema is identical; only the consumer changes.
2. **Feature Flag Dual Delivery:** During migration, the `DELIVERY_TARGET` flag (from FR-CA11-02) controls whether VPO goes to Notion, AFFiNE, or both.

---

## 4. Implementation Plan

### Stage 1: Endpoint Rewire
*Agent:* System Operator
*Inputs:* Canva App source code, `affine_sync.py` webhook URL.
*Outputs:* Modified `compositions/approve.ts` endpoint.

**Steps:**
1. In `conscious-canva-app/api/compositions/approve.ts`, change the webhook target from `notion_sync.py` URL to `affine_sync.py` `/webhook/canva-approve` URL.
2. Add `DELIVERY_TARGET` feature flag check — if `BOTH`, fire both webhooks.
3. The VPO payload remains unchanged:
   - Slide PNGs (individual + horizontal stitch)
   - ZIP download URL
   - VPO metadata: `asset_id`, `recipe_name`, `visual_style`, `TIAR_decay_audit`, `AGSS_scores_per_slide`, `authenticity_checks`, `receipt_chain_status`, `fingerprint_id`
   - "Why This Visual Was Built This Way" rationale text
   - Leadership Farming Note

### Stage 2: AFFiNE Visual Production Console Entry
*Agent:* `affine_sync.py` (existing endpoint)
*Inputs:* VPO payload from Canva App.
*Outputs:* Database entry in coach's AFFiNE Visual Production Console.

**Steps:**
1. `affine_sync.py` receives the VPO at `/webhook/canva-approve`.
2. Creates a database entry in the Visual Production Console with all VPO fields.
3. Embeds slide previews as inline images.
4. "Why This Visual Was Built This Way" rendered as a collapsible section.
5. Technical audit (TIAR, AGSS, Receipt Chain) rendered as a collapsed-by-default section.
6. Deep link to Canva App for post-delivery editing.
7. Write Receipt Chain Guard entry per FR47 DEP-ENG-041 after creating the database entry.

---

## 5. Primary Output Schema

**Data Object:** Visual Production Console Database Entry (`DEP-ENG-081` PROPOSED)

```json
{
  "asset_id": "JP-CCF-20260324-001-CAROUSEL",
  "composition_id": "uuid-comp-001",
  "slides": [
    {"slide_number": 1, "png_url": "https://r2.cdn/slide_001.png", "agss_score": 7.8},
    {"slide_number": 2, "png_url": "https://r2.cdn/slide_002.png", "agss_score": 8.1}
  ],
  "horizontal_stitch_url": "https://r2.cdn/stitch_001.png",
  "zip_download_url": "https://r2.cdn/comp_001.zip",
  "recipe_name": "Dopamine Cliff Carousel",
  "visual_style": "cinematic_color_graded",
  "why_this_visual": "Built from Trigger Map activation event: coach's childhood mirror...",
  "leadership_farming_note": "Exercises Deep Empathy (score: 7.4)",
  "tiar_decay_audit": {"inner compass": "in_distribution", "sovereign leader": "tribal_potential"},
  "receipt_chain_status": "CONFIRMED",
  "fingerprint_id": "SKILL-DOP-JP-DISC-PROM-DEV-20260324-001"
}
```

---

## 6. Backward Compatibility Fallback
Dual delivery (Notion + AFFiNE) during migration via `DELIVERY_TARGET` flag. After full migration, the Notion webhook call is removed.

---

## 7. Tasks

- [ ] **Task 1:** Modify `compositions/approve.ts` to target `affine_sync.py` webhook.
- [ ] **Task 2:** Add `DELIVERY_TARGET` feature flag support to the webhook call.
- [ ] **Task 3:** Implement `/webhook/canva-approve` handler in `affine_sync.py`.
- [ ] **Task 4:** Design AFFiNE Visual Production Console database entry layout (previews, collapsible sections, deep links).

---

## 8. Acceptance Criteria

- [ ] **AC1 (Delivery Redirect):** Approve a composition in Canva App. Assert the VPO appears in AFFiNE Visual Production Console (not Notion, when flag = `AFFINE_ONLY`).
- [ ] **AC2 (Dual Delivery):** Set `DELIVERY_TARGET = BOTH`. Approve a composition. Assert VPO appears in both Notion and AFFiNE.
- [ ] **AC3 (Metadata Integrity):** Assert TIAR decay audit, AGSS scores, and Fingerprint ID in AFFiNE match the source VPO payload exactly.
- [ ] **AC4 (Deep Link):** Click "Edit in Canva App" link from AFFiNE entry. Assert it opens the correct composition in the Canva App.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR-VIS-05 (Canva App) | Internal | Source of VPO. |
| FR-CA11-02 (AFFiNE Sync) | Internal | Delivery target. |
| FR-CA11-01 (Coach Workspace) | Internal | Visual Production Console must exist. |

---

## 10. Testing Strategy

### Unit Tests
- **Payload Passthrough:** Assert VPO payload from Canva App matches the AFFiNE entry exactly (field-by-field comparison).

### Integration Tests
- **Full CVE → AFFiNE Pipeline:** Generate a visual composition through the full CVE pipeline (Abel → Paradoxe → RunningHub → Visual Validation → Canva App → Approve) → assert VPO in AFFiNE.
