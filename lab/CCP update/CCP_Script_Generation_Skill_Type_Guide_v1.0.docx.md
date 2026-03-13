

**CONSCIOUS COACHING PLATFORM**

CCP Authoring Doctrine Series

**Script Generation**

**Skill Type Guide**

| Guide Type: Authoring Methodology | Governs: All CCF script skill authoring |  |
| :---- | :---- | :---- |
| **Version:** 1.0 | **Status:** Draft — Priority: HIGHEST | **Layer:** Architecture Layer 3 |
| **Supersedes:** No prior version — first formal authoring doctrine | **Dependency:** CCP Architecture Report V4.0 |  |

*The methodology layer that governs how every CCF script skill is authored, validated, and certified.*

*Templates produced without this guide are methodologically inconsistent.*

March 2026  ·  CCP Engineering Division

# **00  Preamble — What This Guide Governs**

**This guide is the authoritative methodology for authoring CCF script skills.** It governs every decision an author makes when building a Design Brief Template: what goes in Block A, how each arc phase is specified, how anti-draft intelligence is structured, how CRAL findings are mapped, and what quality standard must be met before Architecture Review submission.

This guide does not govern what content is produced. It governs how the instruction engines that produce content are built. A script skill author is not a content writer — they are building a compiler specification.

## **Where This Guide Sits in the Architecture**

| Layer 1 — Registry Foundation: Dependency Registry v4.0 \+ Adapter Registry v2.0 Layer 2 — Module Intelligence: Container Module Library (ecological adaptations, mood state matrices, anti-draft specimens) Layer 3 — Authoring Methodology: This guide. Governs how Layer 2 intelligence is translated into Layer 4 templates. Layer 4 — Template Library: Design Brief Template Library v1.2 (output this guide produces) Layer 5 — Compilation Engine: Builder Engine \+ JIT Skill Assembler v2.0 Layer 6 — Research Intelligence: CRAL subsystem (DEP-ENG-021/022) Layer 7 — Learning Loop: Fingerprint Archive \+ Maturity Promotion Protocol |
| :---- |

**Critical constraint:** A template produced without this guide is methodologically valid only by accident. Templates submitted for Architecture Review without following this guide will fail the Emotional DNA Integration Test.

## **How to Use This Guide**

1. Read Section I (Eight Architectural Mandates) before touching any template. The mandates are non-negotiable laws.

2. Read Section II (Template Anatomy) to confirm you understand the three-block structure and the variants-vs-invariants distinction.

3. Follow Sections III–VI in order when authoring Block A. These are sequential — the Causal Construction Sequence (III.4) requires the Three-Layer SPR Loading Protocol (IV) to have been completed first.

4. Apply Section V (Anti-Draft Architecture) after Block A is drafted. Anti-draft is not written into the template — it is what the template is designed to defeat.

5. Apply Section VI (CRAL Wiring Protocol) to complete field\_5b before Architecture Review submission.

6. Use Section IX (Emotional DNA Integration Test) as the final gate. If the test does not produce COMPLETE assembly status, the template is not ready.

# **I  The Eight Architectural Mandates**

The eight mandates below are the non-negotiable laws of CCF script skill authoring. Each carries a specific violation consequence documented in the Assembler's diagnostic protocol. No template may be submitted for Architecture Review without complying with all eight.

| \# | Mandate | Architectural Basis | Violation Detection | Consequence |
| ----- | ----- | ----- | ----- | ----- |
| **M-01** | **Negative Space Loads First.** DEP-ENG-004 is loaded absolutely first — before any positive generation constraint is active. The semantic repulsion field must be in place before positive constraints load. | negative-space-loader-adapter fires before irevc-adapter at Assembler Tier 1\. Mechanically enforced. Grounded in Ling et al. (2023): invalid examples must precede valid targets to produce semantic repulsion. | Assembler Tier 1 diagnostic. irevc-adapter firing before negative-space-loader-adapter \= architectural violation. | Level 3 coach-specific drift patterns survive into production outputs undetected. |
| **M-02** | **TTT Is Never Pre-Specified.** Temperature, Texture, and Tone are not compilation variables. No Block A or Block B field may contain a hardcoded TTT value. TTT is resolved at runtime by DEP-ENG-005 Authentication Certificate only. | Trigger-First Engine Inversion (Innovation 3). iRAV framework (Cooney, 2021): virality predicted by intensity of authentic emotional peaks — not average tone. Pre-specification produces average tone. | Block C check C-08. Assembler REJECTS any template containing a hardcoded TTT value. | Compiled skills are emotionally static. iRAV virality mechanism collapses. |
| **M-03** | **No Ghost Variables.** Every field that references a data source must carry a formal DEP ID registered in Dependency Registry v4.0. No template may reach Architecture Review with an unregistered input reference. | Specification gaming (Krakovna et al., 2022): unregistered data sources allow the Assembler to infer or synthesise inputs, producing specification-satisfying but intent-violating outputs. | Block C check C-01. DEP Resolution fails for any unregistered reference. | Ghost variable execution — technically plausible but architecturally invalid outputs. |
| **M-04** | **Templates Are Pure Data — No Subagents.** No template may contain routing logic, agent invocation instructions, conditional execution logic, or subagent embedding. All execution authority lives in agents that consume templates. | CCSB Two-Phase Architecture (Innovation 5). Conflating specification with execution corrupts both. | Assembler Tier 3 Ontological Boundary Violation diagnostic. Section flagged for regeneration. | Templates become brittle and non-deterministic. |
| **M-05** | **All Three Anti-Draft Levels Are Mandatory.** Every compiled skill must contain Levels 1 (Archetypal), 2 (Psychological Mode), and 3 (Coach-Specific). A template producing a skill missing any level receives PARTIAL\_AUTO status — never COMPLETE. | Contrastive Chain-of-Thought (Ling et al., 2023): positive-only examples allow surface pattern satisfaction while violating deep constraints. All three levels are required to close all three failure mode gaps. | Post-assembly quality gate. COMPLETE status requires all three levels present and populated. | Statistical mean-reversion survives into production outputs. |
| **M-06** | **CRAL Wiring Is Mandatory for v1.2 Templates.** Every v1.2 template must have a populated field\_5b CRAL Finding Map before Architecture Review. Every arc phase must carry a cral\_source field. DEP-ENG-021 must be listed in Block B field\_5 as CRITICAL tier\_2. | CRAL Architecture (V4.0). Research must be pre-addressed before compilation — not processed inside generation. The statistical centroid failure mode is partly caused by the agent improvising research context it was never formally given. | Block C C-09 (CRAL Coverage) and C-10 (Moment Object Completeness). | Compilation degrades to v1.1 source chain. Research at generation time. Statistical centroid risk persists. |
| **M-07** | **Psychological Adapters Are Never Encoded Inline.** The three psychological adapters — psych-routing-adapter, payload-masking-adapter, audience-maturity-adapter — are REGISTERED in Adapter Registry v2.0. Their logic must not be re-encoded inline in Block B field\_8 or field\_9. | Single source of truth principle. The template's inline version is never updated when the registry evolves, creating two competing and diverging specifications. | Adapter Registry version mismatch check during Architecture Review. | Template inline logic inherits stale routing rules that the registry has superseded. |
| **M-08** | **Emotional DNA Integration Test Before TESTED Promotion.** No template may be promoted from DRAFT to TESTED without passing the Emotional DNA Integration Test (Section IX). The test requires a complete compilation against real DEP data producing COMPLETE assembly status. | Maturity Promotion Protocol. SkillNet (Liang et al., 2026): curated skills with formalised quality gates produce 40% performance improvement. Skills promoted without gates produce zero compounding gain. | Fingerprint Archive maturity field. TESTED requires assembly\_report.json showing COMPLETE status against real DEP-ENG-003/004/006. | Draft-quality templates enter the active pipeline. Template Library does not improve with production cycles. |

