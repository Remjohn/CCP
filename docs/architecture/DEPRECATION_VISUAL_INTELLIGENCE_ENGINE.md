# Deprecation & Upgrade Specification: Visual Intelligence Engine & RunningHub Integration

**Created:** 2026-05-21  
**Status:** Approved for Deprecation & Upgrade  
**Version:** 1.0  
**Domain:** Media/Content Factory (CMF)  
**Reference Specs:** `FR-VIS-03`, `FR-VIS-04`, `FR-VIS-09`, `FR-VIS-11`, `FR-VIS-14` to `17`, `Sovereign_Visual_Research_Engine_TechSpec_V1`

---

## 1. Executive Summary

The legacy **Visual Intelligence Engine** (built around complex multi-stage AI image generation pipelines, external prompt compilers, and visual validation agents utilizing RunningHub and Canva) is officially deprecated and retired. 

MCDA reviews and operator experience demonstrated that external text-to-image workflows are slow, unpredictable, and expensive, and they frequently suffer from character drift and aesthetic incoherence. 

To resolve these failures, CCP is transitioning to a **Deterministic Local Layout Compositing** model. Headless layout generation, overlay positioning, and palette branding are performed locally using the **Skia Hardware Sidecar**, while design constants and thematic structures are governed directly by the **Primitive Registry Query Service** (`FR-ERA3-06`) and the **Subliminal Function Library** (SFL).

---

## 2. Retired Technical Specifications

The following technical specifications are retired and marked as obsolete in the system ledger:

| Spec ID | Document Name | Retirement Rationale |
| :--- | :--- | :--- |
| **FR-VIS-03** | `FR-VIS-03_PSSL_Prompt_Compilation_Tech_Spec.md` | **RETIRED:** Paradoxe's PSSL-to-RunningHub prompt compiler is obsolete. External text-to-image prompt generation is decommissioned. |
| **FR-VIS-04** | `FR-VIS-04_Visual_Validation_Tech_Spec.md` | **RETIRED:** Vision LLM-based AGSS scoring and character drift validations are retired. Verification is shifted to structural, deterministic checks in SFL. |
| **FR-VIS-09** | `FR-VIS-09_Image_Sourcing_Hierarchy_Tech_Spec.md` | **RETIRED:** Aurore's image sourcing hierarchy (checking Photo Deck -> Stock API -> Stable Diffusion -> Ghibli) is decommissioned. Sourcing is consolidated into local SFL asset directories. |
| **FR-VIS-11** | `FR-VIS-11_In_App_Image_Search_Panel_Tech_Spec.md` | **RETIRED:** The React image search panel component mapping to Notion and Canva templates is decommissioned. |
| **FR-VIS-14** | `FR-VIS-14_ConsciousSmile_Expression_Adapter_Tech_Spec.md` | **RETIRED:** Legacy visual engine face-expression editing adapter is decommissioned. |
| **FR-VIS-15** | `FR-VIS-15_ConsciousPose_Body_Language_Library_Tech_Spec.md` | **RETIRED:** Legacy body pose library mapping is decommissioned. |
| **FR-VIS-16** | `FR-VIS-16_First_Frame_Composer_Tech_Spec.md` | **RETIRED:** Replaced by Skia renderer layout templates. |
| **FR-VIS-17** | `FR-VIS-17_Identity_LoRA_Training_Pipeline_Tech_Spec.md` | **RETIRED:** Programmatic training of character-specific LoRA models on RunPod is decommissioned. |
| **Sovereign** | `Sovereign_Visual_Research_Engine_TechSpec_V1.md` | **RETIRED:** Sovereign visual research database contract is decommissioned. |

---

## 3. Replacement Architecture

```mermaid
graph TD
    subgraph Legacy Pipeline (DEPRECATED)
        PSSL[VCB PSSL Grammar] --> Paradoxe[Paradoxe Prompt Compiler]
        Paradoxe --> RH[RunningHub SDXL API]
        RH --> VVA[Visual Validation Agent: Vision LLM]
        VVA --> Canva[Canva Template Placement]
    end

    subgraph Native Era 3 Architecture (ACTIVE)
        Script[Content Script / Lesson] --> SFL[Subliminal Function Library]
        SFL -->|Inject Brand Tokens & Styles| Skia[Skia Hardware Sidecar]
        PR[Primitive Registry Query Service] -->|Inject HSL Colors / Fonts / Scales| Skia
        Skia -->|Deterministic Headless Composition| WebM[Rendered Video / PNG Asset]
    end
    
    style Legacy Pipeline fill:#3b1e2e,stroke:#313244,stroke-width:1px,color:#cdd6f4
    style Native Era 3 Architecture fill:#181825,stroke:#a6e3a1,stroke-width:2px,color:#cdd6f4
```

1.  **Rendering Engine:** Headless layout compilation is offloaded to `src/ccp/sidecars/skia-renderer/` utilizing Skia's high-performance C++ backend (accessed via python-skia or CanvasKit).
2.  **Design Tokens:** Design constants, including HSL color palettes, typographical scales, and motion curves, are read from YAML files in the `primitives/` directory via the **Primitive Registry Query Service (`FR-ERA3-06`)**.
3.  **Visual Brand Scoping:** Palette adaptation and theme matching are handled directly by the **Subliminal Function Library** (SFL) and the **Contextual Branding Dynamic PAD Engine (`FR-CA11-15`)**, ensuring exact color-mood alignment without generative unpredictability.

---

## 4. Decommissioning & Cleanup Plan

### A. External API Integrations
*   **RunningHub:** Remove all API keys, task-polling loops, and model weight mapping from backend configurations.
*   **Canva Developer API:** Disable all authentication routes and webhook endpoints. Remove any references to Canva templates or layout wrappers.

### B. Obsolete Code File Cleanups
The following active code files must be deleted or stripped of deprecated visual engine components:
*   **Delete:** `src/ccp/api/canvas_api.py`, `src/ccp/services/canvas_composition_service.py`, `src/ccp/services/canva_affine_delivery.py`.
*   **Clean References:** Remove all imports of these services and any prompt compilation logic inside `src/ccp/pipelines/` or the CMF orchestration controllers.
