

**CONSCIOUS COACHING PLATFORM**

**CCP Evolution**

**Architecture Report**

*V3.0 — Complete System Architecture*

| 6 Foundational Innovations | 10 Architecture Components | 10 Implementation Imperatives |
| :---: | :---: | :---: |

Dependency Registry v4.0  ·  Adapter Registry v2.0  ·  Design Brief Template Library  ·  Design Brief Builder Engine  
JIT Skill Assembler v2.0  ·  Container Module Library  ·  Fingerprint Archive  ·  Mood State Architecture  ·  Anti-Draft Intelligence

Version 3.0  ·  March 2026  ·  CCP Engineering Division

Supersedes: CCP Evolution Architecture Report V2.0 (March 2026\)

**00  Executive Summary**

The CCP Evolution Architecture Report V3.0 is the definitive system architecture specification for the Conscious Coaching Platform. It supersedes V2.0 by completing what V2.0 theorised: the operational machinery that translates psychological and coaching intelligence into compiled, traceable, self-improving production skills.

V2.0 established six foundational innovations — Client Intelligence Layer, Psychological Routing & Mood State System, Trigger-First Engine, 3-Dimensional Voice DNA, CCSB Two-Phase Architecture, and L3 Context Premise — each with rigorous scientific grounding and MCDA-validated prioritisation. V3.0 accepts all six as resolved architecture and builds the execution engine on top of them.

The central addition is the JIT Skill Compiler: a seven-component system that replaces ad-hoc skill authoring with a compilation pipeline. Every skill is compiled from a formally specified template, carries a unique fingerprint ID, is psychologically routed before assembly, validated by a three-level contrastive anti-draft system before deployment, and scored against production performance to evolve into canonical reference examples over time. The system does not produce content. It produces the optimised instruction engines that produce content — and it improves itself with every production cycle.

Three previously unresolved gaps are closed in this report: (1) The Psychological Routing & Mood State Architecture is now fully operationally wired — every compiled skill receives a Psychological Routing Brief as a mandatory pre-flight input. (2) The Anti-Draft Intelligence Layer is specified in three levels, integrating Contrastive Prompting theory with the production generation flow. (3) The Fingerprint Archive introduces a skill ID schema that links every compiled skill to every content output and every performance signal — closing the learning loop the V2.0 architecture could not yet complete.

| ARCHITECTURAL STATUS — V3.0 All six V2.0 innovations: RESOLVED ARCHITECTURE. JIT Compiler 7-component system: SPECIFICATION COMPLETE. Fingerprint Archive & Skill ID System: SPECIFICATION COMPLETE. Anti-Draft Intelligence Layer: SPECIFICATION COMPLETE. Mood State Architecture end-to-end wiring: SPECIFICATION COMPLETE. Implementation build sequence: DEFINED, 10-step topological order. Pending: execution of steps 1-10. |
| :---- |

**I  The Six Foundational Innovations — V2.0 Architecture, Retained and Extended**

The following six innovations were fully specified in V2.0 and are carried forward without modification in V3.0. Each is restated here for completeness and then shown in its new context within the JIT Compiler system. V3.0 does not revise these innovations — it activates them operationally.

**Innovation 1 — Client Intelligence Layer (MCDA: 4.55)**

The Client Intelligence Layer produces the foundational data that makes every other innovation possible. It operates across three maturity tiers determined by the quality of available input data, and produces three distinct outputs: the Pain Map, the Mood Context Map, and the Live Psychometric Feed.

| Tier | Data Source | Outputs Available | L3 Confidence |
| :---- | :---- | :---- | :---- |
| Tier 1 (\~60% of clients) | Research baseline only — no live data | Pain Map (L1/L2/L3), probabilistic Mood Context Map | \~60% |
| Tier 2 (\~85%) | Zoom session transcripts — LIWC-22 psychometric extraction | Pain Map \+ empirical Mood Context Map \+ Psychometric State Vector | \~85% |
| Tier 3 (100%) | Full CBCS journal logs \+ transcripts \+ sessions | All outputs \+ longitudinal trajectories \+ real-time feed | \~100% |

V3.0 Role: The Client Intelligence Layer feeds DEP-ENG-006 (Context Premise Map), DEP-ENG-016 (Psychological Routing Brief), DEP-ENG-017 (Audience Maturity Profile), and DEP-ENG-018 (Mood Context Map) — four of the eight new DEP IDs formalised in Dependency Registry v4.0. Without Tier 2+ data, psychological routing operates on probabilistic inference rather than empirical confirmation.

*⬡  LIWC-22 (Pennebaker et al., 2022): First-person singular frequency, hedging markers, and negative emotion word density are empirically validated indicators of regulatory orientation and psychological arousal state. They allow the system to infer whether the audience is in a promotion vs. prevention regulatory frame before any batch is compiled.*

**Innovation 2 — Psychological Routing & Mood State System (MCDA: 4.55 — elevated from 4.45)**

The Psychological Routing System classifies every content production decision across four mood states, each grounded in distinct psychological theory. V3.0 elevates its MCDA score from 4.45 to 4.55 — matching the Client Intelligence Layer — because it has been fully operationally wired (see Section V).

| Mood State | Psychological Basis | Arousal × Valence Sub-Spec | SDT Primary Need | TMT Function |
| :---- | :---- | :---- | :---- | :---- |
| Processing Mode | Terror Management Theory \+ Uses & Gratifications (Cognitive) | High-engagement, variable valence | Relatedness | insight\_delivery → worldview\_construction (loyal cohort only) |
| Escape Mode | Mood Management Theory (Zillmann, 1988\) | HIGH/NEG=Stressed→COOLING | LOW/NEG=Depleted→WARMING | HIGH/POS=Energized→CHANNELING | LOW/POS=Content→MAINTENANCE | Relief | maintenance only — no activation |
| Discovery Mode | Broaden-and-Build Theory (Fredrickson) \+ SDT Competence | Medium-high arousal, positive valence expansion | Competence | not applicable |
| Status Mode | Social Comparison Theory (Festinger, 1954\) | Variable arousal, identity-valence dominant | Autonomy | not applicable |

Audience Maturity Lifecycle — the batch allocation percentages that the Smart Mix Synthesis Protocol must honour, updated from behavioural signals not calendar time:

| Cohort | Processing | Escape | Discovery | Status | Depth Permission | TMT Function Allowed |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| New (0-4wk) | 10% | 40% | 30% | 20% | Surface | insight\_delivery only |
| Developing (4-16wk) | 25% | 35% | 20% | 20% | Mid | insight\_delivery |
| Loyal (16wk+) | 50% | 20% | 15% | 15% | Full | worldview\_construction permitted |

*⬡  Mood Management Theory (Zillmann, 1988): Non-conscious affective homeostasis is the dominant driver of media selection. High semantic affinity between content domain and the audience's primary stress domain is actively counterproductive for Escape Mode — the audience came to escape this exact conversation.*

*⬡  Broaden-and-Build (Fredrickson & Joiner, 2002): The upward spiral is empirically documented. Each iteration of broadened thinking increases likelihood of positive affect, which further broadens thinking. The batch composition engine is a neurological training system for audience depth capacity, not just a content calendar.*

**Innovation 3 — Trigger-First Engine Inversion (MCDA: 4.40)**

The Trigger-First architecture inverts the conventional content production flow. TTT (Temperature, Texture, Tone) is never pre-specified in any Design Brief Template. It is the last resolved variable — determined at runtime by the Authentication Certificate (DEP-ENG-005), which reads the coach's live emotional state at production time and certifies the energetic signature.

**Why this matters at the compiler level:** Every compiled SKILL.md contains a TTT Enforcement Rule — a hard constraint that rejects any hardcoded TTT value in Block A or Block B of the Design Brief. The JIT Skill Assembler v2.0 Block C validation will REJECT any brief that arrives with TTT pre-filled. This enforcement is mechanical, not advisory.

*⬡  iRAV Framework (Cooney et al., 2021): Virality is consistently predicted by the intensity of discrete emotional peaks — not average emotional tone. TTT must be determined at the moment of authentic emotional access, not predetermined. Pre-specification produces average tone rather than authentic peaks.*

**Innovation 4 — 3-Dimensional Voice DNA (MCDA: 4.35)**