# **II  Template Anatomy — Three-Block Structure**

Before authoring begins, the three-block structure and its variants-vs-invariants logic must be fully internalised. The most common authoring error is misclassifying Block A content as Block B, or encoding execution logic in what should be pure data.

| Block | Name | What It Contains | Who Fills It / When |
| ----- | ----- | ----- | ----- |
| **Block A** | **Structural Invariants** | Everything true of this archetype regardless of coach, mood state, cohort, or date. Arc phases and structural laws. Reasoning modules with ecological adaptations. Universal constraint rules. Archetype-invariant quality gates. | **Author** — once, before Architecture Review. **Immutable after TESTED.** Modified only by Architecture Review panel for TESTED+ templates. |
| **Block B** | **Compilation Variables** | Everything that varies per compilation: target format, coach identity, psychological routing context, input DEP IDs, adapter parameters, voice constraints, output artifact schema, psychological success criteria. | **Template author** pre-defines field structure and DEP references. **Builder Engine** populates values at runtime. Author never fills in specific values — only the schema. |
| **Block C** | **Compilation Validation Gate** | Pre-flight checks that run before any assembly begins. Zero generation — pure logical verification. CRITICAL failures return structured rejection JSON to Phase 1\. | **Template author** defines which checks apply and what constitutes failure. **Assembler** executes them at Tier 0\. |

| ⚠  Most common authoring error: encoding a runtime decision (mood\_state routing logic, TTT preference, coach-specific anti-draft) in Block A. Block A must be valid for ALL compilations of this archetype. If a statement is only true for some compilations, it belongs in Block B, the adapter registry, or is undefined (like TTT). |
| :---- |

## **The Variants-vs-Invariants Test**

| TEST: Is this statement true for every compilation of this archetype, regardless of coach, mood state, cohort, or date? YES → Block A. It is an invariant. NO → Block B (varies by compilation context) or Adapter Registry (varies by psychological state) or undefined (runtime value like TTT). Examples: "Stakes precede Result" → Block A (true for all Achievement Story compilations) "Hook leads with loss framing" → Block B / psych-routing-adapter (only true for prevention regulatory frame) "Temperature is TTT-04" → NOT in any block — runtime value, rejected by Block C C-08 "Use tribal vocabulary from DEP-ENG-007" → Block A (invariant directive); specific vocabulary → Block B field\_3 |
| :---- |

# **III  Block A Authoring Protocol**

Block A contains six fields for CCF script skills. Each has a distinct function, a distinct authoring methodology, and a distinct quality standard. They are authored in the sequence below — not in parallel.

## **3.1  Field 1 — Intent**

**What it is:** A procedural mandate stating the archetype's purpose and its Orchestrator routing value. It answers two questions: (1) What cognitive work does this archetype do for the audience? (2) Under what conditions should the Orchestrator select this archetype?

**Authoring rules:**

* The Intent must include a reason clause — not just what the archetype does, but why the audience needs it that cannot be served by any other archetype.

* The Orchestrator routing value must be explicit: emotional state tags and batch strategy function that trigger selection.

* The Intent must be falsifiable: if you cannot construct a scenario where this archetype should NOT be selected, the routing value is too broad.

| Intent Authoring Template: \[ARCHETYPE NAME\] surfaces \[psychological mechanism\] to \[audience cognitive function it serves\]. Exists because \[why this mechanism cannot be substituted with another archetype\]. Orchestrator routing value: load when batch strategy signals \[function\] AND authenticated emotional state registers \[emotion tags\]. Flag for human review if \[edge condition\]. |
| :---- |

| ⚠  Intent statements that use generic language ("to inspire", "to motivate") fail the falsifiability test. Every archetype "inspires" in some sense. The Intent must specify what only THIS archetype does. |
| :---- |

## **3.2  Field 4 — Trigger**

**What it is:** The formal activation condition. References DEP-ENG-005 Authentication Certificate and defines the TTT range at which this archetype is naturally appropriate.

**Authoring rules:**

* Always reference DEP-ENG-005 by ID. The Trigger depends on the authenticated emotional state — never on a hypothetical mood.

* State the TTT natural affinity range as an Orchestrator advisory — not a hard block.

* State the human review flag condition — the TTT or emotional state requiring human confirmation before auto-selection.

## **3.3  Field 6 — Action**

**What it is:** A single cognitive verb phrase defining the generation mode. One subject (the generation agent), one cognitive verb (compress, expose, invert, reveal, construct, etc.).

**Authoring rules:**

* One verb phrase only. If it contains more than one cognitive verb, split the archetype into two.

* The Action must be congruent with Field 7 arc phases. Misalignment between Action and arc structure is the first indicator of a structurally incoherent template.

* In v1.2: the Action must reference that research is resolved upstream via DEP-ENG-021, not at generation time.

| Good: *"Compress authenticated triumph experience into a 5-phase narrative arc. Each phase draws from its pre-addressed CRAL moment finding via DEP-ENG-021. Research is resolved upstream. Generation is execution, not processing."* Bad: *"Write an engaging story about a coach's achievement."* — Non-cognitive, non-architectural, non-falsifiable. Bad: *"Research the coach's background and then create compelling content."* — Violates M-06 (research at generation time) and M-04 (agent instruction in template). |
| :---- |

## **3.4  Field 7 — Method: The Causal Construction Sequence**

**What it is:** Named arc phases with structural laws. This is the most complex field in Block A — and the one where authoring errors are most consequential, because Field 7 is the primary input to the anti-draft architecture and the CRAL wiring map.

**The Causal Construction Sequence — 5 steps per arc phase:**

