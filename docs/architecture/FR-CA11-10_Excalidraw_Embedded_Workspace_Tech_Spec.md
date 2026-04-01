# Tech-Spec: FR-CA11-10 — Excalidraw Embedded Workspace (BlockSuite Custom Block)

**Created:** 2026-03-24
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / PRD Update v2.0 — Capability Area 11)
**Architecture Reference:** PRD-Update-CA11 §4.4, ADR-05
**Skill Implementation:** `ccp-blocks/excalidraw-embed/index.ts`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` (FR35 Excalidraw Pipeline, §9.7)
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd-update-CA11-quad-platform.md`

---

## 2. Overview

### Problem Statement
The existing CCP architecture generates `.excalidraw` JSON files (tier lists, mind maps, progress charts, webinar slides) through `Benjamin` (Excalidraw Composer). These files are delivered as static downloads — the coach opens them in a separate Excalidraw app. This creates a fragmented experience: the coach's workspace is in AFFiNE, but visual content lives elsewhere. There's no inline visual interaction.

### Solution
FR-CA11-10 registers an **`excalidraw-embed` custom block** in AFFiNE's BlockSuite framework. This block renders a full Excalidraw canvas inline within any AFFiNE page. Coaches can view and interact with Excalidraw diagrams — tier lists, mind maps, progress charts, webinar slides — directly within their workspace. The block supports read-only mode (for clients viewing delivered assets) and edit mode (for coaches collaborating on visual content). Canvas state is persisted via YJS CRDT sync.

### Scope
**In scope:**
- BlockSuite custom block registration (`excalidraw-embed` type).
- Excalidraw canvas rendering within AFFiNE page.
- Read-only and edit mode support.
- YJS CRDT state persistence.
- API for programmatic canvas injection (used by `affine_sync.py`).

**Out of scope:**
- Excalidraw canvas generation (existing pipeline via `Benjamin`).
- OBS browser source overlay (FR-CA11-14).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| AFFiNE BlockSuite | Custom Block Framework | HOST — The framework that enables custom block types in AFFiNE. |
| `Benjamin` (Excalidraw Composer) | Visual Pipeline | SOURCE — Generates `.excalidraw` JSON that populates the embed block. |
| YJS CRDT Protocol | Collaboration Layer | PERSISTENCE — Canvas state synced and stored via CRDT. |
| `affine_sync.py` (FR-CA11-02) | Sync Service | CONSUMER — Uses the embed block API to programmatically inject visual content. |

### Technical Decisions
1. **Excalidraw React Component in BlockSuite:** AFFiNE uses BlockSuite (a CRDT-native editor framework). Custom blocks are registered as React components within the BlockSuite plugin system. The `excalidraw-embed` block wraps the `@excalidraw/excalidraw` React component with AFFiNE-specific controls (mode toggle, export, fullscreen).
2. **State in CRDT Layer:** The Excalidraw canvas state (JSON) is stored in AFFiNE's YJS document tree — not in a separate database. This means canvas edits are automatically synced via YJS, enabling real-time collaboration if two people open the same page.
3. **Programmatic Injection API:** `affine_sync.py` can inject `.excalidraw` JSON into any AFFiNE page by creating an `excalidraw-embed` block via the AFFiNE API. This is how progress charts (FR-CA11-09), session mind maps (FR-CA11-05), and concept diagrams (FR-CA11-06) are delivered.

---

## 4. Implementation Plan

### Stage 1: BlockSuite Plugin Development
*Agent:* System Operator (TypeScript development in AFFiNE fork)
*Inputs:* BlockSuite plugin API, `@excalidraw/excalidraw` React package.
*Outputs:* Registered `excalidraw-embed` block type in AFFiNE.

**Steps:**
1. Create `ccp-blocks/excalidraw-embed/` directory in the AFFiNE fork.
2. Implement the block component:
   - Render `@excalidraw/excalidraw` React component within BlockSuite block wrapper.
   - Accept initial state from block props (JSON).
   - Sync state changes to YJS document tree on edit events.
   - Read state from YJS document tree on load.
3. Implement mode controls:
   - **Edit Mode:** Full Excalidraw toolbar visible. Drawing, text, shapes enabled. User must have `editor` role on the workspace.
   - **View Mode:** Toolbar hidden. Pan and zoom only. Used for client workspaces and read-only content.
