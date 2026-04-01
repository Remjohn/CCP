# Tech-Spec: FR-CA11-14 — Excalidraw Live OBS Annotation Overlay

> ⚠️ **RETIRED — 2026-03-25**
> This spec has been absorbed into **FR-CA11-16 (CCP Studio Block — Full Stack Recording & Streaming)**. The Excalidraw annotation overlay is now a native feature of the Studio Block's **Asset Panel** — coaches click visual assets (including Excalidraw canvases) to display them on the recording canvas, eliminating the need for OBS scene switching. ADR-06 (OBS WebSocket) is retired per **ADR-07 (Native CCP Studio Block)**.
>
> **Replacement Spec:** `FR-CA11-16_CCP_Studio_Block_Tech_Spec.md` (Asset Panel, §4 Stage 4)
> **Decision Record:** MCDA IV (CCP Studio Integration Analysis)

**Created:** 2026-03-24
**Status:** ~~Ready for Development~~ **RETIRED**
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / PRD Update v2.0 — Capability Area 11)
**Architecture Reference:** ~~PRD-Update-CA11 §4.5~~ → Absorbed into FR-CA11-16
**Skill Implementation:** ~~Extension to `tools/obs_controller.py`~~ → **DEPRECATED** (functionality in `ccp-blocks/studio-block/`)
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` (FR35 Excalidraw Pipeline, §9.7)
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd-update-CA11-quad-platform.md`

---

## 2. Overview

### Problem Statement
Coaches creating tier lists, reaction explainers, or educational content need to annotate visually during recording — drawing circles around key points, sketching diagrams, writing notes. Currently, this requires post-production editing (adding overlays after recording), which takes 30-60 minutes per video and requires video editing skills most coaches don't have.

### Solution
FR-CA11-14 injects an Excalidraw canvas as an **OBS browser source**, enabling coaches to draw live annotations during recorded or streamed sessions. The `obs_controller.py` `set_browser_source()` method points an OBS browser source to a locally-hosted Excalidraw instance. The coach draws on their tablet or phone; OBS captures it as a transparent overlay on top of the video feed. This enables single-take production of annotated content — no post-production editing required.

### Scope
**In scope:**
- Excalidraw local server setup for OBS browser source.
- OBS browser source injection via `obs_controller.py`.
- Transparent background configuration for overlay rendering.
- Telegram command for overlay activation (`/overlay [on/off]`).

**Out of scope:**
- Excalidraw canvas content generation (manual drawing by coach).
- Embedded Excalidraw in AFFiNE pages (FR-CA11-10 — different use case).
- Session recording (FR-CA11-13 — handles the recording itself).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| FR-CA11-13 (OBS Controller) | Recording Pipeline | HOST — Overlay is injected into OBS via the controller. |
| `@excalidraw/excalidraw` | Excalidraw React App | TOOL — The drawing surface served as a local web page. |
| OBS Browser Source | OBS Feature | HOST — Renders the web page as a video layer. |

