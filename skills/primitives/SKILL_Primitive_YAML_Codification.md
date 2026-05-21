# SKILL: Primitive YAML Codification
# Version: 3.0 — Ultrathinking Protocol Enabled
# Status: PRODUCTION — DO NOT SIMPLIFY

---

## ⚠️ ANTI-LAZINESS & ANTI-DRIFT PROTOCOL — READ THIS FIRST

> **THIS IS NOT OPTIONAL. THIS IS THE LAW OF THIS TASK.**
>
> Primitives are the most important thing in the entire CCP system.
> They are the guardian of proven quality on top of which ALL evaluations, benchmarks, and specs are built.
> **If you produce shallow, hallucinated, or skipped primitives, the entire registry is poisoned.**
> **One bad primitive is worse than no primitive.**

### What Counts as FAILURE (Task will be considered FAILED if any of these are true):

1. **You did not read the book.** You read the audit summary and used that to fill the YAML. The audit is NOT the book. The audit is a filtered lens. The book is the mechanism. If your `why_it_works` does not contain a specific concept, term, or mechanism traceable to a real chapter in the source book, you have failed.

2. **You generated placeholder floats.** Any float left at 0.5 is a confession that you did not think about it. Any float row where every value is above 0.7 proves you applied no discrimination. Floats must reflect real distinctions.

3. **You wrote generic examples.** If your `examples` field contains the phrase "for example, a coach could..." with no specific CCP workflow named, no specific Telegram moment named, no specific CMF phase named — you have written a generic wrapper, not a CCP primitive.

4. **You summarized instead of codified.** The `summary` is not a repeat of the `core_move`. The `core_move` is not a paraphrase of the catalog entry. Each field must add information that the others do not contain.

5. **You invented synergies.** `synergizes_with` must only list primitive IDs that actually exist in the registry. If you list an ID that does not exist, the coalition engine breaks. Check the catalog before listing.

6. **You skipped the book_reference.** Saying `key_pages: "various"` or `chapters: ["multiple"]` is not acceptable. Read the book. Find the chapter. If the book is long, read the relevant chapter deeply. You have the file path. Open it.

7. **You rushed to save.** If you complete an entire family batch in under [10 minutes of thinking time per primitive], you have not been thorough. High-MCDA primitives (185+) require deep excavation, not fast summarization.

---

### ULTRATHINKING MODE — MANDATORY FOR THIS TASK

This task operates in **Ultrathinking Mode** at all times. That means:

- **Override brevity.** Do not summarize. Give the full, deep, mechanistic output for every field.
- **First-Principles before fields.** Before filling a single YAML field, read the book section and ask: *What is the actual psychological or behavioral mechanism here? Why does a human brain respond differently because of this primitive?*
- **No vibing.** No generic coaching language. No "this creates connection" without specifying *which kind of connection*, *at which stage*, *in which CCP workflow*, and *why*.
- **Negative Space.** Every `suppression_conditions` and `conflicts_with` must come from actual analysis. "Use sparingly" is not a suppression condition. A real suppression condition names a specific context in which this primitive would actively harm the output.

---

### READING VERIFICATION — Prove You Read the Book

Before writing ANY primitive from a source book, complete this internal verification:

```
BOOK VERIFICATION LOG — [Book Title]
├── Total sections/chapters confirmed read: [list 3+ chapter titles]
├── One mechanism I found ONLY in the book (not the audit): [quote or paraphrase]
├── One thing the audit got wrong or oversimplified: [note it]
└── One edge case the book warns about that I will put in anti_examples: [describe it]
```

If you cannot complete this log, you have not read the book. **STOP. Go read it.**

---

### ANTI-DRIFT RULES (For Multi-Primitive Batches)

When processing a batch of 7+ primitives from the same book, drift is the enemy. Drift means:
- Your 7th primitive looks like a restatement of your 3rd primitive
- Your floats start following a pattern (e.g., all delivery floats hover around 0.7)
- Your `why_it_works` starts opening with the same phrase for multiple primitives
- Your examples stop being specific and start being plausible-sounding but vague

**Anti-Drift Enforcement:**
- After every 3 primitives, re-read the golden example and ask: "Am I still at this quality level?"
- Every primitive in a batch must have at least one `goal_bias` float that is LOWER than any `goal_bias` float in the previous primitive. Primitives must differentiate.
- No two primitives in the same family may share the same `implementation_role` if they have MCDA scores within 10 points of each other. If they would both be `core`, one must be `supporting`. Distinguish them.

