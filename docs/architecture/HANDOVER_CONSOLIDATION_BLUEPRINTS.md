# Handover & Architectural Design Blueprint: Era 3 Strategic Consolidation

This document serves as the formal handover record and authoritative architectural alignment plan for the next coding agent. It summarizes the strategic pivot of the Conscious Coaching Platform (CCP) in the May 2026 phase, catalogs all deprecated and kept specifications, maps core registries and design files, and provides an actionable step-by-step roadmap for final code construction.

---

## 1. Executive Context & Strategic Pivot

The CCP system has undergone a profound architectural consolidation in May 2026 to align all subsystems with a singular, uncompromising objective: **Conscious Human Transformation through identification and behavioral change**. The entire platform's runtime is structured as an intelligence and delivery ecosystem designed to facilitate this goal.

To secure this vision and avoid architectural drift, several critical pivots have been formalized:

### A. Streaming & Legacy Visual Engine Deprecations
*   All active live-streaming pathways (WebRTC SFU broadcasting, RTMP relays, OBS Studio controller integrations) are officially deprecated and decommissioned.
*   They are replaced by native local asynchronous recording (Loom-style native browser capture) via the **CCP Studio Block (`FR-CA11-16`)**, feeding directly into an S3 multi-part uploading scheme.
*   Legacy monolithic generative visual engines (PSSL-to-RunningHub compilers, external stock search layers, and vision LLM validation gates) are deprecated.

### B. The Reversal of the Visual Intelligence Engine (VIE) Deprecation
*   The previously proposed total deprecation of the Visual Intelligence Engine (VIE) has been **formally reversed**. 
*   Our visual intelligence is highly valuable, hyper-sophisticated, and critical to the **"Living Still"** and Parallax compositional mechanics that define the platform's premium, immersive aesthetic.
*   Instead of monolithic scene generation, we implement the **Hybrid Component Pipeline**:
    1.  **Generate (VIE / LoRA):** The VIE operates as a generative asset feeder. It generates discrete, isolated semantic ingredients matching the semantic and emotional vector. *Crucially, these are gathered asynchronously during the 3-Voice-Note Drafting Session before the final video is even recorded.*
    2.  **Mask & Depth (SAM3 / PRETEXT):** Generated assets and webcam captures are passed through **Segment Anything Model 3 (SAM3)** to extract pixel-perfect alpha masks (coach cutouts), and **PRETEXT** to estimate Z-depth matrices.
    3.  **Composite (Remotion + @remotion/skia):** A centralized Node.js Remotion server consumes the depth-aware layers. We natively integrate React Native Skia (via CanvasKit WebAssembly) inside Remotion to handle deep pixel math and parallax displacement, while using standard React to keep text animation highly intentional and sparse (e.g., using Rough Notation).
*   **The 4 Vertical Video Realization Formats:** The entire media engine is focused exclusively on Vertical Video (Shorts and Long-form), rendered using:
    *   *Format 1: Cinematic Story Commentary* (Transformational arcs, layered memory objects, scenes, parallax).
    *   *Format 2: 2D Avatar / Animated Explainer* (Procedural coaching modules, Excalidraw vector overlays synchronized to cadence).
    *   *Format 3: Living Commentary Reactions* (Proof objects/screenshots remain static. The coach cutout is placed at the bottom reacting. Highlighting uses Rough Notation).
    *   *Format 4: Conscious Reactions Editing* (Solo Reaction, Debate with Jury. Employs memetic sound cues up to **1 per 10 seconds**, compared to the 1 per 30s limit for Formats 1-3).

### C. The Absolute Ban on Synthetic Voice & The Complete Editing Session
*   Human transformation requires trust; trust requires biological authenticity. The use of synthetic AI voice generation (e.g., ElevenLabs clones) to deliver the coach's message is **strictly and permanently prohibited**.
*   **The Complete Editing Session:** To ensure intelligent orchestration and zero data loss, every lesson initiates a stateful "Editing Session" wrapper. This holds all CRAL research, VIE assets, and transcripts in one payload.
*   The system uses a strict **Trigger-First Loop**: Within the Editing Session, the coach receives a static Carousel (rendered via Remotion `renderStill`), engages in a **Drafting Session** (3 Voice Notes + Agent comments), and finally records an authentic reaction video. 
*   Before final editing, the recorded video's performance is formally scored.
*   The raw authentic audio/video recorded is the unassailable core of the system. Final vertical videos will feature only the coach's authentic recorded voice, mixed with system-generated memetic sound cues and atmospheric pads.

