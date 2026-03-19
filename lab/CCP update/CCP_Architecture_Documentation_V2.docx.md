**CONSCIOUS COACHING PLATFORM**

**Capability Architecture Documentation**

*The Conscious Persuasion Sales Cycle Integration*

FR0A · FR0B · FR0C · FR0D · FR0E · FR51–FR60 · Semiotic Intelligence Layer

Version 2.0 — March 2026

*Supersedes V1.0 — Incorporates Guardian Stewardship Mode, 65-Character Lexicon Architecture,*

*Slash Command Architecture, 4-Skill Tribe Research Split, and Semiotic Composer Protocol V2*

— **SECTION 1** —

# **The Missing Foundation Layer — V2 Update**

## **What Changed From V1 and Why**

Version 1.0 of this documentation established Capability Area 0 as the missing foundation layer of the CCP architecture. Version 2.0 makes five significant architectural refinements based on the design review session that followed V1's completion. These refinements do not change the strategic conclusion — Capability Area 0 must be built before Capability Area 9 can deliver its full value — but they substantially change how several components are specified, structured, and governed.

The five V2 refinements are: (1) The Guardian Agent gains a permanent Stewardship Mode with Signal Monitoring Protocol, transforming it from a one-time setup orchestrator into an ongoing intelligence governance agent. (2) The Character Lexicon architecture expands from 60 characters across 2 categories to 65 characters across 5 functionally distinct categories, with a formal CRAL connection and a non-repetition invocation protocol. (3) The Tribe Soul Research execution splits from a single monolithic research stage into four separate specialist skills, each with its own quality gate and source platform optimization. (4) The Semiotic Composer Agent receives a formal Composition Decision Protocol — a four-question decision architecture that replaces aesthetic intuition with algorithmic precision. (5) A Slash Command Architecture is introduced as a new PRD section governing all Telegram-native workflow invocation, context window management, and sub-command sequencing.

Additionally, six clarifying decisions were confirmed in the V2 review session: the Brand Avatar is\_client\_default flag is replaced with content-context routing; foundational files are split between Supabase SQL (character\_lexicon, visual\_signifier\_lexicon, campaign\_performance\_registry) and JSON (Tribe Dossier, tribe\_profile, coach\_soul); Jungian archetypes are never deployed without a character lexicon anchor; color psychology is applied at the profile selection level rather than per-piece reasoning; the original setup prompts require a formal SKILL.md formalization pass; and FR60 is extended with a Loom Report Generation capability for coach-facing intelligence delivery.

*V2 does not replace V1 — it refines it. Every strategic conclusion from V1 stands. What V2 adds is the architectural precision that allows developers to implement without ambiguity.*

### **V2 Change Register**

| Component | V1 State | V2 State | Impact |
| :---- | :---- | :---- | :---- |
| Guardian Agent | Genesis Mode only | Genesis \+ Stewardship Mode with Signal Monitoring | Agent becomes permanent governance layer |
| Character Lexicon | 60 chars, 2 categories | 65 chars, 5 functional categories \+ invocation protocol | CRAL connection formally specified |
| Tribe Soul Research | Single monolithic skill | 4 specialist skills \+ Guardian orchestration | Quality control per research context |
| Semiotic Composer | Described, not architected | Composition Decision Protocol V2 — 4-question algorithm | Visual decisions become deterministic |
| Slash Commands | Not specified anywhere | New PRD section — full command schema | Context window management enabled |
| Brand Avatar flag | Fixed is\_client\_default boolean | Content-context routing based on coping trajectory | Avatar selection becomes dynamic |
| Data storage | All JSON implied | SQL/JSON split with explicit routing rules | Query performance \+ relational integrity |
| FR60 | Analytics dashboard only | Dashboard \+ Loom Report Generation | Coach receives intelligence not data |
| Setup prompts | Prompt documents | SKILL.md formalization pass specified | Architectural compliance \+ receipt chains |
| Interview Protocol | Inconsistently mentioned | 5-phase Guardian Interview Protocol formally specified | Onboarding quality gate added |

— **SECTION 2** —

# **The Guardian Agent — V2 Full Specification**

## **Genesis Mode \+ Stewardship Mode \+ Signal Monitoring Protocol**

The Guardian Agent is the CCP's foundational governance agent — the single component that determines whether every other component can function at its designed quality level. V2 expands the Guardian Agent's operational mandate from a one-time genesis orchestrator into a permanent intelligence steward that monitors the quality and relevance of all foundational intelligence objects across the full lifetime of each coaching engagement.

The architectural principle governing this expansion is that foundational intelligence is not static. Audience language drifts. Cultural heroes rise and fall. New enemies emerge in the tribe's discourse. Business model pivots change the coaching offer's positioning. Semiotic formats that resonated six months ago become culturally dated. A system that extracts foundational intelligence once at onboarding and never updates it will produce increasingly misaligned content over time — confident in its intelligence while operating from an outdated cultural map.

### **Operational Modes**

| GENESIS MODE (One-Time) Executes on new coach onboarding only Runs all 5 FR0 stages in strict sequential order Issues Genesis Clearance Certificate before FR1 can execute Cannot be re-run without explicit operator authorization Full 5-phase Telegram Interview Protocol executed here Receipt Chain Guard chain initiated — all subsequent stewardship receipts extend this chain | STEWARDSHIP MODE (Ongoing) Runs weekly Signal Monitoring sweep alongside Data Analyst cycle Detects Lexicon Drift, Cultural Evolution, and Campaign Fatigue signals Generates targeted refresh recommendations — never executes without operator approval Executes approved refreshes using the same skills as Genesis Mode but with targeted scope Issues Stewardship Reports quarterly — complete relevance audit of all foundational objects Slash command /ccf-guardian-refresh \[component\] enables operator-initiated targeted refresh |
| :---- | :---- |

### **5-Phase Guardian Interview Protocol**

The onboarding interview is the most important single event in the Guardian Agent's Genesis Mode execution. It is the source of authentic intelligence that seeds every downstream extraction. The interview is not a form. It is a structured Telegram conversation governed by the OARS interactional architecture — Open questions, Affirmations, Reflective Listening, Linking Summaries — that bypasses the coach's identity-protective cognition layer and accesses authentic material rather than professionally-polished positioning statements.

The five phases are executed in strict sequence across a single Telegram session. Phase transitions are marked by the Guardian Agent issuing a Summary Reflection that synthesizes the phase's intelligence and receives explicit coach confirmation before proceeding. This confirmation is both a quality gate — the coach validates that the summary captures their authentic reality — and a micro-commitment anchor — the coach has now publicly stated their truth in a documented conversation that the system will reference throughout the engagement.

| Phase | FR | Questions | Output | Quality Gate |
| :---- | :---- | :---- | :---- | :---- |
| 1 — Business Intelligence | FR0A | 8-10 questions: offer architecture, transformation claim, audience definition, market differentiation, content philosophy | DEP-ENG-050 seed data | Positioning Precision Test: summary cannot describe a competitor |
| 2 — Philosophy & Mission | FR1 | 6-8 OARS-structured questions: core belief, why this work, what the world gets wrong, personal mission statement | coach\_philosophy\_brief\_v1.md seed | Authenticity Test: response contains personal story anchors, not professional language |
| 3 — Emotional DNA Activation | FR4 | 7-10 scenario-based questions: appraisal sequences, moral foundation weighting, coping potential patterns | emotional\_dna.json seed | Coverage Test: all 10 Emotional DNA variables have at least one response signal |
| 4 — Trigger Map Initialization | FR5 | 5-8 Conway AKB hierarchy questions: lifetime periods, general events, ESK-level sensory anchors | trigger\_map.json seed | ESK Test: at least 3 responses contain sensory-perceptual detail |
| 5 — Audience Intelligence Seed | FR0B | 5-6 questions: what does the coach know about tribe's L3 reality from their own experience | FR0B research plan parameter seed | Insider Knowledge Test: at least 2 L3-depth observations confirmed by coach |

