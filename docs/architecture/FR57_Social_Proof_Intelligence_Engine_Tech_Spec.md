# FR57: Social Proof Intelligence Engine — Tech Spec

**Created:** 2026-03-18
**Status:** Ready for Development
**Architecture Reference:** CCP_CBCS_CPSC_V3 §FR57

---

## 1. Files Read
- `docs/prd/prd.md`
- `lab/CCP update/CCP_CBCS_CPSC_V3.docx.md`

---

## 2. Overview

### Problem Statement
Testimonials are typically displayed generically ("John made $100k!"). But if John is an advanced practitioner in Coping Position 5, and the reader is a distressed beginner in Coping Position 2, John's testimonial causes alienation, not inspiration. The prospect subconsciously concludes: "That works for John, but it won't work for me." Generic social proof actually reduces conversion at scale.

### Solution
The Social Proof Intelligence Engine (FR57) forces psychological homophily via Tribal Segment Filtering. When compiling a campaign, it queries the `Coach Story Archive` to find a testimonial from a past client whose *historical* psychological markers exactly matched the target prospect's *current* markers. It shows Position 2 clients stories about other Position 2 clients who succeeded, ensuring proof is perfectly resonant.

### Scope
**In scope:**
- The `social-proof-retriever` executing 3-variable filtering logic.
- The `Relevance Stringency Gate` controlling fallback options.
- The Output payload mapping matched testimonials to JSON format.

**Out of scope:**
- Rendering the testimonial on a webpage (handled by Excalidraw / Notion).
- Storing video media (stores text/links exclusively).

---

## 3. Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Produced By | Consumed By |
|---|---|---|---|---|
| `PROPOSED: DEP-ENG-077` | Matched Testimonial Payload | Reusuable text insertion | FR57 | FR51 / FR52 |

### Academic Grounding
- **Research Paper:** *Social Learning Theory* (Bandura, 1977).
- **Mechanism:** Efficacy expectations ("I can do this") are built primarily through *vicarious experience*. However, for peer modeling to trigger behavior change, the observer must perceive the model as highly similar to themselves in baseline competency. 

### Key Files
- `social_proof_retriever.py`
- `bmad-bmm-workflows-cpsc-generator.md`

### Technical Decisions
- **Anti-Fabrication Rule:** The LLM is structurally isolated from generation logic here. This is a pure SQL matching routine. If an LLM rewrote a success story to better match the prompt, it would violate federal Truth-in-Advertising mandates.
- **ADR-01 Isolation:** The database query fetches strictly `where coach_id = auth.uid()` to prevent showing competitors' testimonials to clients.

---

## 4. Implementation Plan

### Stage 1: Variable Resolution Rules (3-Point Segment Filtering)
- **Agent:** `social-proof-retriever`
- **Inputs:** 
  - `target_client_coping` Integer (Origin: FR-CBCS-04)
  - `target_client_spt` Integer (Origin: FR-CBCS-02)
  - `coach_story_archive` (DEP-ID: `DEP-ENG-024` — Origin: Coach Input)
- **Outputs:**
  - Database text and UUID references.
- **Failure Condition:** Missing archive DB table completely.
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `coach_id` + `target_client_coping` logged. **(Mandatory Execution)**.

**Variable Resolution Rule (Filter Precision):** The SQL `WHERE` clause dynamically constructs an exact match mapping to Enum `match_tier_rating`:
- **"PERFECT_MATCH"**: Evaluates `True` IF `Query Coping == Prospect Coping` AND `Query SPT == Prospect SPT`.
- **"ADJACENT_MATCH"**: Evaluates `True` IF `Query Coping == Prospect Coping +/- 1` AND `Query SPT == Prospect SPT`.
- **"BASELINE_DEFAULT"**: Evaluates `True` IF database returns `0` rows for previous bounds. Reverts to highest-performing generic testimonial assigned to the Coach profile.

### Stage 2: Quality Gate Extension
- **Agent:** `social-proof-retriever`
- **Inputs:** Generated Enum `match_tier_rating` from Stage 1.
- **Outputs:** Final JSON `MatchedTestimonialPayloadRow` (DEP-ENG-077).
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `gate_verdict` + `matched_historical_record_id` logged. **(Mandatory Execution)**.
- **Failure Condition:** Fallback evaluation triggers hard omits.

**Quality Gate:** **The Relevance Stringency Gate**
- **Triggered when:** Node identifies a target testimonial row and prepares to pass the string to FR51/FR52 compilers.
- **Exact Thresholds:** Evaluates the `match_tier_rating` Enum string.
- **Verdict - PASS:** Enum == `"PERFECT_MATCH"`. *Downstream Consequence:* String passed directly to compiler. `gate_verdict = PASS`.
- **Verdict - PROVISIONAL:** Enum == `"ADJACENT_MATCH"`. *Downstream Consequence:* String passed to compiler, logs a metadata warning `"PROVISIONAL_ADJACENT"`. Tells the pipeline: "Testimonial is one coping stage off. Relevant, but not identical."
- **Verdict - FAIL:** Enum == `"BASELINE_DEFAULT"`. *Downstream Consequence:* The script intercepts failure, actively disabling the "Social Proof" section of the target funnel brief. It is safe to omit social proof, dangerous to show alienating proof. Sets `gate_verdict = FAIL_OMIT_REQUIRED`. Sets `testimonial_text_raw = null`.

