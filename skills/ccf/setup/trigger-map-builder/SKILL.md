---
name: Trigger Map Builder
description: "🗺️ THE CARTOGRAPHER — Builds the coach's permanent trigger architecture from Emotional DNA. Maps trigger origins, PTG status, archetype affinities, and reconsolidation sensitivity."
session_id: ccf-trigger-map
phase: setup
ccp_layer: Memory (L2)
pi_extensions: [SoulResonance, TriggerFirst]
version: 1.0
inputs:
  - intelligence_library/emotional_dna.json (populated)
  - intelligence_library/coach_soul.json
  - raw/transcripts/ (interview transcripts)
outputs:
  - intelligence_library/trigger_map.json (populated)
depends_on: [emotional-dna-extraction]
---

# Trigger Map Builder — Permanent Fire Architecture

> **Version:** CCP v3.1 — Setup Phase (Genesis)
> **Purpose:** Construct the coach's trigger map — the permanent architecture of what they cannot stop responding to. This is not what the coach believes. It is what fires them. Built from Emotional DNA + interview corpus.

## SYSTEM MESSAGE

**Cognitive State** *(Mandate 1)*:
You are operating in archaeological mode. You are mapping structures that already exist in the coach's history and corpus — not constructing new ones. Your cognitive state is: **structural pattern recognition across temporal layers**. You are looking for the fires that were already burning before you arrived.

---

## SCIENTIFIC FOUNDATION

### Framework 1: Conway Self-Memory System / AKB Hierarchy (2005)
- **Application**: Classifying trigger origin by memory level
- **Key principle**: Autobiographical memory is organized in 3 levels — Lifetime Periods (broad chapters), General Events (clusters), Event-Specific Knowledge (sensory-perceptual records). Only ESK-level triggers contain the full appraisal cascade needed for authentic activation.
- **What we classify**: Each trigger's originating experience into its AKB level. ESK-level triggers are highest value.

### Framework 2: Tedeschi & Calhoun Post-Traumatic Growth (2004)
- **Application**: Assessing trigger resolution status
- **Key principle**: When a person successfully navigates profound adversity, the original neural encoding remains fully intact — a secondary "path out" network is superimposed over it (dual-layer encoding). Only resolved triggers produce dual-layer activation suitable for content. Unresolved triggers produce raw material without resolution signal.
- **PTG Classification**:
  - `resolved_dual_layer` → Coach can access BOTH the original pain AND the resolution. Content carries the full arc. **Highest value for content activation.**
  - `active_processing` → Partial resolution. Content has heat but incomplete resolution signal. **Use with caution — monitor emotional load.**
  - `raw_unresolved` → Live trauma. NOT suitable for content activation. **Flag and protect.**

### Framework 3: McAdams Narrative Identity Theory (2001)
- **Application**: Identifying narrative positioning and sequence type
- **Key principle**: People construct their identity through narrative — specifically through redemption sequences (bad → good) and contamination sequences (good → bad). The coach's dominant sequence type determines their natural content arc.
- **What we extract**: Redemption/contamination sequence type + narrative positioning (reluctant hero, whistleblower, reformed insider, outsider witness, survivor guide).

### Framework 4: Nader Memory Reconsolidation (2000)
- **Application**: Assessing trigger labilization potential
- **Key principle**: Retrieving an episodic memory destabilizes it — returning it to a labile state for ~6 hours. This requires prediction error (discrepancy between expectation and encounter). Triggers with high reconsolidation sensitivity produce the most authentic material when precisely activated.
- **What we assess**: How much prediction error is required to labilize each trigger's episodic trace.

### Framework 5: Haidt MFQ-2 / Moral Foundations Theory (2012/2023)
- **Application**: Mapping each trigger to its moral foundation
- **Key principle**: Every authentic trigger violates a specific moral foundation. The foundation mapping determines which categories of current events will activate this trigger — before any intelligence scanning occurs.

---

## PRE-GENERATION CONSTRAINTS (Mandate 3)

**Constraint A — Emotional DNA Dependency:**
This skill CANNOT run before `emotional_dna.json` is populated. V1-V6 from the Emotional DNA profile are required inputs — they provide the appraisal architecture that each trigger is mapped against.

**Constraint B — PTG Protection:**
Any trigger classified as `raw_unresolved` is IMMEDIATELY flagged and excluded from the activation pipeline. This is a hard safety gate. Unresolved trauma is not content material — it is a boundary the system must respect.

**Constraint C — Evidence-First Mapping:**
Every trigger must trace to specific passages in the interview corpus. A trigger without corpus evidence is a hypothesis, not a map entry. Hypotheses go in a `candidate_triggers` array, not in the primary `triggers` array.

**Constraint D — Minimum Resolution Signal:**
For a trigger to be classified as `resolved_dual_layer`, the corpus must contain BOTH: (a) passages describing the original pain/violation, AND (b) passages demonstrating the path out — evidence the coach has successfully navigated this territory. If only (a) exists, classify as `active_processing`.

---

## EXTRACTION PROTOCOL (I-R-E-V-C)

### INGEST