### Technical Decisions
1. **Local HTTP Server:** A lightweight HTTP server (Express.js or Python's `http.server`) serves the Excalidraw React app at `http://localhost:9876/overlay`. This URL is injected into an OBS browser source. The server runs on the coach's machine alongside OBS.
2. **Transparent Background:** The HTML page has `background: transparent` and OBS browser source is configured with `custom_css: body { background-color: rgba(0,0,0,0); }`. This makes the canvas render as a transparent overlay — only drawn elements (lines, shapes, text) are visible on top of the video feed.
3. **Tablet Input Support:** The Excalidraw instance is configured for touch/stylus input. Coaches can use an iPad or drawing tablet connected to their computer. The canvas also supports mouse input for desktop users.

---

## 4. Implementation Plan

### Stage 1: Excalidraw Overlay Server
*Agent:* System Operator
*Inputs:* `@excalidraw/excalidraw` React package.
*Outputs:* Local HTTP server serving Excalidraw at `localhost:9876/overlay`.

**Steps:**
1. Create a minimal React app wrapping `@excalidraw/excalidraw` component.
2. Configure Excalidraw with:
   - `viewBackgroundColor: "transparent"` — transparent canvas background.
   - `theme: "dark"` — dark mode for contrast against video.
   - Default tools: freehand draw, arrow, rectangle, text (minimal toolbar).
   - Coach's brand colors pre-loaded in color palette.
3. Build the app as a static bundle.
4. Serve via lightweight HTTP server (Node.js or Python).
5. Include in Dockploy deployment or as a local install on coach's machine.

### Stage 2: OBS Browser Source Injection
*Agent:* `obs_controller.py`
*Inputs:* Overlay activation command.
*Outputs:* OBS browser source configured with Excalidraw overlay URL.

**Steps:**
1. Extend `obs_controller.py` with `activate_overlay()` and `deactivate_overlay()` methods.
2. `activate_overlay()`:
   - Call `set_browser_source("CCP_Overlay", "http://localhost:9876/overlay")`.
   - Set browser source dimensions to match recording resolution.
   - Set `custom_css` for transparent background.
   - Move browser source to top layer (above all other sources).
3. `deactivate_overlay()`:
   - Set browser source to blank page or hide the source.

### Stage 3: Telegram Command
*Agent:* CBCS Bot Handler
*Inputs:* Coach Telegram commands.
*Outputs:* Overlay activation/deactivation in OBS.

**Steps:**
1. Register `/overlay on` and `/overlay off` Telegram commands.
2. `/overlay on` → calls `activate_overlay()`. Responds with "Excalidraw overlay activated 🎨".
3. `/overlay off` → calls `deactivate_overlay()`. Responds with "Overlay deactivated".

---

## 5. Primary Output Schema

**Data Object:** OBS Overlay Status Payload (`DEP-ENG-084` PROPOSED)

```json
{
  "overlay_status": "active",
  "excalidraw_url": "http://localhost:9876/overlay",
  "obs_source_name": "CCP_Overlay",
  "resolution": "1920x1080",
  "background": "transparent",
  "theme": "dark",
  "brand_colors": ["#2E86AB", "#F18F01", "#FFFFFF"]
}
```

---

## 6. Backward Compatibility Fallback
If the Excalidraw overlay server is not running, the `/overlay on` command fails gracefully — OBS is not affected, the recording continues, and the coach is notified via Telegram: "Overlay server not running. Recording continues without overlay." The overlay feature is entirely optional and has no impact on any other CA11 functionality.

---

## 7. Tasks

- [ ] **Task 1:** Build minimal Excalidraw overlay React app with transparent background.
- [ ] **Task 2:** Configure for touch/stylus input (iPad, drawing tablet).
- [ ] **Task 3:** Set up lightweight HTTP server to serve the app at `localhost:9876/overlay`.
- [ ] **Task 4:** Extend `obs_controller.py` with `activate_overlay()` and `deactivate_overlay()` methods.
- [ ] **Task 5:** Add `/overlay on` and `/overlay off` Telegram bot commands.
- [ ] **Task 6:** Write coach setup guide (install overlay app, configure OBS browser source, connect tablet).

---

## 8. Acceptance Criteria

- [ ] **AC1 (Overlay Activation):** Send `/overlay on`. Assert OBS shows a transparent Excalidraw canvas layer over the video feed.
- [ ] **AC2 (Drawing Visibility):** Draw on the Excalidraw canvas. Assert drawn elements appear in the OBS preview/recording as overlays.
- [ ] **AC3 (Transparency):** Assert only drawn elements are visible — the canvas background is fully transparent (no white/black rectangle).
- [ ] **AC4 (Deactivation):** Send `/overlay off`. Assert the overlay disappears from OBS.
- [ ] **AC5 (Recording Integration):** Activate overlay → draw → stop recording (FR-CA11-13). Assert the annotations are present in the recorded video file.
- [ ] **AC6 (Graceful Failure):** Stop the overlay server. Send `/overlay on`. Assert Telegram error message and recording is unaffected.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR-CA11-13 (OBS Controller) | Internal | Uses `set_browser_source()` method. |
| `@excalidraw/excalidraw` npm package | External | Drawing surface. |
| OBS Studio v28+ | External | Must support browser sources. |
| Coach's local machine | Infrastructure | Overlay server runs locally. |

---

## 10. Testing Strategy

### Unit Tests
- **Overlay Server Health:** Start server. Assert `GET http://localhost:9876/overlay` returns 200 with correct HTML.
- **Transparent Background:** Render canvas in headless browser. Assert background pixel RGBA = (0,0,0,0).

### Integration Tests
- **Full Overlay Flow:** Start overlay server → start OBS recording → activate overlay → draw a circle → deactivate overlay → stop recording. Assert the circle appears in the recorded video between the activation and deactivation timestamps.

### Usability Tests
- **Tablet Input Latency:** Draw continuous strokes on iPad/tablet. Assert visual latency from stylus movement to OBS preview is < 100ms.