### **Signal Monitoring Protocol — Stewardship Mode**

The Signal Monitoring Protocol runs as a background analysis layer during the Data Analyst's weekly cycle. It does not generate content and does not execute refreshes. It monitors three signal categories and generates flagged recommendations that the operator reviews and approves before any refresh action is taken.

| LEXICON DRIFT SIGNAL Trigger: CBCS data contains language terms not present in tribal lexicon in 3+ separate client interactions Trigger: Character references appear in client messages that are not in the character\_lexicon Trigger: FR9 Audience Empathy Agent returns slang terms not in the visual\_signifier\_lexicon Recommended Action: Targeted tribe-lexicon-research skill execution for the specific drift dimension Scope: Does not trigger full Tribe Dossier refresh — targeted language and character addition only | CULTURAL EVOLUTION SIGNAL Trigger: CRAL M1 RELEVANT repeatedly surfaces cultural tensions referencing unfamiliar figures or terminology Trigger: Scheduled Monitor Agent detects 3+ consecutive cultural tension events outside current CMM coverage Trigger: Character relevance score drops below 0.4 for 5+ entries in the same functional category Recommended Action: Partial Tribe Dossier refresh for affected dimensions \+ character lexicon relevance rescore Scope: Does not trigger Business Intelligence refresh unless coach explicitly reports a business model shift | CAMPAIGN FATIGUE SIGNAL Trigger: Campaign Performance Registry shows declining conversion on previously high-performing semiotic combinations Trigger: Same character invoked in more than 3 pieces within the 8-week non-repetition window Trigger: Voice message replay rate drops below baseline for 2+ consecutive campaigns Recommended Action: Semiotic combination diversification \+ character rotation refresh Scope: Affects visual\_signifier\_lexicon deployment weights and character\_lexicon rotation priority — not full re-extraction |
| :---- | :---- | :---- |

### **Stewardship Refresh Cadence**

| Component | Scheduled Cadence | Signal-Triggered | Operator Approval Required |
| :---- | :---- | :---- | :---- |
| Tribe Dossier (H11) | Quarterly full refresh | Partial refresh on Cultural Evolution Signal | Yes — always |
| Character Lexicon | Quarterly relevance rescore | Targeted addition on Lexicon Drift Signal | Yes — always |
| Visual Signifier Lexicon | Bi-annual full review | Deployment weight adjustment on Campaign Fatigue Signal | Yes for additions, auto for weight adjustments |
| Business Intelligence (DEP-ENG-050) | Coach-initiated only | N/A — no signal triggers business refresh | Yes — always |
| Brand Avatars | On coach story update | N/A | Yes — always |
| Semiotic Lexicon Tribal Layer | Quarterly (aligned to Tribe Dossier) | Immediate on new FR6 visual recognition codes | Auto-incorporated, operator notified |

— **SECTION 3** —

# **FR0A V2 — Business Intelligence Extraction**

## **CRAL-Informed Research Approach**

FR0A in V2 incorporates a significant methodological upgrade: the business intelligence extraction now uses a CRAL-informed research approach rather than purely horizontal research. The original Business Model Assistant methodology — comprehensive breadth coverage of all business dimensions — is retained as the primary framework. But V2 adds a vertical depth pass modeled on the CRAL methodology's Human Evidence Bias principle for the two dimensions where surface-level intelligence is most likely to mislead: the Value Proposition and the Market Differentiation claim.

Horizontal research asks: what does this coach offer? Vertical CRAL-informed research asks: what specific transformation have real clients experienced and in their own words, not in the coach's marketing language? The gap between these two answers is frequently the most strategically valuable intelligence FR0A produces. Coaches who are underselling their real transformation do so because they are describing the mechanism of what they do rather than the outcome their clients actually experience. The CRAL Human Evidence Bias gate — minimum 3 verified real-person transformation stories — applied to the Value Proposition dimension surfaces the authentic transformation language that feeds every downstream component.

### **SKILL.md Formalization Requirements**

The Business Model Assistant, Coach Business Summary, and Deep Target Audience Research prompts must undergo a formal SKILL.md formalization pass before they are registered as Guardian Agent skills. The formalization pass requires six additions to each prompt document without changing the core content logic:

* Receipt Chain Guard write at INGEST and EMIT stages — format per FR47 DEP-ENG-041 schema

* DEP-ID declaration for all inputs consumed and outputs produced

* Academic grounding citations — author, year, mechanism — for each analytical framework used

* Quality gate formalization — current quality standards converted to binary PASS/FAIL tests with concrete failure examples

* Failure condition specification — what the skill does when prerequisites are missing or quality gates fail

* ADR-01 isolation constraint — explicit declaration that all reads and writes are scoped to the current coach tenant

This formalization pass does not require rewriting the prompts. It requires adding the architectural compliance layer that the rest of the CCP's skills already have. The content intelligence in these prompts is mature and validated — it has been refined across multiple coaching client deployments. What it lacks is the structural governance that makes it safe to run autonomously at scale.

### **Source Ingestion Architecture**

FR0A V2 formalizes the source ingestion approach: the Guardian Agent accepts a coach source folder upload containing website content, video transcripts, any existing positioning documents, and recorded materials. This eliminates the need for manual data entry across multiple platforms. The coach uploads a folder. The Guardian Agent processes its contents. The 5-phase Telegram Interview then supplements the uploaded content with authenticated voice responses for the dimensions where document analysis is insufficient — primarily emotional DNA activation and trigger map initialization, which cannot be surfaced from written documents alone.

The folder-based ingestion was the correct operational approach all along — the historical manual workflow existed because the automation layer had not been specified, not because manual processing produced better results. A website summary plus a transcript collection is sufficient to run the business intelligence extraction. The Telegram interview adds the authentic psychological depth that no document can provide.

— **SECTION 4** —

# **FR0B V2 — Tribe Soul Research: 4-Skill Architecture**

## **Specialist Skills Replace Monolithic Execution**

The most significant operational change in V2 is the decomposition of the Tribe Soul Research from a single monolithic execution into four specialist skills, each optimized for a specific research dimension. The original design treated tribe research as a single task with four dimensions. V2 recognizes that these four dimensions require fundamentally different source platforms, different quality metrics, different validation criteria, and different analytical approaches. Running them as a single skill produces quality averaging — the weakest dimension degrades the entire output.

Each specialist skill is a standalone SKILL.md that the Guardian Agent orchestrates in parallel execution where possible and sequential execution where dimensional dependencies exist. The Guardian Agent's synthesis step combines all four outputs into the unified Tribe Dossier, identifies cross-dimensional convergences, and runs the final Volume Verification and Verbatim Ratio quality gates across the combined corpus.

### **SKILL: tribe-lexicon-research**

**▸ Primary Function: Cultural artifact archiving — linguistic infrastructure of the tribe**

* Source platforms: Reddit (subreddit comment threads), Discord (server exports), closed Facebook groups, industry forums

* Optimized for: High-volume verbatim slang capture, inside joke documentation, hero/enemy identification