### D. Single-Tenant Isolation & Global Admin Gateway
*   To preserve absolute single-tenant isolation, the **Global Admin Dashboard (`FR-COM-02`)** operates entirely outside tenant container boundaries. 
*   It utilizes a host-level orchestrator to clone master Docker templates when provisioning new client environments, and queries an authenticated **Host Gateway** using `X-Operator-Token` validation to execute loopback API queries into individual client containers for content previews and operator controls.

---

## 2. Definitive Specification Map

A total of 28 core specifications have been systematically audited. The final system ledger partitions these into deprecated and active tracks.

### A. Deprecated & Obsolete Specifications (2 Specs)
These are retired in their entirety. They must not be built, imported, or referenced in downstream code:
1.  [FR-COM-04_Program_Campaign_Manager_Tech_Spec.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/FR-COM-04_Program_Campaign_Manager_Tech_Spec.md)
2.  [FR-CA11-21_Studio_Guest_Join_Tech_Spec.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/FR-CA11-21_Studio_Guest_Join_Tech_Spec.md)

### B. Kept Specifications for Construction (26 Specs)
These are scheduled for code construction and have been configured in the build registry:
1.  **Commercial & Admin:** [FR-COM-02], [FR-COM-03]
2.  **CBCS Mini-Apps:** [FR_CBCS_02], [FR_CBCS_05], [FR_CBCS_07], [FR_CBCS_12], [FR_CBCS_13], [FR_CBCS_14]
3.  **CA11 Downstream Workspace Services:** [FR-CA11-06], [FR-CA11-07], [FR-CA11-09], [FR-CA11-10], [FR-CA11-12], [FR-CA11-15], [FR-CA11-17], [FR-CA11-18]
4.  **Research Subsystem:** [Sovereign_CRAL_Research_Engine_TechSpec_V1.md]
5.  **Visual Intelligence Engine (VIE) Upstream Assets:** *(These specs will be UPDATED to output generative assets directly into the Remotion 'Complete Editing Session' instead of the legacy compositor).*
    *   [FR-VIS-03_PSSL_Prompt_Compilation_Tech_Spec.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/FR-VIS-03_PSSL_Prompt_Compilation_Tech_Spec.md)
    *   [FR-VIS-04_Visual_Validation_Tech_Spec.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/FR-VIS-04_Visual_Validation_Tech_Spec.md)
    *   [FR-VIS-09_Image_Sourcing_Hierarchy_Tech_Spec.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/FR-VIS-09_Image_Sourcing_Hierarchy_Tech_Spec.md)
    *   [FR-VIS-11_In_App_Image_Search_Panel_Tech_Spec.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/FR-VIS-11_In_App_Image_Search_Panel_Tech_Spec.md)
    *   [FR-VIS-14_ConsciousSmile_Expression_Adapter_Tech_Spec.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/FR-VIS-14_ConsciousSmile_Expression_Adapter_Tech_Spec.md)
    *   [FR-VIS-15_ConsciousPose_Body_Language_Library_Tech_Spec.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/FR-VIS-15_ConsciousPose_Body_Language_Library_Tech_Spec.md)
    *   [FR-VIS-16_First_Frame_Composer_Tech_Spec.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/FR-VIS-16_First_Frame_Composer_Tech_Spec.md)
    *   [FR-VIS-17_Identity_LoRA_Training_Pipeline_Tech_Spec.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/FR-VIS-17_Identity_LoRA_Training_Pipeline_Tech_Spec.md)
    *   [Sovereign_Visual_Research_Engine_TechSpec_V1.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/Sovereign_Visual_Research_Engine_TechSpec_V1.md)

---

## 3. Key Design Files & Code Locations

You must refer directly to the following documents to maintain architectural integrity:

### A. Core Architecture Registries
*   **System Ledger Map:** [CCP_MASTER_SYSTEM_LEDGER.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/CCP_MASTER_SYSTEM_LEDGER.md)
*   **Host Control Plane Spec:** [HOST_CONTROL_PLANE_PROVISIONING_AND_LOOPBACK_ROUTING.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/HOST_CONTROL_PLANE_PROVISIONING_AND_LOOPBACK_ROUTING.md)
*   **Active Build Checklist:** [TRIGGER_COMMAND_BUILD.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/april_updates/TRIGGER_COMMAND_BUILD.md)