4. Implement toolbar extensions:
   - **Export PNG:** Renders canvas to PNG and triggers browser download.
   - **Fullscreen:** Expands embed to full viewport.
5. Register the block type in BlockSuite's block registry.

### Stage 2: Sync Service Integration
*Agent:* `affine_sync.py` endpoint extension
*Inputs:* `.excalidraw` JSON + target page ID.
*Outputs:* `excalidraw-embed` block created in the target AFFiNE page.

**Steps:**
1. Add `POST /push/excalidraw-embed` endpoint to `affine_sync.py`.
2. Endpoint accepts: `workspace_id`, `page_id`, `excalidraw_json`, `mode` (edit/view), `position` (where in the page to insert the block).
3. Create the block via AFFiNE API with the Excalidraw state payload.
4. Write Receipt Chain Guard entry per FR47 DEP-ENG-041 upon initial block creation (CRDT intermediate edits exclude receipt overhead).

---

## 5. Primary Output Schema

**Data Object:** Excalidraw Embed Block Schema (`DEP-ENG-080` PROPOSED)

**Block Schema (AFFiNE BlockSuite):**

```json
{
  "type": "excalidraw-embed",
  "id": "block-uuid-001",
  "props": {
    "excalidraw_state": {
      "type": "excalidraw",
      "version": 2,
      "elements": [],
      "appState": {},
      "files": {}
    },
    "mode": "view",
    "width": "100%",
    "height": "600px",
    "source_asset_id": "JP-CCF-20260324-001-DIAGRAM"
  }
}
```

---

## 6. Backward Compatibility Fallback
If the `excalidraw-embed` block fails to render (browser incompatibility, JavaScript error), AFFiNE displays a fallback: a static PNG screenshot of the canvas (pre-rendered during injection) with a "Download .excalidraw file" link. The coach can open the file in a standalone Excalidraw app.

---

## 7. Tasks

- [ ] **Task 1:** Set up `ccp-blocks/excalidraw-embed/` plugin structure in AFFiNE fork.
- [ ] **Task 2:** Implement React component wrapping `@excalidraw/excalidraw`.
- [ ] **Task 3:** Implement YJS CRDT state sync for canvas persistence.
- [ ] **Task 4:** Implement edit/view mode toggle with role-based access control.
- [ ] **Task 5:** Register block type in BlockSuite block registry.
- [ ] **Task 6:** Add `POST /push/excalidraw-embed` endpoint to `affine_sync.py`.
- [ ] **Task 7:** Build fallback PNG renderer for incompatible browsers.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Block Registration):** Insert an `excalidraw-embed` block in an AFFiNE page. Assert the Excalidraw canvas renders with the correct initial state.
- [ ] **AC2 (Edit Mode):** Open a block in edit mode. Draw a shape. Reload the page. Assert the shape persists.
- [ ] **AC3 (View Mode):** Open a block in view mode. Assert toolbar is hidden and drawing tools are disabled.
- [ ] **AC4 (CRDT Sync):** Open the same page in two browser tabs (simulating 2 users). Edit in Tab A. Assert the edit appears in Tab B within 2 seconds.
- [ ] **AC5 (Programmatic Injection):** Call `POST /push/excalidraw-embed` with test JSON. Assert the block appears in the target AFFiNE page at the correct position.
- [ ] **AC6 (Fallback):** Disable JavaScript in browser. Assert static PNG fallback is displayed with download link.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| AFFiNE (forked instance) | Infrastructure | Must be deployed with BlockSuite plugin support. |
| `@excalidraw/excalidraw` npm package | External | React component for canvas rendering. |
| YJS | External | CRDT protocol for state sync (already used by AFFiNE). |
| FR-CA11-02 (AFFiNE Sync) | Internal | Programmatic injection API. |

---

## 10. Testing Strategy

### Unit Tests
- **Block Rendering:** Pass known `.excalidraw` JSON. Assert React component renders without errors and displays correct elements.
- **Mode Enforcement:** Set mode=view. Assert toolbar component is not rendered.

### Integration Tests
- **Full Injection Pipeline:** Generate a progress chart via `excalidraw_embed.py` → push via `affine_sync.py` → assert block renders in AFFiNE page.

### Browser Compatibility Tests
- **Chrome, Firefox, Safari:** Assert Excalidraw embed renders correctly in all three browsers.
- **Mobile Viewport:** Assert embed scales correctly on mobile viewport widths.