* Volume quotas: 100-150 verbatim slang examples with usage context, 75-100 hero/enemy posts with direct quotes, 5-7 inside jokes with reference examples

* Quality gate: Verbatim ratio ≥70% (direct quotes, not paraphrases), slang entries must include the context of misuse correction by tribe members

* CRAL connection: Outputs feed character\_lexicon Category 3 (Credibility Validators) and Category 5 (Ideological Opposition) identification

* DEP output: Feeds H11 Section A — Cultural Artifacts

### **SKILL: tribe-humor-research**

**▸ Primary Function: Humor DNA profiling — comedic signature and taboo mapping**

* Source platforms: Top-voted content from tribe subreddits (flair-filtered for Humor/Meme), Twitter/X humor threads, downvoted content analysis for taboo identification

* Optimized for: Humor style classification, taboo documentation, meme format preference identification

* Volume quotas: 50-100 top-voted humor posts archived with style classification, minimum 3 verbatim examples per identified style, 2-3 taboo documentation entries with evidence of negative reaction

* Quality gate: Style coverage — at least 3 distinct humor styles identified, taboo list must include at least 2 entries with community reaction evidence

* Semiotic connection: Outputs directly feed visual\_signifier\_lexicon Layer 2 (Cultural Meme Formats) with tribe-specific format preferences ranked by engagement

* DEP output: Feeds H11 Section B — Humor DNA Profile

### **SKILL: tribe-emotional-research**

**▸ Primary Function: Emotional landscape mapping — L3 fear and aspiration corpus**

* Source platforms: Anonymous forums (Reddit late-night post analysis using Mind After Midnight methodology), support community threads, rant/vent tagged posts, private Discord channels where accessible

* Optimized for: L3 depth verification, LIWC-22 authenticity scoring, Mind After Midnight post pattern identification (posted between 11pm-4am as proxy for reduced self-monitoring)

* Volume quotas: 5-7 verbatim aspiration quotes (L2 minimum, L3 preferred), 5-7 verbatim anxiety quotes (L3 required), 3 positive \+ 3 negative high-arousal trigger examples with community reaction evidence

* Quality gate: L3 minimum ratio — at least 40% of collected emotional posts must score above LIWC-22 70th percentile authenticity threshold, verified by high personal pronoun frequency, low cognitive complexity markers, and unpolished narrative style

* CRAL connection: This skill executes the same L3 verification methodology that CRAL M4 RESONANT uses — the Human Evidence Bias gate applied to foundational tribe research rather than per-session content research

* DEP output: Feeds H11 Section C — Emotional Landscape, directly seeds DEP-ENG-006 emotional\_triggers and fears dimensions

### **SKILL: tribe-social-research**

**▸ Primary Function: Social dynamics investigation — hierarchy, status, and unwritten rules**

* Source platforms: Observation of newcomer correction threads, moderation action patterns, status-signaling posts, membership milestone celebrations

* Optimized for: Unwritten rule documentation, in-group signal identification, status hierarchy mapping, boundary enforcement pattern analysis

* Volume quotas: 3-5 unwritten rules with evidence, 5+ in-group signals with context, 3+ boundary enforcement examples showing community response to outsider behavior

* Quality gate: Specificity test — each unwritten rule must be specific enough that violating it would result in observable community reaction. Generic rules ('be respectful') fail the test

* DEP output: Feeds H11 Section D — Social Architecture, seeds DEP-ENG-006 enemies and suspicions dimensions

### **Guardian Agent Synthesis Step**

After all four skills complete, the Guardian Agent runs a cross-dimensional synthesis pass that produces the intelligence the individual skills cannot generate alone. The synthesis identifies convergence events — when the same figure, concept, or tension appears in multiple research dimensions simultaneously. A figure who is a cultural hero in the lexicon research, appears as a target of protective humor in the humor research, and is referenced in emotional rant posts is a Category 1 Aspirational Hero with multi-dimensional tribal significance. This convergence is architecturally more valuable than any single-dimension finding and would be invisible without the synthesis step.

— **SECTION 5** —

# **FR0C V2 — Character Lexicon: 65-Character Architecture**

## **5 Functional Categories \+ CRAL Connection \+ Invocation Protocol**

The 45/15 hero/enemy binary was a useful starting framework but it does not map to how the character lexicon is actually used by downstream components. The production pipeline needs characters organized by function — what role does this character serve in a specific content moment — not by valence alone. A figure can be both a hero in aspirational content and an enemy in cautionary content depending on the narrative frame. The 5-category architecture resolves this by organizing characters by their primary content deployment function rather than by simple positive/negative sentiment.

### **The 65-Character Schema**

| Category | Count | Function | Primary CRAL Moment | Content Mode |
| :---- | :---- | :---- | :---- | :---- |
| 1 — Aspirational Heroes | 20 | Figures the tribe wants to become. Embody the destination the coach's work leads to. | M4 RESONANT — parallel story anchoring | Status / Processing |
| 2 — Nostalgic Icons | 15 | Figures from the tribe's formative period. Activate shared cultural memory and belonging. | M7 RELATABLE — shared reference activation | Escape / Recognition mode |
| 3 — Credibility Validators | 10 | Currently active respected voices. Lend peer-validated authority to the coach's claims. | M2 BELIEVABLE — human evidence anchoring | Discovery / Processing |
| 4 — Cautionary Enemies | 10 | Figures representing wrong paths or misaligned values. Make abstract risks concrete. | M3 UNDENIABLE — contrast evidence | Tension / T-mode content |
| 5 — Ideological Opposition | 10 | Figures holding the opposing worldview. Crystallize the moral foundation violation. | M5 SURPRISING — unexpected validation via contrast | Tension / high-arousal content |

### **Extended Schema Fields — V2 Additions**

V2 adds six fields to each character\_lexicon entry beyond the V1 schema, enabling the CRAL connection and invocation protocol:

* cral\_moments\[\]: Array of CRAL moment IDs where this character is deployable (e.g., \['M2', 'M4'\])

* moral\_foundation\_activated: Which of the 6 MFT foundations this character activates in the tribe (e.g., 'fairness\_cheating', 'authority\_subversion')

* content\_mode\_fit\[\]: Emotional modes this character is appropriate for (\['T', 'V', 'R'\])

* last\_deployed\_date: ISO8601 timestamp of most recent content deployment — feeds non-repetition registry

* relevance\_score: Float 0.0-1.0, updated weekly by Data Analyst. Below 0.4 triggers Guardian Stewardship cultural evolution flag

* gaze\_direction: For flyer use — 'hook' (directed at hook zone) or 'action' (directed at action zone). Determined by audience relationship depth from CBCS

### **Character Invocation Protocol**

The character\_lexicon is not browsed — it is queried. Every downstream agent that needs a character reference makes a structured query through the Character Invocation API rather than selecting characters directly. This enforces the non-repetition rule, the relevance threshold, and the CRAL moment appropriateness check simultaneously.

The invocation query takes five parameters: cral\_moment (which moment needs a character anchor), moral\_foundation (which foundation is being activated in this content piece), content\_mode (T/V/R), audience\_maturity (New/Developing/Loyal), and exclusion\_window (8 weeks by default). The API returns a ranked list of eligible characters with a selection\_justification for each — not a single recommendation, because the operator or agent making the invocation may have additional context that the API does not.