Voice DNA consists of three formally registered data assets that together define the complete psychological and linguistic signature of a coach, and govern every generation pass in the system.

| Dimension | DEP ID | Description | How It Activates |
| :---- | :---- | :---- | :---- |
| Positive Space Object | DEP-ENG-003 | The authenticated voice — lexical patterns, cognitive fingerprint, emotional cadence, structural tendencies | Loaded by irevc-adapter as primary generation constraint |
| Negative Space Object | DEP-ENG-004 | The forbidden voice — patterns the coach produces under cognitive load, drift into professional register, hedging language | Loaded by negative-space-loader-adapter; forms Level 3 anti-draft input |
| Emotional DNA Object | DEP-LIB-001 / DEP-ENG-006 L3 | The wound architecture — the specific L3 pain experiences that produce authentic emotional transfer | Loaded by psych-routing-adapter for regulatory frame calibration |

*⬡  Linguistic relativity (Whorf-Sapir): The vocabulary structure of a generated script determines the emotional experience of the reader before semantic content is processed. Voice DNA is the instrument that controls this pre-semantic register.*

**Innovation 5 — CCSB Two-Phase Skill Architecture (MCDA: 4.00)**

The CCSB (Content Creation Behavior System) separates the intelligence specification process (Phase 1\) from the content assembly process (Phase 2). V3.0 upgrades Phase 1 to the Design Brief Builder Engine and Phase 2 to the JIT Skill Assembler v2.0, both of which are fully specified in Sections III and IV of this report.

The critical architectural rule that carries forward from V2.0: templates are pure data. All execution authority lives in agents that consume them. No subagents may be embedded inside templates. The CCSB Skill Assembler Agent has sole orchestration authority over adapters during Phase 2\.

**Innovation 6 — L3 Context Premise (MCDA: 3.95)**

The Context Premise is the intelligence layer that bridges raw coaching knowledge (DEP-ENG-006) with the content production pipeline. It has three distinct outputs, each serving a different downstream consumer:

| Output | Name | Consumer | Intelligence Tier Required |
| :---- | :---- | :---- | :---- |
| Output 1 | Pain Map — L1/L2/L3 stratified client pain landscape | Batch Composer (DEP-PROTO-006), all script skills | Tier 1+ |
| Output 2 | Mood Context Map — probability distribution across 4 mood states | Mood Routing Stage 1, Design Brief Builder Engine | Tier 1+ (Tier 2+ recommended) |
| Output 3 | Live Psychometric Feed — LIWC-22 extracted state vectors per cohort | Psychological Routing Brief Generator (DEP-ENG-016) | Tier 2+ only |

**II  The JIT Skill Compiler — Complete System Architecture**

The JIT (Just-In-Time) Skill Compiler is the operational engine of the CCP. It does not produce content directly. It produces the optimised instruction engines — compiled SKILL.md files — that the generation agents (Emilio and others) use to produce content. Every decision about psychological routing, structural procedure, voice calibration, and quality constraints is resolved at compilation time, not generation time. Generation agents follow instructions. The compiler is where intelligence lives.

The system has seven components in strict dependency order. They cannot be built or operated out of sequence. A failure in any foundational layer propagates silently through all layers that depend on it.

**The Seven-Component Dependency Map**

| \# | Component | Role | Depends On | Fails Without |
| :---- | :---- | :---- | :---- | :---- |
| 1 | Dependency Registry v4.0 | Canonical data layer — formal IDs for all inputs any skill can ever consume | None — foundational | All other components reference ghost variables |
| 2 | Adapter Registry v2.0 | Transformation layer — how modules mutate per psychological and domain context | Registry v4.0 for DEP ID references | Adapters invoke undefined resources |
| 3 | Container Module Library | Intelligence layer — ecological adaptations per archetype including Mood State Interaction Matrices | Registry v4.0 \+ Adapter Registry v2.0 | Modules have no adapter wiring; generic reasoning applies |
| 4 | Design Brief Template Library | Specification layer — archetype-invariant Block A \+ compilation metadata per archetype | Module Library (Block A sources modules) | Templates without module intelligence; authoring from scratch |
| 5 | Design Brief Builder Engine | Phase 1 compiler — populates Block B, runs Semantic Affinity Guard, validates Block C | All above \+ DEP-ENG-016/017/018 | Incomplete briefs reach assembler; silent mid-assembly failures |
| 6 | JIT Skill Assembler v2.0 | Phase 2 compiler — assembles skills from validated briefs using registered adapters | All above | Unrecoverable pipeline failures; no diagnostic repair |
| 7 | Fingerprint Archive | Memory layer — links every compiled skill to every output and every performance signal | Assembler v2.0 (produces skill IDs) | No learning loop; performance cannot improve the system |

**The 4-Layer Content Production Equation**

Before any skill is compiled, the Orchestrator must resolve four distinct variables for every batch slot. These are not interchangeable — they operate at different layers of abstraction and must remain separate. Conflation between them is the primary cause of structural mediocrity in AI-generated coaching content.

| Layer | Name | What It Is | Answers | Resolved By |
| :---- | :---- | :---- | :---- | :---- |
| 1 | Viral Framework (22 frameworks) | The strategic WHY — the emotional and psychological mechanism that makes content worth sharing | Why does this content deserve to exist? | DEP-LIB-002 Framework Library |
| 2 | Persuasive Angle (9 angles) | The psychological lens — which emotional lever this specific piece pulls | What emotional lever does it pull? | DEP-LIB-003 Angle Taxonomy |
| 3 | Content Archetype | The structural container — the format shape and its invariant construction laws | What structural shape does it take? | DEP-LIB-008 Archetype Classification Library |
| 4 | TTT Palette | The voice temperature — at what energy and register the coach accesses the piece | At what authentic energy register? | DEP-ENG-005 Authentication Certificate (RUNTIME ONLY) |

| CRITICAL RULE — TTT IS NEVER PRE-FILLED TTT (Temperature, Texture, Tone) is not a field in the Design Brief. It is not a compilation variable. It is a runtime output. The JIT Assembler Block C validation rejects any brief that contains a hardcoded TTT value. The Assembler emits a warning (not a block) if natural affinity range is noted — but even a warning TTT value cannot be treated as a directive by the generation agent. |
| :---- |

**III  Registry Architecture — Dependency Registry v4.0 & Adapter Registry v2.0**

**3.1 Dependency Registry v4.0 — Eight New Registrations**

The Dependency Registry v3.0 contains 38 components across 4 categories. The JIT Compiler requires 8 new registrations to eliminate ghost variable risk across all psychological routing fields that were architecturally specified in V2.0 but never formally registered. The ghost variable principle is absolute: any field in any Design Brief Template that references a data source without a formal DEP ID creates a silent failure condition that no Block C validation can catch.

**New Registrations — Engine Outputs & Raw Data Assets (ENG category)**

| DEP ID | Name | File | Topological Tier | Required By | Status |
| :---- | :---- | :---- | :---- | :---- | :---- |
| DEP-ENG-016 | Psychological Routing Brief | psych\_routing\_brief.json | Tier 1 (derived) | All CCF script skills, Builder Engine | PROPOSED |
| DEP-ENG-017 | Audience Maturity Profile | audience\_maturity.json | Tier 1 (derived) | Batch Composer, Builder Engine, Audience Maturity Adapter | PROPOSED |
| DEP-ENG-018 | Mood Context Map | mood\_context\_map.json | Tier 2 (orchestration) | Mood Routing Stage 1, Builder Engine Step 3 | PROPOSED |
| DEP-ENG-019 | Session Transcript Intelligence | transcript\_intel.json | Tier 2 (orchestration) | Context Premise Output 3 (Live Psychometric Feed) | PROPOSED |
| DEP-ENG-020 | Fingerprint Archive Index | fingerprint\_archive.json | Tier 3 (archive) | All compiled skills, Orchestrator quarantine check | PROPOSED |

**New Registrations — Component Library (LIB category)**

| DEP ID | Name | File | Topological Tier | Required By | Status |
| :---- | :---- | :---- | :---- | :---- | :---- |
| DEP-LIB-008 | Archetype Classification Library | archetype\_psych\_map.yaml | Tier 0 (constant) | Orchestrator routing, all Design Brief Templates | PROPOSED |
| DEP-LIB-009 | Compiled Skill Template Registry | skill\_template\_registry.yaml | Tier 0 (constant) | Design Brief Builder Engine (template load) | PROPOSED |