| STEP 1 — NAME THE COGNITIVE FUNCTION Ask: what cognitive state must the audience be in at the END of this phase, before the next phase begins? This is the audience's psychological condition that makes the next phase possible — the bridge between phases. It is not the content of the phase. Phase Type Cognitive Function What It Enables Stakes / Risk Threat activation The audience experiences personal relevance. Without threat activation, the mechanism phase has no urgency. Mechanism / How Causal understanding The audience can identify the lever. Without causal understanding, the Turn has no explanatory power. Turn / Pivot Cognitive revision The audience updates their prior belief. Without cognitive revision, the Result produces no conviction. Result / Evidence Evidential conviction The audience cannot refute the outcome. Without conviction, the Implication is inspiration, not transformation. Implication / Parallel Tribal self-recognition The audience sees themselves in the structural parallel. Activates SDT primary need — converts conviction into identity change.  |
| ----- |

| STEP 2 — IDENTIFY THE DEP SOURCE Ask: which DEP ID carries the primary intelligence for this phase? Every arc phase must draw its primary intelligence from a formally registered DEP ID. If the answer is "the generation agent will figure it out", the phase violates Mandate M-03 (no ghost variables). Phase Primary DEP Source What It Carries Stakes DEP-ENG-010 SoC Batch The coach's authenticated voice about the stakes. Must be derived, not synthesised. Mechanism DEP-ENG-010 \+ DEP-ENG-021\[M4\] SoC \= the voice. M4 RESONANT \= pre-structured narrative unit. Cross-referenced via Builder Engine Step 3.5. Turn DEP-ENG-021\[M5\] M5 SURPRISING IS the Turn in v1.2. Optimal incongruity finding pre-addressed by CRAL. Result DEP-ENG-021\[M6\] \+ DEP-ENG-005 M6 irrefutable evidence anchor. DEP-ENG-005 certifies result authenticity. Implication DEP-ENG-021\[M7\] constrained by DEP-ENG-006 L3 M7 tribal recognition anchor. L3 \= register gate (vocabulary constraint), not content source.  |
| ----- |

| STEP 3 — WRITE THE STRUCTURAL LAW The structural law is the invariant rule governing this phase's construction. Written as a constraint — not a preference. Must be falsifiable: you must be able to construct an output that violates it. Format: \[WHAT the phase must produce\] \+ \[DEP source it draws from\] \+ \[the constraint that cannot be violated\] \+ \[what happens if the constraint is violated\] Good structural law (Turn phase, Achievement Story): *"The Turn is a single identifiable frame — a date, a conversation, a decision, a specific observable event. M5\_SURPRISING IS the Turn finding: the counter-intuitive detail that should not have happened according to the audience's prior belief. A Turn that covers a period of time fails the cognitive revision function — the audience cannot locate the precise moment their prior belief breaks. Without that moment, the Implication has no specific anchor."* Anti-patterns (reject these): *"The Turn should be specific and memorable."* — Advisory, not law. No falsification criterion. *"The Turn should be written in a vivid, sensory style."* — Aesthetic preference, not structural law. *"The coach should describe what changed."* — Instruction to generation agent (M-04 violation). |
| :---- |

| STEP 4 — WRITE THE CRAL SOURCE MAPPING For every arc phase, specify: cral\_source: which CRAL moment finding(s) pre-address intelligence for this phase v1\_1\_source: what the phase drew from before CRAL (the v1.1 source chain) v1\_2\_source: what the phase draws from now (the v1.2 source chain) These are audit trail fields — not instructions to the generation agent. They exist so Architecture Review can verify the CRAL upgrade is a genuine architectural improvement, not a relabelling of the same intelligence. Quality test: For each CRAL moment mapped to a phase, ask: does this moment's finding eliminate a genuine research uncertainty that v1.1 had to synthesise or infer? If yes: the mapping is justified. If no: the CRAL source is decorative — remove it and keep the v1.1 source. |
| :---- |

| STEP 5 — WRITE THE GRACEFUL DEGRADATION PATH For every arc phase, specify what happens if its primary CRAL moment finding is absent. The degradation path must be specific (which v1.1 source chain?), logged (what flag?), and non-blocking (assembly continues). Phase Absent CRAL Moment Fallback Flag \+ Severity Stakes M2 or M3 DEP-ENG-010 SoC Batch only. Stakes land at generic difficulty, not specific prediction error. CRAL\_DEGRADED — HIGH for M2 absent. MEDIUM for M3 absent. Mechanism M4 DEP-ENG-010 SoC candidate passages. Narrative unit reconstructed from SoC alone. CRAL\_DEGRADED — HIGH Turn M5 Reconstructed from SoC. Loses counter-intuitive specificity and calibrated incongruity. CRAL\_DEGRADED — HIGH Result M6 DEP-ENG-010 \+ DEP-ENG-005 only. Result is asserted, not irrefutably anchored. CRAL\_DEGRADED — HIGH Implication M7 Constructed from DEP-ENG-006 L3 vocabulary. Achieves factual accuracy but not tribal recognition. CRAL\_DEGRADED — HIGH. M7 absence has highest impact on audience reception.  |
| ----- |

## **3.5  Field 8 — Structural Modules**

**Authoring rules:**

* **Distillation Funnel —** Specify all four laws (Compression, Distillation, Resonance, Anchoring) in archetype-specific form. In v1.2, update Cross-Input Collision from "DEP-ENG-003 ↔ DEP-ENG-006" to "DEP-ENG-021 (CRAL) ↔ DEP-ENG-003 (Voice)".

* **Contrastive Anchor —** Archetypal Failure Mode must be written prose (3–5 sentences), not description. The prose must be specific enough to be mistaken for a real output. See Section V for full Anti-Draft authoring protocol.

* **MCDA / Deliberation —** Specify evaluation domain and critic rules as yes/no questions against the output. Abstract criteria ("is it good enough") are not valid critic rules.

* **Mandatory adapter declarations —** List irevc-adapter and graceful-degradation-adapter as mandatory. In v1.2 also list cral-finding-router-adapter. Reference registry names only — not their logic.

## **3.6  Field 9 — Structural Constraints**

**Universal rules:** Written as prohibitions ("NEVER..."). Each must be falsifiable. Rules only true for some mood states belong in the adapter registry, not Field 9\.

**v1.2 universal rules to add:** (1) NEVER run research inside generation; (2) NEVER substitute CRAL findings for SoC voice material; (3) NEVER deploy M7\_RELATABLE without confirming tribal recognition test.

**Graceful degradation map:** Every DEP ID referenced anywhere in Block A or Block B must appear here. CRITICAL (halt if absent), IMPORTANT (degrade with flag), INFORMATIONAL (log only).

## **3.7  Field 11 — Structural Success Criteria**

**Authoring rules:** 

* Each gate must have: ID, source, check statement, binary pass condition, fail condition.

* Gates must be testable by the Assembler's critic pass — not by human editorial judgment.

* In v1.2 templates: add SG-06 (M2 deployed), SG-07 (M7 tribal recognition test), SG-08 (Step 3.5 conflict resolved).

* SG-07 pass condition references tribal recognition test — not factual accuracy. Factually correct implication that fails tribal recognition is a partial pass only.