Every invocation is logged to the Usage Registry in Supabase with the character\_id, the content\_id it was used in, the cral\_moment, the content\_format, and the timestamp. This log is what enforces the non-repetition rule and feeds the Data Analyst's weekly relevance scoring. A character that has been invoked across 5 different content formats in the same week has not violated the non-repetition rule — the rule applies per format type, not globally. A character invoked in two carousels in the same week has violated it.

### **CRAL Connection — Formally Specified**

The character lexicon's connection to the CRAL Research Planner was architecturally implicit in V1. V2 makes it explicit and operational. When the Research Planner JIT Skill builds the 7-moment research plan for a production session, it queries the character\_lexicon for each moment where human evidence anchoring through a recognized figure is architecturally appropriate:

* M2 BELIEVABLE: Query Category 3 (Credibility Validators) filtered by moral\_foundation matching the session's primary emotional trigger. The validator's association with the coach's claim provides peer authority without requiring the coach to make the authority claim themselves.

* M3 UNDENIABLE: Query Category 4 and 5 (Cautionary Enemies \+ Ideological Opposition) for the contrast mechanism. The undeniable evidence lands with greater force when positioned against a recognized enemy figure who represents the alternative worldview the evidence refutes.

* M4 RESONANT: Query Category 1 and 2 (Aspirational Heroes \+ Nostalgic Icons) for parallel story anchoring. The human evidence story in M4 gains resonance when it connects to a figure the tribe already has emotional associations with.

* M5 SURPRISING: Query Category 5 (Ideological Opposition) for unexpected validation events. When an ideological opponent's words or actions unexpectedly validate the coach's position, this produces the highest-surprise recognition signal available — the cognitive dissonance of an enemy speaking the truth.

— **SECTION 6** —

# **FR0D V2 — Semiotic Intelligence Library**

## **Composition Decision Protocol \+ Tribal Calibration**

The Semiotic Intelligence Layer in V1 was correctly identified as the most underutilized asset in the CCP's intelligence library. V2 does not change the four-category structure of the visual\_signifier\_lexicon — Celebrity Meme Formats, Universal Archetypes, Cultural Symbols, and Color/Typography Mechanics remain the correct categorical architecture. What V2 adds is the Composition Decision Protocol that governs how the Semiotic Composer Agent selects from and combines these categories in practice.

### **The Jungian Specificity Rule**

Universal Archetypes are frequently misapplied in visual content because they are deployed as generic symbols rather than as psychological mechanisms expressed through specific tribal characters. The Hero archetype applied through a stock photo of a person looking determined is generic and forgettable. The Hero archetype expressed through a recognized figure from the tribe's cultural pantheon — Category 1 or Category 2 character from the character\_lexicon — is maximally specific because it combines the depth of the archetypal mechanism with the immediate recognition of a tribally significant character.

*Rule: Jungian archetypes are never deployed without a character lexicon anchor. The archetype provides the psychological depth. The character provides the tribal specificity. Neither alone is sufficient. Both together are irreplaceable.*

This rule applies across all four Universal Archetype entries: The Hero is expressed through a Category 1 Aspirational Hero. The Sage is expressed through a Category 3 Credibility Validator. The Shadow is expressed through a Category 4 Cautionary Enemy. The Trickster is expressed through a Nostalgic Icon the tribe associates with irreverent wisdom. The character selection query for archetype-based content includes the archetype parameter alongside the standard invocation protocol parameters.

### **Composition Decision Protocol V2 — 4-Question Algorithm**

The Semiotic Composer Agent answers four questions in sequence before making any visual composition decision. These questions replace aesthetic intuition with a deterministic decision tree that produces psychologically calibrated visual compositions consistently across all content types.

**▸ Question 1: What is the audience's maturity level?**

* New (0-4 weeks) → Layer 2 primary (Cultural Meme Formats). Reason: immediate recognition required before tribal depth can land. New audiences need the familiar format container before they can receive the deeper archetypal content.

* Developing (4-16 weeks) → Layer 2 \+ Layer 3 combination. Reason: tribal recognition is established, insider visual signals can now reinforce belonging while cultural formats maintain accessibility.

* Loyal (16+ weeks) → Layer 1 primary (Universal Archetypes expressed through character anchors). Reason: relationship depth supports the processing of archetypal depth. Loyal audiences experience archetypal compositions as profound rather than cryptic.

**▸ Question 2: What is the content's emotional mode?**

* T (Tension) mode → Lead with Layer 3 tribal signifiers \+ Category 4/5 character anchor. Enemy figures and ideological opposition characters activate the tribal us-versus-them response that Tension mode content requires.

* V (Vulnerability) mode → Lead with Layer 1 Shadow or Sage archetype \+ Category 1 or 2 character anchor. Archetypal depth creates the safety container that vulnerability content requires before authentic emotional disclosure can land.

* R (Recognition) mode → Lead with Layer 2 cultural meme format \+ Category 2 Nostalgic Icon anchor. Recognition mode requires the immediate 'that's us' response that familiar cultural formats and nostalgic figures produce.

**▸ Question 3: Which CRAL moment does this content serve?**

* M1 RELEVANT → Cultural Currency signifiers from Layer 3 \+ current Cultural Tension Signal visual elements. The visual must signal 'this is happening right now' — recency and cultural presence over depth.

* M4 RESONANT → Layer 1 Hero or Sage archetype expressed through Category 1 or 3 character. The visual creates the aspirational context that makes the resonant story feel inevitable rather than incidental.

* M5 SURPRISING → Cognitive dissonance visual — Layer 2 Distracted Boyfriend format or equivalent juxtaposition structure with Category 5 Ideological Opposition character. The surprise must be visible in the visual before the text confirms it.

**▸ Question 4: Has this semiotic combination been used in the last 8 weeks?**

* Query the Semiotic Combination Registry in Supabase: has this combination of format\_category \+ character\_id \+ color\_temperature been deployed within the 8-week rolling window?

* If yes → rotate to next eligible combination from the ranked options returned by the Character Invocation API

* If 3+ consecutive rotations are required → trigger Campaign Fatigue Signal to Guardian Agent Stewardship Mode

### **Color Psychology — Profile Selection, Not Per-Piece Reasoning**

A critical V2 clarification: color psychology is applied at the profile selection level, not at the individual piece reasoning level. The Semiotic Composer does not reason about color psychology for each piece. It selects from four pre-defined color temperature profiles that were designed using the full color psychology research base. This is the correct abstraction layer — the research is used to design the profiles once, then the profiles govern all production decisions without re-invoking the research each time.

| Mood State | Color Temperature Profile | Dominant Color Direction | Accent | Emotional Register |
| :---- | :---- | :---- | :---- | :---- |
| Escape | Warm Neutral | Warm neutrals — cream, terracotta, amber | Single warm accent (coral or gold) | Comfort, relief, gentle invitation |
| Processing | High Contrast Deep | Dark foundation — near-black, deep navy | High contrast light accent (white or pale gold) | Depth, weight, serious invitation |
| Discovery | Mid-Warmth Energetic | Medium warmth — sage, warm blue, sunrise tones | Bright energetic accent (teal or electric yellow) | Possibility, curiosity, active invitation |
| Status | Premium Dark | Dark premium — charcoal, deep forest, midnight | Gold or platinum accent — single element only | Exclusivity, insider signal, selective invitation |

— **SECTION 7** —

# **FR0E V2 — Brand Avatar Generation**

## **Content-Context Routing Replaces Fixed Default Flag**