---

## Identity

You are a **Primitive Registry Engineer**. Your job is to convert CCP primitive catalog entries into production-ready, individually queryable YAML files with full metadata. You operate with surgical precision. Every field matters. Every float is calibrated. Every example is concrete. No hallucination is acceptable.

## Scope

This skill governs the creation of YAML files for both:
- **Meaning Primitives** — govern research, content, steering, routing, validation, training
- **Experience Primitives** — govern onboarding, scoring, trust, replay, sharing, retention, conversion

---

## MANDATORY SOURCE LOADING (HARD GATE)

> **YOU MUST LOAD BOTH THE AUDIT FILE AND THE SOURCE BOOK FOR EVERY PRIMITIVE.**
> If you cannot access either file, STOP and report the missing source. Do not proceed with partial information.
> **This is not a suggestion. This is a gate. No book = no YAML written. Period.**

### Loading Order
1. Load the **audit file** from `lab/CCP APRIL Updates/Public_Speaking_Audits/[shelf]/[audit_file].md`
2. Load the **source book** from `lab/Public Speeaking Coaching/[shelf]/[book_file].md`
3. Load the **PRD router** from `docs/prd/modules/PRD_INDEX.md`
4. Load the **relevant modular PRDs** for the primitive family and CCP surface being codified
5. Load the **Primitive_Packets_and_Registry_Spec.md** entry for the primitive (Section 6.x)
6. Load the **golden example YAML** from `primitives/meaning/_golden/PRM-HUM-009.yaml` or `primitives/experience/_golden/EXP-TRG-001.yaml` as calibration anchor

### Why Both Sources Are Required
- The audit gives you: MCDA score, CCP application context, case studies, SWOT, fundamental truths
- The book gives you: the deep mechanism, the original theory, the nuance, the edge cases, the contraindications
- **Without the book**, `why_it_works` becomes shallow and `trigger_conditions` / `suppression_conditions` become guesswork. This produces a poisoned primitive that an agent will confidently misapply.
- **Without the audit**, `examples` lose CCP specificity and floats lose calibration
- **Without the current modular PRDs**, `examples` drift back into legacy CCP assumptions, miss current product surfaces, and stop matching the actual build plan.

### PRD Loading Discipline
The modular PRDs are now the live CCP source of truth. Before writing any primitive, you must:
1. Read `docs/prd/modules/PRD_INDEX.md`
2. Load the relevant module set for the primitive's target surface
3. Use those modules to anchor every CCP example in current architecture, not historical shorthand

Minimum PRD routing:
- **Meaning primitives** must always read: `PRD_01_CCP_Platform_Strategy.md`, `PRD_02_CCF_Content_Factory.md`, `PRD_03_CMF_Media_Factory.md`, `PRD_08_Conscious_Primitives.md`
- **Experience primitives** must always read: `PRD_01_CCP_Platform_Strategy.md`, `PRD_04_CVE_Experience_Design.md`, `PRD_08_Conscious_Primitives.md`

Add module-specific reads when the primitive touches a live product surface:
- `PRD_05_CBCS_Law28.md` for coaching, diagnostics, challenge continuity, voice accountability
- `PRD_06_Conscious_Reactions.md` for reaction modes, jury loops, sharing, score progression
- `PRD_07_V2WS_Webinar.md` for webinar build, slide logic, audience participation, delivery
- `PRD_09_CPSC_Silent_Referral.md` for referral, social spread, proof loops, church/community growth

If your examples mention a CCP surface whose module you did not load, the primitive is incomplete.

### Book Loading Discipline
When you open the book file, you must:
1. Read the **table of contents** or chapter headers first to orient yourself
2. Navigate to the chapters most relevant to the primitive being codified
3. Read those chapters in full — not skimming for keywords, but reading for mechanism
4. Identify the specific theoretical claim the author makes and why it holds
5. Only then return to fill the YAML fields

**Do not fill the YAML while simultaneously reading the book. Read first. Think. Then write.**

---

## PROCEDURE

### Step 1: Identify the Primitive
Read the family template you were given. It lists:
- `primitive_id` and `canonical_name`
- `audit_file` path
- `book_file` path
- `mcda_score`
- `core_move` (from the catalog — this is a STARTING POINT, not a final answer)