**New Registrations — Protocols (PROTO category)**

| DEP ID | Name | Enforced By | Required By | Status |
| :---- | :---- | :---- | :---- | :---- |
| DEP-PROTO-011 | Semantic Affinity Guard Protocol | Batch Compiler, Builder Engine Stage 4, Assembler Block C | All Escape Mode script skills | PROPOSED |
| DEP-PROTO-012 | Fingerprint Scoring Protocol | Fingerprint Archive Engine | All compiled skills (post-production) | PROPOSED |
| DEP-PROTO-013 | Anti-Draft Calibration Protocol | Contrastive Anchor Adapter, Deliberation Adapter | All generation-producing skills | PROPOSED |

*⬡  Specification gaming (Krakovna et al., 2022): Systems optimise for specified objectives while violating their spirit when formal constraints are absent. The ghost variable principle directly applies — unregistered data sources allow the assembler to infer or synthesise inputs that should be formally loaded, producing specification-satisfying but intent-violating outputs.*

**3.2 Adapter Registry v2.0 — Three New Psychological Adapters**

The current Adapter Registry contains 5 adapters governing execution structure and reasoning depth. None carry psychological state awareness. The three new adapters in v2.0 are the operational interface between the Psychological Routing Architecture and the skill compilation process — they are how mood states, regulatory frames, and audience maturity levels get compiled into production skills rather than remaining as YAML fields.

| Adapter ID | Tier | Mandatory For | Inputs | Core Function | Scientific Basis |
| :---- | :---- | :---- | :---- | :---- | :---- |
| psych-routing-adapter | Deep/Premium | ALL CCF script skills | DEP-ENG-016 \+ Design Brief field\_3\_context | Translates mood\_state, arousal\_direction, regulatory\_frame, sdt\_need\_primary into specific sentence rhythm rules, empathy marker requirements, hook construction rules, and energy escalation patterns | Regulatory Focus Theory (Higgins, 1997\) \+ SDT (Deci & Ryan, 1985\) |
| payload-masking-adapter | Deep/Premium | All CCF skills with mood\_state ≠ Processing | mood\_state \+ archetype\_id from validated brief | Generates Trojan Horse construction instruction per archetype × mood combination using Excitation Transfer mechanism | Excitation Transfer (Zillmann, 1971\) \+ Mood Management Theory |
| audience-maturity-adapter | Standard | ALL CCF script skills | DEP-ENG-017 \+ audience\_cohort from brief | Translates cohort into depth permission level, TMT function permission, and batch allocation modifier | Broaden-and-Build (Fredrickson, 1998\) \+ TMT (Greenberg et al., 1986\) |

**Payload Masking Adapter — Mode-Specific Construction Rules**

The Payload Masking Adapter's output is the most sophisticated adapter instruction in the system. It operationalises Excitation Transfer differently for each non-Processing mood state:

* **L3 payload arrives as vehicle resolution subtext. Vehicle must function as standalone entertainment — the truth is the punchline, not the lesson. Semantic Affinity Guard activates before this adapter runs. —** Escape Mode

* **L3 payload embedded in the resolution of a counter-intuitive entry point. Audience receives competence reward (cognitive mastery) before emotional payload. —** Discovery Mode

* **L3 truth encoded in the comparison mechanism — what winners understood. Never stated as explicit lesson. Comparison type (upward assimilation / downward / worldview validation) governs the close. —** Status Mode

**IV  Design Brief Architecture — Three-Block Template System**

The Archetype Design Brief Template is the source code of the JIT Compiler. It is not a prompt. It is a formally specified data document with three blocks, each serving a distinct function in the compilation pipeline. The three-block structure is the architectural resolution of the variants-vs-invariants problem: what must stay constant across all compilations of a given archetype (Block A), what must be populated at runtime for each specific use case (Block B), and what must be validated before any assembly begins (Block C).

**Block A — Structural Invariants (Archetype-Invariant, Pre-Filled Once, Never Modified After TESTED)**

| Field | Name | Content Type | Authoring Authority |
| :---- | :---- | :---- | :---- |
| Field 1 | Intent | Procedural mandate \+ Orchestrator routing value | Architecture Review — immutable after TESTED |
| Field 4 | Trigger | Activation condition referencing DEP-ENG-005 | Architecture Review — immutable after TESTED |
| Field 6 | Action | Cognitive verb phrase defining generation mode | Architecture Review — immutable after TESTED |
| Field 7 | Method | Named arc phases with structural laws | Architecture Review — immutable after TESTED |
| Field 8 (Structural) | Structural Modules | Distillation Funnel, Contrastive Anchor, MCDA species with ecological adaptations \+ mandatory adapters | Architecture Review \+ Module Library maintenance |
| Field 9 (Structural) | Structural Constraints | Universal rules \+ graceful\_degradation\_map with DEP criticality tiers | Architecture Review — modified only by registry changes |
| Field 11 (Structural) | Structural Success Criteria | Archetype-invariant quality gates SG-01 through SG-05 | Architecture Review |

**Block B — Compilation Variables (Populated Per Use Case by Design Brief Builder Engine)**

| Field | Name | Key Contents | DEP ID References |
| :---- | :---- | :---- | :---- |
| Field 2 | Target | output\_format, platform, slide\_count, schema\_ref | DEP-ENG-015 |
| Field 3 | Context | coach\_id \+ 8 psychological routing variables (mood\_state, arousal\_direction, valence\_delivery, regulatory\_frame, semantic\_affinity\_risk, sequencing\_dependency, sdt\_need\_primary, tmt\_function) \+ audience\_cohort \+ depth\_permission | DEP-ENG-003/002/LIB-001/ENG-006/007/008 \+ DEP-ENG-016 |
| Field 5 | Inputs | All DEP IDs organised by topological tier (Tier 0 constants → Tier 1 derived → Tier 2 orchestration) \+ proposed new DEP IDs flagged | Full topological stack |
| Field 8 (Psychological) | Psychological Modules | psych-routing-adapter, payload-masking-adapter, audience-maturity-adapter with inline logic until formally registered | DEP-ENG-016/017 |
| Field 9 (Voice) | Voice Constraints | DEP-ENG-004 Negative Space Object \+ semantic affinity guard logic \+ regulatory\_frame\_hook\_rule \+ arousal\_pacing\_rule \+ sdt\_alignment\_rule | DEP-ENG-004, DEP-PROTO-011 |
| Field 10 | Output Artifact | file\_path\_pattern \+ failure\_path \+ procedural\_log requirements | DEP-ENG-020 (fingerprint registration) |
| Field 11 (Psychological) | Psychological Success Criteria | Mood-state-specific quality gates PG-01 through PG-06 \+ SDT alignment gate | DEP-LIB-007 |

**Block C — Compilation Validation Gate (Runs Before Any Assembly Begins)**

Block C is the pre-flight system that prevents invalid briefs from ever reaching the assembler. It runs entirely without generation or token use — it is pure logical verification. A CRITICAL failure in Block C returns a structured rejection JSON to Phase 1 with the specific failed checks. No assembly begins until all CRITICAL checks pass.

| Check | Name | Pass Condition | Failure Behaviour |
| :---- | :---- | :---- | :---- |
| C-01 | DEP Resolution | All CRITICAL tier DEP IDs resolve in registry | REJECT — return structured failure JSON |
| C-02 | Psychological Routing Brief Present | DEP-ENG-016 exists and is populated for this batch slot | REJECT — trigger Brief Generator re-run |
| C-03 | L3 Layer Threshold | DEP-ENG-006 L3 layer ≥ 10% of total context data | REJECT — insufficient intelligence for deployment |
| C-04 | Achievement Story Candidate | DEP-ENG-010 has ≥1 archetype-tagged story passage | REJECT for story archetypes — flag for non-story archetypes |
| C-05 | Authentication Certificate Valid | DEP-ENG-005 passes LIWC-22 validation | REJECT — cannot compile trigger-first skill without authentic voice access |
| C-06 | Semantic Affinity Pre-Check | HIGH affinity \+ Escape Mode \= BLOCK. MEDIUM \+ Escape \= FLAG. | BLOCK: reclassification instruction. FLAG: logged, proceeds. |
| C-07 | TMT/Cohort Alignment | worldview\_construction \+ non-loyal cohort \= DOWNGRADE | Automatic downgrade to insight\_delivery, logged |
| C-08 | TTT Enforcement | No hardcoded TTT value in any Block B field | REJECT — TTT is never a compilation variable |

