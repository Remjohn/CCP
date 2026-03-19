# FR-CBCS-03: Personal Relevance Trigger — Tech Spec

**Created:** 2026-03-18
**Status:** Ready for Development
**Architecture Reference:** CCP_CBCS_CPSC_V3 §F3, PRD §FR-CBCS-03

---

## 1. Files Read
- `docs/prd/prd.md`
- `lab/CCP update/CCP_CBCS_CPSC_V3.docx.md`
- `lab/CCP update/Context about CCP updates.md`

---

## 2. Overview

### Problem Statement
Standard personalization targets behavioral history ("You missed your last 3 workouts"), which invokes peripheral heuristic processing and defensive reactions. Peripheral processing produces only temporary behavioral compliance rather than lasting attitude change.

### Solution
The Personal Relevance Trigger executes an Identity-First Architecture. It targets who the client *is* at their core. By referencing their specific cognitive protection patterns and identity markers, it activates the central route of the Elaboration Likelihood Model (ELM). This forces genuine cognitive engagement because the brain cannot dismiss an accurate identity statement without evaluation.

### Scope
**In scope:**
- Integration of Emotional DNA, coping mechanisms, moral foundations, and change talk into a unified client Identity Profile.
- Generation of the `Identity Profile JSON` per client via `identity-profile-builder`.
- Execution of the `central-route-trigger-validator` to reject behavioral-first messages.
- Enhancing FR54 (Promotional Asset Compiler) and FR53 (Conversion Sequence).

**Out of scope:**
- The actual creation of the brand assets (handled by FR54 Z-Pattern Flyers).
- Gathering raw Emotional DNA (handled upstream by Voice DNA framework).

---

## 3. Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Produced By | Consumed By |
|---|---|---|---|---|
| `PROPOSED: DEP-ENG-056` | Unified Identity Profile | Merged schema of E-DNA, Coping, Moral, Change Talk | FR-CBCS-03 | FR53, FR54 |
| `PROPOSED: DEP-ENG-057` | Identity-First Validation Gate | Rejects behavioral triggers | FR-CBCS-03 | Campaign Generators |

### Academic Grounding
- **Research Paper:** *The Elaboration Likelihood Model of Persuasion* (Petty & Cacioppo, 1986) + *Do Tailored Behavior Change Instructions Enhance Effectiveness?* (Kreuter & Strecher, 1996).
- **Mechanism:** Activating the central route requires the message to be perceived as intimately relevant to the self-concept. An identity statement bypasses behavioral defenses and forces deep elaboration, leading to lasting change.

### Technical Decisions
- **Synthesis:** `identity-profile-builder` continuously synthesizes disparate data streams into a single JSON profile securely cached for campaign use.
- **Strict Quality Gate:** The `central-route-trigger-validator` acts as a hard stop (Identity-First Trigger Gate). It analyzes draft copy and actively rejects any that relies on behavioral pattern recognition ("you have restarted this goal four times"). 

---

## 4. Implementation Plan

### Stage 1: Identity Profile Synthesis
- **Agent:** `identity-profile-builder` (Python synthesis tool)
- **Inputs:** 
  - `emotional_dna` (DEP-ID: `DEP-LIB-001` — Produced By: FR4 Emotional DNA Extraction)
  - `coping_mechanisms` (DEP-ID: `DEP-ENG-006` — Produced By: FR12 Core Schema Intake)
  - `moral_foundations` (DEP-ID: `DEP-ENG-034` — Produced By: FR12 Core Schema Intake)
  - `change_talk_archive` (DEP-ID: `change_talk_archive` — Produced By: FR-CBCS-01)
- **Outputs:** `PROPOSED: DEP-ENG-056` (Unified Identity Profile JSON) mapped to Context Premise L3.
- **Failure Condition:** If a client is missing `emotional_dna`, the synthesis skips that component, throwing a handled `MissingDataWarning`. Generates a partial but identity-focused profile defaulting to generic archetype strings.
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `client_id` + `last_synthesized` ISO8601 string written to the audit log at the completion of Stage 1.