# **IV  The Three-Layer SPR Loading Protocol**

**SPR (Semantic Pointer Register)** is the structured context the generation agent holds at the moment generation begins. The SPR loading protocol specifies the exact sequence in which the three primary data layers load, what each layer establishes, and what the author must verify before the next layer loads.

The SPR loading protocol is not an authoring step — it is the cognitive architecture the template is designed to produce. Every Block A and Block B field must serve the correct layer without corrupting the load order.

| ⚠  The load order is absolute and mechanically enforced at Assembler Tier 1\. Templates that implicitly assume a different load order (e.g., treating positive voice constraints as primary context) appear structurally complete but fail in execution because the semantic repulsion field is not established first. |
| :---- |

## **Layer 0 — Negative Space (DEP-ENG-004) — Absolute First**

| COGNITIVE FUNCTION: Semantic repulsion field establishment Negative Space is loaded first because it defines the boundary of the cognitive space before any positive instruction enters it. Without the repulsion field, the generation agent defaults to the statistical centroid of its training data — which always satisfies positive instructions while violating the spirit of voice authenticity. DEP-ENG-004 contains: The coach's cognitive load drift patterns — what they default to when uncertain The specific hedging constructions used in professional register Vocabulary items that are technically correct but feel performed rather than lived Structural shortcuts taken when emotional access is shallow What the author must verify before Layer 1 loads: Forbidden Vocabulary List is populated: exact strings, not general categories. "Avoid jargon" is not an entry. "leverage", "optimise", "unlock your potential" are entries. Cognitive load drift pattern documented: at least one specific structural pattern the coach defaults to under cognitive load, documented with an example. Hedging constructions identified: at least two specific hedging constructions listed as forbidden patterns. Template author responsibility: Block B field\_9 must reference DEP-ENG-004 by formal DEP ID. The author must NOT write specific forbidden vocabulary into the template — this would hardcode coach-specific data into an archetype-invariant field. |
| :---- |

## **Layer 1 — Positive Space Voice DNA (DEP-ENG-003) — Second**

| COGNITIVE FUNCTION: Authentic voice constraint establishment Voice DNA loads second — after the semantic repulsion field is in place. Positive voice constraints now operate within the boundary defined by Negative Space. This is the mechanism that prevents the agent from satisfying positive instructions while still defaulting to drift patterns. DEP-ENG-003 contains: Lexical patterns — the vocabulary signature of the coach's authentic register Cognitive fingerprint — how the coach constructs logical arguments and makes conceptual moves Emotional cadence — the rhythm of emotional disclosure and withdrawal Structural tendencies — the shapes the coach's authentic arguments naturally take What the author must verify before Layer 2 loads: No overlap with Layer 0: positive voice constraints must not include items that also appear on the Forbidden Vocabulary List. Conflicts must be resolved at the DEP-ENG-003/004 reconciliation step before the template is authored. Emotional cadence is a rhythm instruction, not a content instruction: "discloses vulnerability before moving to mechanism" is a cadence instruction. "writes about emotions a lot" is not. Cognitive fingerprint includes at least one structural tendency: how does this coach naturally arrive at conclusions? Inductively? Through paradox? Through analogy? This determines how the Mechanism phase must be constructed. Template author responsibility: Block B field\_3 and field\_9 must reference DEP-ENG-003 by formal DEP ID. The irevc-adapter loads this layer. The author ensures the DEP ID is correctly referenced so the adapter can load it. |
| :---- |

## **Layer 2 — Emotional DNA / Soul Kernel (DEP-LIB-001 / DEP-ENG-006 L3) — Third**

| COGNITIVE FUNCTION: Wound architecture activation Emotional DNA loads last — after voice identity is fully established. This ensures that when the generation agent accesses these experiences, it does so through the established voice identity, not through the generic emotional language of the training data. DEP-LIB-001 / DEP-ENG-006 L3 contains: The specific L3 pain experiences — the wound architecture producing authentic emotional transfer Emotional domain taxonomy — which life domains carry L3-weight for this coach Language patterns associated with authentic emotional access in this coach's voice What the author must verify before Field 7 authoring begins: L3 layer threshold: DEP-ENG-006 L3 layer must be ≥10% of total context data (Block C C-03). Emotional domain coverage: at least 3 distinct L3 emotional domains documented. Single-domain L3 data produces one-dimensional emotional access. L3 vocabulary is in the coach's register, not the researcher's: L3 pain descriptions using clinical or academic language are not L3 data — they are L2 data in L3 structure. Template author responsibility: The Implication phase (or archetype equivalent) must reference DEP-ENG-006 L3 as the register constraint for M7\_RELATABLE. This is the v1.2 discipline: L3 \= register gate, not content source. M7 provides the human evidence. L3 constrains the language register it must match. |
| :---- |

| *⬡  Linguistic Relativity (Whorf-Sapir): The vocabulary structure of a generated script determines the emotional experience of the reader before semantic content is processed. The SPR loading protocol exists because the order in which vocabulary constraints are established changes which vocabulary the generation agent reaches for. Negative Space first means the forbidden vocabulary is active as a repulsion field before the positive vocabulary is offered as an attraction field.* |
| :---- |

# **V  The Anti-Draft Three-Level Architecture**

**Anti-Draft Intelligence is the production immune system.** It prevents statistical mean-reversion — the LLM's default behaviour of producing the centroid of training examples that match the positive instructions. That centroid passes every surface quality check and fails every depth test.

Three levels. Three failure mode targets. All three mandatory (Mandate M-05). A template missing any level produces PARTIAL\_AUTO status — never COMPLETE.

## **5.1  Level 1 — Archetypal Anti-Draft (Block A — Invariant)**

| Property | Specification |
| ----- | ----- |
| **Source** | Container Module Library — Contrastive Anchor Calibration block |
| **Answers** | What does generic AI output look like for this archetype? |
| **Load time** | Block A — identical for all compilations of this archetype |
| **Who authors it** | The Container Module author. The template author loads it from the module. If the module lacks a Contrastive Anchor Calibration block, return to module author — it is incomplete. |

**Authoring methodology:**

7. **Write the failure example as prose — not as description.** From Ling et al. (2023): *generated* invalid examples produce semantic repulsion. Described failure modes produce abstract avoidance.

| WRONG — description of failure mode: *"Generic AI achievement stories tend to use vague mechanisms like persistence or belief, and their results are often impressionistic rather than evidential."* CORRECT — generated failure example: *"I worked incredibly hard and never gave up. After months of struggle, I finally achieved my goal. The lesson is that persistence pays off. You can do this too if you believe in yourself."* |
| :---- |

8. **Add a Failure Diagnosis — one sentence per failure element:** Why does each element fail? The diagnosis must identify the specific constraint violated, not just the aesthetic quality problem.

