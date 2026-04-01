# Tech-Spec: FR-CA11-06 — Voice Note → Course Material Pipeline

**Created:** 2026-03-24
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / PRD Update v2.0 — Capability Area 11)
**Architecture Reference:** PRD-Update-CA11 §4.2
**Skill Implementation:** `skills/strategy/voice-to-lesson/SKILL.md`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` (FR2 Sacred Audio, FR3 Voice DNA)
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd-update-CA11-quad-platform.md`

---

## 2. Overview

### Problem Statement
Coaches have thousands of ideas that never become structured content. The friction is the *gap between thinking and teaching* — a coach can explain a concept in 90 seconds via voice note, but turning that into a formatted lesson with visual aids takes 2-3 hours. This transforms coaching expertise from an abundant asset into a bottleneck.

### Solution
FR-CA11-06 converts a coach's Telegram voice note (prefixed with `/lesson`) into a **formatted lesson page** in AFFiNE with an **auto-generated Excalidraw concept diagram**. The pipeline: Whisper transcription → Voice DNA-consistent lesson structuring by `Gabrielle` → Excalidraw concept diagram by `Benjamin` → AFFiNE Content Library push → learning path tagging. The coach's barrier to creating educational content drops to 90 seconds of talking.

### Scope
**In scope:**
- `/lesson` Telegram bot command handler.
- Whisper transcription of voice note.
- Lesson structuring (title, key takeaways, detailed explanation, practical exercise).
- Excalidraw concept diagram auto-generation.
- AFFiNE Content Library push and learning path tagging.

**Out of scope:**
- Session recordings (FR-CA11-05 — different input, different agent).
- Course video rendering (FR-CA11-12 — visual production is separate).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| FR2 (Sacred Audio) | Whisper Pipeline | REUSED — Same transcription infrastructure. |
| `DEP-ENG-003` | Voice DNA (Positive Space) | SOURCE — Lesson tone must match coach's authenticated identity. |
| `Gabrielle` (Learning Path Agent) | Content Categorizer | AGENT — Tags the lesson and assigns it to a learning journey. |
| `Benjamin` (Excalidraw Composer) | Visual Pipeline | AGENT — Generates concept diagram from lesson topics. |

### Technical Decisions
1. **Voice DNA Enforcement on Lesson Text:** The structured lesson uses the coach's Voice DNA (DEP-ENG-003) for tone consistency — the lesson reads like the coach, not like an AI rewrite. `Gabrielle` applies the `voice-separation-adapter` during lesson structuring.
2. **Concept Diagram = Topic Hierarchy:** The Excalidraw diagram is a hierarchical tree showing the lesson's main concept → sub-concepts → practical applications. This visual aid helps clients understand the lesson structure at a glance.

---

## 4. Implementation Plan

### Stage 1: Telegram Command & Transcription
*Agent:* CBCS Bot Handler / Whisper Pipeline
*Inputs:* Voice note file from Telegram, `/lesson` command prefix.
*Outputs:* Raw transcript text.

**Steps:**
1. Coach sends voice note with `/lesson` command to Telegram bot.
2. Bot handler detects `/lesson` prefix, routes to lesson pipeline (not standard CBCS).
3. Whisper transcription produces raw text.

### Stage 2: Lesson Structuring
*Agent:* `Gabrielle` (Learning Path Agent)
*Inputs:* Raw transcript, `coach_soul.json` (DEP-ENG-003).
*Outputs:* Structured lesson JSON.

**Steps:**
1. Parse transcript into logical segments.
2. Apply lesson template: Title (derived from central topic), Key Takeaways (3-5 bullet points), Detailed Explanation (structured prose maintaining Voice DNA), Practical Exercise (Implementation Intention format from FR-CBCS-09).
3. Validate lesson tone against Voice DNA using TTT enforcement (no drift > 15%).

### Stage 3: Concept Diagram & Delivery
*Agent:* `Benjamin` + `affine_sync.py`
*Inputs:* Lesson topic hierarchy.
*Outputs:* `.excalidraw` JSON, AFFiNE lesson page, `learning_path_registry` entry.