### Stage 2: Variable Resolution Rules (Profile Generation)
The following rules determine exactly how the fields for `emotional_architecture` and `core_identity_statement` are computed during Stage 1:
- **`primary_driver`**: Evaluates `emotional_dna.dominant_theme`. IF Null, assigns enum `"Autonomy"`.
- **`defense_mechanism`**: Evaluates `coping_mechanisms.primary_defense`. IF `Intellectualization`, maps to string `"Retreats into logic to avoid vulnerable processing"`. IF `Avoidance`, maps to `"Deflects attention away from the core emotional wound"`. IF Null, assigns `"General Resistance"`.
- **`core_identity_statement`**: Synthesizes a fixed template string: `"Someone who values {moral_foundations.primary} but struggles with {defense_mechanism} when their {primary_driver} is threatened."`

### Stage 3: Trigger Generation & Validation
- **Agent:** `IdentityTargeting` (Pi Extension interacting with `central-route-trigger-validator`)
- **Inputs:** `draft_campaign_message_text`, `PROPOSED: DEP-ENG-056` (Unified Identity Profile)
- **Outputs:** `PROPOSED: DEP-ENG-057` (Validation Verdict: PASS / PROVISIONAL / FAIL).

**Quality Gate:** **Identity-First Trigger Gate**
- **Triggered when:** Campaign Generator drafts behavioral copy meant for the client.
- **Exact Thresholds:**
  - `behavioral_match_count` = `REGEX_COUNT(draft_campaign_message_text, (missed|stopped|failed to|didn't do|last time you|habit tracking|days in a row))`
  - `identity_match_count` = `REGEX_COUNT(draft_campaign_message_text, (who you are|identity|values|belief|the kind of person))`
- **Verdict - PASS:** `behavioral_match_count == 0` AND `identity_match_count >= 1`. *Downstream Consequence:* Trigger permitted into the active campaign queue.
- **Verdict - PROVISIONAL:** `behavioral_match_count > 0` AND `identity_match_count >= 1`. *Downstream Consequence:* Draft contains a mixed message (behavioral framing cushioned by identity). Script queue halts delivery and pushes to `operator_review_queue` UI for manual human clearance, preventing automatic bad sends.
- **Verdict - FAIL:** `behavioral_match_count > 0` AND `identity_match_count == 0`. *Downstream Consequence:* Trigger strictly rejected. System executes a `rewind_generation()` callback to the LLM agent, forcing it to consume the explicit rewrite instruction parsing the specific failed tokens.

### Stage 4: Resolution Rules for Output Schema
Every field in the `UnifiedIdentityProfile` and `IdentityTargetingVerdict` schema is populated via the exact logic below:
- `client_id`: Passed synchronously from input context.
- `coach_id`: Extracted via database relationship mapping.
- `core_identity_statement`: Populated by the Stage 2 string template `f"Someone who values..."`.
- `emotional_architecture.primary_driver`: Assigned via Stage 2 logic evaluating `DEP-LIB-001`.
- `emotional_architecture.defense_mechanism`: Assigned via Stage 2 logic mapping `DEP-ENG-006`.
- `highest_intensity_change_talk`: SQL query `SELECT MAX(liwc_intensity_score) FROM change_talk_archive WHERE client_id = target`.
- `last_synthesized`: UTC ISO8601 timestamp at function conclusion.
- `isValid`: Boolean. Evaluates `True` ONLY if Gate = PASS. Evaluates `False` for FAIL or PROVISIONAL.
- `rewrite_instruction`: String pushing array of explicit failing conditions: `f"Remove behavioral markers: {rejected_behavioral_phrases}. Focus on identity trait: {primary_driver}"`. Null if `isValid` == True.
- `rejected_behavioral_phrases`: Array populated directly by the regex capture groups from `behavioral_match_count`.

---

## 5. Primary Output Schema