### B. May 2026 updates Folder (Canonical Output)
All strategic updates and new specs generated in the May 2026 phase are grouped inside the directory: [May 2026 UPDATES/](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/May%202026%20UPDATES/)
*   **Trigger-First / VIE Reversal Audit:** [Architectural_Audit_Trigger_First_Vision_Visual_Engines.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/May%202026%20UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md) — Details the LW28 speaking programs, the 3-voice-note Drafting Session loop, asynchronous background visual generation, the 4 vertical video formats (including coach cutout layouts), scoring mechanics, memetic sound rules, and the strict ban on synthetic voice.
*   **VIE Retention Deep-Dive:** [AUDIT_Visual_Intelligence_Retention.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/May%202026%20UPDATES/AUDIT_Visual_Intelligence_Retention.md) — Detail-heavy analysis specifying SAM3 segmentations and Skia/Remotion layouts with intentional, sparse animation.
*   **Phase 7 Spec Updates & Prompts:** Located inside the subfolder: [spec_prompts/](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/May%202026%20UPDATES/spec_prompts/)

### C. Agent Scratch Plan Artifacts
*   Implementation Blueprint: [implementation_plan.md](file:///C:/Users/Mitano/.gemini/antigravity/brain/233d4f2f-a979-49ce-bb9e-c135b6252d71/implementation_plan.md)
*   Active Todo Checklist: [task.md](file:///C:/Users/Mitano/.gemini/antigravity/brain/233d4f2f-a979-49ce-bb9e-c135b6252d71/task.md)
*   Phase Walkthrough Log: [walkthrough.md](file:///C:/Users/Mitano/.gemini/antigravity/brain/233d4f2f-a979-49ce-bb9e-c135b6252d71/walkthrough.md)

---

## 4. Execution Roadmap for Code Construction

When code construction is triggered, you must execute the implementation using the following chronological phases:

### Phase 1: Remove Decommissioned Endpoints & Code
Clean the code footprint of retired live-streaming and OBS pipelines.

### Phase 2: Implement the Global Admin & Loopback Routing (`FR-COM-02`)
Implement container network bypasses and secure preview mechanics.

### Phase 3: Construct the Telegram Code Onboarding Agent (`FR-COM-03`)
Build the self-service onboarding Telegram bot state machine collecting user name, email, and goals.

### Phase 4: Construct the Kept CBCS Mini-Apps & CA11 Downstream Blocks
Implement the 6 mini-apps and 8 workspace tools targets sequentially. Ensure evaluation constants are fetched properly and state transition events execute audit trail writing.

### Phase 5: Implement the Hybrid Media Render Pipeline
Implement the centralized Remotion Server-Side pipeline integrating VIE generated components, SAM3 masks, and `@remotion/skia`:
*   **Task 1:** Create the **Complete Editing Session** data model in the backend to store and group all CRAL research, generated VIE assets, and static Carousels under a single lesson context.
*   **Task 2:** Integrate Stable Diffusion + Custom LoRA calls inside the media factory queue to asynchronously generate B-roll / background plates *during the coach's drafting session*, attaching them to the active Editing Session.
*   **Task 3:** Invoke SAM3 to segment foreground subjects (coach cutout) from the recorded video and extract alpha masks.
*   **Task 4:** Configure the Node.js Remotion server to consume the Complete Editing Session payload. It will use `@remotion/skia` for Z-depth parallax and standard React for intentional, sparse animations like Rough Notation. The legacy standalone Python Skia sidecar (`src/ccp/services/cmf_arc_governed_rendering.py`) is to be deleted.
*   **Task 5:** Add execution checks (FR-ERA3-15) validating the performance score and that the authentic video file is present. Apply correct memetic sound limits per format (Format 4 = 1/10s, Others = 1/30s).

### Phase 6: Automated Verification
*   Execute the Pytest framework: `pytest tests/` to confirm that all legacy mock imports have been successfully cleared and the system is fully stabilized.

---

This document represents the absolute, comprehensive architectural truth. Proceed immediately with execution following these bounds.
