# CCP MASTER SYSTEM LEDGER
**Authoritative Operational Map & System Governance Blueprint**  
*Document Version: Era 3 - Phase 1.1*  
*Last Updated: May 2026*  

---

## 1. System Governance & Architectural Philosophy

The Conscious Coaching Platform (CCP) is governed as a dual-layer AI-orchestrated runtime environment:

```mermaid
graph TD
    subgraph Layer 1: Pi Coding Agent Substrate (Earendil Works)
        Pi[Pi Extension Harness] -->|11 Extensions| JIT[JIT Skill Compilation]
        JIT -->|Compiles| CCSB[Custom Code Sandbox]
    end
    
    subgraph Layer 2: CCP Governance & Verification Layer
        CCSB -->|Executes| RCG[Receipt Chain Guard]
        RCG -->|Verifies State| DB[(Supabase Ledger)]
        SAG[Semantic Affinity Guard] -->|Inspects| CCSB
        PRQ[Primitive Registry] -->|Injects Constants| CCSB
        UORG[Upward-Only Routing Gate] -->|Validates Purchase| CCSB
    end
    
    style Layer 1 fill:#1e1e2e,stroke:#313244,stroke-width:2px,color:#cdd6f4
    style Layer 2 fill:#181825,stroke:#f38ba8,stroke-width:2px,color:#cdd6f4
```

### Layer 1: Pi Coding Agent Substrate (Earendil Works)
The foundational substrate handles sandboxed execution, JIT skill compilation, execution pipelines, and automated healing commands. It consists of the **11 Pi Extensions** (including `DamageControl`, `TillDone`, and `TaskRetry`) which execute low-level process management.

### Layer 2: CCP Verification & Governance Layer
The verification layer enforces safety, mathematical scoring integrity, whitelabel branding, and state persistence. This layer contains:
*   **Receipt Chain Guard (`FR47`)**: Ensures write-once, immutable logs of every client transaction and agent choice.
*   **Semantic Affinity Guard (`FR-SAF-02`)**: Inspects dynamic LLM outputs against active brand guidelines to prevent toxic content variations.
*   **Primitive Registry Query Service (`FR-ERA3-06`)**: Queries the 243+ experience and meaning primitives.
*   **Upward-Only Routing Gate**: Enforces purchase pathways and tier eligibility checks based on user profiles.

---

## 2. Product Module Inventory (PRDs)

CCP is organized into 9 modules, defining system capabilities, boundaries, and quality requirements:

| Module ID | Module Name | Core Strategy / Functional Mandate | Active Specs |
|---|---|---|---|
| **PRD-01** | Platform Strategy | Single-tenant isolation, whitelabel mapping, and AFFiNE synchronization. | `FR-ERA3-08`, `FR-ERA3-10` |
| **PRD-02** | CCF Content Factory | Dynamic script compilation, psychological routing, and semantic guardrails. | `FR-ERA3-15`, `FR-ERA3-16` |
| **PRD-03** | CMF Media Factory | CMF shot intelligence, video composition, and hardware-accelerated Skia rendering. | `FR-ERA3-12`, `FR-VIS-14` to `18` |
| **PRD-04** | CVE Experience Design | Telegram Intimacy Index tracking, habit loops, and voice-to-lesson compilation. | `FR-ERA3-13`, `FR-ERA3-17` |
| **PRD-05** | CBCS Law28 | Biometric scorecards, social penetration escalation, and learning paths. | `FR-ERA3-11`, `FR-ERA3-18`, `FR-ERA3-19` |
| **PRD-06** | Conscious Reactions | Async reaction modes, co-creation quizzes, and tournament matchmaking. | `FR-ERA3-05-CORE`, `05a` to `05j` |
| **PRD-07** | V²WS Webinar | Programmatic webinar compilation, interactive replays, and companion app. | `FR-ERA3-01`, `FR-ERA3-07` |
| **PRD-08** | Conscious Primitives | YAML primitive registry query engine and experience-design family locks. | `FR-ERA3-06` |
| **PRD-09** | CPSC Silent Referral | In-chat paywall sheets, dynamic trial gates, and silent social referral loops. | `FR-ERA3-02`, `FR-ERA3-03`, `FR-ERA3-04` |

---

## 3. Spec Directory & Runtime Domain Mapping

