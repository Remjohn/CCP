# Handover & Architectural Design Blueprint: Era 3 Strategic Consolidation

This document serves as the formal handover record and architectural alignment plan for the next coding agent. It summarizes the strategic pivot of the Conscious Coaching Platform (CCP), catalogs all deprecated and kept specifications, links the key design blueprints, and outlines the step-by-step execution roadmap for the upcoming code construction phase.

---

## 1. Executive Context & Strategic Pivot

The CCP system is undergoing a consolidation phase to prune obsolete architectures and prepare for the development of its remaining 17 specifications. Two major pivots have been designed and approved:
1. **Streaming & Legacy Visual Engine Deprecations:** All active live-streaming pathways (WebRTC SFU broadcasting, RTMP relays, OBS controller integration) and legacy visual engines (RunningHub compilers, vision LLM validators) are officially deprecated. They are replaced by local asynchronous recording (Loom-style native browser capture) and deterministic, local rendering using the **Skia Hardware Sidecar** and **Primitive Registry Query Service (`FR-ERA3-06`)**.
2. **Container-Isolated Global Admin Architecture:** To preserve single-tenant isolation, the Global Admin Dashboard operates outside container boundaries. It utilizes a host-level orchestrator to clone master templates when provisioning new client environments, and queries an authenticated Host Gateway to execute loopback API calls to tenant containers for content previews and operator controls.

---

## 2. Definitive Specification Map

A total of 28 specifications were evaluated for construction. The final layout has been cataloged in the system ledger:

### A. Deprecated & Obsolete Specifications (11 Specs)
These are retired in their entirety and must not be built or imported:
* `FR-VIS-03_PSSL_Prompt_Compilation_Tech_Spec.md` (PSSL-to-RunningHub compiler defunct)
* `FR-VIS-04_Visual_Validation_Tech_Spec.md` (Vision LLM-based AGSS validation defunct)
* `FR-VIS-09_Image_Sourcing_Hierarchy_Tech_Spec.md` (External stock search hierarchy defunct)
* `FR-VIS-11_In_App_Image_Search_Panel_Tech_Spec.md` (Canva template integration panels defunct)
* `FR-VIS-14_ConsciousSmile_Expression_Adapter_Tech_Spec.md` (Legacy expression adapter defunct)
* `FR-VIS-15_ConsciousPose_Body_Language_Library_Tech_Spec.md` (Legacy body pose library defunct)
* `FR-VIS-16_First_Frame_Composer_Tech_Spec.md` (Replaced by local Skia composition)
* `FR-VIS-17_Identity_LoRA_Training_Pipeline_Tech_Spec.md` (Programmatic LoRA training defunct)
* `FR-COM-04_Program_Campaign_Manager_Tech_Spec.md` (Campaigns module defunct)
* `FR-CA11-21_Studio_Guest_Join_Tech_Spec.md` (WebRTC multi-party guest join defunct)
* `Sovereign_Visual_Research_Engine_TechSpec_V1.md` (Legacy visual research engine defunct)

### B. Kept Specifications for Construction (17 Specs)
These are scheduled for code construction and have been configured in the build registry:
1. **Commercial & Admin:**
   * `FR-COM-02_Global_Admin_Dashboard_Tech_Spec.md` (Container-isolated preview board)
   * `FR-COM-03_Telegram_Code_Onboarding_Agent_Tech_Spec.md` (Self-service intake bot)
2. **CBCS mini-apps:**
   * `FR_CBCS_02_Social_Penetration_Depth_Gauge_Tech_Spec.md` (Intimacy escalation tracker)
   * `FR_CBCS_05_72_Hour_Identity_Anchor_Protocol_Tech_Spec.md` (Dormancy prevention hooks)
   * `FR_CBCS_07_Telegram_Intimacy_Index_Tech_Spec.md` (Conversational metric trackers)
   * `FR_CBCS_12_Coping_Diagnostic_Invitation_Engine_Tech_Spec.md` (Behavioral diagnostics)
   * `FR_CBCS_13_Counterfactual_Activation_Window_Tech_Spec.md` (Timing-based triggers)
   * `FR_CBCS_14_Conscious_Relationship_Nurturing_Architecture_Tech_Spec.md` (Long-term retention protocols)
3. **CA11 Downstream Workspace Services:**
   * `FR-CA11-06_Voice_Note_Course_Material_Tech_Spec.md` (Voice to slides compiler)
   * `FR-CA11-07_Session_to_Course_Pipeline_Tech_Spec.md` (Transcript compilation engines)
   * `FR-CA11-09_Accountability_Visualization_Tech_Spec.md` (AFFiNE dashboard graphics)
   * `FR-CA11-10_Excalidraw_Embedded_Workspace_Tech_Spec.md` (Direct canvas diagram blocks)
   * `FR-CA11-12_Course_Video_CMF_Pipeline_Tech_Spec.md` (Skia rendering matrices for CMF)
   * `FR-CA11-15_Contextual_Branding_Dynamic_PAD_Tech_Spec.md` (Color-mood palette modifiers)
   * `FR-CA11-17_Studio_Soundboard_Audio_Tech_Spec.md` (Synthesized audio assets compilation)
   * `FR-CA11-18_Social_Scheduling_Performance_Tech_Spec.md` (Social performance grids inside AFFiNE)
4. **Research Subsystem:**
   * `Sovereign_CRAL_Research_Engine_TechSpec_V1.md` (Structured research crawler)