```typescript
type UnifiedIdentityProfile = {
  client_id: string; // uuid4
  coach_id: string; // uuid4 (ADR-01 boundary)
  core_identity_statement: string; // Template resolution
  emotional_architecture: {
    primary_driver: string;
    defense_mechanism: string;
  };
  highest_intensity_change_talk: string; // Max score string
  last_synthesized: string; // ISO8601
};

type IdentityTargetingVerdict = {
  isValid: boolean; // True ONLY if PASS
  rewrite_instruction: string | null; // Null if isValid True
  rejected_behavioral_phrases: string[]; // Regex capture groups
};
```

---

## 6. Backward Compatibility Fallback
For clients with genuinely insufficient contextual upstream strings to form an identity statement:
- The system will use the highest intensity item available (e.g., basic `Change Talk`), dropping the template `core_identity_statement` back to `"Someone aiming for [Change_Talk_Target]"`.
- The `Identity-First Trigger Gate` will continue to aggressively flag and enforce the `behavioral_match_count == 0` rule, ensuring a baseline "No Behavioral Shaming / Guilt-tripping" safety constraint even if deep identity profiling fails upstream.

---

## 7. Tasks
- [ ] **Task 1: Profile Synthesizer Regex** - Write the `identity_profile_synthesizer.py` mapping the precise variable resolution logic linking `DEP-ENG-006` to specific defense mechanism phrasing.
- [ ] **Task 2: Identity Context Storage** - Embed the resulting JSON string safely into the `Context Premise L3` Supabase schema structure.
- [ ] **Task 3: Validation Gate Extension** - Implement `central_route_validator.py` executing the dual regex count arrays (`behavioral_match_count` vs `identity_match_count`) to route PASS/FAIL/PROVISIONAL states.

---

## 8. Acceptance Criteria
- [ ] **AC1 (Central Route Validation Logic):** Draft copy saying "You've missed 3 Journal entries" evaluates `behavioral_match_count = 1`. Returning a `FAIL` verdict and `isValid: false`, along with `rewrite_instruction` pointing to "missed 3". **Failure Example:** The validator evaluates it to `PROVISIONAL` due to failing regex bounds, letting it pass to human review instead of automatic rejection.
- [ ] **AC2 (Synthesis Resilience & Enum mapping):** A client with `coping_mechanisms = Null` MUST still successfully generate a `Unified Identity Profile`, assigning the fallback enum `"General Resistance"` to `defense_mechanism`. **Failure Example:** Synthesis crashes throwing a `KeyError` blocking campaign generation.
- [ ] **AC3 (Loop Prevention / ADR-01 Constraints):** The operator queries the schema for `Client B` while authenticated as `Coach A`. Execution MUST enforce PostgreSQL RLS `auth.uid()` failing explicitly returning `0` rows. **Failure Example:** Application layer filtering bypassed, leaking another coach's identity profiles.

---

## 9. Dependencies
| Dependency | Type | Notes |
|---|---|---|
| FR4 & FR12 | Internal Upstream | Source of `emotional_dna`, `coping_mechanisms`, and `moral_foundations` |
| FR-CBCS-01 Change Talk | Internal Upstream | Source of `highest_intensity_change_talk` |
| FR54 (Promotional Assets) | Internal Downstream | Depends upon `PROPOSED: DEP-ENG-057` Verdict |

---

## 10. Testing Strategy

### Unit Testing
- Execute `central_route_validator.py` against 20 string arrays containing explicitly banned phrases. Target: `behavioral_match_count > 0` calculating 100% REJECT constraint (`isValid == False`).
- Execute Stage 2 Enum Resolution mapping dicts: Map `Intellectualization` -> `"Retreats into logic to avoid vulnerable processing"`. Assert string matches perfectly.

### Integration Testing
- Request a profile synthesis for a mock client spanning across FR1, FR18, and `DEP-LIB-001`. Ensure the JSON payload resolves `core_identity_statement` matching the dynamic f-string template exact word count.

### Safety Testing
- Inject `null` values concurrently into `moral_foundations`, `emotional_dna`, and `coping_mechanisms`. Validate `MissingDataWarning` fires safely, substituting all 3 fallback schema strings, allowing the script to return `200 OK` rather than throwing a `500 Server Error`.