The 146 technical specifications are grouped under **8 Runtime Domains**:

### 3.1 Domain A: Genesis & System Architecture (Genesis)
*   **Specs:** `FR49_Single_Tenant_Deployment_Tech_Spec`, `FR47_Receipt_Chain_Guard_Tech_Spec`
*   **Code Implementation:** `src/ccp/core/receipt_chain.py`, `src/ccp/services/single_tenant_deployment_service.py`
*   **Verification (Tests):** `tests/integration/test_step14_cross_system_integration.py`

### 3.2 Domain B: Coach Identity & Voice DNA (Coach DNA)
*   **Specs:** `FR3_Voice_DNA_Tech_Spec`, `FR-CA11-15_Contextual_Branding_Dynamic_PAD_Tech_Spec` (requires update)
*   **Code Implementation:** `src/ccp/services/coach_soul_adapter.py`, `src/ccp/services/dpa_engine.py`
*   **Verification (Tests):** `tests/integration/test_ca11_fr15_dpa_engine.py`

### 3.3 Domain C: CRAL Research Engine (CRAL Research)
*   **Specs:** `Sovereign_CRAL_Research_Engine_TechSpec_V1` (unimplemented)
*   **Code Implementation:** `src/ccp/services/research_synthesis_protocol.py`
*   **Verification (Tests):** `tests/integration/test_vis02_tiar_integration.py` (requires update)

### 3.4 Domain D: Media/Content Factory (Content Factory)
*   **Specs:** `FR-ERA3-09_Conscious_Editor_Tech_Spec_UPDATED`, `FR-ERA3-12_CMF_Arc_Governed_Rendering_Tech_Spec`
*   **Code Implementation:** `src/ccp/services/content_machine.py`, `src/ccp/services/cmf_arc_governed_rendering.py`, `src/ccp/services/conscious_editor_service.py`
*   **Verification (Tests):** `tests/integration/test_conscious_editor_era3_09.py`, `tests/integration/test_fr_era3_12_cmf_sfl_rendering.py`

### 3.5 Domain E: Client Coaching & Metrics (Client Coaching)
*   **Specs:** `FR-ERA3-11_Challenge_Arena_Tech_Spec`, `FR-ERA3-13_Four_Surface_Async_Skill_Ladder_Tech_Spec`, `FR61_Biometric_Scoring_Tech_Spec`
*   **Code Implementation:** `src/ccp/services/trait_scoring_engine.py`, `src/ccp/services/learning_path_builder.py`, `src/ccp/services/habit_architecture.py`
*   **Verification (Tests):** `tests/integration/test_era3_fr18_cbcs_integration.py`, `tests/integration/test_fr_era3_18_cbcs_sfl_runtime.py`

### 3.6 Domain F: Webinar Delivery (Webinar)
*   **Specs:** `FR-ERA3-01_Webinar_Companion_Tech_Spec`, `FR-ERA3-07_AFFiNE_Broadcasting_Pipeline_Tech_Spec`
*   **Code Implementation:** `src/ccp/services/v2ws_interactive_service.py`, `src/ccp/services/session_to_course.py`
*   **Verification (Tests):** `tests/integration/test_era3_fr01_webinar_companion_api.py`, `tests/integration/test_era3_fr01_webinar_overlay_geometry.py`, `tests/integration/test_era3_fr01_webinar_rep_scoring.py`

### 3.7 Domain G: Commercial & Growth (Commercial)
*   **Specs:** `FR-ERA3-02_In_Chat_Telegram_Payments_Tech_Spec`, `FR-ERA3-03_Silent_Referral_Architecture_Tech_Spec_UPDATED`, `FR58_Offer_Tier_Architecture_Tech_Spec_UPDATED`
*   **Code Implementation:** `src/ccp/services/offer_tier_governor.py`, `src/ccp/services/conversion_sequence_router.py`
*   **Verification (Tests):** `tests/integration/test_cpsc_fr58_offer_tier_governor.py`, `tests/integration/test_cpsc_fr58_offer_tier.py`