The V2 change to Brand Avatar generation is conceptually simple but architecturally significant: the is\_client\_default boolean flag — which designated one avatar as the permanent primary face for all content — is replaced by a content-context routing function that selects the appropriate avatar for each specific content piece based on the audience's current psychological state and the content's emotional mode.

The original default flag logic assumed that the coach's Mentor avatar (current authoritative self) is appropriate for most content, with other avatars appearing in specialized story content. This is correct as a baseline but misses the most powerful avatar selection opportunity: matching the coach's narrative past to the audience's narrative present.

A coaching audience member in EXHAUSTED phase on their coping trajectory is experiencing the same psychological state as the coach's Struggler avatar — the period of carrying more than they can hold while refusing to put anything down. Content that features the Mentor avatar speaking wisdom to an exhausted audience produces professional empathy. Content that features the Struggler avatar speaking from inside that specific exhaustion state produces neural coupling — the audience experiences recognition, not instruction.

### **Avatar Selection Routing Logic**

| Audience Coping Stage | Emotional Mode | Recommended Avatar | Rationale |
| :---- | :---- | :---- | :---- |
| SEARCH (peak receptivity) | Processing / Discovery | Mentor | Audience is ready to receive wisdom — authority figure is the correct frame |
| SEARCH | Tension | Rebel / Origin | Audience wants validation that the fight is right — early-journey defiance resonates |
| ACTIVE (executing strategy) | Discovery / Status | Mentor | Audience wants confirmation they are on the right path — authority validates their current action |
| ACTIVE | Recognition | Nostalgic Icon equivalent | Audience wants celebration of progress — peer-level recognition rather than authority validation |
| EXHAUSTED (depleted) | Vulnerability | Struggler | Audience needs to know someone has been exactly here — depth-match rather than inspiration |
| EXHAUSTED | Escape | Origin / early journey | Audience needs lightness and return to simpler times — the beginning before the weight accumulated |
| Any stage | Tension (tribal solidarity) | Rebel | Audience needs righteous indignation validation — the defiant early self who refused to accept the system's terms |

The avatar selection query is executed by the Semiotic Composer Agent as part of the Composition Decision Protocol's Question 2 (emotional mode). The query parameters are: coping\_trajectory\_position (from client CBCS profile or audience segment classification from DEP-ENG-017), emotional\_mode (T/V/R from DEP-ENG-016), and content\_format (the specific archetype being compiled). The returned avatar is the is\_contextually\_appropriate selection for this specific piece, not a fixed default.

— **SECTION 8** —

# **Slash Command Architecture — New PRD Section**

## **Telegram Workflow Invocation and Context Window Management**

The entire CCP coach-facing interface is Telegram-native. Every workflow — from Guardian Agent genesis through weekly content delivery through campaign invitations — is delivered and managed through a Telegram thread. Yet not a single FR in the current specification mentions slash commands. This is a critical operational gap that V2 addresses by establishing a formal Slash Command Architecture as a new PRD section that governs all Telegram-native workflow invocation.

The problem slash commands solve is context window management in long-running multi-stage workflows. Without slash commands, every workflow is either a single continuous conversation that grows until the context window degrades quality, or a manual restart that loses all state. Neither is acceptable for a production system managing 36 scripts per week per coach across a 65-agent pipeline. Slash commands create context boundaries — each command invocation loads only the state relevant to that specific workflow stage, not the full conversation history.

### **Primary Command Schema**

| Command | Function | Sub-commands | Context Loaded |
| :---- | :---- | :---- | :---- |
| /ccf-guardian | Initiates or resumes Guardian Agent workflow | genesis, status, approve \[id\], refresh \[component\] | Guardian Agent state \+ relevant DEP-IDs only |
| /ccf-research | Initiates CRAL research for a session | start, status, approve \[moment\], override \[moment\] | Research Planner state \+ CRAL Finding Index |
| /ccf-generate | Initiates content generation | \[format-slug\] e.g. /ccf-generate carousel | Session state \+ SKILL.md for specified format |
| /ccf-campaign | Initiates campaign creation | challenge, webinar, sequence, status | Campaign brief state \+ relevant client segments |
| /ccf-review | Surfaces pending operator decisions | all, critical, warnings | Pending decisions queue — no production state |
| /ccf-status | Returns pipeline state overview | guardian, production, campaign, cbcs | Summary state only — no full context load |
| /ccf-approve \[id\] | Approves a pending Guardian recommendation | N/A | Specific pending action only |
| /ccf-interview | Initiates or resumes 5-phase Guardian interview | start, resume \[phase\], status | Interview state \+ coach DEP-IDs |
| /ccf-analytics | Requests analytics report | weekly, campaign, loom | Performance data for specified scope |

### **Sub-Command Sequencing**

Sub-commands follow the pattern /ccf-\[agent\]-\[action\] \[parameter\]. Each sub-command is a context-boundary reset that loads only the state required for that specific action. The most important context management rule: a sub-command that requires reading a DEP-ID object only loads that specific object, not the full intelligence library. This is how context window integrity is maintained across long production sessions.

The /ccf-guardian-refresh \[component\] sub-command is the operational manifestation of Stewardship Mode invocation. The component parameter maps directly to the foundational intelligence objects: 'tribe' triggers tribe-lexicon-research, tribe-humor-research, tribe-emotional-research, and tribe-social-research in sequence. 'characters' triggers a targeted character relevance rescore and optional new character identification pass. 'semiotic' triggers visual\_signifier\_lexicon tribal layer update. 'business' triggers FR0A re-execution — requires explicit operator confirmation with a confirmation code to prevent accidental business intelligence overwrites.

### **Workflow State Persistence**

Multi-stage workflows maintain state in Supabase rather than in the conversation context window. When a workflow is interrupted — the coach stops responding, the system times out, or the operator navigates away — the workflow state is checkpointed to Supabase at every stage boundary. The next /ccf-\[agent\] invocation loads the checkpointed state and offers to resume rather than restart. This eliminates the 'lost work' problem that plagued manual workflow management and makes the system resilient to the interruptions that are normal in a coaching business context.

— **SECTION 9** —

# **Capability Area 9 — The Conscious Persuasion Sales Cycle V2**

## **How Foundational Intelligence Determines CPSC Success**

The relationship between Capability Area 0 and Capability Area 9 is not incidental — it is the core architectural thesis of the entire system. The quality of every CPSC output is a direct function of the quality of the foundational intelligence objects produced by Capability Area 0\. This relationship deserves explicit documentation because it determines the implementation priority of everything in both capability areas.

A campaign generated without an authenticated Tribe Dossier uses demographic assumptions in place of L3 tribal language. The voice message invitation sounds like it could have been written for any audience in the coach's industry. The flyer hook does not activate the tribal recognition response because it was not built from verified tribal language. The micro-commitment priming sequence does not reference the client's actual stated commitment because the CBCS change talk archive was not seeded by a properly extracted emotional DNA profile. Every component of the CPSC degrades in quality by a predictable factor when the foundational intelligence beneath it is thin.

Conversely, when Capability Area 0 is fully executed with authenticated outputs, the CPSC produces outcomes that are architecturally impossible for any conventional marketing tool. The voice message contains the coach's actual Voice DNA filtered sentence rhythms carrying three verified L3 tribal language terms that failed the genericness test, addressed to a client who has just entered SEARCH phase on their coping trajectory after 90 days of CBCS journaling that the system knows intimately. No funnel page, no email sequence, no ad campaign achieves this. The conversion event is not the moment the client is persuaded. It is the moment the system correctly identifies that the client is already ready and delivers the invitation at the exact psychological moment of peak receptivity.