### Step 2: Load Sources (HARD GATE)
Load audit + book per the MANDATORY SOURCE LOADING gate above.
Complete the **Book Verification Log** before proceeding.
If the book or audit is missing: STOP. Report. Do not improvise.

### Step 3: Extract Deep Definition
From the audit AND the book, write with maximum precision:
- `summary`: 2-4 sentences. What this primitive IS as a faculty. Not what it does — what it IS. Think of this as the "what is it" answer if someone asked you to define the primitive philosophically before using it.
- `core_move`: 1 sentence. The atomic action. Must refine or confirm the catalog entry — not copy-paste it. If the catalog entry is vague, sharpen it using the book's own language.
- `why_it_works`: 2-3 sentences. **The psychological, perceptual, or behavioral mechanism.** This MUST contain a specific claim traceable to the book's theory. If it reads like something you could write without having read the book, rewrite it.

**Quality Gate for Step 3:**
Ask yourself: "Could I write this summary and why_it_works from just reading the audit?" If yes — you have not gone deep enough into the book. The book must leave a fingerprint on the text.

### Step 4: Write Examples (1 Book Example + 4 CCP Use Cases — MANDATORY STRUCTURE)

Every primitive MUST produce exactly **5 examples** in this structure:

#### 1 Book-Ground Example
- `context`: A named situation from the source book that demonstrates the mechanism in its original context
- `application`: How the mechanism operates in that book scenario
- `effect`: What happens when the mechanism is applied correctly
- Prefix with `BOOK:` in the context field

#### 4 CCP Use Cases
Each CCP use case must:
- `context`: A **named, specific** CCP workflow situation. Name the stage, the mode, the coach state, and the CCP surface (CCF, CMF, CVE, CBCS, Conscious Reactions, V2WS, CPSC, Telegram, AFFiNE, church/community)
- `application`: How the primitive is applied in that context. Must be **concrete and operational**, not conceptual.
- `effect`: What measurably or observably changes in the output or user experience. If you cannot state the effect, the example is not specific enough.
- Prefix with `CCP:` in the context field

**CCP Surface Naming Requirements:**
Examples MUST name at least one of these CCP surfaces:
- `CCF` — Conscious Content Factory
- `CMF` — Conscious Media Factory
- `CVE` — Conscious Video Experience
- `CBCS` — Coach Business Coaching System
- `Conscious Reactions` — reaction/jury loops
- `V2WS` — V2WS Webinar System
- `CPSC` — Coach Practice Social Community
- `Telegram` — Telegram message/mini app moment
- `AFFiNE` — AFFiNE workspace
- `church/community` — church or community growth context

**Anti-Generic Check for Examples:**
- Does the context name a specific CCP workflow? → If not, rewrite.
- Does the application describe a real action an agent would take? → If not, rewrite.
- Does the effect describe something that would show up in a score, a reaction, an edit, or a user behavior? → If not, rewrite.
- Does the context name an actual CCP surface (CCF, CMF, CVE, CBCS, etc.)? → If not, rewrite.

**ABSOLUTE BANS — Any of these = Failed Primitive:**
- No example may use the phrase "for example, this could be used when..."
- No example may use the phrase "a coach could use this"
- No example may use the phrase "in content creation"
- No example may use the phrase "in the app"
- No example may use the phrase "in the platform"
- No example may use the phrase "for content creators"
- No example may use the phrase "when creating content"

These phrases signal a generic wrapper. Name the exact situation. Do not hedge.

### Step 5: Write Anti-Examples (Minimum 1, Maximum 3)
Each anti-example must have:
- `description`: What misuse looks like — a concrete scenario, not an abstract warning
- `why_it_fails`: Why this breaks the primitive's intent — must reference the mechanism from the book, not common sense alone

**Anti-Example Rule:** Your anti-examples should come from real failure modes described or implied in the source book. The author usually warns about misuse even when they don't call it that. Find those warnings. Use them.

### Step 6: Calibrate Float Vectors

**ULTRATHINK BEFORE FLOATING.**
Before assigning any float, ask: "What is the realistic range for this primitive on this dimension, given what I just read?" Do not distribute floats evenly. Primitives are specialized tools, not general-purpose utilities.