1. **Load** `emotional_dna.json` — verify extraction is complete
2. **Gate**: If `extraction_status.confidence` < 0.5 → WARN. Trigger map will be partial.
3. **Load** `coach_soul.json` — read existing identity data
4. **Load** all transcripts from `raw/transcripts/`
5. **Load** `trigger_map.json` template

### REASON

**Phase 1: Trigger Identification**

Using V4 (Norm Compatibility Threshold) and V6 (Moral Foundations Profile) from `emotional_dna.json`, search the corpus for trigger activation passages — moments where the coach shifts from intellectual discussion to activated response.

Identification markers:
- Shift in sentence length (compression under emotional arousal — Kensinger selective accuracy)
- Shift in pronoun usage (I/me increase — Pennebaker LIWC-22 authentic activation signal)
- Shift in verb tense (present-dominant — immediate engagement vs past-dominant rehearsal)
- Drop in hedging language (certainty increases)
- Increase in exclusive words (but, except, however — cognitive distinctions made in real time)

For each identified trigger passage:
1. Label the trigger (what is the violation/mechanism?)
2. Map to moral foundation from V6 profile
3. Record the activation keywords and mechanisms
4. Cite the specific passage

**Phase 2: Origin Classification (Conway AKB)**

For each trigger, search the corpus for the originating experience:

| AKB Level | Corpus Evidence | Classification |
|---|---|---|
| Event-Specific Knowledge | Coach describes a specific moment — date, place, sensory detail, who was present | ESK → **highest value** |
| General Events | Coach describes a pattern — "the clients I kept seeing get misled" | GE → medium value |
| Lifetime Periods | Coach describes a chapter — "my years in corporate" | LP → low value for activation |

If ESK evidence exists → record sensory anchors and temporal context.
If only GE/LP evidence exists → flag as candidate for deeper interview to surface ESK.

**Phase 3: PTG Assessment (Tedeschi & Calhoun)**

For each trigger, assess resolution status:

1. **Search for pain passages** — does the coach describe the original violation with emotional activation? (evidence of primary encoding intact)
2. **Search for resolution passages** — does the coach describe how they navigated through this? (evidence of secondary "path out" network)
3. **Classify**:
   - Both present → `resolved_dual_layer` ✅
   - Pain only → `active_processing` ⚠️
   - Recent/raw emotional language without analytical distance → `raw_unresolved` 🛑

**Phase 4: Narrative Identity (McAdams)**

For each trigger, identify:
- **Sequence type**: Does the coach tell this as redemption (I went through this → here's what I learned → here's how I help) or contamination (things were good → this happened → everything changed)?
- **Positioning**: How does the coach position themselves relative to this trigger?
  - Reluctant Hero: didn't want to speak up, but had to
  - Whistleblower: exposing what others won't say
  - Reformed Insider: was part of the problem, now fights it
  - Outsider Witness: observed the damage from outside
  - Survivor Guide: went through it, now maps the territory for others

**Phase 5: Reconsolidation Sensitivity (Nader)**

For each trigger, assess how much prediction error is needed to labilize the episodic trace:
- **Low threshold (1-3)**: Coach re-activates easily when topic is raised, even in generic terms
- **Medium threshold (4-6)**: Coach requires specific mechanism detail to shift from intellectual to activated
- **High threshold (7-10)**: Coach requires highly specific, sensory-detailed activation events to access ESK

Cross-validate against V1 (Trigger Specificity Threshold) from `emotional_dna.json` — these should correlate.

**Phase 6: Archetype Mapping**

For each trigger, map the emotional state it produces to the Stage 5 archetype table:
1. Identify dominant emotional state when trigger fires
2. Look up in `trigger_archetype_map` (pre-populated in template)
3. Check TTT compatibility: can this coach credibly occupy the temperature this archetype requires?
4. Set `coach_eligible` = true/false

### EMIT

Write populated `trigger_map.json`:
- Each trigger in `triggers[]` with all fields populated (or explicitly null with reason)
- `trigger_archetype_map.mappings[].coach_eligible` set based on TTT assessment
- `map_status.total_triggers_mapped` updated
- `map_status.confidence` calculated
- `activation_history` left empty (populated during weekly cycles)

### VALIDATE

- [ ] `emotional_dna.json` was loaded and verified before trigger extraction began
- [ ] Every trigger has ≥ 1 evidence passage from the corpus
- [ ] Every trigger has a moral foundation mapping consistent with V6 profile
- [ ] Every trigger has PTG status assessed
- [ ] NO `raw_unresolved` triggers are in the activation pipeline
- [ ] At least 2 triggers are classified `resolved_dual_layer` (minimum for viable content activation)
- [ ] Archetype compatibility checked against coach TTT ceiling
- [ ] Narrative identity positioning consistent across triggers (or explicitly noted as variable)

### CHECKPOINT

- Update `config.yaml`: `sessions.setup.trigger_map.status = "complete"`
- Update `coach_soul.json`: `extraction_pipeline_status.trigger_map_complete = true`
- Log: triggers mapped, PTG distribution, ESK vs GE vs LP counts, archetype eligibility summary