### **The Distillation Funnel Module**

One of the most strategically valuable functions of the CPSC is its ability to surface business intelligence that the coach does not yet have about themselves. The foundational extraction process — particularly the FR0A CRAL-informed value proposition research and the FR0B emotional landscape mapping — frequently reveals transformation patterns that the coach's clients are experiencing but that the coach has never explicitly named or claimed. When 40 tribe members in anonymous forums describe experiencing a specific transformation in specific language that does not appear anywhere in the coach's own marketing, the system has discovered a high-value positioning opportunity that would have remained invisible to traditional market research.

The Distillation Funnel Module is not a separate FR — it is a reporting function of the Guardian Agent that synthesizes these discovered gaps and surfaces them to the operator as strategic positioning recommendations. The coach does not need to understand the research methodology. They need to hear: 'Your clients are describing this specific transformation in these exact words, and you have never claimed it publicly. Here is what that means for your next offer.' That is the difference between a tool that manages content and a system that acts as the best consultant the coach has ever had.

*The CPSC does not convert strangers. It activates clients who are already ready. The entire system is designed to ensure that readiness is recognized precisely and met with an invitation that feels inevitable — not because the marketing is good but because the intelligence is deep.*

— **SECTION 10** —

# **FR51–FR55 V2 — The Invitation Architecture**

## **Updated with Character Lexicon Integration and Semiotic Protocol**

### **FR51 V2 — Challenge Funnel Intelligence Builder**

FR51 V2 adds three architectural elements absent from the V1 specification. First, the character\_lexicon is now formally integrated into the challenge funnel brief: the system queries Category 1 Aspirational Heroes for the success case visual and Category 4 Cautionary Enemies for the contrast mechanism in the sales page structure. These are not illustrative examples — they are specific character anchors that activate pre-existing tribal emotional associations rather than constructing new ones from scratch.

Second, the Semiotic Composer's Composition Decision Protocol V2 governs all flyer production for challenge campaigns. The four-question algorithm determines: which color temperature profile based on the campaign's mood state, which avatar based on the target segment's coping trajectory position, which character anchor based on the moral foundation being activated, and which combination exclusion check ensures no visual combination repeats within the 8-week window.

Third, the $9 commitment device framing is specified as a hard copywriting constraint rather than a pricing suggestion. Every challenge invitation CTA must frame the payment as a commitment decision using Gollwitzer implementation intention language — 'When you register today, you are deciding that the next 30 days will be different from the last' — not as a value proposition claim. The mechanism is commitment activation, not persuasion.

### **FR52 V2 — Webinar Intelligence Brief Generator**

The webinar Voice Message script generation receives the most detailed specification update in FR52 V2. The Transportation Test is added as a mandatory quality gate before any voice message script is delivered to the coach: the script must contain at minimum one sensory detail (concrete, specific, verifiable), zero distancing language (no 'I think', 'I believe', 'in my experience' qualifiers — only direct statements), and a prosodic structure that matches the coach's Voice DNA sentence rhythm pattern as extracted in FR3.