| Failure Diagnosis example (Achievement Story Level 1): Mechanism is non-transferable: "persistence" and "belief" are traits, not levers. A stranger cannot apply them to a different domain. Result is impressionistic: "finally achieved my goal" contains no falsifiable data point. Implication is generic: "you can do this too" constructs no structural parallel to the audience's specific situation. Stakes are absent: no cost of failure is named before the result is mentioned. |
| :---- |

9. **Write the Semantic Distance Instruction:** Output must not share vocabulary, structural pattern, or emotional register with the negative demonstration. Maximum distance from the statistical mean is the objective — not merely exceeding it.

## **5.2  Level 2 — Psychological Mode Anti-Draft (Block B — Compilation-Specific)**

| Property | Specification |
| ----- | ----- |
| **Source** | payload-masking-adapter (REGISTERED — Adapter Registry v2.0) |
| **Answers** | What does the wrong execution of THIS mood state × archetype combination look like? |
| **Load time** | Block B — generated at compilation time by the payload-masking-adapter |
| **Why not in Block A** | Level 2 anti-draft for Achievement Story × Escape Mode is fundamentally different from Achievement Story × Discovery Mode. Pre-writing four mood-state-specific examples in Block A would be simultaneously incomplete (only four combinations) and confusing (conflicting examples). |
| **Template author's responsibility** | Ensure the payload-masking-adapter is listed in Block B field\_8 and that field\_3\_context correctly populates mood\_state at compilation time. The author does NOT write Level 2 content into the template. |

| Level 2 Anti-Draft — Mode-Specific Examples (authored into adapter specification, not the template): Achievement Story × Escape Mode: *"I used to hustle myself into the ground. I learned that rest is actually productive. Here's what changed for me..."* Failure diagnosis: HIGH semantic affinity to primary stress domain. Payload stated not earned. Vehicle adds weight rather than releasing it. The audience came to escape this conversation. Achievement Story × Status Mode: *"I remember when I was at the bottom, struggling to even get a meeting. Now I'm running a team of 40\. Anyone can do it if they work hard enough."* Failure diagnosis: Mechanism is effort (non-transferable). Implication creates envy not aspiration. Status mode requires explicit pathway from audience's position to protagonist's — not just evidence the gap exists. |
| :---- |

## **5.3  Level 3 — Coach-Specific Anti-Draft (Block B — Coach-Specific)**

| Property | Specification |
| ----- | ----- |
| **Source** | voice-separation-adapter \+ DEP-ENG-004 Negative Space Object |
| **Answers** | What does THIS specific coach produce when they have the right structure but fall back to their worst patterns? |
| **Load time** | Block B — loaded from DEP-ENG-004 at compilation time |
| **Why Level 3 is the most valuable** | Levels 1 and 2 protect against generic failures. Level 3 catches the failure mode that looks correct because it has learned the coach's surface patterns without accessing their authentic depth — vocabulary, structure, and emotional domain are all right, but the coach is in professional register, not authentic access. Only DEP-ENG-004 documents this failure mode. |
| **Template author's responsibility** | Ensure DEP-ENG-004 is CRITICAL in the graceful degradation map and that voice-separation-adapter is in the conditional adapter stack. Do NOT write coach-specific anti-draft into the template — ensure the DEP ID is referenced so the adapter extracts it at compilation time. |

## **5.4  The Contrastive Instruction Block Assembly**

The three levels are assembled into one structured block inside every compiled SKILL.md by the Assembler. The template author ensures all three source inputs are formally wired:

| Level | Block Component | Source in Template | Author's Action |
| ----- | ----- | ----- | ----- |
| 1 | Negative Demonstration (prose) | Block A field\_8 Contrastive Anchor | Ensure Container Module contains Contrastive Anchor Calibration block with generated prose. Return to module author if absent. |
| 2 | Mode Failure Example | Block B field\_8 payload-masking-adapter | Ensure payload-masking-adapter listed as conditional adapter. Ensure mood\_state formally referenced in field\_3\_context. |
| 3 | Forbidden Vocabulary List | Block B field\_9 DEP-ENG-004 reference | Ensure DEP-ENG-004 is CRITICAL in degradation map. Ensure voice-separation-adapter in conditional adapter stack. |
| Assembly | Contrastive Instruction Block | Assembled by Assembler Tier 3 from all three sources | No author action required for assembly. Author's job: ensure all three sources formally wired before submission. |

# **VI  The CRAL Wiring Protocol**

**CRAL wiring** is the formal specification of how DEP-ENG-021 is connected to the arc phases of a template. Without this wiring, CRAL findings arrive as global context — available to the generation agent but not assigned to specific phases. With this wiring, each finding is injected at precisely the moment in the arc where it has the highest cognitive impact.

## **6.1  Authoring field\_5b — The CRAL Finding Map**

**field\_5b** is the architectural contract between CRAL and the Assembler. The cral-finding-router-adapter reads this map at assembly time to route each finding to the correct phase entry point.

**Authoring methodology — for each arc phase:**

10. **Identify which CRAL moments pre-address intelligence for this phase.** Question: "What does the generation agent need to know at the start of this phase that it should not have to research or infer?" The answer identifies which CRAL moment provides that intelligence.

11. **Assign use\_at.** The value is the arc phase name (e.g., "Stakes\_phase", "Mechanism\_phase"). The router-adapter fires at phase entry, injects the finding as a structured constraint, and clears the injection context before the next phase begins.

12. **Specify the function.** One paragraph explaining what cognitive work the CRAL finding does at that phase — what the generation agent can do that it could not do without this finding.

13. **Write the degradation behaviour.** If the CRAL finding is absent: which v1.1 source chain does this phase fall back to, and what flag is logged?

**Quality test:** For each moment-to-phase mapping, ask: does this moment's finding eliminate a genuine research uncertainty that v1.1 had to synthesise or infer? If yes: mapping is justified. If no: the CRAL source is decorative — remove it and keep the v1.1 source.

## **6.2  Moment-to-Phase Leverage Hierarchy**

Not all seven CRAL moments have equal impact for all archetype families. The hierarchy below specifies which moments, if absent, produce the highest degradation in output quality for a given archetype family.