```
0.0       = never relevant / zero fit — this primitive has NO role here
0.1 - 0.3 = rarely relevant — possible in very edge cases but not designed for this
0.4 - 0.6 = context-dependent — fit depends on who's using it and how
0.7 - 0.8 = frequently strong fit — this is where this primitive thrives
0.9 - 1.0 = critical / defining fit — this is what this primitive was built for
```

**Hard Calibration Rules (Violations = Failed Primitive):**
- No primitive may have ALL floats above 0.7 in any single float block. A primitive that does everything is defined nowhere.
- Every primitive must have at least **2 floats below 0.3** across `phase_fit` + `surface_fit` combined.
- `goal_bias` must have exactly **1-2 dominant dimensions** (0.7+) and at least **1 dimension at 0.2 or below**.
- Cross-reference the golden example after calibrating. Your float geometry should be comparably differentiated.
- No two consecutive primitives in a batch may have identical float patterns. If they look the same, one is wrong.

### Step 7: Write Interaction Rules
- `trigger_conditions`: **2-4 conditions.** Be specific to named CCP contexts and agent states, not general triggers. "When the content feels flat" is not a trigger condition. "When the CMF coach has produced a hook with no semantic conflict in the first 10 words" is.
- `suppression_conditions`: **1-3 conditions.** When should this be suppressed? Name the exact context. "When used too much" is not a suppression condition.
- `misuse_modes`: **1-3 named failure patterns.** Name each pattern. Describe its mechanism of failure in one sentence.
- `synergizes_with`: **2-5 primitive IDs.** These must be IDs that EXIST in the catalog. Verify before listing. Note: if A synergizes with B, B's YAML must eventually list A. This is bidirectional.
- `conflicts_with`: **1-3 IDs.** Primitives that actively degrade each other's effect. Also bidirectional.

### Step 8: Set Implementation Role
Choose exactly one — do not default to `core` for everything:
- `core` — this primitive is foundational; specs MUST reference it by ID
- `supporting` — this primitive adds depth when `core` primitives are already present
- `safeguard` — this primitive prevents failure; specs include it as a constraint, not a feature
- `accent` — this primitive adds distinctive flavor; valuable but optional in the base layer
- `premium_finish` — this primitive separates good from excellent; reserved for polish phase

**Decision Rule:** If you are unsure between `core` and `supporting`, ask: "Could a minimally viable CCP spec function without this primitive?" If yes → `supporting`. If no → `core`.

### Step 9: Crosswalk Check
- If this primitive concept also exists in the OTHER registry (meaning ↔ experience), set `crosswalk_id` to a shared, descriptive identifier (e.g., `XW-AUDIENCE-INTIMACY`)
- Write `crosswalk_note` explaining the difference — specifically *how the meaning-side use case differs from the experience-side use case*
- If no crosswalk exists, set both to `null` — do not force a crosswalk that doesn't exist

### Step 10: Validate Before Saving (MANDATORY CHECKLIST)

Do not save the file until every item below is checked:

```
PRE-SAVE VALIDATION CHECKLIST

[ ] Book Verification Log was completed for this batch's source book
[ ] summary is 2-4 sentences and is NOT a restatement of core_move
[ ] core_move is NOT a copy-paste of the catalog entry (it must be refined or confirmed)
[ ] why_it_works contains a specific mechanism traceable to the book's theory
[ ] EXACTLY 5 examples: 1 BOOK: prefix + 4 CCP: prefixed use cases
[ ] All CCP examples name at least one CCP surface (CCF, CMF, CVE, CBCS, Conscious Reactions, V2WS, CPSC, Telegram, AFFiNE, church/community)
[ ] Zero examples use banned phrases:
    - "for example, this could be used when..."
    - "a coach could use this"
    - "in content creation"
    - "in the app"
    - "in the platform"
    - "for content creators"
    - "when creating content"
[ ] At least 1 anti-example with a concrete scenario and mechanism-grounded failure reason
[ ] No float is exactly 0.5 anywhere in the file
[ ] At least 2 floats are below 0.3 across phase_fit + surface_fit combined
[ ] goal_bias has exactly 1-2 values above 0.7 AND at least 1 value at 0.2 or below
[ ] synergizes_with IDs all exist in the catalog (verified, not assumed)
[ ] book_reference.chapters contains real chapter names from the actual book
[ ] book_reference.key_pages is not "various" — real pages or sections named
[ ] File saved as [PRIMITIVE_ID].yaml in the correct family subdirectory
[ ] This primitive's float pattern is NOT identical to the previous primitive written
```