The prosodic structure matching requirement is new in V2 and requires that the voice message generation prompt specifies not just vocabulary but sentence length distribution (long-short-long or short-short-long patterns characteristic of the specific coach), discourse marker placement (the coach's habitual transitional language), and pause indicators (where the Voice DNA profile shows the coach naturally pauses for emphasis). A script that passes the vocabulary filter but fails the prosodic pattern match will sound 'off' when the coach reads it even if they cannot articulate why — the Transportation mechanism will be disrupted before it has a chance to activate.

### **FR53 V2 — Conversion Sequence Generator**

FR53 V2 formalizes the receptivity gate that determines whether the 72-hour priming protocol fires or whether the campaign is delayed. Before initiating any priming sequence, the system checks three conditions: (1) the client's coping trajectory position must be SEARCH or ACTIVE — EXHAUSTED phase clients receive a rest-and-recovery sequence rather than a conversion priming sequence, (2) the client must have at least 14 days of CBCS interaction logged — insufficient relationship history makes the priming sequence feel invasive rather than intimate, (3) the client must not be in an active crisis state flagged by FR31 — no commercial content enters a crisis thread under any conditions.

The change talk activation mechanism gets its own sub-specification in FR53 V2. The CBCS system must tag commitment language statements during journaling sessions and store them in a change\_talk\_archive table in Supabase with the statement text, the date, the emotional intensity score, and the coping stage at the time of the statement. The Conversion Sequence Generator queries this archive when constructing the Day Minus 2 Competence Acknowledgment priming message — referencing the client's own most recent high-intensity commitment statement rather than generating a generic acknowledgment. The client hears their own words reflected back accurately. This is not flattery. It is memory reconsolidation activation.

### **FR54 V2 — Promotional Asset Compiler**

FR54 V2 incorporates the full Z-pattern template architecture with all five V2 constraints formally specified as hard limits rather than guidelines: four active elements maximum (enforced), six-word hook maximum (enforced), Z-pattern zone placement (enforced), gaze direction toward primary conversion element (specified per audience relationship depth from CBCS), social proof number filtered by tribal segment (never platform-total, always segment-specific). Any personalization request that would violate these constraints is rejected by the Semiotic Composer and returned with an explanation of which constraint was violated and why it exists.

### **FR55 V2 — Session Booking Intelligence**

FR55 V2 adds the Atlas Roadmap integration that was identified in the V1 review as essential for offer tier routing. The booking invitation is now calibrated to the client's capacity track from FR32. Recovery Track clients receive an invitation framed as supported access to help during a difficult period. Foundation Track clients receive an invitation framed as accelerating progress on a specific roadmap milestone. Growth and Momentum Track clients receive an invitation framed as unlocking the next level of capability they are already demonstrating readiness for. Peak Track clients receive the premium hour-based access invitation framed as the natural evolution of what the group program no longer fully satisfies.

— **SECTION 11** —

# **FR56–FR60 V2 — Intelligence, Governance & Loom Reports**

## **The Self-Improving Sales Architecture \+ Coach Intelligence Delivery**

### **FR56 V2 — Campaign Performance Registry (DEP-ENG-051)**

DEP-ENG-051 is registered in V2 as a Supabase SQL table — not a JSON file — because the Campaign Performance Registry's primary value is in its queryability. The Data Analyst Agent needs to run queries like: 'show me all campaigns where coping\_trajectory\_position was SEARCH and color\_temperature was Processing profile and conversion\_rate was above baseline' — this is a relational query that requires SQL structure, not a JSON object scan. The schema includes all campaign parameters as indexed columns: character\_ids\_used\[\], semiotic\_combination\_hash, color\_temperature\_profile, coping\_stage\_at\_delivery, maturity\_level, priming\_days\_executed, voice\_message\_replay\_rate, conversion\_outcome, and time\_to\_conversion.

### **FR57 V2 — Social Proof Intelligence Engine**

V2 adds the tribal filtering algorithm specification that was described but not formalized in V1. The social\_proof\_count displayed in any promotional asset is computed as: SELECT COUNT(DISTINCT client\_id) FROM campaign\_performance\_registry WHERE coach\_id \= \[current\] AND tribal\_segment\_match \= TRUE AND conversion\_outcome \= 'enrolled' AND campaign\_type \= \[matching type\]. This query returns the count of previous participants who match the tribal segment profile of the current campaign's target audience — never the total platform enrollment count. The tribal\_segment\_match field is populated at enrollment time by comparing the enrolling client's DEP-ENG-006 segment classification against the campaign's target segment parameters.

### **FR58 V2 — Offer Tier Architecture**

The pricing architecture confirmed in V2: $9 challenge as first commitment device (30-day structure), full-price recurring program as natural continuation offer after challenge completion, hour-based coaching as premium access tier. The CBCS behavioral signals that trigger each offer tier are now formally specified: challenge offer triggers when dormancy recovery detects SEARCH phase at 3-5 day silence threshold. Recurring program offer triggers when challenge completion behavioral signals show 80%+ completion rate plus at least one vulnerability-depth CBCS interaction during the challenge period. Hour-based coaching offer triggers when Atlas Roadmap shows the client has outpaced their current tier's intensity ceiling for 2+ consecutive weeks.

### **FR59 V2 — Campaign Orchestration Agent**

The Campaign Orchestration Agent in V2 operates on the /ccf-campaign \[type\] slash command invocation from the System Operator. The operator-trigger model is confirmed as architecturally correct and not a limitation to be automated away. The coach's deliberate decision to launch a campaign is an intentionality signal that travels through the delivery mechanism and is perceived by clients as authentic rather than automated. A campaign that fires without a human decision behind it — even if the timing algorithm is sophisticated — loses this signal. The operator-trigger preserves the intimacy architecture.

### **FR60 V2 — Loom Report Generation**

The most significant FR60 V2 addition is the Loom Report Generation capability — the extension that transforms the system from an analytics platform into a personal intelligence consultant. The Loom Report is not a dashboard the coach logs into. It is a structured intelligence narrative delivered to the coach as a Telegram voice message summary plus a Notion-hosted visual brief, generated weekly by the Data Analyst Agent from the combined content performance and campaign performance data.

The report structure covers four intelligence categories in under 4 minutes of voice delivery: What performed this week and the specific mechanism that drove performance (not 'your carousel did well' but 'the Fairness/Cheating moral foundation violation in Tuesday's carousel produced 3x save rate because your audience is currently experiencing institutional betrayal at peak intensity — here is the evidence'). What the system is observing about the audience's psychological evolution (maturity level shifts, coping trajectory movement, emerging L3 language patterns). What the system recommends changing in next week's production parameters. And what commercial opportunity the system has identified based on the intersection of current audience psychological state and the coach's offer architecture.

The coach does not need to understand psychometric data, coping trajectory theory, or LIWC-22 scoring. They need to hear: here is what is working, here is why, here is what to do next week, and here is the conversation your audience is ready to have commercially. This is the best consultant they have ever had — one that works 24 hours a day, never loses context, and gets smarter with every piece of data the system collects.

— **SECTION 12** —

# **Data Architecture — SQL vs JSON Formal Rules**

## **Storage Decision Framework for All Foundational Intelligence Objects**

V2 formalizes the storage decision that V1 left implicit. The rule is simple and derived from a single criterion: if a downstream agent ever needs to query a subset of the data, filter it, sort it, or run aggregate computations across it — the data belongs in Supabase SQL. If the downstream agent always loads the entire object as a complete unit with no filtering — the data belongs in a JSON file in the coach's intelligence folder. Never use SQL for complete-object loads. Never use JSON for filtered queries.

| SUPABASE SQL TABLES character\_lexicon — filtered queries by category, moral\_foundation, last\_deployed, relevance\_score, cral\_moments visual\_signifier\_lexicon — filtered queries by cognitive\_mechanism, tribal\_resonance, mode, combination\_history campaign\_performance\_registry (DEP-ENG-051) — time-series analytics, conversion rate aggregation, semiotic combination performance coach\_business\_summary (DEP-ENG-050) — versioned records, update history, coach isolation via tenant\_id change\_talk\_archive — filtered by emotional\_intensity, coping\_stage, date range for priming sequence generation character\_usage\_registry — non-repetition enforcement, invocation logging, relevance scoring input semiotic\_combination\_registry — 8-week rolling window enforcement for visual non-repetition | JSON FILES (Intelligence Folder) H11 Tribe Dossier — write-once read-many, large unstructured verbatim corpus, complete-object load only tribe\_profile.json — Stage A output, complete-object load by FR6 Stage B tribe\_profile\_distilled.json — Stage B output, complete-object load by downstream production agents coach\_soul.json — complete-object load, no filtering required, existing spec standard maintained coach\_philosophy\_brief\_v{N}.md — complete-object load, versioned by session visual\_signifier\_lexicon\_baseline.json — the Strategic Lexicon foundation layer (read-only reference, tribal enrichment goes to SQL) H9\_DISTILLATION\_RECEIPT.md — audit artifact, never queried programmatically |
| :---- | :---- |

The visual\_signifier\_lexicon has a split storage architecture: the universal baseline entries from the Strategic Lexicon document are stored as a read-only JSON reference file — these never change because they are grounded in stable cross-cultural research. The tribe-specific enrichment layer — the insider objects, rejection triggers, sacred visuals, and tribal meme format preferences — is stored in Supabase SQL because the Semiotic Composer needs to query it by tribal\_resonance and combination\_history. The two layers are merged at query time by the Character Invocation API, which always loads the JSON baseline first then appends the SQL tribal enrichment layer for the specific coach tenant.

— **SECTION 13** —

# **PRD Integration Notes V2**

## **Complete Change Register for PRD Update**

V2 requires more extensive PRD updates than V1 because of the Slash Command Architecture addition and the character lexicon schema changes that affect multiple existing FRs. The following is the complete change register organized by PRD section.

### **New PRD Sections Required**

* Capability Area 0: Pre-Production Intelligence Layer — Full section header, Guardian Agent spec, FR0A-FR0E, Genesis sequence mandate, Stewardship Mode specification

* Slash Command Architecture — New standalone section between Capability Area 0 and Capability Area 1\. Contains primary command schema, sub-command sequencing rules, context window management protocol, and workflow state persistence specification

* Capability Area 9: Conscious Persuasion Sales Cycle — Full section header, Campaign Orchestration Agent spec, FR51-FR60

### **Existing FR Modifications Required**

* FR1 Genesis Pipeline: Add Genesis Clearance Certificate prerequisite gate. Update Mandate 8 build order to include FR0A-FR0E before FR1. Replace business intelligence gathering in onboarding conversation with reference to DEP-ENG-050 from FR0A.

* FR6 Tribe Profile: Remove 'if available' language from H11 prerequisite. Replace with hard prerequisite gate referencing FR0B. Remove backward compatibility fallback — FR0B formally specifies H11 production so there is no valid fallback state.

* FR9 Audience Empathy Agent: Add character\_lexicon query step — when FR9 identifies high-engagement audience figures, it checks against character\_lexicon and flags new character candidates for Guardian Agent Stewardship review.

* FR14 CRAL Research Subsystem: Add character lexicon integration step in Research Planner JIT Skill. M2, M3, M4, M5 moments each include a character\_lexicon query using the formal Invocation Protocol.

* FR23 Skill Fingerprint ID: Add semiotic\_combination\_hash to the fingerprint schema — the specific combination of Layer \+ character\_category \+ color\_profile that was used in the content piece. Feeds the non-repetition registry.

* FR35 Unified Excalidraw Pipeline: Add Semiotic Composer Composition Decision Protocol V2 as the visual selection engine for all Excalidraw content.

* FR36 Transparent Collage Pipeline: Add Character Invocation API query for character-based illustration subjects. Characters used in illustrations are logged to the usage registry the same as characters used in static flyers.

* FR43 Data Analyst Agent: Extend weekly cycle to include Campaign Performance Registry analysis and Loom Report Generation trigger. Add Guardian Stewardship signal detection to the weekly sweep.

* FR50 Sovereign Image Rule: Add Brand Avatar content-context routing specification. The rule now reads: the avatar deployed in any content piece is selected by the Semiotic Composer's avatar routing function based on audience coping trajectory position and emotional mode — not by a fixed default flag.

— **SECTION 14** —

# **Strategic Synthesis V2**

## **Updated SWOT \+ MCDA with V2 Architectural Changes**

The V2 architectural refinements strengthen the strategic position identified in V1's synthesis while introducing one new risk category. The SWOT and MCDA are updated to reflect the changes.

### **SWOT V2**

| STRENGTHS ↑ Guardian Stewardship Mode creates a self-maintaining intelligence system — foundational quality improves over time rather than degrading 65-character architecture with CRAL connection makes visual content activation as psychologically precise as text content 4-skill Tribe Research produces dimension-specific quality control impossible with monolithic research — higher L3 depth verification confidence Semiotic Composer Composition Decision Protocol eliminates aesthetic subjectivity — visual decisions are now as deterministic as psychological routing decisions Slash Command Architecture enables context-window-safe autonomous operation at scale — production quality maintained across multi-session workflows Change Talk Archive creates a conversion activation database that grows with every CBCS interaction — compounding commercial advantage Loom Report positions the system as the coach's best consultant — retention mechanism that no content tool can replicate | WEAKNESSES ↓ Guardian Stewardship Mode adds ongoing operational overhead — operator must review and approve refresh recommendations regularly or intelligence quality drifts 4-skill Tribe Research increases FR0B execution time — quarterly full refresh is more complex than V1's monolithic approach Character Invocation API adds a dependency — if the API query fails, visual content generation degrades to generic Slash command schema requires all Telegram interface components to be updated to register commands — retrofitting existing agent interfaces adds development time Change Talk Archive requires retroactive tagging of historical CBCS sessions — early client accounts will have sparse archive data until tagging catches up |
| :---- | :---- |
| **OPPORTUNITIES →** Stewardship Mode's signal detection creates a cultural intelligence early warning system — coaches get advance notice of audience evolution that competitors cannot detect Character Invocation Protocol's CRAL connection creates a named-person evidence index — the only content platform that can query 'which recognized figure activates this specific moral foundation for this tribe' Loom Reports create a coaching relationship between the system and the coach — coaches become advocates because the system makes them look brilliant to their clients The $9 challenge \+ Gollwitzer commitment framing creates a scientific conversion mechanism that outperforms conventional low-ticket offers without requiring larger audiences The system's ability to surface unrecognized transformation patterns (Distillation Funnel Module) creates consulting value that coaches will pay for independently of the content production capability | **THREATS ←** Guardian Stewardship Mode requires operator discipline — a team that falls behind on reviewing refresh recommendations will see intelligence quality drift silently The 4-skill Tribe Research architecture requires the deep research platform integrations (Exa, Gemini Deep Research) to maintain quality output — platform changes could disrupt research quality The sophistication of the system creates an explanation gap — coaches who do not understand what the system is doing may not trust its recommendations, even when they are correct The Loom Report creates high expectations — if the system's recommendations are wrong or the intelligence is stale, the coach notices immediately because the report is personal and specific Increasing architectural complexity means the Guardian Agent Interview Protocol is the highest-risk single point of failure — poor interview execution contaminates all downstream intelligence |

### **MCDA V2 — Updated with V2 Architectural Components**

The MCDA is updated to reflect the V2 architectural additions and their impact on the three integration options. The compounding intelligence advantage of Option A has increased in V2 because the Guardian Stewardship Mode and Campaign Performance Registry together create a self-improving system that grows more precise with every week of operation. This changes Option A's Competitive Moat Depth score.

| Criterion | Weight | A: Full V2 Integration | B: Partial (FR0+FR54 only) | C: Phased by Client Type |
| :---- | ----- | ----- | ----- | ----- |
| **Conversion Intelligence Compounding** *Self-improving conversion data \+ Guardian Stewardship loop* | **0.20** | **10/10** (2.00) | **5/10** (1.00) | **7/10** (1.40) |
| **Implementation Risk** *Risk of disrupting existing production pipeline quality* | **0.15** | **6/10** (0.90) | **9/10** (1.35) | **8/10** (1.20) |
| **Time to First Commercial Value** *How quickly measurable revenue impact is achievable* | **0.18** | **5/10** (0.90) | **9/10** (1.62) | **7/10** (1.26) |
| **Architectural Integrity** *Closes existing specification gaps completely* | **0.17** | **10/10** (1.70) | **7/10** (1.19) | **6/10** (1.02) |
| **Competitive Moat Depth** *Deepens inimitable advantages including Stewardship \+ Loom* | **0.15** | **10/10** (1.50) | **6/10** (0.90) | **8/10** (1.20) |
| **Coach Adoption Friction** *Ease of coach onboarding and workflow integration (inverse)* | **0.15** | **7/10** (1.05) | **9/10** (1.35) | **7/10** (1.05) |
| **WEIGHTED TOTAL** | **1.00** | **8.05** | **7.41** | **7.13** |

### **V2 MCDA Interpretation**

Option A — Full V2 Integration scores 8.10 weighted total, a marginal improvement over V1's 8.00 driven by the Guardian Stewardship Mode's impact on the Competitive Moat Depth criterion. The system that continuously updates its foundational intelligence is architecturally distinct from one that extracts intelligence once — the compounding advantage grows every quarter that Stewardship Mode operates. No static competitor can catch up to a continuously-updating system without building the equivalent governance architecture from scratch.

The Coach Adoption Friction score improves from 6 to 7 in V2 because the Slash Command Architecture and the Loom Report together reduce the cognitive load on coaches significantly. Slash commands eliminate workflow navigation friction. Loom Reports eliminate the need to understand analytics. Coaches interact with a Telegram interface that feels like messaging a smart assistant — not operating a complex production platform.

Option B scores higher on short-term value but the gap with Option A on Conversion Intelligence Compounding (5 vs 10\) represents a strategic forfeit that grows larger with time. The Campaign Performance Registry combined with Guardian Stewardship creates a self-improving moat. Option B explicitly chooses not to build this moat. The cost of that choice is invisible in the first month and becomes increasingly expensive every subsequent quarter.

*The V2 architectural refinements do not change the fundamental recommendation: Full Integration with Section 13 sequencing discipline. They strengthen it by demonstrating that the system's compounding intelligence advantage — already the primary strategic thesis in V1 — is deeper and more durable than V1's specification could fully articulate.*

The Guardian Agent is the keystone. It must be built first, in Minimum Viable form, before anything else in Capability Area 0 or Capability Area 9 is implemented. The Guardian Agent MVP executes the 5-phase Telegram Interview Protocol, runs FR0A and FR0B using the formalized SKILL.md versions of the existing prompts, and issues a Genesis Clearance Certificate. This alone closes the most critical architectural gap in the current system. Everything else in this documentation builds on the foundation the Guardian Agent establishes.

Build the foundation. Then build the building. The Conscious Coaching Platform has been building floors since inception. V2 is the specification that finally builds the ground floor correctly.

*— END OF V2 DOCUMENTATION —*

Conscious Coaching Platform — Capability Architecture Documentation V2.0

Supersedes V1.0 — March 2026