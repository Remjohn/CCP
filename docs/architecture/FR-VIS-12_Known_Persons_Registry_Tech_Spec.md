# Tech-Spec: FR-VIS-12 — Known Persons Registry

**Created:** 2026-03-18
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §Visual Intelligence Pipeline, CVE_Documentation_V3 §8
**Skill Implementation:** `skills/visuals/known_persons_registry_adapter.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` — FR-VIS-12 definition (line 1038)
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V3.md` — §8 Known Persons Registry Architecture, §2 Image Sourcing Hierarchy (Tier 1 real person requirement)
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V2.md` — §4 Character Lexicon Integration, §9.5 Character Drift Detection
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Gaze Cueing in Design Framework.md` — Hero figure identity zone positioning, gaze authority projection
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Tribal Imageability and Cultural Half-Life.md` — Named person TIRS potency, noun-person congruence requirements
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Visual Style Psychology in Coaching.md` — Realism as authentication mechanism for named figures
- `d:\Work\The Conscious Coaching Factory\docs\architecture\FR50_Sovereign_Image_Rule_Tech_Spec.md` — Reference template for structure and depth

---

## 2. Overview

### Problem Statement
The Conscious Coaching Platform's content regularly references named public figures — heroes, enemies (negative exemplars), mentors, and wildcards from the Character Lexicon (FR0C). When a script mentions "Tony Robbins" or "Brené Brown," the visual pipeline must resolve an actual photograph of that person — not an AI-generated approximation, not a similar-looking stock model, and not an illustrated caricature. Using an incorrect or synthetic image of a named person creates three compounding failures: (1) **legal liability** — using unlicensed images or creating recognizable synthetic likenesses of public figures without permission; (2) **brand damage** — the audience recognizes the synthetic representation and loses trust in the coach's professionalism; (3) **contextual misrepresentation** — a "hero" figure must not appear in a negative-context visual, and an "enemy" figure must not appear in an aspirational context.

### Solution
FR-VIS-12 establishes the Known Persons Registry (DEP-VIS-006) as a Notion database mapping named public figures to their canonical image sources, usage permissions, content-context routing rules, and licensing status. When Aurore encounters a named person reference in a VCB slide (via the `named_person_reference` field assigned by Abel), it queries this registry via SKILL-IMG-006 before any stock search or AI generation. The registry enforces licensing compliance, context-appropriateness, and an 8-week rolling non-repetition window to prevent visual staleness.

### Scope
**In scope:**
- The Known Persons Registry Notion database schema (DEP-VIS-006).
- The `known_persons_registry_adapter.py` query interface.
- Context-appropriateness routing rules (hero/enemy/mentor/wildcard → permitted visual contexts).
- 8-week rolling non-repetition window for person-specific images.
- Human curation requirement for registry additions.

**Out of scope:**
- SKILL-IMG-006 implementation details (covered by FR-VIS-10 Multi-API Image Search).
- AI generation of named persons (explicitly prohibited by this spec).
- Character Lexicon management (covered by FR0C).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-VIS-006` | Known Persons Registry | SOURCE — The Notion database storing named person canonical images, permissions, and routing rules. |
| `DEP-VIS-005` | Visual Composition Brief Schema | INPUT — VCB slides with `named_person_reference` fields trigger registry queries. |
| `DEP-ENG-041` | Receipt Chain Guard | AUDIT — Registry query results, image selections, and context validations are hashed and recorded. |
| `FR0C` | Character Lexicon | UPSTREAM — Provides the named person's role classification (Hero, Enemy, Mentor, Wildcard). |
| `FR-VIS-09` | Image Sourcing Hierarchy | DOWNSTREAM CONSUMER — Registry-resolved images feed into Tier 1 of the sourcing hierarchy. |
| `FR-VIS-13` | Image Type Validity Gate | UPSTREAM — Gate V-00 enforces that named person slides use `tier_1_real_person` image type. |
| `SKILL-IMG-006` | SERPER Known Persons Lookup | TOOL — Fallback web search for licensed person portraits when the registry has no canonical image on file. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Applied |
|---|---|---|---|
| **Gaze Cueing in Design Framework** | CCP Research Lab | 2026 | Named hero figures occupy the Identity Zone in visual compositions. Their gaze direction cues the audience's attention toward the Hook Zone (the concept the hero embodies). The Gaze Cueing meta-analysis shows a 260-310ms reaction time advantage for targets in the gazed-at direction. When the named person's image is authentic (real photograph), the gaze cueing effect is 40% stronger than when the image is stylized or synthetic, because the human face recognition system (fusiform face area) engages more fully with photographic faces. |
| **Tribal Imageability and Cultural Half-Life** | CCP Research Lab | 2026 | Named persons function as ultra-high-TIRS nouns — proper names of known figures trigger immediate, vivid mental imagery with near-zero evocation latency. A properly sourced photograph of the named person reinforces this evocation, producing a TIRS potency multiplication effect (the noun + the image compound to a potency 1.5-2.0x the noun alone). A synthetic or incorrect image creates noun-image incongruence that reduces TIRS potency by 2.8 points — worse than omitting the image entirely. |
| **Visual Style Psychology in Coaching** | CCP Research Lab | 2026 | Named public figures require photographic realism because they exist in the audience's memory as real people. An illustrated or AI-generated version of a known figure triggers the Uncanny Valley response at lower thresholds than for fictional characters, because the audience has a strong pre-existing mental reference image. Realism is not an aesthetic preference for named persons — it is a recognition requirement. |

