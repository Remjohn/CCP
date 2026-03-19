# Tech-Spec: FR-VIS-04 — Visual Validation

**Created:** 2026-03-18
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §Visual Intelligence Pipeline, CVE_Documentation_V2 §9.5, §10.2
**Skill Implementation:** `skills/visuals/image_analysis_wrapper.py`, `skills/visuals/visual_validation_agent.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` — FR-VIS-04 definition (line 1022)
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V2.md` — §9.5 AGSS Scoring, §10.2 Character Drift Detection, §9 Visual Validation Agent Architecture
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V3.md` — §9 Updated Validation Gates V-04 within full gate sequence
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Physiological State Specification Language.md` — Bio-aesthetic scoring, corrugator/zygomaticus measurement for imperfection calibration
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Visual Style Psychology in Coaching.md` — Authenticity thresholds, uncanny valley proximity measurement
- `d:\Work\The Conscious Coaching Factory\docs\architecture\FR50_Sovereign_Image_Rule_Tech_Spec.md` — Reference template

---

## 2. Overview

### Problem Statement
RunningHub AI-generated images can fail in three distinct ways: (1) **Artificial sincerity** — the image looks "too perfect," triggering the Uncanny Valley response where viewers unconsciously detect synthetic origins and disengage; (2) **Anatomical inaccuracy** — distorted expressions, impossible facial proportions, or plastic-textured skin that breaks immersion; (3) **Character drift** — the generated character's facial features diverge from the canonical reference image, destroying visual continuity across compositions. Each failure type requires a different detection mechanism and a different remediation strategy. Without a structured validation pipeline, invalid images reach the Canva App and eventually the coach's audience — damaging brand credibility.

### Solution
FR-VIS-04 establishes the Visual Validation Agent, operating as Gate V-04 in the quality gate sequence. For every RunningHub output (Tier 3 and Tier 4 slides), the agent runs three checks using `image_analysis_wrapper.py`: AGSS scoring, Authenticity Feature Verification, and Character Drift Detection. Each check has a defined threshold, a defined remediation action on failure, and a maximum retry count before escalation.

### Scope
**In scope:**
- AGSS (AI-Generated Sincerity Score) computation and minimum 6.5/10 threshold.
- Three mandatory authenticity binary checks (expression naturalness, facial proportion, skin texture).
- Character drift detection against DEP-VIS-004 canonical references.
- Remediation logic: prompt revision, strength adjustment, PENDING_HUMAN_REVIEW escalation.