| Archetype Family | Highest-Leverage Moments | Leverage Basis | If Absent — Impact |
| ----- | ----- | ----- | ----- |
| **Storytelling**(Achievement, Transformation) | **M2\_BELIEVABLE**M7\_RELATABLE | Stakes credibility \+ tribal recognition. The two phases directly determining whether the audience believes the mechanism and sees themselves in the implication. | Stakes land at generic difficulty. Implication achieves factual accuracy but not tribal recognition. Conversion to identity change does not occur. |
| **Myth & Scam**(Indignation, Empowering) | **M6\_IRREFUTABLE**M3\_UNDENIABLE | Institutional evidence \+ prediction gap. The myth debunk requires irrefutable source evidence AND the audience's specific held belief precisely identified and violated. | Debunk feels like opinion not revelation. Audience can dismiss because evidence is not irrefutable. |
| **Listicle**(Fear-Anxiety, Shocking) | **M3\_UNDENIABLE**M5\_SURPRISING | List credibility requires prediction gaps AND at least one counter-intuitive finding that violates the audience's prior belief about the subject. | List items feel confirmatory rather than revelatory. Engagement pattern: scroll, not save. |
| **Case Study**(Surprising, Relatable) | **M6\_IRREFUTABLE**M4\_RESONANT | Falsifiable result anchor \+ complete narrative unit. Case study credibility rests on the result being irrefutable and the subject story being structured and verifiable. | Case study reads as anecdote not evidence. Audience saves for inspiration, not application. |
| **Comparison**(Shocking, Surprising) | **M2\_BELIEVABLE**M5\_SURPRISING | Delta credibility \+ most surprising item. The comparison arc requires the delta to be structurally real and at least one item to genuinely violate expectation. | Comparison collapses into list format — parallel structure without genuine structural delta. |

## **6.3  The Builder Test — Validating CRAL Wiring Before Architecture Review**

Before submitting for Architecture Review, run the Builder Test — five checks confirming field\_5b CRAL wiring is architecturally correct:

| Check | Test Question | How to Evaluate | Pass Condition |
| ----- | ----- | ----- | ----- |
| **BT-01** | Does each CRAL moment mapped to a phase eliminate a genuine research uncertainty that v1.1 had to synthesise or infer? | For each mapping: identify what the agent did in v1.1 without pre-addressed CRAL intelligence. Was it inferring? Synthesising from SoC? Using probabilistic context? | If CRAL eliminates real uncertainty: pass. If it repackages intelligence the agent already had: mapping is decorative — remove it. |
| **BT-02** | Is M7\_RELATABLE mapped to the archetype's audience-facing close phase? | Identify which arc phase makes the structural parallel to the audience's situation. M7 must map to this phase — not to an earlier phase where tribal recognition has not yet been earned. | M7 mapped to the final or penultimate arc phase. |
| **BT-03** | Is the v1\_1\_source genuinely different from the v1\_2\_source for each phase? | For each phase, compare v1\_1\_source and v1\_2\_source fields. If they reference the same DEP ID or intelligence, the v1.2 upgrade for that phase is cosmetic. | v1\_2\_source references DEP-ENG-021\[moment\_id\] as a distinct intelligence source — not a repackaging of v1\_1\_source material. |
| **BT-04** | Does every arc phase have a graceful degradation path that does NOT block assembly? | Read each degradation specification. Confirm absent CRAL findings degrade to v1.1 source chain and log flags — they do not halt the Assembler. | All absent moment degradation paths are non-blocking. Assembly continues with reduced intelligence quality. |
| **BT-05** | Are there conflicts between any CRAL moment mapping and SoC source material that Step 3.5 would need to resolve? | For each CRAL moment that cross-references SoC material (M4 vs DEP-ENG-010, M6 vs DEP-ENG-005): construct one plausible conflict scenario. Is the resolution logic in the template clear? | At least one conflict scenario per cross-reference point has a documented resolution path. Templates with no Step 3.5 conflict resolution logic are incomplete. |

# **VII  Block B Template Design — What Authors Pre-Define**

Block B is populated by the Builder Engine at compilation time — but the template author designs the structure. Authors pre-define the field schema, DEP ID references, adapter parameters, and validation rules. They do not fill in specific values for coach\_id, mood\_state, or any runtime variable.

| Field | Author Pre-Defines | Builder Engine Populates | Ghost Variable Risk |
| ----- | ----- | ----- | ----- |
| **field\_2 Target** | Field names. Permitted values for output\_format and platform. | Specific format, platform, slide count, word count. | None — schema and permitted values prevent Builder Engine from inventing invalid formats. |
| **field\_3 Context** | All field names. DEP ID references for each variable. Structure of cral\_session\_id and cral\_coverage\_status (v1.2). | Specific coach\_id, mood\_state, regulatory\_frame, cral\_session\_id, all 8 routing variables. | **HIGH** — any field\_3 variable without a formal DEP ID source is a ghost variable. |
| **field\_5 Inputs** | Complete input list by topological tier. DEP ID, name, file, criticality for each. v1.2: DEP-ENG-021 at tier\_2, DEP-ENG-022 at tier\_3. | Nothing — field\_5 is authored once and reflects what the Builder Engine loads. | **HIGH** — missing DEP IDs \= ghost variables. |
| **field\_5b CRAL Finding Map** | Complete 7-moment mapping per Section VI. | Nothing — static once authored. | LOW — fully specified by template author. |
| **field\_8 Modules** | Adapter declarations (mandatory and conditional). Names only — not their logic. | Adapter instantiation parameters from field\_3 context at compilation time. | **MEDIUM** — listing an adapter not in Adapter Registry v2.0 creates a ghost adapter reference. |
| **field\_9 Voice Constraints** | Field structure. DEP-ENG-004 reference. DEP-PROTO-011 reference. Routing constraint field names (human-readable reference only — adapters are authoritative). | Forbidden Vocabulary List from DEP-ENG-004. Specific routing rules from adapters. | **MEDIUM** — inline routing logic duplicating adapter logic violates Mandate M-07. |
| **field\_10 Output Artifact** | File path pattern. Failure path pattern. Procedural log requirements list. | Specific file path for this compilation. Specific failure path if blocked. | LOW — patterns are structural. |
| **field\_11 Psych Gates** | PG-01 through PG-06 definitions. SDT alignment gate reference. | Nothing — invariant gate definitions. | LOW — fully authored by template author. |

# **VIII  Block C Pre-Flight Gate Design**

Block C defines the pre-flight validation that runs at Assembler Tier 0 — before any adapters load, before any sections are assembled. The template author defines which checks apply and what constitutes failure.

**Universal checks — required for all CCF script skills (reference by ID only — do not re-author):**

| Check | Name | Pass Condition | Failure Behaviour |
| ----- | ----- | ----- | ----- |
| C-01 | DEP Resolution | All CRITICAL tier DEP IDs in field\_5 resolve in Dependency Registry v4.0 | REJECT — structured failure JSON |
| C-02 | Psychological Routing Brief Present | DEP-ENG-016 exists and is populated | REJECT — trigger Brief Generator re-run |
| C-03 | L3 Layer Threshold | DEP-ENG-006 L3 layer ≥10% of total context data | REJECT — insufficient intelligence |
| C-05 | Authentication Certificate Valid | DEP-ENG-005 passes LIWC-22 validation | REJECT — cannot compile without authentic voice access |
| C-06 | Semantic Affinity Pre-Check | HIGH affinity \+ Escape Mode \= BLOCK. MEDIUM \+ Escape \= FLAG. | BLOCK: reclassification instruction. FLAG: logged, proceeds. |
| C-07 | TMT/Cohort Alignment | worldview\_construction \+ non-loyal cohort \= DOWNGRADE | Automatic downgrade to insight\_delivery |
| C-08 | TTT Enforcement | No hardcoded TTT value in any Block B field | REJECT — TTT is never a compilation variable |
| **C-09** | **CRAL Coverage Check** | DEP-ENG-021 present with ≥5 of 7 moment findings \= COMPLETE. 3–4 \= PARTIAL. \<3 or absent \= ABSENT | COMPLETE: proceed. PARTIAL: CRAL\_DEGRADED flags. ABSENT: v1.1 fallback \+ alert |
| **C-10** | **CRAL Moment Object Completeness** | Each DEP-ENG-021 finding object must contain: finding, register, use\_at, verifiability\_citation | Incomplete object treated as absent. HIGH severity for M2/M7. |

