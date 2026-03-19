# FR-CBCS-10: Deep Disclosure Protocol — Tech Spec

**Created:** 2026-03-18
**Status:** Ready for Development
**Architecture Reference:** CCP_CBCS_CPSC_V3 §F10, PRD §FR-CBCS-10

---

## 1. Files Read
- `docs/prd/prd.md`
- `lab/CCP update/CCP_CBCS_CPSC_V3.docx.md`
- `lab/CVE + CPSC research papers/Disclosure, Attachment, and Conversion Architecture.md`

---

## 2. Overview

### Problem Statement
When NLP agents adopt a "Customer Service" or "Help Desk" persona (e.g., "How can I help you today?"), they permanently categorize the interaction as transactional. Clients will not disclose vulnerable psychological states to a transactional entity, stunting their progress on the Social Penetration Depth Gauge (FR-CBCS-02) and blocking all downstream conversions.

### Solution
The Deep Disclosure Protocol enforces the CASA (Computers Are Social Actors) paradigm across the Daily Cycle conversational nodes. It actively screens AI-generated drafts to ensure they use human-like first-person singular pronouns, avoid robotic qualifiers, and utilize specific conversational modes (like Active-Constructive Responding) based on the exact emotional valence of the client's input.

### Scope
**In scope:**
- The `casa-linguistic-validator` Pi Extension.
- The 3-Mode interaction state machine routing.
- The `CASA Linguistic Gate` validating AI drafts.
- Storage schema for `disclosure_interaction_logs`.

**Out of scope:**
- LLM prompt generation engine (handled by core system framework).
- TII calculation (handled by FR-CBCS-07).

---

## 3. Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Produced By | Consumed By |
|---|---|---|---|---|
| `disclosure_interaction_logs` | Audit SQL Table | Tracks CASA execution | FR-CBCS-10 | FR-CBCS-14 |
| `PROPOSED: DEP-ENG-065` | CASA Linguistic Verdict | Draft deployment guard | FR-CBCS-10 | CBCS Replies |

### Academic Grounding
- **Research Paper:** *The Media Equation: How People Treat Computers, Television, and New Media Like Real People and Places* (Reeves & Nass, 1996) + *Active-Constructive Responding* (Gable et al., 2004).
- **Mechanism:** The human brain applies social rules to computers automatically if the computer provides social cues. By enforcing "I" statements and removing subservient AI language, the client's brain categorizes the bot as a peer/coach, unlocking deep self-disclosure routines.

### Technical Decisions
- **Regex Blocking:** It is notoriously difficult to prevent LLMs from acting like AI assistants. The only reliable architectural pattern is a hard regex-parse post-generation that rewinds the generation upon failure.
- **Single Question Rule:** A known trap of AI therapists is ending every message with a question, creating a relentless interrogation loop. The protocol enforces exactly zero or one reflective question per payload.

---

## 4. Implementation Plan

### Stage 1: Interaction Mode Routing
- **Variable Resolution Rule (Interaction Mode):** Before the LLM drafts a reply, a Python pre-processor evaluates the client's last message to set the `interaction_mode` string Enum driving the prompt instructions:
  - **"VULNERABLE_RECEPTION"**: Evaluates `True` IF the client's input `liwc_scores.negative_emotion > 0.05`. *Prompt Instruction:* "Validate the emotion using reflective listening. Do not offer solutions. Wait."
  - **"ELEVATED_CHALLENGE"**: Evaluates `True` IF `liwc_scores.cognitive_processes > 0.1` AND `social_penetration_depth_gauge.spt_stage >= 3`. *Prompt Instruction:* "Push back on a limiting belief logically. They are secure enough to handle it."
  - **"ACTIVE_CONSTRUCTIVE_RESPONDING"**: Evaluates `True` IF `liwc_scores.positive_emotion > 0.05`. *Prompt Instruction:* "Match their energy exactly. Ask them what part of their success made them the most proud."

### Stage 2: CASA Validation Extraction
- **Agent:** `casa-linguistic-validator` (Python text parser executing on LLM Draft output)
- **Inputs:** 
  - `draft_ai_reply` (DEP-ID: `DEP-ENG-053` — Produced By: FR53 / FR10 CBCS Generation Loop)
  - `interaction_mode` (DEP-ID: **Generated in Stage 1**)
- **Outputs:** `PROPOSED: DEP-ENG-065` (CASA Validation Verdict).
- **Failure Condition:** If the LLM generation times out, script cleanly aborts returning `False` without crashing the message queue bus.
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `client_id` + `casa_verdict` written to the system audit log validating the post-processing verification.

**Metrics Calculated via explicit parsing:**
- `first_person_singular_count`: `REGEX_COUNT(draft, \b(I|me|my|mine)\b)`.
- `robotic_qualifier_count`: `REGEX_COUNT(draft, \b(As an AI|I am here to help|Let me know if|assistant|virtual)\b)`.
- `reflective_question_count`: `REGEX_COUNT(draft, \b(\w+\s+)+\?$)`. (Counts terminal question marks).

