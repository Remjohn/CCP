

**CONSCIOUS COACHING PLATFORM**

**Script Generation**

**Skill Type Guide**

*The Authoring Doctrine for All CCF Script Skills*

| Type: Script Generation | Status: v1.0 — Active | Supersedes: None — first issue |
| :---- | :---- | :---- |

| Registry: skills/ccf/guides/ | Depends On: DEP Registry v4.0 · Adapter Registry v2.0 · CRAL V4.0 | Governs: All 92+ CCF script skill archetypes |
| :---- | :---- | :---- |

Version 1.0  ·  March 2026  ·  CCP Engineering Division

# **00  Purpose and Scope**

This guide is the authoring doctrine for every CCF script skill. It governs how Block A Structural Invariants are written, how voice intelligence is loaded, how anti-draft architecture is constructed, how CRAL findings are wired into arc phases, and what quality conditions must be met before any compiled skill is promoted from draft to TESTED maturity.

The guide sits between two architectural layers. Below it is the Container Module Library, which defines what every module must contain. Above it is the Design Brief Template Library, which is the output the authoring process produces. Without this guide, authors apply module specifications with inconsistent interpretations, producing templates that are structurally conforming but methodologically incoherent. A structurally conforming template with incoherent methodology produces a compiled skill that passes Block C validation and fails every depth test.

| WHAT THIS GUIDE IS The step-by-step methodology for authoring every section of a Design Brief Template The six mandatory competencies every skill author must demonstrate before a template reaches Architecture Review The doctrine that determines whether a compiled skill deserves TESTED maturity promotion The reference that resolves authoring disputes — when two authors disagree about a Block A field, this guide is the authority WHAT THIS GUIDE IS NOT A description of the compilation pipeline — see CCP Architecture Report V4.0 A specification of individual archetypes — see the Design Brief Template Library A production instruction for generation agents — see compiled SKILL.md files A guide for Research Analyst skill authoring — see Research Analyst Skill Type Guide |
| :---- |

The guide is structured in six sections, each corresponding to a mandatory authoring competency. An author who cannot demonstrate all six has not completed skill authoring — they have completed a draft. The Emotional DNA Integration Test in Section VI is the formal gate that distinguishes a draft from a skill that can be compiled.

# **I  The Eight Architectural Mandates**

These eight mandates are non-negotiable laws. Every CCF script skill must comply with all eight at all maturity levels, from draft through reference. There are no exceptions, no partial compliance states, and no maturity level at which a mandate becomes optional. Each mandate carries a specific violation consequence — not a quality warning, a structural failure mode.

**How to use this section:** Read each mandate before beginning any authoring work. After completing a template, run through each mandate as a checklist. A single mandate violation prevents Architecture Review submission.

| M1 | Anti-Draft is Mandatory at All Three Levels Every compiled CCF script skill must contain anti-draft intelligence at all three levels: Level 1 (archetype failure mode, written as concrete prose), Level 2 (psychological mode failure, generated at compilation time by payload-masking-adapter), and Level 3 (coach-specific drift patterns extracted from DEP-ENG-004). A template that specifies Level 1 anti-draft as a description rather than concrete prose has not satisfied this mandate. A template that omits Level 3 because coach-specific data is unavailable has not satisfied this mandate — the graceful degradation path for absent DEP-ENG-004 must be specified, not the requirement waived. Violation: Assembly\_report.json returns PARTIAL\_AUTO. The Deployment Quarantine Rule applies. Skill cannot be used in production until all three levels are present. |
| :---: | :---- |

| M2 | CRAL Wiring is Mandatory in All v1.2+ Templates Every Design Brief Template authored or upgraded under this guide is v1.2 architecture. v1.2 architecture requires field\_5b CRAL Finding Map, DEP-ENG-021 in tier\_2\_orchestration inputs, cral\_session\_id and cral\_coverage\_status in Block B field\_3\_context, and C-09/C-10 in Block C. A template without field\_5b has no CRAL wiring contract. A template with field\_5b but without DEP-ENG-021 in the inputs list has an incomplete dependency chain. Both are v1.1 architecture — they must not be submitted as v1.2. Violation: Template submitted as v1.2 fails Block C check C-09 on first compilation. CRAL\_DEGRADED logged on every output. DEP-ENG-022 records accumulate without compounding into the Standing Trigger Intelligence Library. |
| :---: | :---- |

| M3 | Negative Space Loads Before Positive Space — Always DEP-ENG-004 (Negative Space Object) must be the first dependency loaded in every compilation. It is listed first in the tier\_1\_derived inputs with the annotation 'ABSOLUTE FIRST before any generation constraint loads.' This is not a preference — it is the operational implementation of the contrastive architecture. If positive voice DNA (DEP-ENG-003) loads before forbidden vocabulary patterns are established, the generation agent has no boundary condition for its first token decision. Anything it generates before loading Negative Space is unconstrained and may be exactly what must not be produced. Violation: Generation agent produces voice-accurate content that contains the coach's cognitive-load drift patterns. Level 3 Anti-Draft fails silently because the Forbidden Vocabulary List is not yet active at first-token generation. |
| :---: | :---- |

| M4 | TTT is Never a Compilation Variable Temperature, Texture, and Tone are never fields in any Block A or Block B section of any Design Brief Template. They are never listed as inputs. They are never referenced in structural laws. The only permissible TTT reference in any template is the TTT Enforcement Rule in Block C (C-08) and the natural affinity range note — which is a warning reference, not a directive. Any template that contains a field labelled 'TTT', 'temperature', 'tone', or 'register' as a compilation input is non-compliant. The TTT enforcement mechanism is the Authentication Certificate (DEP-ENG-005) at runtime. Violation: Block C C-08 REJECTS the compiled brief. No assembly begins. The pre-flight gate catches this, but the template must be corrected and re-submitted — the authoring error has already caused pipeline interruption. |
| :---: | :---- |

