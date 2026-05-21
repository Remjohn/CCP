# CMF Visual & Sonic Orchestration Brief

> **Session:** 2026-04-15 | **Context:** High-level documentation brief for the upcoming CMF Pipeline orchestration upgrades based on the CutClaw analysis and Sovereign Computing directives. Technical specifications will be drafted in a separate phase.

## 1. Executive Summary

To achieve absolute platform sovereignty and 90% automation efficiency in the Conscious Movie Factory (CMF) pipeline, three core architectural changes will be implemented. These upgrades replace third-party dependencies (Suno AI), eliminate expensive post-production AI fixes (Smart Cropping), and introduce a world-class semantic memory for all visual assets.

1.  **Sovereign Music Generation:** Replacing Suno AI with local `ACE-Step-1.5` inference to gain absolute control over music stems, silent pauses, and beat-sync routing.
2.  **Source-Level Framing:** Implementing a "Red Guide" UI in the Telegram Mini App to force perfect 9:16 framing from coaches, leaving mathematically precise negative space for post-production jump cuts without decapitating the subject.
3.  **Multi-Modal Visual Vector Library:** Transforming all video assets (historical, A-Roll, AI-generated B-Roll, E-Roll) into a 1-FPS vector-searchable database using sovereign Vision-Language Models (VLM).

---

## 2. Component 1: Sovereign Music Generation (ACE-Step-1.5)

We are localizing music generation to remove API dependency and unlock precise audio mixing that third-party APIs refuse to allow.

### The Strategy
*   **Local Inference Node:** `ACE-Step-1.5` will be deployed natively within the sovereign NIM stack.
*   **Sonic Sommelier Upgrade:** The `sommelier.md` and `scribe.md` agents will output `ACE-Step` configuration parameters (BPM, structural tags, stem directives) instead of generic prompt strings.
*   **Stem-Level Mixing:** Because we run the model locally, we can extract isolated stems (Vocals, Drums, Melody). The pipeline will automatically duck (mute) the generated vocal stem when the coach is speaking, and boost it during tracked "silent pauses" in the VO for maximum emotional hit.
*   **Audio-Dialogue Sync Engine:** The generated audio will be parsed to extract a mathematical beat array. Remotion transitions (e.g., Turn → Result phase shifts) will snap perfectly to these downbeats.

---

## 3. Component 2: Source-Level Framing (Mini App UI Guides)

Instead of relying on computationally heavy AI to fix bad framing in post-production via smart cropping, we will enforce correct framing at the moment of recording through "poka-yoke" (error-proofing) UI design.

### The Strategy
*   **Telegram Mini App Camera UI:** Implement a recording overlay featuring a "Red Guide" alignment grid.
*   **Coach Instructions:** Visual cues will instruct the coach exactly where their eyes and shoulders must sit within the 9:16 frame.
*   **Jump-Cut Padding:** The grid will deliberately enforce framing that leaves negative space (padding). This ensures that automated `EFFECT-M-04 (Punch-In)` jump cuts (typically a 115% scale increase) will not cut off the coach's head in post-production.
*   **Post-Processing Fallback:** All *new* Daily Mini App content will be perfectly framed by the coaches. The pipeline will only use basic center-cropping or lightweight FFmpeg cropping for older archival footage.

---

## 4. Component 3: The Multi-Modal Visual Library (1-FPS Annotation)

This is the most strategic upgrade: turning dead archive footage into an active, searchable database with precise cinematic intelligence built for our 5-phase Causal Construction workflows.

### The Strategy
*   **NIM Containerized Captioning:** A sovereign Vision-Language Model (like Qwen-VL or Gemini-3) will run asynchronously over the historical archive, new E-Roll, and previously generated assets.
*   **Per-Second Cadence (1-FPS):** Since our assets are short (5-20s for A-Roll, 5-8s for cinematic B-Roll) and edits MUST snap to music downbeats, visual captioning will occur at a strict 1-second cadence. This guarantees frame-accurate retrieval.
*   **World-Class Semantic Schemas:** Metadata tagging will be ruthlessly optimized for our storytelling architecture. It will NOT just list objects ("man sitting"). It will annotate:
    *   **Emotional State:** "exhibiting processing mood", "authoritative stance"
    *   **Juxtaposition Value:** "visual contradiction"
    *   **Tension & Framing Proximity:** "claustrophobic tight crop", "isolated wide shot"
*   **Vector Database Integration (Chroma/Milvus):** These high-frequency visual captions will be stored alongside their exact mathematical timestamps.
*   **Agent Enhancement:** `deep-researcher` and `asset_hunter` agents will no longer rely on file names or manual text tags. They will query the vector database directly with a visual/emotional premise, pulling the exact seconds of footage needed to satisfy the psychological routing of the script.

---

> **Next Steps:** This document serves as the high-level brief. Detailed Technical Specifications (Tech Specs) for each of these three components will be drafted and reviewed in the next phase before any codebase implementation begins.