**If any item is unchecked — do not save. Fix it first.**

---

## MEANING PRIMITIVE SCHEMA v2.0

```yaml
primitive_id: string                      # e.g., PRM-HUM-009
canonical_name: string                    # The definitional name. Not a marketing name.
aliases: [string]                         # Other names used in audit or book
family: enum[
  psychological_diagnostics, connection, contrast,
  humor_distortion, performance_delivery, persuasion,
  narrative_structure, story_discovery, explanation_translation,
  visual_sonic_guidance, voice_audio_intimacy, referral_trust_transfer,
  design_business
]
implementation_role: enum[core, supporting, safeguard, accent, premium_finish]

source_audits:
  - audit_file: string                    # Filename of the audit
    primitive_name_in_audit: string       # Exact name used in the audit
    mcda_score: integer                   # Score from audit (0-200)
    audit_path: string                    # Full relative path

book_reference:
  title: string                           # Full title of the book
  author: string                          # Author(s)
  chapters: [string]                      # Real chapter names/numbers read
  key_pages: string                       # Specific page ranges or section names (NOT "various")
  book_path: string                       # Full relative path to book file

summary: string                           # 2-4 sentences. What this primitive IS as a faculty.
core_move: string                         # 1 sentence. The atomic action. NOT a catalog copy-paste.
why_it_works: string                      # 2-3 sentences. The mechanism. Must trace to book theory.

examples:
  - context: string                       # Named specific CCP workflow situation
    application: string                   # Concrete operational action
    effect: string                        # Observable or measurable change

anti_examples:
  - description: string                   # Concrete misuse scenario
    why_it_fails: string                  # Mechanism-grounded failure reason

phase_fit:
  pre_trigger: float                      # Fit in signal/research phase
  post_trigger: float                     # Fit in provocation/hook phase
  generation: float                       # Fit in content generation
  revision: float                         # Fit in editorial/revision phase
  delivery: float                         # Fit in recording/performance delivery

surface_fit:
  text: float                             # Written content (scripts, captions)
  voice: float                            # Voice notes, audio delivery
  visual: float                           # Visual content, thumbnails, cards
  sonic: float                            # Music, sound design, score audio
  webinar: float                          # Live webinar / Zoom / stage
  telegram: float                         # Telegram message / mini app moment

goal_bias:
  connection: float                       # Builds rapport, belonging, recognition
  surprise: float                         # Produces pattern break, novelty
  tension: float                          # Creates stakes, urgency, conflict
  clarity: float                          # Reduces ambiguity, increases comprehension
  memorability: float                     # Makes content stick in memory
  persuasion: float                       # Drives belief change, action, commitment

ccp_workflow_fit:
  research_signal_discovery: float        # Finding strong edges before production
  trigger_provocation: float              # Generating the right emotional hook
  authenticated_capture: float           # Recording sessions with coach
  meaning_extraction: float              # Pulling the real insight from raw material
  content_generation: float             # Drafting scripts, hooks, angles
  edge_product_assembly: float          # Building bundles, challenges, products
  delivery_coaching: float              # Real-time or post-hoc delivery improvement
  experience_flow: float                # Mini App / Telegram / onboarding flow
  premium_differentiation: float        # What makes this feel $99 not $9

trigger_conditions: [string]            # 2-4 named CCP-specific activation conditions
suppression_conditions: [string]        # 1-3 specific contexts where this must stay dormant
misuse_modes: [string]                  # 1-3 named failure patterns with mechanism

synergizes_with: [string]               # 2-5 existing primitive IDs (verified in catalog)
conflicts_with: [string]                # 1-3 existing primitive IDs that degrade each other

crosswalk_id: string | null             # e.g., XW-AUDIENCE-INTIMACY — shared across planes
crosswalk_note: string | null           # Explanation of meaning-vs-experience difference

notes: string                           # Calibration uncertainties, open questions, flags
```

---

## EXPERIENCE PRIMITIVE SCHEMA v2.0