**V  JIT Skill Assembler v2.0 — Four-Tier Resilient Compilation**

The JIT Skill Assembler v2.0 addresses four structural vulnerabilities in the current CCBS assembler: single point of execution failure, blind repair with no diagnostic logic, no fallback for unregistered adapters, and no pre-flight gate. The v2.0 architecture introduces tier isolation, diagnostic repair classification, and the Deployment Quarantine Rule — a mandatory Orchestrator-level enforcement mechanism that prevents partial skills from ever entering the active pipeline.

**5.1 The Four Failure Modes of the Current Assembler**

| Failure Mode | What Happens | Why It's Silent | Impact |
| :---- | :---- | :---- | :---- |
| Single Point of Execution | Any adapter failure halts the entire pipeline | No section-level isolation — one failure stops everything | 100% pipeline loss for one adapter failure |
| Blind Repair Pass | 'Maximum 1 repair pass' with no diagnosis | Retry runs identical instruction — same failure reoccurs | Quality issues silently degrade to PARTIAL\_MANUAL |
| No Fallback for MANUAL\_ADAPTATION\_REQUIRED | Unregistered adapter outputs gaps in deployed skills | Skill deploys with \[GAP\] placeholders that generation agents skip | Generation agents operate without required constraints |
| No Pre-Flight Gate | Block C validation not run before Step 1 | Missing DEP IDs discovered during assembly — mid-process halt | Wasted assembly cost; no clean rejection at input |

**5.2 The Four-Tier Assembly Architecture**

| INPUT: Validated Design Brief (from Builder Engine) \+ Compilation Request ID ═══════════════════════════════════════════════════════════════ TIER 0 — PRE-FLIGHT (zero generation, zero tokens, pure verification) ═══════════════════════════════════════════════════════════════   Run all Block C validation checks (C-01 through C-08)   Verify all CRITICAL DEP IDs resolve in registry   Verify DEP-ENG-016 (Psych Routing Brief) exists and is populated   Verify DEP-ENG-005 Authentication Certificate passed LIWC-22   FAIL any check → REJECTED status, return diagnostic JSON, DO NOT PROCEED ═══════════════════════════════════════════════════════════════ TIER 1 — MANDATORY ADAPTERS (parallel execution, atomic) ═══════════════════════════════════════════════════════════════   irevc-adapter   negative-space-loader-adapter           ← Load DEP-ENG-004 FIRST   pre-generation-constraints-adapter   graceful-degradation-adapter   psych-routing-adapter                   ← NEW: mandatory for all CCF script skills   audience-maturity-adapter               ← NEW: mandatory for all CCF script skills   FAIL any → HALT with specific adapter diagnostic, DO NOT PROCEED to Tier 2 ═══════════════════════════════════════════════════════════════ TIER 2 — CONDITIONAL ADAPTERS (parallel, fully isolated) ═══════════════════════════════════════════════════════════════   distillation-funnel-adapter     (if in Field 8 modules)   contrastive-anchor-adapter      (if in Field 8 modules)   deliberation-adapter            (if in Field 8 modules)   voice-separation-adapter        (if in Field 8 modules)   payload-masking-adapter         (if mood\_state ≠ Processing)   semiotic-filter-adapter         (if in Field 8 modules)   mcda-adapter                    (if in Field 8 modules)   Unregistered modules → MANUAL\_ADAPTATION\_REQUIRED flag (assembly continues)   Individual adapter failure → flag \+ continue with remaining adapters ═══════════════════════════════════════════════════════════════ TIER 3 — SECTION ASSEMBLY (section-by-section, fully isolated) ═══════════════════════════════════════════════════════════════   Each of 10 SKILL.md sections assembled independently   Section failure → \[MANUAL\_COMPLETION\_REQUIRED: reason\] placeholder   Assembly ALWAYS completes — never halts mid-document ═══════════════════════════════════════════════════════════════ POST-ASSEMBLY — VALIDATION \+ DIAGNOSTIC REPAIR ═══════════════════════════════════════════════════════════════   SG-01 through SG-05: Structural quality gates   PC-01 through PC-05: Psychological quality gates (NEW)   Failure → classified diagnostic repair (max 1 targeted pass per section) OUTPUT: SKILL.md \+ assembly\_report.json   deployment\_status: COMPLETE | PARTIAL\_AUTO | PARTIAL\_MANUAL | REJECTED |
| :---- |

**5.3 Post-Assembly Psychological Quality Gates (PC-01 through PC-05)**

| Gate ID | Name | Pass Condition | Fail → Repair Action |
| :---- | :---- | :---- | :---- |
| PC-01 | Mood State Calibration Injection | psych-routing-adapter output present in Reasoning Architecture section | RERUN psych-routing-adapter with diagnostic context |
| PC-02 | Payload Masking Instruction | Masking instruction present for all non-Processing Mode compilations | RERUN payload-masking-adapter |
| PC-03 | Semantic Affinity Guard | Guard rule present in Negative Space section for Escape Mode skills | REGENERATE Negative Space section |
| PC-04 | Regulatory Frame Hook Rule | Hook engineering rule present in Pre-Generation Constraints section | REGENERATE Constraints section |
| PC-05 | TMT/Cohort Alignment | tmt\_function matches audience\_cohort permission level exactly | ESCALATE\_TO\_MANUAL — requires human review |

**5.4 Diagnostic Repair Protocol**

| Failure Classification | Root Cause | Repair Action | Max Repair Passes |
| :---- | :---- | :---- | :---- |
| Generation quality failure | Output produced but below threshold — too few items, wrong format, wrong depth | REGENERATE\_SECTION with explicit gap noted in instruction | 1 |
| Missing input failure | A CRITICAL DEP ID was absent, empty, or below threshold | ESCALATE\_TO\_MANUAL immediately — cannot synthesise critical inputs | 0 — immediate escalation |
| Adapter output integration failure | Adapter produced output but assembly mapping failed to integrate correctly | RERUN\_ADAPTER with diagnostic context appended | 1 |
| Ontological boundary violation | SKILL.md contains routing logic, agent instructions, or subagent language | REGENERATE\_SECTION with explicit ontological prohibition | 1 |

| DEPLOYMENT QUARANTINE RULE — NON-NEGOTIABLE: No compiled skill may enter the active pipeline without its assembly\_report.json being read by the Orchestrator. If assembly\_status \= PARTIAL\_MANUAL or REJECTED, the skill is QUARANTINED. It cannot be invoked under any circumstance until all MANUAL\_COMPLETION\_REQUIRED sections are resolved and the report is updated to COMPLETE or PARTIAL\_AUTO. This rule is enforced at the Orchestrator level — it is not merely documented in the assembly report. |
| :---- |

**VI  Container Module Library — Archetype Intelligence Infrastructure**

The Container Module Library is the highest-leverage investment in the JIT Compiler system. It is the single location where structural intelligence is encoded. Because modules are referenced by templates and loaded by the assembler, an improvement to any module automatically propagates to every skill compiled using that archetype — without modifying any template, any skill, or any generation instruction. The leverage ratio is: one module update improves all N compilations that reference it, permanently.

**6.1 Archetype Family Taxonomy**

| Family | Archetypes (examples) | Core Structural Law | Psychological Primary Mode |
| :---- | :---- | :---- | :---- |
| Storytelling | Achievement, Transformation, Inspiration, Relief, Surprise | Stakes ceiling \= emotional ceiling of Turn phase. Mechanism must be transferable. | Processing (loyal), Discovery (developing) |
| Listicle | Shocking, Funny Relatable, Nostalgia, Fear-Anxiety, Curiosity, Hope | First item earns the list. Last item earns the read. No item can carry the whole weight. | Escape, Discovery, Status |
| Case Study | Surprising, Inspirational, Relatable, FOMO, Social Proof | Result must be falsifiable. Mechanism must be transferable. Implication must be personalised. | Processing, Discovery |
| Comparison | Shocking, Funny, Surprising, Outrageous, Nostalgia | Delta must be structural not superficial. Resolution must resolve the tension not sidestep it. | Status, Escape, Discovery |
| Myth & Scam | Indignation, Curiosity, Empowering, Fear-Anxiety | The myth must be real and widely held. Debunk with mechanism not opinion. Install new frame. | Processing, Discovery |
| Tier List | Authority, Controversial, Relatable, Nostalgia, Red Flag | Criteria must be stated before verdicts. Hidden criteria \= credibility collapse. | Status, Processing |
| Core Formats | Dopamine Cliff, Relief Peak, Persuasive Tweet | Arc hinge is the structural key. Cannot be telegraphed. Transition timing is everything. | Escape, Processing, Discovery |