### 3.8 Domain H: Workspaces & Mini App Shell (Workspace)
*   **Specs:** `FR-ERA3-08_Mini_App_Host_Shell_Tech_Spec`, `FR-CA11-02_AFFiNE_Sync_Service_Tech_Spec`, `FR-CA11-16_CCP_Studio_Block_Tech_Spec_UPDATED`
*   **Code Implementation:** `src/ccp/services/affine_sync.py`, `src/ccp/services/affine_workspace_provisioner.py`, `src/ccp/services/affine_client_workspace.py`
*   **Verification (Tests):** `tests/integration/test_ca11_fr02_affine_sync.py`

---

## 4. Active Infrastructure Topology

The active deployment architecture excludes third-party canvas builders and OBS Studio, relying entirely on native web surfaces and lightweight local rendering engines:

```
+-------------------------------------------------------------+
|                     Client Web / TMA WebApp                 |
|       - Vite/React Mini Apps (Solo, Debate, Tierlist)       |
|       - Telegram WebApp SDK                                 |
+------------------------------+------------------------------+
                               |
                               v HTTP / WebSockets
+-------------------------------------------------------------+
|                   FastAPI Web Server Gateway                 |
|       - Route: /api/telegram/webhook                        |
|       - Route: /api/sacred-audio/upload                     |
+------------------------------+------------------------------+
                               |
            +------------------+------------------+
            |                                     |
            v                                     v
+-----------------------+             +-----------------------+
|  Supabase (Postgres)  |             |  Skia Render Sidecar  |
|  - RLS Policies       |             |  - Hardware CMF shots |
|  - Postgres Tables    |             |  - Headless CanvasKit |
+-----------------------+             +-----------------------+
```

*   **FastAPI Engine (Python 3.11+)**: Serving as the primary application layer in `src/ccp/api/main.py`.
*   **Supabase (PostgreSQL 15)**: Database persistent storage, including RLS constraints on tables (`receipt_chain`, `asset_registry`, `person_registry`, `cultural_memory_map`, etc.).
*   **Redis Database**: Lightweight message-broker and status caching.
*   **AFFiNE Workspace**: Content management system and client dashboard repository. Notion is completely removed.
*   **Skia Hardware Sidecar**: Hardware-accelerated image/video layout composer in `src/ccp/sidecars/skia-renderer/`. OBS Studio and Canva are completely removed.

---

## 5. Orchestration Boundaries (Pi vs. CCP)

```
+-------------------------------------------------------------------+
|                        Pi Coding Agent                            |
|  - Orchestrates tasks, triggers compilation Retries, sandbox      |
|  - Monitors runtime exceptions via DamageControl.                 |
+---------------------------------+---------------------------------+
                                  |
                                  v JIT Invocation
+---------------------------------+---------------------------------+
|                    CCP Verification Layer                         |
|  - Verification of Receipt Chains on Supabase.                    |
|  - Pydantic models structure validations.                         |
|  - Trait scoring engines and biometric evaluations.               |
+-------------------------------------------------------------------+
```

*   **Pi Substrate Scope**: Executes low-level script automation, initializes coach environments, loads JIT extensions, and manages filesystem configurations.
*   **CCP Verification Scope**: Dictates business rules, processes Telegram messages through `vidye_router.py`, records immutable transactions on `receipt_chain.py`, performs validation with `ca11_models.py`, and maps psychological profiles in Neo4j.

---

## 6. Runtime-Critical Governance Systems

### 6.1 Receipt Chain Guard (`FR47`)
Every transactional choice or scoring output must write to the `receipt_chain` database table with the following payload structure:
```json
{
  "receipt_id": "rcpt_uuid_0000",
  "agent_id": "agent_uuid_1111",
  "action": "biometric_scoring_complete",
  "asset_id": "ast_xxxx",
  "person_id": "pers_yyyy",
  "verified_at": "2026-05-20T13:00:00Z"
}
```

### 6.2 Primitive Registry Query Service (`FR-ERA3-06`)
All system interactions query dynamic parameters from `primitives/` YAML records. prose-based instruction templates are strictly banned in favor of structured primitive values.

### 6.3 Semantic Affinity Guard
Intercepts visual content generation cues to block mismatching themes, fonts, or colors relative to the coach's resolved PAD brand values.

### 6.4 Upward-Only Routing Gate
Enforces sequential, non-downgradable tier access rules. When a client upgrades their program tier, they are permanently locked into that tier or higher; downgrades do not decrease the stored psychological values.