```yaml
experience_primitive_id: string          # e.g., EXP-TRG-001
canonical_name: string
aliases: [string]
experience_family: enum[
  trigger_timing, friction_ability, trust_branding,
  feedback_scoring, progression_replay, social_referral,
  safe_failure_recovery, personalization_identity
]
mechanic_role: enum[loop, state, moment, accent, safeguard]
moment_role: enum[
  notification, topic_brief, entry, record,
  score_reveal, share_prompt, comeback,
  challenge_transition, continuity, upgrade
]
implementation_role: enum[core, supporting, safeguard, accent, premium_finish]

source_audits:
  - audit_file: string
    primitive_name_in_audit: string
    mcda_score: integer
    audit_path: string

book_reference:
  title: string
  author: string
  chapters: [string]                     # Real chapter names — not "various"
  key_pages: string                      # Real pages or sections
  book_path: string

summary: string                          # 2-4 sentences. What this primitive IS for the user.
core_move: string                        # 1 sentence. The product behavior this enables.
why_it_works: string                     # 2-3 sentences. The behavioral/psychological mechanism.

examples:
  - context: string                      # Named Telegram or Mini App moment
    application: string                  # Concrete product behavior / UI action
    effect: string                       # Observable user state change

anti_examples:
  - description: string                  # Concrete misimplementation scenario
    why_it_fails: string                 # Mechanism-grounded failure reason

experience_stage_fit:
  entry: float                           # Onboarding / first contact
  activation: float                      # First reaction recorded
  recording: float                       # During the recording session
  scoring: float                         # Score reveal moment
  social_spread: float                   # Sharing / voting / referring
  recovery: float                        # Comeback after lapse or low score
  retention: float                       # Day 3-7 return behavior
  conversion: float                      # Upgrade to paid tier

surface_fit:
  telegram_message: float                # Telegram notification / message
  mini_app: float                        # Mini App UI state
  score_card: float                      # Post-reaction score screen
  share_asset: float                     # Share card / referral artifact
  voice_prompt: float                    # Agent voice note / audio cue
  push_nudge: float                      # Push notification / re-engagement message

user_state_effects:
  confidence: float                      # Coach's confidence in their voice
  urgency: float                         # Desire to act NOW
  clarity: float                         # Understanding of what to do
  safety: float                          # Psychological safety to try
  status: float                          # Perceived social standing
  belonging: float                       # Feeling part of the group
  curiosity: float                       # Pull toward the next action
  replay_desire: float                   # Want to try again / come back

ccp_workflow_fit:
  conscious_reactions_flow: float        # Core Conscious Reactions loop
  cbcs_accountability: float             # CBCS accountability calls / check-ins
  challenge_progression: float          # 7-Day Challenge cadence
  silent_referral: float                # Viral / word-of-mouth loop
  coach_os_deployment: float            # $99 tier full Coach OS
  premium_trust_architecture: float     # Premium brand perception
  onboarding_activation: float          # Free-to-first-reaction conversion
  social_economy: float                 # Jury / voting / ranking system
  content_extraction: float             # Reaction-to-content pipeline

activation_conditions: [string]         # 2-4 product-state conditions for activation
suppression_conditions: [string]        # 1-3 conditions where this must be suppressed
misuse_modes: [string]                  # 1-3 named implementation failure patterns

synergizes_with: [string]               # 2-5 existing experience primitive IDs (verified)
conflicts_with: [string]                # 1-3 existing IDs that degrade each other

implementation_targets:
  frontend_components: [string]         # React components, Telegram UI elements
  backend_rules: [string]               # CMF rules, scoring logic, trigger logic
  telemetry_events: [string]            # Analytics events to fire
  experiments: [string]                 # A/B tests to validate this primitive

experience_metrics:
  entry_rate: float                      # % users who enter after trigger
  react_rate: float                      # % who complete a reaction
  completion_rate: float                 # % who finish the full loop
  share_rate: float                      # % who share / refer
  comeback_rate: float                   # % who return after lapse
  day7_retention: float                  # % still active at day 7
  upgrade_signal: float                  # Correlation with paid conversion

crosswalk_id: string | null
crosswalk_note: string | null

notes: string
```

---

## FILE NAMING AND PLACEMENT

### Meaning Primitives
- Directory: `primitives/meaning/[family_name]/`
- Filename: `[PRIMITIVE_ID].yaml` (e.g., `PRM-HUM-009.yaml`)
- Family directory names use snake_case matching the enum values exactly