**6.2 What Every Container Module Must Contain**

* **The universal structural procedure expressed as named phases with laws. Archetype-invariant. Stored in Block A of every template that uses this archetype. Never modified after STABLE maturity. —** Core DNA Block

* **Explicit instructions for how each of the 4 Distillation Funnel laws (Compression, Distillation, Resonance, Anchoring) mutates for this specific archetype. What does Compression mean for a Tier List vs. an Achievement Story? Domain-specific definitions are required. —** Ecological Adaptation Protocol

* **The precise archetypal failure mode for this archetype — what does generic AI output look like? Must be written as a concrete example (3-5 sentences), not described abstractly. This is the Level 1 Anti-Draft input for every compiled skill using this archetype. —** Contrastive Anchor Calibration

* **How all four mood states change the execution of this specific archetype. Hook engineering, arc modification, payload delivery, and semantic affinity risk — all four specified per mood state. —** Mood State Interaction Matrix

* **The default Trojan Horse construction instruction for this archetype per mood state. Achievement Story in Discovery Mode: counter-intuitive historical success fact. Shocking Listicle in Escape Mode: absurdist premise that makes the L3 truth the punchline. —** Payload Masking Default

* **One complete Block A \+ Block B Design Brief showing a full compilation for a known archetype × mood × coach combination. The 'canonical shot' that anchors assembler quality for this archetype. —** Reference Production Example

**6.3 Mood State Interaction Matrix — Achievement Story Reference**

| Mood State | Hook Engineering | Arc Modification | Payload Delivery | Semantic Affinity Risk | Guard Behaviour |
| :---- | :---- | :---- | :---- | :---- | :---- |
| Processing | Stakes-first, direct L3 entry — no vehicle | Full 5-phase arc; TMT function may activate for loyal cohort | Implication \= direct existential parallel to audience's wound | HIGH — appropriate for this mode | No guard — high affinity is the intent |
| Escape | Vehicle-first (humor/absurdity); Stakes fully buried | Arc compressed into vehicle resolution; vehicle must work as standalone entertainment | Truth arrives as punchline in phase 5 — earned not stated | HIGH — GUARD ACTIVATES | Domain swap required before compilation proceeds |
| Discovery | Counter-intuitive historical fact opens; mechanism as surprise | Stakes revealed through fact resolution | Implication \= competence reward \+ L3 parallel | LOW — entry domain is semantically distant | No guard — low affinity is the design |
| Status | Achievement framed as comparison signal — what this person understood | Mechanism \= what winners know that others don't | Implication \= identity marker, not lesson — never stated as advice | MEDIUM — flag if active stress \= achievement pressure | Flag if DEP-ENG-016 shows achievement domain L3 stress |

*⬡  Social Comparison Theory (Festinger, 1954): Upward assimilation (Status Mode) requires explicit pathway framing or it flips to contrast and produces envy rather than aspiration. The Mood State Interaction Matrix for Status Mode must always specify which comparison type (upward assimilation, downward, worldview validation) is operative — and the construction must match exactly.*

**VII  Fingerprint Archive — Skill ID System and the Learning Loop**

Every compiled skill needs a unique, trackable, human-readable ID that links it to: (1) the archetype template it was compiled from, (2) the psychological context it was compiled for, (3) every content output it produced, and (4) every performance signal those outputs generated. Without this linkage, the system produces skills, observes performance, and has no mechanism to connect a viral piece of content back to the specific compiled skill that generated it. The learning loop does not exist until the Fingerprint Archive exists.

**7.1 The Skill Fingerprint ID Schema**

| SKILL-{ARCH\_ID}-{COACH\_ID}-{MOOD}-{REG\_FRAME}-{COHORT}-{YYYYMMDD}-{SEQ} Component definitions:   ARCH\_ID     \= Archetype identifier  (STORY01, LIST02, CASE03, COMP04, MYTH05, TIER06, CLIFF07 ...)   COACH\_ID    \= Coach short ID — 3-4 chars from coach\_soul.json   MOOD        \= P (Processing)  |  E (Escape)  |  D (Discovery)  |  S (Status)   REG\_FRAME   \= PRO (promotion-focused)  |  PRV (prevention-focused)   COHORT      \= N (new 0-4wk)  |  DEV (developing 4-16wk)  |  L (loyal 16wk+)   YYYYMMDD    \= Compilation date   SEQ         \= Sequential number for same-day compilations of same type Examples:   SKILL-STORY01-EMI-P-PRV-L-20260315-001     Achievement Story / Coach Emilio / Processing Mode / Prevention Frame     Loyal Cohort / March 15 2026 / First compilation of this type that day   SKILL-LIST02-ANA-E-PRO-N-20260315-001     Shocking Listicle / Coach Ana / Escape Mode / Promotion Frame     New Cohort / March 15 2026   SKILL-CLIFF07-MAR-D-PRO-DEV-20260315-001     Dopamine Cliff / Coach Maria / Discovery Mode / Promotion Frame     Developing Cohort / March 15 2026 |
| :---- |

**7.2 The Fingerprint Archive Record — Full Schema**