---

## 7. REST APIs & Services Directory

### Active API Routes
*   `POST /api/telegram/webhook`: Main integration webhook receiving updates from the Telegram Bot API, passing payloads directly to `vidye_router.py`.
*   `POST /api/sacred-audio/upload`: Direct upload endpoint for client and coach voice notes, storing files in the private `sacred-audio` S3 bucket.
*   `GET /health`: Diagnostic health checks returning coach configuration variables and connection statuses.

*Deprecated routes `POST /api/notion/webhook` and `GET/POST /api/canvas/*` are fully disabled.*

---

## 8. Obsolete Spec & Code Deprecation Catalog

The following legacy, Notion, Canva, WebRTC, and Trivianar files must be cleaned or deleted from the active codebase:

### 8.1 Technical Specifications Flagged Obsolete
1.  `FR-CA11-11_CVE_Canva_AFFiNE_Delivery_Tech_Spec.md` (Canva template integration)
2.  `FR-CA11-13_OBS_Recording_Controller_Tech_Spec.md` (Superseded by `FR-CA11-16`)
3.  `FR-CA11-14_Excalidraw_Live_OBS_Overlay_Tech_Spec.md` (Superseded by `FR-CA11-16`)
4.  `FR-CA11-19_Interactive_Trivianar_Engine_Tech_Spec.md` (Superseded by `FR-ERA3-05-CORE`)
5.  `FR-CA11-20_Trivianar_Lead_Capture_Tech_Spec.md` (Superseded by `FR-ERA3-03`)
6.  `FR-CA11-22_Stream_Overlay_Trivianar_Display_Tech_Spec.md` (Obsolete)
7.  `FR-VIS-05_Canvas_Composition_Delivery_Tech_Spec.md` (Superseded by `FR-ERA3-12`)
8.  `FR-VIS-06_Notion_Visual_Content_Card_Tech_Spec.md` (Obsolete)
9.  `FR45_Notion_Export_Pipeline_Tech_Spec.md` (Obsolete)
10. `SPEC_REWRITE_BRIEFING.md` (Superseded by `ERA3_Tech_Spec_Writing_Protocol.md`)
11. `FR-COM-04_Program_Campaign_Manager_Tech_Spec.md` (Obsolete Campaign module)
12. `FR-VIS-03_PSSL_Prompt_Compilation_Tech_Spec.md` (Obsolete Visual engine component)
13. `FR-VIS-04_Visual_Validation_Tech_Spec.md` (Obsolete Visual engine component)
14. `FR-VIS-09_Image_Sourcing_Hierarchy_Tech_Spec.md` (Obsolete Visual engine component)
15. `FR-VIS-11_In_App_Image_Search_Panel_Tech_Spec.md` (Obsolete Visual engine component)
16. `FR-VIS-14_ConsciousSmile_Expression_Adapter_Tech_Spec.md` (Obsolete Visual engine adapter)
17. `FR-VIS-15_ConsciousPose_Body_Language_Library_Tech_Spec.md` (Obsolete Visual engine adapter)
18. `FR-VIS-16_First_Frame_Composer_Tech_Spec.md` (Obsolete Visual engine component)
19. `FR-VIS-17_Identity_LoRA_Training_Pipeline_Tech_Spec.md` (Obsolete Visual training component)
20. `Sovereign_Visual_Research_Engine_TechSpec_V1.md` (Obsolete Visual research engine)
21. `FR-CA11-21_Studio_Guest_Join_Tech_Spec.md` (Obsolete WebRTC multi-party streaming)


### 8.2 Code Files Flagged Obsolete & Clean-up Directives

#### 1. Notion Cleanup (33 Files)
*   **Files Deleted:**
    *   `src/ccp/api/notion_webhook.py`
    *   `src/ccp/services/notion_sync.py`
    *   `src/ccp/services/notion_config.py`
    *   `src/ccp/services/notion_export_service.py`
    *   `src/ccp/services/notion_visual_content_card.py`
    *   `src/ccp/services/notion_content_builder.py`
    *   `src/ccp/services/notion_client_builder.py`
    *   `src/ccp/services/notion_audio.py`
    *   `src/ccp/scripts/setup_notion_workspace.py`
    *   `tests/integration/test_vis06_notion_card.py`