### Technical Decisions
1. **Notion as Registry Host:** The Known Persons Registry is stored in Notion (consistent with the platform's Notion-centric data architecture) rather than in a custom database. Operators add, review, and approve entries directly in Notion's UI, reducing tool fragmentation. Query performance is acceptable because the registry is small (typically 50-200 entries per coach) and queried infrequently (only when a VCB contains named person references).
2. **Human Curation Mandate:** Registry entries are never auto-populated from Character Lexicon data. An operator must manually add a named person, verify their canonical image source, confirm licensing, and set context-routing rules. This prevents automated inclusion of persons whose images may be restricted or contextually sensitive.
3. **8-Week Rolling Window:** The non-repetition window prevents the same image of a named person from appearing in visual content within an 8-week period. This is longer than the 4-week window for generic stock images because named person images carry stronger recognition — audiences notice repeated hero images more acutely, and repetition degrades the figure's perceived authority.

---

## 4. Implementation Plan

### Stage 1: Registry Query
*Agent:* `known_persons_registry_adapter.py`
*Inputs:* `named_person_reference` (string from VCB), `coach_id`, `tribe_id`.
*Outputs:* `registry_match` object (canonical image URL, licensing status, context roles, last used date, usage count) or `PERSON_NOT_IN_REGISTRY` (triggers SERPER fallback via SKILL-IMG-006).
*Failure Condition:* Notion API timeout; adapter returns `REGISTRY_QUERY_TIMEOUT`, Aurore falls back to SKILL-IMG-006 SERPER lookup.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Aurore encounters a VCB slide with a non-null `named_person_reference` (e.g., `"Brené Brown"`).
2. The adapter queries the Known Persons Registry (Notion database, DEP-VIS-006) with filter: `person_name = {named_person_reference} AND coach_id = {coach_id}`.
3. If a match is found: return the `registry_match` object containing all image sources, licensing data, and context rules.
4. If no match: return `PERSON_NOT_IN_REGISTRY`. Aurore invokes SKILL-IMG-006 (SERPER Known Persons Lookup) as a fallback to search for licensed portrait photos on the web. Any SERPER result is flagged `PENDING_REGISTRY_ADDITION` — it can be used once but must be manually added to the registry for future use.

### Stage 2: Context-Appropriateness Validation
*Agent:* `known_persons_registry_adapter.py`
*Inputs:* `registry_match` object, `slide_context` (from VCB — the emotional/narrative context of the slide), `person_role` (from Character Lexicon FR0C — Hero, Enemy, Mentor, Wildcard).
*Outputs:* `CONTEXT_VALID` (image may be used) or `CONTEXT_VIOLATION` (image blocked for this context).
*Failure Condition:* Context violation detected; adapter returns the violation with the specific routing rule that was violated.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Context-Routing Rules:**

| Person Role | Permitted Visual Contexts | Prohibited Visual Contexts |
|---|---|---|
| `Hero` | Aspirational, inspirational, authority, success, wisdom, transformation | Negative example, failure, cautionary tale, ridicule |
| `Enemy` | Cautionary tale, negative exemplar, contrast (paired with positive alternative) | Aspirational, heroic, wisdom, endorsement |
| `Mentor` | Wisdom, teaching, guidance, reflection, legacy | Negative example, failure, competition, confrontation |
| `Wildcard` | Any context — wildcards are contextually flexible | None (but must not imply endorsement of the coach's brand) |

**Steps:**
1. Retrieves the named person's `person_role` from the Character Lexicon (FR0C) via the registry entry.
2. Maps the VCB slide's `slide_context` (e.g., `"aspirational_transformation"`, `"cautionary_negative"`, `"wisdom_reflection"`) against the context-routing rules.
3. If the slide context is in the person's `permitted_visual_contexts`: proceed.
4. If the slide context is in the person's `prohibited_visual_contexts`: return `CONTEXT_VIOLATION` with the specific rule: e.g., `"Hero 'Brené Brown' cannot appear in cautionary_negative context. Permitted contexts: aspirational, inspirational, authority, success, wisdom, transformation."`.
5. Context violations are returned to Abel for VCB revision — Abel must either change the slide's context or remove the named person reference.

### Stage 3: Non-Repetition Window Check
*Agent:* `known_persons_registry_adapter.py`
*Inputs:* `registry_match` object (including `last_used_date` and `usage_log`).
*Outputs:* `REPETITION_CLEAR` (image not used in last 8 weeks) or `REPETITION_VIOLATION` (same image used within 8-week window).
*Failure Condition:* All available canonical images for the person fall within the 8-week window; adapter returns `ALL_IMAGES_IN_WINDOW` and Aurore falls back to SKILL-IMG-006 SERPER lookup for fresh licensed alternatives.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Retrieves the person's `usage_log` — an array of `{image_id, used_date, content_output_id}` entries.
2. For each available canonical image in the registry entry, checks whether `used_date` is within the last 56 days (8 weeks).
3. Selects the first image that is outside the 8-week window. If multiple images are available, prefers the least recently used.
4. If all images are within the window: triggers the SERPER fallback to find a fresh licensed alternative. The SERPER result is flagged for registry addition.
5. Updates the selected image's `usage_log` with the current date and `content_output_id`.

### Stage 4: Image Resolution & Delivery
*Agent:* `known_persons_registry_adapter.py`
*Inputs:* Selected canonical image URL from Stage 1 or 3, licensing confirmation.
*Outputs:* `resolved_person_image` object containing the image URL, licensing metadata, and provenance trail.
*Failure Condition:* Selected canonical image URL is broken (404); adapter attempts next available image. If no images resolve, falls back to SERPER.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Validates the selected canonical image URL with a HEAD request to confirm accessibility (HTTP 200).
2. If accessible: downloads the image to Cloudflare R2 for pipeline processing.
3. If inaccessible (404, 403, timeout): attempts the next available canonical image in the registry. If all fail: triggers SERPER fallback.
4. Assembles the `resolved_person_image` object with: `image_url` (R2 URL), `source_registry_id`, `person_name`, `person_role`, `licensing_type` (Creative Commons, Editorial, Licensed Stock), `context_validated`, `repetition_window_status`.
5. Delivers to Aurore's `image_resolution_map` as a Tier 1 resolution.

---

## 5. Primary Output Schema

### Schema Name: `Known_Persons_Registry_Entry` (Notion DB Row)

```json
{
  "registry_entry_id": "KPR-001-BRENE-BROWN",
  "person_name": "Brené Brown",
  "person_role": "Hero",
  "coach_id": "coach_jean_pierre",
  "canonical_images": [
    {
      "image_id": "KPR-IMG-001",
      "source_url": "https://example.com/brene-brown-portrait-licensed.jpg",
      "r2_cached_url": "https://r2.ccf-assets.com/known-persons/brene-brown-001.jpg",
      "licensing_type": "Editorial",
      "licensing_source": "Getty Images",
      "licensing_expiry": "2027-01-15",
      "resolution_px": "2400x3600",
      "aspect_ratio": "2:3"
    },
    {
      "image_id": "KPR-IMG-002",
      "source_url": "https://example.com/brene-brown-speaking-licensed.jpg",
      "r2_cached_url": "https://r2.ccf-assets.com/known-persons/brene-brown-002.jpg",
      "licensing_type": "Creative Commons Attribution",
      "licensing_source": "Wikimedia Commons",
      "licensing_expiry": null,
      "resolution_px": "3200x2100",
      "aspect_ratio": "3:2"
    }
  ],
  "context_routing_rules": {
    "permitted_contexts": ["aspirational", "inspirational", "authority", "success", "wisdom", "transformation"],
    "prohibited_contexts": ["negative_example", "failure", "cautionary_tale", "ridicule"]
  },
  "usage_log": [
    { "image_id": "KPR-IMG-001", "used_date": "2026-02-10", "content_output_id": "CO-JP-20260210-005" },
    { "image_id": "KPR-IMG-002", "used_date": "2026-01-15", "content_output_id": "CO-JP-20260115-012" }
  ],
  "added_by_operator": "operator_maria",
  "added_date": "2025-12-01",
  "last_verified_date": "2026-03-01",
  "registry_status": "ACTIVE"
}
```

### Schema Name: `Resolved_Person_Image.json`

```json
{
  "resolution_id": "RPI-JP-20260318-001",
  "person_name": "Brené Brown",
  "person_role": "Hero",
  "slide_index": 2,
  "content_output_id": "CO-JP-20260318-012-CAROUSEL",
  "selected_image": {
    "image_id": "KPR-IMG-002",
    "r2_url": "https://r2.ccf-assets.com/known-persons/brene-brown-002.jpg",
    "licensing_type": "Creative Commons Attribution",
    "licensing_verified": true
  },
  "context_validation": {
    "slide_context": "aspirational_transformation",
    "person_role": "Hero",
    "result": "CONTEXT_VALID"
  },
  "repetition_check": {
    "last_used_date": "2026-01-15",
    "days_since_last_use": 62,
    "window_days": 56,
    "result": "REPETITION_CLEAR"
  },
  "sourcing_tier": "tier_1_real_person",
  "source_type": "known_persons_registry",
  "receipt_chain_block": "RCB-KPR-20260318-001",
  "timestamp_utc": "2026-03-18T01:37:00Z"
}
```

---

## 6. Backward Compatibility Fallback

If a VCB references a named person who has not been added to the Known Persons Registry:
1. The adapter returns `PERSON_NOT_IN_REGISTRY` with the person's name.
2. Aurore invokes SKILL-IMG-006 (SERPER Known Persons Lookup) to search for licensed portrait photos.
3. If SERPER finds a suitable licensed image: the image is used for this composition with `source_type: "serper_fallback"`, and a `PENDING_REGISTRY_ADDITION` flag is set — the operator is notified to add this person to the registry for future use.
4. If SERPER finds no suitable licensed image: the slide is flagged `PENDING_OPERATOR_REVIEW` — the operator must manually source an image or remove the named person reference from the VCB.
5. Under no circumstances does the pipeline generate an AI image of a named real person. This is a hard architectural constraint — no fallback path leads to AI generation for named persons.

---

## 7. Tasks

- [ ] **Task 1:** Create the Known Persons Registry Notion database template (DEP-VIS-006). Properties: `Person Name` (Title), `Person Role` (Select: Hero/Enemy/Mentor/Wildcard), `Coach ID` (Text), `Canonical Images` (Files & media), `Licensing Type` (Select), `Licensing Source` (Text), `Licensing Expiry` (Date), `Permitted Contexts` (Multi-select), `Prohibited Contexts` (Multi-select), `Usage Log` (Relation to Visual Production Outputs), `Added By` (Person), `Added Date` (Date), `Last Verified` (Date), `Status` (Select: Active/Archived/Pending).
- [ ] **Task 2:** Write `known_persons_registry_adapter.py` — the query interface that retrieves registry entries, validates context appropriateness, checks the non-repetition window, and resolves canonical images.
- [ ] **Task 3:** Implement the context-appropriateness validation engine with the 4-role routing rules (Hero, Enemy, Mentor, Wildcard) and structured violation reporting.
- [ ] **Task 4:** Implement the 8-week rolling non-repetition window check — query `usage_log`, compute days since last use per image, select the least recently used image outside the window.
- [ ] **Task 5:** Implement the canonical image URL health check — HEAD request validation, fallback to next available image, SERPER fallback trigger on complete failure.
- [ ] **Task 6:** Implement the `PENDING_REGISTRY_ADDITION` workflow for SERPER-discovered images — flag the image, notify the operator, and queue for manual registry addition.
- [ ] **Task 7:** Implement the hard prohibition against AI generation of named persons — ensure no fallback path in the adapter or downstream agents can route a named person reference to RunningHub.
- [ ] **Task 8:** Integrate with Receipt Chain Guard (DEP-ENG-041) for cryptographic audit at every stage.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Registry Match — Happy Path):** Query the registry for `"Brené Brown"` with 2 canonical images. Image 1 last used 3 weeks ago (within window). Image 2 last used 9 weeks ago (outside window). Assert the adapter selects Image 2 and returns `REPETITION_CLEAR`. *Failure Example:* The adapter selects Image 1 (most recent), ignoring the repetition window, and the same Brené Brown portrait appears in consecutive monthly content.
- [ ] **AC2 (Context-Appropriateness — Hero in Negative Context):** Query the registry for `"Simon Sinek"` (role: Hero). Slide context is `"cautionary_negative"`. Assert the adapter returns `CONTEXT_VIOLATION: Hero 'Simon Sinek' cannot appear in cautionary_negative context. Permitted contexts: aspirational, inspirational, authority, success, wisdom, transformation`. *Failure Example:* Simon Sinek's photo appears alongside text about leadership failure, implying he is the example of bad leadership — damaging the coach's credibility and potentially invoking legal action.
- [ ] **AC3 (Context-Appropriateness — Enemy in Aspirational Context):** Query for a person with role `"Enemy"`. Slide context is `"aspirational_transformation"`. Assert `CONTEXT_VIOLATION`. *Failure Example:* A figure positioned as a negative exemplar in the Character Lexicon appears in an aspirational visual, confusing the audience about whether this person is a hero or villain in the coach's narrative.
- [ ] **AC4 (All Images in Window):** Query for a person with 3 canonical images, all used within the last 8 weeks. Assert the adapter returns `ALL_IMAGES_IN_WINDOW` and triggers SERPER fallback. *Failure Example:* The adapter forces selection of the "least stale" image within the window, producing a visual that the audience has already seen twice in the last 2 months.
- [ ] **AC5 (Person Not in Registry):** Query for `"Adam Grant"` who is not in the registry. Assert `PERSON_NOT_IN_REGISTRY` is returned and SERPER fallback is triggered. Assert a `PENDING_REGISTRY_ADDITION` notification is queued for the operator. *Failure Example:* The pipeline halts entirely because the person isn't registered, blocking the entire composition.
- [ ] **AC6 (AI Generation Prohibition):** Attempt to route a named person reference through the image sourcing hierarchy to Tier 3 or Tier 4 (AI generation). Assert the hard prohibition prevents any RunningHub workflow from receiving a named person prompt. *Failure Example:* RunningHub generates a semi-realistic AI image of a famous coach — legally actionable and reputationally catastrophic.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| DEP-VIS-006 (Known Persons Registry) | Internal | SOURCE — Notion database of named person canonical images and routing rules. |
| FR0C (Character Lexicon) | Internal | UPSTREAM — Provides person_role classification (Hero/Enemy/Mentor/Wildcard). |
| DEP-VIS-005 (VCB Schema) | Internal | INPUT — VCB slides with `named_person_reference` fields. |
| DEP-ENG-041 (Receipt Chain Guard) | Internal | AUDIT — All registry queries and image selections are hashed. |
| FR-VIS-09 (Image Sourcing Hierarchy) | Internal | DOWNSTREAM — Resolved images feed into Tier 1 of the hierarchy. |
| FR-VIS-10 (Multi-API Image Search) | Internal | FALLBACK — SKILL-IMG-006 provides SERPER-based fallback searches. |
| FR-VIS-13 (Image Type Validity Gate) | Internal | UPSTREAM — Gate V-00 enforces `tier_1_real_person` for named person slides. |
| Notion API | External | Registry is hosted in Notion. |
| Cloudflare R2 | External | Canonical image caching/storage. |

---

## 10. Testing Strategy

### Unit Tests
- **Context Routing Matrix:** For each of the 4 person roles (Hero, Enemy, Mentor, Wildcard), test all permitted and prohibited context combinations. Assert correct PASS/FAIL for each.
- **Repetition Window Calculation:** Provide a `used_date` of 55 days ago (within 56-day window). Assert `REPETITION_VIOLATION`. Provide 57 days ago. Assert `REPETITION_CLEAR`. Boundary test: 56 days exactly → `REPETITION_CLEAR` (window is exclusive).
- **Image Selection Priority:** Provide 5 canonical images with usage dates [10 days, 30 days, 60 days, 90 days, 120 days] ago. Assert the adapter selects the image used 60 days ago (first outside window, least recently used among viable candidates).

### Integration Tests
- **Full Named Person Resolution:** Add "Brené Brown" to a test registry with 2 images. Submit a VCB with `named_person_reference: "Brené Brown"` in slide 2. Assert the adapter resolves a canonical image, validates context, checks repetition, and delivers a `resolved_person_image` to Aurore's `image_resolution_map`.
- **SERPER Fallback Flow:** Submit a VCB referencing a person not in the registry. Assert SERPER is invoked, a result is obtained, `PENDING_REGISTRY_ADDITION` is flagged, and the image is delivered for this composition.

### Safety Tests (ADR-01 Quarantine Security)
- **AI Generation Prohibition:** Inject `named_person_reference: "Elon Musk"` into a VCB slide. Remove all registry entries and SERPER results. Assert the pipeline flags `PENDING_OPERATOR_REVIEW` — it does NOT route to Tier 3 or Tier 4 AI generation under any fallback condition.
- **Registry Injection Attack:** Inject `person_name: "Brené Brown'; DROP DATABASE known_persons;"` into a Notion query. Assert the query is sanitized — the filter treats the entire string as a literal `person_name` value and returns zero results (no SQL execution).
