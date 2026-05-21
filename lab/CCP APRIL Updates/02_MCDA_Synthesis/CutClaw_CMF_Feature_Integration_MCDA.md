# MCDA: CutClaw feature integration into CMF Pipeline

> **Session:** 2026-04-15 | **Context:** Evaluation of the GVCLab/CutClaw automated video editing architecture for potential feature cherry-picking into the Conscious Coaching Factory (CCF) CMF Pipeline.

## 1. Executive Summary

CutClaw demonstrates a highly capable approach to long-form video editing using a Screenwriter-Editor-Reviewer loop based on music synchronization and visual captions. 

While the CMF pipeline's current architecture (Builder → Assembler → Critic) with Voice DNA LoRAs and strict 8-gate SG validation is **far superior for coach-specific psychological routing and dialogue**, CutClaw excels in **signal-driven asset manipulation**. We can cherry-pick three specific features to massively upgrade the CMF's visual engagement and automation efficiency without disrupting our existing cognitive reasoning models.

---

## 2. Feature Evaluation Matrix (MCDA)

We analyzed 4 core features of CutClaw against the CMF Pipeline using the Multi-Criteria Decision Analysis framework.

### Feature 1: Music-Aware Synchronization (The "Beat-Sync Cut")
**CutClaw Approach:** Uses ASR alongside music-structure parsing (extracting downbeat, pitch, and mel_energy) to force video cuts and transitions to snap to musical cues rather than arbitrary timestamps.
**Current CMF Capability:** Our `layered_questions_scene_builder.runtime.json` controls tension and unpredictability, but Remotion manifest transitions are mathematically timed to dialogue text (duration), not underlying audio energy spikes.
**Integration Value:** **P0 (Critical Upgrade)**
- **Why we need it:** CMF relies heavily on Master Effects (`EFFECT-M-04 Punch-In`, `EFFECT-A-05 Impact Hit`). If these effects snap precisely to the audio downbeat rather than just the dialogue start, the dopamine hit of the edit increases exponentially.
- **How to integrate:** Add an Audio Parser step to the `manifest-assembler` (SKILL-VID-006). Extract the beat array, and apply a "snap-to-nearest-downbeat" constraint to the Remotion frame maths when rendering phase transitions (e.g., Turn → Result).

### Feature 2: Smart Auto-Cropping (Content-Aware Framing)
**CutClaw Approach:** Uses visual parsing to identify core subjects in long-form landscape video and dynamically crops/tracks them to a 9:16 aspect ratio for shorts.
**Current CMF Capability:** The Virtual Director selects templates, but A-Roll and found E-Roll usually require manual framing adjustments to ensure the subject's face is dead center in the Telegram Mini App 9:16 viewport.
**Integration Value:** **P1 (High Upgrade)**
- **Why we need it:** To hit our 90% automation success rate for the Daily Mini App recordings, the pipeline must guarantee that coach/subject faces are never awkwardly cropped out of frame, especially when integrating mixed-aspect E-Roll.
- **How to integrate:** Introduce an active bounding-box tracker in the Remotion pipeline for the `talking_head_pattern_match` components, feeding the XY coordinates of the subject directly into the JSON manifest's crop attributes.

### Feature 3: One-Click Deconstruction (Hour-Long Visual Captioning)
**CutClaw Approach:** Uses LLVs (Large Language-Vision models like Gemini-3/Qwen3.5) to turn hours of raw video into heavily annotated, searchable "visual caption" databases (`shot_plan`).
**Current CMF Capability:** We use FR2-FR3 to extract Voice DNA from text/transcripts, but our visual hunting relies on keyword metadata rather than dense, framy-by-frame visual analysis.
**Integration Value:** **P2 (Deferred Upgrade)**
- **Why we need it:** Could revolutionize the E-roll `deep-researcher` variants. Instead of searching stock sites or databases by title, the agent could search a visual caption database for "coach exhibiting processing mood through body language."
- **How to integrate:** Use CutClaw's deconstruction method asynchronously on the archival footage database, turning all past coach videos into a vector-searchable visual library.

### Feature 4: Agentic Editing Loop (Screenwriter → Editor → Reviewer)
**CutClaw Approach:** Uses LLMs (Claude-4.5) to collaboratively generate a `shot_plan` and `shot_point` via an autonomous cycle.
**Current CMF Capability:** We use Builder → Assembler → Critic with 8 falsifiable SG Gates (SG-01 to SG-08), CRAL wiring, and Level 1-3 Anti-Draft checks executed by fine-tuned LoRAs.
**Integration Value:** **REJECTED (Downgrade)**
- **Why we reject it:** CutClaw's loop is highly generic. It solves for "make a cool montage." Our loop solves for "execute the Challenger archetype using a 5-phase Causal Construction sequence without violating the coach's negative space." Replacing our mathematically rigorous SKILL pipeline with CutClaw's generic agent loop would destroy the Voice DNA fidelity.

---

## 3. Implementation Plan: The "CutClaw Interventions"

We will NOT adopt CutClaw entirely. Instead, we will abstract their mathematical techniques into our CMF Editors.

### Step 1: Upgrade the Manifest Assembler (SKILL-VID-006)
- **Action:** Integrate librosa / Spotify pedal-board equivalent logic. When compiling the final Remotion manifest, output an array of `audio_downbeats_ms`.
- **Logic Rule:** If `master_effect` == `Impact`, shift the transition frame timestamp to `nearest(audio_downbeats_ms)`.

### Step 2: Empower the Editor Copilot (EC-13)
- **Action:** Add a new classification to the Edit Taxonomy in `cmf/skills/cmf/video/editor/SKILL.md`.
- **New Edit Class:** `EC-14 (AUDIO_SYNC_PATCH)`
- **Behavior:** The Copilot can now issue a natural language command: "Sync the B-Roll montage to the track energy" and output a patch that forces remotion transitions onto the beat grid.

### Step 3: Upgrade Daily Mini App Ingestion
- **Action:** Apply Content-Aware Auto-Cropping to all incoming WebRTC/Live daily video recordings.
- **Goal:** The coach just records. The server automatically tracks their face, centers it 9:16, trims silence, and injects it into the pipeline as clean A-Roll.

## 4. Conclusion
CutClaw is an impressive brute-force approach to montage making. **We will extract their music synchronization and auto-cropping algorithms to dramatically increase the "cinematic feel" and "zero-touch automation" of our outputs**, while fiercely protecting our SKILL-based cognitive architecture from their generic LLM loop.