---

## 3. Key Design Files & Code Locations

You must use the following files to maintain architectural consistency during implementation:

### A. Active Blueprints & Handover Assets
* **System Ledger Map:** [CCP_MASTER_SYSTEM_LEDGER.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/CCP_MASTER_SYSTEM_LEDGER.md) — Aligned Section 8.1 to formally register the deprecated specs.
* **Host Control Plane & Loopback Routing Spec:** [HOST_CONTROL_PLANE_PROVISIONING_AND_LOOPBACK_ROUTING.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/HOST_CONTROL_PLANE_PROVISIONING_AND_LOOPBACK_ROUTING.md) — Contains the exact Docker environment cloning script (`clone-tenant.sh`), the FastAPI Host Gateway loopback router proxy, the local security bypass middleware, and the CBCS integration pattern.
* **Decommissioning Specs:**
  * Streaming Subsystem: [DEPRECATION_STREAMING_PLATFORM.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/DEPRECATION_STREAMING_PLATFORM.md)
  * Visual Intelligence Engine: [DEPRECATION_VISUAL_INTELLIGENCE_ENGINE.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/DEPRECATION_VISUAL_INTELLIGENCE_ENGINE.md)
* **Onboarding Bot Spec:** [FR-COM-03_Telegram_Code_Onboarding_Agent_Tech_Spec.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/FR-COM-03_Telegram_Code_Onboarding_Agent_Tech_Spec.md) — Updated to query the direct AFFiNE-synchronized schema instead of the retired `FR-COM-04`.
* **Studio Block Spec:** [FR-CA11-16_CCP_Studio_Block_Tech_Spec_UPDATED.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/april_updates/FR-CA11-16_CCP_Studio_Block_Tech_Spec_UPDATED.md) — Details the client-side `loom_quick` record matrices and direct-to-S3 multi-part uploading.
* **Build Sequence Trigger:** [TRIGGER_COMMAND_BUILD.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/april_updates/TRIGGER_COMMAND_BUILD.md) — Cataloged build checklist pruned of deprecated components.

### B. Project Implementation Scratches
* Master Implementation Plan: [implementation_plan.md](file:///C:/Users/Mitano/.gemini/antigravity/brain/233d4f2f-a979-49ce-bb9e-c135b6252d71/implementation_plan.md)
* Living Task Checklist: [task.md](file:///C:/Users/Mitano/.gemini/antigravity/brain/233d4f2f-a979-49ce-bb9e-c135b6252d71/task.md)
* Living Walkthrough Log: [walkthrough.md](file:///C:/Users/Mitano/.gemini/antigravity/brain/233d4f2f-a979-49ce-bb9e-c135b6252d71/walkthrough.md)

---

## 4. Execution Blueprint for the Next Agent

When you begin the execution phase, follow this sequential roadmap:

### Step 1: Remove Decommissioned Endpoints & Code
Clean up the codebase by removing legacy real-time WebRTC and OBS broadcast routes.
* **Target 1:** Remove the endpoints `POST /studio/broadcast/signal`, `POST /studio/guest-invite`, and websockets `/ws/stream/{session_id}` and `/signal/{session_id}` from `src/ccp/api/studio_block_api.py`.
* **Target 2:** Delete the physical files `src/ccp/services/guest_join_service.py`, `src/ccp/services/studio_block_service.py`, and `tests/integration/test_ca11_fr21_guest_join.py`.
* **Target 3:** Delete all references to the `ccp-stream-service` microservice configurations in docker-compose.yml files.

### Step 2: Implement the Global Admin & Loopback Routing (`FR-COM-02`)
Implement the host gateway and tenant authorization proxies.
* **Task 1:** Create the host gateway route mapping endpoints inside the operator FastAPI codebase (mapping request proxying as described in `HOST_CONTROL_PLANE_PROVISIONING_AND_LOOPBACK_ROUTING.md`).
* **Task 2:** Add the `X-Operator-Token` validation middleware inside the tenant FastAPI container pipeline to securely bypass standard Row-Level Security checks for loopback admin queries.
* **Task 3:** Setup the Shell/Python orchestrator trigger scripts for Docker container duplication on the host control plane.

### Step 3: Implement the Telegram Code Onboarding Agent (`FR-COM-03`)
Create the self-service conversational onboarding bot.
* **Task 1:** Build the Telegram bot intake state machine collecting user name, email, and goals.
* **Task 2:** Query the direct Supabase registry schemas to validate program codes.
* **Task 3:** Auto-provision the client profile, report credit metrics via the Billing Middleware (`FR-COM-01`), and append the client card onto the AFFiNE coach workspace board.

### Step 4: Construct the Kept CBCS Mini-Apps & Downstream CA11 Blocks
Implement the 6 mini-apps and 8 workspace tools targets sequentially:
* **Task 1:** Ensure all mini-apps fetch their evaluation constants from the YAML registry utilizing the `PrimitiveRegistryQueryService` (`FR-ERA3-06`).
* **Task 2:** Ensure all state transition events execute audit trail writing using `ReceiptChainGuard` (`FR47`).
* **Task 3:** Implement the Skia Hardware Sidecar layout rendering layers in the CMF course video pipelines.

### Step 5: Test Verification
* Execute the pytest suite (`pytest tests/`) to confirm that all legacy mock imports have been successfully cleared and the system is fully stabilized.