*   **Active Files Cleaned (Notion references removed):**
    *   `src/ccp/services/affine_sync.py`
    *   `src/ccp/services/affine_workspace_provisioner.py`
    *   `src/ccp/services/affine_client_workspace.py`
    *   `src/ccp/models/coach_registry.py` (fields: `notion_workspace_id`, `notion_token_ref` removed)
    *   `src/ccp/core/asset_id.py`
    *   `src/ccp/scripts/setup_supabase.py`, `scaffold_coach.py`, `setup_neo4j.py`
    *   `src/ccp/services/tiar_adapter.py`, `photo_deck_sync.py`, `publer_sync_service.py`, `known_persons_registry_adapter.py`, `data_analyst_service.py`, `distribution.py`, `client_onboarding.py`, `operator_review.py`, `sovereign_image_service.py`
    *   Tests: `test_ca11_fr01_workspace_provisioner.py`, `test_ca11_fr02_affine_sync.py`, `test_step14_cross_system_integration.py`, `test_vis02_tiar_integration.py`, `test_vis11_search_panel.py`

#### 2. Canva/Canvas Cleanup (38 Files)
*   **Files/Folders Deleted:**
    *   `src/ccp/api/canvas_api.py`
    *   `src/ccp/services/canvas_composition_service.py`
    *   `src/ccp/services/canva_affine_delivery.py`
    *   `tests/integration/test_canvas_api.py`
    *   `tests/integration/test_ca11_fr11_canva_delivery.py`
    *   `tests/integration/test_vis05_canvas_composition.py`
    *   `canva-app/` (Next.js frontend directory)
*   **Active Files Cleaned (Canva references removed):**
    *   `src/ccp/api/cmf_arc_render_api.py` & `phase0_eval_cards.py`
    *   `src/ccp/models/conscious_editor_models.py`, `reaction_debate_models.py`, `reaction_duel_models.py`, `reaction_mirror_quiz_models.py`, `spatial_engine_models.py`, `v5_models.py`
    *   `src/ccp/pipelines/spatial_composition_pipeline.py`
    *   `src/ccp/services/transparent_collage.py`, `layout_resolver_service.py`, `image_search_panel_adapter.py`, `excalidraw_overlay.py`, `excalidraw_compiler.py`, `debate_with_jury_service.py`, `conscious_editor_service.py`, `cmm_extraction.py`, `cmf_arc_governed_rendering.py`, `reaction_duel_service.py`, `saliency_analysis_service.py`
    *   Tests: `test_ca11_fr16_studio_block.py`, `test_conscious_editor_era3_09.py`, `test_era3_fr05c_reaction_duel_rendering.py`, `test_fr_era3_12_cmf_sfl_rendering.py`, `test_conscious_editor.py`, `test_frca1116_studio_block.py`

#### 3. WebRTC Cleanup (4 Files)
*   **Files Deleted:**
    *   `src/ccp/api/studio_block_api.py`
    *   `src/ccp/services/guest_join_service.py`
    *   `src/ccp/services/studio_block_service.py`
    *   `tests/integration/test_ca11_fr21_guest_join.py`

#### 4. Trivianar Cleanup (4 Files)
*   **Files Deleted/Shimmed:**
    *   `src/ccp/services/trivianar_engine_service.py` (Downgraded to minimal `TrivianarShim` compatibility class, then removed when downstream is refactored)
    *   `src/ccp/services/stream_overlay_service.py` (Deleted)
    *   `src/ccp/services/lead_capture_service.py` & `test_ca11_fr20_lead_capture.py` (Trivianar logic cleaned)
    *   `tests/integration/test_ca11_fr19_trivianar_engine.py` & `test_ca11_fr22_stream_overlay.py` (Deleted)

---

## 9. Dependency Graph & Gaps Analysis

### Foundational Gaps & Missing Specs
*   `DEP-ENG-023` (Cultural Memory Map): Mapped to a static DB file. Need to define an active producer spec.
*   `DEP-ENG-010` (Segment Analysis): Consumed by onboarding trackers. Needs spec calibration.
*   `DEP-ENG-018` (Active Archetype Schema): Handled via local primitives in Era 3.

---

### Verification and Approval Status
**Phase 1 Ledger Compiled Successfully.**  
Approved for platform execution mapping.