**Steps:**
1. `Benjamin` generates hierarchical concept diagram from lesson topics.
2. `affine_sync.py` creates lesson page in coach's AFFiNE Content Library.
3. `Gabrielle` tags the lesson in `learning_path_registry` (topic cluster, difficulty, program tag).
4. Coach receives Telegram confirmation: "Your lesson is ready in your Content Library! 📚"

---

## 5. Primary Output Schema

**Data Object:** Structured Lesson Output (`DEP-ENG-076` PROPOSED)

```json
{
  "lesson_id": "uuid-lesson-001",
  "asset_id": "JP-LESSON-20260324-001-TEXT",
  "coach_id": "uuid-coach-001",
  "title": "The Approval Trap: Why External Validation Destroys Inner Authority",
  "key_takeaways": [
    "External validation creates dependency, not confidence",
    "The approval-seeking pattern originates from childhood authority dynamics",
    "True confidence is an inside job that requires deliberate practice"
  ],
  "detailed_explanation_markdown": "## The Pattern Behind the Pattern\n...",
  "practical_exercise": {
    "implementation_intention": "When I notice myself seeking approval before making a decision, I will pause and ask: 'What do I actually want here?'",
    "duration": "5 minutes daily for 7 days"
  },
  "concept_diagram_url": "s3://JP/excalidraw/lesson_uuid-lesson-001_diagram.json",
  "learning_path_registry": {
    "topic_cluster": "external_validation",
    "difficulty_level": "developing",
    "content_type": "voice_lesson"
  }
}
```

---

## 6. Backward Compatibility Fallback
If lesson structuring fails, the raw transcript is still delivered to AFFiNE as an unstructured page with a "Raw Notes" tag. The coach can manually edit it. The concept diagram generation failure is non-blocking — the lesson page is created without the diagram, and the diagram generation is queued for retry.

---

## 7. Tasks

- [ ] **Task 1:** Add `/lesson` command handler to CBCS Telegram bot.
- [ ] **Task 2:** Write `voice-to-lesson` SKILL.md for `Gabrielle` (lesson structuring with Voice DNA enforcement).
- [ ] **Task 3:** Build concept diagram template for `Benjamin` (hierarchical tree, CCP branded colors).
- [ ] **Task 4:** Wire lesson output to `affine_sync.py` Content Library push.
- [ ] **Task 5:** Wire lesson output to `learning_path_builder.py` for automatic categorization.

---

## 8. Acceptance Criteria

- [ ] **AC1 (90-Second Lesson):** Record a 90-second voice note. Send with `/lesson`. Assert a structured lesson page appears in AFFiNE within 3 minutes.
- [ ] **AC2 (Voice DNA Consistency):** Compare lesson text against coach's Voice DNA. Assert TTT drift < 15%.
- [ ] **AC3 (Concept Diagram):** Assert the `.excalidraw` diagram contains nodes matching the lesson's key concepts.
- [ ] **AC4 (Learning Path Tagged):** Assert the lesson appears in `learning_path_registry` with correct topic cluster and difficulty level.
- [ ] **AC5 (Practical Exercise Format):** Assert every generated lesson includes an Implementation Intention formatted exercise.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR2 (Whisper Pipeline) | Internal | Transcription. |
| FR-CA11-04 (Learning Path Builder) | Internal | Categories and tags the lesson. |
| FR-CA11-02 (AFFiNE Sync) | Internal | Delivers to AFFiNE. |
| `DEP-ENG-003` (Voice DNA) | Internal | Tone enforcement. |

---

## 10. Testing Strategy

### Unit Tests
- **Lesson Structure Completeness:** Pass a known transcript. Assert output has all 4 sections (title, takeaways, explanation, exercise).

### Integration Tests
- **Full Pipeline:** Send `/lesson` voice note via test bot → assert transcription → structuring → diagram → AFFiNE delivery → learning path tagging all complete within 3 minutes.
