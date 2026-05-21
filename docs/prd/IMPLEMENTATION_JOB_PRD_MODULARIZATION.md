# IMPLEMENTATION JOB: Modular PRD Completion
# Status: READY FOR HANDOFF
# Priority: CRITICAL / HIGH-FIDELITY
# Target: Modularize PRD-02 through PRD-09

---

## 1. Objective

Complete the brownfield rebuild of the Conscious Coaching Platform (CCP) PRD suite. Transition the remaining legacy documentation into a deterministic, modular, Era 3-compliant architecture. Every module must be an agent-queryable source of truth that adheres to the **Invisible App Doctrine** and the **Self-Translation Principle**.

---

## 2. Mandatory Context (Load First)

Before writing any content, the incoming agent MUST load:

1. **The Router:** `docs/prd/modules/PRD_INDEX.md`
2. **The Discernment Map:** `docs/prd/evolution_timeline.md` (Mandatory Era 3 filter)
3. **The Governing SKILL:** `skills/prd/SKILL_PRD_Module_Writer.md` (Hard constraints & Templates)
4. **Current Progress:** Run `powershell -File "docs/prd/modules/count.ps1"` to see current status.

---

## 3. The Execution Protocol

Follow the `SKILL_PRD_Module_Writer.md` for every module. Key constraints:

- **Word Count:** 4,800 – 5,400 words per module. (Absolute floor/ceiling).
- **Compliance:** Zero violations of the 11 Evolution Timeline Rules (Rule 11: No JV/Joint Venture references, use Silent Referral).
- **Structure:** 10 sections following the mandated Section Template.
- **Tone:** Technical, dense, high-fidelity, non-generic.

---

## 4. Immediate Task: Finish PRD-08

`PRD_08_Conscious_Primitives.md` is currently at ~3,817 words. It is **UNDER** the floor.
- **Action:** Expand PRD-08 to ~5,100 words.
- **Focus:** Deepen the logic for **Coalition Formation**, **Anti-Centroid Law** enforcement in primitives, and the **Orchestration Dichotomy** (Deterministic vs Probabilistic layers).
- **Sources:** `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md`, `Primitive_Packets_and_Registry_Spec.md`.

---

## 5. Batch Sequence: PRDs 02 – 09

Execute the modules in the following order:

### Batch A: The Content & Media Engine
- **PRD-02: CCF Content Factory** (Focus: Trigger-First pipeline, Edge extraction)
- **PRD-03: CMF Media Factory** (Focus: Narrative → Cinematic → Sonic pipeline, Skia/SAM3 stack)

### Batch B: Experience & Skill Design
- **PRD-04: CVE Experience Design** (Focus: 4 Skill Surfaces, Voice-First Doctrine)
- **PRD-05: CBCS Law28** (Focus: 4-Engine Coaching, Biometric-gated progression)

### Batch C: Engagement & Conversion
- **PRD-06: Conscious Reactions** (Focus: Async modes, viral thresholds, Trivianar absorption)
- **PRD-07: V²WS Webinar** (Focus: Teaching-while-selling, YOLO/Interactive modes)

### Batch D: Commercialization
- **PRD-09: CPSC Silent Referral** (Focus: $29/$99 ladder, participation-driven loops)

---

## 6. Anti-Laziness Checklist

The job is not complete until:
- [ ] All 9 modules exist in `docs/prd/modules/`.
- [ ] Every module passes the word count check (4,800 - 5,400 words).
- [ ] No module contains "JV", "Trivianar" (standalone), or Era 1/2 pricing.
- [ ] The `PRD_INDEX.md` module registry word counts are updated to match reality.
- [ ] A final `powershell` count check is run and provided as a Completion Receipt.

---

## 7. Handover Note to Agent

You are an Architect. You are not a copywriter. Your job is to codify the *logic* of the system. Do not use fluff. If you are under the word count, you have missed a technical detail from the source documents. Go back to the `lab/CCP APRIL Updates/` directory and find the deeper architectural truth.

**Final Fatal Error Warning:** If you mention "Joint Venture" or "JV" as a current strategy, you have failed the Discernment Map. Use **Silent Referral**.