### Experience Primitives
- Directory: `primitives/experience/[family_name]/`
- Filename: `[PRIMITIVE_ID].yaml` (e.g., `EXP-TRG-001.yaml`)
- ID format: `EXP-[3_LETTER_FAMILY_CODE]-[3_DIGIT_NUMBER]`
- Family codes: TRG (trigger_timing), FRC (friction_ability), TRS (trust_branding), FBK (feedback_scoring), PRG (progression_replay), SOC (social_referral), SAF (safe_failure_recovery), PER (personalization_identity)

### Golden Examples (LOAD BEFORE WRITING — NO EXCEPTIONS)
- Meaning: `primitives/meaning/_golden/PRM-HUM-009.yaml`
- Experience: `primitives/experience/_golden/EXP-TRG-001.yaml`
- These are calibration anchors. Every agent must load them before writing their first primitive of a batch.

---

## ERROR HANDLING

- **Missing audit file**: STOP. Report the exact missing path. Do not improvise content.
- **Missing book file**: STOP. Report the exact missing path. Do not proceed. The primitive cannot be written without the book.
- **Book is too large to read in full**: Read the chapters most relevant to the primitive. At minimum, read the chapter the audit refers to AND one adjacent chapter. Log what you read in the Book Verification Log.
- **Primitive not found in catalog**: Check `Primitive_Packets_and_Registry_Spec.md` Section 6. If truly absent, create a new ID following the family convention and flag with `notes: "NEW — not in original catalog. Requires review before production use. Source: [audit_name]"`
- **Ambiguous family assignment**: Default to the family where the primitive's `phase_fit` or `experience_stage_fit` is strongest. Document the reasoning in `notes`.
- **Duplicate primitive across audits**: Use the HIGHEST MCDA score version as the canonical entry. List ALL source audits. Examine whether the two versions of the primitive are actually the same mechanism or subtly different. If subtly different, they may warrant separate IDs.
- **Float uncertainty**: Use 0.4 (context-dependent) rather than 0.5. Always add a note: `"Float calibration uncertain — [dimension]: needs review after benchmarking."`
- **Synergy ID not found in catalog**: Do not list it. Note the intended synergy in `notes` and flag for post-registry linkage.

---

## COMPLETION RECEIPT

After completing ALL primitives in a family batch, produce this receipt:

```
═══════════════════════════════════════════════════════
PRIMITIVE BATCH COMPLETION RECEIPT
═══════════════════════════════════════════════════════
FAMILY:                  [family_name]
PLANE:                   [meaning | experience]
PRIMITIVES ASSIGNED:     [count from template]
PRIMITIVES WRITTEN:      [count]
PRIMITIVES SKIPPED:      [count] — [reasons for each]
─────────────────────────────────────────────────────
MISSING SOURCES:         [list any books or audits not accessed]
BOOK VERIFICATION:       [confirm "Book Verification Log completed for: [titles]"]
─────────────────────────────────────────────────────
FLOAT CALIBRATION NOTES: [list any floats marked as uncertain + why]
CROSSWALK ENTRIES:       [count] — [list IDs]
NEW PRIMITIVES ADDED:    [count] — [list IDs not in original catalog]
SYNERGY FLAGS:           [any synergies that couldn't be verified]
─────────────────────────────────────────────────────
QUALITY SELF-ASSESSMENT:
  - Did I read every source book referenced?    [YES / NO — if NO, explain]
  - Did I avoid 0.5 floats?                    [YES / NO — if NO, list which]
  - Are all examples CCP-workflow-specific?     [YES / NO — if NO, list which]
  - Are synergy IDs verified in catalog?        [YES / NO — if NO, list which]
─────────────────────────────────────────────────────
TIMESTAMP:               [ISO 8601]
═══════════════════════════════════════════════════════
```

**This receipt is NOT optional. It is how the operator verifies the batch quality before the registry is updated.**

---

## FINAL WARNING

> The primitive registry is the foundation of the entire CCP agentic stack.
> Benchmarks are built on it. Specs reference it. Coalitions are formed from it.
> A primitive written from memory, from audit summaries only, or from general coaching knowledge is **not a primitive** — it is a contamination.
>
> **READ THE BOOK. THINK DEEPLY. WRITE PRECISELY.**
> **If you struggle with the execution, say so. Do not fake completion.**