### Stage 3: Quality Gate Extension
**Quality Gate:** **The CASA Linguistic Gate**
- **Triggered when:** The daily conversational engine drafts a reply to the client.
- **Exact Thresholds:**
  - `Condition_1`: `first_person_singular_count > 0`
  - `Condition_2`: `robotic_qualifier_count == 0`
  - `Condition_3`: `reflective_question_count <= 1`
- **Verdict - PASS:** All 3 conditions evaluate `True`. *Downstream Consequence:* Reply dispatched to Telegram Webhook.
- **Verdict - PROVISIONAL:** Conditions 1 and 2 are `True`, BUT `reflective_question_count > 1`. *Downstream Consequence:* The draft is human and sovereign, but it's slipping into "Interrogation Mode." The script intercepts and actively trims the draft string at the end of the first detected question mark matching sentence, then proceeds to dispatch.
- **Verdict - FAIL:** Condition 2 is `False` (`robotic_qualifier_count > 0`) OR Condition 1 is `False`. *Downstream Consequence:* Hard reject. Triggers `rewind_generation()`, returning the LLM a system penalty prompt: "You broke character. Never refer to yourself as an assistant. Rewrite."

### Stage 4: Resolution Rules for Output Schema
The `DisclosureInteractionLog` row is populated per transaction linking inputs to outputs:
- `interaction_id`: `uuid.uuid4()`.
- `client_id` / `coach_id`: Synchronous mapping.
- `interaction_mode`: Strict string Enum populated by Stage 1 mapping logic ("VULNERABLE_RECEPTION" | "ELEVATED_CHALLENGE" | "ACTIVE_CONSTRUCTIVE_RESPONDING").
- `casa_verdict`: "PASS" | "PROVISIONAL_TRIMMED" | "FAIL_REWRITE".
- `metrics_payload.fp_count`: Integer mapping directly to `first_person_singular_count`.
- `metrics_payload.robotic_count`: Integer mapping directly to `robotic_qualifier_count`.
- `metrics_payload.question_count`: Integer mapping directly to `reflective_question_count`.
- `final_dispatched_text`: The string actually sent to Telegram (may be shorter than original draft if `PROVISIONAL_TRIMMED`).
- `timestamp_utc`: `datetime.now(timezone.utc).isoformat()`.

---

## 5. Primary Output Schema

```typescript
type DisclosureInteractionLogRow = {
  interaction_id: string; // uuid4
  client_id: string; // uuid4
  coach_id: string; // uuid4 (ADR-01 boundary)
  interaction_mode: "VULNERABLE_RECEPTION" | "ELEVATED_CHALLENGE" | "ACTIVE_CONSTRUCTIVE_RESPONDING";
  casa_verdict: "PASS" | "PROVISIONAL_TRIMMED" | "FAIL_REWRITE";
  metrics_payload: {
    fp_count: number;
    robotic_count: number;
    question_count: number;
  };
  final_dispatched_text: string;
  timestamp_utc: string; // ISO8601
};
```

---

## 6. Backward Compatibility Fallback
For FR45 generic webhook outputs deployed outside of the main FR-CBCS interaction loop (like system billing alerts):
- The `CASA Linguistic Gate` is explicitly disabled for "Operational" message tags.
- The system will allow generic language for purely administrative prompts to save server tokens.

---

## 7. Tasks
- [ ] **Task 1: Pre-Processor Mode Logic** - Build `interaction_router.py` evaluating the client's latest LIWC scores against the 3 `interaction_mode` condition paths prior to LLM trigger.
- [ ] **Task 2: CASA Validator** - Develop `casa_validator.py` maintaining the blacklisted regex keywords for `Condition 2`.
- [ ] **Task 3: Provisional Trimmer Sequence** - Write the Python string manipulation function to execute `string.split('?')[0] + '?'` to enforce the single-question rule natively on PROVISIONAL states without requiring a costly LLM rewrite.

---

## 8. Acceptance Criteria
- [ ] **AC1 (Robotic Break Condition):** A drafted text reading "I understand. As an AI language model..." evaluates `robotic_qualifier_count = 1`. Gate MUST `FAIL` returning `casa_verdict = FAIL_REWRITE`. **Failure Example:** The LLM's safety tuning slips through the gate, permanently destroying the user's parasocial trust.
- [ ] **AC2 (Interrogation Trimming):** A drafted text reading "I hear you. Why did you do that? What else are you feeling?" evaluates `reflective_question_count = 2`. Gate MUST evaluate `PROVISIONAL_TRIMMED` and rewrite `final_dispatched_text` strictly deleting "What else are you feeling?". **Failure Example:** The bot spams the client with 4 questions in a single text, creating massive cognitive load.
- [ ] **AC3 (Mode Targeting):** A client message evaluating `positive_emotion = 0.08` hits the pre-processor. Script MUST assign Enum `ACTIVE_CONSTRUCTIVE_RESPONDING`. **Failure Example:** The system defaults to standard stoic response, failing to celebrate the client's win.