| M5 | Ghost Variables are Prohibited Every data source referenced in every template field must have a formal DEP ID registered in Dependency Registry v4.0. This applies to Block A structural laws ('derived from the coach's authentic voice' is a ghost variable — DEP-ENG-003 is not), Block B input lists (any input without a DEP ID is unregistered), and Block C validation checks (any check that validates a field without a formal DEP ID cannot verify what it claims to verify). The author is responsible for checking the registry before referencing any data source. If a required asset does not have a DEP ID, the registry must be updated before the template is authored — not after. Violation: Block C validation cannot verify the ghost variable. The Assembler infers or synthesises the missing input. Output satisfies surface quality checks and violates intent. The failure is undetectable without architectural audit. |
| :---: | :---- |

| M6 | Structural Laws Must Be Phase-Specific and Falsifiable Every structural law in Block A field\_7 method must meet two criteria: (1) it must apply to a named arc phase, not to the piece in general; (2) it must be falsifiable — there must be a concrete test that determines whether the law was followed or violated. 'Make the mechanism transferable' is not a falsifiable law. 'The mechanism must be stated as a principle that a person in a different domain could apply without knowing the coach's context' is falsifiable. The author must be able to write the corresponding quality gate (SG series) for every structural law they write. If you cannot write the SG gate, the law is not specific enough. Violation: Assembled skills pass SG checks on form but fail on depth. The critic subagent at generation time cannot distinguish a mechanism that is technically stated as a principle from one that is genuinely transferable. The archetype's central value proposition dissolves. |
| :---: | :---- |

| M7 | The Archetype Anti-Draft Must Be Written as Prose, Not Described Level 1 anti-draft (Block A, invariant) is a concrete example of what generic AI output looks like for this archetype — written as prose, as if the AI had actually produced it. It is not a description of failure modes. It is not a list of what to avoid. It is a written example that the Contrastive Anchor Adapter loads as a negative demonstration. The difference between 'this archetype often produces effort-based mechanisms' (description) and 'I worked incredibly hard and never gave up. After months of struggle, I finally achieved my goal...' (prose) is the difference between abstract avoidance and semantic repulsion. Semantic repulsion is the architectural mechanism. Description does not produce it. Violation: Level 1 Anti-Draft produces abstract avoidance, not semantic repulsion. The generation agent produces output that avoids the described category but not the specific language register, structural pattern, and emotional posture of the archetype's statistical centroid. Statistical mean-reversion survives Level 1\. |
| :---: | :---- |

| M8 | Every Arc Phase Must Have a Traceable DEP Source and a CRAL Moment Mapping Block A field\_7 arc phases have two mandatory traceability requirements in v1.2 architecture. First: every phase must identify its primary DEP source — the specific registered data asset that carries the primary intelligence for that phase. If a phase says 'use the coach's emotional experience of the turn moment' without identifying DEP-ENG-010 as the source, it has a ghost variable. Second: every phase must have a CRAL source mapping in field\_5b — the specific moment finding(s) that pre-address research for that phase. If a phase has no CRAL mapping, CRAL intelligence cannot be injected at phase entry. The cral-finding-router-adapter has no contract to honour. Violation: The cral-finding-router-adapter skips the phase. CRAL findings are not injected. The phase assembles from raw DEP sources — v1.1 behaviour inside a v1.2 template. CRAL\_DEGRADED logged. DEP-ENG-022 records cannot accumulate quality scores for the affected phase. |
| :---: | :---- |

| MANDATE COMPLIANCE CHECKLIST — Run Before Architecture Review Submission M Mandate Status M1 Anti-draft present at all three levels. Level 1 written as prose. PASS / FAIL / N/A M2 field\_5b CRAL Finding Map present. DEP-ENG-021 in inputs. C-09/C-10 in Block C. PASS / FAIL / N/A M3 DEP-ENG-004 first in tier\_1\_derived with ABSOLUTE FIRST annotation. PASS / FAIL / N/A M4 No TTT field, temperature, tone, or register field in Block A or Block B. PASS / FAIL / N/A M5 Every data source has a DEP ID. No ghost variables anywhere in the template. PASS / FAIL / N/A M6 Every structural law is phase-specific and has a corresponding SG gate. PASS / FAIL / N/A M7 Level 1 anti-draft is prose example, not description or list. PASS / FAIL / N/A M8 Every arc phase has a DEP source and a CRAL moment mapping in field\_5b. PASS / FAIL / N/A  |
| ----- |

# **II  Three-Layer SPR Loading Protocol**

The Semantic Pointer Register (SPR) is the cognitive state the generation agent occupies when it begins producing a script. It is not a technical mechanism with a formal API — it is the cumulative effect of the constraint loading sequence on the agent's probabilistic output distribution. Concretely: what the agent loads first, and in what order, determines the boundary conditions for its first token. Those boundary conditions propagate through every subsequent token. The SPR loading protocol is the authoring specification for how Block B inputs are ordered and what each layer must establish before the next layer loads.

**Why order matters:** Each layer of the SPR narrows the generation space for the next. If the positive voice DNA loads before the forbidden vocabulary, the agent has already established its positive generation direction — the Negative Space Object then becomes a filter applied to an already-formed trajectory rather than a boundary condition on an unformed one. The filtering effect is weaker. Contrastive loading (Negative first, then Positive) produces a generation space that is shaped by what cannot be said before it is shaped by what should be said. This is the architectural implementation of the Law of the Negative Anchor.

## **2.1 Layer Zero — Environmental Pre-Conditions**

Layer Zero is not a DEP load — it is the author's responsibility to verify these conditions are met before any input specification is written. They are pre-conditions for the entire loading sequence to function as designed.

| LAYER ZERO — ENVIRONMENTAL PRE-CONDITIONS Condition 0.1 — Block C Must Be Complete First:  Never begin Block B input specification until Block C validation logic is fully written. Block C defines what DEP IDs are CRITICAL. CRITICAL DEP IDs in Block C determine the load order in Block B. Writing Block B before Block C produces an input list that may not match the validation requirements it will be checked against. Condition 0.2 — All DEP IDs Must Resolve:  Before writing any DEP ID into any input field, verify it exists in Dependency Registry v4.0. Open the registry. Find the ID. Confirm its file path, topological tier, and status. Do not write from memory. Ghost variables are the most common authoring error and the most expensive failure mode. Condition 0.3 — The Archetype's Primary Cognitive Function Must Be Named:  Before specifying inputs, you must have answered: what specific cognitive state must the audience be in at the end of this piece? This is not the mood state — mood state is a routing variable. This is the specific cognitive outcome the archetype produces. Achievement Story: 'The audience carries a falsifiable mechanism they believe is applicable to their situation.' If you cannot name this, you do not know what intelligence the skill needs to load. |
| :---- |

## **2.2 The Three Loading Layers**

| 1 | Negative Space Layer — DEP-ENG-004 Load first. Before any positive generation constraint is active. What it establishes: The Forbidden Vocabulary List — the exact strings, constructions, and patterns that constitute the coach's cognitive-load drift. Not general rules. Exact strings. The generation agent reads this before it reads anything positive. Its first generation token cannot be drawn from any element of the Negative Space. What the author must specify in the template: (1) The DEP-ENG-004 entry in tier\_1\_derived inputs with the load\_order annotation 'ABSOLUTE FIRST before any generation constraint loads.' (2) The field\_9\_voice\_constraints.coach\_specific section which will be populated at compilation time from DEP-ENG-004 — the template must contain the field structure even if the content is compilation-variable. (3) The graceful degradation instruction for absent DEP-ENG-004: CRITICAL — halt if absent. This is not negotiable. There is no graceful degradation path for missing Negative Space — the Forbidden Vocabulary List cannot be inferred or synthesised. Author verification: Before submitting the template, read the Forbidden Vocabulary List specification. Ask: could a person who has never met this coach produce a plausible list from this specification? If yes, the specification is too general. It must reference DEP-ENG-004 data directly, not describe the category of things that should be forbidden. |
| :---: | :---- |

| 2 | Positive Space Layer — DEP-ENG-003 \+ DEP-LIB-001 Load second. After Negative Space is fully active. What it establishes: The authenticated voice — lexical patterns, cognitive fingerprint, emotional cadence, structural tendencies (DEP-ENG-003), and the wound architecture — the specific L3 pain experiences that produce authentic emotional transfer (DEP-LIB-001 via DEP-ENG-006 L3 layer). Together these two assets define the positive generation space: the vocabulary, rhythm, and emotional architecture the generation agent is directed toward. What the author must specify: (1) DEP-ENG-003 in tier\_1\_derived inputs loaded by irevc-adapter as primary generation constraint. (2) DEP-LIB-001 Coach Soul Kernel referenced in field\_3\_context as soul\_kernel\_ref. (3) The emotional DNA integration requirement in field\_7 — which specific emotional DNA variable (from the 10-variable set in DEP-ENG-003) is the primary activation mechanism for this archetype. Not all ten variables are equally relevant to every archetype. Achievement Story activates the 'vindication or earned certainty' variable. The template must specify which one. Author verification: Read the field\_8 Distillation Funnel Cross-Input Collision specification. The collision should now be between DEP-ENG-021 CRAL intelligence and DEP-ENG-003 Emotional DNA — not between raw research and raw voice. If the collision still references raw DEP-ENG-006 data on one side, the template predates the v1.2 CRAL upgrade. Update it. |
| :---: | :---- |

| 3 | Contextual Intelligence Layer — DEP-ENG-006 \+ DEP-ENG-016 \+ DEP-ENG-021 Load third. After voice DNA is fully established. What it establishes: The audience intelligence layer — who the generation is for, what they know, what they fear, what they need, and what research intelligence has been pre-addressed for each arc phase of this compilation. This layer is where CRAL intelligence enters the SPR. DEP-ENG-016 (Psychological Routing Brief) calibrates the generation register. DEP-ENG-021 (CRAL Finding Index) provides the pre-addressed research findings. DEP-ENG-006 (Context Premise) provides the L3 vocabulary constraint. Critical ordering within Layer 3: DEP-ENG-016 must load before DEP-ENG-021. The Psychological Routing Brief establishes which mood state the compilation targets — this determines which register each CRAL finding should arrive in. DEP-ENG-021 findings that are loaded before mood state is established may carry the wrong register for the target audience state. The cral-finding-router-adapter handles the injection at phase entry — but it reads DEP-ENG-016 to determine register calibration. What the author must specify: (1) DEP-ENG-016 in tier\_2\_orchestration as CRITICAL — not IMPORTANT. (2) DEP-ENG-021 in tier\_2\_orchestration as CRITICAL in v1.2. (3) DEP-ENG-006 role in the template — specify that it serves as a register constraint for M7\_RELATABLE vocabulary, not as a content source for the Implication phase. In v1.2 architecture, DEP-ENG-006 L3 vocabulary governs the language register of the Implication, but the content of the Implication is delivered by M7\_RELATABLE. Author verification: Read the Implication phase specification in field\_7. Confirm it says 'DEP-ENG-006 L3 vocabulary remains the constraint on language register — M7 supplies the human evidence', not 'load from DEP-ENG-006 Context Premise L3 layer.' If the Implication phase still references DEP-ENG-006 as the content source, it is v1.1 architecture. The migration has not been completed. |
| :---: | :---- |

| *⬡  Semantic Pointer Architecture (Eliasmith, 2013): Cognitive representations are bound and composed through high-dimensional vector operations. The loading order of representation constraints is functionally equivalent to binding operations — earlier-loaded constraints constrain later ones structurally, not just additionally. This is the scientific basis for the SPR loading protocol's strict ordering requirement.* |
| :---- |

# **III  Anti-Draft Three-Level Architecture**

The Anti-Draft Architecture is the immune system of the compiled skill. It operates at three levels because statistical mean-reversion has three failure modes: failure at the archetype level (the content is generic regardless of who produced it), failure at the psychological mode level (the content is archetype-correct but mode-wrong), and failure at the coach level (the content is archetype-correct and mode-correct but voiceless). Each level requires different authoring methodology. Each level targets a different failure mode. All three must be present in every compiled skill.

**The Law of the Negative Anchor (Ling et al., 2023):** Explicitly generated invalid examples produce measurable semantic distance in subsequent generation. The critical word is generated — concrete, written failure examples produce semantic repulsion. Abstract descriptions of failure modes produce abstract avoidance. Abstract avoidance does not prevent statistical mean-reversion. The entire anti-draft architecture depends on the author's ability to write failure modes as concrete prose examples, not describe them.

## **3.1 Level 1 — Archetype Anti-Draft (Block A Invariant)**

Level 1 is authored once per archetype and never changes after STABLE maturity. It answers one question: what does generic AI output look like for this archetype? It must be written as concrete prose — an actual example of what would be produced, not a description of why it fails.

### **How to Write Level 1**

| A | Generate the statistical centroid Before writing anything, generate the actual bad output. Give a generic AI system the archetype's intent and nothing else — no voice DNA, no psychological routing, no DEP data. Read what it produces. That is the Level 1 anti-draft. The generation agent you are writing the anti-draft for will produce something in this neighbourhood unless the anti-draft creates semantic repulsion away from it. What to capture: (1) The opening construction — how does generic AI enter this archetype? (2) The mechanism language — what non-transferable mechanisms does it produce? (3) The resolution language — how does it close? (4) The register — where does it sit emotionally? These four elements together define the statistical centroid. |
| :---: | :---- |

| B | Write the prose example (3–5 sentences) Write the bad output as if it had been produced. Not 'the model tends to produce effort narratives' — write the effort narrative. Between three and five sentences. It should feel uncomfortable to read because it sounds like exactly what you are trying to prevent. LEVEL 1 ANTI-DRAFT — Achievement Story (reference example) *"I worked incredibly hard and never gave up. After months of struggle, I finally achieved my goal. The lesson is that persistence pays off, and if you believe in yourself, you can accomplish anything. The journey taught me that success requires dedication and the willingness to keep going even when things get difficult. You have what it takes — you just have to start."* Why this is the centroid: Mechanism is non-transferable (persistence/belief). Result is impressionistic (achieved my goal). Implication is generic inspiration (you have what it takes). No Stakes phase. No Turn frame. No falsifiable evidence. Every structural law of the archetype is violated. This is the statistical average of all achievement narrative training examples.  |
| :---: | :---- |

| C | Write the failure diagnosis (one sentence per element) After the prose example, write a diagnosis of why each element fails. This is the component that trains the generation agent's self-evaluation. The agent reads this at generation time and checks its own draft against these diagnoses in Pass 2 (Critic Subagent evaluation). Diagnosis format: 'Why \[element\] fails: \[specific constraint violated\].' Not 'the mechanism is too general' — 'Why mechanism fails: persistence/belief is not transferable to a person in a different domain because it identifies a psychological attitude rather than a behavioural principle that produces a specific result.' |
| :---: | :---- |

| D | Write the semantic distance instruction Close the Level 1 block with an explicit distance requirement. The generation agent is not instructed to 'avoid' the anti-draft — it is instructed to maximise semantic distance from it. Distance is the target, not threshold clearance. Standard phrasing: 'Output must not share vocabulary, structural pattern, or emotional register with the negative demonstration above. Proximity to any element of the demonstration is a quality failure regardless of overall output quality. Maximise distance from the statistical centroid — exceeding it is not sufficient.' |
| :---: | :---- |

## **3.2 Level 2 — Psychological Mode Anti-Draft (Block B, Compilation-Specific)**

Level 2 is not authored in the template — it is generated at compilation time by the payload-masking-adapter. But the template author is responsible for writing the specification that tells the adapter what to generate. This is the most frequently misunderstood section of the template. Authors often treat Level 2 as a static field they can pre-fill. They cannot. Level 2 requires the psychological routing context — which is not available until compilation time.

**What the author must specify in the template:** The Level 2 generation instruction for the payload-masking-adapter — a meta-specification that tells the adapter what constitutes a mode failure for this specific archetype × mood state combination.

### **Level 2 Specification by Mood State**

| Mood State | Mode Failure Pattern | What the Author Specifies |
| ----- | ----- | ----- |
| **Processing** | The mechanism and implication are stated correctly but the payload arrives before the vehicle earns it — the audience is handed the truth before they have emotionally earned the right to receive it. | Specify: 'Level 2 anti-draft for Processing Mode shows the archetype with correct mechanism but no earned arc — payload stated in paragraph 1 without Stakes or Turn preceding it. The audience is told the truth before they feel the cost of not knowing it.' |
| **Escape** | The vehicle and the L3 payload share high semantic affinity — the topic the audience came to escape IS the topic of the piece. The Semantic Affinity Guard should have blocked this but the author must still specify the failure mode. | Specify: 'Level 2 anti-draft for Escape Mode shows the archetype where the vehicle's entry domain mirrors the coach's active L3 pain domain. Example: an achievement story about career burnout delivered in Escape Mode — the vehicle is structurally correct but the semantic domain is the exact stress the audience needs relief from.' |
| **Discovery** | The counter-intuitive entry is not counter-intuitive — the 'surprising' fact is either common knowledge or merely unusual without producing genuine prediction error. | Specify: 'Level 2 anti-draft for Discovery Mode shows the archetype where the entry fact is presented as surprising but is already known to the tribe. The hook produces no cognitive reward because the audience already holds the knowledge — competence reward does not arrive, mechanism has no surprise vehicle to ride.' |
| **Status** | The mechanism is stated as a lesson rather than encoded as a comparison signal — 'here is what I learned' rather than 'here is what winners understand that others don't.' | Specify: 'Level 2 anti-draft for Status Mode shows the archetype where the mechanism and implication are delivered as explicit instruction rather than as comparison signal. The audience is taught rather than recognised. Identity function collapses — the piece becomes a lesson, not a signal about what kind of person understands this.' |

## **3.3 Level 3 — Coach-Specific Anti-Draft (Block B, Coach-Specific)**

Level 3 is the most precise and the hardest to author. It answers: what does THIS specific coach produce when they have the right structure and the right mode but fall back to their worst patterns? It cannot be written without DEP-ENG-004 data. The author's role is to specify the extraction methodology that the compilation process uses to populate Level 3 — not to pre-fill it with guesses about the coach.

### **Extracting Level 3 from DEP-ENG-004**

**The four DEP-ENG-004 extraction categories:** Every Negative Space Object in the registry contains data in four categories. The template specification must reference all four.

| Category | What It Contains | How to Specify in Template |
| ----- | ----- | ----- |
| **Cognitive Load Drift Patterns** | The specific constructions the coach defaults to when uncertain — what their writing does when they don't know how to say something | 'Extract cognitive load drift patterns from DEP-ENG-004 Section 2\. Write each pattern as an exact construction: \[specific sentence opening\] or \[specific phrase\]. Not a description of the pattern — the actual string.' |
| **Professional Register Hedges** | The specific hedging language the coach uses when they slip into professional or corporate register — often latinate vocabulary, passive constructions, or distancing language | 'Extract professional register markers from DEP-ENG-004 Section 3\. Include: vocabulary substitutions (informal → formal drift), passive construction patterns, and distancing language markers. Each as exact string.' |
| **Performed vs. Lived Vocabulary** | Vocabulary items that are technically in the coach's domain but feel performed — correct word, wrong register. Often aspirational language the coach uses in professional contexts but never in authentic self-expression | 'Extract performed vocabulary from DEP-ENG-004 Section 4\. These are words that appear in the coach's professional materials but not in their unguarded conversation. Each as exact string. Mark as FORBIDDEN-PERFORMED.' |
| **Structural Shortcuts** | The structural moves the coach makes when emotional access is shallow — abbreviated arcs, summary closings instead of earned implication, mechanism-as-lesson instead of mechanism-as-revelation | 'Extract structural shortcut patterns from DEP-ENG-004 Section 5\. Write each as a structural move description: \[specific pattern\] — e.g., "closing with lessons learned list when emotional arc is incomplete." ' |

| *⬡  Contrastive Chain-of-Thought (Ling et al., 2023): Paired contrastive negatives — positive example alongside negative example — significantly outperform positive-only prompting. The improvement is largest on tasks requiring constraint satisfaction across multiple criteria simultaneously, which is exactly the challenge a script skill faces. All three levels of anti-draft must be present for the full contrastive effect.* |
| :---- |

# **IV  Causal Construction Sequence**

The Causal Construction Sequence is the five-step process for writing every arc phase specification in Block A field\_7. It is called causal because each step produces a specific output that is the causal precondition for the next step. Skipping a step does not produce a faster result — it produces a phase specification that is incomplete at a specific structural position, which propagates as a failure through every compilation that uses the template.

**When to use it:** Use this sequence every time you write or upgrade a Block A field\_7 arc phase. Use it when migrating a v1.1 template to v1.2 — the migration is not complete until every phase has been rebuilt through this sequence. Use it when a compiled skill's quality gate SG-01 through SG-08 returns a failure — identify which step of the sequence the failing phase was built without.

## **4.1 The Five-Step Sequence**

| 1 | Name the Phase's Cognitive Function Answer: what specific cognitive state must the audience be in at the END of this phase? Not what happens in the phase — what state the audience leaves it in. Format: 'At the end of \[phase name\], the audience is in \[specific cognitive state\] because \[specific mechanism\].' Achievement Story — Stakes example: 'At the end of the Stakes phase, the audience occupies the emotional reality of what failure costs because the Stakes phase has named a specific, falsifiable cost that belongs to the audience's structural situation, not the coach's.' The test: Read the cognitive function statement to someone who has never seen the archetype. If they can describe what the phase accomplishes, the statement is specific enough. If they ask 'but what does that mean in practice?', it is not specific enough. |
| :---: | :---- |

| 2 | Identify the Primary DEP Source Answer: which specific registered data asset carries the primary intelligence for this phase? Primary means: if this asset were absent, this phase would fail catastrophically, not gracefully degrade. Format: 'Primary DEP source: \[DEP-ID\] — \[why this asset is primary for this phase and not another\].' Common authoring error to avoid: Listing multiple DEP sources as co-equal for a phase. Every phase has one primary source. Secondary sources provide context or enrichment — they are important but the phase does not require them to attempt assembly. If you cannot name one primary source, you have not understood what the phase fundamentally needs. DEP source decision tree: Ask (1) Does this phase require the coach's authentic voice for its primary content? → DEP-ENG-010 or DEP-ENG-003. (2) Does this phase require external verifiable evidence? → DEP-ENG-021 CRAL moment. (3) Does this phase require audience intelligence? → DEP-ENG-006, DEP-ENG-016, or DEP-ENG-021\[M7\]. (4) Does this phase require the authenticated result? → DEP-ENG-005. |
| :---: | :---- |

| 3 | Write the Structural Law Answer: what specific, falsifiable rule governs the construction of this phase? One law per phase. Not guidelines — a law is something that, if violated, makes the phase structurally wrong regardless of how good the surrounding content is. Falsifiability test: For every structural law you write, you must be able to complete this sentence: 'I can tell this law was violated because \[observable condition\].' If you cannot complete it, the law is not falsifiable. Write the falsifiability condition alongside the law — it becomes the SG gate in Step 5\. Bad structural law (not falsifiable): 'The Mechanism must be specific and transferable.' Good structural law (falsifiable): 'The Mechanism must be stated as a principle that names what to do differently, not why to try harder — a person in a different industry who reads only the Mechanism phase must be able to describe a concrete action they would take based on it.' Common over-specification error: Writing multiple laws for one phase. This produces Phase specifications that cannot be enforced — the generation agent and the Critic Subagent cannot simultaneously satisfy five laws per phase without explicit prioritisation. Write one primary law. If additional constraints are necessary, write them as secondary laws with an explicit priority order. |
| :---: | :---- |

| 4 | Write the CRAL Source Mapping Answer: which CRAL moment finding(s) pre-address research for this phase? This is the v1.2 architecture requirement. This step builds the content that goes into field\_5b CRAL Finding Map for this phase. Format: 'CRAL source: \[M\#\_MOMENT\_ID\]. Function: \[what this moment finding provides that the phase needs\]. Use\_at: \[phase name\].' Two questions to answer: (1) What research does this phase need that the coach's SoC cannot provide? That is the CRAL moment. (2) What does the SoC provide that CRAL cannot? That is the voice layer the phase still requires from DEP-ENG-010. Both must be present in the phase specification — CRAL provides intelligence, SoC provides authentic voice. They are not substitutes. When a phase has two CRAL sources: Some phases require two moment findings — Stakes in Achievement Story uses both M2 (mechanism instance) and M3 (prediction gap). When specifying two sources, write their functions separately and specify their relationship: 'M2 provides the external evidence anchor. M3 provides the audience's specific prediction error. M2 makes the stakes real. M3 makes the stakes land at the right cognitive register. Neither substitutes for the other.' When a phase has no CRAL source: This is architecturally valid for phases that are purely voice-dependent — phases where the primary content must be the coach's authentic expression and no research intelligence is needed. In this case, specify explicitly: 'No CRAL mapping — this phase is voice-primary. Source: DEP-ENG-010 SoC only. CRAL would contaminate authenticity at this phase.' |
| :---: | :---- |

| 5 | Write the Structural Quality Gate (SG) Answer: what is the observable pass/fail condition that the Critic Subagent uses to evaluate whether this phase was executed correctly? This is the SG gate. It must be derivable directly from the structural law in Step 3 — if it requires new reasoning not present in Step 3, Step 3's law was incomplete. Format: 'SG-\[N\]: \[Check description\] — PASS: \[observable condition\]. FAIL: \[observable condition\].' The gate must be binary: A quality gate is not a scoring rubric. It is a binary check: either the condition was met or it was not. 'The mechanism is somewhat transferable' is not a gate — it is an assessment. 'The mechanism is stated as a principle a person in a different industry could apply without knowing the coach's context' is a gate. CRAL gate in addition to structural gate: Every phase that has a CRAL source mapping (Step 4\) requires an additional SG gate: 'The \[phase name\] deploys \[M\#\_MOMENT\_ID\] finding or is flagged CRAL\_DEGRADED.' This is the gate that the cral-finding-router-adapter's injection is verified against. Phases without this gate have no enforcement mechanism for CRAL injection. Numbering: SG-01 through SG-05 are the five gates from V3.0 architecture (specified in the original template format). SG-06, SG-07, SG-08 are the three CRAL gates added in v1.2. If your archetype requires additional phase-specific gates beyond eight, number them SG-09 onwards and document the reason for the additional gate in the template meta block. |
| :---: | :---- |

## **4.2 Phase Specification Completeness Check**

After building all arc phases through the five-step sequence, run this completeness check before moving to Block B authoring. Every row must be completed. An incomplete row means the phase specification is not ready for Architecture Review.

| Arc Phase | Step 1: Cognitive Function Named | Step 2: Primary DEP Source | Step 3: Structural Law (Falsifiable) | Step 4: CRAL Source Mapped | Step 5: SG Gate Written |
| ----- | ----- | ----- | ----- | ----- | ----- |
| Phase 1 name | Y / N | DEP-ID | Y / N \+ falsifiability condition | M\# or NONE | SG-\# written |
| Phase 2 name | Y / N | DEP-ID | Y / N \+ falsifiability condition | M\# or NONE | SG-\# written |
| Phase 3 name | Y / N | DEP-ID | Y / N \+ falsifiability condition | M\# or NONE | SG-\# written |
| Phase 4 name | Y / N | DEP-ID | Y / N \+ falsifiability condition | M\# or NONE | SG-\# written |
| Phase 5 name | Y / N | DEP-ID | Y / N \+ falsifiability condition | M\# or NONE | SG-\# written |

# **V  CRAL Wiring Protocol**

The CRAL Wiring Protocol is the authoring methodology for field\_5b CRAL Finding Map — the architectural contract between the CRAL research subsystem and the Assembler. Without field\_5b, the cral-finding-router-adapter has no contract to honour. It cannot know which moment finding belongs at which arc phase. The protocol ensures that the contract is: (1) complete — all seven moments are addressed, (2) precise — each mapping specifies function not just assignment, and (3) archetype-specific — the mapping reflects this archetype's structure, not a generic template.

## **5.1 Understanding the Seven Moments Before Mapping**

Before mapping any moment to any phase, the author must understand what each moment produces and what it requires. Authors who map moments to phases without this understanding produce maps that are formally complete but functionally wrong — the right moment assigned to the wrong phase produces findings that arrive at a phase that cannot use them.

| Moment | What It Produces | What It Requires From the Archetype | What Phase Benefits Most |
| ----- | ----- | ----- | ----- |
| **M1\_RELEVANT** | The cultural NOW — the conversation the tribe is actively having at the production moment | A point in the archetype where cultural context makes the content feel timely rather than evergreen | Pre-assembly — shapes trigger quality. Never maps to a production arc phase. Informs the hook's cultural relevance but does not inject into a named phase. |
| **M2\_BELIEVABLE** | A named, verifiable, unchallengeable evidence anchor — specific entity, documented decision, date | A phase that needs external verification — where the audience must accept the premise before the arc can proceed | Any phase that makes a claim the audience could reject. In Storytelling: Stakes phase. In Case Study: Result phase. In Myth: Myth establishment. |
| **M3\_UNDENIABLE** | The audience's measurably wrong prediction — the specific belief the tribe holds that this piece will correct | A phase that must create cognitive dissonance to achieve its function. The phase must know what wrong belief it is disrupting. | Any phase that works by correcting a wrong assumption. Maps alongside M2 wherever the wrong assumption is the Stakes. |
| **M4\_RESONANT** | A complete narrative unit: protagonist \+ status \+ documented moment of contact with the mechanism \+ outcome | A phase that needs human evidence for a mechanism — a phase that must show the mechanism working in a real person's life | The mechanism phase in any archetype. The narrative unit IS the mechanism made human and therefore believable. |
| **M5\_SURPRISING** | A counter-intuitive finding at optimal incongruity — violates the audience's held belief without being incomprehensible | A phase that must produce maximum cognitive activation — where the audience's attention is at peak because something should not be true and is | The pivot or turn phase. The single frame where the mechanism's result contradicts the audience's prediction. Discovery Mode hook also benefits. |
| **M6\_IRREFUTABLE** | Maximum source proximity evidence — the internal document, the enemy's own admission, the filing that closes deniability | A phase that must close the audience's last remaining path to doubt. The phase that carries the piece's evidential burden. | The result phase or the evidence revelation phase. Wherever the archetype needs to close deniability. |
| **M7\_RELATABLE** | A tribal recognition anchor — named person from inside the tribe, vernacular-precise testimony | A phase that must produce tribal recognition, not factual accuracy. The phase where the audience feels seen, not merely described. | The implication or parallel phase in any archetype. The phase that closes the distance between the coach's story and the audience's life. |

## **5.2 Mapping Process — Three Decision Tests**

For each arc phase in the archetype, apply three decision tests to determine which CRAL moment(s) map to it.

| DECISION TEST 1 — What does the phase need that the coach's voice cannot provide? The coach's SoC (DEP-ENG-010) provides authentic voice. It provides the coach's lived experience and emotional truth. It does not provide external verification, tribal intelligence, or calibrated research. Ask: does this phase need something the coach cannot produce from inside their own experience? If yes — the phase needs a CRAL moment. Identify which moment provides what the phase needs. If no — the phase is voice-primary. It may still benefit from CRAL context, but the primary source is SoC. |
| :---- |

| DECISION TEST 2 — What would make this phase fail to convince if CRAL were absent? Imagine the phase assembled with only SoC data and no CRAL findings. What is the most likely failure mode? If the failure is 'the claim is unverifiable' — M2 or M6. If the failure is 'the audience can dismiss this because their contrary belief is intact' — M3. If the failure is 'the mechanism has no human evidence' — M4. If the failure is 'the surprise doesn't land because it was expected' — M5. If the failure is 'the parallel feels generic' — M7. |
| :---- |

| DECISION TEST 3 — Can this phase accept the finding at phase entry, or does it need it earlier? The cral-finding-router-adapter injects findings at phase ENTRY — the moment the Assembler begins constructing this phase. If the finding needs to shape the phase from its first token, map it here. If the finding is context that a preceding phase needs to set up, map it to the preceding phase instead. The use\_at field in field\_5b is the Assembler's instruction for when to call DEP-ENG-021\[moment\_id\]. Get it wrong and the finding arrives too late to shape the phase it is intended for. |
| :---- |

## **5.3 field\_5b CRAL Finding Map — Authoring Standard**

The field\_5b block must contain one entry per moment (all seven) plus M1's special pre-assembly status. Below is the required structure for each entry and the quality standard for each field.

| Field | Format | Quality Standard | Req? |
| ----- | ----- | ----- | ----- |
| **moment\_id** | M\#\_LABEL | Must match one of the seven canonical IDs exactly: M1\_RELEVANT, M2\_BELIEVABLE, M3\_UNDENIABLE, M4\_RESONANT, M5\_SURPRISING, M6\_IRREFUTABLE, M7\_RELATABLE. No aliases. | **YES** |
| **use\_at** | phase name or 'pre\_assembly' | Must match the exact phase name from field\_7 arc\_phases. Case-sensitive. M1 always uses 'pre\_assembly\_context'. No phase name may appear in use\_at for two different moments unless both moments are mapped to the same phase intentionally (M2+M3 both map to Stakes in Storytelling). | **YES** |
| **arc\_phase** | Number \+ name | The phase number and label from field\_7. Used by the Assembler to verify the use\_at mapping is consistent with the template's phase sequence. Must match exactly. | **YES** |
| **function** | Free prose 2–4 sentences | Describes what this specific moment finding provides to this specific phase. Must explain: (1) what the finding contains, (2) why this phase needs it, (3) how it upgrades the phase over v1.1 SoC-only construction. This field is the primary authoring quality signal — a generic function description is a red flag. | **YES** |
| **v1\_1\_source** | DEP reference string | The data source this phase used in v1.1 architecture. Allows audit trails for migration work. Required for all templates migrated from v1.1. For new templates authored from scratch: include anyway — specify what the equivalent v1.1 source would have been. | **YES** |
| **v1\_2\_source** | DEP reference string \+ CRAL ID | The data source chain for v1.2. Format: 'DEP-ENG-021\[M\#\] \+ \[fallback source\]'. Specifies both the primary CRAL source and the fallback for when DEP-ENG-021\[M\#\] is absent (CRAL\_DEGRADED state). | **YES** |

## **5.4 Builder Test — Validating CRAL Wiring Before Architecture Review**

Before submitting any template to Architecture Review, run the Builder Test. This is a manual simulation of what the cral-finding-router-adapter will do with the field\_5b map. If the test passes, the wiring is valid. If it fails, the map has a structural error that will produce CRAL\_DEGRADED outputs on every compilation.

| BUILDER TEST — CRAL WIRING VALIDATION Test 1 — Coverage: List all seven moment IDs. Confirm each appears exactly once in field\_5b. If any moment is absent, the map is incomplete. If any moment appears twice, there is a mapping conflict. Test 2 — Phase Alignment: List all arc phase names from field\_7. Confirm every use\_at value in field\_5b matches an arc phase name exactly (except M1 which maps to pre\_assembly\_context). If any use\_at value does not match a phase name, the adapter cannot route the finding. Test 3 — Function Specificity: Read each function description in field\_5b. For each, ask: could this function description apply to a different archetype family? If yes, it is generic — rewrite it with archetype-specific reasoning. A generic function description means the map will work formally but the cral-finding-router-adapter's injection will be contextually misaligned. Test 4 — v1.1 Source Chain: For each CRAL mapping, verify that the v1\_1\_source field specifies a valid fallback. If DEP-ENG-021\[M\#\] is absent during a compilation, the Assembler falls back to v1\_1\_source. If v1\_1\_source is empty or invalid, the fallback fails and the phase cannot assemble at all — PARTIAL\_MANUAL, not CRAL\_DEGRADED. Test 5 — SG Gate Completeness: For every CRAL-mapped phase, confirm there is an SG gate in field\_11 that checks CRAL injection. Standard phrasing: 'The \[phase name\] deploys DEP-ENG-021\[M\#\_ID\] or is explicitly flagged CRAL\_DEGRADED with fallback source logged.' If this gate is absent, the Assembler has no enforcement mechanism for CRAL injection at this phase. |
| :---- |

# **VI  Emotional DNA Integration Test**

The Emotional DNA Integration Test is the quality gate for TESTED maturity promotion. A compiled skill cannot be promoted from draft to TESTED without passing all five test conditions. This is not a subjective assessment — each condition has a binary pass/fail criterion that an Architecture Reviewer applies without knowing the author of the template.

**Why this test exists:** Draft maturity means the skill was compiled and did not fail at assembly. It does not mean the skill is psychologically coherent, architecturally sound, or capable of producing content that survives the Critic Subagent's three-level evaluation. Many skills that compile successfully are structurally correct but emotionally hollow — they pass the mechanical checks and fail every depth test. The Emotional DNA Integration Test is designed to catch exactly this failure mode before the skill enters the production pipeline.

## **6.1 The Five Test Conditions**

| \# | Condition Name | Pass Criterion | Fail Indicator |
| ----- | ----- | ----- | ----- |
| **T1** | **Phase Source Traceability** | Every arc phase in the compiled skill has a documented source path: either a DEP ID (for voice-primary phases) or DEP-ENG-021\[M\#\] \+ DEP ID fallback (for CRAL-mapped phases). No phase can be assembled without the Assembler being able to trace what intelligence it drew from. | Any phase in the compiled skill whose source cannot be traced to a specific DEP ID. Ghost variable in the output. |
| **T2** | **CRAL Finding Map Completeness** | field\_5b contains all seven moment mappings. M1 maps to pre\_assembly\_context. M2 through M7 each map to a named arc phase. All five Builder Test checks pass without human override. | Any moment absent from field\_5b. Any use\_at value that does not match a named arc phase. Any function description that cannot be distinguished from a generic template. |
| **T3** | **Anti-Draft Level 3 From Real DEP-ENG-004 Data** | The Level 3 anti-draft Forbidden Vocabulary List in the compiled skill contains strings that are traceable to the coach's actual DEP-ENG-004 Negative Space Object. The strings are exact constructions or vocabulary items — not descriptions of categories. The list contains at least 5 specific strings. | Forbidden Vocabulary List contains fewer than 5 items. Any item is a description ('avoid corporate language') rather than a string ('leverage', 'synergise', 'going forward'). Any item that applies equally well to any coach rather than this specific coach. |
| **T4** | **Block C Passes Without Human Override** | A test compilation using real or simulated Block B data passes all Block C checks C-01 through C-10 without any check requiring human override to proceed. The cral\_coverage\_status field is populated. C-09 returns COMPLETE or PARTIAL (not ABSENT unless CRAL has not run, which must be documented). | Any Block C check requiring human override on a test compilation. C-09 returning ABSENT with no documentation. C-08 catching a hardcoded TTT value that slipped into Block B. Any CRITICAL tier DEP ID failing to resolve. |
| **T5** | **Test Compilation Returns COMPLETE Assembly Status** | At least one test compilation produces assembly\_report.json with deployment\_status: COMPLETE. PARTIAL\_AUTO is acceptable only if the PARTIAL sections are documented with specific resolution paths. PARTIAL\_MANUAL and REJECTED are test failures — the template must be corrected before TESTED promotion. | assembly\_report.json showing PARTIAL\_MANUAL without documented resolution path. Any REJECTED status. Any section with \[MANUAL\_COMPLETION\_REQUIRED\] placeholder that has no documented reason for the gap. |

## **6.2 Running the Integration Test — Reviewer Protocol**

The Integration Test is run by an Architecture Reviewer who did not author the template being reviewed. The reviewer follows this protocol in strict sequence. The author may not be present during the review — the template must speak for itself.

| 1 | Read Block A field\_7 in full For each arc phase, apply the Phase Source Traceability check (T1). Open Dependency Registry v4.0 in a separate window. Verify every DEP ID referenced in every phase specification resolves in the registry. Write the verification result for each phase before proceeding. |
| :---: | :---- |

| 2 | Audit field\_5b CRAL Finding Map Run all five Builder Test checks (Section V.4). Record pass/fail for each. A single Builder Test failure is sufficient to halt the review — return the template to the author with the specific failed check noted. Do not proceed to T3 if T2 fails. |
| :---: | :---- |

| 3 | Evaluate the Level 3 Anti-Draft Read the Forbidden Vocabulary List specification in field\_8/field\_9 voice constraints. Apply T3 criteria: count specific strings (minimum 5), verify they are exact constructions not descriptions, verify each is coach-specific not generic. If the template has not been compiled against real DEP-ENG-004 data yet, this test requires a simulated Level 3 from available coach data — document which source was used for simulation. |
| :---: | :---- |

| 4 | Run a test compilation Using real or simulated Block B data, trigger a test compilation. Read the full assembly\_report.json. Apply T4 (Block C clean pass) and T5 (COMPLETE status). If the compilation is not available to run live, the reviewer must request a compilation log from a prior assembly attempt. A template without any compilation history cannot be promoted to TESTED. |
| :---: | :---- |

| 5 | Issue the promotion decision All five conditions must pass for TESTED promotion. A template that passes T1, T2, T3, T4 but fails T5 is still a draft — it has passed all the structural tests but has not been successfully compiled. A template that passes T5 but fails T3 is a PARTIAL\_AUTO at best — it compiles but with incomplete voice intelligence. Partial passes do not receive TESTED status. Promotion documentation format: 'TESTED promotion approved — \[date\]. Reviewer: \[ID\]. Conditions: T1 PASS, T2 PASS, T3 PASS, T4 PASS, T5 PASS. Compilation log: \[ID\]. Next review trigger: 10 production outputs OR significant DEP-ENG-004 update.' |
| :---: | :---- |

## **6.3 The Emotional DNA Integration Test — Underlying Logic**

The test is called the Emotional DNA Integration Test because all five conditions, at their root, are verifying whether the compiled skill has genuinely integrated the coach's emotional DNA into every structural layer — or whether it has structurally referenced it while leaving it disconnected from the actual generation architecture.

A skill that passes T1 but not T3 has source traceability but no actual voice intelligence loaded — the DEP IDs exist in the inputs list but the extracted Forbidden Vocabulary List is not coach-specific. The skill looks connected but is not. A skill that passes T3 but not T2 has real voice intelligence but no CRAL wiring — the intelligence it has is excellent but it is only voice intelligence, not research intelligence. The content will be authentic but may be culturally disconnected or evidentially weak.

The only skill that is genuinely ready for production is one that passes all five conditions — source traceability, research wiring, real voice intelligence, clean compilation, and successful assembly. These five conditions together represent the minimum viable integration of the coach's emotional DNA, the CRAL research intelligence, and the psychological routing architecture.

| INTEGRATION TEST SCORECARD — Template ID: \_\_\_\_\_\_\_\_\_\_\_\_ \# Condition Reviewer Result Evidence Ref Notes T1 Phase Source Traceability PASS / FAIL \_\_\_ T2 CRAL Finding Map Completeness (Builder Test 1–5) PASS / FAIL \_\_\_ T3 Anti-Draft Level 3 From Real DEP-ENG-004 Data PASS / FAIL \_\_\_ T4 Block C Passes Without Human Override PASS / FAIL \_\_\_ T5 Test Compilation Returns COMPLETE Assembly Status PASS / FAIL \_\_\_ DECISION All five conditions required for TESTED promotion PROMOTED / DRAFT Reviewer ID: Date:  |
| ----- |

# **Appendix — Quick Reference and Authoring Checklist**

## **A.1 Authoring Sequence — Start to Architecture Review**

This is the canonical sequence for authoring a new Design Brief Template or upgrading an existing one to v1.2. Follow it in order. Do not begin a later step while an earlier step has open items.

| Order | Step | Output | Gate Before Next Step |
| ----- | ----- | ----- | ----- |
| 1 | Read this guide in full. Identify which archetype family the template belongs to. | Author's understanding of: 8 mandates, 3-layer SPR, anti-draft levels, causal construction sequence, CRAL wiring protocol, integration test | Author can answer: what is the primary cognitive function of each arc phase? |
| 2 | Verify all required DEP IDs exist in Dependency Registry v4.0 | Confirmed list of DEP IDs with status REGISTERED for all inputs this template will reference | Zero ghost variables before Block authoring begins |
| 3 | Write Block C validation gates first (C-01 through C-10) | Complete Block C with all CRITICAL DEP IDs identified | Block C defines CRITICAL inputs. CRITICAL inputs determine Block B load order. |
| 4 | Build all arc phases using Causal Construction Sequence (Section IV) | Completed Phase Specification Completeness Check table (all rows filled) | Every phase has: cognitive function, DEP source, structural law, CRAL mapping, SG gate |
| 5 | Write Level 1 Anti-Draft (Section III.1 — steps A through D) | 3–5 sentence prose example \+ failure diagnosis \+ semantic distance instruction | Level 1 is prose, not description. Mandate M7 verified. |
| 6 | Specify Level 2 Anti-Draft per mood state (Section III.2) | Mode failure specification for all four mood states this archetype supports | Each mode failure is specific to this archetype × mode combination, not generic |
| 7 | Specify Level 3 extraction methodology (Section III.3) | Four-category DEP-ENG-004 extraction specification | Extraction categories are coach-extractable, not pre-filled guesses |
| 8 | Complete Block B input specification using SPR loading protocol (Section II) | Ordered input list: Layer 0 pre-conditions verified → Layer 1 (DEP-ENG-004 first) → Layer 2 (DEP-ENG-003 \+ DEP-LIB-001) → Layer 3 (DEP-ENG-016, DEP-ENG-021, DEP-ENG-006) | DEP-ENG-004 is first in tier\_1\_derived. No TTT fields anywhere. |
| 9 | Write field\_5b CRAL Finding Map using CRAL Wiring Protocol (Section V) | Complete field\_5b with all seven moments mapped. All five Builder Tests pass. | Builder Test 1–5 all PASS. Every SG gate for CRAL phases written. |
| 10 | Run Mandate Compliance Checklist (Section I) | All 8 mandates marked PASS | All 8 mandates PASS. No mandate marked FAIL or left blank. |
| 11 | Submit to Architecture Review for Emotional DNA Integration Test (Section VI) | Architecture Review result: PROMOTED or DRAFT (with specific failure conditions noted) | All T1–T5 PASS \= TESTED promotion. Any failure \= return to authoring with specific gap identified. |

## **A.2 Common Authoring Errors and Corrections**

| Error | Why It's an Error | Correction |
| ----- | ----- | ----- |
| Writing 'the coach's authentic emotional experience' without a DEP ID | Ghost variable. No DEP ID \= the Assembler cannot formally load this. | Replace with: 'from DEP-ENG-010 SoC Batch' or 'from DEP-ENG-003 Emotional DNA.' |
| Specifying Level 1 anti-draft as 'avoid generic AI tropes' | Description, not prose. Mandate M7 violation. Semantic repulsion requires concrete negative example. | Write 3–5 sentence prose example as if the AI had actually produced it. See Section III.1. |
| Listing DEP-ENG-021 in Block B but leaving field\_5b empty | The Assembler has the Finding Index but no routing contract. cral-finding-router-adapter cannot inject anything without field\_5b. | Complete field\_5b using CRAL Wiring Protocol (Section V). Run all five Builder Tests. |
| Writing two structural laws per phase without priority order | The Critic Subagent cannot simultaneously enforce two laws without knowing which takes priority when they conflict. | Write one primary law per phase. If secondary laws are needed, explicitly label primary/secondary and state the conflict resolution rule. |
| Pre-filling the Implication phase from DEP-ENG-006 L3 data | v1.1 architecture. In v1.2, DEP-ENG-006 L3 is the register constraint. M7\_RELATABLE provides the content. | Map M7\_RELATABLE to Implication phase in field\_5b. Update Implication phase spec to reference DEP-ENG-021\[M7\] as primary source. |
| Marking all three psychological adapters as 'PROPOSED' | All three (psych-routing, payload-masking, audience-maturity) are REGISTERED in Adapter Registry v2.0. Marking them PROPOSED leaves inline logic in field\_9 as authoritative. | Update status to REGISTERED. Mark inline logic as 'human-readable reference only — Adapter Registry v2.0 is authoritative.' |

——

Script Generation Skill Type Guide  ·  Version 1.0  ·  March 2026

CCP Engineering Division  ·  Governs all 92+ CCF script skill archetypes