**Archetype-specific checks — authored by the template author:**

In addition to the universal checks, most archetypes require one or two archetype-specific checks for DEP inputs so critical to this archetype's core structural function that their absence should block compilation.

| Archetype-Specific Check Template: C-\[N\]: \[Name\] Pass condition: \[specific binary condition that must be true\] Failure behaviour: \[REJECT | DOWNGRADE | FLAG\] — \[diagnostic message | recovery instruction\] Example (Achievement Story C-04): C-04: Achievement Story Candidate Pass condition: DEP-ENG-010 has ≥1 archetype-tagged story passage with a falsifiable result metric Failure behaviour: REJECT for Achievement Story. Recovery: return to elicitation with DEP-ENG-013 Provocation Questions for falsifiable result. |
| :---- |

| ⚠  Do not add archetype-specific checks that duplicate universal checks. The most common error: adding a check that verifies DEP-ENG-016 presence (already covered by C-02). Duplicate checks inflate Block C without adding protection. |
| :---- |

# **IX  The Emotional DNA Integration Test — TESTED Maturity Gate**

**The Emotional DNA Integration Test is the quality gate between DRAFT and TESTED maturity.** A template that passes structural review but has not passed this test remains at DRAFT maturity. The test requires a complete compilation against real DEP data producing COMPLETE assembly status.

The test is named for its most discriminating check: Level 3 anti-draft population. This check requires DEP-ENG-004 data to be real, populated, and specific to a coach — because only real Negative Space data produces Level 3 anti-draft that catches the specific failure modes of that coach's voice.

| ⚠  Synthetic test data produces synthetic test results. The integration test is designed to verify the template's architectural wiring works against real coaching intelligence. Testing against fabricated DEP data produces a false COMPLETE status that masks real wiring failures. |
| :---- |

## **9.1  Test Prerequisites**

* **Real DEP-ENG-003** (Emotional DNA) for at least one coach

* **Real DEP-ENG-004** (Negative Space Object) for the same coach — must contain Forbidden Vocabulary List and at least one cognitive load drift pattern

* **Real DEP-ENG-006** (Context Premise Map) with L3 layer ≥10%

* **Real DEP-ENG-010** (SoC Batch) with at least one archetype-tagged passage for this archetype

* **Real DEP-ENG-016** (Psychological Routing Brief) for a specific mood state

* **DEP-ENG-021** (CRAL Finding Index) with ≥5 of 7 moment findings for the trigger category being tested

## **9.2  The Five Integration Checks**

| Check | Name | Pass Condition | Fail → Action |
| ----- | ----- | ----- | ----- |
| **IC-01** | **DEP Source Traceability** | Every arc phase in the compiled skill traces its primary content to a named DEP ID. No phase contains synthesised intelligence. | Identify phases lacking DEP traceability. Return to Field 7 authoring — add explicit DEP source reference to the structural law for that phase. |
| **IC-02** | **CRAL Finding Map Deployment** | The compiled skill shows evidence that CRAL moment findings were injected at the correct arc phases. assembly\_report.json shows cral\_coverage\_status \= COMPLETE and zero CRAL\_DEGRADED phases. | Check field\_5b mapping for the degraded phase. Check DEP-ENG-021 coverage. Verify cral-finding-router-adapter fired. |
| **IC-03** | **Level 3 Anti-Draft Population** | The compiled skill's anti-draft block contains a Level 3 Forbidden Vocabulary List with ≥3 exact coach-specific strings from DEP-ENG-004. At least one cognitive load drift pattern from DEP-ENG-004 appears in the Level 3 diagnostic. | Check DEP-ENG-004 completeness. Verify voice-separation-adapter is in the conditional adapter stack. Check assembly\_report.json for Tier 2 adapter failures. |
| **IC-04** | **Block C Silent Pass** | All Block C checks pass without human override. assembly\_report.json shows no manually overridden checks. Any manually overridden check indicates an unresolved architectural gap. | Identify which checks failed. If C-01 failed: registry incomplete. If C-09 failed: CRAL coverage below threshold. Fix the upstream source, not the check. |
| **IC-05** | **COMPLETE Assembly Status** | assembly\_report.json shows deployment\_status: COMPLETE. This is the definitive pass condition. | **PARTIAL\_AUTO:** diagnose adapter failures — check Tier 1 and Tier 2 logs. **PARTIAL\_MANUAL:** identify \[MANUAL\_COMPLETION\_REQUIRED\] sections — trace back to template section responsible. |

## **9.3  Test Execution Procedure**

14. Confirm all test prerequisites are met. Do not proceed if any DEP is synthetic.

15. Run the Builder Engine for one specific test compilation: choose a specific coach, mood state (recommend: Processing Mode, Prevention Frame, Loyal Cohort — the most demanding combination), and a real CRAL session.

16. Read assembly\_report.json. Check deployment\_status first. If REJECTED: fix the failing Block C check. If PARTIAL\_\*: diagnose per the IC table above.

17. Read the compiled SKILL.md. Apply IC checks manually: trace DEP sources for each arc phase (IC-01), check for CRAL findings in arc phase content (IC-02), verify Level 3 anti-draft contains real DEP-ENG-004 content (IC-03).

18. If all five checks pass: update template maturity to TESTED. Record the test compilation in the Fingerprint Archive with assembly\_status \= COMPLETE. Submit for Architecture Review.

19. If any check fails: return to the relevant section of this guide, fix the architectural gap, and re-run the full test from Step 1\. Partial fixes are not accepted.

# **X  Maturity Lifecycle — The Author's Role at Each Stage**