| {   'skill\_id': 'SKILL-STORY01-EMI-P-PRV-L-20260315-001',   'archetype\_template\_id': 'ARCH-STORY-01',   'archetype\_template\_version': '1.2',   'compilation\_date': '2026-03-15',   'maturity': 'draft',             // draft | tested | stable | reference   'assembly\_status': 'COMPLETE',   // COMPLETE | PARTIAL\_AUTO | PARTIAL\_MANUAL | REJECTED   'context': {     'coach\_id': 'EMI',     'mood\_state': 'Processing',     'arousal\_direction': 'raises',     'regulatory\_frame': 'prevention',     'audience\_cohort': 'loyal',     'tmt\_function': 'worldview\_construction',     'sdt\_need\_primary': 'relatedness',     'semantic\_affinity\_risk': 'high'   },   'dep\_snapshot': {     'DEP-ENG-003': 'hash\_of\_emotional\_dna\_used',     'DEP-ENG-004': 'hash\_of\_negative\_space\_used',     'DEP-ENG-006': 'hash\_of\_context\_premise\_used',     'DEP-ENG-016': 'hash\_of\_psych\_routing\_brief\_used'   },   'outputs': \[\],          // populated when content is produced using this skill   'performance\_scores': {},   'promoted\_to\_stable': false } |
| :---- |

**7.3 Output Linkage — Connecting Skill to Content Performance**

When a compiled skill produces a content output, the output is registered back to the skill's archive record. This is the operational close of the learning loop:

| 'outputs': \[   {     'output\_id': 'OUT-STORY01-EMI-20260316-001',     'content\_title': 'The day I got promoted was the loneliest day of my career',     'platform': 'instagram\_reel',     'published\_date': '2026-03-16',     'performance': {       'saves': 2847,  'shares': 1203,  'comments': 892,       'reach': 147000,  'engagement\_rate': 0.034,       'viral\_quartet\_score': 4.2   // saves \+ shares \+ DM velocity \+ comment depth     },     'audience\_signals': {       'dm\_vulnerability\_ratio': 0.18,       'comment\_depth\_score': 3.4,       'save\_to\_share\_ratio': 2.37     }   } \] |
| :---- |

**7.4 Maturity Promotion Protocol**

| Maturity | Trigger Condition | Plasticity | Modification Rule | Learning Loop Action |
| :---- | :---- | :---- | :---- | :---- |
| Draft | Newly compiled — no production outputs | High — free iteration | Accept breaking changes | None — accumulate outputs |
| Tested | 3+ production outputs without assembly failure | Medium | Changes require written justification | Module Library notes compilation patterns |
| Stable | 10+ outputs across diverse inputs \+ ≥1 high-performer (saves ≥2× category avg) | Low — locked | Structural augmentation only \+ full regression review | Module Library receives calibration update |
| Reference | Stable \+ confirmed as canonical example across ≥2 coaches or ≥2 cohorts | Immutable except by Architecture Review | New version required; old version preserved | Full Block A \+ Block B promoted to Template Library as Reference Example — learning loop closes |

*⬡  SkillNet (Liang et al., 2026): Formalising skills as composable, tracked assets with performance scoring produces 40% agent performance improvement. Self-generated skills without curation produce zero gain. The Fingerprint Archive is the curation mechanism — the difference between a system that learns and one that merely generates.*

*⬡  Agent Skills benchmark (Li et al., 2025): Curated agent skills boost LLM performance by \+16.2 percentage points. The Reference tier promotion is the curation gate that produces this effect.*

**VIII  Anti-Draft Intelligence — Contrastive Prompting as the Production Immune System**

The compiled skill is the final intervention point before content generation. Every architectural decision upstream — client intelligence, psychological routing, trigger-first activation, context premise — can be executed perfectly and still produce mediocre content if the generation agent defaults to statistical mean-reversion at generation time. The LLM's default behaviour is to produce the centroid of all training examples that match the positive instructions. That centroid passes every surface quality check and fails every depth test. Anti-Draft Intelligence is the immune system that prevents this.

Ling et al. (2023) established the Law of the Negative Anchor: providing explicitly generated invalid examples forces semantic repulsion away from mean-reversion. The critical word is generated — described failure modes produce abstract avoidance. Concrete, written failure examples produce measurable semantic distance in subsequent generation.

**8.1 The Three-Level Anti-Draft Architecture**

Every compiled SKILL.md contains three levels of anti-draft intelligence, each targeting a different failure mode:

**Level 1 — Archetype Anti-Draft (from Container Module, Block A — Invariant)**

Answers: what does generic AI output look like for this archetype? Written as concrete example prose in the module and arrives in every compilation unchanged. Targets statistical mean-reversion — the most common and least visible failure mode.

| ACHIEVEMENT STORY — LEVEL 1 ANTI-DRAFT EXAMPLE Generic AI achievement story: 'I worked incredibly hard and never gave up. After months of struggle, I finally achieved my goal. The lesson is that persistence pays off. You can do this too if you believe in yourself.' Why this fails: mechanism is non-transferable (persistence/belief), result is impressionistic not evidential, implication is generic inspiration not personalised parallel. This is the statistical centroid. Maximise distance from every element. |
| :---- |

**Level 2 — Psychological Mode Anti-Draft (from Payload Masking Adapter, Block B — Compilation-Specific)**

Answers: what does the wrong execution of THIS mood state × archetype combination look like? Cannot be pre-written in Block A — it requires the psychological routing context to be meaningful. Generated at compilation time by the payload-masking-adapter.

| ACHIEVEMENT STORY × ESCAPE MODE — LEVEL 2 ANTI-DRAFT EXAMPLE Mode failure: 'I used to hustle myself into the ground. I learned that rest is actually productive. Here's what changed for me...' Why this fails: Topic (hustle culture, achievement anxiety) carries HIGH semantic affinity to primary stress domain. Payload is stated, not earned through vehicle resolution. Vehicle adds emotional weight rather than releasing it. The audience came to escape this exact conversation — this opens the wound it was supposed to soothe. |
| :---- |

**Level 3 — Coach-Specific Anti-Draft (from Voice Separation Adapter \+ DEP-ENG-004, Block B — Coach-Specific)**

Answers: what does THIS specific coach produce when they have the right structure but fall back to their worst patterns? Extracted from DEP-ENG-004 Negative Space Object. The most precise level — catches subtle failures that survive Levels 1 and 2 because they appear stylistically acceptable but miss the voice's authentic register.

| COACH-SPECIFIC ANTI-DRAFT — STRUCTURAL PATTERN Level 3 anti-draft contains: (1) The coach's identified cognitive load drift patterns — what they default to when uncertain. (2) The specific hedging constructions they use in professional register. (3) The vocabulary items that are technically correct but feel performed rather than lived. (4) The structural shortcuts they take when emotional access is shallow. These are extracted from DEP-ENG-004 and written as the Forbidden Vocabulary List in every compiled skill. |
| :---- |

**8.2 The Contrastive Instruction Block**

The three anti-draft levels are assembled into a structured block inside every compiled skill. The generation agent reads this block before generating any output. Four components:

* **The actual bad output text — written as prose, not described. 3-5 sentences of exactly what must not be produced. Making the failure mode concrete activates semantic repulsion; abstract avoidance does not. —** Negative Demonstration

* **One sentence per failure mode identifying the exact constraint violated. Why does each element fail? This trains the generation agent's self-evaluation of its own draft. —** Failure Diagnosis

* **The explicit distance requirement: output must not share vocabulary, structural pattern, or emotional register with the negative demonstration. Maximum distance from statistical mean is the objective, not merely exceeding it. —** Semantic Distance Instruction

* **From DEP-ENG-004 plus mode-specific additions. Exact strings — not general rules. Updated at each compilation with the current batch's psychological context. —** Forbidden Vocabulary List

**8.3 The Draft → Anti-Draft → Synthesis Loop**

The contrastive architecture integrates with the Deliberation Adapter to create a three-pass quality loop for every compiled script skill. This is how the intelligence of the compiled skill is operationalised at generation time:

| ═══════════════════════════════════════ PASS 1 — DRAFT GENERATION ═══════════════════════════════════════   Emilio generates initial script following all positive constraints   Chain-of-Draft reasoning: each logical step ≤5 words before full generation   Deliberation Adapter governs step-count and confidence thresholds   Output: draft\_v1.md ═══════════════════════════════════════ PASS 2 — ANTI-DRAFT EVALUATION (Critic Subagent) ═══════════════════════════════════════   Spawn Critic Subagent with anti-draft block as PRIMARY context   Critic evaluates draft\_v1 against all three anti-draft levels:     Level 1: Is any element of the Archetype Anti-Draft present?     Level 2: Is the psychological mode failure pattern present?     Level 3: Are any coach-specific drift patterns from DEP-ENG-004 present?   Critic also runs structural gates SG-01 through SG-05   Critic also runs psychological gates PG-01 through PG-06   Output: critic\_report.json with flagged elements \+ severity classification ═══════════════════════════════════════ PASS 3 — SYNTHESIS ═══════════════════════════════════════   IF Critic flags ≥2 violations → full regeneration with critic report as constraint   IF Critic flags 1 violation → targeted revision of flagged element only   IF Critic flags 0 violations → confirm draft, proceed to Voice Distiller   Log: deliberation\_override: true/false \+ specific violations resolved   Output: final\_script.md \+ deliberation\_log.json |
| :---- |

**8.4 Chain-of-Draft Reasoning Integration**

Chain-of-Draft (Xu et al., 2025\) is not an optional quality enhancement — it is the mechanism that prevents the generation agent from producing a confident, structurally satisfying, psychologically wrong output. Each reasoning step is constrained to ≤5 words before the full generation, which forces the agent to verify psychological alignment at every structural decision point rather than generating a complete draft and retroactively justifying it.

* Step labelling — every reasoning step must be explicitly tagged (\#\#\# HOOK CONSTRUCTION, \#\#\# STAKES CALIBRATION, \#\#\# TURN TIMING). Structure forces the cognitive behaviour. Flowing prose reasoning allows psychological constraint violations to be skipped.

* Confidence thresholds — the Deliberation Adapter specifies minimum confidence before each major structural phase. If confidence in psychological routing alignment is below threshold at the Hook phase, the draft pauses rather than proceeding on a misaligned foundation.

* Verification gates — psychological routing verification (does this hook serve the correct mood state and regulatory frame?) must pass before narrative stakes are established. Wrong mood state at hook \+ correct arc mechanics \= still a failed skill.

*⬡  Chain-of-Draft (Xu et al., 2025): Intermediate reasoning traces of ≤5 words per step significantly outperform standard Chain-of-Thought on complex tasks while using 80% fewer tokens. The brevity constraint forces reasoning compression — verbose reasoning often hides logical gaps that brief, forced articulation exposes.*

*⬡  Contrastive Chain-of-Thought (Ling et al., 2023): Positive-only examples allow the model to satisfy surface patterns while violating deep constraints. Paired contrastive negatives close this gap — the failure mode must be as specifically generated as the target mode.*

**IX  Mood State Architecture — Complete Operational Wiring**

The Psychological Routing & Mood State Architecture was theorised and academically grounded in V2.0 across seven distinct research frameworks. The gap V2.0 left open was operational wiring: which system reads which data, in what order, with what failure behaviour, and how the routing produces a conflict-resolved compilation trigger. V3.0 closes this gap entirely.

**9.1 The Five-Stage Routing Flow**

| STAGE 1 — MOOD CONTEXT DETECTION   Source: DEP-ENG-018 (Mood Context Map)   Intelligence Tier 1: Probabilistic inference from DEP-ENG-006 contextual signals   Intelligence Tier 2+: Empirical from LIWC-22 transcript analysis (DEP-ENG-019)   Output: Probability distribution across 4 mood states for this batch window   Default if no data: Escape 40% / Discovery 30% / Status 20% / Processing 10%            (New cohort priors — most conservative allocation) STAGE 2 — AUDIENCE MATURITY CLASSIFICATION   Source: DEP-ENG-017 (Audience Maturity Profile)   Input: Engagement depth signals — saves, DMs, comment vulnerability, replay rate   Rule: Behavioural signals override calendar-time thresholds   Output: Cohort classification (new/developing/loyal) \+ batch allocation % STAGE 3 — PSYCHOLOGICAL ROUTING BRIEF GENERATION   Source: DEP-ENG-016 (produced by Design Brief Builder Engine — Step 3\)   Inputs: Stage 1 output \+ Stage 2 output \+ DEP-ENG-006 L3 pain domain data   Output: psych\_routing\_brief.json per batch slot with all 8 routing variables     Fields: mood\_state, arousal\_direction, valence\_delivery, regulatory\_frame,              sdt\_need\_primary, semantic\_affinity\_risk, tmt\_function, audience\_cohort STAGE 4 — SEMANTIC AFFINITY GUARD (DEP-PROTO-011)   Inputs: psych\_routing\_brief.json \+ DEP-ENG-006 active L3 pain domain   Logic:     IF semantic\_affinity\_risk \= HIGH AND mood\_state \= Escape  → BLOCK        Return: affinity\_mode\_conflict \+ reclassification instruction     IF semantic\_affinity\_risk \= HIGH AND mood\_state \= Processing → PERMIT        High affinity is appropriate — this mode is designed for it     IF semantic\_affinity\_risk \= MEDIUM AND mood\_state \= Escape  → FLAG        Proceed with warning logged in routing brief     IF semantic\_affinity\_risk \= LOW (any mood state)  → PERMIT STAGE 5 — COMPILATION TRIGGER   DEP-ENG-016 (validated \+ Guard-cleared) → Design Brief Builder Engine   Builder injects psych\_routing\_brief into Block B field\_3\_context   Block C checks include Guard decision (C-06 Semantic Affinity Pre-Check)   Validated brief → JIT Skill Assembler v2.0   Assembled skill contains fully wired psychological intelligence |
| :---- |

**9.2 The Upward Spiral as Active Platform Strategy**

The Audience Maturity Lifecycle is not passive observation — it is an active neurological training protocol that the batch composition engine executes. Each Escape/Discovery piece that lands successfully builds cognitive capacity for the next Processing Mode piece. The batch engine, when correctly calibrated, trains the audience toward increasing depth over time — it is not just serving them where they are, it is systematically moving them to where they can receive more.

Operational implication: the Fingerprint Archive should track cohort-level progression signals, not just individual skill performance. If a developing cohort is showing loyal-cohort behavioural signals (save rates ≥ loyal baseline, DM vulnerability ratios in loyal range, comment depth scores advancing) before the 16-week calendar threshold, the Audience Maturity Adapter must advance their classification immediately. Calendar time is a weak proxy for behavioural reality.

*⬡  Broaden-and-Build (Fredrickson & Joiner, 2002): The upward spiral is empirically documented — each iteration of broadened thinking increases the probability of positive affect, which further broadens thinking. Applied operationally: the batch composition percentages are not arbitrary allocations — they are the intervention schedule for a documented neurological training effect.*

*⬡  Terror Management Theory (Burke, Martens & Faucher, 2010): When worldview investment activates (loyal cohort, Processing Mode, worldview\_construction function), the audience begins defending the coach's framework as their own worldview. This state produces advocacy, churn resistance, and referral behaviour that no performance-optimisation algorithm can replicate, because it is not an engagement behaviour — it is an identity behaviour.*

**9.3 Trojan Horse / Format-Emotion Collision Architecture**

For non-Processing mood states, the system's most sophisticated psychological manoeuvre is the Trojan Horse construction: the emotional vehicle (format) is chosen for its mood-appropriate surface, while the L3 payload is embedded and arrives through the vehicle's natural resolution rather than through explicit teaching. Two inviolable constraints govern every Trojan Horse construction:

* **The vehicle must function as standalone entertainment, humour, or inspiration. If the Trojan Horse only makes sense in hindsight (once the payload is visible), it has failed as a vehicle. The audience must choose to watch/read/engage for the vehicle's own value. —** Constraint 1 — Vehicle Independence

* **The payload must arrive through the vehicle's natural resolution mechanism — not appended to it. Appended payloads are structurally detectable. The audience experiences them as a bait-and-switch. The payload must be the punchline, not the lesson added after the punchline. —** Constraint 2 — Resolution-Native Payload

*⬡  Zillmann Excitation Transfer (1971): Residual physiological arousal from an initial high-affect stimulus (humour, surprise) is misattributed to the emotional response triggered by the subsequent stimulus (the L3 payload). The amplification is neurological, not stylistic. The vehicle must produce genuine physiological arousal — performed or mechanical humour does not produce the transfer effect.*

**X  MCDA Evaluation — V3.0 Architecture Scoring**

The Multi-Criteria Decision Analysis framework used in V2.0 is updated to reflect the operational completeness of V3.0. Scores are evaluated across five dimensions: Strategic Leverage (compounding ROI across the system), Operational Necessity (how much the system breaks without this component), Psychological Validity (scientific grounding strength), Implementation Feasibility (reversibility and cost of building), and Learning Loop Contribution (does it help the system improve itself).

**V3.0 MCDA Scores — All Architecture Components**

| Innovation | Score | Primary Driver | Key Scientific Basis |
| :---- | :---: | :---- | :---- |
| **Client Intelligence Layer** | **4.55** | *Tier 3 data unlocks 100% accuracy for all downstream routing* | *LIWC-22 (Pennebaker, 2022), UGT (Katz, 1973\)* |
| **Psychological Routing & Mood State System** | **4.55** | *Operationally wired in V3.0 — elevated from 4.45* | *MMT (Zillmann, 1988), RFT (Higgins, 1997\)* |
| **Trigger-First Engine Inversion** | **4.40** | *TTT enforcement makes every skill psychologically alive* | *iRAV (Cooney, 2021), emotional peaks → virality* |
| **3-Dimensional Voice DNA** | **4.35** | *Anti-draft Level 3 is impossible without DEP-ENG-004* | *Linguistic relativity (Whorf-Sapir), voice transfer* |
| **Container Module Library** | **4.30** | *NEW — highest leverage: one update improves all compilations* | *SkillNet (Liang, 2026), SkillFactory (Deng, 2025\)* |
| **Anti-Draft Intelligence Layer** | **4.25** | *NEW — immune system against statistical mean-reversion at generation* | *Contrastive CoT (Ling, 2023), SteerEval (Xu, 2025\)* |
| **JIT Skill Assembler v2.0** | **4.15** | *NEW — four-tier isolation eliminates single-point failure* | *Evolving PSN (Shi, 2025), 84.6% vs 68.75% success* |
| **Fingerprint Archive & Skill ID System** | **4.10** | *NEW — closes the learning loop; without it, no compounding* | *SkillNet \+40% performance with tracked skills* |
| **CCSB Two-Phase Architecture** | **4.00** | *Separates intelligence specification from content assembly* | *SkillFactory self-distillation (Deng, 2025\)* |
| **Design Brief Builder Engine** | **3.95** | *NEW — without it, incomplete briefs reach assembler silently* | *Specification gaming prevention (Krakovna, 2022\)* |
| **L3 Context Premise** | **3.95** | *Foundation for all routing; quality ceiling for all outputs* | *TMT (Greenberg, 1986), pain-transfer research* |
| **Design Brief Template Library** | **3.80** | *Codifies invariant archetype intelligence — stops re-authoring* | *Institutional knowledge formalisation* |

**Score Movement from V2.0 to V3.0**

| Component | V2.0 Score | V3.0 Score | Reason for Change |
| :---- | :---- | :---- | :---- |
| Client Intelligence Layer | 4.55 | 4.55 | Maintained — foundational data layer unchanged |
| Psychological Routing & Mood State System | 4.45 | 4.55 | Elevated — fully operationally wired in V3.0; no longer theoretical |
| Trigger-First Engine Inversion | 4.40 | 4.40 | Maintained — implementation unchanged |
| 3-Dimensional Voice DNA | 4.35 | 4.35 | Maintained — architecture unchanged |
| Container Module Library | Not scored | 4.30 | New in V3.0 — highest leverage single investment in system |
| Anti-Draft Intelligence Layer | Not scored | 4.25 | New in V3.0 — closes final quality gap at generation |
| JIT Skill Assembler v2.0 | Part of CCSB (4.00) | 4.15 | Separated and elevated — resilience architecture adds distinct value |
| Fingerprint Archive & Skill ID | Not scored | 4.10 | New in V3.0 — learning loop enabler |
| CCSB Two-Phase Architecture | 4.00 | 4.00 | Maintained — now expressed as Builder \+ Assembler pair |
| L3 Context Premise | 3.95 | 3.95 | Maintained |

**XI  Implementation Imperatives — Ten Non-Negotiable Rules**

The ten imperatives below govern the implementation and ongoing operation of the CCP JIT Compiler system. They are not guidelines or recommendations — they are architectural laws. Violating any one of them produces a specific failure mode that is documented against it. The PRD v2.0 update must incorporate all ten.

| \# | Imperative | Violation Consequence | Priority |
| :---- | :---- | :---- | :---- |
| 1 | Every field in every Design Brief Template that references a data source MUST have a formal DEP ID. No template may reach TESTED maturity with unregistered input references. | Ghost variable execution — adapters synthesise inputs that should be formally loaded, producing specification-satisfying but intent-violating skills | CRITICAL |
| 2 | TTT (Temperature, Texture, Tone) is NEVER a compilation variable. Any Design Brief containing a hardcoded TTT value is REJECTED by Block C. | Compiled skills become emotionally static — average tone rather than authentic peaks. iRAV virality prediction mechanism collapses. | CRITICAL |
| 3 | No compiled skill may deploy without its assembly\_report.json being read by the Orchestrator. PARTIAL\_MANUAL and REJECTED skills are QUARANTINED. | Partial skills deploy with gap placeholders. Generation agents skip constraints and produce unguided outputs. | CRITICAL |
| 4 | The Semantic Affinity Guard (DEP-PROTO-011) must run before every Escape Mode compilation. HIGH affinity \+ Escape Mode \= BLOCK — no exceptions. | Escape Mode content directly amplifies active stress. Mood Management Theory homeostasis mechanism reverses — content causes harm rather than relief. | CRITICAL |
| 5 | The CCF pipeline must include the 5-Stage Mood Routing Flow as a mandatory pre-generation stage. No batch slot receives a compilation trigger without a validated DEP-ENG-016. | Psychological routing operates on architectural defaults rather than actual audience state. All subsequent adaptation is built on inference. | HIGH |
| 6 | The Smart Mix Synthesis Protocol (DEP-PROTO-006) must read from DEP-ENG-017 Audience Maturity Profile and enforce cohort-specific batch allocation before assembling any batch. | Audience receives wrong depth/mode ratio for their cognitive capacity. Upward spiral training effect does not occur. TMT investment never builds. | HIGH |
| 7 | Module Library modules are IMMUTABLE after reaching STABLE maturity. New scientific findings must be implemented as module augmentations, not modifications to the stable core. | Evolving PSN oscillatory regression — converged modules regress when modified by downstream update pressure. Stability enables compounding. | HIGH |
| 8 | The Fingerprint Archive must be updated before production compilations begin (Step 9 in build sequence). Performance data must be registered within 48 hours of publication. | Learning loop is never closed. Reference-tier promotion cannot occur. The system produces skills in isolation rather than improving itself. | HIGH |
| 9 | The Anti-Draft Instruction Block must contain all three levels (Archetype, Mode, Coach-Specific). A compiled skill missing any level is PARTIAL\_AUTO at best — not COMPLETE. | Statistical mean-reversion at generation is not caught at compilation level. Level 3 coach-specific drift patterns survive into production outputs. | HIGH |
| 10 | DEP-LIB-008, DEP-LIB-009, and all three new PROTO registrations must be completed and verified before any Design Brief Template is authored. The registries are foundational — they are never downstream of templates. | Templates reference unregistered resources. Block C cannot validate what the registry cannot confirm. The pre-flight gate has no ground truth. | CRITICAL |

**XII  Implementation Build Sequence — Topological Order**

The seven JIT Compiler components plus three supporting infrastructure elements must be built in strict topological order. The sequence below honours all dependency relationships — nothing that references a component is built before that component exists. This is the critical path discipline that prevents the most common agentic system failure: building creative work on top of an incomplete data foundation.

| Step | Build Target | Unblocks | Effort | Why This Step First |
| :---- | :---- | :---- | :---- | :---- |
| 1 | Dependency Registry v4.0 — 8 new DEP IDs \+ updated topological sort | Everything. Ghost variable prevention is the precondition for all other work. | ½ day | No template, adapter, or protocol can be formally validated without its DEP IDs existing. |
| 2 | Adapter Registry v2.0 — 3 psychological adapters formally registered | Assembler v2.0, all CCF compiled skills | 1 day | Adapters must exist in the registry before the Assembler can invoke them. Consumer cannot pre-exist the resource. |
| 3 | DEP-PROTO-011 Semantic Affinity Guard — formal protocol definition | Builder Engine Stage 4, all Escape Mode skills | ½ day | Guard must be formally defined before any Escape Mode brief can pass Block C check C-06. |
| 4 | DEP-LIB-008 Archetype Classification Library — 8-variable YAML for all 22+ archetypes | Orchestrator routing, all Design Brief Templates, Builder Engine | 2 days | This is the routing database. Templates reference it. Must pre-exist every template. |
| 5 | Container Module Library — all archetype families (7 families, 30+ archetypes) including Mood State Interaction Matrices | Design Brief Templates, Assembler Tier 3 section assembly | 3-4 days | Highest leverage investment. Module quality compounds across all compilations that reference the module. |
| 6 | Design Brief Template Library — full three-block templates for all archetypes using completed modules | Design Brief Builder Engine | 2 days | Templates consume modules. Modules must pre-exist templates. |
| 7 | Design Brief Builder Engine — 5-step Phase 1 compiler with psychological routing brief generator | JIT Assembler v2.0 | 2 days | Builder produces validated briefs the Assembler consumes. |
| 8 | JIT Skill Assembler v2.0 — 4-tier resilient compiler with diagnostic repair and Deployment Quarantine Rule | All compiled skill production | 2 days | Assembler consumes validated briefs and adapters. Both must pre-exist. |
| 9 | Fingerprint Archive Engine — ID schema \+ DEP-ENG-020 \+ scoring protocol \+ output linkage | Performance learning loop | 1 day | Must be active before first production compilation. Archive cannot be backfilled. |
| 10 | First production compilations — pilot: 2 archetypes × 2 coaches × 4 mood states \= 16 skills | Full pipeline validation \+ Reference tier promotion pipeline | Ongoing | Online validation. Skills deployed, performance tracked, maturity promoted, Reference Examples fed back to Template Library. |

| Steps 1 → 2 → 3 → 4 are the CRITICAL PATH. No creative work (modules, templates, builder, assembler) can reach production quality until the four foundational registries are complete and correct. Beginning creative work before the data layer is clean produces technically impressive work that references variables that do not formally exist — the most expensive failure mode in the system. |
| :---- |

——

**CCP Evolution Architecture Report**

Version 3.0  ·  March 2026

*Supersedes V1.0 (March 2026\) and V2.0 (March 2026\)*

CCP Engineering Division  ·  Confidential