**Out of scope:**
- Pre-generation validation (handled by Gates V-00 through V-03).
- Canva App composition assembly (handled by FR-VIS-05).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-VIS-004` | Brand Character Reference Archive | REFERENCE — Canonical faces for drift comparison. |
| `DEP-ENG-041` | Receipt Chain Guard | AUDIT — All validation scores are hashed and recorded. |
| `FR-VIS-03` | PSSL Prompt Compilation | UPSTREAM — Paradoxe generated the image; on failure, Paradoxe revises the prompt. |
| `FR-VIS-05` | Canvas Composition & Delivery | DOWNSTREAM — Only validated images are delivered to the Canva App. |
| `image_analysis_wrapper.py` | Image Analysis Tool | TOOL — Python wrapper for LLM Vision API calls that perform AGSS, authenticity, and drift scoring. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Applied |
|---|---|---|---|
| **Visual Style Psychology in Coaching** | CCP Research Lab | 2026 | The Uncanny Valley in coaching visual content is measured via the AGSS — a composite score of feature distance from the training distribution center. Images scoring <6.5 fall into the "uncomfortable synthetic" zone where viewers consciously or unconsciously detect the artificial origin. The 6.5 threshold was calibrated against dwell time data: images scoring ≥6.5 produce dwell times statistically indistinguishable from real photographs (p > 0.05), while images scoring <6.5 show a 28% dwell time reduction. |
| **Physiological State Specification Language** | CCP Research Lab | 2026 | The imperfection specification in Paradoxe's prompts (FR-VIS-03) is calibrated to maximize AGSS scores. The bio-aesthetic evidence base shows that micro-asymmetries of 0.5-1.5% in facial features produce the highest AGSS scores (7.2-8.5 range) because human faces are naturally asymmetric. Perfect symmetry scores lower (5.5-6.5) because the visual processing system detects the unnatural regularity. On AGSS failure, the remediation strategy enhances the imperfection specification — adding more specific micro-flaw instructions. |

### Technical Decisions
1. **LLM Vision for AGSS:** The AGSS is computed via an LLM Vision API call (not a custom ML model) using a structured prompt that instructs the vision model to evaluate sincerity, naturalness, and feature consistency. This avoids the need for a custom training pipeline while providing sufficiently reliable scoring for the pipeline's quality threshold.
2. **One Retry per Failure Type:** Each check type gets exactly one automated remediation attempt. On AGSS failure: enhanced imperfection spec. On authenticity failure: enhanced imperfection spec. On character drift: increased reference strength (0.85 → 0.95). A second failure of any type on the same slide → PENDING_HUMAN_REVIEW. This limits RunningHub API consumption while providing a meaningful remediation attempt.
3. **Slide-Level Independence:** Each slide's validation is independent. Slide 3 failing validation does not halt slides 1, 2, 4, 5, 6, 7. Failed slides are flagged individually, and the composition is delivered with placeholders in flagged slots.

---

## 4. Implementation Plan

### Stage 1: AGSS Scoring
*Agent:* Visual Validation Agent (`image_analysis_wrapper.py`)
*Inputs:* RunningHub generated image (URL or binary), VCB slide specification.
*Outputs:* `agss_score` (float 0.0-10.0), `agss_detail` (component breakdown).
*Failure Condition:* Score < 6.5 → trigger remediation.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**AGSS Component Breakdown:**
- **Lighting Naturalism** (weight 0.25): Does the lighting in the image match natural physics? Are shadows consistent with a single or defined light source? Score 1-10.
- **Texture Authenticity** (weight 0.25): Do surfaces (skin, fabric, wood, metal) have believable texture at the pixel level? Or do they show the characteristic "AI smoothing" artifact? Score 1-10.
- **Compositional Coherence** (weight 0.25): Do objects in the scene maintain consistent scale, perspective, and spatial relationships? Are there floating elements or impossible geometry? Score 1-10.
- **Emotional Believability** (weight 0.25): Does the subject's expression, posture, and environmental interaction feel natural and spontaneous rather than posed or procedurally generated? Score 1-10.

**Composite AGSS = weighted average of all 4 components, scaled to 0-10.**

### Stage 2: Authenticity Feature Verification
*Agent:* Visual Validation Agent (`image_analysis_wrapper.py`)
*Inputs:* Same generated image.
*Outputs:* Three binary PASS/FAIL checks.
*Failure Condition:* Any single check fails → trigger remediation.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Three Mandatory Checks:**

| Check | Assessment Criteria | PASS | FAIL |
|---|---|---|---|
| Expression Naturalness | Micro-expression coherence: do the eyes, mouth, brow, and cheek muscles form a physiologically possible expression? Do the eyes and mouth express the same emotion? | All facial muscles coherent | Mixed signals (smiling mouth + sad eyes) or impossible micro-expression |
| Facial Proportion | Anatomical accuracy: eye spacing, nose-to-mouth ratio, ear position, jawline symmetry within natural human variation (2-5% asymmetry acceptable) | Within natural variation | Beyond natural variation (AI distortion artifacts) |
| Skin Texture | Pore-level detail consistency: are there visible pores, slight color variations, natural sheen patterns? Or is the skin uniformly smooth with the "airbrush" artifact? | Visible natural texture | Uniform smoothness or plastic-like surface |

### Stage 3: Character Drift Detection
*Agent:* Visual Validation Agent (`image_analysis_wrapper.py`)
*Inputs:* Generated image, canonical reference image from DEP-VIS-004.
*Outputs:* `drift_score` (0.0 = identical, 1.0 = completely different), `drift_assessment`.
*Failure Condition:* `drift_score > 0.30` (more than 30% feature deviation from reference) → trigger remediation.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Only runs for slides that used character reference images (Tier 3 with DEP-VIS-004 references).
2. Compares the generated face against the canonical reference using the LLM Vision API.
3. Evaluates: facial structure similarity, skin tone match, hair texture/style match, distinguishing feature preservation.
4. Outputs a `drift_score` — 0.0 means the character is perfectly preserved; 1.0 means the generated face bears no resemblance.
5. Threshold: `drift_score ≤ 0.30` = PASS. `drift_score > 0.30` = FAIL.

### Stage 4: Remediation & Escalation
*Agent:* Visual Validation Agent + Paradoxe (for prompt revision)
*Inputs:* Failure type (AGSS, Authenticity, or Drift), failure details, retry count.
*Outputs:* Revised image (on successful retry) or `PENDING_HUMAN_REVIEW` flag.
*Failure Condition:* Second failure of any type → escalation.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Remediation Rules:**

| Failure Type | First Remediation | Second Failure |
|---|---|---|
| AGSS < 6.5 | Paradoxe revises prompt with enhanced imperfection specification (increased micro-flaw detail, added environmental imperfections) | Slide flagged `PENDING_HUMAN_REVIEW`, operator alerted |
| Authenticity check FAIL | Paradoxe revises prompt with explicit correction for the failed check (e.g., "ensure micro-expression coherence between eyes and mouth") | Slide flagged `PENDING_HUMAN_REVIEW`, operator alerted |
| Character drift > 0.30 | Paradoxe resubmits with `reference_image_strength: 0.95` (increased from 0.85) | Slide flagged `PENDING_HUMAN_REVIEW`, operator alerted |

---

## 5. Primary Output Schema

### Schema Name: `Visual_Validation_Result.json`

```json
{
  "validation_id": "VVR-JP-20260318-012-S00",
  "vcb_id": "VCB-JP-20260318-012",
  "slide_index": 0,
  "image_url": "https://r2.ccf-assets.com/generated/rh-task-a7b3c9-output.png",
  "agss": {
    "composite_score": 7.8,
    "lighting_naturalism": 8.2,
    "texture_authenticity": 7.5,
    "compositional_coherence": 7.9,
    "emotional_believability": 7.6,
    "threshold": 6.5,
    "result": "PASS"
  },
  "authenticity": {
    "expression_naturalness": "PASS",
    "facial_proportion": "PASS",
    "skin_texture": "PASS",
    "overall_result": "PASS"
  },
  "character_drift": {
    "reference_image_used": true,
    "reference_character_id": "CHAR-JP-PROTAGONIST-001",
    "drift_score": 0.18,
    "threshold": 0.30,
    "result": "PASS"
  },
  "overall_verdict": "VALIDATED",
  "retry_count": 0,
  "receipt_chain_block": "RCB-VVR-20260318-012-S00",
  "timestamp_utc": "2026-03-18T01:40:00Z"
}
```

---

## 6. Backward Compatibility Fallback

If `image_analysis_wrapper.py` is unavailable (LLM Vision API quota exceeded, service outage):
1. The validation agent logs `VALIDATION_SERVICE_UNAVAILABLE`.
2. All generated images are flagged `PENDING_HUMAN_REVIEW` — they are not auto-approved.
3. The composition is delivered to the Canva App with all AI-generated slots requiring manual operator approval.
4. The validation agent does NOT skip validation — there is no "assume valid" path.

---

## 7. Tasks

- [ ] **Task 1:** Write `image_analysis_wrapper.py` — the Python tool that calls the LLM Vision API with structured AGSS, authenticity, and drift prompts.
- [ ] **Task 2:** Write `visual_validation_agent.py` — the orchestrator that runs all 3 checks per slide, handles remediation logic, and manages retries.
- [ ] **Task 3:** Implement the AGSS scoring prompt — structured LLM Vision prompt with 4 component scores and weighted composite calculation.
- [ ] **Task 4:** Implement the 3 authenticity binary check prompts — each with clear PASS/FAIL criteria for the LLM Vision API.
- [ ] **Task 5:** Implement character drift detection — LLM Vision comparison between generated image and DEP-VIS-004 canonical reference with 0-1.0 drift scoring.
- [ ] **Task 6:** Implement the remediation pipeline — enhanced imperfection spec for AGSS/authenticity failures, reference strength increase for drift failures.
- [ ] **Task 7:** Implement PENDING_HUMAN_REVIEW escalation on second failure — operator notification with full validation history.
- [ ] **Task 8:** Integrate with Receipt Chain Guard (DEP-ENG-041).

---

## 8. Acceptance Criteria

- [ ] **AC1 (AGSS Pass):** Submit a generated image with natural lighting, believable textures, coherent composition. Assert AGSS ≥ 6.5 and overall verdict VALIDATED. *Failure Example:* A high-quality image is rejected because the AGSS prompt is miscalibrated and scores all AI images below threshold.
- [ ] **AC2 (AGSS Fail → Remediation → Pass):** Submit an image scoring AGSS 5.8. Assert remediation triggers enhanced imperfection prompt. Submit the regenerated image (scoring 7.2). Assert VALIDATED. *Failure Example:* Paradoxe re-sends the same prompt without modification, producing another 5.8.
- [ ] **AC3 (Authenticity Fail — Expression):** Submit an image where the subject has smiling mouth but sad eyes (micro-expression incoherence). Assert Expression Naturalness check fails. *Failure Example:* The check passes because the LLM only evaluates "is the person smiling?" without checking eye-mouth coherence.
- [ ] **AC4 (Character Drift — Remediation):** Submit an image with drift_score 0.42 against the canonical reference. Assert remediation increases reference_image_strength to 0.95. Submit the regenerated image with drift_score 0.22. Assert PASS. *Failure Example:* Remediation doesn't adjust reference strength, producing another drifted image.
- [ ] **AC5 (Second Failure Escalation):** Submit an image that fails AGSS twice (both original and regenerated). Assert the slide is flagged PENDING_HUMAN_REVIEW and the operator notification contains both validation results. *Failure Example:* The validation agent attempts infinite retries, consuming RunningHub quota.
- [ ] **AC6 (Slide Independence):** Submit a 7-slide carousel. Slides 0, 1, 3, 4, 6 pass validation. Slide 2 fails AGSS. Slide 5 fails drift. Assert slides 2 and 5 are flagged individually while slides 0, 1, 3, 4, 6 are VALIDATED. *Failure Example:* The entire batch is flagged because two slides failed.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| DEP-VIS-004 (Brand Character Reference Archive) | Internal | REFERENCE for character drift comparison. |
| DEP-ENG-041 (Receipt Chain Guard) | Internal | AUDIT. |
| FR-VIS-03 (PSSL Prompt Compilation) | Internal | UPSTREAM — images generated by Paradoxe's prompts; FEEDBACK — Paradoxe revises on failure. |
| FR-VIS-05 (Canvas Composition) | Internal | DOWNSTREAM — only validated images delivered to Canva App. |
| LLM Vision API | External | AGSS scoring, authenticity checks, drift detection. |
| RunningHub API | External | Regeneration on failure. |

---

## 10. Testing Strategy

### Unit Tests
- **AGSS Prompt Structure:** Assert the LLM Vision prompt requests all 4 component scores and a composite. Assert the weighted average calculation is correct.
- **Drift Score Calibration:** Provide identical images → drift_score 0.0. Provide visually similar images → drift_score 0.1-0.3. Provide dissimilar images → drift_score > 0.5.

### Integration Tests
- **Full Validation Flow:** Submit a RunningHub output through all 3 checks. Assert validation results contain all scores. Assert Receipt Chain contains the validation hash.
- **Remediation Flow:** Submit a failing image. Assert Paradoxe regenerates. Assert the regenerated image is re-validated.

### Safety Tests (ADR-01 Quarantine Security)
- **Image Payload Injection:** Submit a malformed image file (e.g., a renamed HTML file). Assert `image_analysis_wrapper.py` detects the invalid format and rejects with `INVALID_IMAGE_FORMAT`.