| Maturity | Trigger Condition | Author May Change | Author May NOT Change | Learning Loop Action |
| ----- | ----- | ----- | ----- | ----- |
| **DRAFT** | Newly authored — no production outputs | Everything. Breaking changes accepted. | Nothing is locked. | None. Accumulate test compilation results in Fingerprint Archive as draft maturity. |
| **TESTED** | Emotional DNA Integration Test passes. Architecture Review passed. | Block B schema additions. Block C additions. field\_5b enhancements. CRAL moment mapping refinements based on test output. | **Block A arc phases and structural laws** are now locked. Changes require written justification and Architecture Review re-submission. | Module Library notes compilation patterns that produced COMPLETE status. Becomes calibration data for other archetype templates in the same family. |
| **STABLE** | 10+ production outputs across diverse inputs \+ ≥1 high-performer (saves ≥2× category average) | Structural augmentations only — adding new CRAL moment mappings, updating DEP ID references when registry updates. Must not change existing structural laws. | **Block A is locked.** Block C universal checks are locked. Any modification to structural laws requires creating a new template version. | Module Library receives calibration update. High-performing patterns documented as Reference Production Examples. |
| **REFERENCE** | STABLE \+ confirmed canonical across ≥2 coaches or ≥2 cohorts | Nothing — REFERENCE templates are immutable. | **Everything is locked.** New research or improvements require a new template version. REFERENCE version permanently preserved. | Full Block A \+ Block B promoted to Template Library as canonical Reference Example. The learning loop closes — the highest-performing compiled output feeds back into the specification layer. |

| ⚠  Most common maturity error: treating a template that passed Architecture Review at TESTED as equivalent to STABLE. TESTED means "passes the Emotional DNA Integration Test". STABLE means "demonstrates consistent high-quality outputs across diverse production conditions". These are different quality thresholds. Never advance to STABLE without the production data. |
| :---- |

# **XI  Quality Assurance Checklist — Before Architecture Review Submission**

Complete this checklist before submitting any template for Architecture Review. Every item must be confirmed. Unconfirmed items are blockers, not advisories.

## **Block A Completeness**

| Check | Item | Confirmed? |
| ----- | ----- | ----- |
| A-01 | Field 1 Intent contains a reason clause distinguishing this archetype from all others in the same family |  |
| A-02 | Field 1 Intent contains an explicit Orchestrator routing value with emotional state tags and batch strategy function |  |
| A-03 | Field 4 Trigger references DEP-ENG-005 by formal DEP ID |  |
| A-04 | Field 4 Trigger states TTT natural affinity range (advisory, not block) |  |
| A-05 | Field 6 Action is a single cognitive verb phrase, congruent with Field 7 arc phases |  |
| A-06 | Field 6 Action references DEP-ENG-021 as the pre-addressed intelligence source (v1.2) |  |
| A-07 | Every arc phase in Field 7 has: cognitive function, DEP source, structural law, cral\_source, v1\_1\_source, v1\_2\_source, graceful degradation path |  |
| A-08 | Field 7 structural laws are written as prohibitions or invariant constraints — not preferences |  |
| A-09 | Field 8 Distillation Funnel specifies all four laws in archetype-specific form (not generic module descriptions) |  |
| A-10 | Field 8 Contrastive Anchor contains generated failure prose (3–5 sentences), not a description of failure modes |  |
| A-11 | Field 8 adapter declarations reference registry names only — no inline logic |  |
| A-12 | cral-finding-router-adapter listed as mandatory in Field 8 (v1.2) |  |
| A-13 | Field 9 universal rules written as prohibitions ("NEVER...") |  |
| A-14 | Field 9 includes three v1.2 CRAL universal rules |  |
| A-15 | Field 9 graceful degradation map includes every DEP ID referenced in Block A and Block B |  |
| A-16 | Field 11 structural gates include SG-06, SG-07, SG-08 (v1.2) |  |

## **Block B Completeness**

| Check | Item | Confirmed? |
| ----- | ----- | ----- |
| B-01 | Every field\_3 context variable has a formal DEP ID source — zero ghost variables |  |
| B-02 | field\_3 includes cral\_session\_id, cral\_finding\_index\_ref (DEP-ENG-021), cral\_coverage\_status, cral\_degraded\_phases (v1.2) |  |
| B-03 | field\_5 inputs include DEP-ENG-021 at tier\_2\_orchestration (CRITICAL) and DEP-ENG-022 at tier\_3\_archive (IMPORTANT) |  |
| B-04 | field\_5b CRAL Finding Map fully authored — all 7 moments mapped, each with use\_at, arc\_phase, function, degradation\_behaviour |  |
| B-05 | Builder Test checks BT-01 through BT-05 all pass |  |
| B-06 | All three psychological adapters listed in field\_8 as REGISTERED (not PROPOSED) |  |
| B-07 | field\_9 voice constraints reference DEP-ENG-004 by formal DEP ID — no inline Forbidden Vocabulary List |  |
| B-08 | field\_9 Semantic Affinity Guard references DEP-PROTO-011 by formal DEP ID |  |
| B-09 | field\_10 procedural log requirements include cral\_session\_id and cral\_coverage\_status |  |

## **Block C Completeness**

| Check | Item | Confirmed? |
| ----- | ----- | ----- |
| C-01 | All 10 universal checks referenced (C-01 through C-10) |  |
| C-02 | Archetype-specific checks authored for any DEP input whose absence should block compilation for this archetype |  |
| C-03 | Builder Engine Step 3.5 block authored — at minimum one conflict type documented with resolution logic |  |
| C-04 | No check duplicates a universal check by applying the same pass condition under a different ID |  |
| C-05 | proposed\_registrations\_reminder updated: V3.0 PROPOSED items marked REGISTERED; DEP-ENG-021, DEP-ENG-022, cral-finding-router-adapter marked REGISTERED |  |

## **Mandate Compliance**

| Check | Mandate | Confirmed? |
| ----- | ----- | ----- |
| M-01 | DEP-ENG-004 listed as CRITICAL with load\_order: ABSOLUTE FIRST |  |
| M-02 | No TTT value appears in any Block A or Block B field |  |
| M-03 | Every data source reference has a formal DEP ID — zero unregistered references |  |
| M-04 | No routing logic, agent invocation, or subagent embedding appears anywhere in the template |  |
| M-05 | All three anti-draft source inputs formally wired (Block A Contrastive Anchor \+ payload-masking-adapter \+ DEP-ENG-004) |  |
| M-06 | field\_5b CRAL Finding Map fully authored and passes Builder Test BT-01 through BT-05 |  |
| M-07 | No psychological adapter logic encoded inline in Block B — all three adapters listed by registry name only |  |
| M-08 | Emotional DNA Integration Test run against real DEP data, produced COMPLETE assembly status, result recorded in Fingerprint Archive |  |

| Architecture Review Submission Statement: All items in this checklist are confirmed. The Emotional DNA Integration Test has been run against real DEP-ENG-003/004/006/010 data and produced COMPLETE assembly status. The assembly\_report.json from the test compilation is attached. Template ID: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Archetype Name: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Template Version: 1.2 Test Compilation Coach ID: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Test Compilation Mood State: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Test Compilation CRAL Coverage Status: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Assembly Status from Integration Test: COMPLETE Author: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Date: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ |
| :---- |

——

**Script Generation Skill Type Guide**  
Version 1.0  ·  March 2026  ·  CCP Authoring Doctrine Series  
*Architecture Layer 3 — Methodology layer governing all CCF script skill authoring*