### Phase 3: Field-by-Field Schema Mapping
Every schema field specifies exact evaluation origin:
- `retrieval_id`: Returns `uuid.uuid4()`.
- `target_client_id_linked`: Returns contextual ID mapping.
- `coach_id`: Returns `auth.uid()` enforcing ADR-01 bound.
- `match_tier_rating`: Returns explicitly mapped Stage 1 Enum ("PERFECT_MATCH" | "ADJACENT_MATCH" | "BASELINE_DEFAULT").
- `gate_verdict`: Returns String mapped by Stage 2 ("PASS" | "PROVISIONAL" | "FAIL_OMIT_REQUIRED").
- `testimonial_text_raw`: Returns substring text retrieved. IF `gate_verdict` evaluates `FAIL_OMIT_REQUIRED`, resolves strictly to `null`.
- `matched_historical_record_id`: Returns ID mapping to specific `Coach Story Archive` source row. Null if omitted.
- `computation_timestamp`: Returns `datetime.now(timezone.utc).isoformat()`.

---

## 5. Primary Output Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "MatchedTestimonialPayloadRow (DEP-ENG-077)",
  "type": "object",
  "properties": {
    "retrieval_id": { "type": "string", "format": "uuid" },
    "target_client_id_linked": { "type": "string" },
    "coach_id": { "type": "string", "format": "uuid", "description": "ADR-01 Boundary Key" },
    "match_tier_rating": { "type": "string", "enum": ["PERFECT_MATCH", "ADJACENT_MATCH", "BASELINE_DEFAULT"] },
    "gate_verdict": { "type": "string", "enum": ["PASS", "PROVISIONAL", "FAIL_OMIT_REQUIRED"] },
    "testimonial_text_raw": { "type": ["string", "null"] },
    "matched_historical_record_id": { "type": ["string", "null"] },
    "computation_timestamp": { "type": "string", "format": "date-time" }
  },
  "required": [
    "retrieval_id", "target_client_id_linked", "coach_id", "match_tier_rating",
    "gate_verdict", "testimonial_text_raw", "matched_historical_record_id", "computation_timestamp"
  ]
}
```

---

## 6. Backward Compatibility Fallback
For new coaches onboarding who have exactly zero testimonials stored in `DEP-ENG-024`:
The system automatically defaults query to 0 rows. Triggers `BASELINE_DEFAULT` -> `FAIL_OMIT_REQUIRED` logic path. The system elegantly removes "Here's what our students say" modules from the webinar format structurally, ensuring no `<insert testimonial here>` placeholders ever render.

---

## 7. Tasks
- [ ] Task 1: Execute Python PostgreSQL `SELECT` evaluating integer array bound logic for `Coping` and `SPT` equivalency.
- [ ] Task 2: Code rigorous `FAIL_OMIT_REQUIRED` backward logic plumbed upstream into FR51 and FR52 compilers to strip target JSON nodes completely if executed.
- [ ] Task 3: Perform Text Sanitization verification asserting no formatting/whitespace cleaning logic parses the raw `testimonial_text_raw` string to enforce Truth in Advertising laws.

---

## 8. Acceptance Criteria
- [ ] **AC1 (Hard Omission Rejection):** Prospect `coping=2`. Database only contains `coping=5` testimonials. Query MUST evaluate `BASELINE_DEFAULT` tripping Gate `FAIL_OMIT_REQUIRED`. Row returns `testimonial_text_raw = null`. **Failure Example:** System passes advanced "millionaire" testimonial to an exhausted beginner.
- [ ] **AC2 (Provisional Fallback Acceptance):** Prospect `coping=3`. Database holds `coping=4`. Logic evaluates `ADJACENT_MATCH` saving `PROVISIONAL`. Testimonial returned successfully. **Failure Example:** Script throws critical routing error due to strict identical match parameters stranding the compiler.
- [ ] **AC3 (Enum Schema Mapping Integrity):** Reversal: `PERFECT_MATCH` retrieval MUST rigorously map the identical dict matching `Primary_Key` directly to output UUID `matched_historical_record_id`. **Failure Example:** System populates the phrase but orphans the ID, breaking forensic audits of what client data was distributed.

---

## 9. Dependencies
- **Upstream:**
  - `FR-CBCS-02`: SPT Stage Integer.
  - `FR-CBCS-04`: Coping Trajectory.
  - `DEP-ENG-024`: Coach Story Archive.
- **Downstream:**
  - `FR51`: Consumes Output payload inserting into Challenge text.
  - `FR52`: Consumes Output payload inserting into Webinar templates.
- **Infrastructure:**
  - `Receipt Chain Guard (DEP-ENG-041)`.

---

## 10. Testing Strategy

### Unit Tests
- `Test_Coping_Tolerance_Logic`: Submit `prospect_coping=3`. Run script evaluating against Mock DB rows `[Coping=2, Coping=5, Coping=3]`. Assert integer array math returns `"PERFECT_MATCH"` indexing strictly row 3. Submit `prospect=1`. Assert logic bounds match `"ADJACENT_MATCH"` indexing row 1.
- `Test_Gateway_Omission_Enforcement`: Pass Mock `match_tier_rating = BASELINE_DEFAULT` explicitly to Stage 2 func. Assert output boolean evaluates `FAIL_OMIT_REQUIRED` explicitly nulling the tuple schema target string.

### Integration Tests
- `Test_SQL_Query_Auth_Bound`: Attempt requesting records from `DEP-ENG-024` overriding the API parameters passing an opponent's UID string. Assert RowLevelSecurity enforces a 403 Forbidden intercept prior to `social_proof_retriever.py` invoking query.

### Safety / Isolation Tests
- `Test_Anti_Hallucinogen_Truncation`: Inject a mock 10,000 word testimonial text payload evaluating `PERFECT_MATCH`. Asssert system refuses to summarize, trim, or truncate via LLM, enforcing exact substring passage down the line or failing cleanly if memory limits are exceeded.
